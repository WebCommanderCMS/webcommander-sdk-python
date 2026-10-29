"""Where an access token lives between calls."""

from __future__ import annotations

import copy
import hashlib
import json
import logging
import os
import sys
import tempfile
import threading
import time
import warnings
from abc import ABC, abstractmethod
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import portalocker

from webcommander.errors import (
    DegradedTokenLockWarning,
    SdkConfigError,
    SdkError,
    SdkTokenCacheError,
    SdkTokenLockError,
)

DEFAULT_TOKEN_CACHE_FILENAME = "wc_python_token.json"

MAX_TOKEN_CACHE_BYTES = 4 * 1024 * 1024

_LOCK_SUFFIX = ".lock"
_LOCK_TIMEOUT_SECONDS = 30
_LOCK_POLL_SECONDS = 0.05
_DEFAULT_NAMESPACE = "default"
_REPLACE_RETRY_ATTEMPTS = 5
_REPLACE_RETRY_INITIAL_SECONDS = 0.01

_LOGGER = logging.getLogger("webcommander.auth.token_store")


class _PathGuard:
    """The in-process half of the lock for one cache path, shared by every store pointed at it."""

    __slots__ = ("lock", "depth", "degradation_reported")

    def __init__(self) -> None:
        self.lock = threading.RLock()
        self.depth = 0
        #: Whether the current run of refusals has already been announced.
        self.degradation_reported = False


_PROCESS_GUARDS: dict[str, _PathGuard] = {}
_PROCESS_GUARDS_LOCK = threading.Lock()


def _resolved_target(file_path: str) -> Path:
    return Path(os.path.realpath(str(file_path)))


def _guard_for(path: Path) -> _PathGuard:
    key = os.path.normcase(str(path))
    with _PROCESS_GUARDS_LOCK:
        guard = _PROCESS_GUARDS.get(key)
        if guard is None:
            guard = _PathGuard()
            _PROCESS_GUARDS[key] = guard
        return guard


def build_credentials_namespace(
    base_url: str,
    client_id: str,
    client_secret: str = "",
    auth_string: str = "",
    grant_type: str = "",
) -> str:
    """Fingerprint a set of credentials as a short, stable key for a shared token file."""
    material = "".join(
        f"{len(value)}:{value}"
        for value in ("v3", base_url, client_id, client_secret, auth_string, grant_type)
    )
    digest = hashlib.sha256(material.encode("utf-8"))
    return digest.hexdigest()[:16]


def build_default_token_cache_path(
    filename: str = DEFAULT_TOKEN_CACHE_FILENAME,
) -> str:
    """Return the conventional per-user cache path for this platform, creating the directory
    if missing, so tokens stay out of the working directory."""
    if sys.platform == "win32":
        root = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    elif sys.platform == "darwin":
        root = os.path.join(os.path.expanduser("~"), "Library", "Caches")
    else:
        root = os.environ.get("XDG_CACHE_HOME") or os.path.join(os.path.expanduser("~"), ".cache")
    if not os.path.isabs(root):
        # No home to expand leaves a literal ``~``, which would put a refresh token in the cwd.
        root = tempfile.gettempdir()
    directory = Path(root) / "webcommander"
    directory.mkdir(parents=True, exist_ok=True)
    _restrict_to_owner(directory)
    return str(directory / filename)


def _restrict_to_owner(path: Path) -> None:
    """Best-effort ``0600``/``0700`` so only this user can read the tokens; a no-op on
    Windows, where inherited NTFS ACLs govern instead."""
    try:
        os.chmod(path, 0o700 if path.is_dir() else 0o600)
    except (OSError, NotImplementedError):
        pass


class TokenStore(ABC):
    """Interface for token persistence and refresh coordination."""

    @abstractmethod
    def read_token_record(self) -> dict[str, Any] | None:
        """Return the stored token, or ``None`` when absent; a present but unusable store raises."""

    @abstractmethod
    def write_token_record(self, record: dict[str, Any]) -> None:
        """Persist a token, replacing whatever was there."""

    @abstractmethod
    def clear_token_record(self) -> None:
        """Discard the stored token. A no-op when there is none."""

    @abstractmethod
    @contextmanager
    def acquire_token_refresh_lock(self) -> Iterator[None]:
        """Hold the refresh lock for the block, so one worker fetches and others wait."""


class MemoryTokenStore(TokenStore):
    """In-process token storage, isolated per instance."""

    def __init__(self) -> None:
        self._record: dict[str, Any] | None = None
        self._lock = threading.RLock()

    def read_token_record(self) -> dict[str, Any] | None:
        """A deep copy of the stored token, or ``None``, so editing it cannot change the store."""
        with self._lock:
            return copy.deepcopy(self._record) if self._record else None

    def write_token_record(self, record: dict[str, Any]) -> None:
        """Store a deep copy of a token, parting from the caller's mapping here."""
        with self._lock:
            self._record = copy.deepcopy(record)

    def clear_token_record(self) -> None:
        """Forget the stored token."""
        with self._lock:
            self._record = None

    @contextmanager
    def acquire_token_refresh_lock(self) -> Iterator[None]:
        """Serialise refreshes across threads in this process."""
        with self._lock:
            yield


class FileTokenStore(TokenStore):
    """Token storage in a JSON file, safe to share across processes."""

    def __init__(self, file_path: str, namespace: str | None = None) -> None:
        self._path = _resolved_target(file_path)
        self._lock_path = Path(str(self._path) + _LOCK_SUFFIX)
        self._namespace = namespace or _DEFAULT_NAMESPACE
        # Per path, not per instance: see :class:`_PathGuard`.
        self._guard = _guard_for(self._path)
        if not self._path.parent.exists():
            try:
                self._path.parent.mkdir(parents=True, exist_ok=True)
            except OSError as error:
                raise SdkConfigError(
                    "token_cache_path: its directory could not be created; pass a path "
                    "whose parent exists, or None to keep the token in memory",
                    detail=f"the directory for {self._path}: {error.strerror or error}",
                    cause=error,
                ) from None

    def read_token_record(self) -> dict[str, Any] | None:
        """Read this store's namespace, or ``None`` when the file holds no entry for it; a corrupt
        or unreadable file raises :class:`~webcommander.errors.SdkTokenCacheError`."""
        with self._guard.lock:
            entry = self._read_all_namespaces().get(self._namespace)
            return dict(entry) if isinstance(entry, dict) else None

    def write_token_record(self, record: dict[str, Any]) -> None:
        """Write the token atomically, leaving other namespaces intact."""
        with self.acquire_token_refresh_lock():
            stored = self._read_all_namespaces()
            stored[self._namespace] = dict(record)
            self._write_all_namespaces(stored)

    def _write_all_namespaces(self, stored: dict[str, Any]) -> None:
        with self._guard.lock:
            handle, temporary_path = tempfile.mkstemp(
                dir=str(self._path.parent), prefix=self._path.name, suffix=".tmp"
            )
            try:
                with os.fdopen(handle, "w", encoding="utf-8") as stream:
                    json.dump(stored, stream)
                self._replace_the_token_file(temporary_path)
                _restrict_to_owner(self._path)
            except BaseException:
                try:
                    os.unlink(temporary_path)
                except OSError:
                    pass
                raise

    def _replace_the_token_file(self, temporary_path: str) -> None:
        """Move the written temporary file into place, retrying on Windows, where another process
        merely reading the file makes ``os.replace`` fail; bounded, the last failure raised."""
        for attempt in range(_REPLACE_RETRY_ATTEMPTS):
            try:
                os.replace(temporary_path, self._path)
                return
            except PermissionError:
                if sys.platform != "win32" or attempt == _REPLACE_RETRY_ATTEMPTS - 1:
                    raise
                time.sleep(_REPLACE_RETRY_INITIAL_SECONDS * (2**attempt))

    def clear_token_record(self) -> None:
        """Drop this store's entry, leaving other instances' tokens alone."""
        with self.acquire_token_refresh_lock():
            stored = self._read_all_namespaces()
            if stored.pop(self._namespace, None) is None:
                return
            if stored:
                self._write_all_namespaces(stored)
            else:
                try:
                    self._path.unlink()
                except FileNotFoundError:
                    pass
                except OSError as failure:
                    # A usable token is still on disk, so a success here would fake a revocation.
                    raise SdkError(
                        "the token cache file could not be deleted",
                        detail=f"{self._path}: {failure.strerror or failure}",
                        cause=failure,
                    ) from None

    def _read_all_namespaces(self) -> dict[str, Any]:
        try:
            content = self._read_within_the_cap()
        except FileNotFoundError:
            return {}
        except ValueError as error:
            raise self._refuse_the_cache_file("is not UTF-8 text", error) from None
        except OSError as error:
            raise self._refuse_the_cache_file("could not be read", error) from None
        if not content.strip():
            return {}
        try:
            stored = json.loads(content)
        except (ValueError, RecursionError) as error:
            raise self._refuse_the_cache_file("does not hold valid JSON", error) from None
        if not isinstance(stored, dict):
            raise self._refuse_the_cache_file(
                f"holds a JSON {type(stored).__name__} where an object of credential "
                f"namespaces was expected",
                None,
            )
        return stored

    def _read_within_the_cap(self) -> str:
        """The cache file's text, read to one byte past :data:`MAX_TOKEN_CACHE_BYTES` and no
        further — enough to know the file is too big without holding it."""
        with self._path.open("rb") as handle:
            raw = handle.read(MAX_TOKEN_CACHE_BYTES + 1)
        if len(raw) > MAX_TOKEN_CACHE_BYTES:
            raise self._refuse_the_cache_file(
                f"is larger than the {MAX_TOKEN_CACHE_BYTES}-byte ceiling this SDK reads "
                f"it to, so it was not loaded",
                None,
            )
        return raw.decode("utf-8")

    def _refuse_the_cache_file(self, problem: str, error: Exception | None) -> SdkTokenCacheError:
        """The one refusal for an unusable cache file, naming what is wrong and what to do."""
        native = ""
        if error is not None:
            # ``strerror`` before ``str`` for an ``OSError``: the latter repeats the path.
            native = f": {getattr(error, 'strerror', None) or error}"
        return SdkTokenCacheError(
            f"the token cache {problem}; repair it or pass token_cache_path=None",
            detail=f"{self._path}{native}",
            cause=error,
        )

    @contextmanager
    def acquire_token_refresh_lock(self) -> Iterator[None]:
        """Serialise refreshes across threads and processes, failing closed with a lock error.
        Reentrant per file: the OS lock is taken at the outermost level and the depth counted."""
        with self._guard.lock:
            if self._guard.depth > 0:
                with self._nested_in_the_held_lock():
                    yield
                return

            try:
                self._lock_path.parent.mkdir(parents=True, exist_ok=True)
                lock_handle = open(self._lock_path, "a", encoding="utf-8")
            except OSError as error:
                raise self._refuse_the_lock(
                    "the lock file could not be opened",
                    detail=f"{self._lock_path}: {error.strerror or error}",
                    cause=error,
                ) from None

            with lock_handle:
                if not self._lock_sidecar(lock_handle):
                    raise self._refuse_the_lock(
                        f"another process held the lock for longer than {_LOCK_TIMEOUT_SECONDS}s"
                    )
                # Re-armed, so a condition that recurs after a recovery is announced again.
                self._guard.degradation_reported = False
                self._guard.depth += 1
                try:
                    yield
                finally:
                    self._guard.depth -= 1
                    portalocker.unlock(lock_handle)

    def _refuse_the_lock(
        self,
        reason: str,
        *,
        detail: str | None = None,
        cause: BaseException | None = None,
    ) -> SdkTokenLockError:
        """Record the condition, announce it once per run of refusals, and return the refusal."""
        refusal = SdkTokenLockError(
            f"the token cache could not be locked: {reason}",
            detail=detail or str(self._path),
            cause=cause,
        )
        if self._guard.degradation_reported:
            return refusal
        _LOGGER.warning("%s", refusal.message)
        warnings.warn(refusal.message, DegradedTokenLockWarning)
        # After the warning, which may raise as an error; latched first, later ones would be silent.
        self._guard.degradation_reported = True
        return refusal

    def _lock_sidecar(self, lock_handle: Any) -> bool:
        """Take the OS lock on the sidecar by polling ``LOCK_NB``; ``False`` past the deadline."""
        deadline = time.monotonic() + _LOCK_TIMEOUT_SECONDS
        while True:
            try:
                portalocker.lock(lock_handle, portalocker.LOCK_EX | portalocker.LOCK_NB)
                return True
            except portalocker.exceptions.BaseLockException:
                if time.monotonic() >= deadline:
                    return False
                time.sleep(_LOCK_POLL_SECONDS)

    @contextmanager
    def _nested_in_the_held_lock(self) -> Iterator[None]:
        """Count the nesting depth and yield, without taking the OS file lock again."""
        self._guard.depth += 1
        try:
            yield
        finally:
            self._guard.depth -= 1
