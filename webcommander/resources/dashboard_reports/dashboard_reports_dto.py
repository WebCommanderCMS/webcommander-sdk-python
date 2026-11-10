"""Typed views over the dashboard report bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class ReportPeriod(Dto):
    """The period a report covers and the one before it, as dates; ``time_zone`` is the store's and
    ``currency`` the code money figures are in. ``duration`` is ``custom`` for a date range."""

    duration: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    previous_start_date: str | None = None
    previous_end_date: str | None = None
    time_zone: str | None = None
    currency: str | None = None


class ReportKpi(Dto):
    """One figure with the previous period's. ``format`` is ``money``, ``count`` or ``percent`` and
    ``direction`` is ``up``, ``down`` or ``flat``; ``change_percent`` is ``None`` when the previous
    value was zero. In ``trends`` there is no ``group``."""

    key: str | None = None
    code: str | None = None
    label: str | None = None
    group: str | None = None
    format: str | None = None
    value: float | None = None
    previous_value: float | None = None
    change_percent: float | None = None
    direction: str | None = None


class ReportOrders(Dto):
    """Order counts of the period."""

    count: int | None = None
    pending: int | None = None
    cancelled: int | None = None


class ReportSales(Dto):
    """Sales figures of the period, rounded to 2 decimals."""

    subtotal: float | None = None
    total: float | None = None
    items_sold: int | None = None
    average_order_value: float | None = None


class ReportCustomers(Dto):
    """Customers registered in the period."""

    new: int | None = None


class ReportProducts(Dto):
    """Products added in the period, and those out of stock now."""

    new: int | None = None
    out_of_stock: int | None = None


class ReportPageViews(Dto):
    """Page views of the period."""

    total: int | None = None
    unique: int | None = None


class ReportEntity(Dto):
    """A page, product or post by id and name."""

    id: int | None = None
    name: str | None = None


class ReportViewItem(Dto):
    """One row of the most viewed list: a ``page`` or, with ``entity_name`` ``product``, a
    ``product``."""

    page: ReportEntity | None = None
    product: ReportEntity | None = None
    views: int | None = None


class ReportViews(Dto):
    """The most viewed pages, or products when the query's ``entity_name`` is ``product``;
    ``entity`` says which."""

    entity: str | None = None
    items: list[ReportViewItem | None] | None = None


class QuickReport(Dto):
    """The quick report. ``kpis`` holds the 27 metrics, or only the ones the query's ``kpis`` names,
    in that order. Inside a summary only the grouped totals and ``view_report`` are present."""

    period: ReportPeriod | None = None
    kpis: list[ReportKpi | None] | None = None
    orders: ReportOrders | None = None
    sales: ReportSales | None = None
    customers: ReportCustomers | None = None
    products: ReportProducts | None = None
    page_views: ReportPageViews | None = None
    view_report: ReportViews | None = None
    trends: list[ReportKpi | None] | None = None


class SalesRow(Dto):
    """One row of the sales report: a day for a period up to a month, else a month. Without
    ``breakdown`` only the date fields, ``label``, ``month_name``, ``sales`` and ``total_sales``
    are present; ``day`` is present on day rows only."""

    date: str | None = None
    year: int | None = None
    month: int | None = None
    day: int | None = None
    label: str | None = None
    month_name: str | None = None
    sales: float | None = None
    total_sales: float | None = None
    orders: int | None = None
    orders_value: float | None = None
    gross_sales: float | None = None
    shipping: float | None = None
    handling: float | None = None
    tax: float | None = None
    discount: float | None = None
    refunds: float | None = None
    average_order_value: float | None = None
    top_product: ReportEntity | None = None


class SalesTotals(Dto):
    """The rows added up; ``sales`` always, the rest with ``breakdown``."""

    sales: float | None = None
    orders: int | None = None
    orders_value: float | None = None
    gross_sales: float | None = None
    shipping: float | None = None
    handling: float | None = None
    tax: float | None = None
    discount: float | None = None
    refunds: float | None = None
    average_order_value: float | None = None


class SalesReport(Dto):
    """The sales report. ``group_by`` is ``day`` for a period up to a month and ``month`` for a
    longer one; ``sort`` (``date`` or ``sales``) and ``order`` (``asc`` or ``desc``) echo what was
    applied. A period with no sales has no rows."""

    period: ReportPeriod | None = None
    group_by: str | None = None
    sort: str | None = None
    order: str | None = None
    rows: list[SalesRow | None] | None = None
    totals: SalesTotals | None = None


class OrderCount(Dto):
    """Orders placed in one month."""

    date: str | None = None
    year: int | None = None
    month: int | None = None
    count: int | None = None


class MostVisitedProduct(Dto):
    """A product and its views."""

    product: ReportEntity | None = None
    views: int | None = None


class BestSellingProduct(Dto):
    """A product and the units sold, highest first."""

    product: ReportEntity | None = None
    units_sold: int | None = None


class OrderUpdates(Dto):
    """What needs attention now; ``pending_fulfillment`` is the orders waiting to ship."""

    low_stock_items: int | None = None
    pending_fulfillment: int | None = None
    payments_to_capture: int | None = None


class SummaryReport(Dto):
    """The summary: every section of the Dashboard in one answer. ``quick_report`` has no
    ``kpis``."""

    period: ReportPeriod | None = None
    quick_report: QuickReport | None = None
    order_by_month: list[OrderCount | None] | None = None
    orders_over_time: list[OrderCount | None] | None = None
    sales_report: list[SalesRow | None] | None = None
    most_visited_products: list[MostVisitedProduct | None] | None = None
    best_selling_products: list[BestSellingProduct | None] | None = None
    order_updates: OrderUpdates | None = None
