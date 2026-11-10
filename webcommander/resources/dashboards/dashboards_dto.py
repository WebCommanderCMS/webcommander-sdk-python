"""Typed views over the dashboard layout bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class DashboardPart(Dto):
    """One part of the ``seo`` section. Read back, the title and ``can_hide`` come with it; a write
    needs only ``key`` and ``visible``. The ``kpis`` part cannot be hidden."""

    key: str | None = None
    title: str | None = None
    visible: bool | None = None
    can_hide: bool | None = None


class DashboardTab(Dto):
    """One tab of the ``section_tabs`` section: ``ecommerce``, ``content``, ``bookings``,
    ``courses`` or ``blog``. A write needs ``key`` and sets ``visible`` or ``position``, counted
    from 1 among the tabs."""

    key: str | None = None
    title: str | None = None
    description: str | None = None
    visible: bool | None = None
    can_hide: bool | None = None
    position: int | None = None


class DashboardSection(Dto):
    """A section of a layout. The standard ones are ``announcement``, ``performance``, ``activity``
    and ``contact``; they only show or hide, and ``contact`` cannot hide. The customisable ones are
    ``setup_guide``, ``section_tabs`` (with ``tabs``) and ``seo`` (with ``parts``); they also take
    a ``position``. Read back, the title, description and ``can_hide`` come with it; a write needs
    only ``key`` and what changes."""

    key: str | None = None
    title: str | None = None
    description: str | None = None
    visible: bool | None = None
    can_hide: bool | None = None
    position: int | None = None
    tabs: list[DashboardTab | None] | None = None
    parts: list[DashboardPart | None] | None = None


class DashboardKpi(Dto):
    """One KPI tile of a layout, in tile order. ``key`` is a ``kpi_options`` metric key."""

    position: int | None = None
    key: str | None = None
    label: str | None = None
    group: str | None = None


class Dashboard(Dto):
    """One layout. ``id`` is the ``dashboard_id`` of the other calls, a UUID. Exactly one layout
    is the default."""

    id: str | None = None
    name: str | None = None
    default: bool | None = None
    standard_sections: list[DashboardSection | None] | None = None
    customisable_sections: list[DashboardSection | None] | None = None
    kpis: list[DashboardKpi | None] | None = None
    created_at: str | None = None
    updated_at: str | None = None


class DashboardSummary(Dto):
    """A layout as the listing shows it, without its sections and tiles."""

    id: str | None = None
    name: str | None = None
    default: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None


class DashboardListing(Dto):
    """The listing: every layout of the admin, with no paging."""

    dashboards: list[DashboardSummary | None] | None = None


class DashboardInput(Dto):
    """The write body, bare. A create needs ``name``, unique among the admin's layouts (``409``);
    it starts as a copy of the ``copy_from`` layout, the default one when that is left out. A patch
    sends only what changes; the sections named are merged into the layout, the rest is kept.
    ``kpis`` is the full list of 2 to 5 metric keys in tile order. A standard section takes no
    ``position`` (``400``). ``default`` ``true`` makes this layout the store's default layout;
    ``false`` on the default layout is ``409``, as the default moves only by making another layout
    the default."""

    name: str | None = None
    default: bool | None = None
    copy_from: str | None = None
    standard_sections: list[DashboardSection | None] | None = None
    customisable_sections: list[DashboardSection | None] | None = None
    kpis: list[str | None] | None = None
