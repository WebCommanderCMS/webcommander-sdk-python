"""Path templates for the order endpoints."""

from __future__ import annotations

ORDERS = "/api/{api_version}/admin/orders"
ORDERS_COUNT = "/api/{api_version}/admin/orders/count"
ORDERS_WITH_PAYMENT = "/api/{api_version}/admin/orders/with-payment"
ORDER = "/api/{api_version}/admin/orders/{order_id}"
ORDER_ADDRESSES = "/api/{api_version}/admin/orders/{order_id}/addresses"
ORDER_CANCEL = "/api/{api_version}/admin/orders/{order_id}/cancel"
ORDER_COMMENTS = "/api/{api_version}/admin/orders/{order_id}/comments"
ORDER_PAYMENTS = "/api/{api_version}/admin/orders/{order_id}/payments"
ORDER_REFUNDS = "/api/{api_version}/admin/orders/{order_id}/refunds"
ORDER_SHIPMENT_STATUS = "/api/{api_version}/admin/orders/{order_id}/shipment-status"
ORDER_SHIPMENTS = "/api/{api_version}/admin/orders/{order_id}/shipments"
ORDER_SHIPMENT = "/api/{api_version}/admin/orders/{order_id}/shipments/{shipment_id}"
ORDER_UPDATE_STATUS = "/api/{api_version}/admin/orders/{order_id}/update-status"

ORDER_CUSTOM_FIELDS = "/api/{api_version}/admin/orders/{order_id}/custom_fields"
ORDER_SEND_INVOICE = "/api/{api_version}/admin/orders/{order_id}/send-invoice"

PAYMENT_REFUNDS = "/api/{api_version}/admin/payment/{payment_id}/refunds"
ORDER_STATUS_ADD = "/api/{api_version}/admin/order/add-order-status"
CUSTOMER_ORDERS = "/api/{api_version}/admin/customers/{customer_id}/orders"

#: The header a payment refund is refused without; a repeat under one key replays the first.
IDEMPOTENCY_KEY_HEADER = "Idempotency-Key"

#: Files a created order under this transaction number; a differing top-level ``transaction_no`` is ``400 header_body_mismatch``.
TRANSACTION_NO_HEADER = "X-Transaction-No"
