"""Typed views over the order bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class Reference(Dto):
    """A country or a state as the store answers it: ``{"id", "name", "code"}``."""

    id: int | None = None
    name: str | None = None
    code: str | None = None


class OrderCustomer(Dto):
    """The order's ``customer`` section, also sent as ``customer_summary``. A listing row
    carries five of these keys; ``customer_id`` is the public id, ``internal_id`` the other."""

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


class OrderAddress(Dto):
    """A billing or shipping address. ``company_name`` reads ``""`` whatever was written."""

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


class OrderItem(Dto):
    """One order line, under ``items`` or ``order_line_details``; ``variations`` is ``[]``, except
    on a create's answer, which sends ``null``."""

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


class OrderShipping(Dto):
    """The ``shipping`` section; ``shipping_type`` is the first shipment's method."""

    delivery_type: str | None = None
    shipping_type: str | None = None
    shipping_status: str | None = None
    shipping_cost: float | None = None
    shipping_tax: float | None = None


class OrderDiscounts(Dto):
    """The ``discounts`` section."""

    total_discount: float | None = None
    coupon_code: str | None = None
    gift_card_code: str | None = None


class OrderChargesTotals(Dto):
    """The ``charges_totals`` section; a payment refund lowers ``paid`` and an order refund
    does not."""

    sub_total: float | None = None
    total_tax: float | None = None
    handling_cost: float | None = None
    total_surcharge: float | None = None
    other_charges: float | None = None
    grand_total: float | None = None
    paid: float | None = None
    due: float | None = None
    refunded: float | None = None
    refund_status: str | None = None
    items_total: int | None = None


class OrderPayment(Dto):
    """One entry of an order's ``payments``; ``gateway_response`` comes only in the flat shape."""

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


class OrderFulfillment(Dto):
    """The ``fulfillment`` section."""

    fulfillment_mode: str | None = None
    fulfillment_term: str | None = None
    invoice_mode: str | None = None
    payment_term: str | None = None
    customer_po_number: str | None = None
    external_reference_order_id: str | None = None
    external_reference_store_id: str | None = None
    external_reference_order_no: str | None = None
    external_reference_status: str | None = None
    external_reference_url: str | None = None
    custom_fields: list[Any] | None = None


class SectionMeta(Dto):
    """One ``group_meta`` entry."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block; the listing's has no entry for the two addresses."""

    customer: SectionMeta | None = None
    billing_address: SectionMeta | None = None
    shipping_address: SectionMeta | None = None
    items: SectionMeta | None = None
    shipping: SectionMeta | None = None
    discounts: SectionMeta | None = None
    charges_totals: SectionMeta | None = None
    payments: SectionMeta | None = None
    fulfillment: SectionMeta | None = None


class Order(Dto):
    """One order in sections: the row path's body, a ``PUT`` or ``PATCH`` answer, and a listing
    row, which carries no ``billing_address`` or ``shipping_address``."""

    ENVELOPE_KEY = "order"

    order_id: int | None = None
    order_no: int | None = None
    internal_id: int | None = None
    #: A UUID string the store assigns; not writable.
    uuid: str | None = None
    order_status: str | None = None
    payment_status: str | None = None
    shipping_status: str | None = None
    currency_code: str | None = None
    transaction_no: str | None = None
    ip_address: str | None = None
    order_channel: str | None = None
    created_on: str | None = None
    last_updated_on: str | None = None
    customer: OrderCustomer | None = None
    billing_address: OrderAddress | None = None
    shipping_address: OrderAddress | None = None
    items: list[OrderItem | None] | None = None
    shipping: OrderShipping | None = None
    discounts: OrderDiscounts | None = None
    charges_totals: OrderChargesTotals | None = None
    payments: list[OrderPayment | None] | None = None
    fulfillment: OrderFulfillment | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None


class Pagination(Dto):
    """The listing's ten-key ``pagination`` block; ``limit`` is the size applied, at most 20."""

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


class OrderPage(Dto):
    """One page of the listing, with the ``field_metadata`` block when it was asked for."""

    orders: list[Order | None] | None = None
    pagination: Pagination | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None


class OrderCount(Dto):
    """The count sub-path's body, ``{"orders": {"count": N}}``."""

    ENVELOPE_KEY = "orders"

    count: int | None = None


class FlatOrder(Dto):
    """One order with its totals and fulfilment at the top: what a create, a cancel and a status
    change answer, and a per-customer listing row. A create adds ``status`` beside the envelope."""

    ENVELOPE_KEY = "order"

    order_id: int | None = None
    order_no: int | None = None
    internal_id: int | None = None
    uuid: str | None = None
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
    customer_summary: OrderCustomer | None = None
    order_line_details: list[OrderItem | None] | None = None
    payments: list[OrderPayment | None] | None = None
    external_reference_order_id: str | None = None
    external_reference_store_id: str | None = None
    external_reference_order_no: str | None = None
    external_reference_status: str | None = None
    external_reference_url: str | None = None
    customer_po_number: str | None = None
    payment_term: str | None = None
    fulfillment_mode: str | None = None
    fulfillment_term: str | None = None
    invoice_mode: str | None = None
    billing_address: OrderAddress | None = None
    shipping_address: OrderAddress | None = None
    custom_fields: list[Any] | None = None
    status: str | None = None


class CustomerOrders(Dto):
    """One customer's orders, unpaged, cancelled ones left out."""

    customer_id: int | None = None
    internal_id: int | None = None
    orders: list[FlatOrder | None] | None = None


class OrderAddresses(Dto):
    """What the addresses sub-path answers: both addresses as they now stand."""

    order_id: int | None = None
    internal_id: int | None = None
    billing_address: OrderAddress | None = None
    shipping_address: OrderAddress | None = None


class OrderComment(Dto):
    """One comment; ``created`` is ``M/D/YYYY`` and a time two spaces apart, not ISO 8601."""

    ENVELOPE_KEY = "comment"

    id: int | None = None
    content: str | None = None
    admin_name: str | None = None
    visible_to_customer: bool | None = None
    admin: bool | None = None
    created: str | None = None


class OrderCommentList(Dto):
    """An order's comments, oldest first and unpaged."""

    comments: list[OrderComment | None] | None = None


class OrderCustomFields(Dto):
    """An order's custom field values; ``order_id`` echoes the ``internal_id`` asked for, and a
    ``delivery`` order adds ``delivery_cost``."""

    order_id: int | None = None
    custom_fields: list[Any] | None = None
    delivery_cost: float | None = None


class PaymentReceiptCustomer(Dto):
    """The customer a payment receipt names."""

    id: int | None = None
    internal_id: int | None = None
    name: str | None = None


class PaymentReceipt(Dto):
    """What recording a payment answers; ``id`` is the ``payment_id`` a payment refund takes."""

    ENVELOPE_KEY = "payment"

    status: str | None = None
    id: int | None = None
    date: str | None = None
    transaction_date: str | None = None
    transaction_reference: str | None = None
    payment_applied: float | None = None
    payment_method: str | None = None
    payer_info: str | None = None
    order_id: int | None = None
    order_internal_id: int | None = None
    order_total: float | None = None
    due_amount: float | None = None
    paid_amount: float | None = None
    customer: PaymentReceiptCustomer | None = None
    created_by: str | None = None
    created_at: str | None = None


class OrderRefund(Dto):
    """What an order refund answers; ``amount`` is the text that was sent."""

    status: str | None = None
    refund_id: int | None = None
    order_id: int | None = None
    internal_id: int | None = None
    amount: str | None = None


class OrderRefundRecordLine(Dto):
    """One order line a refund was spread over; the money fields are decimal text such as
    ``"1.00"``. ``ext_item_referer`` was ``null`` on every line read, so it is not typed."""

    order_item_id: int | None = None
    product_sku: str | None = None
    product_name: str | None = None
    ext_item_referer: Any = None
    plugin_line: bool | None = None
    quantity: int | None = None
    line_paid: str | None = None
    amount: str | None = None
    line_refunded_total: str | None = None
    line_fully_refunded: bool | None = None


class OrderRefundRecord(Dto):
    """One refund an order holds. ``order_id`` is the order's internal id. A payment refund fills
    ``record_only`` to ``lines``; an order refund leaves them ``null`` and ``lines`` empty.
    ``gateway_charge_id``, ``gateway_refund_id`` and ``failure_cause`` were ``null`` on every
    refund read, so they are not typed."""

    gateway: str | None = None
    gateway_charge_id: Any = None
    gateway_refund_id: Any = None
    record_only: bool | None = None
    initiated_by: str | None = None
    cancelled_with_order: bool | None = None
    notify_customer: bool | None = None
    allocation: str | None = None
    other_amount: str | None = None
    lines: list[OrderRefundRecordLine | None] | None = None
    refund_id: int | None = None
    payment_id: int | None = None
    order_id: int | None = None
    amount: float | None = None
    status: str | None = None
    transaction_status: str | None = None
    transaction_id: str | None = None
    reason: str | None = None
    failure_cause: Any = None
    created_at: str | None = None
    updated_at: str | None = None


class OrderRefundPage(Dto):
    """One page of an order's refunds, newest first. ``order_id`` is the order's internal id and
    ``order_no`` the ``{order_id}`` the path took."""

    order_id: int | None = None
    order_no: int | None = None
    refunds: list[OrderRefundRecord | None] | None = None
    pagination: Pagination | None = None


class PaymentRefund(Dto):
    """What a payment refund answers. ``order_id`` holds the order's internal id and ``order_no``
    its order id; a replay drops four flags and adds ``idempotent_replay``."""

    status: str | None = None
    refund_id: int | None = None
    payment_id: int | None = None
    order_id: int | None = None
    order_no: int | None = None
    currency: str | None = None
    amount: float | None = None
    reason: str | None = None
    gateway_refund: bool | None = None
    gateway_transaction_id: str | None = None
    transaction_status: str | None = None
    payment_status: str | None = None
    payment_refund_status: str | None = None
    order_refund_status: str | None = None
    order_refunded_total: float | None = None
    order_adjustment: float | None = None
    order_total: float | None = None
    available_for_refund: float | None = None
    adjust_with_order: bool | None = None
    refund_email_queued: bool | None = None
    inventory_readjusted: bool | None = None
    refunded_at: str | None = None
    idempotent_replay: bool | None = None


class InvoiceDispatch(Dto):
    """What sending an invoice answers: who it went to and when."""

    status: str | None = None
    order_id: int | None = None
    internal_id: int | None = None
    sent_to: str | None = None
    template: str | None = None
    invoice_document: Any = None
    sent_at: str | None = None


class ShipmentTracking(Dto):
    """One shipment as the shipment status lists it."""

    shipping_provider: str | None = None
    tracking_number: str | None = None
    last_updated: str | None = None


class ShipmentStatus(Dto):
    """The shipment status: ``unshipped``, ``partial`` or ``shipped``, where the order itself
    reads ``not_shipped`` for the first."""

    order_id: int | None = None
    internal_id: int | None = None
    shipment_status: str | None = None
    shipments_info: list[ShipmentTracking | None] | None = None


class ShipmentItem(Dto):
    """One line a shipment carries."""

    order_item_id: int | None = None
    product_id: int | None = None
    product_name: str | None = None
    product_sku: str | None = None
    shipping_class: str | None = None
    order_quantity: int | None = None
    shipped_quantity: int | None = None
    total_amount: float | None = None


class OrderShipment(Dto):
    """One shipment. A write sends ``method``, ``tracking_info`` and ``shipping_date``, read back
    as ``shipping_method``, ``tracking_number`` and ``date_created``; ``status`` sits beside."""

    ENVELOPE_KEY = "shipment"

    shipping_id: int | None = None
    order_id: int | None = None
    order_internal_id: int | None = None
    customer_id: int | None = None
    customer_internal_id: int | None = None
    order_address_id: int | None = None
    date_created: str | None = None
    tracking_number: str | None = None
    shipping_method: str | None = None
    shipping_address: OrderAddress | None = None
    billing_address: OrderAddress | None = None
    items: list[ShipmentItem | None] | None = None
    status: str | None = None


class OrderShipmentList(Dto):
    """An order's shipments, unpaged."""

    shipments: list[OrderShipment | None] | None = None


class OrderAddressInput(Dto):
    """An address to write, replacing the whole one: a field left out reads ``""``."""

    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    company_name: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    post_code: str | None = None
    phone: str | None = None
    mobile: str | None = None
    fax: str | None = None
    country_code: str | None = None
    state_code: str | None = None


class OrderProductInput(Dto):
    """One line to order, by the product's ``id``."""

    product_id: int | None = None
    quantity: int | None = None


class OrderInput(Dto):
    """The create body, with no envelope. ``payment_gateway`` takes a code, ``PIS`` for pay in
    store, and ``delivery_type`` is lower case; ``PAY_IN_STORE`` and ``SHIPPING`` are ``400``."""

    customer_id: int | None = None
    payment_gateway: str | None = None
    delivery_type: str | None = None
    is_send_email: bool | None = None
    transaction_no: str | None = None
    external_reference_order_id: str | None = None
    billing_address: OrderAddressInput | None = None
    shipping_address: OrderAddressInput | None = None
    products: list[OrderProductInput | None] | None = None
    order_channel: str | None = None
    ip_address: str | None = None


class InitialPaymentInput(Dto):
    """The payment a create-with-payment records. It is filed under method ``API``, and
    ``payer_info``, ``transaction_reference`` and ``transaction_date`` are not kept."""

    amount: float | None = None
    surcharge: float | None = None
    status: str | None = None
    payment_method: str | None = None
    track_info: str | None = None
    payer_info: str | None = None
    transaction_reference: str | None = None
    transaction_date: str | None = None


class OrderWithPaymentInput(OrderInput):
    """The create-with-payment body: a create's fields and the ``payment`` it records."""

    payment: InitialPaymentInput | None = None


class OrderUpdateInput(Dto):
    """The ``PUT`` body; it writes the customer and the two addresses, and nothing else."""

    ENVELOPE_KEY = "order"

    customer_id: int | None = None
    billing_address: OrderAddressInput | None = None
    shipping_address: OrderAddressInput | None = None


class OrderPatchInput(Dto):
    """The ``PATCH`` body: the seven fields it writes; an address sent replaces that address."""

    ENVELOPE_KEY = "order"

    order_status: str | None = None
    customer_po_number: str | None = None
    payment_term: str | None = None
    billing_address: OrderAddressInput | None = None
    shipping_address: OrderAddressInput | None = None
    order_channel: str | None = None
    ip_address: str | None = None


class OrderAddressesInput(Dto):
    """The addresses sub-path's body; at least one address, and one left out is untouched."""

    transaction_no: str | None = None
    billing_address: OrderAddressInput | None = None
    shipping_address: OrderAddressInput | None = None


class OrderCancelInput(Dto):
    """The cancel body; every field is optional and an empty request cancels too."""

    transaction_no: str | None = None
    reason: str | None = None
    refund_automatically: bool | None = None
    is_gateway_refund: bool | None = None


class OrderCommentInput(Dto):
    """The comment body, with no envelope; ``content`` is required."""

    content: str | None = None
    save_and_send: bool | None = None
    transaction_no: str | None = None


class OrderPaymentInput(Dto):
    """The payment body: ``{"payment": {...}}`` with ``transaction_no`` beside the envelope."""

    ENVELOPE_KEY = "payment"
    TOP_LEVEL = ("transaction_no",)

    amount: float | None = None
    payment_method: str | None = None
    payment_status: str | None = None
    track_info: str | None = None
    payer_info: str | None = None
    transaction_date: str | None = None
    transaction_reference: str | None = None
    surcharge: float | None = None
    transaction_no: str | None = None


class RefundLineInput(Dto):
    """One line an order refund names, by the order line's ``item_id``."""

    order_item_id: int | None = None
    quantity: int | None = None
    amount: float | None = None


class OrderRefundInput(Dto):
    """The order refund body, ``{"refund": {...}}``; ``refund_date`` is required, and ``amount``
    may not pass what was paid less earlier refunds."""

    ENVELOPE_KEY = "refund"

    amount: str | None = None
    refund_date: str | None = None
    reason: str | None = None
    line_items: list[RefundLineInput | None] | None = None


class PaymentRefundInput(Dto):
    """The payment refund body: ``{"refund": {...}}`` with ``transaction_no`` beside it."""

    ENVELOPE_KEY = "refund"
    TOP_LEVEL = ("transaction_no",)

    amount: str | None = None
    reason: str | None = None
    is_gateway_refund: bool | None = None
    send_refund_email: bool | None = None
    adjust_with_order: bool | None = None
    transaction_no: str | None = None


class ShipmentItemInput(Dto):
    """One line to ship, by the order line's ``item_id``."""

    order_item_id: int | None = None
    quantity: int | None = None


class OrderShipmentInput(Dto):
    """The shipment body; a create needs ``method``, ``shipping_date`` and ``shipment_items``. An
    update changes only what it names, and new ``shipment_items`` need ``change_note``."""

    transaction_no: str | None = None
    method: str | None = None
    tracking_info: str | None = None
    shipping_date: str | None = None
    shipment_items: list[ShipmentItemInput | None] | None = None
    change_note: str | None = None


class OrderStatusInput(Dto):
    """The status body; ``status`` is required: ``cancelled``, ``completed``, ``draft``,
    ``in_progress``, ``paused`` or ``reopened``."""

    status: str | None = None
    transaction_no: str | None = None
    refund_automatically: bool | None = None


class CustomOrderStatusInput(Dto):
    """The custom status body; ``order_id`` is required, a missing one is ``500``."""

    order_id: int | None = None
    order_status_value: str | None = None
    order_status_label: str | None = None
    order_type: str | None = None
    status_type: str | None = None
