"""Product endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.errors import SdkUsageError
from webcommander.resources.products import products_urls
from webcommander.resources.products.products_dto import (
    Product,
    ProductCount,
    ProductInventoryResult,
    ProductMediaImage,
    ProductMediaOrder,
    ProductMediaUploaded,
    ProductPage,
    ProductReview,
    ProductReviewList,
    ProductReviews,
    ProductsBulkDeleteResult,
    ProductSeo,
    ProductSkuCheck,
    ProductSpecialPage,
    ProductStock,
    ProductStockAdjustmentPage,
    ProductStockPatchResult,
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
    "count_products",
    "check_product_sku",
    "list_special_products",
    "bulk_delete_products",
    "list_product_reviews",
    "get_product_review",
    "patch_product_review",
    "delete_product_review",
    "create_product_inventory",
    "create_product_image",
    "create_product_media",
    "delete_product_media_image",
    "update_product_media_order",
    "patch_product_media_image",
    "get_product_seo",
    "patch_product_stock",
    "list_product_stock_adjustments",
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


def count_products(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductCount]:
    """Count products — ``GET /admin/products/count``; ``{"total": n, "count": n}``. It takes the
    list's filters (``search_text``, ``name``, ``sku``, ``ids``, ``parent``, ``product_type``,
    ``stock``, ``is_available``, ``is_inventory_enabled``, ``created_by``, ``price_from``,
    ``price_to`` and the four date bounds) and refuses its paging and sorting, and ``status``, as
    ``400 unknown_parameter``. A trashed product is not counted."""
    return client.send_get_request(
        products_urls.PRODUCTS_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductCount,
    )


def check_product_sku(
    client: Any,
    sku: str,
    exclude_product_id: int | str | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductSkuCheck]:
    """Ask whether a SKU is free — ``GET /admin/products/check-sku``. The match ignores case and
    sees a SKU held by a trashed product or by a variant; ``exclude_product_id`` is the ``id`` of a
    product that may hold it, as when that product is being edited. Any other query name, and
    ``SKU`` in capitals, is ``400 unknown_parameter``."""
    if sku is None or str(sku) == "":
        raise SdkUsageError("sku is required")
    return client.send_get_request(
        products_urls.PRODUCTS_CHECK_SKU,
        query_params={"sku": sku, "exclude_product_id": exclude_product_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductSkuCheck,
    )


def list_special_products(
    client: Any,
    query_params: Mapping[str, Any],
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductSpecialPage]:
    """List a special selection of products — ``GET /admin/products/special``. ``type`` is
    required: ``onSale``, ``featured``, ``new``, ``topSelling``, ``lastBought`` or ``lastViewed``.
    ``max`` (1 to 100, default 10) and ``offset`` page it. The last two are per customer and need
    ``customerId`` (the ``customer_id`` or ``internal_id`` of a customer) or ``customer_email``;
    ``customer_id`` is not read, and an unknown customer is ``400 unknown_reference``. A name it
    does not know is ignored."""
    return client.send_get_request(
        products_urls.PRODUCTS_SPECIAL,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductSpecialPage,
    )


def bulk_delete_products(
    client: Any,
    payload: ProductPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductsBulkDeleteResult]:
    """Move several products to the trash — ``POST /admin/products/bulk-delete``, answered ``200``
    even when an id failed. The body is ``{"ids": [...]}`` (the collection sends ``product_ids``,
    which the store answers ``400 required`` for ``ids``); an empty list is ``400``. Each id that
    is not a product is counted in ``failed`` and listed in ``errors``."""
    require_payload(payload)
    return client.send_post_request(
        products_urls.PRODUCTS_BULK_DELETE,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductsBulkDeleteResult,
    )


def list_product_reviews(
    client: Any,
    product_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductReviewList]:
    """List a product's reviews — ``GET /admin/products/{product_id}/reviews``; ``{"reviews":
    [...]}`` with no paging block. ``status``, ``limit`` and ``offset`` are in the collection and
    this store ignores them, as it does any other name."""
    return client.send_get_request(
        products_urls.PRODUCT_REVIEWS,
        path_params={"product_id": product_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductReviewList,
    )


def get_product_review(
    client: Any,
    product_id: int | str,
    review_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductReview]:
    """Read one review under ``review`` —
    ``GET /admin/products/{product_id}/reviews/{review_id}``. ``review_id`` is a review's ``id``;
    an unknown one is ``404``."""
    return client.send_get_request(
        products_urls.PRODUCT_REVIEW,
        path_params={"product_id": product_id, "review_id": review_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductReview,
    )


def patch_product_review(
    client: Any,
    product_id: int | str,
    review_id: int | str,
    payload: ProductPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductReview]:
    """Change one review — ``PATCH /admin/products/{product_id}/reviews/{review_id}``, a bare body
    answered ``200`` with the review under ``review``. ``status`` is ``pending`` (what an imported
    review without one reads) or ``approved``; ``rejected``, which the collection uses, is
    ``400 invalid_enum``. ``rating`` and ``comment`` change too."""
    require_payload(payload)
    return client.send_patch_request(
        products_urls.PRODUCT_REVIEW,
        path_params={"product_id": product_id, "review_id": review_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductReview,
    )


def delete_product_review(
    client: Any,
    product_id: int | str,
    review_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one review for good; ``204``, and a second delete is ``404``.
    ``DELETE /admin/products/{product_id}/reviews/{review_id}``"""
    return client.send_delete_request(
        products_urls.PRODUCT_REVIEW,
        path_params={"product_id": product_id, "review_id": review_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_product_inventory(
    client: Any,
    product_id: int | str,
    payload: ProductPayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductInventoryResult]:
    """Set a product's stock figure — ``POST /admin/products/{product_id}/inventories``, answered
    ``201``. The body is ``{"product": {"product_pricing_and_stock": {"track_inventory": true,
    "available_stock": n}}}``; ``low_level_stock`` sets the low level. It records a history row
    and a variant keeps its own figure. The header is stored as the product's ``transaction_no``
    when it has none, and the answer echoes the value from before the write."""
    require_payload(payload)
    return client.send_post_request(
        products_urls.PRODUCT_INVENTORIES,
        path_params={"product_id": product_id},
        json_body=payload,
        headers=None
        if transaction_no is None
        else {products_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductInventoryResult,
    )


def create_product_image(
    client: Any,
    product_id: int | str,
    payload: ProductPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductMediaUploaded]:
    """Store images on a product — ``POST /admin/products/{product_id}/image``, answered ``201``
    with the files just stored. The body is JSON, ``{"product": {"image_and_video": {"images":
    [{"filename": ..., "base64": ...}]}}}``; a multipart body is ``415``."""
    require_payload(payload)
    return client.send_post_request(
        products_urls.PRODUCT_IMAGE,
        path_params={"product_id": product_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductMediaUploaded,
    )


def create_product_media(
    client: Any,
    product_id: int | str,
    payload: ProductPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductMediaImage]:
    """Store one file on a product — ``POST /admin/products/{product_id}/media``, answered ``201``
    with a ``Location`` header and the file just stored as one flat row, not under ``product``:
    ``id``, ``filename``, ``position``, ``primary``, ``alt_text``, ``url`` and ``thumbnail_url``.
    A bare JSON body of ``type``, ``filename`` and ``content`` (base64
    or a ``data:`` URI). Only ``type`` ``images`` is accepted; ``videos`` and
    ``specification_file`` are ``400 not_supported``. ``position`` (1-based) is accepted."""
    require_payload(payload)
    return client.send_post_request(
        products_urls.PRODUCT_MEDIA,
        path_params={"product_id": product_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductMediaImage,
    )


def delete_product_media_image(
    client: Any,
    product_id: int | str,
    image_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one image from a product; ``204``, and a second delete is ``404``. ``image_id`` is
    an image's ``id`` on the product.
    ``DELETE /admin/products/{product_id}/media/images/{image_id}``"""
    return client.send_delete_request(
        products_urls.PRODUCT_MEDIA_IMAGE,
        path_params={"product_id": product_id, "image_id": image_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_product_media_order(
    client: Any,
    product_id: int | str,
    payload: ProductPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductMediaOrder]:
    """Set the order of a product's images; the first becomes ``primary``. A bare
    ``{"type": "images", "ids": [...]}`` naming every image once, answered with ``images`` in the
    new order. ``PUT /admin/products/{product_id}/media/order``"""
    require_payload(payload)
    return client.send_put_request(
        products_urls.PRODUCT_MEDIA_ORDER,
        path_params={"product_id": product_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductMediaOrder,
    )


def patch_product_media_image(
    client: Any,
    product_id: int | str,
    image_id: int | str,
    payload: ProductPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductMediaImage]:
    """Move one image to a 1-based ``position``; a bare ``{"position": n}`` is the only body, and
    the image is answered as one flat row. ``image_id`` is an image's ``id`` on the product.
    ``PATCH /admin/products/{product_id}/media/images/{image_id}``"""
    require_payload(payload)
    return client.send_patch_request(
        products_urls.PRODUCT_MEDIA_IMAGE,
        path_params={"product_id": product_id, "image_id": image_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductMediaImage,
    )


def get_product_seo(
    client: Any,
    product_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductSeo]:
    """A product's SEO, analytics, custom code, social and AI visibility settings under ``seo``.
    ``GET /admin/products/{product_id}/seo``"""
    return client.send_get_request(
        products_urls.PRODUCT_SEO,
        path_params={"product_id": product_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductSeo,
    )


def patch_product_stock(
    client: Any,
    product_id: int | str,
    payload: ProductPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductStockPatchResult]:
    """Change a product's stock; a bare body of ``tracking``, ``locations``, ``note`` and
    ``transaction_no``, at least one of them. Answered with the ``stock`` now and the
    ``adjustment`` it recorded, ``null`` when the figure did not change.
    ``PATCH /admin/products/{product_id}/stock``"""
    require_payload(payload)
    return client.send_patch_request(
        products_urls.PRODUCT_STOCK,
        path_params={"product_id": product_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductStockPatchResult,
    )


def list_product_stock_adjustments(
    client: Any,
    product_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductStockAdjustmentPage]:
    """A product's stock history, newest first, paged by ``limit`` and ``offset``.
    ``GET /admin/products/{product_id}/stock/adjustments``"""
    return client.send_get_request(
        products_urls.PRODUCT_STOCK_ADJUSTMENTS,
        path_params={"product_id": product_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductStockAdjustmentPage,
    )
