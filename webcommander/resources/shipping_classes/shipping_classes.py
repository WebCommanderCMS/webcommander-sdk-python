"""Shipping class endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.shipping_classes import shipping_classes_urls
from webcommander.resources.shipping_classes.shipping_classes_dto import (
    ShippingClass,
    ShippingClassCount,
    ShippingClassPage,
)

__all__ = [
    "list_shipping_classes",
    "head_shipping_classes",
    "count_shipping_classes",
    "create_shipping_class",
    "get_shipping_class",
    "head_shipping_class",
    "update_shipping_class",
    "delete_shipping_class",
    "set_shipping_class_default",
]

ShippingClassPayload = Mapping[str, Any] | str | Dto


def list_shipping_classes(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingClassPage]:
    """List the classes — ``GET /admin/shipping_classes``, a created row listed first. Takes
    ``limit`` (capped at 20), ``offset``, ``page`` and ``field_metadata``; ``sort`` is 400."""
    return client.send_get_request(
        shipping_classes_urls.SHIPPING_CLASSES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingClassPage,
    )


def head_shipping_classes(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection answers — ``HEAD /admin/shipping_classes``; 200 with no body."""
    return client.send_api_request(
        "HEAD",
        shipping_classes_urls.SHIPPING_CLASSES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def count_shipping_classes(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingClassCount]:
    """How many classes the store holds — ``GET /admin/shipping_classes/count``, answering
    ``{"shipping_classes": {"count": N}}``; no query parameter narrows it."""
    return client.send_get_request(
        shipping_classes_urls.SHIPPING_CLASSES_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingClassCount,
    )


def create_shipping_class(
    client: Any,
    payload: ShippingClassPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingClass]:
    """Create a class — ``POST /admin/shipping_classes``, 201; the ``shipping_class`` wrapper is
    required, ``id`` and ``is_default`` are discarded, and an omitted ``description`` is null."""
    require_payload(payload)
    return client.send_post_request(
        shipping_classes_urls.SHIPPING_CLASSES,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingClass,
    )


def get_shipping_class(
    client: Any,
    shipping_class_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingClass]:
    """Retrieve one class — ``GET /admin/shipping_classes/{shipping_class_id}``, the row under
    ``shipping_class``; ``field_metadata=true`` adds the schema beside it. An unknown id is 404."""
    return client.send_get_request(
        shipping_classes_urls.SHIPPING_CLASS,
        path_params={"shipping_class_id": shipping_class_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingClass,
    )


def head_shipping_class(
    client: Any,
    shipping_class_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether a class's path answers — ``HEAD /admin/shipping_classes/{shipping_class_id}``;
    200 for an id the ``GET`` answers 404, so it confirms the path and not the row."""
    return client.send_api_request(
        "HEAD",
        shipping_classes_urls.SHIPPING_CLASS,
        path_params={"shipping_class_id": shipping_class_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_shipping_class(
    client: Any,
    shipping_class_id: int | str,
    payload: ShippingClassPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingClass]:
    """Replace one class — ``PUT /admin/shipping_classes/{shipping_class_id}``, wrapper and
    ``name`` required; a ``description`` left out comes back null. ``PATCH`` has no handler."""
    require_payload(payload)
    return client.send_put_request(
        shipping_classes_urls.SHIPPING_CLASS,
        path_params={"shipping_class_id": shipping_class_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingClass,
    )


def delete_shipping_class(
    client: Any,
    shipping_class_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one class — ``DELETE /admin/shipping_classes/{shipping_class_id}``, 204 and hard.
    The row holding ``is_default`` is ``409 conflict`` until the flag moves to another."""
    return client.send_delete_request(
        shipping_classes_urls.SHIPPING_CLASS,
        path_params={"shipping_class_id": shipping_class_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def set_shipping_class_default(
    client: Any,
    shipping_class_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingClass]:
    """Make one class the default — ``PUT /admin/shipping_classes/{shipping_class_id}/default``,
    no body read. The flag is exclusive: the row that held it loses it."""
    return client.send_put_request(
        shipping_classes_urls.SHIPPING_CLASS_DEFAULT,
        path_params={"shipping_class_id": shipping_class_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingClass,
    )
