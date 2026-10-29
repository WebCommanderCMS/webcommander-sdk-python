"""Typed views over the tax profile bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class TaxProfileRuleCode(Dto):
    """The tax code a nested rule points at."""

    id: int | None = None
    name: str | None = None
    is_default: bool | None = None


class TaxProfileRuleZone(Dto):
    """One tax zone a nested rule points at."""

    id: int | None = None
    name: str | None = None
    is_system_generated: bool | None = None
    is_default: bool | None = None


class TaxProfileRule(Dto):
    """One tax rule as a profile nests it, the same ten keys a ``/admin/tax_rules`` read sends."""

    id: int | None = None
    name: str | None = None
    code: TaxProfileRuleCode | None = None
    description: str | None = None
    default: bool | None = None
    rounding_type: str | None = None
    decimal_point: int | None = None
    zones: list[TaxProfileRuleZone] | None = None
    created_at: str | None = None
    updated_at: str | None = None


class TaxProfile(Dto):
    """One tax profile, the same seven keys on the listing row and on the row path; a new
    profile's ``tax_rules`` is empty. ``default`` is exclusive: the row that held it loses it."""

    ENVELOPE_KEY = "tax_profile"

    id: int | None = None
    name: str | None = None
    description: str | None = None
    default: bool | None = None
    tax_rules: list[TaxProfileRule] | None = None
    created_at: str | None = None
    updated_at: str | None = None


class TaxProfileInput(Dto):
    """The writable form of :class:`TaxProfile`, shared by the create and the update; a merge.
    ``default`` is one-way: ``false`` leaves the flag on."""

    ENVELOPE_KEY = "tax_profile"

    name: str | None = None
    description: str | None = None
    default: bool | None = None


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


class TaxProfilePage(Dto):
    """One page of the tax profile listing: the rows, and the block that says where they sit."""

    tax_profiles: list[TaxProfile] | None = None
    pagination: Pagination | None = None
