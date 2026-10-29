"""Variation type and product variant endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.variations import variations_urls
from webcommander.resources.variations.variations_dto import (
    ProductVariations,
    ProductVariationsBulkResult,
    ProductVariationsImportResult,
    Variation,
    VariationPage,
)

__all__ = [
    "list_variations",
    "head_variations",
    "create_variation",
    "get_variation",
    "head_variation",
    "update_variation",
    "patch_variation",
    "delete_variation",
    "delete_variation_option",
    "list_product_variations",
    "import_product_variations",
    "update_product_variations",
]

VariationPayload = Mapping[str, Any] | str | Dto


def list_variations(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[VariationPage]:
    """List the types by ascending id — ``GET /admin/variations``. Accepts ``search`` (name),
    ``standard``, ``limit`` (1 to 100), ``offset`` or ``page``, and ``field_metadata``."""
    return client.send_get_request(
        variations_urls.VARIATIONS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=VariationPage,
    )


def head_variations(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/variations``; no body."""
    return client.send_api_request(
        "HEAD",
        variations_urls.VARIATIONS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_variation(
    client: Any,
    payload: VariationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Variation]:
    """Create a type — ``POST /admin/variations``, answered ``201``. The body is
    ``{"variation": {...}}`` with ``name``, ``standard`` and at least one option."""
    require_payload(payload)
    return client.send_post_request(
        variations_urls.VARIATIONS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Variation,
    )


def get_variation(
    client: Any,
    variation_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Variation]:
    """Retrieve one type; ``field_metadata`` adds the schema beside it.
    ``GET /admin/variations/{variation_id}``"""
    return client.send_get_request(
        variations_urls.VARIATION,
        path_params={"variation_id": variation_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Variation,
    )


def head_variation(
    client: Any,
    variation_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one type is there; no body, the row read's ``ETag``.
    ``HEAD /admin/variations/{variation_id}``"""
    return client.send_api_request(
        "HEAD",
        variations_urls.VARIATION,
        path_params={"variation_id": variation_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_variation(
    client: Any,
    variation_id: int | str,
    payload: VariationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Variation]:
    """Replace one type — ``PUT /admin/variations/{variation_id}``. ``name`` and ``options`` are
    required, and an option left out of the list is deleted."""
    require_payload(payload)
    return client.send_put_request(
        variations_urls.VARIATION,
        path_params={"variation_id": variation_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Variation,
    )


def patch_variation(
    client: Any,
    variation_id: int | str,
    payload: VariationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Variation]:
    """Merge into one type — ``PATCH /admin/variations/{variation_id}``. Only the options sent
    are added, or changed where an ``id`` names one; the rest are kept."""
    require_payload(payload)
    return client.send_patch_request(
        variations_urls.VARIATION,
        path_params={"variation_id": variation_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Variation,
    )


def delete_variation(
    client: Any,
    variation_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one type — ``DELETE /admin/variations/{variation_id}``; ``204``. A type with
    options is ``409`` unless ``cascade`` is ``true``, which deletes them with it."""
    return client.send_delete_request(
        variations_urls.VARIATION,
        path_params={"variation_id": variation_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def delete_variation_option(
    client: Any,
    variation_id: int | str,
    variation_option_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one option of a type; ``204``, and a type's last option is ``409``.
    ``DELETE /admin/variations/{variation_id}/options/{variation_option_id}``"""
    return client.send_delete_request(
        variations_urls.VARIATION_OPTION,
        path_params={"variation_id": variation_id, "variation_option_id": variation_option_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def list_product_variations(
    client: Any,
    product_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductVariations]:
    """One product's variants, grouped, with no paging; a tax-inclusive product's prices read
    net of tax. ``GET /admin/products/{product_id}/variations``"""
    return client.send_get_request(
        variations_urls.PRODUCT_VARIATIONS,
        path_params={"product_id": product_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductVariations,
    )


def import_product_variations(
    client: Any,
    product_id: int | str,
    payload: VariationPayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductVariationsImportResult]:
    """Add or change a product's variants by ``key``; ``201``. A ``product_key`` naming other types
    than the product's is ``409``. ``POST /admin/products/{product_id}/variations``"""
    require_payload(payload)
    return client.send_post_request(
        variations_urls.PRODUCT_VARIATIONS,
        path_params={"product_id": product_id},
        json_body=payload,
        headers=None
        if transaction_no is None
        else {variations_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductVariationsImportResult,
    )


def update_product_variations(
    client: Any,
    product_id: int | str,
    payload: VariationPayload,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductVariationsBulkResult]:
    """Set fields on several variants of one product; a bare record, no envelope. ``response``
    is ``slim`` or ``full``. ``PATCH /admin/products/{product_id}/variations/bulk``"""
    require_payload(payload)
    return client.send_patch_request(
        variations_urls.PRODUCT_VARIATIONS_BULK,
        path_params={"product_id": product_id},
        query_params=query_params,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductVariationsBulkResult,
    )
