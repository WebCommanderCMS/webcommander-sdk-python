"""Common settings endpoints, under ``/api/{api_version}``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.common_settings import common_settings_urls
from webcommander.resources.common_settings.common_settings_dto import (
    CommonSettings,
    CustomerFields,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "get_settings",
    "head_settings",
    "update_settings",
    "save_settings",
    "get_create_customer_fields",
    "head_create_customer_fields",
]

CommonSettingsPayload = Mapping[str, Any] | str | Dto


def get_settings(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CommonSettings]:
    """Read the store's settings — ``GET /settings``, ``{"settings": {group: [{"config_key",
    "value"}]}}``. ``type`` names one group, an unknown one ``404``; ``config_key`` one key, with
    or without ``type``. A comma list of keys matches nothing and answers ``{"settings": {}}``.
    Secrets read ``***``. Other names, paging included, are ``400``. Without ``type`` the
    answer is every group, about 2 MB, and can take 30 seconds or more."""
    return client.send_get_request(
        common_settings_urls.SETTINGS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CommonSettings,
    )


def head_settings(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the settings are reachable — ``HEAD /settings``; no body. It runs the read's
    query, so pass a ``type``: an unknown one is ``404``."""
    return client.send_api_request(
        "HEAD",
        common_settings_urls.SETTINGS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_settings(
    client: Any,
    payload: CommonSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CommonSettings]:
    """Save settings — ``PUT /settings`` with ``{"settings": {group: ...}}``; ``200`` and every
    group of the store. Only the keys sent change, and one bad entry refuses the whole
    request with ``400``. A write was measured at 5 to 53 seconds, past the default 30 of
    ``timeout_seconds`` at the slow end: build the client with a longer one."""
    require_payload(payload)
    return client.send_put_request(
        common_settings_urls.SETTINGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CommonSettings,
    )


def save_settings(
    client: Any,
    payload: CommonSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CommonSettings]:
    """Save settings — ``POST /settings``, the ``PUT``'s body, behaviour and timing, answered
    ``201``. A ``POST`` is not resent after a timeout, so read the keys back before retrying."""
    require_payload(payload)
    return client.send_post_request(
        common_settings_urls.SETTINGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CommonSettings,
    )


def get_create_customer_fields(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerFields]:
    """Read the customer registration form — ``GET /create-customer-fields``, the active
    ``fields`` in order and every field's ``fields_configs``. Any query name is ``400``."""
    return client.send_get_request(
        common_settings_urls.CREATE_CUSTOMER_FIELDS,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerFields,
    )


def head_create_customer_fields(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the registration form is there — ``HEAD /create-customer-fields``; no body."""
    return client.send_api_request(
        "HEAD",
        common_settings_urls.CREATE_CUSTOMER_FIELDS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
