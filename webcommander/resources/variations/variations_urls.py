"""Path templates for the variation type and product variant endpoints."""

from __future__ import annotations

VARIATIONS = "/api/{api_version}/admin/variations"
VARIATION = "/api/{api_version}/admin/variations/{variation_id}"
VARIATION_OPTION = (
    "/api/{api_version}/admin/variations/{variation_id}/options/{variation_option_id}"
)
PRODUCT_VARIATIONS = "/api/{api_version}/admin/products/{product_id}/variations"
PRODUCT_VARIATIONS_BULK = "/api/{api_version}/admin/products/{product_id}/variations/bulk"

#: Tags a write with a transaction number; it wins over a body ``transaction_no`` it disagrees with.
TRANSACTION_NO_HEADER = "X-Transaction-No"
