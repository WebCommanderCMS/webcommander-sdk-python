"""Typed views over the product bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class ProductUrls(Dto):
    """The product's slug and its absolute storefront address."""

    url: str | None = None
    product_url: str | None = None


class ProductNamedReference(Dto):
    """An ``id`` and a ``name``: an author, a page, a customer or a customer group."""

    id: int | None = None
    name: str | None = None


class ProductParent(Dto):
    """One category the product is filed under."""

    id: int | None = None
    name: str | None = None
    is_in_trash: bool | None = None
    is_parent_in_trash: bool | None = None
    is_disposable: bool | None = None


class ProductSelectedCustomer(Dto):
    """One customer an audience names: ``id`` is the customer's ``customer_id``, ``internal_id``
    its ``internal_id``."""

    id: int | None = None
    internal_id: int | None = None
    name: str | None = None


class ProductSelectedCustomers(Dto):
    """Who ``available_for: selected`` admits, or whom a restriction names; both lists are empty
    when nobody is named."""

    customers: list[ProductSelectedCustomer | None] | None = None
    groups: list[ProductNamedReference | None] | None = None


class ProductSelectedCustomersInput(Dto):
    """An audience to write: customer and group ids. A group written as ``{"id": ...}`` is
    ``400``."""

    customers: list[int | None] | None = None
    groups: list[int | None] | None = None


class ProductWeekday(Dto):
    """One day of the weekday schedule."""

    day: str | None = None
    start_hour: int | None = None
    start_minute: int | None = None
    end_hour: int | None = None
    end_minute: int | None = None
    is_full_day: bool | None = None
    enabled: bool | None = None


class ProductAvailableOnWeekdays(Dto):
    """The weekday schedule: a switch and the seven days."""

    enabled: bool | None = None
    weekdays: list[ProductWeekday | None] | None = None


class ProductProperties(Dto):
    """Dimensions as written; the top level of the product repeats the four numbers read-only."""

    length: float | None = None
    width: float | None = None
    height: float | None = None
    weight: float | None = None
    length_unit: str | None = None
    weight_unit: str | None = None


class ProductTaxSettings(Dto):
    """Per-product tax overrides, applied only when ``overwrite_default_config`` is ``true``."""

    overwrite_default_config: bool | None = None
    is_tax_exempt: bool | None = None
    show_price_with_tax: bool | None = None
    is_price_with_tax: bool | None = None
    system_default_tax: bool | None = None
    tax_message: str | None = None
    base_price_rounding: str | None = None
    default_tax_code: str | None = None
    custom_tax_profile_id: str | None = None


class ProductVariationPriceDisplay(Dto):
    """Which variant price a listing shows, and the labels it shows it with. ``lowest_price_label``
    and ``highest_price_label`` are second names for the two ``label_for_*`` fields."""

    method: str | None = None
    label_for_lowest_price: str | None = None
    label_for_highest_price: str | None = None
    lowest_price_label: str | None = None
    highest_price_label: str | None = None


class ProductWarehouseStock(Dto):
    """One location's units in the legacy shape; ``warehouse`` is the location id as text."""

    warehouse: str | None = None
    stock: int | None = None


class ProductStockLocation(Dto):
    """One location's holding of the product; exactly one row of a product holds ``is_default``."""

    warehouse: int | None = None
    warehouse_name: str | None = None
    stock: int | None = None
    low_stock_level: int | None = None
    is_default: bool | None = None


class ProductPricingAndStock(Dto):
    """The pricing and stock block. ``locations`` matches the stock sub-path's rows, and
    ``low_level_stock`` follows the default location's ``low_stock_level``."""

    track_inventory: bool | None = None
    available_stock: int | None = None
    low_level_stock: int | None = None
    warehouses: list[ProductWarehouseStock | None] | None = None
    minimum_order_quantity: int | None = None
    maximum_order_quantity: int | None = None
    tax_profile: Any = None
    shipping_profile: Any = None
    enable_multiple_order: bool | None = None
    multiple_order_quantity: int | None = None
    on_sale: bool | None = None
    on_sale_price_type: str | None = None
    on_sale_price: float | None = None
    expected_to_pay: bool | None = None
    expected_to_pay_price: float | None = None
    enable_call_for_price: bool | None = None
    restrict_price_for: str | None = None
    restrict_price_for_except_customers: list[Any] | None = None
    restrict_purchase_for: str | None = None
    restrict_purchase_for_selected_customers: list[Any] | None = None
    hide_price: bool | None = None
    enable_combined_stock_selling_limit: bool | None = None
    combined_stock_selling_limit: int | None = None
    enable_advance_pricing: bool | None = None
    suppliers: list[Any] | None = None
    is_multi_location_enabled: bool | None = None
    locations: list[ProductStockLocation | None] | None = None


class ProductImage(Dto):
    """One product image."""

    id: int | None = None
    filename: str | None = None
    alt_text: str | None = None
    thumbnail: str | None = None
    link: str | None = None


class ProductVideo(Dto):
    """One product video, on the product or on a variant."""

    id: int | None = None
    filename: str | None = None
    thumbnail: str | None = None
    link: str | None = None


class ProductImageAndVideo(Dto):
    """The media block."""

    images: list[ProductImage | None] | None = None
    videos: list[ProductVideo | None] | None = None
    specs: list[Any] | None = None


class ProductAdvanceInformation(Dto):
    """Identifiers and origin; ``mpn``, ``upc``, ``barcode`` and ``hs_code`` are written here,
    not at the top level, which refuses them."""

    global_trade_item_number: str | None = None
    enable_product_identifiers: bool | None = None
    gtin: str | None = None
    mpn: str | None = None
    upc: str | None = None
    barcode: str | None = None
    country_of_origin: str | None = None
    hs_code: str | None = None
    product_condition: str | None = None
    model: str | None = None


class ProductFlag(Dto):
    """A flag and the label shown with it."""

    enabled: bool | None = None
    label: str | None = None


class ProductFlags(Dto):
    """The flags in blocks: ``is_featured``, ``is_new``, ``sold_out`` and ``model`` again.
    ``sold_out`` is read-only."""

    featured: ProductFlag | None = None
    new_product: bool | None = None
    sold_out: ProductFlag | None = None
    model_number: str | None = None


class ProductDimension(Dto):
    """``product_properties`` again; the two units are read-only here."""

    length_unit: str | None = None
    weight_unit: str | None = None
    width: float | None = None
    height: float | None = None
    length: float | None = None
    weight: float | None = None


class ProductIdentifiers(Dto):
    """``advance_information`` again: a write here changes it there, ``condition`` being its
    ``product_condition``."""

    enabled: bool | None = None
    gtin: str | None = None
    condition: str | None = None
    barcode: str | None = None
    hs_code: str | None = None
    country_of_origin: str | None = None
    mpn: str | None = None
    upc: str | None = None


class ProductWebtool(Dto):
    """``webtool_disable_tracking`` again, read-only."""

    disable_tracking: bool | None = None


class ProductAdvanced(Dto):
    """The advanced block."""

    advance_information: ProductAdvanceInformation | None = None
    webtool_disable_tracking: bool | None = None
    meta_tags: list[Any] | None = None
    product_flags: ProductFlags | None = None
    product_dimension: ProductDimension | None = None
    product_identifiers: ProductIdentifiers | None = None
    webtool: ProductWebtool | None = None


class ProductLink(Dto):
    """A related, similar or up-sell product. A write takes ``{"id": ...}``; a list of bare ids in
    ``up_sell_products`` is answered ``200`` and leaves it empty."""

    id: int | None = None
    name: str | None = None
    url: str | None = None
    status: str | None = None
    sku: str | None = None
    in_stock: bool | None = None
    price: float | None = None


class ProductBundle(Dto):
    """The bundle block; ``bundle`` is ``null`` on a product that is not a bundle."""

    price_fixed: bool | None = None
    quantity_flexible: bool | None = None
    items: list[Any] | None = None


class ProductSeoConfig(Dto):
    """One SEO setting on the product."""

    id: int | None = None
    value: str | None = None
    type: str | None = None
    config_key: str | None = None
    meta_tags: list[Any] | None = None


class ProductTagValue(Dto):
    """One value of a product tag."""

    id: int | None = None
    title: str | None = None
    value: str | None = None
    url: str | None = None


class ProductTag(Dto):
    """One tag on the product, with its values."""

    id: int | None = None
    tag_id: int | None = None
    name: str | None = None
    values: list[ProductTagValue | None] | None = None
    display_in_product_page: bool | None = None
    enable_expanded_view: bool | None = None


class ProductCustomProperty(Dto):
    """One custom property."""

    id: int | None = None
    label: str | None = None
    description: str | None = None


class ProductReviewer(Dto):
    """Who wrote a review; ``name`` and ``email`` again."""

    name: str | None = None
    email: str | None = None


class ProductReview(Dto):
    """One review. ``product_id``, ``comment`` and ``created_at`` repeat ``productId``, ``review``
    and ``date``; ``created_at`` carries a ``Z``."""

    id: int | None = None
    productId: int | None = None
    name: str | None = None
    email: str | None = None
    review: str | None = None
    rating: float | None = None
    date: str | None = None
    status: str | None = None
    files: list[Any] | None = None
    product_id: int | None = None
    reviewer: ProductReviewer | None = None
    comment: str | None = None
    created_at: str | None = None


class ProductVariationTypeOption(Dto):
    """One option of a variation type the product uses."""

    id: int | None = None
    label: str | None = None
    value: str | None = None
    default: bool | None = None


class ProductVariationType(Dto):
    """One variation type the product uses, with its options."""

    id: int | None = None
    name: str | None = None
    standard: str | None = None
    options: list[ProductVariationTypeOption | None] | None = None


class ProductCombinationOptionType(Dto):
    """The type one option of a combination belongs to."""

    id: int | None = None
    role: str | None = None
    name: str | None = None
    standard: str | None = None
    is_disposable: bool | None = None


class ProductCombinationOption(Dto):
    """One option of a combination; ``type`` is a list of one type."""

    id: int | None = None
    index: int | None = None
    type: list[ProductCombinationOptionType | None] | None = None
    label: str | None = None
    value: str | None = None
    color_has_swatch: bool | None = None
    color_swatch_value: str | None = None
    image_base_url: str | None = None


class ProductCombinationImage(Dto):
    """One variant image."""

    id: int | None = None
    thumbnail: str | None = None
    url: str | None = None


class ProductCombinationPriceAndStock(Dto):
    """A variant's pricing and stock block."""

    track_inventory: bool | None = None
    available_stock: int | None = None
    low_level_stock: int | None = None
    minimum_order_quantity: int | None = None
    maximum_order_quantity: int | None = None
    supported_max_order_quantity: int | None = None
    enable_multiple_order: bool | None = None
    multiple_order_quantity: int | None = None
    on_sale: bool | None = None
    sold_out: bool | None = None
    sold_out_label: str | None = None
    on_sale_price_type: str | None = None
    on_sale_price: float | None = None
    expected_to_pay: bool | None = None
    expected_to_pay_price: float | None = None
    enable_call_for_price: bool | None = None
    hide_price: bool | None = None


class ProductCombinationDetails(Dto):
    """One variant. ``weight``, ``height``, ``length`` and ``width`` arrive as a number or as text,
    so they are not typed."""

    variation_id: int | None = None
    available: bool | None = None
    product_name: str | None = None
    sku: str | None = None
    custom_sku: str | None = None
    urls: ProductUrls | None = None
    meta_tags: list[Any] | None = None
    is_inventory_enabled: bool | None = None
    available_stock: int | None = None
    low_stock_level: int | None = None
    spec: str | None = None
    is_multiple_order_quantity: bool | None = None
    is_on_sale: bool | None = None
    is_expect_to_pay: bool | None = None
    is_call_for_price_enabled: bool | None = None
    is_new: bool | None = None
    is_featured: bool | None = None
    on_sale_amount_type: str | None = None
    title: str | None = None
    heading: str | None = None
    summary: str | None = None
    description: str | None = None
    model: str | None = None
    product_condition: str | None = None
    featured_label: str | None = None
    base_price: float | None = None
    cost_price: float | None = None
    compare_at_price: float | None = None
    sale_price: float | None = None
    expect_to_pay_price: float | None = None
    weight: Any = None
    height: Any = None
    length: Any = None
    width: Any = None
    display_price: float | None = None
    previous_price: float | None = None
    price_and_stock: ProductCombinationPriceAndStock | None = None
    images: list[ProductCombinationImage | None] | None = None
    videos: list[ProductVideo | None] | None = None
    specs: list[Any] | None = None
    supported_max_order_quantity: int | None = None
    is_base: bool | None = None
    barcode: str | None = None
    country_of_origin: str | None = None
    hs_code: str | None = None
    tax: float | None = None
    tax_message: str | None = None


class ProductCombination(Dto):
    """One option combination and the variant it makes."""

    options: list[ProductCombinationOption | None] | None = None
    details: ProductCombinationDetails | None = None


class ProductVariation(Dto):
    """The variation block; ``{}`` on a product with no variations, so every field reads ``None``."""

    types: list[ProductVariationType | None] | None = None
    available_combinations: list[ProductCombination | None] | None = None


class ProductCategory(Dto):
    """One category the product is filed under, as ``categories`` lists it; ``parents`` again."""

    id: int | None = None
    name: str | None = None
    in_trash: bool | None = None
    parent_in_trash: bool | None = None
    disposable: bool | None = None


class ProductMediaImage(Dto):
    """One image in the media block."""

    id: int | None = None
    filename: str | None = None
    position: int | None = None
    primary: bool | None = None
    alt_text: str | None = None
    url: str | None = None
    thumbnail_url: str | None = None


class ProductMediaVideo(Dto):
    """One video in the media block."""

    id: int | None = None
    filename: str | None = None
    position: int | None = None
    url: str | None = None
    thumbnail_url: str | None = None


class ProductMedia(Dto):
    """The media block. A write names files the product already holds, by ``id``; another id is
    ``400``. ``specification_file`` was ``null`` on every product read, so it is not typed."""

    images: list[ProductMediaImage | None] | None = None
    videos: list[ProductMediaVideo | None] | None = None
    specification_file: Any = None


class ProductWeekdayWindow(Dto):
    """One day of the schedule; times are ``HH:mm``."""

    enabled: bool | None = None
    full_day: bool | None = None
    start_time: str | None = None
    end_time: str | None = None


class ProductScheduleWeekdays(Dto):
    """The seven days of the schedule, each always present."""

    monday: ProductWeekdayWindow | None = None
    tuesday: ProductWeekdayWindow | None = None
    wednesday: ProductWeekdayWindow | None = None
    thursday: ProductWeekdayWindow | None = None
    friday: ProductWeekdayWindow | None = None
    saturday: ProductWeekdayWindow | None = None
    sunday: ProductWeekdayWindow | None = None


class ProductSchedule(Dto):
    """When the product is on sale. ``type`` is ``schedule_type`` (``date_range`` or
    ``custom_schedule``), ``preset`` is ``custom_schedule_option`` (``all_days``, ``weekdays``,
    ``business_hour``, ``weekends`` or ``custom``)."""

    enabled: bool | None = None
    type: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    preset: str | None = None
    weekdays: ProductScheduleWeekdays | None = None


class ProductPasswordProtection(Dto):
    """``password_protected`` and ``password`` again; a set password reads ``***``."""

    enabled: bool | None = None
    password: str | None = None


class ProductAvailableForPurchase(Dto):
    """Availability in one block: ``enabled`` is ``available``, ``active`` is
    ``administrative_status``, ``who_can_view`` is ``available_for``.
    ``restrict_for_selected_customers`` is read-only."""

    enabled: bool | None = None
    active: bool | None = None
    who_can_view: str | None = None
    selected_customers: ProductSelectedCustomers | None = None
    restrict_for_selected_customers: ProductSelectedCustomers | None = None
    schedule: ProductSchedule | None = None
    password_protection: ProductPasswordProtection | None = None


class ProductAvailableForPurchaseInput(Dto):
    """The availability block to write. While ``enabled`` is ``false`` the store answers ``200``
    and keeps none of ``who_can_view``, ``schedule`` or ``password_protection``."""

    enabled: bool | None = None
    active: bool | None = None
    who_can_view: str | None = None
    selected_customers: ProductSelectedCustomersInput | None = None
    schedule: ProductSchedule | None = None
    password_protection: ProductPasswordProtection | None = None


class ProductOnSale(Dto):
    """The sale price; ``amount_type`` is ``on_sale_price_type``."""

    enabled: bool | None = None
    discounted_price: float | None = None
    amount_type: str | None = None


class ProductQuantityMultiple(Dto):
    """Order in multiples of ``multiple_of``."""

    enabled: bool | None = None
    multiple_of: int | None = None


class ProductExpectToPay(Dto):
    """The expect-to-pay price."""

    enabled: bool | None = None
    price: float | None = None


class ProductAdvancedPricing(Dto):
    """The advanced pricing switches."""

    enabled: bool | None = None
    quantity_multiple: ProductQuantityMultiple | None = None
    expect_to_pay: ProductExpectToPay | None = None
    call_for_price: bool | None = None


class ProductPricing(Dto):
    """Prices in one block; ``rrp_price`` is ``compare_at_price``. On a create ``base_price`` here
    stands in for the top-level one."""

    base_price: float | None = None
    cost_price: float | None = None
    rrp_price: float | None = None
    on_sale: ProductOnSale | None = None
    advanced_pricing: ProductAdvancedPricing | None = None


class ProductInventoryTracking(Dto):
    """Stock tracking; ``suppliers`` echoes the ids written."""

    enabled: bool | None = None
    available_stock: int | None = None
    low_stock_level: int | None = None
    suppliers: list[Any] | None = None


class ProductCombinedStockLimit(Dto):
    """The combined stock selling limit."""

    enabled: bool | None = None
    units: int | None = None


class ProductInventory(Dto):
    """Stock in one block; ``preorder`` is ``preorder_enabled``."""

    tracking: ProductInventoryTracking | None = None
    combined_stock_limit: ProductCombinedStockLimit | None = None
    preorder: bool | None = None


class ProductOrdering(Dto):
    """The order quantity limits; a ``max_quantity`` of ``0`` is no maximum."""

    min_quantity: int | None = None
    max_quantity: int | None = None


class ProductRestriction(Dto):
    """A price or purchase restriction. Only ``mode`` is written; ``enabled`` is read-only and
    ``customers`` is answered ``200`` but kept empty."""

    enabled: bool | None = None
    mode: str | None = None
    customers: list[Any] | None = None


class ProductRestrictions(Dto):
    """``restrict_price_for`` and ``restrict_purchase_for`` in one block; ``enabled`` and
    ``display_only`` are read-only."""

    enabled: bool | None = None
    price: ProductRestriction | None = None
    purchase: ProductRestriction | None = None
    display_only: bool | None = None


class ProductPriceIncludesTax(Dto):
    """Whether ``base_price`` includes tax, and how it is rounded."""

    enabled: bool | None = None
    base_price_rounding: str | None = None


class ProductTax(Dto):
    """``tax_settings`` in one block; ``enabled`` is ``overwrite_default_config``. A write takes
    ``custom_tax_profile`` as an id or ``{"id": ...}`` of a custom tax profile."""

    enabled: bool | None = None
    exempt: bool | None = None
    custom_tax_profile: ProductNamedReference | None = None
    message: str | None = None
    show_price_with_tax: bool | None = None
    price_includes_tax: ProductPriceIncludesTax | None = None


class ProductShipping(Dto):
    """The shipping profile; ``enabled`` is read-only and true while a profile is set. A create
    drops ``profile``; an update takes it as an id or ``{"id": ...}``."""

    enabled: bool | None = None
    profile: ProductNamedReference | None = None


class ProductLinks(Dto):
    """API paths of the product and its sub-paths, read-only."""

    self: str | None = None
    variations: str | None = None
    stock: str | None = None
    reviews: str | None = None


class Product(Dto):
    """One product: the row read's body and every write's answer. ``field_metadata`` sits beside
    ``product`` when the read asks for it."""

    ENVELOPE_KEY = "product"

    id: int | None = None
    name: str | None = None
    sku: str | None = None
    status: str | None = None
    urls: ProductUrls | None = None
    heading: str | None = None
    parents: list[ProductParent | None] | None = None
    created_by: ProductNamedReference | None = None
    created_at: str | None = None
    updated_at: str | None = None
    transaction_no: str | None = None
    product_type: str | None = None
    custom_type: str | None = None
    is_virtual: bool | None = None
    invoice_note: str | None = None
    available: bool | None = None
    product_page: ProductNamedReference | None = None
    product_layout: Any = None
    custom_class: str | None = None
    available_on_date_range: bool | None = None
    available_from_date: str | None = None
    available_to_date: str | None = None
    available_for: str | None = None
    selected_customers: ProductSelectedCustomers | None = None
    restrict_for_selected_customers: ProductSelectedCustomers | None = None
    password_protected: bool | None = None
    password: str | None = None
    available_on_weekdays: ProductAvailableOnWeekdays | None = None
    base_price: float | None = None
    cost_price: float | None = None
    compare_at_price: float | None = None
    is_on_sale: bool | None = None
    sale_price: float | None = None
    sold_out: bool | None = None
    length: float | None = None
    width: float | None = None
    height: float | None = None
    weight: float | None = None
    sold_out_label: str | None = None
    is_featured: bool | None = None
    featured_label: str | None = None
    is_new: bool | None = None
    featured: bool | None = None
    new: bool | None = None
    model: str | None = None
    product_properties: ProductProperties | None = None
    version: int | None = None
    created_on: str | None = None
    last_updated_on: str | None = None
    last_updated_by: ProductNamedReference | None = None
    schedule_type: str | None = None
    custom_schedule_option: str | None = None
    tax_settings: ProductTaxSettings | None = None
    variation_price_display: ProductVariationPriceDisplay | None = None
    administrative_status: bool | None = None
    is_draft: bool | None = None
    product_summary: str | None = None
    product_description: str | None = None
    product_pricing_and_stock: ProductPricingAndStock | None = None
    image_and_video: ProductImageAndVideo | None = None
    advanced: ProductAdvanced | None = None
    related_products: list[ProductLink | None] | None = None
    similar_products: list[ProductLink | None] | None = None
    bundle: ProductBundle | None = None
    seo_configs: list[ProductSeoConfig | None] | None = None
    tags: list[ProductTag | None] | None = None
    custom_properties: list[ProductCustomProperty | None] | None = None
    reviews: list[ProductReview | None] | None = None
    product_variation: ProductVariation | None = None
    preorder_enabled: bool | None = None
    has_variations: bool | None = None
    # The block-shaped copy of the fields above; a write to either changes both.
    product_url: str | None = None
    updated_by: ProductNamedReference | None = None
    virtual: bool | None = None
    summary: str | None = None
    description: str | None = None
    categories: list[ProductCategory | None] | None = None
    up_sell_products: list[ProductLink | None] | None = None
    media: ProductMedia | None = None
    available_for_purchase: ProductAvailableForPurchase | None = None
    pricing: ProductPricing | None = None
    inventory: ProductInventory | None = None
    ordering: ProductOrdering | None = None
    restrictions: ProductRestrictions | None = None
    tax: ProductTax | None = None
    shipping: ProductShipping | None = None
    links: ProductLinks | None = None
    field_metadata: Any = None


class Pagination(Dto):
    """The five-key ``pagination`` block; ``limit`` is the page size applied."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class ProductPage(Dto):
    """One page of the listing: full product records, where they sit and any schema."""

    products: list[Product | None] | None = None
    pagination: Pagination | None = None
    field_metadata: Any = None


class ProductInput(Dto):
    """The create's, ``PUT``'s and ``PATCH``'s bare record; an update merges it at every level,
    and a ``PUT`` also needs the ten fields ``update_product`` lists. A changed read-only field is
    ``400 read_only_field``; ``product_url``, ``links`` and ``restrict_for_selected_customers``
    are read-only, and ``updated_by`` is answered ``200`` and ignored."""

    name: str | None = None
    sku: str | None = None
    #: Stored on a create; an update stores it only on a product without one, else drops it.
    transaction_no: str | None = None
    heading: str | None = None
    product_type: str | None = None
    custom_type: str | None = None
    is_virtual: bool | None = None
    invoice_note: str | None = None
    available: bool | None = None
    available_on_date_range: bool | None = None
    available_from_date: str | None = None
    available_to_date: str | None = None
    available_for: str | None = None
    selected_customers: ProductSelectedCustomersInput | None = None
    password_protected: bool | None = None
    password: str | None = None
    available_on_weekdays: ProductAvailableOnWeekdays | None = None
    base_price: float | None = None
    cost_price: float | None = None
    compare_at_price: float | None = None
    is_on_sale: bool | None = None
    sale_price: float | None = None
    is_featured: bool | None = None
    featured_label: str | None = None
    is_new: bool | None = None
    product_properties: ProductProperties | None = None
    schedule_type: str | None = None
    custom_schedule_option: str | None = None
    tax_settings: ProductTaxSettings | None = None
    variation_price_display: ProductVariationPriceDisplay | None = None
    administrative_status: bool | None = None
    product_summary: str | None = None
    product_description: str | None = None
    product_pricing_and_stock: ProductPricingAndStock | None = None
    image_and_video: ProductImageAndVideo | None = None
    advanced: ProductAdvanced | None = None
    parents: list[int | None] | None = None
    related_products: list[Any] | None = None
    similar_products: list[Any] | None = None
    tags: list[Any] | None = None
    preorder_enabled: bool | None = None
    virtual: bool | None = None
    summary: str | None = None
    description: str | None = None
    #: Category ids or ``{"id": ...}`` records; ``[]`` is answered ``200`` and changes nothing.
    categories: list[int | None] | None = None
    up_sell_products: list[ProductLink | None] | None = None
    media: ProductMedia | None = None
    available_for_purchase: ProductAvailableForPurchaseInput | None = None
    pricing: ProductPricing | None = None
    inventory: ProductInventory | None = None
    ordering: ProductOrdering | None = None
    restrictions: ProductRestrictions | None = None
    tax: ProductTax | None = None
    shipping: ProductShipping | None = None


class ProductReviews(Dto):
    """The review import's answer: every review the product holds, the ones just added last."""

    ENVELOPE_KEY = "product"

    reviews: list[ProductReview | None] | None = None


class ProductReviewInput(Dto):
    """One review to add. ``name``, ``email`` and a ``rating`` of 1 to 5 are required; a second
    review under an ``email`` the product already has overwrites that review."""

    name: str | None = None
    email: str | None = None
    rating: float | None = None
    review: str | None = None
    #: The same text as ``review``, under its alternative key.
    comment: str | None = None
    status: str | None = None
    #: ``yyyy-MM-ddTHH:mm:ss``; the read's ``date`` key is refused on the write.
    dateCreated: str | None = None


class ProductReviewsImportInput(Dto):
    """The review import's body: ``{"product": {"reviews": [...]}}`` with ``transaction_no``
    beside the envelope; ``reviews`` must not be empty."""

    ENVELOPE_KEY = "product"
    TOP_LEVEL = ("transaction_no",)

    reviews: list[ProductReviewInput | None] | None = None
    transaction_no: str | None = None


class ProductStockVariation(Dto):
    """One variant's stock on a product with variations."""

    variation_id: int | None = None
    product_id: int | None = None
    name: str | None = None
    sku: str | None = None
    available_stock: int | None = None
    locations: list[ProductStockLocation | None] | None = None


class ProductStock(Dto):
    """The stock sub-path's body, read and written. ``available_stock`` is the sum of the rows'
    ``stock``; ``variations`` is there only on a product with variations."""

    status: str | None = None
    product_id: int | None = None
    multi_location_enabled: bool | None = None
    track_inventory: bool | None = None
    available_stock: int | None = None
    locations: list[ProductStockLocation | None] | None = None
    variations: list[ProductStockVariation | None] | None = None


class ProductStockLocationInput(Dto):
    """One row of the stock write. An omitted ``low_stock_level`` is stored ``null``; with no row
    marked ``is_default``, the first row sent becomes the default."""

    warehouse: int | None = None
    stock: int | None = None
    low_stock_level: int | None = None
    is_default: bool | None = None


class ProductStockInput(Dto):
    """The stock write's body: ``locations`` is required and replaces the product's whole set, so a
    location left out is unassigned whatever it holds."""

    note: str | None = None
    locations: list[ProductStockLocationInput | None] | None = None
