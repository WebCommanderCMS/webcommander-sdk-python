"""Order endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.orders import orders_urls
from webcommander.resources.orders.orders_dto import (
    CustomerOrders,
    FlatOrder,
    InvoiceDispatch,
    Order,
    OrderAddresses,
    OrderComment,
    OrderCommentList,
    OrderCount,
    OrderCustomFields,
    OrderPage,
    OrderRefund,
    OrderRefundPage,
    OrderShipment,
    OrderShipmentList,
    PaymentReceipt,
    PaymentRefund,
    ShipmentStatus,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_orders",
    "count_orders",
    "create_order",
    "create_order_with_payment",
    "get_order",
    "update_order",
    "patch_order",
    "delete_order",
    "update_order_addresses",
    "cancel_order",
    "list_order_comments",
    "create_order_comment",
    "get_order_custom_fields",
    "create_order_payment",
    "list_order_refunds",
    "create_order_refund",
    "create_payment_refund",
    "send_order_invoice",
    "get_order_shipment_status",
    "list_order_shipments",
    "create_order_shipment",
    "update_order_shipment",
    "update_order_status",
    "create_order_status",
    "list_customer_orders",
]

OrderPayload = Mapping[str, Any] | str | Dto


def list_orders(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderPage]:
    """List orders — ``GET /admin/orders``, newest first; cancelled only under ``order_status``.
    ``limit`` caps at 20, ``customerId`` takes an ``internal_id``, an unknown name is ``400``."""
    return client.send_get_request(
        orders_urls.ORDERS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderPage,
    )


def count_orders(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderCount]:
    """Count orders — ``GET /admin/orders/count``, ``{"orders": {"count": N}}``. The listing's
    filters narrow it; its paging, sort and ``field_metadata`` change nothing."""
    return client.send_get_request(
        orders_urls.ORDERS_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderCount,
    )


def create_order(
    client: Any,
    payload: OrderPayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[FlatOrder]:
    """Create an order — ``POST /admin/orders``, ``201`` with the flat order shape and ``status``.
    Only ``products`` is required; ``payment_gateway`` takes a code such as ``PIS``.
    ``transaction_no`` is sent as ``X-Transaction-No`` and files the order under that number."""
    require_payload(payload)
    return client.send_post_request(
        orders_urls.ORDERS,
        json_body=payload,
        headers=None
        if transaction_no is None
        else {orders_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=FlatOrder,
    )


def create_order_with_payment(
    client: Any,
    payload: OrderPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[FlatOrder]:
    """Create an order and record a payment on it — ``POST /admin/orders/with-payment``; ``201``.
    ``payment`` is required and filed under gateway ``API``; ``transaction_no`` is dropped."""
    require_payload(payload)
    return client.send_post_request(
        orders_urls.ORDERS_WITH_PAYMENT,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=FlatOrder,
    )


def get_order(
    client: Any,
    order_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Order]:
    """Retrieve one order — ``GET /admin/orders/{order_id}``. ``field_metadata`` adds the
    listing's schema block; any other parameter is ignored."""
    return client.send_get_request(
        orders_urls.ORDER,
        path_params={"order_id": order_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Order,
    )


def update_order(
    client: Any,
    order_id: int | str,
    payload: OrderPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Order]:
    """Update an order — ``PUT /admin/orders/{order_id}``: the customer and the addresses, each
    address sent replacing the stored one. Sections left out are kept; ``items`` is ``400``."""
    require_payload(payload)
    return client.send_put_request(
        orders_urls.ORDER,
        path_params={"order_id": order_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Order,
    )


def patch_order(
    client: Any,
    order_id: int | str,
    payload: OrderPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Order]:
    """Change named fields — ``PATCH /admin/orders/{order_id}``: ``order_status``, the addresses,
    ``customer_po_number``, ``payment_term``, ``order_channel`` and ``ip_address``, flat or under
    ``fulfillment``."""
    require_payload(payload)
    return client.send_patch_request(
        orders_urls.ORDER,
        path_params={"order_id": order_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Order,
    )


def delete_order(
    client: Any,
    order_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete an order — ``DELETE /admin/orders/{order_id}``; hard. Read ``status``: ``deleted``, or
    ``not_found`` for an id no order holds, both at ``200``."""
    return client.send_delete_request(
        orders_urls.ORDER,
        path_params={"order_id": order_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_order_addresses(
    client: Any,
    order_id: int | str,
    payload: OrderPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderAddresses]:
    """Replace one or both addresses — ``PATCH /admin/orders/{order_id}/addresses``; an address
    left out is untouched, and ``country_code`` or a ``country`` object both resolve."""
    require_payload(payload)
    return client.send_patch_request(
        orders_urls.ORDER_ADDRESSES,
        path_params={"order_id": order_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderAddresses,
    )


def cancel_order(
    client: Any,
    order_id: int | str,
    payload: OrderPayload | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[FlatOrder]:
    """Cancel an order — ``POST /admin/orders/{order_id}/cancel``; ``201``, the body optional. An
    order already cancelled is ``409``; ``update_order_status`` can move it back."""
    return client.send_post_request(
        orders_urls.ORDER_CANCEL,
        path_params={"order_id": order_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=FlatOrder,
    )


def list_order_comments(
    client: Any,
    order_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderCommentList]:
    """An order's comments, oldest first and unpaged — ``GET /admin/orders/{order_id}/comments``."""
    return client.send_get_request(
        orders_urls.ORDER_COMMENTS,
        path_params={"order_id": order_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderCommentList,
    )


def create_order_comment(
    client: Any,
    order_id: int | str,
    payload: OrderPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderComment]:
    """Add a comment — ``POST /admin/orders/{order_id}/comments``; ``201``. A bare record: a
    ``comment`` wrapper hides ``content`` and is ``400``."""
    require_payload(payload)
    return client.send_post_request(
        orders_urls.ORDER_COMMENTS,
        path_params={"order_id": order_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderComment,
    )


def get_order_custom_fields(
    client: Any,
    order_internal_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderCustomFields]:
    """An order's custom field values — ``GET /admin/orders/{order_internal_id}/custom_fields``.
    Pass ``internal_id``: an ``order_id`` there reads the order whose ``internal_id`` it is."""
    return client.send_get_request(
        orders_urls.ORDER_CUSTOM_FIELDS,
        path_params={"order_internal_id": order_internal_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderCustomFields,
    )


def create_order_payment(
    client: Any,
    order_id: int | str,
    payload: OrderPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PaymentReceipt]:
    """Record a payment — ``POST /admin/orders/{order_id}/payments``; ``201``. The ``payment``
    wrapper is required, and the receipt's ``id`` is what a payment refund takes."""
    require_payload(payload)
    return client.send_post_request(
        orders_urls.ORDER_PAYMENTS,
        path_params={"order_id": order_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PaymentReceipt,
    )


def list_order_refunds(
    client: Any,
    order_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderRefundPage]:
    """List an order's refunds, newest first — ``GET /admin/orders/{order_id}/refunds``, by the
    order's ``order_id``. ``limit`` is 1 to 20 (above 20 is capped, ``0`` is ``400``), with
    ``offset`` or a 1-based ``page``; any other name is ignored."""
    return client.send_get_request(
        orders_urls.ORDER_REFUNDS,
        path_params={"order_id": order_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderRefundPage,
    )


def create_order_refund(
    client: Any,
    order_id: int | str,
    payload: OrderPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderRefund]:
    """Refund against an order — ``POST /admin/orders/{order_id}/refunds``; ``201``. It raises
    ``refunded``, leaves ``paid`` alone, and cannot pass what was paid less earlier refunds."""
    require_payload(payload)
    return client.send_post_request(
        orders_urls.ORDER_REFUNDS,
        path_params={"order_id": order_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderRefund,
    )


def create_payment_refund(
    client: Any,
    payment_id: int | str,
    payload: OrderPayload,
    idempotency_key: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PaymentRefund]:
    """Refund part of a payment — ``POST /admin/payment/{payment_id}/refunds``; ``200``. Refused
    without ``idempotency_key``; a repeat under the same key replays the first refund."""
    require_payload(payload)
    return client.send_post_request(
        orders_urls.PAYMENT_REFUNDS,
        path_params={"payment_id": payment_id},
        json_body=payload,
        headers={orders_urls.IDEMPOTENCY_KEY_HEADER: idempotency_key},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PaymentRefund,
    )


def send_order_invoice(
    client: Any,
    order_internal_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[InvoiceDispatch]:
    """Email the invoice — ``POST /admin/orders/{order_internal_id}/send-invoice``; no body. Pass
    ``internal_id``: an ``order_id`` there names the order holding it as its ``internal_id``."""
    return client.send_post_request(
        orders_urls.ORDER_SEND_INVOICE,
        path_params={"order_internal_id": order_internal_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=InvoiceDispatch,
    )


def get_order_shipment_status(
    client: Any,
    order_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShipmentStatus]:
    """How far an order has shipped — ``GET /admin/orders/{order_id}/shipment-status``."""
    return client.send_get_request(
        orders_urls.ORDER_SHIPMENT_STATUS,
        path_params={"order_id": order_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShipmentStatus,
    )


def list_order_shipments(
    client: Any,
    order_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderShipmentList]:
    """List an order's shipments — ``GET /admin/orders/{order_id}/shipments``; unpaged."""
    return client.send_get_request(
        orders_urls.ORDER_SHIPMENTS,
        path_params={"order_id": order_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderShipmentList,
    )


def create_order_shipment(
    client: Any,
    order_id: int | str,
    payload: OrderPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderShipment]:
    """Ship order lines — ``POST /admin/orders/{order_id}/shipments``; ``201``. ``method``,
    ``shipping_date`` and ``shipment_items`` are required; ``tracking_info`` may be left out."""
    require_payload(payload)
    return client.send_post_request(
        orders_urls.ORDER_SHIPMENTS,
        path_params={"order_id": order_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderShipment,
    )


def update_order_shipment(
    client: Any,
    order_id: int | str,
    shipment_id: int | str,
    payload: OrderPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderShipment]:
    """Change a shipment — ``PATCH /admin/orders/{order_id}/shipments/{shipment_id}``, by its
    ``shipping_id``; a field left out is kept, and ``shipment_items`` needs ``change_note``."""
    require_payload(payload)
    return client.send_patch_request(
        orders_urls.ORDER_SHIPMENT,
        path_params={"order_id": order_id, "shipment_id": shipment_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderShipment,
    )


def update_order_status(
    client: Any,
    order_id: int | str,
    payload: OrderPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[FlatOrder]:
    """Move an order's status — ``PATCH /admin/orders/{order_id}/update-status``; answered with the
    flat order shape. A completed or cancelled order can be moved again."""
    require_payload(payload)
    return client.send_patch_request(
        orders_urls.ORDER_UPDATE_STATUS,
        path_params={"order_id": order_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=FlatOrder,
    )


def create_order_status(
    client: Any,
    payload: OrderPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Add a custom order status — ``POST /admin/order/add-order-status``; ``201 {"success":
    "true"}``. No endpoint lists, applies or deletes one, and the order keeps its status."""
    require_payload(payload)
    return client.send_post_request(
        orders_urls.ORDER_STATUS_ADD,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def list_customer_orders(
    client: Any,
    customer_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerOrders]:
    """One customer's orders — ``GET /admin/customers/{customer_id}/orders``, by the public
    ``customer_id``; unpaged, no parameter read, and cancelled orders left out."""
    return client.send_get_request(
        orders_urls.CUSTOMER_ORDERS,
        path_params={"customer_id": customer_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerOrders,
    )
