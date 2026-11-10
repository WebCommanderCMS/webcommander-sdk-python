"""Dashboard report endpoints, under ``/api/{api_version}/admin/dashboard/reports``. Every report
takes the same period query: ``duration`` (``today``, ``yesterday``, ``last_24_hours``,
``last_7_days``, ``last_30_days``, ``this_month``, ``last_month``, ``last_3_months``,
``last_6_months``, ``last_12_months``, ``last_24_months``, ``last_36_months``,
``last_48_months``, ``last_60_months`` or ``custom``; ``last_30_days`` when left out) or
``start_date`` with ``end_date`` (``YYYY-MM-DD``, sent together, not reversed and not in the
future). A bad value, a repeated ``duration`` and a lone date are ``400`` with every bad field
listed; a name the report does not know is ignored."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.resources.dashboard_reports import dashboard_reports_urls
from webcommander.resources.dashboard_reports.dashboard_reports_dto import (
    QuickReport,
    SalesReport,
    SummaryReport,
)

__all__ = [
    "get_dashboard_report_quick",
    "head_dashboard_report_quick",
    "get_dashboard_report_sales",
    "head_dashboard_report_sales",
    "get_dashboard_report_summary",
    "head_dashboard_report_summary",
]


def get_dashboard_report_quick(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[QuickReport]:
    """Read the quick report — ``GET /admin/dashboard/reports/quick``: ``period``, ``kpis``,
    grouped totals, the most viewed pages under ``view_report`` and ``trends``. ``kpis`` is a
    comma list of metric keys (an unknown one is ``400``) that narrows ``kpis`` to those, in that
    order; ``entity_name`` is ``page`` (the default) or ``product`` and picks what ``view_report``
    ranks."""
    return client.send_get_request(
        dashboard_reports_urls.DASHBOARD_REPORT_QUICK,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=QuickReport,
    )


def head_dashboard_report_quick(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the quick report is reachable — ``HEAD /admin/dashboard/reports/quick``; the
    status of the read, with no body. It runs the read's query, so a bad value is ``400``."""
    return client.send_api_request(
        "HEAD",
        dashboard_reports_urls.DASHBOARD_REPORT_QUICK,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_dashboard_report_sales(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SalesReport]:
    """Read the sales report — ``GET /admin/dashboard/reports/sales``: ``rows`` by day or month and
    ``totals``. ``breakdown`` (``true`` or ``false``) adds orders, shipping, tax, discount, refunds
    and the top product to each row and total; ``sort`` is ``date`` (the default) or ``sales`` and
    ``order`` is ``asc`` (the default) or ``desc``; any other value is ``400``."""
    return client.send_get_request(
        dashboard_reports_urls.DASHBOARD_REPORT_SALES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SalesReport,
    )


def head_dashboard_report_sales(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the sales report is reachable — ``HEAD /admin/dashboard/reports/sales``; the
    status of the read, with no body. It runs the read's query, so a bad value is ``400``."""
    return client.send_api_request(
        "HEAD",
        dashboard_reports_urls.DASHBOARD_REPORT_SALES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_dashboard_report_summary(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SummaryReport]:
    """Read the summary — ``GET /admin/dashboard/reports/summary``: the quick report without
    ``kpis``, orders by month, sales rows, the most visited and best selling products and the
    order updates, in one answer. ``compare_previous`` (``true`` or ``false``) is checked as a
    boolean; any other value is ``400``."""
    return client.send_get_request(
        dashboard_reports_urls.DASHBOARD_REPORT_SUMMARY,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SummaryReport,
    )


def head_dashboard_report_summary(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the summary is reachable — ``HEAD /admin/dashboard/reports/summary``; the
    status of the read, with no body. It runs the read's query, so a bad value is ``400``."""
    return client.send_api_request(
        "HEAD",
        dashboard_reports_urls.DASHBOARD_REPORT_SUMMARY,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
