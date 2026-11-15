"""Typed views over the admin cart and checkout bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto
from webcommander.resources.carts.carts_dto import Reference
from webcommander.resources.orders.orders_dto import OrderAddressInput


class AdminCartSession(Dto):
    """The session block. ``session_id`` starts ``PRV-`` and is the ``session_id`` of every other
    call. ``expires_at`` is 30 minutes after the last write."""

    session_id: str | None = None
    status: str | None = None
    created_at: str | None = None
    expires_at: str | None = None


class AdminCartCustomer(Dto):
    """The customer the cart is for; ``customer_id`` is the customer's normal id."""

    customer_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class AdminCartItem(Dto):
    """One line, priced by the store. ``cart_item_id`` is what the line's update and delete take;
    a replace of the cart numbers its lines again."""

    cart_item_id: int | None = None
    product_id: int | None = None
    product_name: str | None = None
    variation_id: int | None = None
    variation_name: str | None = None
    sku: str | None = None
    price: float | None = None
    quantity: int | None = None
    discount: float | None = None
    tax: float | None = None
    total_amount: float | None = None
    taxable: bool | None = None
    shippable: bool | None = None


class AdminCartTotals(Dto):
    """The cart's money before shipping."""

    sub_total: float | None = None
    total_discount: float | None = None
    total_tax: float | None = None
    grand_total: float | None = None


class AdminCart(Dto):
    """A cart: what every cart call but the deletes answers."""

    ENVELOPE_KEY = "cart"

    session: AdminCartSession | None = None
    customer: AdminCartCustomer | None = None
    currency_code: str | None = None
    items: list[AdminCartItem | None] | None = None
    totals: AdminCartTotals | None = None


class CheckoutAddress(Dto):
    """A billing or shipping address as the checkout reads it back; ``state`` is ``{}`` when the
    address has none."""

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


class CheckoutShipping(Dto):
    """The delivery the checkout was priced for; empty until a ``delivery_type`` is set."""

    delivery_type: str | None = None
    shipping_type: str | None = None
    shipping_cost: float | None = None
    shipping_tax: float | None = None


class CheckoutCoupon(Dto):
    """The coupon applied: ``applied_amount`` is the discount it takes off."""

    code: str | None = None
    status: str | None = None
    applied_amount: float | None = None


class CheckoutGiftCard(Dto):
    """The gift card applied: ``applied_amount`` is the lesser of its balance and the grand total."""

    code: str | None = None
    status: str | None = None
    applied_amount: float | None = None
    remaining_balance: float | None = None


class CheckoutDiscounts(Dto):
    """At most one coupon and one gift card; ``None`` for one not applied."""

    coupon: CheckoutCoupon | None = None
    gift_card: CheckoutGiftCard | None = None


class CheckoutTotals(Dto):
    """The money. A gift card lowers ``due``, not ``grand_total``."""

    sub_total: float | None = None
    total_discount: float | None = None
    total_tax: float | None = None
    shipping_cost: float | None = None
    handling_cost: float | None = None
    total_surcharge: float | None = None
    gift_card_applied: float | None = None
    grand_total: float | None = None
    due: float | None = None


class CheckoutIssue(Dto):
    """One thing still blocking a confirm, such as ``delivery_type`` ``required``."""

    field: str | None = None
    code: str | None = None
    message: str | None = None


class AdminCheckout(Dto):
    """The checkout. The read and the update answer every field; the coupon, gift card and
    delivery schedule calls answer the parts they change. ``delivery_schedule`` is ``None``
    until one is set."""

    ENVELOPE_KEY = "checkout"

    session: AdminCartSession | None = None
    customer: AdminCartCustomer | None = None
    delivery_type: str | None = None
    currency_code: str | None = None
    items: list[AdminCartItem | None] | None = None
    billing_address: CheckoutAddress | None = None
    shipping_address: CheckoutAddress | None = None
    shipping: CheckoutShipping | None = None
    discounts: CheckoutDiscounts | None = None
    delivery_schedule: Any = None
    totals: CheckoutTotals | None = None
    issues: list[CheckoutIssue | None] | None = None


class AdminCartProductInput(Dto):
    """One product line to put on a cart. ``product_id`` and ``quantity`` are required;
    ``variation_id`` picks the variation of a variable product."""

    product_id: int | None = None
    variation_id: int | None = None
    quantity: int | None = None


class AdminCartInput(Dto):
    """The create and replace body, bare. ``products`` is required, and so is ``customer_id``
    on a replace; ``session_id`` on a create names the session yourself, in the ``PRV-`` form.
    An unknown field is ``400 unknown_field``."""

    customer_id: int | None = None
    session_id: str | None = None
    products: list[AdminCartProductInput | None] | None = None


class AdminCartCustomerInput(Dto):
    """The cart update body: the customer to move the cart to. ``customer_id`` is required."""

    customer_id: int | None = None


class AdminCartItemsInput(Dto):
    """The add-lines body. Adding a product already on the cart raises that line's quantity."""

    products: list[AdminCartProductInput | None] | None = None


class AdminCartItemUpdateInput(Dto):
    """The line update body: the new ``quantity``, required."""

    quantity: int | None = None


class AdminCheckoutInput(Dto):
    """The checkout update body. ``delivery_type`` is ``shipping``, ``delivery``,
    ``others_shipping`` or ``store_pickup``; an address replaces the whole one."""

    delivery_type: str | None = None
    billing_address: OrderAddressInput | None = None
    shipping_address: OrderAddressInput | None = None


class AdminCheckoutCodeInput(Dto):
    """The body of a coupon or gift card call: ``code``, required."""

    code: str | None = None


class AdminCheckoutPaymentInput(Dto):
    """The payment a confirm records. ``amount`` and ``payment_method`` are required; an
    ``amount`` above what is due is refused."""

    amount: float | None = None
    payment_status: str | None = None
    payment_method: str | None = None
    transaction_reference: str | None = None
    transaction_date: str | None = None


class AdminCheckoutConfirmInput(Dto):
    """The confirm body, bare, and optional. ``payment_gateway`` takes one of the store's codes,
    such as ``PIS``; an unknown field is ``400``."""

    payment_gateway: str | None = None
    transaction_no: str | None = None
    send_email: bool | None = None
    payment: AdminCheckoutPaymentInput | None = None


class AdminCheckoutDeliveryScheduleInput(Dto):
    """The delivery schedule to choose: its ``id`` and the ``date`` wanted, both required."""

    id: int | None = None
    date: str | None = None
