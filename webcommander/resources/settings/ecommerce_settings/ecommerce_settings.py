"""Ecommerce settings endpoints, under ``/api/{api_version}/admin/settings/ecommerce_settings``.
The area is a facade over six sections; its ``order_flags`` key is not one of them."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.ecommerce_settings import ecommerce_settings_urls
from webcommander.resources.settings.ecommerce_settings.ecommerce_settings_dto import (
    EcommerceSettings,
)

__all__ = [
    "get_ecommerce_settings",
    "patch_ecommerce_settings",
    "head_ecommerce_settings",
    "get_ecommerce_settings_section",
    "patch_ecommerce_settings_section",
]

EcommerceSettingsPayload = Mapping[str, Any] | str | Dto


def get_ecommerce_settings(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[EcommerceSettings]:
    """Read the whole area — ``GET /admin/settings/ecommerce_settings``; carries an ``ETag``."""
    return client.send_get_request(
        ecommerce_settings_urls.ECOMMERCE_SETTINGS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=EcommerceSettings,
    )


def patch_ecommerce_settings(
    client: Any,
    payload: EcommerceSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[EcommerceSettings]:
    """Write fields in one or more sections — ``PATCH /admin/settings/ecommerce_settings``.
    The body must be wrapped in ``ecommerce_settings``; ``order_flags`` in it is dropped."""
    require_payload(payload)
    return client.send_patch_request(
        ecommerce_settings_urls.ECOMMERCE_SETTINGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=EcommerceSettings,
    )


def head_ecommerce_settings(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/ecommerce_settings``; no body."""
    return client.send_api_request(
        "HEAD",
        ecommerce_settings_urls.ECOMMERCE_SETTINGS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_ecommerce_settings_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[EcommerceSettings]:
    """Read one section — ``GET /admin/settings/ecommerce_settings/{section}``.
    ``.data`` is under the section's own key, with no ``group_meta``."""
    return client.send_get_request(
        ecommerce_settings_urls.ECOMMERCE_SETTINGS_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=EcommerceSettings,
    )


def patch_ecommerce_settings_section(
    client: Any,
    section: str,
    payload: EcommerceSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[EcommerceSettings]:
    """Write fields in one section — ``PATCH /admin/settings/ecommerce_settings/{section}``.
    An unrecognised field is ``400`` even beside a known one."""
    require_payload(payload)
    return client.send_patch_request(
        ecommerce_settings_urls.ECOMMERCE_SETTINGS_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=EcommerceSettings,
    )
