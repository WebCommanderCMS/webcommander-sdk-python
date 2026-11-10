"""Dashboard KPI endpoints, under ``/api/{api_version}/admin/dashboard``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.dashboard_kpis import dashboard_kpis_urls
from webcommander.resources.dashboard_kpis.dashboard_kpis_dto import KpiOptions, KpiSelection
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "get_dashboard_kpi_options",
    "get_dashboard_kpi_selection",
    "update_dashboard_kpi_selection",
]

DashboardKpiPayload = Mapping[str, Any] | str | Dto


def get_dashboard_kpi_options(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[KpiOptions]:
    """List the metrics a tile can show — ``GET /admin/dashboard/kpi_options``, grouped, with
    ``min`` 2 and ``max`` 5 tiles and the keys now in use under ``selected``. It reads the same
    tiles as ``kpi_selection``."""
    return client.send_get_request(
        dashboard_kpis_urls.DASHBOARD_KPI_OPTIONS,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=KpiOptions,
    )


def get_dashboard_kpi_selection(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[KpiSelection]:
    """Read the tiles in use with their figures — ``GET /admin/dashboard/kpi_selection``, the tiles
    of the default layout under ``selected`` in position order. ``duration`` (``last_30_days`` when
    left out) or ``start_date`` with ``end_date`` (``YYYY-MM-DD``, sent together) choose the
    period; a bad value is ``400``."""
    return client.send_get_request(
        dashboard_kpis_urls.DASHBOARD_KPI_SELECTION,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=KpiSelection,
    )


def update_dashboard_kpi_selection(
    client: Any,
    payload: DashboardKpiPayload,
    *,
    query_params: Mapping[str, Any] | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[KpiSelection]:
    """Save the tiles — ``PUT /admin/dashboard/kpi_selection`` with ``{"metrics": [...]}``, answered
    ``200`` like the read. The list replaces the default layout's tiles, which is store-wide state,
    and is read back at once by that layout and by ``kpi_options``. Fewer than 2 or more than 5, a
    repeat, an unknown key, a missing ``metrics`` and a non-list are ``400``. ``duration`` or the
    dates in the query set the period of the figures in the answer."""
    require_payload(payload)
    return client.send_put_request(
        dashboard_kpis_urls.DASHBOARD_KPI_SELECTION,
        json_body=payload,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=KpiSelection,
    )
