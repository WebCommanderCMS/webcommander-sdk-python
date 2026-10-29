"""Shipping settings endpoints, under ``/api/{api_version}/admin/settings/shipping_settings``.
The area is flat: its seven keys are fields, not sections."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.shipping_settings import shipping_settings_urls
from webcommander.resources.settings.shipping_settings.shipping_settings_dto import ShippingSettings

__all__ = [
    "get_shipping_settings",
    "patch_shipping_settings",
    "head_shipping_settings",
]

ShippingSettingsPayload = Mapping[str, Any] | str | Dto


def get_shipping_settings(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingSettings]:
    """Read the whole area — ``GET /admin/settings/shipping_settings``; seven fields, flat."""
    return client.send_get_request(
        shipping_settings_urls.SHIPPING_SETTINGS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingSettings,
    )


def patch_shipping_settings(
    client: Any,
    payload: ShippingSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingSettings]:
    """Write one field or several — ``PATCH /admin/settings/shipping_settings``, wrapped or bare.
    Turning ``enable_shipping_class`` off also clears ``enable_flat_view_class``; write both."""
    require_payload(payload)
    return client.send_patch_request(
        shipping_settings_urls.SHIPPING_SETTINGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingSettings,
    )


def head_shipping_settings(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/shipping_settings``; no body."""
    return client.send_api_request(
        "HEAD",
        shipping_settings_urls.SHIPPING_SETTINGS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
