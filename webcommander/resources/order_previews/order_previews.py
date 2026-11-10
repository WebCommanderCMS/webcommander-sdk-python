"""Order preview endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.order_previews import order_previews_urls
from webcommander.resources.order_previews.order_previews_dto import OrderPreview
from webcommander.resources.orders.orders_dto import FlatOrder
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "create_order_preview",
    "get_order_preview",
    "confirm_order_preview",
    "apply_order_preview_coupon",
    "remove_order_preview_coupon",
    "apply_order_preview_gift_card",
    "remove_order_preview_gift_card",
]

OrderPreviewPayload = Mapping[str, Any] | str | Dto


def create_order_preview(
    client: Any,
    payload: OrderPreviewPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderPreview]:
    """Start an order preview — ``POST /admin/orders/preview``, ``201``, a priced session that
    places no order. ``products`` is required; read ``order.session.session_id``, which every other
    call takes as ``preview_session_id``. The session lasts 30 minutes."""
    require_payload(payload)
    return client.send_post_request(
        order_previews_urls.ORDER_PREVIEWS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderPreview,
    )


def get_order_preview(
    client: Any,
    preview_session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderPreview]:
    """Read an order preview — ``GET /admin/orders/preview/{preview_session_id}``, where the slot
    takes the ``session_id`` the start answered. A read does not extend the session. An unknown id
    is ``404``, and a session already confirmed is ``410`` ``session_confirmed``."""
    return client.send_get_request(
        order_previews_urls.ORDER_PREVIEW,
        path_params={"preview_session_id": preview_session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderPreview,
    )


def confirm_order_preview(
    client: Any,
    preview_session_id: str,
    payload: OrderPreviewPayload | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[FlatOrder]:
    """Place the order — ``POST /admin/orders/preview/{preview_session_id}/confirm``; ``201`` with
    the created order, and the body optional. This creates a real order and closes the session,
    so a second confirm, or any other call on it, is ``410`` ``session_confirmed``. Without a
    ``payment`` the order is unpaid, and so it is after a ``payment_gateway`` alone."""
    return client.send_post_request(
        order_previews_urls.ORDER_PREVIEW_CONFIRM,
        path_params={"preview_session_id": preview_session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=FlatOrder,
    )


def apply_order_preview_coupon(
    client: Any,
    preview_session_id: str,
    payload: OrderPreviewPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderPreview]:
    """Apply a coupon — ``POST /admin/orders/preview/{preview_session_id}/coupon``, ``200`` with
    ``session``, ``discounts`` and ``totals``. One coupon at a time: a second is ``409``, and a code
    the store does not accept is ``422`` ``invalid_coupon``."""
    require_payload(payload)
    return client.send_post_request(
        order_previews_urls.ORDER_PREVIEW_COUPON,
        path_params={"preview_session_id": preview_session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderPreview,
    )


def remove_order_preview_coupon(
    client: Any,
    preview_session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Remove the coupon — ``DELETE /admin/orders/preview/{preview_session_id}/coupon``, ``204``
    with no body. With none applied it is ``404`` ``coupon_not_applied``."""
    return client.send_delete_request(
        order_previews_urls.ORDER_PREVIEW_COUPON,
        path_params={"preview_session_id": preview_session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def apply_order_preview_gift_card(
    client: Any,
    preview_session_id: str,
    payload: OrderPreviewPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderPreview]:
    """Apply a gift card — ``POST /admin/orders/preview/{preview_session_id}/gift-card``, ``200``
    with ``session``, ``discounts`` and ``totals``. The card must be the previewed customer's, active,
    paid, in date and with a balance, else ``422`` ``invalid_gift_card``; a second card is ``409``.
    It lowers ``due`` and spends nothing until an order is placed with it applied."""
    require_payload(payload)
    return client.send_post_request(
        order_previews_urls.ORDER_PREVIEW_GIFT_CARD,
        path_params={"preview_session_id": preview_session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderPreview,
    )


def remove_order_preview_gift_card(
    client: Any,
    preview_session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Remove the gift card — ``DELETE /admin/orders/preview/{preview_session_id}/gift-card``,
    ``204`` with no body. With none applied it is ``404`` ``gift_card_not_applied``."""
    return client.send_delete_request(
        order_previews_urls.ORDER_PREVIEW_GIFT_CARD,
        path_params={"preview_session_id": preview_session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
