"""Shopping cart settings endpoints — a facade over two sections, under
``/api/{api_version}/admin/settings/page_settings/shopping_cart``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.page_settings import shopping_cart_urls
from webcommander.resources.settings.page_settings.shopping_cart_dto import ShoppingCart

__all__ = [
    "get_shopping_cart",
    "patch_shopping_cart",
    "head_shopping_cart",
    "get_shopping_cart_section",
    "patch_shopping_cart_section",
]

ShoppingCartPayload = Mapping[str, Any] | str | Dto


def get_shopping_cart(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShoppingCart]:
    """Read the whole area — ``GET /admin/settings/page_settings/shopping_cart``."""
    return client.send_get_request(
        shopping_cart_urls.SHOPPING_CART,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShoppingCart,
    )


def patch_shopping_cart(
    client: Any,
    payload: ShoppingCartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShoppingCart]:
    """Write fields in one section or both — ``PATCH /admin/settings/page_settings/shopping_cart``.
    The body must be wrapped in ``shopping_cart``."""
    require_payload(payload)
    return client.send_patch_request(
        shopping_cart_urls.SHOPPING_CART,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShoppingCart,
    )


def head_shopping_cart(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/page_settings/shopping_cart``."""
    return client.send_api_request(
        "HEAD",
        shopping_cart_urls.SHOPPING_CART,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_shopping_cart_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShoppingCart]:
    """Read one section — ``GET /admin/settings/page_settings/shopping_cart/{section}``.
    ``.data`` is under the section's own key, with no ``group_meta``."""
    return client.send_get_request(
        shopping_cart_urls.SHOPPING_CART_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShoppingCart,
    )


def patch_shopping_cart_section(
    client: Any,
    section: str,
    payload: ShoppingCartPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShoppingCart]:
    """Write fields in one section, wrapped in the section's own key.
    ``PATCH /admin/settings/page_settings/shopping_cart/{section}``"""
    require_payload(payload)
    return client.send_patch_request(
        shopping_cart_urls.SHOPPING_CART_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShoppingCart,
    )
