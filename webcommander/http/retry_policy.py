"""Retry decisions and backoff timing."""

from __future__ import annotations

import math
import random
import reprlib
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import requests
import urllib3.exceptions

from webcommander.errors import SdkConfigError

DEFAULT_MAX_ATTEMPTS = 1
DEFAULT_BACKOFF_SECONDS = 0.5
DEFAULT_BACKOFF_MAX_SECONDS = 20.0

#: No ``401``: it is refreshed and replayed a layer up, so a retry would resend a dead token.
DEFAULT_RETRYABLE_HTTP_CODES = frozenset({429, 500, 502, 503, 504})

#: RFC 9110 §9.2.1 safe methods, and the only way into the unrestricted status retry.
SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "TRACE"})

DEFAULT_UNSAFE_RETRYABLE_HTTP_CODES: frozenset[int] = frozenset()

#: Methods a possibly-delivered request can be sent again as.
IDEMPOTENT_METHODS = SAFE_METHODS | frozenset({"PUT", "DELETE"})

#: The characters RFC 9110 §5.6.2 allows in a token, which an HTTP method and a header name are.
_TOKEN_CHARACTERS = frozenset(
    "!#$%&'*+-.^_`|~0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
)

_MIN_STATUS_CODE = 100
_MAX_STATUS_CODE = 599


def is_http_method_token(method: Any) -> bool:
    """Whether a value is an RFC 9110 token, as an HTTP method and a header name must be."""
    if not isinstance(method, str) or not method:
        return False
    return all(character in _TOKEN_CHARACTERS for character in method)


def check_status_code(name: str, value: Any) -> int:
    """Validate one configured status code, returning it."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise SdkConfigError(
            f"{name}: expected HTTP status codes as integers from {_MIN_STATUS_CODE} "
            f"through {_MAX_STATUS_CODE}, got {reprlib.repr(value)}"
        )
    if not _MIN_STATUS_CODE <= value <= _MAX_STATUS_CODE:
        raise SdkConfigError(
            f"{name}: {value} is not an HTTP status code "
            f"({_MIN_STATUS_CODE}-{_MAX_STATUS_CODE} is every code there is)"
        )
    return value


#: Failed before delivery, so the store cannot have run it: safe to resend as any method.
FAILURE_BEFORE_DELIVERY = "before_delivery"

#: Failed after the request was sent, so it may have run: resend only an idempotent method.
FAILURE_AFTER_DELIVERY = "after_delivery"

#: Not a delivery problem, such as a malformed URL: another attempt would fail the same way.
FAILURE_NOT_A_DELIVERY_PROBLEM = "not_a_delivery_problem"

#: Connection establishment failures, each with a ``requests`` class of its own.
_BEFORE_DELIVERY_CLASSES = (
    requests.exceptions.ConnectTimeout,
    requests.exceptions.ProxyError,
    requests.exceptions.SSLError,
)

#: Failures that can only happen once the request has gone out.
_AFTER_DELIVERY_CLASSES = (
    requests.exceptions.ReadTimeout,
    requests.exceptions.ChunkedEncodingError,
    requests.exceptions.ContentDecodingError,
)

#: Establishment failures inside a bare ``ConnectionError``, told apart by the ``urllib3`` reason.
_BEFORE_DELIVERY_REASONS = (
    urllib3.exceptions.NewConnectionError,
    urllib3.exceptions.ProxyError,
    urllib3.exceptions.SSLError,
)

#: The largest ``2.0 ** n`` exponent without ``OverflowError``; the window is clamped past it.
_MAX_BACKOFF_DOUBLINGS = 1023


def is_real_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _normalised_method(method: Any) -> str:
    if not isinstance(method, str):
        return ""
    stripped = method.strip()
    return stripped.upper() if is_http_method_token(stripped) else ""


def _is_safe_method(method: Any) -> bool:
    return _normalised_method(method) in SAFE_METHODS


def _is_idempotent_method(method: Any) -> bool:
    """Whether resending this method cannot add an effect; an unrecognised one answers ``False``."""
    return _normalised_method(method) in IDEMPOTENT_METHODS


def _wrapped_reason(exception: BaseException) -> BaseException | None:
    """The ``urllib3`` failure inside a ``requests`` exception, or ``None``: a refusal, a DNS
    failure, a read timeout and a reset all arrive as one ``ConnectionError``."""
    for argument in exception.args:
        if isinstance(argument, urllib3.exceptions.MaxRetryError):
            return argument.reason
        if isinstance(argument, BaseException):
            return argument
    return None


def classify_transport_failure(exception: BaseException) -> str:
    """Whether this failure happened before or after delivery, the table the retry decision
    reads; a timeout's error category comes from :func:`transport_failure_timed_out`."""
    # Before the ``ConnectionError`` arm below: all three derive from it.
    if isinstance(exception, _BEFORE_DELIVERY_CLASSES):
        return FAILURE_BEFORE_DELIVERY
    if isinstance(exception, _AFTER_DELIVERY_CLASSES):
        return FAILURE_AFTER_DELIVERY
    if isinstance(exception, requests.exceptions.ConnectionError):
        reason = _wrapped_reason(exception)
        if isinstance(reason, _BEFORE_DELIVERY_REASONS):
            return FAILURE_BEFORE_DELIVERY
        # An unnamed reason reads as possibly delivered: the safe way, withholding a write replay.
        return FAILURE_AFTER_DELIVERY
    if isinstance(exception, requests.exceptions.Timeout):
        return FAILURE_AFTER_DELIVERY
    return FAILURE_NOT_A_DELIVERY_PROBLEM


def transport_failure_timed_out(exception: BaseException) -> bool:
    """Whether this failure was a deadline rather than a connection problem, ``TIMEOUT`` not
    ``NETWORK``; ``NewConnectionError`` derives from ``ConnectTimeoutError``, so it is excluded."""
    reason = _wrapped_reason(exception)
    if isinstance(reason, urllib3.exceptions.NewConnectionError):
        return False
    if isinstance(reason, urllib3.exceptions.TimeoutError):
        return True
    return isinstance(exception, requests.exceptions.Timeout)


@dataclass(frozen=True)
class RetryPolicy:
    """How many attempts to make, on what, and how long to wait between them."""

    max_attempts: int = DEFAULT_MAX_ATTEMPTS
    backoff_seconds: float = DEFAULT_BACKOFF_SECONDS
    backoff_max_seconds: float = DEFAULT_BACKOFF_MAX_SECONDS
    retryable_status_codes: frozenset[int] = DEFAULT_RETRYABLE_HTTP_CODES
    unsafe_retryable_status_codes: frozenset[int] = DEFAULT_UNSAFE_RETRYABLE_HTTP_CODES

    def __post_init__(self) -> None:
        """Freeze the status sets and refuse an unusable policy."""
        for name in ("retryable_status_codes", "unsafe_retryable_status_codes"):
            codes = getattr(self, name)
            if isinstance(codes, (str, bytes, bytearray)):
                raise SdkConfigError(
                    f"{name}: expected an iterable of HTTP status codes, got {codes!r}"
                )
            try:
                frozen = frozenset(codes)
            except TypeError:
                raise SdkConfigError(
                    f"{name}: expected an iterable of HTTP status codes, got {codes!r}"
                ) from None
            for code in sorted(frozen, key=repr):
                check_status_code(name, code)
            object.__setattr__(self, name, frozen)
        if (
            not isinstance(self.max_attempts, int)
            or isinstance(self.max_attempts, bool)
            or self.max_attempts < 1
        ):
            raise SdkConfigError(
                f"max_attempts: must be at least 1 (1 disables retry), got {self.max_attempts!r}"
            )
        for name in ("backoff_seconds", "backoff_max_seconds"):
            value = getattr(self, name)
            if not is_real_number(value):
                raise SdkConfigError(f"{name}: expected a number of seconds, got {value!r}")
        if self.backoff_seconds < 0:
            raise SdkConfigError(f"backoff_seconds: must be >= 0, got {self.backoff_seconds!r}")
        if self.backoff_max_seconds < self.backoff_seconds:
            raise SdkConfigError(
                f"backoff_max_seconds: must be >= backoff_seconds, got "
                f"{self.backoff_max_seconds!r} < {self.backoff_seconds!r}"
            )

    @classmethod
    def snapshot(cls, policy: Any) -> "RetryPolicy":
        """A private copy of a supplied policy, revalidated as if it had been built here."""
        return cls(
            max_attempts=policy.max_attempts,
            backoff_seconds=policy.backoff_seconds,
            backoff_max_seconds=policy.backoff_max_seconds,
            retryable_status_codes=policy.retryable_status_codes,
            unsafe_retryable_status_codes=policy.unsafe_retryable_status_codes,
        )

    @classmethod
    def from_config(cls, config: Any) -> "RetryPolicy":
        """Build a policy mirroring an ``SdkConfig``'s retry settings."""
        return cls(
            max_attempts=config.max_retries,
            backoff_seconds=config.retry_backoff_seconds,
            backoff_max_seconds=config.retry_backoff_max_seconds,
            retryable_status_codes=config.retryable_http_codes,
            unsafe_retryable_status_codes=config.unsafe_retryable_http_codes,
        )

    def should_retry_status_code(self, status_code: int, method: str = "GET") -> bool:
        """Whether a response with this status warrants another attempt."""
        if status_code not in self.retryable_status_codes:
            return False
        if _is_safe_method(method):
            return True
        return status_code in self.unsafe_retryable_status_codes

    def should_retry_after_exception(self, exception: BaseException, method: str = "GET") -> bool:
        """Whether a transport failure warrants another attempt: only one that never arrived."""
        failure = classify_transport_failure(exception)
        if failure == FAILURE_BEFORE_DELIVERY:
            return True
        if failure == FAILURE_AFTER_DELIVERY:
            return _is_idempotent_method(method)
        return False

    def compute_backoff_seconds(self, attempt: int, retry_after: str | None = None) -> float:
        """Seconds to sleep before the next 1-based ``attempt``: exponential with full jitter. A
        ``Retry-After`` in either form beats the jitter, clamped by ``backoff_max_seconds``."""
        server_delay = _parse_retry_after(retry_after)
        if server_delay is not None:
            return min(server_delay, self.backoff_max_seconds)
        doublings = min(max(0, attempt - 1), _MAX_BACKOFF_DOUBLINGS)
        window = min(self.backoff_seconds * 2.0**doublings, self.backoff_max_seconds)
        return random.uniform(0.0, window)


def _parse_retry_after(retry_after: str | None) -> float | None:
    if not retry_after:
        return None
    value = retry_after.strip()
    # ``float()`` reads "1_0" as 10.0, not legal delta-seconds, so those take the date path.
    if "_" not in value:
        try:
            # Order matters: ``max(0.0, nan)`` is 0.0, but ``max(nan, 0.0)`` is ``nan``.
            return max(0.0, float(value))
        except ValueError:
            pass
    try:
        when = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return max(0.0, (when - datetime.now(timezone.utc)).total_seconds())
