"""Typed views over the tax rule bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class TaxRuleCode(Dto):
    """The tax code a rule points at; no write on the rule resource sets it."""

    id: int | None = None
    name: str | None = None
    is_default: bool | None = None


class TaxRuleZone(Dto):
    """One tax zone a rule points at, as the rule nests it; no write sets this list."""

    id: int | None = None
    name: str | None = None
    is_system_generated: bool | None = None
    is_default: bool | None = None


class TaxRule(Dto):
    """One tax rule, the same ten keys on the listing row and on the row path.
    ``code``, ``zones``, ``decimal_point`` and ``rounding_type`` are read-only."""

    ENVELOPE_KEY = "tax_rule"

    id: int | None = None
    name: str | None = None
    code: TaxRuleCode | None = None
    description: str | None = None
    default: bool | None = None
    rounding_type: str | None = None
    decimal_point: int | None = None
    zones: list[TaxRuleZone] | None = None
    created_at: str | None = None
    updated_at: str | None = None


class TaxRuleInput(Dto):
    """The writable form of :class:`TaxRule`: ``name`` and ``description``, the two fields read.
    The update is a merge."""

    ENVELOPE_KEY = "tax_rule"

    name: str | None = None
    description: str | None = None


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


class TaxRulePage(Dto):
    """One page of the tax rule listing: the rows, and the block that says where they sit."""

    tax_rules: list[TaxRule] | None = None
    pagination: Pagination | None = None
