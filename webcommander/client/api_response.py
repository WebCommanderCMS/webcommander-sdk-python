"""What every SDK call returns."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Collection, Generic, Iterator, Mapping, TypeVar, cast
from urllib.parse import urlsplit

from webcommander.config.sdk_config import (
    DEFAULT_RESPONSE_FORMAT,
    RESPONSE_FORMAT_DTO,
    RESPONSE_FORMAT_JSON,
    VALID_RESPONSE_FORMATS,
)
from webcommander.dto import Dto
from webcommander.errors import SdkAuthError, SdkError, SdkUsageError
from webcommander.redaction import (
    REDACTED,
    redact_mapping,
    redact_snapshot,
    redact_text,
    should_redact,
)

_MAX_REPORTED_MESSAGES = 50
#: Deep enough for ``errors[] -> entry -> message -> [..]``.
_MAX_MESSAGE_DEPTH = 4

_SUCCESS_FLAG_FIELD = "isSuccess"

#: Not built yet, as against built and ``None``: a binary body has no text and no DTO.
_NOT_BUILT = object()

JSON_MEDIA_TYPE = "application/json"

TEXT_MEDIA_TYPE_PREFIX = "text/"

CONTENT_TYPE_HEADER = "Content-Type"

#: A codec that cannot fail, so a mislabelled charset still yields text.
TEXT_FALLBACK_CHARSET = "iso-8859-1"

DtoT = TypeVar("DtoT", bound=Dto)


class ErrorType(str, Enum):
    """Classification of a failed call, derived from the HTTP status."""

    NONE = "none"
    #: The whole ``3xx`` range: redirects are not followed, so one reaches the caller.
    REDIRECT = "redirect"
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    NOT_FOUND = "not_found"
    METHOD_NOT_ALLOWED = "method_not_allowed"
    CONFLICT = "conflict"
    RATE_LIMIT = "rate_limit"
    SERVER = "server"
    NETWORK = "network"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"

    __str__ = str.__str__


#: The unredacted target, a private attribute rather than a field so nothing renders it.
_COMPARISON_URL_SLOT = "_comparison_url"


def comparison_url(request_info: Any) -> str:
    """The request target as it was sent, unredacted, for private comparison only."""
    value = getattr(request_info, _COMPARISON_URL_SLOT, "")
    return value if isinstance(value, str) else ""


@dataclass(frozen=True)
class RequestInfo:
    """Everything about the request behind a response, safe to log: each field that can carry a
    value is redacted and frozen at every depth, so JSON needs ``default=dict``."""

    client_name: str
    api_version: str
    http_method: str
    url: str
    query_params: Mapping[str, Any] = field(default_factory=dict)
    body: Any = None
    headers: Mapping[str, str] = field(default_factory=dict)
    attempt_count: int = 1
    max_attempts: int = 1
    elapsed_seconds: float = 0.0
    #: The endpoint template errors and logs print, never the resolved path; defaults to the path.
    endpoint_template: str = ""

    def __post_init__(self) -> None:
        """Redact, snapshot and freeze every field that can carry a value, whoever built it."""
        object.__setattr__(self, _COMPARISON_URL_SLOT, self.url)
        object.__setattr__(self, "query_params", _frozen(_redact_query_params(self.query_params)))
        object.__setattr__(self, "url", redact_text(self.url))
        object.__setattr__(self, "headers", _frozen(redact_mapping(self.headers)))
        object.__setattr__(self, "body", _frozen(redact_snapshot(self.body)))
        object.__setattr__(self, "endpoint_template", self.endpoint_template or _url_path(self.url))


@dataclass(frozen=True)
class ApiResponse(Generic[DtoT]):
    """One HTTP exchange: what was sent and what came back. ``.map`` is always the decoded body;
    ``.data`` follows ``response_format``, and is ``None`` where that form does not exist."""

    status_code: int
    data: Any
    headers: Mapping[str, str]
    content_type: str | None
    request_info: RequestInfo
    error_type: ErrorType = ErrorType.NONE
    raw_body: bytes | None = None
    response_format: str = DEFAULT_RESPONSE_FORMAT
    dto_type: type[DtoT] | None = None

    _decoded_body: Any = field(init=False, repr=False, compare=False, default=None)
    _json_text: Any = field(init=False, repr=False, compare=False, default=_NOT_BUILT)
    _dto_view: Any = field(init=False, repr=False, compare=False, default=_NOT_BUILT)

    def __post_init__(self) -> None:
        """Make the classification hold whoever built the record."""
        object.__setattr__(self, "_decoded_body", self.data)
        if self.response_format not in VALID_RESPONSE_FORMATS:
            raise SdkUsageError(
                f"unknown response_format {self.response_format!r}; expected one of: "
                f"{', '.join(VALID_RESPONSE_FORMATS)}"
            )
        if not isinstance(self.error_type, ErrorType):
            try:
                object.__setattr__(self, "error_type", ErrorType(self.error_type))
            except ValueError:
                available = ", ".join(member.value for member in ErrorType)
                raise SdkUsageError(
                    f"unknown error_type {self.error_type!r}; expected an "
                    f"ErrorType or one of: {available}"
                ) from None
        if self.error_type is ErrorType.NONE and not self.succeeded:
            derived = classify_error_type(self.status_code, _body_denies_success(self.map))
            object.__setattr__(self, "error_type", derived)
        # Last, so nothing above reads a re-pointed ``.data``; no fallback to the other form.
        if self.response_format == RESPONSE_FORMAT_JSON:
            object.__setattr__(self, "data", self.json)
        elif self.response_format == RESPONSE_FORMAT_DTO:
            object.__setattr__(self, "data", self.dto)

    @property
    def map(self) -> Any:
        """The decoded body, whatever ``response_format`` says: ``dict``/``list`` for JSON,
        ``str`` for ``text/*``, ``bytes`` otherwise, ``None`` for an empty body."""
        return self._decoded_body

    @property
    def json(self) -> str | None:
        """The server's own body text, whatever ``response_format`` says, decoded from the bytes
        that arrived; ``None`` for a binary or empty body rather than a stringified one."""
        cached = self._json_text
        if cached is not _NOT_BUILT:
            return cached
        text = self._read_body_text()
        object.__setattr__(self, "_json_text", text)
        return text

    @property
    def dto(self) -> DtoT | None:
        """The typed view, of the type the endpoint declared, whatever ``response_format`` says;
        ``None`` for a body that is not a record, or a call that named no type."""
        cached = self._dto_view
        if cached is not _NOT_BUILT:
            return cast("DtoT | None", cached)
        view = self._build_dto()
        object.__setattr__(self, "_dto_view", view)
        return view

    def _build_dto(self) -> DtoT | None:
        body = self.map
        if not isinstance(body, Mapping) or self.dto_type is None:
            return None
        return self.dto_type.from_map(body)

    def _read_body_text(self) -> str | None:
        if isinstance(self.map, str):
            return self.map
        if not self.raw_body:
            return None
        if not _body_has_text(self.content_type):
            return None
        try:
            return self.raw_body.decode("utf-8")
        except UnicodeDecodeError:
            return self.raw_body.decode(TEXT_FALLBACK_CHARSET)

    @property
    def succeeded(self) -> bool:
        """Whether the call succeeded: a 2xx status **and** a body that agrees."""
        return 200 <= self.status_code < 300 and not _body_denies_success(self.map)

    def get_error_messages(self) -> list[str]:
        """Human-readable problems from an error body; empty when it carried none."""
        body = self.map
        if not isinstance(body, Mapping):
            body = _parse_json_body(body)
        if body is None:
            return []

        messages = _read_error_entries(body.get("errors"))
        if not messages:
            messages = _read_message_value(body.get("message"))
        if not messages:
            messages = _read_message_value(body.get("error")) or _read_message_value(
                body.get("errorCode")
            )
        if not messages:
            messages = _read_message_value(body.get("detail")) or _read_message_value(
                body.get("title")
            )
        return _cap_messages(messages)

    def raise_for_status(self) -> "ApiResponse[DtoT]":
        """Raise when the call failed, otherwise return self so the call can chain."""
        if self.succeeded:
            return self

        messages = self.get_error_messages()
        error_class = SdkAuthError if self.status_code in (401, 403) else SdkError
        error = error_class(
            self._failure_summary(len(messages)),
            status_code=self.status_code,
            error_type=self.error_type,
            raw_response=redact_snapshot(self.map),
            response_headers=redact_mapping(self.headers),
            request_info=self.request_info,
        )
        for message in messages:
            error.add_error(message)
        raise error

    def _failure_summary(self, reported: int) -> str:
        """The SDK's one-sentence summary of a failure: a problem count, not the store's text."""
        if 200 <= self.status_code < 300:
            return f"the store answered {self.status_code} but its body denied success"
        detail = f"{reported} problem(s) reported" if reported else "no per-field detail reported"
        return f"the store answered {self.status_code}, {detail}"


def is_json_media_type(content_type: str | None) -> bool:
    """Whether a ``Content-Type`` names JSON, ``+json`` suffixes included: the one rule the
    decoder and :attr:`ApiResponse.json` both read, so the two never disagree."""
    media_type = _media_type(content_type)
    return media_type == JSON_MEDIA_TYPE or media_type.endswith("+json")


def _media_type(content_type: str | None) -> str:
    return (content_type or "").lower().split(";", 1)[0].strip()


def _body_has_text(content_type: str | None) -> bool:
    return is_json_media_type(content_type) or _media_type(content_type).startswith(
        TEXT_MEDIA_TYPE_PREFIX
    )


def _redact_query_params(params: Mapping[str, Any] | None) -> dict[str, Any]:
    if not params:
        return {}
    return {
        key: (REDACTED if should_redact(str(key)) else redact_snapshot(value))
        for key, value in params.items()
    }


class _FrozenMapping(Mapping[Any, Any]):
    """A read-only mapping on a :class:`RequestInfo`. Not a ``dict`` subclass: an inherited
    mutator called against the base class would write past the redaction."""

    __slots__ = ("_entries",)

    def __init__(self, entries: Mapping[Any, Any]) -> None:
        # Copied, so whoever holds the original cannot reach these entries.
        self._entries: dict[Any, Any] = dict(entries)

    def __getitem__(self, key: Any) -> Any:
        return self._entries[key]

    def __iter__(self) -> Iterator[Any]:
        return iter(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    def __contains__(self, key: Any) -> bool:
        # Not the mixin's ``in``, which raises ``TypeError`` on an unhashable key.
        try:
            return key in self._entries
        except TypeError:
            return False

    def __eq__(self, other: Any) -> bool:
        """Equal to any mapping holding the same entries, a plain ``dict`` included."""
        if isinstance(other, _FrozenMapping):
            return self._entries == other._entries
        if isinstance(other, Mapping):
            return self._entries == dict(other)
        return NotImplemented

    def __repr__(self) -> str:
        return repr(self._entries)

    def copy(self) -> dict[Any, Any]:
        """A plain, mutable ``dict`` of the entries."""
        return dict(self._entries)


def _frozen(value: Any) -> Any:
    """Make one redacted value immutable at every depth: mappings become :class:`_FrozenMapping`,
    sequences tuples and writable buffers ``bytes``, so nothing behind the record can change."""
    if isinstance(value, Mapping):
        return _FrozenMapping({key: _frozen(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_frozen(item) for item in value)
    if isinstance(value, memoryview):
        # ``tobytes`` rather than ``bytes(...)``, which refuses a non-contiguous view.
        return value.tobytes()
    if isinstance(value, bytearray):
        return bytes(value)
    return value


def _url_path(url: str) -> str:
    """A URL's path alone, for a record built without a template; host and query are left out."""
    return urlsplit(url).path


def _body_denies_success(data: Any) -> bool:
    """Whether a body carries an explicit ``isSuccess`` denial. A truthy value never denies, the
    string ``"false"`` included: wrongly denying would break working calls."""
    return (
        isinstance(data, Mapping)
        and _SUCCESS_FLAG_FIELD in data
        and not _is_truthy(data[_SUCCESS_FLAG_FIELD])
    )


def _is_truthy(value: Any) -> bool:
    """JSON truthiness, as a store's ``isSuccess`` flag counts it."""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    # After the ``bool`` arm: ``bool`` subclasses ``int``, so ``True`` would read as 1.
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, Collection):
        return len(value) > 0
    return True


def _parse_json_body(data: Any) -> Mapping[str, Any] | None:
    """Parse a JSON body that did not arrive decoded."""
    if isinstance(data, bytes):
        try:
            data = data.decode("utf-8")
        except UnicodeDecodeError:
            return None
    if not isinstance(data, str):
        return None
    text = data.strip().lstrip("\ufeff").strip()
    if not text.startswith(("{", "[")):
        return None
    try:
        parsed = json.loads(text)
    except ValueError:
        return None
    return parsed if isinstance(parsed, Mapping) else None


def _read_message_value(value: Any, depth: int = 0) -> list[str]:
    """Any value from an error body as human-readable messages, blank ones dropped."""
    if value is None or depth > _MAX_MESSAGE_DEPTH:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, Mapping):
        return _read_message_value(_message_or_code(value), depth + 1)
    if isinstance(value, (list, tuple)):
        messages: list[str] = []
        for item in value:
            messages.extend(_read_message_value(item, depth + 1))
        return messages
    text = str(value)
    return [text] if text.strip() else []


def _read_error_entries(entries: Any) -> list[str]:
    """Read the ``errors`` tier in whichever of its three shapes arrived, and nothing
    else, so a stray ``"errors": 0`` cannot shadow a good ``message``."""
    if isinstance(entries, Mapping):
        messages: list[str] = []
        for field_name, value in entries.items():
            messages.extend(_prefix_field(field_name, _read_message_value(value)))
        return messages
    if isinstance(entries, (list, tuple)):
        messages = []
        for entry in entries:
            if isinstance(entry, Mapping):
                entry_messages = _read_message_value(_message_or_code(entry))
                messages.extend(_prefix_field(entry.get("field"), entry_messages))
            else:
                messages.extend(_read_message_value(entry))
        return messages
    if isinstance(entries, str):
        return _read_message_value(entries)
    return []


def _message_or_code(entry: Mapping[str, Any]) -> Any:
    text = entry.get("message")
    return entry.get("code") if text is None else text


def _prefix_field(field_name: Any, messages: list[str]) -> list[str]:
    """Prefix each message with its field name, ``0`` included."""
    if field_name is None or not str(field_name).strip():
        return messages
    return [f"{field_name}: {message}" for message in messages]


def _cap_messages(messages: list[str]) -> list[str]:
    """Cap the reported problems, replacing the tail with a count."""
    if len(messages) <= _MAX_REPORTED_MESSAGES:
        return messages
    remainder = len(messages) - _MAX_REPORTED_MESSAGES
    return messages[:_MAX_REPORTED_MESSAGES] + [f"+{remainder} more problems"]


def classify_error_type(status_code: int, body_denies_success: bool = False) -> ErrorType:
    """Map an HTTP status to an :class:`ErrorType`, from the status rather than the body. A 2xx
    whose body denies success is ``UNKNOWN``, matching :attr:`ApiResponse.succeeded`."""
    if 200 <= status_code < 300:
        return ErrorType.UNKNOWN if body_denies_success else ErrorType.NONE
    if 300 <= status_code < 400:
        return ErrorType.REDIRECT
    if status_code in (400, 422):
        return ErrorType.VALIDATION
    if status_code == 401:
        return ErrorType.AUTHENTICATION
    if status_code == 403:
        return ErrorType.AUTHORIZATION
    if status_code == 404:
        return ErrorType.NOT_FOUND
    if status_code == 405:
        return ErrorType.METHOD_NOT_ALLOWED
    if status_code == 409:
        return ErrorType.CONFLICT
    if status_code == 429:
        return ErrorType.RATE_LIMIT
    if 500 <= status_code < 600:
        return ErrorType.SERVER
    return ErrorType.UNKNOWN
