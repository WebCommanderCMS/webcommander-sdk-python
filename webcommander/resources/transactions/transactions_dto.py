"""Typed views over the transaction-number bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class TransactionListEntry(Dto):
    """One listing row: a number, how many records carry it, and its read path."""

    transaction_no: str | None = None
    total_records: int | None = None
    url: str | None = None


class TransactionTypeCount(Dto):
    """One ``by_type`` row of a number's read: ``count`` is ``created`` plus ``updated``, and
    ``trashed`` counts those of them now in the trash. ``items_url`` is sent on every row,
    ``count`` ``0`` included; it form-encodes the number, so a space arrives as ``+``."""

    type: str | None = None
    count: int | None = None
    created: int | None = None
    updated: int | None = None
    trashed: int | None = None
    items_url: str | None = None


class Transaction(Dto):
    """One number's read: a bare body, its 15 ``by_type`` rows always in the same order."""

    transaction_no: str | None = None
    total_records: int | None = None
    by_type: list[TransactionTypeCount | None] | None = None


class TransactionItem(Dto):
    """One record under a number, as ``detail=slim`` sends it: ``type``, ``id``, ``stamp``
    (``created`` or ``updated``), ``trashed`` and the fields of its ``type``. ``category`` sends
    ``name`` and ``url``; ``product`` and ``product_variation`` add ``sku``; ``product_review``
    adds ``rating``; ``customer`` sends ``email``, ``first_name``, ``last_name`` and ``url``;
    ``order`` sends ``order_no``, ``grand_total``, ``status`` and a ``url`` ending in
    ``order_no``; ``currency`` adds ``code`` and ``symbol``;
    ``custom_tax_profile`` adds ``code``; ``custom_tax_rule`` sends ``name`` alone;
    ``custom_tax_rule_zone`` sends ``country_code``, ``state_name``, ``postcode``, ``rate`` and
    ``priority``; ``shipping_profile`` adds ``description``; ``shipping_rate`` adds
    ``policy_type``. A field the type does not send reads ``None``. Under ``detail=full`` a row
    is the record's own read body, which stays in ``response.map``."""

    type: str | None = None
    id: int | None = None
    stamp: str | None = None
    trashed: bool | None = None
    name: str | None = None
    sku: str | None = None
    rating: float | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    order_no: int | None = None
    grand_total: float | None = None
    status: str | None = None
    code: str | None = None
    symbol: str | None = None
    country_code: str | None = None
    state_name: str | None = None
    postcode: str | None = None
    rate: float | None = None
    priority: int | None = None
    description: str | None = None
    policy_type: str | None = None
    url: str | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block of both listings; ``limit`` is the page size applied.
    There is no next-page link, so step ``offset``."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class TransactionPage(Dto):
    """One page of the numbers; a ``transaction_no`` filter answers ``pagination`` too."""

    transactions: list[TransactionListEntry | None] | None = None
    pagination: Pagination | None = None


class TransactionItemPage(Dto):
    """One page of the records carrying a number, beside the number; each item names its own
    ``type``. A number or a type with no records answers ``items`` empty and ``pagination.total``
    ``0``."""

    transaction_no: str | None = None
    items: list[TransactionItem | None] | None = None
    pagination: Pagination | None = None
