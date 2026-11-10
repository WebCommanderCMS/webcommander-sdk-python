"""Path templates for the order preview endpoints."""

from __future__ import annotations

ORDER_PREVIEWS = "/api/{api_version}/admin/orders/preview"
ORDER_PREVIEW = "/api/{api_version}/admin/orders/preview/{preview_session_id}"
ORDER_PREVIEW_CONFIRM = "/api/{api_version}/admin/orders/preview/{preview_session_id}/confirm"
ORDER_PREVIEW_COUPON = "/api/{api_version}/admin/orders/preview/{preview_session_id}/coupon"
ORDER_PREVIEW_GIFT_CARD = "/api/{api_version}/admin/orders/preview/{preview_session_id}/gift-card"
