"""Immutable SDK configuration — how the SDK behaves."""

from __future__ import annotations

import json
import os
import re
import reprlib
from dataclasses import MISSING, dataclass, fields, replace
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from webcommander.config.auth_config import AuthConfig, snapshot_a_path
from webcommander.errors import SdkConfigError, SdkUsageError
from webcommander.http.retry_policy import (
    DEFAULT_BACKOFF_MAX_SECONDS,
    DEFAULT_BACKOFF_SECONDS,
    DEFAULT_MAX_ATTEMPTS,
    check_status_code,
    is_http_method_token,
    is_real_number,
)
from webcommander.http.retry_policy import (
    DEFAULT_RETRYABLE_HTTP_CODES as _RETRYABLE_HTTP_CODES,
)
from webcommander.http.retry_policy import (
    DEFAULT_UNSAFE_RETRYABLE_HTTP_CODES as _UNSAFE_RETRYABLE_HTTP_CODES,
)
from webcommander.redaction import redact_fields


def _read_installed_version() -> str:
    """The installed package version, or ``0.0.0+source`` when the package is not installed."""
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("webcommander")
    except PackageNotFoundError:
        return "0.0.0+source"


SDK_VERSION = _read_installed_version()

DEFAULT_API_VERSION = "v4"
DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_CONNECT_TIMEOUT_SECONDS = 10.0
DEFAULT_RETRYABLE_HTTP_CODES = tuple(sorted(_RETRYABLE_HTTP_CODES))
DEFAULT_UNSAFE_RETRYABLE_HTTP_CODES = tuple(sorted(_UNSAFE_RETRYABLE_HTTP_CODES))
DEFAULT_POOL_MAXSIZE = 10
DEFAULT_MAX_RESPONSE_BYTES = 64 * 1024 * 1024

#: One budget for the whole request body, multipart framing included.
DEFAULT_MAX_UPLOAD_BYTES = 64 * 1024 * 1024

MAX_CA_BUNDLE_BYTES = 8 * 1024 * 1024
DEFAULT_LOG_LEVEL = "WARNING"
DEFAULT_USER_AGENT = f"webcommander/{SDK_VERSION}"

PRINT_FORMAT_PRETTY = "pretty"
PRINT_FORMAT_COMPACT = "compact"
DEFAULT_PRINT_FORMAT = PRINT_FORMAT_PRETTY

#: The forms ``response.data`` can take; ``.map``, ``.json`` and ``.dto`` are always there.
RESPONSE_FORMAT_MAP = "map"
RESPONSE_FORMAT_JSON = "json"
RESPONSE_FORMAT_DTO = "dto"
VALID_RESPONSE_FORMATS = (
    RESPONSE_FORMAT_MAP,
    RESPONSE_FORMAT_JSON,
    RESPONSE_FORMAT_DTO,
)
DEFAULT_RESPONSE_FORMAT = RESPONSE_FORMAT_MAP
#: Read when ``response_format`` is not set in code.
RESPONSE_FORMAT_ENV_VAR = "WC_RESPONSE_FORMAT"


_VALID_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
_VALID_PRINT_FORMATS = (PRINT_FORMAT_PRETTY, PRINT_FORMAT_COMPACT)
#: ``[0-9]`` not ``\d``, which is Unicode-aware, and no leading zero: both would 404 later.
_API_VERSION_PATTERN = re.compile(r"^v?[1-9][0-9]*$", re.IGNORECASE)
_HEADER_VALUE_TYPES = (str, int, float, bool)

#: The RFC 9110 field value.
_HEADER_VALUE_PATTERN = re.compile(r"\A(?:[\x21-\x7e](?:[\x09\x20-\x7e]*[\x21-\x7e])?)?\Z")
_BOUNDED_REPR = reprlib.Repr()
_BOUNDED_REPR.maxstring = 120
_BOUNDED_REPR.maxother = 120
_BOUNDED_REPR.maxlist = 10
_BOUNDED_REPR.maxtuple = 10
_BOUNDED_REPR.maxdict = 5
_BOUNDED_REPR.maxset = 10
_BOUNDED_REPR.maxlevel = 3


def _bounded(value: Any) -> str:
    return _BOUNDED_REPR.repr(value)


def header_name_problem(name: str) -> str:
    """What makes a header name unsendable, or ``""`` when it is sendable; every path that
    accepts a header reads this, so the constructor and the send agree."""
    if not name:
        return "a blank name"
    if not is_http_method_token(name):
        return "a name outside the RFC 9110 token set"
    return ""


def header_value_problem(value: str) -> str:
    """What makes a header value unsendable, or ``""``; ``requests`` would pass NUL, controls and
    bytes ``>= 0x80``. The position is named, never the byte: it may be a credential."""
    if _HEADER_VALUE_PATTERN.match(value):
        return ""
    for index, character in enumerate(value):
        code = ord(character)
        if code >= 0x80:
            return (
                f"a non-ASCII character at character {index}; encode it yourself - base64, "
                f"or RFC 8187 percent-encoding"
            )
        if (code < 0x20 and character != "\t") or code == 0x7F:
            return f"a control character at character {index}"
    return "a value opening or ending with a space or a tab, which HTTP clients trim"


@dataclass(frozen=True, repr=False)
class SdkConfig:
    """Frozen SDK configuration — every setting the SDK reads."""

    auth: AuthConfig

    api_version: str = DEFAULT_API_VERSION

    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    connect_timeout_seconds: float = DEFAULT_CONNECT_TIMEOUT_SECONDS
    max_retries: int = DEFAULT_MAX_ATTEMPTS
    retryable_http_codes: tuple[int, ...] = DEFAULT_RETRYABLE_HTTP_CODES
    unsafe_retryable_http_codes: tuple[int, ...] = DEFAULT_UNSAFE_RETRYABLE_HTTP_CODES
    retry_backoff_seconds: float = DEFAULT_BACKOFF_SECONDS
    retry_backoff_max_seconds: float = DEFAULT_BACKOFF_MAX_SECONDS

    verify_ssl: bool = True
    ca_bundle: str | os.PathLike[str] | None = None
    proxy_url: str | None = None
    pool_maxsize: int = DEFAULT_POOL_MAXSIZE
    max_response_bytes: int = DEFAULT_MAX_RESPONSE_BYTES
    max_upload_bytes: int = DEFAULT_MAX_UPLOAD_BYTES
    default_headers: tuple[tuple[str, str], ...] = ()
    raise_on_error: bool = False
    #: ``None`` reads ``WC_RESPONSE_FORMAT``, then falls back to ``"map"``.
    response_format: str | None = None
    user_agent: str = DEFAULT_USER_AGENT

    log_level: str = DEFAULT_LOG_LEVEL
    log_bodies: bool = False
    log_file: str | os.PathLike[str] | None = None

    print_api_info: bool = False
    print_request_payload: bool = False
    print_response_body: bool = False
    print_headers: bool = False
    print_curl: bool = False
    print_only_on_error: bool = False
    print_format: str = DEFAULT_PRINT_FORMAT
    print_color: bool = False
    print_max_chars: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "api_version", _normalise_api_version(self.api_version))
        object.__setattr__(self, "ca_bundle", snapshot_a_path(self.ca_bundle))
        object.__setattr__(self, "log_file", snapshot_a_path(self.log_file))
        object.__setattr__(self, "log_level", _normalise_case(self.log_level, str.upper))
        object.__setattr__(self, "print_format", _normalise_case(self.print_format, str.lower))
        object.__setattr__(
            self, "retryable_http_codes", _normalise_codes(self.retryable_http_codes)
        )
        object.__setattr__(
            self,
            "unsafe_retryable_http_codes",
            _normalise_codes(self.unsafe_retryable_http_codes),
        )
        resolved_format, format_problem = _resolve_response_format(self.response_format)
        object.__setattr__(self, "response_format", resolved_format)
        header_problem: str | None = None
        try:
            normalised_headers = _normalise_headers(self.default_headers)
        except SdkConfigError as error:
            header_problem, normalised_headers = str(error), ()
        object.__setattr__(self, "default_headers", normalised_headers)
        self._validate(header_problem, format_problem)

    def _validate(
        self,
        header_problem: str | None = None,
        format_problem: str | None = None,
    ) -> None:
        problems: list[str] = []
        withheld: list[str] = []
        if header_problem:
            problems.append(header_problem)
        if format_problem:
            problems.append(format_problem)

        if not isinstance(self.auth, AuthConfig):
            problems.append(f"auth: expected an AuthConfig, got {type(self.auth).__name__}")

        mistyped: set[str] = set()
        for name, is_valid, expected in _FIELD_TYPES:
            value = getattr(self, name)
            if not is_valid(value):
                mistyped.add(name)
                problems.append(f"{name}: expected {expected}, got {_bounded(value)}")

        if "api_version" not in mistyped and not _API_VERSION_PATTERN.match(self.api_version):
            problems.append(
                f"api_version: expected something like 'v4' or '4', "
                f"got {_bounded(self.api_version)}"
            )

        if "max_retries" not in mistyped and self.max_retries < 1:
            problems.append(
                f"max_retries: must be at least 1 (1 disables retry), got {self.max_retries}"
            )
        if "timeout_seconds" not in mistyped and self.timeout_seconds <= 0:
            problems.append("timeout_seconds: must be > 0")
        if "connect_timeout_seconds" not in mistyped and self.connect_timeout_seconds <= 0:
            problems.append("connect_timeout_seconds: must be > 0")
        if "retry_backoff_seconds" not in mistyped and self.retry_backoff_seconds < 0:
            problems.append("retry_backoff_seconds: must be >= 0")
        if not mistyped & {"retry_backoff_seconds", "retry_backoff_max_seconds"} and (
            self.retry_backoff_max_seconds < self.retry_backoff_seconds
        ):
            problems.append("retry_backoff_max_seconds: must be >= retry_backoff_seconds")
        if "pool_maxsize" not in mistyped and self.pool_maxsize < 1:
            problems.append("pool_maxsize: must be at least 1")
        if "max_response_bytes" not in mistyped and self.max_response_bytes < 1:
            problems.append(
                f"max_response_bytes: must be at least 1 byte, got {self.max_response_bytes}"
            )
        if "max_upload_bytes" not in mistyped and self.max_upload_bytes < 1:
            problems.append(
                f"max_upload_bytes: must be at least 1 byte, got {self.max_upload_bytes}"
            )

        for name in ("retryable_http_codes", "unsafe_retryable_http_codes"):
            if name in mistyped:
                continue
            for code in getattr(self, name):
                try:
                    check_status_code(name, code)
                except SdkConfigError as error:
                    problems.append(error.message)

        if "log_level" not in mistyped and self.log_level not in _VALID_LOG_LEVELS:
            problems.append(
                f"log_level: expected one of {', '.join(_VALID_LOG_LEVELS)}, "
                f"got {_bounded(self.log_level)}"
            )
        if "print_format" not in mistyped and self.print_format not in _VALID_PRINT_FORMATS:
            problems.append(
                f"print_format: expected one of {', '.join(_VALID_PRINT_FORMATS)}, "
                f"got {_bounded(self.print_format)}"
            )
        if "print_max_chars" not in mistyped and self.print_max_chars < 0:
            problems.append("print_max_chars: must be >= 0 (0 = unlimited)")

        if "ca_bundle" not in mistyped and self.ca_bundle:
            if not self.verify_ssl:
                problems.append(
                    "ca_bundle and verify_ssl=False are contradictory: one supplies a "
                    "trust store, the other disables verification"
                )
            if not Path(self.ca_bundle).is_file():
                # The setting is named, not the path: a filesystem layout goes on the detail tier.
                problems.append("ca_bundle: no such file")
                withheld.append(f"ca_bundle={self.ca_bundle}")
            else:
                size = Path(self.ca_bundle).stat().st_size
                if size > MAX_CA_BUNDLE_BYTES:
                    withheld.append(f"ca_bundle={self.ca_bundle}")
                    problems.append(
                        f"ca_bundle: the file is {size} bytes, over the "
                        f"{MAX_CA_BUNDLE_BYTES}-byte ceiling this SDK accepts for a trust "
                        f"store; point it at a PEM bundle rather than an archive"
                    )

        if problems:
            raise SdkConfigError(
                "; ".join(problems),
                detail="; ".join(withheld) or None,
            )

    @property
    def base_url(self) -> str:
        """The instance URL, from :attr:`auth`."""
        return self.auth.base_url

    @property
    def client_id(self) -> str:
        """The OAuth2 client id, from :attr:`auth`."""
        return self.auth.client_id

    @property
    def client_secret(self) -> str:
        """The OAuth2 client secret, from :attr:`auth`."""
        return self.auth.client_secret

    @property
    def redirect_uri(self) -> str:
        """The OAuth2 redirect uri, from :attr:`auth`."""
        return self.auth.redirect_uri

    @property
    def auth_string(self) -> str:
        """The WebCommander auth string, from :attr:`auth`."""
        return self.auth.auth_string

    @property
    def client_name(self) -> str:
        """This instance's label, from :attr:`auth`."""
        return self.auth.client_name

    @property
    def grant_type(self) -> str:
        """The OAuth2 grant type, from :attr:`auth`."""
        return self.auth.grant_type

    @property
    def token_cache_path(self) -> Any:
        """Where tokens are cached, from :attr:`auth`."""
        return self.auth.token_cache_path

    @property
    def timeout(self) -> tuple[float, float]:
        """``(connect_timeout_seconds, timeout_seconds)``, as ``requests`` expects; the transport
        also applies the second as a ceiling on the whole response body, not only each read."""
        return (self.connect_timeout_seconds, self.timeout_seconds)

    @property
    def default_headers_dict(self) -> dict[str, str]:
        """``default_headers`` as a fresh ``dict``, so mutating it cannot affect the config."""
        return dict(self.default_headers)

    @classmethod
    def from_credentials(
        cls,
        credentials: Sequence[Any],
        instance: int | str | None = None,
        **overrides: Any,
    ) -> "SdkConfig":
        """Pick one credential block by position or ``client_name``, the first for ``None``, and
        build a config; a mapping gives the fields or a ready-made ``auth``, not both."""
        chosen = select_credentials(credentials, instance)
        if isinstance(chosen, cls):
            return chosen.with_overrides(**overrides) if overrides else chosen
        if isinstance(chosen, AuthConfig):
            _reject_unknown_config_fields(overrides)
            return cls(chosen, **overrides)
        if not isinstance(chosen, Mapping):
            raise SdkConfigError(
                f"credentials[{0 if instance is None else instance!r}]: expected an "
                f"SdkConfig, an AuthConfig or a mapping of config fields, got "
                f"{type(chosen).__name__}"
            )
        block = dict(chosen)
        supplied_auth = block.pop("auth", None)
        auth_names = {field.name for field in fields(AuthConfig)}
        auth_values = {name: block.pop(name) for name in list(block) if name in auth_names}
        settings = {**block, **overrides}
        _reject_unknown_config_fields(settings)
        if supplied_auth is None:
            absent = [
                field.name
                for field in fields(AuthConfig)
                if field.default is MISSING
                and field.default_factory is MISSING
                and field.name not in auth_values
            ]
            if absent:
                raise SdkConfigError(f"credentials: missing required field(s): {', '.join(absent)}")
            return cls(AuthConfig(**auth_values), **settings)
        if auth_values:
            raise SdkConfigError(
                f"auth: an AuthConfig was supplied alongside the credential field(s) "
                f"{', '.join(sorted(auth_values))}; pass one or the other"
            )
        return cls(supplied_auth, **settings)

    def with_overrides(self, **changes: Any) -> "SdkConfig":
        """Derive a new validated config from this one, which is left untouched."""
        _reject_unknown_config_fields(changes)
        return replace(self, **changes)

    def __repr__(self) -> str:
        """Return a ``repr`` safe to log, with credentials redacted."""
        shown = redact_fields(self, [field.name for field in fields(self)])
        return f"SdkConfig({', '.join(shown)})"


def select_credentials(
    credentials: Sequence[Any],
    instance: int | str | None = None,
) -> Any:
    """Return one block from a list, chosen by position or by ``client_name``, exactly as
    supplied and not a copy. ``None`` takes the first."""
    blocks = list(credentials)
    if not blocks:
        raise SdkUsageError("no credentials were supplied")

    if instance is None:
        return blocks[0]

    if isinstance(instance, int) and not isinstance(instance, bool):
        try:
            return blocks[instance]
        except IndexError:
            raise SdkUsageError(
                f"no credentials at index {instance}; {len(blocks)} supplied (0-{len(blocks) - 1})"
            ) from None

    matched = [index for index, block in enumerate(blocks) if read_client_name(block) == instance]
    if len(matched) > 1:
        # First-match-wins would silently send one tenant's credentials to another.
        raise SdkUsageError(
            f"instance {instance!r} is defined more than once, at index "
            f"{' and '.join(str(index) for index in matched)}; "
            f"client_name has to identify one entry"
        )
    if matched:
        return blocks[matched[0]]

    available = ", ".join(
        read_client_name(block) or f"<index {index}>" for index, block in enumerate(blocks)
    )
    raise SdkUsageError(f"unknown instance {instance!r}; available: {available}")


def read_client_name(block: Any) -> str | None:
    """An entry's ``client_name``, whether a config or a mapping, or ``None`` when it sets none."""
    if isinstance(block, (SdkConfig, AuthConfig)):
        return block.client_name
    if isinstance(block, Mapping):
        value = block.get("client_name")
        return str(value) if value else None
    return None


def _is_text(value: Any) -> bool:
    return isinstance(value, str)


def _is_boolean(value: Any) -> bool:
    return isinstance(value, bool)


def _is_whole_number(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_code_sequence(value: Any) -> bool:
    return isinstance(value, tuple)


def _is_optional_text(value: Any) -> bool:
    return value is None or isinstance(value, str)


#: ``(field, predicate, description)`` for each field a value check would raise on.
_FIELD_TYPES: tuple[tuple[str, Callable[[Any], bool], str], ...] = (
    ("api_version", _is_text, "a string like 'v4' or '4'"),
    ("timeout_seconds", is_real_number, "a number of seconds"),
    ("connect_timeout_seconds", is_real_number, "a number of seconds"),
    ("max_retries", _is_whole_number, "an integer"),
    ("retryable_http_codes", _is_code_sequence, "an iterable of HTTP status codes"),
    (
        "unsafe_retryable_http_codes",
        _is_code_sequence,
        "an iterable of HTTP status codes",
    ),
    ("retry_backoff_seconds", is_real_number, "a number of seconds"),
    ("retry_backoff_max_seconds", is_real_number, "a number of seconds"),
    # Refused, not coerced: ``"false"`` is truthy and would reach ``requests`` as a CA path.
    ("verify_ssl", _is_boolean, "True or False"),
    ("ca_bundle", _is_optional_text, "a path or None"),
    ("proxy_url", _is_optional_text, "a proxy URL or None"),
    ("pool_maxsize", _is_whole_number, "an integer"),
    ("max_response_bytes", _is_whole_number, "an integer number of bytes"),
    ("max_upload_bytes", _is_whole_number, "an integer number of bytes"),
    ("raise_on_error", _is_boolean, "True or False"),
    ("response_format", _is_text, "a string"),
    ("user_agent", _is_text, "a string"),
    ("log_level", _is_text, "a string"),
    ("log_bodies", _is_boolean, "True or False"),
    ("log_file", _is_optional_text, "a path or None"),
    ("print_api_info", _is_boolean, "True or False"),
    ("print_request_payload", _is_boolean, "True or False"),
    ("print_response_body", _is_boolean, "True or False"),
    ("print_headers", _is_boolean, "True or False"),
    ("print_curl", _is_boolean, "True or False"),
    ("print_only_on_error", _is_boolean, "True or False"),
    ("print_format", _is_text, "a string"),
    ("print_color", _is_boolean, "True or False"),
    ("print_max_chars", _is_whole_number, "an integer"),
)


def _reject_unknown_config_fields(values: Mapping[str, Any]) -> None:
    """Raise for any name that is not a field on :class:`SdkConfig`."""
    unknown = set(values) - {field.name for field in fields(SdkConfig)}
    if unknown:
        raise SdkConfigError(f"unknown config field(s): {', '.join(sorted(unknown))}")


def _normalise_api_version(raw_value: Any) -> Any:
    if raw_value is not None and not isinstance(raw_value, str):
        return raw_value
    value = (raw_value or "").strip().lower()
    if value and not value.startswith("v"):
        value = f"v{value}"
    return value


def _resolve_response_format(raw_value: Any) -> tuple[Any, str | None]:
    """Resolve ``response_format`` through its tiers, returning the value and any problem for
    the batched report. Only ``None`` reaches ``WC_RESPONSE_FORMAT``: code beats environment."""
    source: str | None = None
    if raw_value is None:
        raw_value = os.environ.get(RESPONSE_FORMAT_ENV_VAR)
        source = RESPONSE_FORMAT_ENV_VAR
        if raw_value is None or not raw_value.strip():
            return DEFAULT_RESPONSE_FORMAT, None
    value = _normalise_case(raw_value, str.lower)
    if not isinstance(value, str):
        return value, None
    if value not in VALID_RESPONSE_FORMATS:
        from_where = f" from {source}" if source else ""
        return value, f"{_response_format_problem(value)}{from_where}"
    return value, None


def check_response_format(raw_value: Any) -> str:
    """One call's ``response_format``, trimmed and lower-cased; an unknown form raises."""
    value = _normalise_case(raw_value, str.lower)
    if value not in VALID_RESPONSE_FORMATS:
        raise SdkUsageError(_response_format_problem(value))
    return value


def _response_format_problem(value: Any) -> str:
    return (
        f"response_format: expected one of {', '.join(VALID_RESPONSE_FORMATS)}, "
        f"got {_bounded(value)}"
    )


def _normalise_case(raw_value: Any, transform: Callable[[str], str]) -> Any:
    if raw_value is not None and not isinstance(raw_value, str):
        return raw_value
    return transform((raw_value or "").strip())


def _normalise_codes(raw_value: Any) -> Any:
    if isinstance(raw_value, (str, bytes)) or not isinstance(raw_value, Iterable):
        return raw_value
    return tuple(raw_value)


def _header_value(key: Any, value: Any) -> str:
    """Stringify one header value, refusing anything that is not a scalar."""
    if not isinstance(value, _HEADER_VALUE_TYPES):
        raise SdkConfigError(
            f"default_headers: {_bounded(str(key))} holds {_bounded(value)}, which "
            f"is not a header value; headers must be flat"
        )
    return str(value)


def _header_pair(key: Any, value: Any) -> tuple[str, str]:
    """Normalise one header pair to text, refusing one the transport's grammar would refuse."""
    pair = (str(key), _header_value(key, value))
    problem = header_name_problem(pair[0]) or header_value_problem(pair[1])
    if problem:
        raise SdkConfigError(
            f"default_headers: {ascii(_bounded(pair[0]))} cannot be sent as a header - "
            f"{problem}. The value is not shown: it may be a credential"
        )
    return pair


def _normalise_headers(raw_value: Any) -> tuple[tuple[str, str], ...]:
    if not raw_value:
        return ()
    if isinstance(raw_value, Mapping):
        return tuple(_header_pair(key, value) for key, value in raw_value.items())
    if isinstance(raw_value, str):
        try:
            decoded = json.loads(raw_value)
        except json.JSONDecodeError as error:
            raise SdkConfigError(
                f"default_headers: expected a mapping or a JSON object, "
                f"got {_bounded(raw_value)} ({error})"
            ) from None
        if not isinstance(decoded, dict):
            raise SdkConfigError("default_headers: JSON must be an object")
        return tuple(_header_pair(key, value) for key, value in decoded.items())
    if not isinstance(raw_value, Iterable):
        raise SdkConfigError(
            f"default_headers: expected a mapping, a JSON object or "
            f"(name, value) pairs, got {_bounded(raw_value)}"
        )
    pairs: list[tuple[str, str]] = []
    for entry in raw_value:
        # Checked before unpacking, which would read ``["ab", "cd"]`` as two pairs.
        if (
            isinstance(entry, (str, bytes, bytearray))
            or not isinstance(entry, Sequence)
            or len(entry) != 2
        ):
            raise SdkConfigError(
                f"default_headers: expected (name, value) pairs, got {_bounded(entry)}"
            )
        name, value = entry
        pairs.append(_header_pair(name, value))
    return tuple(pairs)
