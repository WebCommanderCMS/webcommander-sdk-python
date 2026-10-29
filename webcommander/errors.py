"""Exception hierarchy for the WebCommander SDK."""

from __future__ import annotations

import os
import re
from typing import Any, Mapping

#: Includes U+2028 and U+2029, which would break the lines of :meth:`SdkError.explain`.
_CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f-\x9f\u2028\u2029]")
_CONTROL_CHARACTERS_EXCEPT_NEWLINE = re.compile(r"[\x00-\x09\x0b-\x1f\x7f-\x9f\u2028\u2029]")

DIAGNOSTICS_ENVIRONMENT_VARIABLE = "WC_ERROR_DIAGNOSTICS"

_AFFIRMATIVE = frozenset({"1", "true", "yes", "on"})

_DIAGNOSTICS_REMEDY = (
    "call explain(diagnostics=True), or set WC_ERROR_DIAGNOSTICS=1, for the "
    "store's message, the response body, the query values, the resolved URL, the "
    "path or origin this failure names and the native cause's own wording"
)


def _diagnostics_from_environment() -> bool:
    return (os.environ.get(DIAGNOSTICS_ENVIRONMENT_VARIABLE) or "").strip().lower() in _AFFIRMATIVE


_diagnostics = _diagnostics_from_environment()


def error_diagnostics_enabled() -> bool:
    """Whether :meth:`SdkError.explain` includes its diagnostic tier by default."""
    return _diagnostics


def set_error_diagnostics(enabled: bool) -> bool:
    """Turn the diagnostic tier on or off process-wide, returning what it was so a
    diagnostic block can put it back."""
    global _diagnostics
    previous = _diagnostics
    _diagnostics = bool(enabled)
    return previous


def _flatten(value: Any) -> str:
    """A server value as one escaped line, so a ``message`` cannot forge an ``explain`` field."""
    return neutralise_controls(str(value))


def neutralise_controls(text: str, *, keep_newlines: bool = False) -> str:
    """Escape control characters in one outside value, since a terminal acts on escapes."""
    pattern = _CONTROL_CHARACTERS_EXCEPT_NEWLINE if keep_newlines else _CONTROL_CHARACTERS
    return pattern.sub(lambda match: match.group().encode("unicode_escape").decode("ascii"), text)


class SdkError(Exception):
    """Base class for every error the SDK raises, and raised directly for any non-2xx that
    is not more specifically an authentication or usage problem."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        error_type: Any = None,
        raw_response: Any = None,
        response_headers: Mapping[str, str] | None = None,
        request_info: Any = None,
        detail: str | None = None,
        cause: BaseException | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        # Typed ``Any`` so this module stays a dependency leaf.
        self.error_type = error_type
        self.raw_response = raw_response
        self.response_headers: dict[str, str] = dict(response_headers or {})
        self.request_info = request_info
        self.detail = detail
        #: The native failure underneath, kept but never chained, so a traceback shows one message.
        self.cause = cause
        self.errors: list[str] = []

    def add_error(self, error_message: str) -> "SdkError":
        """Append one field-level message and return this exception, so calls chain."""
        self.errors.append(error_message)
        return self

    def get_error_messages(self) -> list[str]:
        """The API's field-level messages; empty when it gave none, so read ``.message`` then."""
        return list(self.errors)

    def get_hint(self) -> str | None:
        """A one-line suggestion for this failure, or ``None``."""
        if self.status_code is None:
            return None
        return _HINTS_BY_STATUS.get(self.status_code)

    def explain(self, *, diagnostics: bool | None = None) -> str:
        """Return this failure as one printable block: a structural tier always, plus the
        data tier when ``diagnostics`` is on (``None`` defers to the process setting)."""
        include = error_diagnostics_enabled() if diagnostics is None else bool(diagnostics)
        lines = [str(self)]

        info = self.request_info
        detail = []
        if info is not None:
            if info.attempt_count and info.max_attempts:
                detail.append(f"attempt : {info.attempt_count}/{info.max_attempts}")
            if info.elapsed_seconds is not None:
                detail.append(f"elapsed : {info.elapsed_seconds}s")
        if self.cause is not None:
            # The class name only: a native library's text can name a path, a host or a value.
            detail.append(f"cause   : {type(self.cause).__name__}")
        hint = self.get_hint()
        if hint:
            detail.append(f"hint    : {hint}")
        lines += [f"  {line}" for line in detail]

        if not include:
            lines.append(f"  detail  : withheld — {_DIAGNOSTICS_REMEDY}")
            return "\n".join(lines)

        lines += [f"  {line}" for line in self._diagnostic_lines()]
        return "\n".join(lines)

    def _diagnostic_lines(self) -> list[str]:
        """The tier :meth:`explain` withholds by default; the raiser has already redacted it."""
        lines = []

        if self.detail:
            lines.append(f"detail  : {_flatten(self.detail)}")
        if self.cause is not None:
            lines.append(f"cause   : {type(self.cause).__name__}: {_flatten(self.cause)}")

        info = self.request_info
        if info is not None:
            if info.url:
                lines.append(f"url     : {_flatten(_shorten_url(info.url))}")
            if info.query_params:
                lines.append(f"params  : {dict(info.query_params)}")

        location = _redirect_target(self.response_headers)
        if location:
            lines.append(f"location: {_flatten(location)}")

        messages = self.get_error_messages()
        if messages:
            lines.append("reported:")
            lines += [f"  - {_flatten(message)}" for message in messages]

        if self.raw_response is not None:
            body = _flatten(self.raw_response)
            if len(body) > 500:
                body = body[:500] + f"... +{len(body) - 500} chars"
            lines.append(f"body    : {body}")

        return lines

    def __str__(self) -> str:
        """One line naming the status, the category, the call and this SDK's own reason."""
        parts = []
        if self.status_code:
            parts.append(str(self.status_code))
        if self.error_type is not None:
            parts.append(f"[{_flatten(self.error_type)}]")
        info = self.request_info
        if info is not None:
            if info.http_method and info.endpoint_template:
                parts.append(f"{_flatten(info.http_method)} {_flatten(info.endpoint_template)}")
        reason = _flatten(self.message)
        return f"{' '.join(parts)} - {reason}" if parts else reason


_REDIRECT_STATUS_CODES = (301, 302, 303, 307, 308)

_REDIRECT_HINT = "the SDK does not follow redirects; read the Location header off the response"

_HINTS_BY_STATUS: dict[int, str] = {
    **{status: _REDIRECT_HINT for status in _REDIRECT_STATUS_CODES},
    400: (
        "the API rejected the request itself - check the payload shape and "
        "the query parameter names against the endpoint's docstring"
    ),
    401: (
        "credentials were rejected, or the token expired and could not be "
        "renewed - check client_id, client_secret and auth_string"
    ),
    403: "authenticated, but this client is not allowed to do that",
    404: "no such record - check the id you passed actually exists",
    405: "wrong HTTP method for this path",
    409: "conflicts with existing data, e.g. an email already in use",
    429: "rate limited - slow down, or raise max_retries so the SDK waits and retries for you",
    500: (
        "the server failed. Retrying may help on a read; the SDK will not "
        "retry a write on a 500, because it cannot tell whether the server "
        "committed"
    ),
}


_LOCATION_HEADER = "location"


def _redirect_target(headers: Mapping[str, str]) -> str | None:
    """Return the ``Location`` a response named, whatever case it arrived in."""
    for name, value in headers.items():
        if name.lower() == _LOCATION_HEADER:
            return value
    return None


def _shorten_url(url: str) -> str:
    """Drop the scheme and host, keeping the path that identifies the call."""
    marker = "://"
    if marker not in url:
        return url
    remainder = url.split(marker, 1)[1]
    return remainder[remainder.index("/") :] if "/" in remainder else url


class SdkConfigError(SdkError):
    """Configuration is missing or invalid, raised at construction time and listing every
    problem it found rather than the first."""


class SdkUsageError(SdkError):
    """The caller made a mistake the SDK detects before any network I/O."""


class SdkAttributeError(SdkUsageError, AttributeError):
    """A name that does not exist on a client or a bound resource."""


class SdkAuthError(SdkError):
    """Authentication failed."""


class SdkTokenCacheError(SdkError):
    """The token cache file exists but cannot be read or parsed."""


class SdkTokenLockError(SdkError):
    """The token cache's cross-process lock could not be taken, so the refresh is refused."""


class InsecureTransportWarning(UserWarning):
    """Certificate verification is off, so responses cannot be trusted."""


class DegradedTokenCacheWarning(UserWarning):
    """A token was obtained but not persisted, so the next process pays for its own grant."""


class DegradedTokenLockWarning(UserWarning):
    """A file token store could not take its cross-process lock, so it refused to refresh."""
