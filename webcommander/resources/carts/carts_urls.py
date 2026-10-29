"""Path templates for the cart endpoints."""

from __future__ import annotations

CARTS = "/api/{api_version}/carts"
CART = "/api/{api_version}/carts/{session_id}"
CART_ITEM = "/api/{api_version}/carts/{session_id}/cart_items/{cart_item_id}"
CART_ORDER = "/api/{api_version}/admin/orders/carts/{session_id}"

#: Files the order a cart becomes under this transaction number; it beats ``transaction_no``.
TRANSACTION_NO_HEADER = "X-Transaction-No"
