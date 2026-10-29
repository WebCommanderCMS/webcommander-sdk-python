"""Typed views over the cart bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class CartTotals(Dto):
    """The cart's ``totals``; ``subtotal`` sums each line's ``unit_price`` times its quantity."""

    subtotal: float | None = None
    discount: float | None = None
    shipping_discount: float | None = None
    tax: float | None = None
    total: float | None = None
    grand_total: float | None = None
    paid: float | None = None


class CartShipping(Dto):
    """The cart's ``shipping`` block; its two taxes follow the shipping address's country."""

    cost: float | None = None
    handling_fee: float | None = None
    handling_tax: float | None = None
    shipping_tax: float | None = None
    total_tax: float | None = None


class CartItemPricing(Dto):
    """One line's ``pricing``."""

    unit_price: float | None = None
    display_unit_price: float | None = None
    total: float | None = None
    discount: float | None = None
    discount_tax: float | None = None
    tax: float | None = None


class CartItemProduct(Dto):
    """The product one line holds; ``available_stock`` is the product's, not the line's."""

    id: int | None = None
    sku: str | None = None
    base_price: float | None = None
    available_stock: int | None = None
    on_sale: bool | None = None
    cost_price: float | None = None
    sale_price: float | None = None
    url: str | None = None
    name: str | None = None
    product_type: str | None = None
    image_link: str | None = None


class CartItem(Dto):
    """One line of the cart; ``id`` is the ``cart_item_id`` the line's writes take."""

    id: int | None = None
    quantity: int | None = None
    variations: Any = None
    taxable: bool | None = None
    shippable: bool | None = None
    pricing: CartItemPricing | None = None
    product: CartItemProduct | None = None


class CartDiscount(Dto):
    """The cart's ``discount`` block."""

    discount: float | None = None
    order_discount: float | None = None
    shipping_discount: float | None = None
    discount_on_tax: float | None = None
    discount_on_shipping_tax: float | None = None


class CartDiscountMessage(Dto):
    """The ``discount`` entry of ``messages``."""

    message: str | None = None
    status: Any = None


class CartMessages(Dto):
    """The cart's ``messages`` block."""

    discount: CartDiscountMessage | None = None


class SectionMeta(Dto):
    """The one entry of ``group_meta``."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only a read sends."""

    cart: SectionMeta | None = None


class Cart(Dto):
    """One cart: the answer of the add, the read and the line update."""

    ENVELOPE_KEY = "cart"

    customer_id: int | None = None
    session_id: str | None = None
    currency_code: str | None = None
    currency_symbol: str | None = None
    delivery_type: str | None = None
    totals: CartTotals | None = None
    shipping: CartShipping | None = None
    items: list[CartItem] | None = None
    discount: CartDiscount | None = None
    messages: CartMessages | None = None
    group_meta: GroupMeta | None = None


class CartAddressInput(Dto):
    """A ``shipping_address`` or ``billing_address``; the cart answers neither back."""

    first_name: str | None = None
    last_name: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    post_code: str | None = None
    phone: str | None = None
    mobile: str | None = None
    fax: str | None = None
    email: str | None = None
    country_code: str | None = None
    state_code: str | None = None


class CartItemInput(Dto):
    """The add's body, no envelope; ``customer_id`` takes the customer's ``internal_id``."""

    product_id: int | None = None
    quantity: int | None = None
    customer_id: int | None = None
    session_id: str | None = None
    shipping_address: CartAddressInput | None = None


class CartItemUpdateInput(Dto):
    """The line update's body, no envelope; ``cart_item_id`` and ``quantity`` are required."""

    cart_item_id: int | None = None
    quantity: int | None = None
    shipping_address: CartAddressInput | None = None
    billing_address: CartAddressInput | None = None


class CartSessionInput(Dto):
    """The session write's body; an unset ``sessionId`` sends ``{}``."""

    sessionId: str | None = None


class CartSession(Dto):
    """The session write's answer."""

    sessionId: str | None = None


class CartOrderInput(Dto):
    """The order write's body, no envelope; ``customer_id`` takes the customer's ``customer_id``."""

    customer_id: int | None = None
    payment_gateway: str | None = None
    delivery_type: str | None = None
    transaction_no: str | None = None


class Reference(Dto):
    """A country or a state, as an object; a state arrives ``{}`` when the address has none."""

    id: int | None = None
    name: str | None = None
    code: str | None = None


class CartOrderCustomer(Dto):
    """The order's ``customer_summary``, carrying both of the customer's ids."""

    first_name: str | None = None
    last_name: str | None = None
    customer_group: str | None = None
    gender: str | None = None
    customer_id: int | None = None
    internal_id: int | None = None
    email: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    country: Reference | None = None
    state: Reference | None = None
    post_code: str | None = None
    phone: str | None = None
    mobile: str | None = None
    fax: str | None = None
    company_name: str | None = None


class CartOrderLine(Dto):
    """One entry of the order's ``order_line_details``."""

    item_id: int | None = None
    product_name: str | None = None
    product_id: int | None = None
    sku: str | None = None
    quantity: int | None = None
    price: float | None = None
    total_amount: float | None = None
    tax: float | None = None
    discount: float | None = None
    tax_discount: float | None = None
    is_taxable: bool | None = None
    is_shippable: bool | None = None
    image_url: str | None = None
    variations: list[Any] | None = None
    serial_batch_number: str | None = None


class CartOrderPayment(Dto):
    """One entry of the order's ``payments``."""

    id: int | None = None
    status: str | None = None
    amount: float | None = None
    payment_method: str | None = None
    track_info: str | None = None
    gateway_name: str | None = None
    gateway_code: str | None = None
    gateway_response: str | None = None
    payer_info: str | None = None
    paying_date: str | None = None
    transaction_date: str | None = None
    transaction_reference: str | None = None


class CartOrderAddress(Dto):
    """The order's ``billing_address`` or ``shipping_address``: the customer's, unless a line update
    sent addresses through the conversion's own HTTP session; the add's never arrive here."""

    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    company_name: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    country: Reference | None = None
    state: Reference | None = None
    city: str | None = None
    post_code: str | None = None
    mobile: str | None = None
    phone: str | None = None
    fax: str | None = None


class CartOrder(Dto):
    """The order a cart became, with the write's ``status`` read from beside the envelope.
    ``transaction_no`` answers ``null`` here even when the write stored one."""

    ENVELOPE_KEY = "order"

    status: str | None = None
    order_id: int | None = None
    internal_id: int | None = None
    order_no: int | None = None
    transaction_no: str | None = None
    currency_code: str | None = None
    order_status: str | None = None
    payment_status: str | None = None
    shipping_status: str | None = None
    sub_total: float | None = None
    shipping_cost: float | None = None
    shipping_tax: float | None = None
    handling_cost: float | None = None
    total_surcharge: float | None = None
    total_discount: float | None = None
    total_tax: float | None = None
    grand_total: float | None = None
    paid: float | None = None
    due: float | None = None
    items_total: int | None = None
    ip_address: str | None = None
    order_channel: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    customer_summary: CartOrderCustomer | None = None
    order_line_details: list[CartOrderLine] | None = None
    payments: list[CartOrderPayment] | None = None
    external_reference_order_id: Any = None
    external_reference_store_id: Any = None
    external_reference_order_no: Any = None
    external_reference_status: Any = None
    external_reference_url: Any = None
    customer_po_number: str | None = None
    payment_term: str | None = None
    fulfillment_mode: str | None = None
    fulfillment_term: str | None = None
    invoice_mode: str | None = None
    billing_address: CartOrderAddress | None = None
    shipping_address: CartOrderAddress | None = None
    custom_fields: list[Any] | None = None
