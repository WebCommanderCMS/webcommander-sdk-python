"""Typed views over the country tax bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class TaxCountry(Dto):
    """A country as this family nests it, on a country tax's ``country``; ``null`` on the
    rest-of-the-world row."""

    id: int | None = None
    name: str | None = None
    code: str | None = None


class TaxState(Dto):
    """A state as a state rule nests it, on its ``state``."""

    id: int | None = None
    name: str | None = None
    code: str | None = None


class CountryTaxStateRule(Dto):
    """One entry of a country tax's ``state_rules``, which only the row path and the update send."""

    id: int | None = None
    name: str | None = None
    state: TaxState | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    post_code: str | None = None
    tax_rate: float | None = None
    tax_rule: str | None = None
    effective_tax_rate: float | None = None
    is_default: bool | None = None
    created_on: str | None = None
    last_updated_on: str | None = None
    last_updated_by: Any = None


class CountryTax(Dto):
    """One country tax; the row path and the update add ``state_rules`` to the twelve keys a
    listing row and the create answer carry. ``tax_method`` reads lower case."""

    ENVELOPE_KEY = "country_tax"

    id: int | None = None
    name: str | None = None
    country: TaxCountry | None = None
    tax_code: str | None = None
    tax_rate: float | None = None
    tax_method: str | None = None
    is_default: bool | None = None
    is_rest_of_world: bool | None = None
    state_rules_count: int | None = None
    created_on: str | None = None
    last_updated_on: str | None = None
    last_updated_by: Any = None
    state_rules: list[CountryTaxStateRule] | None = None


class CountryTaxInput(Dto):
    """The writable form of :class:`CountryTax`, shared by the create and the update.
    ``country_code`` is the create's one requirement; the update is a merge."""

    ENVELOPE_KEY = "country_tax"
    TOP_LEVEL = ("transaction_no",)

    country_code: str | None = None
    name: str | None = None
    tax_code: str | None = None
    tax_rate: float | None = None
    tax_method: str | None = None
    is_default: bool | None = None
    transaction_no: str | None = None


class ResourceMeta(Dto):
    """One ``group_meta`` entry: what the path is, whether it is writable and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block only the listing sends."""

    country_tax: ResourceMeta | None = None
    state_rules: ResourceMeta | None = None


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


class CountryTaxPage(Dto):
    """One page of the country tax listing: the rows, ``group_meta`` and the paging block."""

    country_taxes: list[CountryTax] | None = None
    group_meta: GroupMeta | None = None
    pagination: Pagination | None = None
