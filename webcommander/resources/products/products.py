"""Product endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.products import products_urls
from webcommander.resources.products.products_dto import (
    Product,
    ProductPage,
    ProductReviews,
    ProductStock,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_products",
    "create_product",
    "get_product",
    "update_product",
    "patch_product",
    "delete_product",
    "import_product_reviews",
    "get_product_stock",
    "update_product_stock",
    "delete_product_stock_location",
]

ProductPayload = Mapping[str, Any] | str | Dto


def list_products(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductPage]:
    """List products, the most recently updated first — ``GET /admin/products``; each row is the
    full record the row read answers, and a trashed product is not listed. ``limit`` is 1 to 100
    (default 20, above 100 is ``400``), with ``offset`` or a 1-based ``page``. ``search_text``
    matches ``name`` or ``sku``; ``name``, ``sku``, ``ids`` (repeat the name for more; a comma list
    is ``500``), ``parent`` (a category id), ``product_type``, ``stock`` (``in``, ``out`` or
    ``low``), ``is_available``, ``is_inventory_enabled``, ``created_by``, ``price_from``,
    ``price_to``, ``created_from``, ``created_to``, ``updated_from`` and ``updated_to`` narrow it.
    ``sort`` takes ``name``, ``isAvailable``, ``sku``, ``parent``, ``basePrice``,
    ``isInventoryEnabled``, ``createdBy``, ``created``, ``updated`` or ``id``, with ``dir``;
    ``field_metadata`` adds a schema. Any other name is ``400``."""
    return client.send_get_request(
        products_urls.PRODUCTS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductPage,
    )


def create_product(
    client: Any,
    payload: ProductPayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Product]:
    """Create a product — ``POST /admin/products``, answered ``201``. A bare record: ``name`` and
    ``base_price`` are required, ``sku`` must be free, and the store makes one when left out."""
    require_payload(payload)
    return client.send_post_request(
        products_urls.PRODUCTS,
        json_body=payload,
        headers=None
        if transaction_no is None
        else {products_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Product,
    )


def get_product(
    client: Any,
    product_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Product]:
    """Retrieve one product — ``GET /admin/products/{product_id}``. ``field_metadata=true`` adds a
    field schema beside ``product``; any other name is ``400 unknown_parameter``."""
    return client.send_get_request(
        products_urls.PRODUCT,
        path_params={"product_id": product_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Product,
    )


def update_product(
    client: Any,
    product_id: int | str,
    payload: ProductPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Product]:
    """Update one product — ``PUT /admin/products/{product_id}``. A bare record merged at every
    level; it must carry ``name``, ``sku``, ``base_price``, ``product_type``, ``available``,
    ``is_on_sale``, ``available_on_date_range``, ``available_on_weekdays``, ``available_for`` and
    ``selected_customers`` (``400 required`` otherwise), and fields left out keep their values.
    ``{"product": {...}}`` is ``400 unknown_field``."""
    require_payload(payload)
    return client.send_put_request(
        products_urls.PRODUCT,
        path_params={"product_id": product_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Product,
    )


def patch_product(
    client: Any,
    product_id: int | str,
    payload: ProductPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Product]:
    """Merge into one product — ``PATCH /admin/products/{product_id}``, the same bare record the
    ``PUT`` takes; a product in the trash is ``409``."""
    require_payload(payload)
    return client.send_patch_request(
        products_urls.PRODUCT,
        path_params={"product_id": product_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Product,
    )


def delete_product(
    client: Any,
    product_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Move a product to the trash — ``DELETE /admin/products/{product_id}``; ``204``. It still
    reads back, ``status`` ``trashed``, and a second delete is ``404``."""
    return client.send_delete_request(
        products_urls.PRODUCT,
        path_params={"product_id": product_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def import_product_reviews(
    client: Any,
    product_id: int | str,
    payload: ProductPayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductReviews]:
    """Add reviews to a product; ``201`` with every review it holds. The body is
    ``{"product": {"reviews": [...]}}``. ``POST /admin/products/{product_id}/reviews``"""
    require_payload(payload)
    return client.send_post_request(
        products_urls.PRODUCT_REVIEWS,
        path_params={"product_id": product_id},
        json_body=payload,
        headers=None
        if transaction_no is None
        else {products_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductReviews,
    )


def get_product_stock(
    client: Any,
    product_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductStock]:
    """One product's stock at each location — ``GET /admin/products/{product_id}/stock``."""
    return client.send_get_request(
        products_urls.PRODUCT_STOCK,
        path_params={"product_id": product_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductStock,
    )


def update_product_stock(
    client: Any,
    product_id: int | str,
    payload: ProductPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductStock]:
    """Set the product's stock — ``PUT /admin/products/{product_id}/stock``. ``locations`` replaces
    the whole set: a location left out is unassigned, so send every row that is to stay."""
    require_payload(payload)
    return client.send_put_request(
        products_urls.PRODUCT_STOCK,
        path_params={"product_id": product_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductStock,
    )


def delete_product_stock_location(
    client: Any,
    product_id: int | str,
    inventory_location_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Unassign one location from the product; ``204``. The location must hold ``0`` units and not
    be the product's default, or it is ``409``.
    ``DELETE /admin/products/{product_id}/stock/locations/{inventory_location_id}``"""
    return client.send_delete_request(
        products_urls.PRODUCT_STOCK_LOCATION,
        path_params={"product_id": product_id, "inventory_location_id": inventory_location_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
