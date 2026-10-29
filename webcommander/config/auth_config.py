"""Who you are and which instance you are talking to."""

from __future__ import annotations

import os
from dataclasses import dataclass, fields, replace
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from webcommander.auth.token_store import (
    DEFAULT_TOKEN_CACHE_FILENAME,
    build_default_token_cache_path,
)
from webcommander.errors import SdkConfigError
from webcommander.redaction import redact_fields, redact_text

DEFAULT_CLIENT_NAME = "default"
DEFAULT_GRANT_TYPE = "client_credentials"

REQUIRED_FIELDS = (
    "base_url",
    "client_id",
    "client_secret",
    "redirect_uri",
    "auth_string",
)

_TEXT_FIELDS = REQUIRED_FIELDS + ("client_name", "grant_type")


class _UseDefaultTokenCache:
    """Sentinel: resolve the platform's per-user cache path."""

    def __repr__(self) -> str:
        return "<platform default>"


#: Default ``token_cache_path``: the platform per-user cache; ``None`` keeps it in memory.
USE_DEFAULT_TOKEN_CACHE = _UseDefaultTokenCache()


@dataclass(frozen=True, repr=False)
class AuthConfig:
    """Credentials for one WebCommander instance."""

    base_url: str
    client_id: str
    client_secret: str
    redirect_uri: str
    auth_string: str
    # Required, and sixth: callers pass the five credentials above positionally.
    client_name: str

    grant_type: str = DEFAULT_GRANT_TYPE
    token_cache_path: Any = USE_DEFAULT_TOKEN_CACHE

    def __post_init__(self) -> None:
        object.__setattr__(self, "base_url", _normalise_base_url(self.base_url))
        object.__setattr__(self, "token_cache_path", snapshot_a_path(self.token_cache_path))
        # Validated first: resolving the sentinel creates a directory a bad config should not leave.
        self._validate()
        if isinstance(self.token_cache_path, _UseDefaultTokenCache):
            try:
                resolved = build_default_token_cache_path(DEFAULT_TOKEN_CACHE_FILENAME)
            except OSError as error:
                raise SdkConfigError(
                    f"instance {self.client_name}: token_cache_path: the default "
                    f"cache directory could not be created; pass a path, or None to "
                    f"keep the token in memory",
                    detail=str(error),
                    cause=error,
                ) from None
            object.__setattr__(self, "token_cache_path", resolved)

    def _validate(self) -> None:
        problems: list[str] = []

        # Types before values, since a value check on a wrong type raises bare.
        mistyped: set[str] = set()
        for name in _TEXT_FIELDS:
            value = getattr(self, name)
            if value is not None and not isinstance(value, str):
                mistyped.add(name)
                problems.append(f"{name}: expected a string, got {type(value).__name__}")

        missing = [
            name
            for name in REQUIRED_FIELDS
            if name not in mistyped and not str(getattr(self, name) or "").strip()
        ]
        if missing:
            problems.append("missing required values: " + ", ".join(missing))

        if self.base_url and "base_url" not in mistyped:
            problems.extend(_problems_with_the_base_url(self.base_url))

        for name in ("client_name", "grant_type"):
            if name not in mistyped and not str(getattr(self, name) or "").strip():
                problems.append(f"{name}: must not be blank")

        if not isinstance(self.token_cache_path, (str, _UseDefaultTokenCache, type(None))):
            problems.append(
                f"token_cache_path: expected a path or None, got {self.token_cache_path!r}"
            )
        elif isinstance(self.token_cache_path, str) and not self.token_cache_path.strip():
            problems.append(
                "token_cache_path: must not be blank — pass None to keep the "
                "token in memory, or a path to cache it"
            )
        elif isinstance(self.token_cache_path, str) and Path(self.token_cache_path).is_dir():
            problems.append(
                f"token_cache_path: {self.token_cache_path!r} is an "
                f"existing directory, so nothing could be written to it — pass the "
                f"file to write, or None to keep the token in memory"
            )

        if problems:
            # Stripped and ``str``-wrapped: a mistyped name reaches here too.
            label = str(self.client_name or "").strip() or "<unnamed>"
            raise SdkConfigError(f"instance {label}: " + "; ".join(problems))

    def with_overrides(self, **changes: Any) -> "AuthConfig":
        """Derive a new validated set of credentials, leaving this one untouched."""
        unknown = set(changes) - {field.name for field in fields(self)}
        if unknown:
            raise SdkConfigError(f"unknown auth field(s): {', '.join(sorted(unknown))}")
        return replace(self, **changes)

    def __repr__(self) -> str:
        """Return a ``repr`` safe to log, with credentials redacted."""
        shown = redact_fields(self, [field.name for field in fields(self)])
        return f"AuthConfig({', '.join(shown)})"


def snapshot_a_path(value: Any) -> Any:
    """Decode an ``os.PathLike`` to text once, so the stored path cannot change after
    construction. Anything else is handed straight back for ``_validate`` to judge."""
    if not isinstance(value, os.PathLike):
        return value
    try:
        return os.fsdecode(value)
    except (TypeError, ValueError):
        # A ``__fspath__`` that answers with the wrong type; reported as a type problem.
        return value


def _normalise_base_url(raw_value: Any) -> Any:
    """Trim a base URL; a value of the wrong type goes back for ``_validate`` to report."""
    if not isinstance(raw_value, str):
        return raw_value
    return raw_value.strip().rstrip("/")


def _problems_with_the_base_url(base_url: str) -> list[str]:
    try:
        parsed = urlparse(base_url)
    except ValueError as error:
        return [f"base_url: is not a URL ({error})"]
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return [
            f"base_url: must start with http:// or https:// and include a host, "
            f"got {redact_text(base_url)!r}"
        ]
    problems = []
    if parsed.username is not None or parsed.password is not None:
        # Not echoed: it holds a password.
        problems.append(
            f"base_url: host {parsed.hostname} carries embedded credentials, which "
            f"would replace the bearer token; strip the userinfo"
        )
    if parsed.query or parsed.fragment or parsed.params:
        # Paths are concatenated, so anything after the host lands inside the query.
        problems.append(
            "base_url: must be the instance origin only, with no query string or "
            f"fragment, got {redact_text(base_url)!r}"
        )
    return problems
