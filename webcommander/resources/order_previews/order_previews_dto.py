"""Typed views over the order preview bodies."""

from __future__ import annotations

from webcommander.dto import Dto
from webcommander.resources.orders.orders_dto import OrderAddressInput, OrderProductInput


class PreviewSession(Dto):
    """The session block. ``session_id`` starts ``PRV-`` and is the ``preview_session_id`` of every
    other call. ``expires_at`` is 30 minutes after ``created_at``; a coupon or gift card call, applying
    or removing, moves it 30 minutes past that call, and a read does not."""

    session_id: str | None = None
    status: str | None = None
    created_at: str | None = None
    expires_at: str | None = None


class PreviewCustomer(Dto):
    """The customer as the preview shows it: the billing address names win over the record's."""

    customer_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class PreviewItem(Dto):
    """One line of the preview, priced by the store."""

    product_id: int | None = None
    product_name: str | None = None
    sku: str | None = None
    quantity: int | None = None
    price: float | None = None
    discount: float | None = None
    tax: float | None = None
    total_amount: float | None = None
    taxable: bool | None = None
    shippable: bool | None = None


class PreviewShipping(Dto):
    """The delivery the preview was priced for. A ``store_pickup`` has no shipping cost."""

    delivery_type: str | None = None
    shipping_type: str | None = None
    shipping_cost: float | None = None
    shipping_tax: float | None = None


class PreviewCoupon(Dto):
    """The coupon on the preview: ``amount`` is the discount it takes off, ``status`` ``applied``."""

    code: str | None = None
    status: str | None = None
    amount: float | None = None


class PreviewGiftCard(Dto):
    """The gift card on the preview: ``applied_amount`` is the lesser of its balance and the grand
    total. ``remaining_balance`` came back ``null``."""

    code: str | None = None
    status: str | None = None
    applied_amount: float | None = None
    remaining_balance: float | None = None


class PreviewDiscounts(Dto):
    """At most one coupon and one gift card; ``None`` for one not applied."""

    coupon: PreviewCoupon | None = None
    gift_card: PreviewGiftCard | None = None


class PreviewTotals(Dto):
    """The money. ``grand_total`` is ``sub_total`` less ``total_discount`` plus the tax, shipping
    (and its tax), handling and surcharge; a gift card lowers ``due``, not ``grand_total``."""

    sub_total: float | None = None
    total_discount: float | None = None
    total_tax: float | None = None
    shipping_cost: float | None = None
    handling_cost: float | None = None
    total_surcharge: float | None = None
    gift_card_applied: float | None = None
    grand_total: float | None = None
    due: float | None = None


class OrderPreview(Dto):
    """A preview. The start and the read answer every field; a coupon or gift card call answers
    only ``session``, ``discounts`` and ``totals``."""

    ENVELOPE_KEY = "order"

    session: PreviewSession | None = None
    customer: PreviewCustomer | None = None
    delivery_type: str | None = None
    currency_code: str | None = None
    items: list[PreviewItem | None] | None = None
    shipping: PreviewShipping | None = None
    discounts: PreviewDiscounts | None = None
    totals: PreviewTotals | None = None


class OrderPreviewInput(Dto):
    """The start body, bare. ``products`` is required. Without ``customer_id`` the billing address
    is required, and a shipping address too unless ``delivery_type`` is ``store_pickup``.
    ``delivery_type`` is ``shipping`` unless it is ``delivery``, ``others_shipping`` or
    ``store_pickup``. An unknown field, such as ``coupon_code`` or a product line's ``price``, is
    ``400``."""

    customer_id: int | None = None
    delivery_type: str | None = None
    billing_address: OrderAddressInput | None = None
    shipping_address: OrderAddressInput | None = None
    products: list[OrderProductInput | None] | None = None


class OrderPreviewCodeInput(Dto):
    """The body of a coupon or gift card call: ``code``, required, at most 100 characters."""

    code: str | None = None


class OrderPreviewPaymentInput(Dto):
    """The payment a confirm records. ``amount`` above what is due is ``422``, a missing
    ``payment_method`` is ``400``, and ``payment_status`` ``failed`` leaves the order unpaid."""

    amount: float | None = None
    payment_status: str | None = None
    payment_method: str | None = None
    transaction_reference: str | None = None
    transaction_date: str | None = None


class OrderPreviewConfirmInput(Dto):
    """The confirm body, bare, and optional. ``payment_gateway`` takes a code such as ``PIS`` and
    leaves the order unpaid; an unknown field is ``400``."""

    payment_gateway: str | None = None
    transaction_no: str | None = None
    send_email: bool | None = None
    payment: OrderPreviewPaymentInput | None = None
