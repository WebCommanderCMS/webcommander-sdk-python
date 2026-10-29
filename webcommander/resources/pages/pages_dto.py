"""Typed views over the page bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class PageReference(Dto):
    """An ``{id, name}`` pair: the layout, an access-list customer or group, the navigation and
    the author. A write names one by ``{"id": ...}``; ``name`` is read-only."""

    id: int | None = None
    name: str | None = None


class PagePasswordProtection(Dto):
    """The password gate. A listing row masks the password as ``***``; the row read and the
    writes answer it as saved, and switching it off keeps the stored password."""

    enabled: bool | None = None
    password: str | None = None


class PageMenuPlacement(Dto):
    """Whether the page is linked from a navigation; ``navigation`` is ``None`` when it is not,
    and must be ``{"id": ...}`` when a write sends ``enabled`` true."""

    enabled: bool | None = None
    navigation: PageReference | None = None


class PagePublishing(Dto):
    """The draft and approval state; the draft and published ids are ``None``, never ``0``."""

    draft: bool | None = None
    draft_page_id: int | None = None
    published_page_id: int | None = None
    pending_approval: bool | None = None
    pending_approval_count: int | None = None
    pending_approval_ids: list[int | None] | None = None
    disposable: bool | None = None


class Page(Dto):
    """One page: a listing row, the row read and every write's answer, the same 23 keys.
    ``visibility`` is ``open``, ``hidden`` or ``restricted``; ``visible_to`` is ``all`` or
    ``selected`` on a restricted page and ``None`` otherwise."""

    ENVELOPE_KEY = "page"

    id: int | None = None
    name: str | None = None
    title: str | None = None
    subtitle: str | None = None
    url: str | None = None
    full_url: str | None = None
    layout: PageReference | None = None
    visibility: str | None = None
    visible_to: str | None = None
    customers: list[PageReference | None] | None = None
    customer_groups: list[PageReference | None] | None = None
    body_class: str | None = None
    password_protection: PagePasswordProtection | None = None
    menu_placement: PageMenuPlacement | None = None
    active: bool | None = None
    disable_tracking: bool | None = None
    landing: bool | None = None
    in_trash: bool | None = None
    publishing: PagePublishing | None = None
    # None on every page the store holds; no store-bound page could be read to type it.
    store: Any = None
    author: PageReference | None = None
    created_at: str | None = None
    updated_at: str | None = None


class PageInput(Dto):
    """The writable fields, wrapped in ``page``, for the create, the ``PUT`` replace and the
    ``PATCH``. ``customers`` take public ``customer_id`` values, groups their ids, either bare
    or as ``{"id": ...}``. Fields left ``None`` are not sent: to clear one, pass a mapping."""

    ENVELOPE_KEY = "page"

    name: str | None = None
    title: str | None = None
    subtitle: str | None = None
    url: str | None = None
    layout: PageReference | None = None
    visibility: str | None = None
    visible_to: str | None = None
    customers: list[int | PageReference] | None = None
    customer_groups: list[int | PageReference] | None = None
    body_class: str | None = None
    password_protection: PagePasswordProtection | None = None
    menu_placement: PageMenuPlacement | None = None
    active: bool | None = None
    disable_tracking: bool | None = None


class PageUrlInput(Dto):
    """The URL write's bare body, ``{"url": ...}``; a ``page`` wrapper is ``400``."""

    url: str | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block; ``limit`` is the page size applied, the total under
    ``limit=all``."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class PageListing(Dto):
    """One page of the listing: the rows, outside the trash, and where they sit."""

    pages: list[Page | None] | None = None
    pagination: Pagination | None = None


class PageCount(Dto):
    """The count sub-path's body, a bare ``{"total": N}``."""

    total: int | None = None


class PageDeleteBlocker(Dto):
    """One reason the page cannot be deleted, such as ``landing_page``."""

    code: str | None = None
    message: str | None = None


class PageDeleteBlockers(Dto):
    """The delete check's body: whether a delete would pass, what blocks it and what links to
    the page. ``linked`` was empty on every page read, so its rows stay untyped."""

    can_delete: bool | None = None
    blockers: list[PageDeleteBlocker | None] | None = None
    linked: list[Any] | None = None
