"""Site settings endpoints, under ``/api/{api_version}/admin/settings/site_settings``.
The area is a facade over eight sections; a section is a path value."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.site_settings import site_settings_urls
from webcommander.resources.settings.site_settings.site_settings_dto import SiteSettings

__all__ = [
    "get_site_settings",
    "patch_site_settings",
    "head_site_settings",
    "get_site_settings_section",
    "patch_site_settings_section",
]

SiteSettingsPayload = Mapping[str, Any] | str | Dto


def get_site_settings(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SiteSettings]:
    """Read the whole area — ``GET /admin/settings/site_settings``, every section inlined."""
    return client.send_get_request(
        site_settings_urls.SITE_SETTINGS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SiteSettings,
    )


def patch_site_settings(
    client: Any,
    payload: SiteSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SiteSettings]:
    """Write fields in one or more sections — ``PATCH /admin/settings/site_settings``.
    A key whose value is not a mapping is ignored with a ``200``, so nest each section's fields."""
    require_payload(payload)
    return client.send_patch_request(
        site_settings_urls.SITE_SETTINGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SiteSettings,
    )


def head_site_settings(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/site_settings``; no body."""
    return client.send_api_request(
        "HEAD",
        site_settings_urls.SITE_SETTINGS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_site_settings_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SiteSettings]:
    """Read one section — ``GET /admin/settings/site_settings/{section}``.
    ``.data`` is under the section's own key, with no ``group_meta``."""
    return client.send_get_request(
        site_settings_urls.SITE_SETTINGS_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SiteSettings,
    )


def patch_site_settings_section(
    client: Any,
    section: str,
    payload: SiteSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SiteSettings]:
    """Write fields in one section — ``PATCH /admin/settings/site_settings/{section}``.
    Name only the fields moved: two secrets read back as ``***``, and an echo stores the mask."""
    require_payload(payload)
    return client.send_patch_request(
        site_settings_urls.SITE_SETTINGS_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SiteSettings,
    )
