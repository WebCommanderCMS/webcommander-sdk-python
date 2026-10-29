"""Typed views over the variation type and product variant bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class VariationOptionImage(Dto):
    """An image option's stored picture; ``null`` on text and color options."""

    url: str | None = None
    file_name: str | None = None


class VariationOption(Dto):
    """One option of a type. ``value`` is ``null`` on an image option."""

    id: int | None = None
    label: str | None = None
    value: str | None = None
    order: int | None = None
    default: bool | None = None
    image: VariationOptionImage | None = None


class Variation(Dto):
    """One variation type: a listing row, a row read and every type write's answer."""

    ENVELOPE_KEY = "variation"

    id: int | None = None
    name: str | None = None
    standard: str | None = None
    disposable: bool | None = None
    options: list[VariationOption | None] | None = None
    field_metadata: Any = None


class Pagination(Dto):
    """The listing's five-key ``pagination`` block."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class VariationPage(Dto):
    """One page of the listing, and the schema when ``field_metadata`` is asked for."""

    variations: list[Variation | None] | None = None
    field_metadata: Any = None
    pagination: Pagination | None = None


class VariationOptionImageInput(Dto):
    """An image option's upload; written as ``filename``, read back as ``file_name``."""

    base64: str | None = None
    filename: str | None = None


class VariationOptionInput(Dto):
    """One option in a type write; an ``id`` names an option of this type to change."""

    id: int | None = None
    label: str | None = None
    value: str | None = None
    order: int | None = None
    default: bool | None = None
    image: VariationOptionImageInput | None = None


class VariationInput(Dto):
    """The type writes' body, ``{"variation": {...}}``; ``standard`` cannot change after create."""

    ENVELOPE_KEY = "variation"

    name: str | None = None
    standard: str | None = None
    options: list[VariationOptionInput | None] | None = None


class ProductVariantExpectToPay(Dto):
    """A variant's expected-price display."""

    is_enabled: bool | None = None
    price: float | None = None


class ProductVariantPricing(Dto):
    """A variant's prices; the bulk write answers the first four fields."""

    base_price: float | None = None
    cost_price: float | None = None
    sale_price: float | None = None
    is_on_sale: bool | None = None
    sale_amount_type: str | None = None
    hide_price: bool | None = None
    is_call_for_price: bool | None = None
    expect_to_pay: ProductVariantExpectToPay | None = None
    tiered_pricing: Any = None


class ProductVariantInventory(Dto):
    """A variant's stock; the bulk write answers the first three fields."""

    is_enabled: bool | None = None
    quantity: int | None = None
    low_stock_threshold: int | None = None
    is_sold_out: bool | None = None
    sold_out_label: str | None = None


class ProductVariantOrdering(Dto):
    """A variant's order quantities; ``max_quantity`` 0 is no maximum."""

    min_quantity: int | None = None
    max_quantity: int | None = None
    multiple_of: int | None = None
    is_multiple_quantity_required: bool | None = None


class ProductVariantDimensions(Dto):
    """A variant's size and weight."""

    length: float | None = None
    width: float | None = None
    height: float | None = None
    weight: float | None = None


class ProductVariantBadges(Dto):
    """A variant's two badges."""

    is_featured: bool | None = None
    is_new_arrival: bool | None = None


class ProductVariant(Dto):
    """One variant of a product; ``key`` joins its option labels with ``/``."""

    variation_id: int | None = None
    available: bool | None = None
    is_base: bool | None = None
    key: str | None = None
    name: str | None = None
    sku: str | None = None
    custom_sku: str | None = None
    title: str | None = None
    summary: str | None = None
    description: str | None = None
    barcode: str | None = None
    country_of_origin: str | None = None
    hs_code: str | None = None
    pricing: ProductVariantPricing | None = None
    inventory: ProductVariantInventory | None = None
    ordering: ProductVariantOrdering | None = None
    dimensions: ProductVariantDimensions | None = None
    badges: ProductVariantBadges | None = None
    images: list[Any] | None = None


class ProductVariationGroup(Dto):
    """A product's variants, under ``product_key``: its type names joined with ``/``."""

    product_key: str | None = None
    variants: list[ProductVariant | None] | None = None


class ProductVariations(Dto):
    """The product read's body; ``variations`` is empty for a product without variants."""

    variations: list[ProductVariationGroup | None] | None = None


class ProductVariantOptionReference(Dto):
    """One option a variant carries, in the bulk write's full answer."""

    id: int | None = None
    type: str | None = None
    label: str | None = None


class ProductVariantUpdate(Dto):
    """One written variant: ``id`` and ``name``, and the rest with ``response=full``."""

    id: int | None = None
    name: str | None = None
    sku: str | None = None
    custom_sku: str | None = None
    barcode: str | None = None
    country_of_origin: str | None = None
    hs_code: str | None = None
    available: bool | None = None
    options: list[ProductVariantOptionReference | None] | None = None
    pricing: ProductVariantPricing | None = None
    inventory: ProductVariantInventory | None = None
    ordering: ProductVariantOrdering | None = None
    transaction_no: str | None = None
    url: str | None = None


class ProductVariationsBulkResult(Dto):
    """The bulk write's answer; ``failed`` stays empty, a refused id refuses the whole write."""

    status: str | None = None
    message: str | None = None
    updated: list[ProductVariantUpdate | None] | None = None
    failed: list[Any] | None = None


class ProductVariationsBulkInput(Dto):
    """The bulk write's body, no envelope: the variant ids and at least one of the six fields."""

    variation_ids: list[int] | None = None
    available: bool | None = None
    base_price: float | None = None
    cost_price: float | None = None
    available_stock: int | None = None
    min_order_quantity: int | None = None
    max_order_quantity: int | None = None


class ProductVariantInput(Dto):
    """One variant to import; ``key`` joins one option label per type with ``/`` and is required.
    A key the product has is that variant, changed; an unknown field is ``400 unknown_field``."""

    key: str | None = None
    name: str | None = None
    sku: str | None = None
    custom_sku: str | None = None
    title: str | None = None
    summary: str | None = None
    description: str | None = None
    barcode: str | None = None
    country_of_origin: str | None = None
    hs_code: str | None = None
    pricing: ProductVariantPricing | None = None
    inventory: ProductVariantInventory | None = None
    ordering: ProductVariantOrdering | None = None
    dimensions: ProductVariantDimensions | None = None
    badges: ProductVariantBadges | None = None
    images: list[Any] | None = None


class ProductVariationGroupInput(Dto):
    """One group to import: ``product_key`` names the types, joined with ``/``, and ``variants``
    must not be empty. A type name the store has is reused, an option label it lacks is added."""

    product_key: str | None = None
    variants: list[ProductVariantInput | None] | None = None


class ProductVariationsImportInput(Dto):
    """The import's body, no envelope; ``variations`` must not be empty."""

    transaction_no: str | None = None
    variations: list[ProductVariationGroupInput | None] | None = None


class ProductVariationsImportResult(Dto):
    """The import's answer: ``status``, a ``message`` counting the variants and ``total_variants``."""

    status: str | None = None
    message: str | None = None
    total_variants: int | None = None
