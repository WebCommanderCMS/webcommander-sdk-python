"""Typed views over the shipping rate bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class ShippingReference(Dto):
    """An ``{id, name}`` pair: a rule that uses the rate."""

    id: int | None = None
    name: str | None = None


class ShippingCost(Dto):
    """A shipping or handling cost; ``type`` is ``fixed`` or ``percent``."""

    amount: float | None = None
    type: str | None = None


class ShippingAdditionalRule(Dto):
    """The charge for each item past the first; the other two keys read ``None`` while
    ``enabled`` is false, and ``enabled`` true needs both."""

    enabled: bool | None = None
    for_each_additional: int | None = None
    additional_cost: float | None = None


class ShippingRate(Dto):
    """One rate, the same fourteen keys on a listing row, the row read and every write's answer,
    whatever the method. ``method`` is ``flat_rate``, ``free_shipping``, ``ship_by_price``,
    ``ship_by_quantity``, ``ship_by_weight``, ``ship_by_variation`` or ``shipping_variant``. A flat
    rate carries ``shipping_cost`` and ``handling_cost``, the ``ship_by_*`` methods carry them per
    row in ``conditions``, and a key the method does not use reads ``None`` or an empty list.
    ``weight_unit`` is the store's, ``None`` unless the method is ``ship_by_weight``."""

    ENVELOPE_KEY = "shipping_rate"

    id: int | None = None
    name: str | None = None
    method: str | None = None
    calculate_for_entire_order: bool | None = None
    price_entered_with_tax: bool | None = None
    shipping_cost: ShippingCost | None = None
    handling_cost: ShippingCost | None = None
    weight_unit: str | None = None
    # A row's ``from`` is a Python keyword, so each row stays a mapping.
    conditions: list[Any] | None = None
    additional_rule: ShippingAdditionalRule | None = None
    shipping_rules: list[ShippingReference | None] | None = None
    transaction_no: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class ShippingRateInput(Dto):
    """The writable fields, wrapped in ``shipping_rate``, for the create, the ``PUT`` replace and
    the ``PATCH``. ``name`` and ``method`` are required on a create; a flat rate also needs
    ``shipping_cost`` and the ``ship_by_*`` methods need ``conditions``. ``PUT`` needs every
    field of the rate, ``handling_cost`` and ``additional_rule`` as ``None`` when unused.
    ``shipping_rule_id`` attaches the new rate to a rule that has none. Fields left ``None`` are
    not sent: to clear one, pass a mapping."""

    ENVELOPE_KEY = "shipping_rate"

    name: str | None = None
    method: str | None = None
    calculate_for_entire_order: bool | None = None
    price_entered_with_tax: bool | None = None
    shipping_cost: ShippingCost | None = None
    handling_cost: ShippingCost | None = None
    conditions: list[Any] | None = None
    additional_rule: ShippingAdditionalRule | None = None
    shipping_rule_id: int | None = None
    transaction_no: str | None = None
    suggest_name: bool | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block; ``limit`` is the size the store applied."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class ShippingRateListing(Dto):
    """One page of the listing, newest first."""

    shipping_rates: list[ShippingRate | None] | None = None
    pagination: Pagination | None = None


class ShippingRateCount(Dto):
    """The count sub-path's body, a bare ``{"total": N}``."""

    total: int | None = None
