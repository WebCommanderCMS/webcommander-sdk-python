"""Python SDK for the WebCommander REST API."""

from __future__ import annotations

import logging

from webcommander.auth.token_provider import TokenProvider, TokenRecord, build_token_path
from webcommander.auth.token_store import (
    FileTokenStore,
    MemoryTokenStore,
    TokenStore,
    build_credentials_namespace,
    build_default_token_cache_path,
)
from webcommander.client.api_response import ApiResponse, ErrorType, RequestInfo
from webcommander.client.client_registry import (
    ClientRegistry,
    get_registered_instances,
    list_instance_names,
    register_instances,
)
from webcommander.client.console import build_curl_command, render_exchange
from webcommander.client.pagination import iter_pages, iter_records
from webcommander.client.resource_binding import (
    BoundResource,
    register_resource_module,
    registered_resource_names,
)
from webcommander.client.web_commander_client import WebCommanderClient, build_client
from webcommander.config.auth_config import USE_DEFAULT_TOKEN_CACHE, AuthConfig
from webcommander.config.sdk_config import (
    DEFAULT_RETRYABLE_HTTP_CODES,
    DEFAULT_UNSAFE_RETRYABLE_HTTP_CODES,
    SDK_VERSION,
    SdkConfig,
    read_client_name,
    select_credentials,
)
from webcommander.dto import Dto
from webcommander.errors import (
    DIAGNOSTICS_ENVIRONMENT_VARIABLE,
    DegradedTokenCacheWarning,
    DegradedTokenLockWarning,
    InsecureTransportWarning,
    SdkAttributeError,
    SdkAuthError,
    SdkConfigError,
    SdkError,
    SdkTokenCacheError,
    SdkTokenLockError,
    SdkUsageError,
    error_diagnostics_enabled,
    set_error_diagnostics,
)
from webcommander.http.query_params import SortDirection, build_query_params
from webcommander.http.retry_policy import RetryPolicy
from webcommander.http.transport import Transport
from webcommander.http.url_builder import build_url, substitute_path_params
from webcommander.redaction import (
    CIRCULAR,
    MAX_REDACTION_DEPTH,
    REDACTED,
    SENSITIVE_KEY_MARKERS,
    TOO_DEEP,
    redact_mapping,
    redact_text,
    redact_value,
    should_redact,
)

__version__ = SDK_VERSION

logging.getLogger("webcommander").addHandler(logging.NullHandler())

__all__ = [
    "__version__",
    "SDK_VERSION",
    "AuthConfig",
    "USE_DEFAULT_TOKEN_CACHE",
    "SdkConfig",
    "DEFAULT_RETRYABLE_HTTP_CODES",
    "DEFAULT_UNSAFE_RETRYABLE_HTTP_CODES",
    "select_credentials",
    "read_client_name",
    "WebCommanderClient",
    "build_client",
    "ClientRegistry",
    "register_instances",
    "list_instance_names",
    "get_registered_instances",
    "register_resource_module",
    "registered_resource_names",
    "BoundResource",
    "render_exchange",
    "build_curl_command",
    "iter_pages",
    "iter_records",
    "REDACTED",
    "SENSITIVE_KEY_MARKERS",
    "TOO_DEEP",
    "CIRCULAR",
    "MAX_REDACTION_DEPTH",
    "should_redact",
    "redact_value",
    "redact_mapping",
    "redact_text",
    "ApiResponse",
    "RequestInfo",
    "ErrorType",
    "Dto",
    "SdkError",
    "SdkConfigError",
    "SdkUsageError",
    "SdkAttributeError",
    "SdkAuthError",
    "SdkTokenCacheError",
    "SdkTokenLockError",
    "InsecureTransportWarning",
    "DegradedTokenLockWarning",
    "DegradedTokenCacheWarning",
    "error_diagnostics_enabled",
    "set_error_diagnostics",
    "DIAGNOSTICS_ENVIRONMENT_VARIABLE",
    "TokenProvider",
    "TokenRecord",
    "TokenStore",
    "MemoryTokenStore",
    "FileTokenStore",
    "build_credentials_namespace",
    "build_default_token_cache_path",
    "build_token_path",
    "Transport",
    "RetryPolicy",
    "SortDirection",
    "build_query_params",
    "build_url",
    "substitute_path_params",
]
