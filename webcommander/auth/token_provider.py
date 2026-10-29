"""Obtaining and refreshing the OAuth2 access token."""

from __future__ import annotations

import math
import re
import threading
import time
import warnings
from dataclasses import dataclass, fields
from typing import Any

from webcommander.errors import (
    DegradedTokenCacheWarning,
    SdkAuthError,
    SdkError,
    SdkTokenCacheError,
    SdkUsageError,
)
from webcommander.http.transport import Transport
from webcommander.redaction import redact_fields, redact_mapping, redact_snapshot

TOKEN_PATH_TEMPLATE = "/api/{api_version}/oauth2/token"
DEFAULT_TOKEN_TTL_SECONDS = 3600
EXPIRY_SKEW_SECONDS = 60

#: The longest lifetime accepted, and the furthest ahead a cached expiry is believed.
MAX_TOKEN_TTL_SECONDS = 24 * 60 * 60

_REFRESH_GRANT_TYPE = "refresh_token"

#: RFC 6750 §2.1 ``b64token``: what may follow ``Bearer`` in an ``Authorization`` header.
_BEARER_CREDENTIAL = re.compile(r"^[A-Za-z0-9\-._~+/]+=*$")

#: RFC 6749 ``1*VSCHAR``: a token-request field, so not held to the Bearer grammar above.
_REFRESH_CREDENTIAL = re.compile(r"^[\x20-\x7e]+$")


def check_access_credential(value: Any) -> str:
    """Validate a credential bound for an ``Authorization: Bearer`` header, an RFC 6750
    ``b64token``; the refusal never says which character was wrong, the value being a secret."""
    if not isinstance(value, str):
        raise SdkUsageError(f"access_token: expected text, got {type(value).__name__}")
    if not _BEARER_CREDENTIAL.fullmatch(value):
        raise SdkUsageError("access_token: expected a Bearer credential string")
    return value


def check_refresh_credential(value: Any) -> str:
    """Validate a credential that will be sent as a field of a token request, so RFC 6749
    §5.1 visible text rather than the Bearer grammar. The value itself is never shown."""
    if not isinstance(value, str):
        raise SdkUsageError(
            f"refresh_token: expected the credential as text, got {type(value).__name__}"
        )
    if not _REFRESH_CREDENTIAL.fullmatch(value):
        raise SdkUsageError("refresh_token: not a token-response value")
    return value


def build_token_path(api_version: str) -> str:
    """Build the token endpoint path for a normalised API version such as ``"v4"``."""
    return TOKEN_PATH_TEMPLATE.format(api_version=api_version)


@dataclass(frozen=True, repr=False)
class TokenRecord:
    """An access token and when it stops being usable."""

    access_token: str
    refresh_token: str | None
    expires_at: float
    #: How early to treat this token as expired.
    skew_seconds: float = EXPIRY_SKEW_SECONDS

    def __post_init__(self) -> None:
        """Refuse a record whose credentials could not be sent as what they are."""
        check_access_credential(self.access_token)
        if self.refresh_token is not None:
            check_refresh_credential(self.refresh_token)

    def needs_refresh(self, skew_seconds: float | None = None) -> bool:
        """Whether to treat the token as expired, at the record's own skew unless overridden."""
        effective_skew = self.skew_seconds if skew_seconds is None else skew_seconds
        now = time.time()
        if self.expires_at - now > MAX_TOKEN_TTL_SECONDS:
            # Further ahead than any accepted lifetime, so the stamp is another clock's.
            return True
        return now >= (self.expires_at - effective_skew)

    def to_dict(self) -> dict[str, Any]:
        """Convert to the plain mapping a token store persists."""
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at,
            "skew_seconds": self.skew_seconds,
        }

    @classmethod
    def from_dict(cls, record: dict[str, Any] | None) -> "TokenRecord | None":
        """Rebuild from a stored mapping, or ``None`` when the store held nothing; a present but
        unusable entry raises rather than hiding a corrupt cache behind a grant on every call."""
        if not record:
            return None
        skew_seconds = record.get("skew_seconds")
        if (
            not isinstance(skew_seconds, (int, float))
            or isinstance(skew_seconds, bool)
            or not math.isfinite(skew_seconds)
            or skew_seconds < 0
        ):
            skew_seconds = EXPIRY_SKEW_SECONDS
        expires_at = record.get("expires_at")
        if (
            not isinstance(expires_at, (int, float))
            or isinstance(expires_at, bool)
            or not math.isfinite(expires_at)
        ):
            raise cls._corrupt_record("expires_at is not a finite number of seconds")
        try:
            return cls(
                access_token=record.get("access_token"),
                refresh_token=record.get("refresh_token"),
                expires_at=float(expires_at),
                skew_seconds=min(float(skew_seconds), MAX_TOKEN_TTL_SECONDS),
            )
        except SdkUsageError as error:
            raise cls._corrupt_record(str(error)) from None

    @staticmethod
    def _corrupt_record(problem: str) -> SdkTokenCacheError:
        return SdkTokenCacheError(
            f"the cached token record is unusable: {problem}; clear it or pass "
            f"token_cache_path=None"
        )

    def __repr__(self) -> str:
        """Return a ``repr`` safe to log, with both tokens redacted."""
        shown = redact_fields(self, [field.name for field in fields(self)])
        return f"TokenRecord({', '.join(shown)})"


class TokenProvider:
    """Fetches, caches and renews the access token."""

    def __init__(
        self,
        config: Any,
        transport: Transport,
        token_store: Any,
        *,
        token_path: str | None = None,
    ) -> None:
        self._config = config
        self._transport = transport
        self._token_store = token_store
        self._token_path = token_path or build_token_path(config.api_version)
        self._thread_lock = threading.Lock()

    @property
    def token_url(self) -> str:
        """The absolute token endpoint URL: base URL joined with the token path."""
        return self._config.base_url + self._token_path

    def get_access_token(self) -> str:
        """Return a usable bearer token, fetching one only if needed."""
        record = TokenRecord.from_dict(self._token_store.read_token_record())
        if record and not record.needs_refresh():
            return record.access_token
        return self._renew_access_token(stale_access_token=None, any_cached_token_will_do=True)

    def refresh_access_token(self, stale_access_token: str | None) -> str:
        """Replace a token that the API has just rejected."""
        return self._renew_access_token(
            stale_access_token=stale_access_token, any_cached_token_will_do=False
        )

    def _renew_access_token(
        self, *, stale_access_token: str | None, any_cached_token_will_do: bool
    ) -> str:
        with self._thread_lock:
            with self._token_store.acquire_token_refresh_lock():
                record = TokenRecord.from_dict(self._token_store.read_token_record())
                if record and not record.needs_refresh():
                    # A refresh accepts only a *different* token, not just a fresh one.
                    if any_cached_token_will_do or (
                        stale_access_token is not None and record.access_token != stale_access_token
                    ):
                        return record.access_token

                new_record = None
                if record and record.refresh_token:
                    new_record = self._request_token_with_refresh_grant(record.refresh_token)
                if new_record is None:
                    new_record = self._request_token_with_credentials()

                try:
                    self._token_store.write_token_record(new_record.to_dict())
                except (OSError, SdkError):
                    warnings.warn(
                        "the access token could not be cached, so the next process will "
                        "obtain its own; the call itself succeeded",
                        DegradedTokenCacheWarning,
                        stacklevel=2,
                    )
                return new_record.access_token

    def _request_token_with_credentials(self) -> TokenRecord:
        response = self._transport.send_http_request(
            "POST",
            self.token_url,
            json_body=self._grant_payload(
                grant_type=self._config.grant_type, auth_string=self._config.auth_string
            ),
            headers=self._token_headers(),
            endpoint_template=TOKEN_PATH_TEMPLATE,
        )
        if not response.succeeded:
            messages = response.get_error_messages()
            # Counted, not quoted: an OAuth2 failure body may echo the rejected request.
            reported = f"{len(messages)} problem(s) reported" if messages else "no detail reported"
            error = SdkAuthError(
                f"the token endpoint answered {response.status_code}, {reported}; check "
                f"client_id, client_secret, auth_string and grant_type",
                status_code=response.status_code,
                error_type=response.error_type,
                raw_response=redact_snapshot(response.map),
                response_headers=redact_mapping(response.headers),
                request_info=response.request_info,
            )
            for message in messages:
                error.add_error(message)
            raise error
        return self._build_token_record(response.map, response)

    def _grant_payload(self, **grant: str) -> dict[str, Any]:
        return {
            **grant,
            "redirect_uri": self._config.redirect_uri,
            "client_id": self._config.client_id,
            "client_secret": self._config.client_secret,
        }

    def _request_token_with_refresh_grant(self, refresh_token: str) -> TokenRecord | None:
        payload = self._grant_payload(grant_type=_REFRESH_GRANT_TYPE, refresh_token=refresh_token)
        try:
            response = self._transport.send_http_request(
                "POST",
                self.token_url,
                json_body=payload,
                headers=self._token_headers(),
                endpoint_template=TOKEN_PATH_TEMPLATE,
            )
        except SdkError:
            # An expired refresh token is an ordinary outcome, so fall back to the full grant.
            return None
        if not response.succeeded:
            return None
        try:
            return self._build_token_record(
                response.map, response, previous_refresh_token=refresh_token
            )
        except SdkAuthError:
            return None

    def _token_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self._config.user_agent,
        }

    def _build_token_record(
        self, body: Any, response: Any, *, previous_refresh_token: str | None = None
    ) -> TokenRecord:
        if not isinstance(body, dict) or not body.get("access_token"):
            raise SdkAuthError(
                "token response did not contain an access_token",
                status_code=response.status_code,
                raw_response=redact_snapshot(body),
                request_info=response.request_info,
            )
        expires_in = body.get("expires_in")
        try:
            ttl_seconds = float(expires_in) if expires_in is not None else DEFAULT_TOKEN_TTL_SECONDS
        except (TypeError, ValueError):
            ttl_seconds = DEFAULT_TOKEN_TTL_SECONDS
        if not math.isfinite(ttl_seconds) or ttl_seconds <= 0:
            ttl_seconds = DEFAULT_TOKEN_TTL_SECONDS
        ttl_seconds = min(ttl_seconds, MAX_TOKEN_TTL_SECONDS)
        try:
            return TokenRecord(
                access_token=body["access_token"],
                # A new refresh token is optional in RFC 6749, so keep the held one if none is sent.
                refresh_token=body.get("refresh_token") or previous_refresh_token,
                expires_at=time.time() + ttl_seconds,
                # A lifetime shorter than the standing skew would leave no usable window.
                skew_seconds=min(EXPIRY_SKEW_SECONDS, ttl_seconds / 2),
            )
        except SdkUsageError as error:
            raise SdkAuthError(
                f"the token endpoint answered with a credential this SDK cannot send — {error}",
                status_code=response.status_code,
                raw_response=redact_snapshot(body),
                request_info=response.request_info,
            ) from None
