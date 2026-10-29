"""Shipping method endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.shipping_methods import shipping_methods_urls
from webcommander.resources.shipping_methods.shipping_methods_dto import (
    ShippingMethod,
    ShippingMethodCount,
    ShippingMethodPage,
)

__all__ = [
    "list_shipping_methods",
    "head_shipping_methods",
    "count_shipping_methods",
    "create_shipping_method",
    "get_shipping_method",
    "head_shipping_method",
    "update_shipping_method",
    "delete_shipping_method",
    "set_shipping_method_default",
]

ShippingMethodPayload = Mapping[str, Any] | str | Dto


def list_shipping_methods(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingMethodPage]:
    """List the methods — ``GET /admin/shipping_methods``. ``limit`` is capped at 20, and an
    unknown query parameter is ``400``."""
    return client.send_get_request(
        shipping_methods_urls.SHIPPING_METHODS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingMethodPage,
    )


def head_shipping_methods(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/shipping_methods``; no body."""
    return client.send_api_request(
        "HEAD",
        shipping_methods_urls.SHIPPING_METHODS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def count_shipping_methods(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingMethodCount]:
    """How many methods the store holds — ``GET /admin/shipping_methods/count``.
    ``.data`` is ``{"shipping_methods": {"count": N}}``, and nothing narrows it."""
    return client.send_get_request(
        shipping_methods_urls.SHIPPING_METHODS_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingMethodCount,
    )


def create_shipping_method(
    client: Any,
    payload: ShippingMethodPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingMethod]:
    """Create a method — ``POST /admin/shipping_methods``, answered ``201``. The body is wrapped in
    ``shipping_method``, and ``name`` is required and must be free, or it is ``409``."""
    require_payload(payload)
    return client.send_post_request(
        shipping_methods_urls.SHIPPING_METHODS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingMethod,
    )


def get_shipping_method(
    client: Any,
    shipping_method_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingMethod]:
    """Retrieve one method — ``GET /admin/shipping_methods/{shipping_method_id}``."""
    return client.send_get_request(
        shipping_methods_urls.SHIPPING_METHOD,
        path_params={"shipping_method_id": shipping_method_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingMethod,
    )


def head_shipping_method(
    client: Any,
    shipping_method_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one method is there — ``HEAD /admin/shipping_methods/{shipping_method_id}``.
    An id no method holds is ``200`` too, so this is no existence check."""
    return client.send_api_request(
        "HEAD",
        shipping_methods_urls.SHIPPING_METHOD,
        path_params={"shipping_method_id": shipping_method_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_shipping_method(
    client: Any,
    shipping_method_id: int | str,
    payload: ShippingMethodPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingMethod]:
    """Rename one method — ``PUT /admin/shipping_methods/{shipping_method_id}``, wrapped in
    ``shipping_method``; ``name`` is the only field read."""
    require_payload(payload)
    return client.send_put_request(
        shipping_methods_urls.SHIPPING_METHOD,
        path_params={"shipping_method_id": shipping_method_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingMethod,
    )


def delete_shipping_method(
    client: Any,
    shipping_method_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete a method — ``DELETE /admin/shipping_methods/{shipping_method_id}``; ``204``.
    The default row is ``409``: move the flag with :func:`set_shipping_method_default` first."""
    return client.send_delete_request(
        shipping_methods_urls.SHIPPING_METHOD,
        path_params={"shipping_method_id": shipping_method_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def set_shipping_method_default(
    client: Any,
    shipping_method_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingMethod]:
    """Make one method the default; no body, and the flag leaves the row that held it.
    ``PUT /admin/shipping_methods/{shipping_method_id}/default``"""
    return client.send_put_request(
        shipping_methods_urls.SHIPPING_METHOD_DEFAULT,
        path_params={"shipping_method_id": shipping_method_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingMethod,
    )
