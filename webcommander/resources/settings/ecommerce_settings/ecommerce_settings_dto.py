"""Typed views over the ecommerce settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class ContinueShopping(Dto):
    """The ``continue_shopping`` section; its target is a page slug the store validates."""

    ENVELOPE_KEY = "continue_shopping"

    enable_continue_shopping: bool | None = None
    continue_shopping_target: str | None = None
    continue_shopping_specified_target: str | None = None


class ProductInventory(Dto):
    """The ``product_inventory`` section — out-of-stock handling and when a sale draws stock."""

    ENVELOPE_KEY = "product_inventory"

    show_out_of_stock_products: bool | None = None
    low_stock_notification: bool | None = None
    out_of_stock_notification: bool | None = None
    hide_on_sale_tag_for_out_of_stock_product: bool | None = None
    order_quantity_over_stock: str | None = None
    update_stock: str | None = None


class Pricing(Dto):
    """The ``pricing`` section — purchase floors, credit and payment terms.
    Each ``depends_on`` switch is enforced, not advisory."""

    ENVELOPE_KEY = "pricing"

    update_price_range: bool | None = None
    enable_minimum_purchase_amount: bool | None = None
    minimum_purchase_amount: float | None = None
    enable_minimum_purchase_amount_in_cart: bool | None = None
    minimum_purchase_amount_in_cart: float | None = None
    enable_on_account_purchase: bool | None = None
    assign_credit_limit_per_order: bool | None = None
    credit_limit_per_order: float | None = None
    enable_payment_terms: bool | None = None
    payment_terms: str | None = None
    enable_customer_price_restriction: bool | None = None


class ProductRestriction(Dto):
    """The ``product_restriction`` section — one switch."""

    ENVELOPE_KEY = "product_restriction"

    enable_product_restriction_based_on_parent_category: bool | None = None


class OrderFilters(Dto):
    """The ``order_filters`` section — the status each admin order list opens on."""

    ENVELOPE_KEY = "order_filters"

    default_order_status: str | None = None
    default_payment_status: str | None = None
    default_shipment_status: str | None = None


class InventoryLocation(Dto):
    """One row of ``location_settings.locations``, a read-only preview of a stock location."""

    id: int | None = None
    name: str | None = None
    address: str | None = None
    active: bool | None = None
    default: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None


class LocationSettings(Dto):
    """The ``location_settings`` section; ``enable_multi_location`` is the only writable field."""

    ENVELOPE_KEY = "location_settings"

    enable_multi_location: bool | None = None
    locations: list[InventoryLocation] | None = None


class OrderFlag(Dto):
    """One row of ``order_flags``, as the facade inlines it; never written here."""

    id: int | None = None
    name: str | None = None
    color: str | None = None
    description: str | None = None
    type: str | None = None


class SectionMeta(Dto):
    """One ``group_meta`` entry; ``location_settings`` adds a fourth key, ``locations_href``."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None
    locations_href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends; ``order_flags`` included."""

    continue_shopping: SectionMeta | None = None
    product_inventory: SectionMeta | None = None
    pricing: SectionMeta | None = None
    product_restriction: SectionMeta | None = None
    order_filters: SectionMeta | None = None
    location_settings: SectionMeta | None = None
    order_flags: SectionMeta | None = None


class EcommerceSettings(Dto):
    """The ecommerce settings, as the facade's body or as one section's body."""

    ENVELOPE_KEY = "ecommerce_settings"

    continue_shopping: ContinueShopping | None = None
    product_inventory: ProductInventory | None = None
    pricing: Pricing | None = None
    product_restriction: ProductRestriction | None = None
    order_filters: OrderFilters | None = None
    location_settings: LocationSettings | None = None
    order_flags: list[OrderFlag] | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
