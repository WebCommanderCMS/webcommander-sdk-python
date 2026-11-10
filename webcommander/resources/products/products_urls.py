"""Path templates for the product endpoints."""

from __future__ import annotations

PRODUCTS = "/api/{api_version}/admin/products"
PRODUCTS_COUNT = "/api/{api_version}/admin/products/count"
PRODUCTS_CHECK_SKU = "/api/{api_version}/admin/products/check-sku"
PRODUCTS_SPECIAL = "/api/{api_version}/admin/products/special"
PRODUCTS_BULK_DELETE = "/api/{api_version}/admin/products/bulk-delete"
PRODUCT = "/api/{api_version}/admin/products/{product_id}"
PRODUCT_REVIEWS = "/api/{api_version}/admin/products/{product_id}/reviews"
PRODUCT_REVIEW = "/api/{api_version}/admin/products/{product_id}/reviews/{review_id}"
PRODUCT_IMAGE = "/api/{api_version}/admin/products/{product_id}/image"
PRODUCT_MEDIA = "/api/{api_version}/admin/products/{product_id}/media"
PRODUCT_MEDIA_IMAGE = "/api/{api_version}/admin/products/{product_id}/media/images/{image_id}"
PRODUCT_INVENTORIES = "/api/{api_version}/admin/products/{product_id}/inventories"
PRODUCT_STOCK = "/api/{api_version}/admin/products/{product_id}/stock"
PRODUCT_STOCK_ADJUSTMENTS = "/api/{api_version}/admin/products/{product_id}/stock/adjustments"
PRODUCT_SEO = "/api/{api_version}/admin/products/{product_id}/seo"
PRODUCT_MEDIA_ORDER = "/api/{api_version}/admin/products/{product_id}/media/order"
PRODUCT_STOCK_LOCATION = (
    "/api/{api_version}/admin/products/{product_id}/stock/locations/{inventory_location_id}"
)

#: Tags a write with a transaction number; it wins over a body ``transaction_no`` it disagrees with.
TRANSACTION_NO_HEADER = "X-Transaction-No"
