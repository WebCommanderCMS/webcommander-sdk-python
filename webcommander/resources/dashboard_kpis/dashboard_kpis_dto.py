"""Typed views over the dashboard KPI bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class DashboardRef(Dto):
    """The default layout the KPI tiles belong to; ``id`` is its ``dashboard_id``."""

    id: str | None = None
    name: str | None = None


class KpiPeriod(Dto):
    """The period a figure covers and the one before it, as dates; ``time_zone`` is the store's
    and ``currency`` the code money figures are in."""

    duration: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    previous_start_date: str | None = None
    previous_end_date: str | None = None
    time_zone: str | None = None
    currency: str | None = None


class KpiMetric(Dto):
    """One metric a tile can show. ``key`` is what a selection takes; ``code`` is the report's own
    name for it and differs for some, such as ``aov`` and ``average_order_value``."""

    key: str | None = None
    code: str | None = None
    label: str | None = None
    format: str | None = None
    in_use: bool | None = None


class KpiGroup(Dto):
    """A group of metrics: ``ecommerce``, ``content``, ``blog``, ``bookings`` or ``courses``."""

    key: str | None = None
    label: str | None = None
    metrics: list[KpiMetric | None] | None = None


class KpiOptions(Dto):
    """Every metric a tile can show. ``min`` and ``max`` bound the number of tiles, and
    ``selected`` lists the keys in use, in tile order."""

    dashboard: DashboardRef | None = None
    min: int | None = None
    max: int | None = None
    selected: list[str | None] | None = None
    groups: list[KpiGroup | None] | None = None


class KpiTile(Dto):
    """One selected tile with its figure. ``format`` is ``money``, ``count`` or ``percent`` and
    ``direction`` is ``up``, ``down`` or ``flat``; ``change_percent`` is ``None`` when the
    previous period was zero. Every count is a float on the wire."""

    position: int | None = None
    key: str | None = None
    code: str | None = None
    label: str | None = None
    group: str | None = None
    format: str | None = None
    value: float | None = None
    previous_value: float | None = None
    change_percent: float | None = None
    direction: str | None = None


class KpiSelection(Dto):
    """The tiles in use with their figures for the period; the read and the save answer alike."""

    dashboard: DashboardRef | None = None
    online_store: bool | None = None
    period: KpiPeriod | None = None
    selected: list[KpiTile | None] | None = None


class KpiSelectionInput(Dto):
    """The save body, bare: ``metrics`` is the full list of 2 to 5 distinct metric keys, in tile
    order. It replaces the default layout's tiles."""

    metrics: list[str | None] | None = None
