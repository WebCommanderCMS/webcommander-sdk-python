"""Dashboard layout endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.dashboards import dashboards_urls
from webcommander.resources.dashboards.dashboards_dto import Dashboard, DashboardListing
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_dashboards",
    "create_dashboard",
    "get_dashboard",
    "patch_dashboard",
    "delete_dashboard",
]

DashboardPayload = Mapping[str, Any] | str | Dto


def list_dashboards(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DashboardListing]:
    """List the admin's layouts — ``GET /admin/dashboards``, ``{"dashboards": [...]}`` with no
    paging. Each row is ``id``, ``name``, ``default`` and the two timestamps, and exactly one row
    is the default."""
    return client.send_get_request(
        dashboards_urls.DASHBOARDS,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DashboardListing,
    )


def create_dashboard(
    client: Any,
    payload: DashboardPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Dashboard]:
    """Create a layout — ``POST /admin/dashboards``, answered ``201`` with the whole layout, bare
    and with no ``Location``. The body is bare and needs ``name``, unique among the admin's layouts
    (``409`` ``name_taken``); an empty body is ``400``. It starts as a copy of the layout named in
    ``copy_from`` or of the default one, then the sections and ``kpis`` sent are applied. Unknown
    fields are ignored."""
    require_payload(payload)
    return client.send_post_request(
        dashboards_urls.DASHBOARDS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Dashboard,
    )


def get_dashboard(
    client: Any,
    dashboard_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Dashboard]:
    """Read one layout by its ``id`` — ``GET /admin/dashboards/{dashboard_id}``, the layout bare.
    An unknown id is ``404`` ``not_found`` on ``dashboard_id``."""
    return client.send_get_request(
        dashboards_urls.DASHBOARD,
        path_params={"dashboard_id": dashboard_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Dashboard,
    )


def patch_dashboard(
    client: Any,
    dashboard_id: str,
    payload: DashboardPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Dashboard]:
    """Change only the fields sent — ``PATCH /admin/dashboards/{dashboard_id}``, answered ``200``
    with the whole layout. An empty body is ``400``; unknown fields are ignored. A blank ``name``
    or one over 60 characters is ``400``, a section key the layout does not have is ``400``, a
    standard section with a ``position`` is ``400`` and hiding ``contact`` is ``400``. ``default``
    ``true`` moves the store's default layout to this one."""
    require_payload(payload)
    return client.send_patch_request(
        dashboards_urls.DASHBOARD,
        path_params={"dashboard_id": dashboard_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Dashboard,
    )


def delete_dashboard(
    client: Any,
    dashboard_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one layout — ``DELETE /admin/dashboards/{dashboard_id}``, ``204`` with no body; the
    layout then reads ``404``."""
    return client.send_delete_request(
        dashboards_urls.DASHBOARD,
        path_params={"dashboard_id": dashboard_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
