"""Path templates for the search result page settings endpoints."""

from __future__ import annotations

SEARCH_RESULT_PAGE = "/api/{api_version}/admin/settings/page_settings/search_result_page"
SEARCH_RESULT_PAGE_SECTION = (
    "/api/{api_version}/admin/settings/page_settings/search_result_page/{section}"
)
SEARCH_RESULT_PAGE_PRODUCT_PROMOTIONS = (
    "/api/{api_version}/admin/settings/page_settings/search_result_page/product_promotion"
)
SEARCH_RESULT_PAGE_PRODUCT_PROMOTION = (
    "/api/{api_version}/admin/settings/page_settings/search_result_page/product_promotion"
    "/{promotion_id}"
)
SEARCH_RESULT_PAGE_PRODUCT_PROMOTION_ACTIVE = (
    "/api/{api_version}/admin/settings/page_settings/search_result_page/product_promotion"
    "/{promotion_id}/active"
)
