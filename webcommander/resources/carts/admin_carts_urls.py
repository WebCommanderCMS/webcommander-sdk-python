"""Path templates for the admin cart and checkout endpoints."""

from __future__ import annotations

ADMIN_CARTS = "/api/{api_version}/admin/orders/carts"
ADMIN_CART = "/api/{api_version}/admin/orders/carts/{session_id}"
ADMIN_CART_ITEMS = "/api/{api_version}/admin/orders/carts/{session_id}/cart_items"
ADMIN_CART_ITEM = "/api/{api_version}/admin/orders/carts/{session_id}/cart_items/{cart_item_id}"
ADMIN_CHECKOUT = "/api/{api_version}/admin/orders/checkout/{session_id}"
ADMIN_CHECKOUT_CONFIRM = "/api/{api_version}/admin/orders/checkout/{session_id}/confirm"
ADMIN_CHECKOUT_COUPON = "/api/{api_version}/admin/orders/checkout/{session_id}/coupon"
ADMIN_CHECKOUT_GIFT_CARD = "/api/{api_version}/admin/orders/checkout/{session_id}/gift_card"
ADMIN_CHECKOUT_DELIVERY_SCHEDULES = (
    "/api/{api_version}/admin/orders/checkout/{session_id}/delivery_schedules"
)

#: Files the order a checkout places under this transaction number; a differing top-level ``transaction_no`` is ``400 header_body_mismatch``.
TRANSACTION_NO_HEADER = "X-Transaction-No"
