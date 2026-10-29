"""The WebCommander API client and ``build_client``."""

from __future__ import annotations

import ipaddress
import json
import logging
import os
import threading
import warnings
from contextlib import contextmanager
from typing import Any, Iterator, Mapping, Sequence
from urllib.parse import parse_qsl, quote, urlsplit

from requests.structures import CaseInsensitiveDict

from webcommander.auth.token_provider import TokenProvider
from webcommander.auth.token_store import (
    FileTokenStore,
    MemoryTokenStore,
    TokenStore,
    build_credentials_namespace,
)
from webcommander.client.api_response import ApiResponse
from webcommander.client.console import (
    render_exchange,
    render_json_value,
    summarise_payload,
)
from webcommander.client.resource_binding import (
    BoundResource,
    registered_resource_names,
    resolve_resource_module,
)
from webcommander.config.sdk_config import (
    SdkConfig,
    check_response_format,
    header_name_problem,
    header_value_problem,
)
from webcommander.dto import Dto
from webcommander.errors import (
    InsecureTransportWarning,
    SdkConfigError,
    SdkError,
    SdkUsageError,
)
from webcommander.http.query_params import build_query_params, materialise_query_params
from webcommander.http.retry_policy import SAFE_METHODS, RetryPolicy
from webcommander.http.transport import (
    Transport,
    materialise_body,
    normalise_http_method,
)
from webcommander.http.url_builder import (
    build_url,
    find_path_param_names,
    substitute_path_params,
)
from webcommander.redaction import redact_snapshot

__all__ = ["WebCommanderClient", "build_client"]

LOGGER_NAME = "webcommander"

_API_VERSION_PARAM = "api_version"

_AUTHORIZATION_HEADER = "Authorization"

#: Stamped on a ``log_file`` handler: how many clients write through it, and a mark it is ours.
_HANDLER_USERS = "_webcommander_client_count"


def _header_name(key: Any) -> str:
    """Validate one caller-supplied header name; a non-text one is refused, not coerced."""
    if isinstance(key, bytes):
        key = key.decode("latin-1")
    if not isinstance(key, str):
        raise SdkUsageError(
            f"headers: a header name must be text, got {type(key).__name__} {ascii(key)}"
        )
    problem = header_name_problem(key)
    if problem:
        raise SdkUsageError(f"headers: a header name may not carry {problem}, got {ascii(key)}")
    return key


def _header_value(name: str, value: Any) -> Any:
    """Validate one caller header value; the refusal never quotes it, as it may be a credential."""
    if not isinstance(value, (str, bytes)):
        raise SdkUsageError(
            f"headers: the value for {ascii(name)} must be text, got {type(value).__name__}"
        )
    text = value.decode("latin-1") if isinstance(value, bytes) else value
    problem = header_value_problem(text)
    if problem:
        raise SdkUsageError(
            f"headers: the value for {ascii(name)} carries {problem}. The value is not "
            f"shown: it may be a credential"
        )
    return value


def _normalise_caller_headers(headers: Mapping[str, Any] | None) -> dict[str, Any]:
    normalised: dict[str, Any] = {}
    for key, value in (headers or {}).items():
        name = _header_name(key)
        normalised[name] = _header_value(name, value)
    return normalised


def _validate_path(path: Any) -> str:
    """Refuse a non-text or blank path."""
    if not isinstance(path, str):
        raise SdkUsageError(f"path must be text, got {type(path).__name__} {path!r}")
    if not path.strip():
        raise SdkUsageError(f"path must name an endpoint, got {path!r}")
    return path


def _log_path_template(path: str) -> str:
    """What a log record may name a call: the path template, never the resolved path."""
    split = urlsplit(path)
    return split.path or path


def _reject_duplicated_query_params(url: str, params: Mapping[str, Any]) -> None:
    """Refuse a name the URL's own query already carries: ``requests`` would send both values."""
    if not params:
        return
    existing = {name for name, _ in parse_qsl(urlsplit(url).query, keep_blank_values=True)}
    clash = sorted(existing & set(params))
    if clash:
        raise SdkUsageError(
            f"query_params {', '.join(clash)} already appear in the path's query string"
        )


_LOOPBACK_HOSTNAMES = frozenset({"localhost", "localhost.localdomain"})


def _is_loopback_host(hostname: str | None) -> bool:
    """Whether a host name or address refers only to this machine."""
    if not hostname:
        return False
    if hostname.lower() in _LOOPBACK_HOSTNAMES:
        return True
    try:
        return ipaddress.ip_address(hostname.strip("[]")).is_loopback
    except ValueError:
        return False


def _with_authorization(headers: Mapping[str, str], access_token: str | None) -> dict[str, str]:
    request_headers = dict(headers)
    if access_token:
        request_headers[_AUTHORIZATION_HEADER] = f"Bearer {access_token}"
    return request_headers


def _logger_safe(client_name: str) -> str:
    """Flatten a ``client_name`` into one logger-name segment, injectively; a dot nests loggers."""
    return quote(client_name, safe="").replace(".", "%2E")


class WebCommanderClient:
    """Authenticated access to one WebCommander store."""

    def __init__(
        self,
        config: SdkConfig,
        *,
        token_store: TokenStore | None = None,
        transport: Transport | None = None,
        retry_policy: RetryPolicy | None = None,
        token_provider: TokenProvider | None = None,
    ) -> None:
        # Before anything that can raise, so ``close_client`` finds the latch.
        self._closed = False
        self._lifecycle_lock = threading.RLock()
        self._sends_in_flight = 0
        self._release_when_idle = False
        if transport is not None and retry_policy is not None:
            raise SdkUsageError("pass transport or retry_policy, not both")
        self._config = config
        self._logger = logging.getLogger(f"{LOGGER_NAME}.{_logger_safe(self._config.client_name)}")
        # Without this the logger inherits root's WARNING and every log_* goes inert.
        self._logger.setLevel(getattr(logging, self._config.log_level))
        self._attach_log_file()

        try:
            if not self._config.verify_ssl:
                message = (
                    "TLS verification is disabled (verify_ssl=False); responses cannot be trusted"
                )
                self._logger.warning(message)
                warnings.warn(message, InsecureTransportWarning, stacklevel=2)

            self._warn_about_plaintext_transport()

            self._owns_transport = transport is None
            self._transport = (
                Transport(
                    self._config, retry_policy=retry_policy, on_progress=self._report_progress
                )
                if transport is None
                else transport
            )
            self._token_store = token_store or self._build_token_store(self._config)
            self._token_provider = token_provider or TokenProvider(
                self._config, self._transport, self._token_store
            )
        except BaseException:
            self._detach_log_file()
            raise

    def _warn_about_plaintext_transport(self) -> None:
        """Warn on an ``http://`` ``base_url`` off this machine: the token would cross in clear."""
        parsed = urlsplit(self._config.base_url)
        if parsed.scheme != "http" or _is_loopback_host(parsed.hostname):
            return
        # The client name, not the host: a configured host is not published to warnings and logs.
        message = (
            f"instance {self._config.client_name!r}: base_url uses http://, so every "
            f"request crosses the network in cleartext — the bearer token, and the "
            f"credentials in the token request itself. Use https:// unless this is a "
            f"local development instance"
        )
        self._logger.warning(message)
        warnings.warn(message, InsecureTransportWarning, stacklevel=3)

    @property
    def config(self) -> SdkConfig:
        """The frozen configuration this client was built with."""
        return self._config

    @property
    def name(self) -> str:
        """This client's name, as it appears in logs and printed output."""
        return self._config.client_name

    def send_api_request(
        self,
        http_method: str,
        path: str,
        *,
        path_params: Mapping[str, Any] | None = None,
        query_params: Mapping[str, Any] | None = None,
        json_body: Any = None,
        form_data: Any = None,
        files: Any = None,
        headers: Mapping[str, str] | None = None,
        authenticated: bool = True,
        raise_on_error: bool | None = None,
        response_format: str | None = None,
        dto_type: Any = None,
    ) -> ApiResponse:
        """Send one request and return the response; ``json_body`` may be a mapping, raw JSON text
        or a :class:`~webcommander.dto.Dto`. A caller mistake is refused before the token grant."""
        with self._one_send():
            http_method = normalise_http_method(http_method)
            path = _validate_path(path)
            resolved_format = self._resolve_response_format(response_format)

            # Frozen before the body is read: reading it runs caller code that could edit them.
            logged_path = _log_path_template(path)
            resolved_path = substitute_path_params(path, self._seed_api_version(path, path_params))
            url = build_url(self._config.base_url, resolved_path)
            normalised_params = build_query_params(query_params)
            _reject_duplicated_query_params(url, normalised_params)
            prepared_params = materialise_query_params(normalised_params)
            base_headers = self._materialise_request_headers(headers)

            json_body = self._validate_request_payload(json_body=json_body, form_data=form_data)
            # Snapshotted before ``materialise_body`` runs caller code that could edit the mapping.
            json_snapshot = None if json_body is None else redact_snapshot(json_body)
            prepared = materialise_body(
                json_body,
                form_data,
                files,
                max_upload_bytes=self._config.max_upload_bytes,
                max_prepare_seconds=self._config.timeout_seconds,
            )
            reported_body = (
                json_snapshot if json_body is not None else redact_snapshot(prepared.form_record)
            )
            reported_files = prepared.files
            reported_payload = summarise_payload(reported_body, reported_files)
            form_encoded = prepared.form_encoded

            access_token = self._token_provider.get_access_token() if authenticated else None

            def send_once(token: str | None) -> ApiResponse:
                """Send the request once, with ``Authorization`` built for ``token``."""
                request_headers = _with_authorization(base_headers, token)
                try:
                    return self._transport.send_prepared_request(
                        http_method,
                        url,
                        prepared,
                        params=prepared_params,
                        headers=request_headers,
                        request_info_headers=request_headers,
                        request_info_body=reported_payload,
                        endpoint_template=logged_path,
                        response_format=resolved_format,
                        dto_type=dto_type,
                    )
                except SdkError as error:
                    if error.request_info is not None:
                        self._report_exchange(
                            _FailedExchange(error),
                            reported_body,
                            reported_files,
                            path_template=logged_path,
                            level=logging.ERROR,
                            form_encoded=form_encoded,
                        )
                    raise

            response = send_once(access_token)

            if authenticated and _means_expired_token(response, http_method):
                if prepared.replayable:
                    self._report_exchange(
                        response,
                        reported_body,
                        reported_files,
                        path_template=logged_path,
                        level=logging.WARNING,
                        form_encoded=form_encoded,
                    )
                    response = send_once(self._token_provider.refresh_access_token(access_token))

            self._report_exchange(
                response,
                reported_body,
                reported_files,
                path_template=logged_path,
                form_encoded=form_encoded,
            )

            should_raise = self._config.raise_on_error if raise_on_error is None else raise_on_error
            if should_raise:
                response.raise_for_status()
            return response

    def send_get_request(self, path: str, **kwargs: Any) -> ApiResponse:
        """Send a ``GET``; see :meth:`send_api_request`."""
        return self.send_api_request("GET", path, **kwargs)

    def send_post_request(self, path: str, **kwargs: Any) -> ApiResponse:
        """Send a ``POST``; see :meth:`send_api_request`."""
        return self.send_api_request("POST", path, **kwargs)

    def send_put_request(self, path: str, **kwargs: Any) -> ApiResponse:
        """Send a ``PUT``; see :meth:`send_api_request`."""
        return self.send_api_request("PUT", path, **kwargs)

    def send_patch_request(self, path: str, **kwargs: Any) -> ApiResponse:
        """Send a ``PATCH``; see :meth:`send_api_request`."""
        return self.send_api_request("PATCH", path, **kwargs)

    def send_delete_request(self, path: str, **kwargs: Any) -> ApiResponse:
        """Send a ``DELETE``; see :meth:`send_api_request`."""
        return self.send_api_request("DELETE", path, **kwargs)

    def _refuse_if_closed(self) -> None:
        """Refuse a closed client's send: its pool would silently re-open. Call under the lock."""
        if self._closed:
            raise SdkUsageError(
                f"client {self._config.client_name!r} is closed: close_client() "
                f"released its log file and the session it opened, so it cannot send "
                f"again — build a new client rather than reusing a closed one"
            )

    @contextmanager
    def _one_send(self) -> Iterator[None]:
        """Hold the lifecycle gate for one logical request."""
        with self._lifecycle_lock:
            self._refuse_if_closed()
            self._sends_in_flight += 1
        try:
            yield
        finally:
            with self._lifecycle_lock:
                self._sends_in_flight -= 1
                if self._release_when_idle and self._sends_in_flight == 0:
                    self._release_when_idle = False
                    self._release_what_this_client_opened()

    def close_client(self) -> None:
        """Release the session this client opened and its ``log_file`` handle, keeping the cached
        token and any injected transport. Idempotent; calls in flight finish before the release."""
        with self._lifecycle_lock:
            if self._closed:
                return
            self._closed = True
            if self._sends_in_flight:
                self._release_when_idle = True
                return
            self._release_what_this_client_opened()

    def _release_what_this_client_opened(self) -> None:
        try:
            # An injected transport may be serving another client, so only an owned one is closed.
            if self._owns_transport:
                self._transport.close_transport()
        finally:
            self._detach_log_file()

    def __enter__(self) -> "WebCommanderClient":
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close_client()

    def __getattr__(self, name: str) -> Any:
        """Expose a registered resource module bound to this client, cached once resolved. An
        unknown name raises ``SdkAttributeError``, an ``AttributeError``, so ``hasattr`` works."""
        if name.startswith("_"):
            raise AttributeError(name)
        namespace = BoundResource(self, resolve_resource_module(name))
        object.__setattr__(self, name, namespace)
        return namespace

    def list_resource_names(self) -> tuple[str, ...]:
        """Every resource reachable as an attribute, e.g. ``('admin_customers',)``."""
        return registered_resource_names()

    @staticmethod
    def _build_token_store(config: SdkConfig) -> TokenStore:
        if config.token_cache_path:
            return FileTokenStore(
                config.token_cache_path,
                build_credentials_namespace(
                    config.base_url,
                    config.client_id,
                    config.client_secret,
                    config.auth_string,
                    config.grant_type,
                ),
            )
        return MemoryTokenStore()

    def _seed_api_version(self, path: str, path_params: Mapping[str, Any] | None) -> dict[str, Any]:
        resolved = dict(path_params or {})
        if _API_VERSION_PARAM in find_path_param_names(path) and _API_VERSION_PARAM not in resolved:
            resolved[_API_VERSION_PARAM] = self._config.api_version
        return resolved

    def _materialise_request_headers(self, headers: Mapping[str, str] | None) -> dict[str, str]:
        """Merge the SDK's headers, ``default_headers`` and the caller's once, before the grant.
        ``Authorization`` is left out: the one header a replay changes, it is added per attempt."""
        # Case-insensitive: a plain dict would let a caller's ``authorization`` win.
        own = {
            "Accept": "application/json",
            "User-Agent": self._config.user_agent,
        }
        merged = CaseInsensitiveDict(own)
        merged.update(self._config.default_headers_dict)
        if headers:
            merged.update(_normalise_caller_headers(headers))
        canonical = {key.lower(): key for key in (_AUTHORIZATION_HEADER, *own)}
        return {canonical.get(key.lower(), key): value for key, value in merged.items()}

    def _resolve_response_format(self, response_format: Any) -> str:
        """The form ``.data`` takes for one call: the parameter if given, else the client's."""
        if response_format is None:
            return self._config.response_format
        return check_response_format(response_format)

    def _validate_request_payload(self, *, json_body: Any, form_data: Any) -> Any:
        """Refuse a payload that could never be sent, and return the body to send."""
        if json_body is not None and form_data is not None:
            raise SdkUsageError(
                "pass json_body or form_data, not both — they are different "
                "content types and only one can be sent"
            )
        if json_body is None:
            return json_body
        if isinstance(json_body, str):
            try:
                decoded = json.loads(json_body)
            except (ValueError, RecursionError) as error:
                raise SdkUsageError(f"json_body: not valid JSON: {error}") from None
            if not isinstance(decoded, (dict, list)):
                raise SdkUsageError(
                    f"json_body: a JSON string must hold an object or an array, got "
                    f"{type(decoded).__name__}"
                )
            return json_body
        if isinstance(json_body, Dto):
            json_body = json_body.to_map()
        if not isinstance(json_body, (Mapping, list, tuple)):
            raise SdkUsageError(
                f"json_body must be a JSON string, a mapping or a list, got "
                f"{type(json_body).__name__}"
            )
        return json_body

    def _attach_log_file(self) -> None:
        """Give this client's logger one file handler, at most one per logger."""
        self._log_handler: logging.FileHandler | None = None
        if not self._config.log_file:
            return
        # ``baseFilename`` is absolute, so a relative ``log_file`` would never match.
        target = os.path.abspath(self._config.log_file)
        for handler in self._logger.handlers:
            existing = getattr(handler, "baseFilename", None)
            if existing == target:
                users = getattr(handler, _HANDLER_USERS, None)
                if users is not None and isinstance(handler, logging.FileHandler):
                    setattr(handler, _HANDLER_USERS, users + 1)
                    self._log_handler = handler
                return
            if existing is not None:
                raise SdkConfigError(
                    f"log_file: client_name {self._config.client_name!r} already logs "
                    f"to a different file, so adding this one would write every record "
                    f"from both clients into both files — give this client its own "
                    f"client_name, or close the first one first",
                    detail=f"already logging to {existing}; asked for {target}",
                )
        try:
            file_handler = logging.FileHandler(target, encoding="utf-8")
        except (OSError, ValueError) as error:
            raise SdkConfigError(
                "log_file: the file could not be opened for writing; point it at a path "
                "whose directory exists and is writable, or leave it unset",
                detail=f"{target}: {getattr(error, 'strerror', None) or error}",
                cause=error,
            ) from None
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )
        file_handler.setLevel(getattr(logging, self._config.log_level))
        setattr(file_handler, _HANDLER_USERS, 1)
        self._logger.addHandler(file_handler)
        self._log_handler = file_handler

    def _detach_log_file(self) -> None:
        """Release this client's claim on its file handler, closing it on the last release."""
        handler = self._log_handler
        if handler is None:
            return
        self._log_handler = None
        remaining = getattr(handler, _HANDLER_USERS, 1) - 1
        setattr(handler, _HANDLER_USERS, remaining)
        if remaining > 0:
            return
        self._logger.removeHandler(handler)
        handler.close()

    def _report_progress(self, message: str) -> None:
        """Report a request in flight or a retry waiting, so a slow store and a hang differ."""
        config = self._config
        if config.print_api_info and not config.print_only_on_error:
            print(message, flush=True)
        self._logger.log(logging.INFO, "%s", message)

    def _report_exchange(
        self,
        response: ApiResponse | _FailedExchange,
        payload: Any,
        files: Any,
        *,
        path_template: str,
        level: int = logging.INFO,
        form_encoded: bool = False,
    ) -> None:
        """Print the exchange block when the caller asked for one, and log one line."""
        config = self._config
        wants_print = (
            config.print_api_info
            or config.print_request_payload
            or config.print_response_body
            or config.print_headers
            or config.print_curl
        )
        if wants_print and not (config.print_only_on_error and response.succeeded):
            print(render_exchange(response, payload, files, config, form_encoded=form_encoded))

        self._logger.log(
            level,
            "%s %s -> %s in %ss (attempt %s/%s)",
            response.request_info.http_method,
            path_template,
            response.status_code,
            response.request_info.elapsed_seconds,
            response.request_info.attempt_count,
            response.request_info.max_attempts,
        )
        if config.log_bodies:
            self._logger.log(
                logging.DEBUG,
                "payload=%s response=%s",
                render_json_value(summarise_payload(payload, files), compact=True),
                render_json_value(redact_snapshot(response.map), compact=True),
            )


def build_client(
    instance: int | str | None = None,
    *,
    credentials: Sequence[Any] | None = None,
    **overrides: Any,
) -> "WebCommanderClient":
    """Build a client for one registered instance: the first when ``instance`` is omitted, else by
    index or ``client_name``; ``overrides`` beat its fields. Close it, or use ``with``."""
    from webcommander.client.client_registry import get_registered_instances

    blocks = credentials if credentials is not None else get_registered_instances()
    return WebCommanderClient(SdkConfig.from_credentials(blocks, instance, **overrides))


_TOKEN_FAILURE_ERROR = "unauthorized"
_TOKEN_FAILURE_MESSAGES = ("invalid_access_token", "invalid_request")

#: Shown where a status would go when no response arrived; text, so it never reads as one.
_NO_RESPONSE_STATUS = "no response"


class _FailedExchange:
    """A request that produced no response, as the five attributes ``render_exchange`` reads."""

    succeeded = False
    map = None

    def __init__(self, error: SdkError) -> None:
        self.status_code = _NO_RESPONSE_STATUS
        self.headers: Mapping[str, str] = {}
        self.request_info = error.request_info


def _means_expired_token(response: ApiResponse, http_method: str) -> bool:
    """Whether a 401 means the access token rather than the request."""
    if response.status_code != 401:
        return False
    body = response.map
    if not isinstance(body, Mapping):
        # A proxy's HTML page says nothing; guessing "stale" duplicates a write.
        return http_method.upper() in SAFE_METHODS
    if _normalised_reason(body.get("error")) == _TOKEN_FAILURE_ERROR:
        return True
    return _normalised_reason(body.get("message")) in _TOKEN_FAILURE_MESSAGES


def _normalised_reason(value: Any) -> str:
    return str(value or "").strip().lower()
