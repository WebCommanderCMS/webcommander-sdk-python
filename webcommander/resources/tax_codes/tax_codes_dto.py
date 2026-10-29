"""Typed views over the tax code bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class TaxCode(Dto):
    """One tax code, the same eight keys on the listing row and on the row path.
    ``default`` is read-only and not exclusive: it marks a code the store built."""

    ENVELOPE_KEY = "tax_code"

    id: int | None = None
    name: str | None = None
    label: str | None = None
    description: str | None = None
    rate: float | None = None
    resolver_type: str | None = None
    priority: int | None = None
    default: bool | None = None


class TaxCodeInput(Dto):
    """The writable form of :class:`TaxCode`, shared by the create and the update.
    The update resets ``priority`` and ``resolver_type`` when they are left unset."""

    ENVELOPE_KEY = "tax_code"

    name: str | None = None
    label: str | None = None
    description: str | None = None
    rate: float | None = None
    resolver_type: str | None = None
    priority: int | None = None


class Pagination(Dto):
    """The ten-key ``pagination`` block; ``limit`` is the size the store applied, capped at 100."""

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


class TaxCodePage(Dto):
    """One page of the tax code listing: the rows, and the block that says where they sit."""

    tax_codes: list[TaxCode] | None = None
    pagination: Pagination | None = None
