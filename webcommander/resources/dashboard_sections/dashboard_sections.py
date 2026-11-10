"""Dashboard section endpoints, under ``/api/{api_version}/admin/dashboard/sections``. The Dashboard
shows five tabs; a tab is a path value."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.resources.dashboard_sections import dashboard_sections_urls
from webcommander.resources.dashboard_sections.dashboard_sections_dto import (
    DashboardSectionReport,
)

__all__ = ["get_dashboard_section"]


def get_dashboard_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DashboardSectionReport]:
    """Read one tab — ``GET /admin/dashboard/sections/{section}``, ``section`` being one of
    ``DASHBOARD_SECTIONS`` (``ecommerce``, ``content``, ``bookings``, ``courses``, ``blog``); the
    answer is bare, ``section`` echoing it, with ``period`` and that tab's own fields. Any other
    value is ``404`` ``not_found`` on ``key``. ``duration`` or ``start_date`` with ``end_date``
    choose the period, as in the reports."""
    return client.send_get_request(
        dashboard_sections_urls.DASHBOARD_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DashboardSectionReport,
    )
