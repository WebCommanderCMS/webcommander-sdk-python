"""Typed views over the price display settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class DisplayScopes(Dto):
    """The storefront surfaces one setting applies to; each block allows its own subset."""

    shopping_cart: bool | None = None
    checkout: bool | None = None
    order_success: bool | None = None


class ScopedToggle(Dto):
    """A setting with a master switch and optional per-surface control.
    While ``customize`` is off the store answers ``scopes`` following ``enabled``."""

    enabled: bool | None = None
    customize: bool | None = None
    scopes: DisplayScopes | None = None


class PlainToggle(Dto):
    """A setting with nothing but a master switch."""

    enabled: bool | None = None


class Subtotal(Dto):
    """The ``subtotal`` block; ``show`` is a :class:`DisplayScopes` rather than a toggle."""

    show: DisplayScopes | None = None
    include_tax: ScopedToggle | None = None
    include_discount: ScopedToggle | None = None


class Discount(Dto):
    """The ``discount`` block — where the discount line shows, and whether it carries tax."""

    show: DisplayScopes | None = None
    hide_if_zero: ScopedToggle | None = None
    include_tax: ScopedToggle | None = None


class ShippingCost(Dto):
    """The ``shipping_cost`` block — where the shipping line shows, and what it carries."""

    show: DisplayScopes | None = None
    include_tax: ScopedToggle | None = None
    include_discount: ScopedToggle | None = None


class ShippingDiscount(Dto):
    """The ``shipping_discount`` block — the shipping discount line and the shipping tax line."""

    show: DisplayScopes | None = None
    include_tax: ScopedToggle | None = None
    shipping_tax: PlainToggle | None = None


class Handling(Dto):
    """The ``handling`` block — handling shown apart from shipping, and its tax settings."""

    show_separately: DisplayScopes | None = None
    include_tax: ScopedToggle | None = None
    handling_tax: ScopedToggle | None = None


class PricingInfo(Dto):
    """The ``pricing_info`` block — the note after the total, and hiding the due amount."""

    enabled: bool | None = None
    text: str | None = None
    customize: bool | None = None
    scopes: DisplayScopes | None = None
    do_not_show_due_amount: bool | None = None


class OrderItem(Dto):
    """The ``order_item`` section — how a line item's own price is displayed."""

    ENVELOPE_KEY = "order_item"

    price_including_tax: ScopedToggle | None = None
    price_including_discount: ScopedToggle | None = None
    tax_in_line: ScopedToggle | None = None
    discount_in_line_item: ScopedToggle | None = None
    item_total_including_tax: ScopedToggle | None = None


class OrderSummary(Dto):
    """The ``order_summary`` section — the summary panel's lines and what each includes."""

    ENVELOPE_KEY = "order_summary"

    order_total_excluding_tax: ScopedToggle | None = None
    order_total_including_discount: ScopedToggle | None = None
    subtotal: Subtotal | None = None
    discount: Discount | None = None
    subtotal_tax: PlainToggle | None = None
    total_tax: PlainToggle | None = None
    order_total: PlainToggle | None = None
    shipping_cost: ShippingCost | None = None
    shipping_discount: ShippingDiscount | None = None
    handling: Handling | None = None
    payment_surcharge: ScopedToggle | None = None
    pricing_info: PricingInfo | None = None


class SectionMeta(Dto):
    """One entry of ``group_meta``: what a section is, whether it can be written and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends."""

    order_item: SectionMeta | None = None
    order_summary: SectionMeta | None = None


class PriceDisplaySettings(Dto):
    """The price display settings, as the facade's body or as one section's body."""

    ENVELOPE_KEY = "price_display_settings"

    order_item: OrderItem | None = None
    order_summary: OrderSummary | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
