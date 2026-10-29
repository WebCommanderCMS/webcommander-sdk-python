"""Typed views over the discount profile bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class AmountDetails(Dto):
    """The block an ``amount`` profile carries. ``tiers`` reads as tier ids, and tier records
    sent are not stored."""

    type: str | None = None
    apply_to: str | None = None
    single_amount: float | None = None
    single_amount_type: str | None = None
    minimum_amount_on: str | None = None
    tiers: list[int] | None = None


class ShippingDetails(Dto):
    """The block a ``shipping`` profile carries."""

    type: str | None = None
    apply_to: str | None = None
    minimum_qty_on: str | None = None
    amount_type: str | None = None
    single_amount_type: str | None = None
    minimum_qty: int | None = None
    minimum_amount: float | None = None
    single_amount: Any = None
    cap_amount: Any = None
    maximum_time: Any = None
    zone: Any = None
    shipping_class: Any = None
    tiers: list[Any] | None = None


class ProductDetails(Dto):
    """The block a ``product`` profile carries; ``product_ids`` sent is not stored."""

    type: str | None = None
    free_product_min_qty_on: str | None = None
    free_product_max_qty: int | None = None
    free_product_min_amount: float | None = None
    minimum_qty_on: str | None = None
    amount_type: str | None = None
    single_amount_type: str | None = None
    single_amount: Any = None
    cap_price: Any = None
    cap_price_max_qty: Any = None
    product_ids: list[Any] | None = None
    category_ids: list[Any] | None = None
    tiers: list[Any] | None = None


class CustomerCoupon(Dto):
    """One generated coupon; ``customer_email`` is ``""`` until a customer is assigned."""

    id: int | None = None
    code: str | None = None
    customer_email: str | None = None


class DiscountProfile(Dto):
    """One discount profile: a listing row, a row path's body, and every write's answer.
    It carries the one details block its ``discount_details_type`` names, not the other two."""

    ENVELOPE_KEY = "discount_profile"

    id: int | None = None
    uuid: str | None = None
    name: str | None = None
    type: str | None = None
    discount_details_type: str | None = None
    amount_details: AmountDetails | None = None
    shipping_details: ShippingDetails | None = None
    product_details: ProductDetails | None = None
    is_active: bool | None = None
    start_date: str | None = None
    is_specify_end_date: bool | None = None
    end_date: str | None = None
    is_apply_coupon_code: bool | None = None
    default_coupon_code: str | None = None
    is_coupon_code_auto_generate: bool | None = None
    is_create_unique_coupon_each_customer: bool | None = None
    is_imported_coupon: bool | None = None
    is_maximum_use_total: bool | None = None
    maximum_use_count: int | None = None
    is_maximum_use_customer: bool | None = None
    maximum_use_customer_count: int | None = None
    is_maximum_discount_allowed: bool | None = None
    maximum_discount_allowed_amount: float | None = None
    is_exclude_products_on_sale: bool | None = None
    is_discount_used_with_other_discount: bool | None = None
    is_display_discount_information_prod_detail: bool | None = None
    is_display_text_coupon: bool | None = None
    display_text_coupon: str | None = None
    is_display_text_cart: bool | None = None
    display_text_cart: str | None = None
    is_display_text_partial_discount_condition: bool | None = None
    display_text_partial_discount_condition: str | None = None
    invoice_note: str | None = None
    exclude_products: list[int] | None = None
    customer_coupons: list[CustomerCoupon] | None = None
    usage: list[int] | None = None
    created_on: str | None = None
    last_updated_on: str | None = None
    field_metadata: Any = None


class DiscountProfileInput(Dto):
    """The writable form of :class:`DiscountProfile`, for the create and the update; no envelope.
    The update resets every ``is_*`` flag, date and limit it omits."""

    name: str | None = None
    type: str | None = None
    discount_details_type: str | None = None
    amount_details: AmountDetails | None = None
    shipping_details: ShippingDetails | None = None
    product_details: ProductDetails | None = None
    is_active: bool | None = None
    start_date: str | None = None
    is_specify_end_date: bool | None = None
    end_date: str | None = None
    is_apply_coupon_code: bool | None = None
    default_coupon_code: str | None = None
    is_coupon_code_auto_generate: bool | None = None
    is_create_unique_coupon_each_customer: bool | None = None
    is_imported_coupon: bool | None = None
    is_maximum_use_total: bool | None = None
    maximum_use_count: int | None = None
    is_maximum_use_customer: bool | None = None
    maximum_use_customer_count: int | None = None
    is_maximum_discount_allowed: bool | None = None
    maximum_discount_allowed_amount: float | None = None
    is_exclude_products_on_sale: bool | None = None
    is_discount_used_with_other_discount: bool | None = None
    is_display_discount_information_prod_detail: bool | None = None
    is_display_text_coupon: bool | None = None
    display_text_coupon: str | None = None
    is_display_text_cart: bool | None = None
    display_text_cart: str | None = None
    is_display_text_partial_discount_condition: bool | None = None
    display_text_partial_discount_condition: str | None = None
    invoice_note: str | None = None
    exclude_products: list[int] | None = None


class Pagination(Dto):
    """The listing's ten-key ``pagination`` block; ``limit`` is the size applied, capped at 20."""

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


class ResourceMeta(Dto):
    """The one ``group_meta`` entry: what the collection is, whether it is writable and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The listing's ``group_meta`` block."""

    discount_profiles: ResourceMeta | None = None


class DiscountProfilePage(Dto):
    """One page of the listing: the rows, where they sit, the ``group_meta`` and any schema."""

    discount_profiles: list[DiscountProfile] | None = None
    pagination: Pagination | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None


class DiscountProfileCoupons(Dto):
    """The create-coupons answer: the codes generated, beside ``status`` and ``message``."""

    status: str | None = None
    message: str | None = None
    codes: list[str] | None = None


class DiscountProfileCouponsInput(Dto):
    """The create-coupons body; ``requested_codes`` is required and at least 1."""

    requested_codes: int | None = None


class DiscountCouponCustomerInput(Dto):
    """The assign-customer body: a generated ``code`` and the ``email`` of an existing customer."""

    code: str | None = None
    email: str | None = None
