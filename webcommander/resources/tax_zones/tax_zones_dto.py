"""Typed views over the tax zone bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class TaxCountry(Dto):
    """A country as this family nests it; a zone write sends this record, never a bare id."""

    id: int | None = None
    name: str | None = None
    code: str | None = None


class TaxState(Dto):
    """A state as a tax zone nests it in ``states``; a zone write sends this record."""

    id: int | None = None
    name: str | None = None
    code: str | None = None


class TaxZone(Dto):
    """One tax zone, the same twelve keys on the listing row and on the row path.
    ``post_code`` reads as the flat list of strings a write sends."""

    ENVELOPE_KEY = "tax_zone"

    id: int | None = None
    name: str | None = None
    system_generated: bool | None = None
    default: bool | None = None
    use_radius: bool | None = None
    radius: float | None = None
    start_location: str | None = None
    countries: list[TaxCountry] | None = None
    states: list[TaxState] | None = None
    post_code: list[str] | None = None
    created_at: str | None = None
    updated_at: str | None = None


class TaxZoneInput(Dto):
    """The writable form of :class:`TaxZone`, shared by the create and the update.
    ``name`` is required by both, and the update empties any list left unset."""

    ENVELOPE_KEY = "tax_zone"

    name: str | None = None
    countries: list[TaxCountry] | None = None
    states: list[TaxState] | None = None
    post_code: list[str] | None = None
    radius: float | None = None
    start_location: str | None = None
    use_radius: bool | None = None


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


class TaxZonePage(Dto):
    """One page of the tax zone listing: the rows, and the block that says where they sit."""

    tax_zones: list[TaxZone] | None = None
    pagination: Pagination | None = None
