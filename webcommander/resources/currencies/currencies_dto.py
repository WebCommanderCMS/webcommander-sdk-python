"""Typed views over the currency bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class CurrencyCountry(Dto):
    """The country a currency is filed under, as every row answers it."""

    id: int | None = None
    code: str | None = None
    name: str | None = None


class Currency(Dto):
    """One currency: a listing row, the row path's body and every row write's answer. The base
    write answers only ``id``, ``name``, ``code`` and ``base`` of it."""

    ENVELOPE_KEY = "currency"

    id: int | None = None
    name: str | None = None
    code: str | None = None
    symbol: str | None = None
    country: CurrencyCountry | None = None
    conversion_rate: float | None = None
    rounding: str | None = None
    precision: int | None = None
    active: bool | None = None
    base: bool | None = None
    updated_at: str | None = None
    field_metadata: Any = None


class CurrencyInput(Dto):
    """The writable fields, for the create, the ``PUT`` replace and the ``PATCH``; no envelope.
    ``country`` takes a country's id, code, name or ``{"code": ...}``."""

    name: str | None = None
    code: str | None = None
    symbol: str | None = None
    country: int | str | CurrencyCountry | None = None
    conversion_rate: float | None = None
    rounding: str | None = None
    precision: int | None = None
    active: bool | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block; ``limit`` is the page size applied."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class CurrencyPage(Dto):
    """One page of the listing: the rows, where they sit and any schema."""

    currencies: list[Currency | None] | None = None
    pagination: Pagination | None = None
    field_metadata: Any = None


class CurrencyCount(Dto):
    """The count sub-path's body, a bare ``{"total": N}``."""

    total: int | None = None


class CurrencyReference(Dto):
    """The row that held the base flag before a base write."""

    id: int | None = None
    code: str | None = None
    name: str | None = None


class CurrencyBaseChange(Dto):
    """The base write's body: the new base, and the row that held the flag or ``None``."""

    currency: Currency | None = None
    previous_base: CurrencyReference | None = None
