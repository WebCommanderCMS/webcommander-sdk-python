"""Typed views over the shipping class bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class ShippingClass(Dto):
    """One shipping class: a listing row, or a row path's ``shipping_class`` record, the same four
    fields either way."""

    ENVELOPE_KEY = "shipping_class"

    id: int | None = None
    name: str | None = None
    description: str | None = None
    is_default: bool | None = None
    field_metadata: Any = None


class ShippingClassInput(Dto):
    """The body both writes take: ``name``, required, unique and 50 characters or fewer, and
    ``description``, 100 characters or fewer."""

    ENVELOPE_KEY = "shipping_class"

    name: str | None = None
    description: str | None = None


class Pagination(Dto):
    """The listing's ten-key ``pagination`` block; ``limit`` is the size the store applied."""

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


class ShippingClassPage(Dto):
    """One page of the listing, with the ``field_metadata`` block when it was asked for."""

    shipping_classes: list[ShippingClass] | None = None
    pagination: Pagination | None = None
    field_metadata: Any = None


class ShippingClassCount(Dto):
    """The count sub-path's ``{"shipping_classes": {"count": N}}``."""

    ENVELOPE_KEY = "shipping_classes"

    count: int | None = None
