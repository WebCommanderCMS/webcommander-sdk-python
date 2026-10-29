"""Path templates for the category endpoints."""

from __future__ import annotations

CATEGORIES = "/api/{api_version}/admin/categories"
CATEGORIES_COUNT = "/api/{api_version}/admin/categories/count"
CATEGORIES_CHECK_NAME = "/api/{api_version}/admin/categories/check-name"
CATEGORY = "/api/{api_version}/admin/categories/{category_id}"
CATEGORY_SECTION = "/api/{api_version}/admin/categories/{category_id}/{section}"

#: The six ``{section}`` path values, each also a key of the row and of ``group_meta``.
CATEGORY_SECTIONS = (
    "general",
    "description",
    "images_media",
    "availability_visibility",
    "tax_shipping",
    "assign_products",
)

#: Files a new category under this transaction number; it beats ``category.transaction_no``.
TRANSACTION_NO_HEADER = "X-Transaction-No"
