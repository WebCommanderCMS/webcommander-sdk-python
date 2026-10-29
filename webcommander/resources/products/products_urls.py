"""Path templates for the product endpoints."""

from __future__ import annotations

PRODUCTS = "/api/{api_version}/admin/products"
PRODUCT = "/api/{api_version}/admin/products/{product_id}"
PRODUCT_REVIEWS = "/api/{api_version}/admin/products/{product_id}/reviews"
PRODUCT_STOCK = "/api/{api_version}/admin/products/{product_id}/stock"
PRODUCT_STOCK_LOCATION = (
    "/api/{api_version}/admin/products/{product_id}/stock/locations/{inventory_location_id}"
)

#: Tags a write with a transaction number; it wins over a body ``transaction_no`` it disagrees with.
TRANSACTION_NO_HEADER = "X-Transaction-No"
