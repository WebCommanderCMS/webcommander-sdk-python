"""Typed views over the dashboard banner bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class BannerStep(Dto):
    """One step of an ``open_modal`` banner's walkthrough."""

    title: str | None = None
    description: str | None = None


class BannerLearnMore(Dto):
    """What the banner's learn-more button does. ``action`` is ``open_link``, with an ``https``
    ``url``, or ``open_modal``, with a ``title``, a ``subtitle`` and at least one of ``steps``. A
    patch replaces the whole block, so an ``open_modal`` block sent over an ``open_link`` one drops
    the ``url``."""

    action: str | None = None
    label: str | None = None
    url: str | None = None
    title: str | None = None
    subtitle: str | None = None
    steps: list[BannerStep | None] | None = None


class BannerTryIt(Dto):
    """The optional second button; both fields are needed."""

    label: str | None = None
    url: str | None = None


class DashboardBanner(Dto):
    """One banner. ``key`` is the ``banner_key`` of the other calls. ``position`` counts from 1
    over every banner, hidden ones included, and ``active`` false hides it from the Dashboard
    feed only."""

    key: str | None = None
    position: int | None = None
    active: bool | None = None
    icon: str | None = None
    title: str | None = None
    description: str | None = None
    tags: list[str | None] | None = None
    learn_more: BannerLearnMore | None = None
    try_it: BannerTryIt | None = None
    created_at: str | None = None
    updated_at: str | None = None


class DashboardBannerListing(Dto):
    """The management list: every banner, active or not, in position order."""

    banners: list[DashboardBanner | None] | None = None


class DashboardBannerInput(Dto):
    """The write body, bare. A create needs ``key`` (``a-z``, ``0-9`` and ``_``, starting with a
    letter, up to 64 characters, unique), ``title`` (1 to 80 characters), ``description`` (1 to
    200) and ``learn_more``; ``tags`` holds at most 3, ``active`` defaults to ``true`` and
    ``position`` to the end of the list. A patch sends only what changes and cannot send ``key``.
    ``icon`` is stored as sent. ``position`` runs from 1 to one past the banner count, and the
    banners after it shift down."""

    key: str | None = None
    icon: str | None = None
    title: str | None = None
    description: str | None = None
    tags: list[str | None] | None = None
    learn_more: BannerLearnMore | None = None
    try_it: BannerTryIt | None = None
    position: int | None = None
    active: bool | None = None


class BannerContact(Dto):
    """The support card of the Dashboard."""

    email: str | None = None
    phone: str | None = None
    live_chat: str | None = None
    help_center_url: str | None = None


class DashboardContentInfo(Dto):
    """The Dashboard's feed: only the active banners, in position order, the support card, whether
    the store is an online store and the label of the membership."""

    banners: list[DashboardBanner | None] | None = None
    contact: BannerContact | None = None
    online_store: bool | None = None
    member_label: str | None = None
