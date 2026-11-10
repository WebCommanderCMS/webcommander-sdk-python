"""Typed views over the dashboard section bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class SectionPeriod(Dto):
    """The period a section covers and the one before it, as dates; ``time_zone`` is the store's
    and ``currency`` the code money figures are in."""

    duration: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    previous_start_date: str | None = None
    previous_end_date: str | None = None
    time_zone: str | None = None
    currency: str | None = None


class SectionEntity(Dto):
    """A product, page or post by id and name."""

    id: int | None = None
    name: str | None = None


class SectionOrderUpdates(Dto):
    """What needs attention now; ``pending_fulfillment`` is the orders waiting to ship."""

    low_stock_items: int | None = None
    pending_fulfillment: int | None = None
    payments_to_capture: int | None = None


class SectionBestSeller(Dto):
    """A product and the units sold, highest first."""

    product: SectionEntity | None = None
    units_sold: int | None = None


class SectionContentUpdate(Dto):
    """One content item to review; ``count`` is an empty string on the rows measured."""

    key: str | None = None
    label: str | None = None
    count: str | None = None


class SectionTopPage(Dto):
    """A page and its views."""

    page: SectionEntity | None = None
    views: int | None = None


class SectionNeedsAttention(Dto):
    """The bookings that need attention: how many, and the latest of them."""

    count: int | None = None
    # Empty on the store measured, so the row's shape is not known.
    latest: list[Any] | None = None


class SectionDraft(Dto):
    """A blog draft waiting to be published."""

    post: SectionEntity | None = None
    updated_at: str | None = None


class SectionDrafts(Dto):
    """The blog drafts to publish: how many, and the latest."""

    count: int | None = None
    latest: list[SectionDraft | None] | None = None


class SectionViewedPost(Dto):
    """A blog post and its views."""

    post: SectionEntity | None = None
    views: int | None = None


class DashboardSectionReport(Dto):
    """One tab of the Dashboard. ``section`` echoes the path value, and only the fields of that
    tab are present. ``ecommerce``: ``order_updates``, ``best_selling_products``. ``content``:
    ``content_updates``, ``top_pages``. ``bookings``: ``needs_attention``, ``upcoming``.
    ``courses``: ``new_enrolments``, ``unpaid_orders``, ``popular_courses``. ``blog``:
    ``comments_to_moderate``, ``drafts_to_publish``, ``most_viewed_posts``."""

    section: str | None = None
    period: SectionPeriod | None = None
    order_updates: SectionOrderUpdates | None = None
    best_selling_products: list[SectionBestSeller | None] | None = None
    content_updates: list[SectionContentUpdate | None] | None = None
    top_pages: list[SectionTopPage | None] | None = None
    needs_attention: SectionNeedsAttention | None = None
    # Empty on the store measured, so the row's shape is not known.
    upcoming: list[Any] | None = None
    new_enrolments: int | None = None
    unpaid_orders: int | None = None
    popular_courses: list[Any] | None = None
    comments_to_moderate: int | None = None
    drafts_to_publish: SectionDrafts | None = None
    most_viewed_posts: list[SectionViewedPost | None] | None = None
