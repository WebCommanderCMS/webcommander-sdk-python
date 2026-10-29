"""Cart endpoints, under ``/api/{api_version}/carts``, and the order write under ``/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.carts import carts_urls
from webcommander.resources.carts.carts_dto import Cart, CartOrder, CartSession
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "add_cart_item",
    "get_cart",
    "resolve_cart_session",
    "update_cart_item",
    "delete_cart",
    "delete_cart_item",
    "create_order_from_cart",
]

CartPayload = Mapping[str, Any] | str | Dto


def add_cart_item(
    client: Any,
    payload: CartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Cart]:
    """Add a product to the cart ``session_id`` names, creating it — ``POST /carts``, ``201``;
    re-adding raises the line's quantity. ``customer_id`` is the customer's ``internal_id``."""
    require_payload(payload)
    return client.send_post_request(
        carts_urls.CARTS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Cart,
    )


def get_cart(
    client: Any,
    session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Cart]:
    """Retrieve the cart — ``GET /carts/{session_id}``, with ``group_meta`` beside it. A cart
    with no line is ``400`` ``Your shopping cart is empty``."""
    return client.send_get_request(
        carts_urls.CART,
        path_params={"session_id": session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Cart,
    )


def resolve_cart_session(
    client: Any,
    session_id: str,
    payload: CartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CartSession]:
    """Ask which session id to use — ``PUT /carts/{session_id}``; nothing is stored. Answers the
    body's ``sessionId``, the HTTP session's id when that is empty or null, else the path's."""
    require_payload(payload)
    return client.send_put_request(
        carts_urls.CART,
        path_params={"session_id": session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CartSession,
    )


def update_cart_item(
    client: Any,
    session_id: str,
    payload: CartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Cart]:
    """Change one line's quantity — ``PATCH /carts/{session_id}``. ``cart_item_id`` and
    ``quantity`` are required; the addresses are optional."""
    require_payload(payload)
    return client.send_patch_request(
        carts_urls.CART,
        path_params={"session_id": session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Cart,
    )


def delete_cart(
    client: Any,
    session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Empty the cart — ``DELETE /carts/{session_id}``; ``204``, after which a read is ``400``."""
    return client.send_delete_request(
        carts_urls.CART,
        path_params={"session_id": session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def delete_cart_item(
    client: Any,
    session_id: str,
    cart_item_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Remove one line — ``DELETE /carts/{session_id}/cart_items/{cart_item_id}``; ``204``.
    ``cart_item_id`` is a line's ``id``; removing the last line empties the cart."""
    return client.send_delete_request(
        carts_urls.CART_ITEM,
        path_params={"session_id": session_id, "cart_item_id": cart_item_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_order_from_cart(
    client: Any,
    session_id: str,
    payload: CartPayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CartOrder]:
    """Turn the cart into an order — ``POST /admin/orders/carts/{session_id}``, ``201``, and the
    cart is gone. ``customer_id`` is the customer's ``customer_id``, not its ``internal_id``.
    ``transaction_no`` is sent as ``X-Transaction-No`` and files the order under that number."""
    require_payload(payload)
    return client.send_post_request(
        carts_urls.CART_ORDER,
        path_params={"session_id": session_id},
        json_body=payload,
        headers=None
        if transaction_no is None
        else {carts_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CartOrder,
    )
