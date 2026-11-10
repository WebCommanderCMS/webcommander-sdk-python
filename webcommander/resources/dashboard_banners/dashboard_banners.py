"""Dashboard banner endpoints, under ``/api/{api_version}/admin/dashboard``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.dashboard_banners import dashboard_banners_urls
from webcommander.resources.dashboard_banners.dashboard_banners_dto import (
    DashboardBanner,
    DashboardBannerListing,
    DashboardContentInfo,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_dashboard_banners",
    "create_dashboard_banner",
    "get_dashboard_banner",
    "patch_dashboard_banner",
    "delete_dashboard_banner",
    "get_dashboard_content_info",
]

DashboardBannerPayload = Mapping[str, Any] | str | Dto


def list_dashboard_banners(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DashboardBannerListing]:
    """List every banner, active or not — ``GET /admin/dashboard/banners``,
    ``{"banners": [...]}`` in position order, positions counting from 1 without a gap."""
    return client.send_get_request(
        dashboard_banners_urls.DASHBOARD_BANNERS,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DashboardBannerListing,
    )


def create_dashboard_banner(
    client: Any,
    payload: DashboardBannerPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DashboardBanner]:
    """Create a banner — ``POST /admin/dashboard/banners``, answered ``201`` with the banner bare
    and no ``Location``. The body is bare; every failing field is listed in one ``400``, a ``key``
    already used is ``400`` ``duplicate``, an unknown field is ``400``. It joins the Dashboard feed
    at once while ``active``."""
    require_payload(payload)
    return client.send_post_request(
        dashboard_banners_urls.DASHBOARD_BANNERS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DashboardBanner,
    )


def get_dashboard_banner(
    client: Any,
    banner_key: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DashboardBanner]:
    """Read one banner by its ``key`` — ``GET /admin/dashboard/banners/{banner_key}``, the banner
    bare, hidden ones included. An unknown key is ``404``."""
    return client.send_get_request(
        dashboard_banners_urls.DASHBOARD_BANNER,
        path_params={"banner_key": banner_key},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DashboardBanner,
    )


def patch_dashboard_banner(
    client: Any,
    banner_key: str,
    payload: DashboardBannerPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DashboardBanner]:
    """Change only the fields sent — ``PATCH /admin/dashboard/banners/{banner_key}``, answered
    ``200`` with the banner. An empty body, a blank ``title``, a ``key`` and an unknown field are
    ``400``; an unknown banner is ``404``. ``learn_more`` and ``try_it`` are replaced whole, and
    ``try_it`` ``None`` removes the second button. ``updated_at`` is not moved."""
    require_payload(payload)
    return client.send_patch_request(
        dashboard_banners_urls.DASHBOARD_BANNER,
        path_params={"banner_key": banner_key},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DashboardBanner,
    )


def delete_dashboard_banner(
    client: Any,
    banner_key: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one banner — ``DELETE /admin/dashboard/banners/{banner_key}``, ``204`` with no body.
    The banners after it move up, so the positions stay without a gap; an unknown key is
    ``404``."""
    return client.send_delete_request(
        dashboard_banners_urls.DASHBOARD_BANNER,
        path_params={"banner_key": banner_key},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_dashboard_content_info(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DashboardContentInfo]:
    """Read what the Dashboard shows besides the figures — ``GET /admin/dashboard/content_info``:
    the active banners under ``banners``, the support card under ``contact``, ``online_store`` and
    ``member_label``. A hidden banner is not listed."""
    return client.send_get_request(
        dashboard_banners_urls.DASHBOARD_CONTENT_INFO,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DashboardContentInfo,
    )
