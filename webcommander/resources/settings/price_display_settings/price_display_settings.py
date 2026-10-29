"""Price display settings endpoints — a facade over two sections, under
``/api/{api_version}/admin/settings/price_display_settings``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.price_display_settings import price_display_settings_urls
from webcommander.resources.settings.price_display_settings.price_display_settings_dto import (
    PriceDisplaySettings,
)

__all__ = [
    "get_price_display_settings",
    "patch_price_display_settings",
    "head_price_display_settings",
    "get_price_display_settings_section",
    "patch_price_display_settings_section",
]

PriceDisplaySettingsPayload = Mapping[str, Any] | str | Dto


def get_price_display_settings(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PriceDisplaySettings]:
    """Read the whole area — ``GET /admin/settings/price_display_settings``."""
    return client.send_get_request(
        price_display_settings_urls.PRICE_DISPLAY_SETTINGS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PriceDisplaySettings,
    )


def patch_price_display_settings(
    client: Any,
    payload: PriceDisplaySettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PriceDisplaySettings]:
    """Write fields in one section or both — ``PATCH /admin/settings/price_display_settings``.
    The body must be wrapped in ``price_display_settings``."""
    require_payload(payload)
    return client.send_patch_request(
        price_display_settings_urls.PRICE_DISPLAY_SETTINGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PriceDisplaySettings,
    )


def head_price_display_settings(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/price_display_settings``."""
    return client.send_api_request(
        "HEAD",
        price_display_settings_urls.PRICE_DISPLAY_SETTINGS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_price_display_settings_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PriceDisplaySettings]:
    """Read one section — ``GET /admin/settings/price_display_settings/{section}``.
    ``.data`` is under the section's own key, with no ``group_meta``."""
    return client.send_get_request(
        price_display_settings_urls.PRICE_DISPLAY_SETTINGS_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PriceDisplaySettings,
    )


def patch_price_display_settings_section(
    client: Any,
    section: str,
    payload: PriceDisplaySettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PriceDisplaySettings]:
    """Write fields in one section — ``PATCH /admin/settings/price_display_settings/{section}``.
    The answer is computed: while ``customize`` is off, ``scopes`` follow ``enabled``."""
    require_payload(payload)
    return client.send_patch_request(
        price_display_settings_urls.PRICE_DISPLAY_SETTINGS_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PriceDisplaySettings,
    )
