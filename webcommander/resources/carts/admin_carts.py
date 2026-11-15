"""Admin cart and checkout endpoints, under ``/api/{api_version}/admin/orders``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.carts import admin_carts_urls
from webcommander.resources.carts.admin_carts_dto import AdminCart, AdminCheckout
from webcommander.resources.orders.orders_dto import FlatOrder
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "create_admin_cart",
    "get_admin_cart",
    "replace_admin_cart",
    "update_admin_cart",
    "delete_admin_cart",
    "add_admin_cart_items",
    "clear_admin_cart_items",
    "update_admin_cart_item",
    "delete_admin_cart_item",
    "get_checkout",
    "update_checkout",
    "confirm_checkout",
    "apply_checkout_coupon",
    "remove_checkout_coupon",
    "apply_checkout_gift_card",
    "remove_checkout_gift_card",
    "get_checkout_delivery_schedules",
    "set_checkout_delivery_schedule",
    "clear_checkout_delivery_schedule",
]

AdminCartPayload = Mapping[str, Any] | str | Dto


def create_admin_cart(
    client: Any,
    payload: AdminCartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCart]:
    """Start a cart for a customer — ``POST /admin/orders/carts``, ``201``. ``customer_id`` is the
    customer's ``customer_id`` and ``products`` (``product_id`` and ``quantity``) is required. Keep
    ``cart.session.session_id``: every other call takes it as ``session_id``. The session lasts 30
    minutes from the last write."""
    require_payload(payload)
    return client.send_post_request(
        admin_carts_urls.ADMIN_CARTS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCart,
    )


def get_admin_cart(
    client: Any,
    session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCart]:
    """Read the cart — ``GET /admin/orders/carts/{session_id}``, where the slot takes
    ``cart.session.session_id``. A deleted cart is ``410 session_deleted`` and one an order was
    placed from is ``410 session_confirmed``."""
    return client.send_get_request(
        admin_carts_urls.ADMIN_CART,
        path_params={"session_id": session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCart,
    )


def replace_admin_cart(
    client: Any,
    session_id: str,
    payload: AdminCartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCart]:
    """Replace the cart's customer and lines — ``PUT /admin/orders/carts/{session_id}``, ``200``.
    ``customer_id`` and ``products`` are both sent. The lines are put on again, so each gets a new
    ``cart_item_id``."""
    require_payload(payload)
    return client.send_put_request(
        admin_carts_urls.ADMIN_CART,
        path_params={"session_id": session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCart,
    )


def update_admin_cart(
    client: Any,
    session_id: str,
    payload: AdminCartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCart]:
    """Change the cart's customer — ``PATCH /admin/orders/carts/{session_id}``, ``200``. Only
    ``customer_id`` is taken, and it is required: ``products`` is ``400 unknown_field``."""
    require_payload(payload)
    return client.send_patch_request(
        admin_carts_urls.ADMIN_CART,
        path_params={"session_id": session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCart,
    )


def delete_admin_cart(
    client: Any,
    session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete the cart — ``DELETE /admin/orders/carts/{session_id}``; ``204`` with no body, after
    which every call on the session is ``410``."""
    return client.send_delete_request(
        admin_carts_urls.ADMIN_CART,
        path_params={"session_id": session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def add_admin_cart_items(
    client: Any,
    session_id: str,
    payload: AdminCartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCart]:
    """Put products on the cart — ``POST /admin/orders/carts/{session_id}/cart_items``, ``201``
    with the whole cart. ``products`` is required; one already on the cart raises that line's
    quantity."""
    require_payload(payload)
    return client.send_post_request(
        admin_carts_urls.ADMIN_CART_ITEMS,
        path_params={"session_id": session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCart,
    )


def clear_admin_cart_items(
    client: Any,
    session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCart]:
    """Take every line off the cart — ``DELETE /admin/orders/carts/{session_id}/cart_items``,
    ``200`` with the empty cart. The session stays."""
    return client.send_delete_request(
        admin_carts_urls.ADMIN_CART_ITEMS,
        path_params={"session_id": session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCart,
    )


def update_admin_cart_item(
    client: Any,
    session_id: str,
    cart_item_id: int | str,
    payload: AdminCartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCart]:
    """Set one line's quantity — ``PATCH /admin/orders/carts/{session_id}/cart_items/{cart_item_id}``,
    ``200`` with the cart. ``cart_item_id`` is a line's ``cart_item_id`` and ``quantity`` is
    required. A line the cart does not hold is ``404``."""
    require_payload(payload)
    return client.send_patch_request(
        admin_carts_urls.ADMIN_CART_ITEM,
        path_params={"session_id": session_id, "cart_item_id": cart_item_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCart,
    )


def delete_admin_cart_item(
    client: Any,
    session_id: str,
    cart_item_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCart]:
    """Take one line off the cart —
    ``DELETE /admin/orders/carts/{session_id}/cart_items/{cart_item_id}``, ``200`` with the cart.
    ``cart_item_id`` is a line's ``cart_item_id``; one the cart does not hold is ``404``."""
    return client.send_delete_request(
        admin_carts_urls.ADMIN_CART_ITEM,
        path_params={"session_id": session_id, "cart_item_id": cart_item_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCart,
    )


def get_checkout(
    client: Any,
    session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCheckout]:
    """Read the checkout of a cart — ``GET /admin/orders/checkout/{session_id}``. ``issues`` lists
    what still blocks a confirm, ``delivery_type`` ``required`` until one is set; the addresses
    start as the customer's."""
    return client.send_get_request(
        admin_carts_urls.ADMIN_CHECKOUT,
        path_params={"session_id": session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCheckout,
    )


def update_checkout(
    client: Any,
    session_id: str,
    payload: AdminCartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCheckout]:
    """Set the delivery and addresses — ``PATCH /admin/orders/checkout/{session_id}``, ``200`` with
    the priced checkout. Only ``delivery_type``, ``billing_address`` and ``shipping_address`` are
    taken. The shipping and handling cost follow the shipping address, so set it with
    ``delivery_type``."""
    require_payload(payload)
    return client.send_patch_request(
        admin_carts_urls.ADMIN_CHECKOUT,
        path_params={"session_id": session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCheckout,
    )


def confirm_checkout(
    client: Any,
    session_id: str,
    payload: AdminCartPayload | None = None,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[FlatOrder]:
    """Place the order — ``POST /admin/orders/checkout/{session_id}/confirm``; ``201`` with the
    order, and the body optional. This creates a real order and closes the session, so every later
    call on it is ``410 session_confirmed``. A checkout with ``issues`` is ``422 checkout_incomplete``. Without a
    ``payment`` the order is unpaid. ``transaction_no`` is sent as ``X-Transaction-No`` and files
    the order under that number."""
    return client.send_post_request(
        admin_carts_urls.ADMIN_CHECKOUT_CONFIRM,
        path_params={"session_id": session_id},
        json_body=payload,
        headers=None
        if transaction_no is None
        else {admin_carts_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=FlatOrder,
    )


def apply_checkout_coupon(
    client: Any,
    session_id: str,
    payload: AdminCartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCheckout]:
    """Apply a coupon — ``POST /admin/orders/checkout/{session_id}/coupon``, ``200``. ``code`` is
    required. One coupon at a time: a second is ``409``, and a code the store does not accept is
    ``422 invalid_coupon``."""
    require_payload(payload)
    return client.send_post_request(
        admin_carts_urls.ADMIN_CHECKOUT_COUPON,
        path_params={"session_id": session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCheckout,
    )


def remove_checkout_coupon(
    client: Any,
    session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCheckout]:
    """Remove the coupon — ``DELETE /admin/orders/checkout/{session_id}/coupon``. With none applied
    it is ``404 coupon_not_applied``."""
    return client.send_delete_request(
        admin_carts_urls.ADMIN_CHECKOUT_COUPON,
        path_params={"session_id": session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCheckout,
    )


def apply_checkout_gift_card(
    client: Any,
    session_id: str,
    payload: AdminCartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCheckout]:
    """Apply a gift card — ``POST /admin/orders/checkout/{session_id}/gift_card``, ``200``. ``code``
    is required. The card must be usable by the cart's customer, else ``422 invalid_gift_card``; a
    second card is ``409``. It lowers ``due`` and spends nothing until an order is placed."""
    require_payload(payload)
    return client.send_post_request(
        admin_carts_urls.ADMIN_CHECKOUT_GIFT_CARD,
        path_params={"session_id": session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCheckout,
    )


def remove_checkout_gift_card(
    client: Any,
    session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCheckout]:
    """Remove the gift card — ``DELETE /admin/orders/checkout/{session_id}/gift_card``. With none
    applied it is ``404 gift_card_not_applied``."""
    return client.send_delete_request(
        admin_carts_urls.ADMIN_CHECKOUT_GIFT_CARD,
        path_params={"session_id": session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCheckout,
    )


def get_checkout_delivery_schedules(
    client: Any,
    session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCheckout]:
    """Read the chosen delivery schedule — ``GET /admin/orders/checkout/{session_id}/delivery_schedules``,
    with ``session`` and ``delivery_schedule``, which is ``None`` until one is set."""
    return client.send_get_request(
        admin_carts_urls.ADMIN_CHECKOUT_DELIVERY_SCHEDULES,
        path_params={"session_id": session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCheckout,
    )


def set_checkout_delivery_schedule(
    client: Any,
    session_id: str,
    payload: AdminCartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AdminCheckout]:
    """Choose a delivery schedule and date —
    ``PUT /admin/orders/checkout/{session_id}/delivery_schedules``. ``id`` and ``date`` are both
    required. Only a ``delivery_type`` of ``delivery`` takes one (else ``422``), an unknown ``id``
    is ``404`` and one that does not apply to the order is ``422 schedule_not_applicable``."""
    require_payload(payload)
    return client.send_put_request(
        admin_carts_urls.ADMIN_CHECKOUT_DELIVERY_SCHEDULES,
        path_params={"session_id": session_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AdminCheckout,
    )


def clear_checkout_delivery_schedule(
    client: Any,
    session_id: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Clear the delivery schedule — ``DELETE /admin/orders/checkout/{session_id}/delivery_schedules``;
    ``204`` with no body, and also when none was set."""
    return client.send_delete_request(
        admin_carts_urls.ADMIN_CHECKOUT_DELIVERY_SCHEDULES,
        path_params={"session_id": session_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
