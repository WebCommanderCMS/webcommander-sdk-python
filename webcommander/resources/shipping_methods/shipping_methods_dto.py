"""Typed views over the shipping method bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class ShippingMethod(Dto):
    """One shipping method, the same three fields on the listing row and on the row path.
    ``is_default`` is exclusive and moves only through the default sub-path."""

    ENVELOPE_KEY = "shipping_method"

    id: int | None = None
    name: str | None = None
    is_default: bool | None = None
    field_metadata: Any = None


class ShippingMethodInput(Dto):
    """The writable form of :class:`ShippingMethod`: ``name``, the only field the store reads.
    Required, at most 100 characters, and unique, or the write is ``409``."""

    ENVELOPE_KEY = "shipping_method"

    name: str | None = None


class Pagination(Dto):
    """The ten-key ``pagination`` block; ``limit`` is the size the store applied, capped at 20."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    count: int | None = None
    current_page: int | None = None
    total_pages: int | None = None
    has_next: bool | None = None
    has_previous: bool | None = None
    previous_page: str | None = None
    next_page: str | None = None


class ShippingMethodPage(Dto):
    """One page of the listing: the rows, the block that says where they sit, and any schema."""

    shipping_methods: list[ShippingMethod] | None = None
    pagination: Pagination | None = None
    field_metadata: Any = None


class ShippingMethodCount(Dto):
    """The count sub-path's body, ``{"shipping_methods": {"count": N}}``."""

    ENVELOPE_KEY = "shipping_methods"

    count: int | None = None
