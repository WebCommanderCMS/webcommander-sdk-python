"""Search result page settings endpoints — three sections and a promotions collection, under
``/api/{api_version}/admin/settings/page_settings/search_result_page``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.customers.admin_customers_dto import Page
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.page_settings import search_result_page_urls
from webcommander.resources.settings.page_settings.search_result_page_dto import (
    ProductPromotion,
    SearchResultPage,
)

__all__ = [
    "get_search_result_page",
    "patch_search_result_page",
    "head_search_result_page",
    "get_search_result_page_section",
    "patch_search_result_page_section",
    "get_search_result_page_product_promotions",
    "head_search_result_page_product_promotions",
    "create_search_result_page_product_promotion",
    "get_search_result_page_product_promotion",
    "head_search_result_page_product_promotion",
    "patch_search_result_page_product_promotion",
    "patch_search_result_page_product_promotion_active",
    "delete_search_result_page_product_promotion",
]

SearchResultPagePayload = Mapping[str, Any] | str | Dto


def get_search_result_page(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SearchResultPage]:
    """Read the whole area; the promotions collection is not inlined.
    ``GET /admin/settings/page_settings/search_result_page``"""
    return client.send_get_request(
        search_result_page_urls.SEARCH_RESULT_PAGE,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SearchResultPage,
    )


def patch_search_result_page(
    client: Any,
    payload: SearchResultPagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SearchResultPage]:
    """Write fields in the writable section, wrapped in ``search_result_page``.
    ``PATCH /admin/settings/page_settings/search_result_page``"""
    require_payload(payload)
    return client.send_patch_request(
        search_result_page_urls.SEARCH_RESULT_PAGE,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SearchResultPage,
    )


def head_search_result_page(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable; no body.
    ``HEAD /admin/settings/page_settings/search_result_page``"""
    return client.send_api_request(
        "HEAD",
        search_result_page_urls.SEARCH_RESULT_PAGE,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_search_result_page_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SearchResultPage]:
    """Read one section, under the facade's key with the section one level in.
    ``GET /admin/settings/page_settings/search_result_page/{section}``"""
    return client.send_get_request(
        search_result_page_urls.SEARCH_RESULT_PAGE_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SearchResultPage,
    )


def patch_search_result_page_section(
    client: Any,
    section: str,
    payload: SearchResultPagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SearchResultPage]:
    """Write fields in ``product_information``, the one writable section.
    ``PATCH /admin/settings/page_settings/search_result_page/{section}``"""
    require_payload(payload)
    return client.send_patch_request(
        search_result_page_urls.SEARCH_RESULT_PAGE_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SearchResultPage,
    )


def get_search_result_page_product_promotions(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page[ProductPromotion]]:
    """List the promotions, under ``product_promotions``; ``limit`` is not applied.
    ``GET /admin/settings/page_settings/search_result_page/product_promotion``"""
    return client.send_get_request(
        search_result_page_urls.SEARCH_RESULT_PAGE_PRODUCT_PROMOTIONS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page.of(ProductPromotion),
    )


def head_search_result_page_product_promotions(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the promotions collection is reachable; no body.
    ``HEAD /admin/settings/page_settings/search_result_page/product_promotion``"""
    return client.send_api_request(
        "HEAD",
        search_result_page_urls.SEARCH_RESULT_PAGE_PRODUCT_PROMOTIONS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_search_result_page_product_promotion(
    client: Any,
    payload: SearchResultPagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductPromotion]:
    """Add a promotion, wrapped in ``product_promotion``; needs ``name``, ``rule`` and ``position``.
    ``POST /admin/settings/page_settings/search_result_page/product_promotion``"""
    require_payload(payload)
    return client.send_post_request(
        search_result_page_urls.SEARCH_RESULT_PAGE_PRODUCT_PROMOTIONS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductPromotion,
    )


def get_search_result_page_product_promotion(
    client: Any,
    promotion_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductPromotion]:
    """Read one promotion.
    ``GET /admin/settings/page_settings/search_result_page/product_promotion/{promotion_id}``"""
    return client.send_get_request(
        search_result_page_urls.SEARCH_RESULT_PAGE_PRODUCT_PROMOTION,
        path_params={"promotion_id": promotion_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductPromotion,
    )


def head_search_result_page_product_promotion(
    client: Any,
    promotion_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one promotion is there; no body, an ``ETag``, and ``404`` for an unknown id.
    ``HEAD /admin/settings/page_settings/search_result_page/product_promotion/{promotion_id}``"""
    return client.send_api_request(
        "HEAD",
        search_result_page_urls.SEARCH_RESULT_PAGE_PRODUCT_PROMOTION,
        path_params={"promotion_id": promotion_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def patch_search_result_page_product_promotion(
    client: Any,
    promotion_id: int | str,
    payload: SearchResultPagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductPromotion]:
    """Change one promotion, with a create's wrapped body; partial.
    ``PATCH /admin/settings/page_settings/search_result_page/product_promotion/{promotion_id}``"""
    require_payload(payload)
    return client.send_patch_request(
        search_result_page_urls.SEARCH_RESULT_PAGE_PRODUCT_PROMOTION,
        path_params={"promotion_id": promotion_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductPromotion,
    )


def patch_search_result_page_product_promotion_active(
    client: Any,
    promotion_id: int | str,
    payload: SearchResultPagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductPromotion]:
    """Turn one promotion on or off; ``is_active`` is the only field read.
    ``PATCH .../search_result_page/product_promotion/{promotion_id}/active``"""
    require_payload(payload)
    return client.send_patch_request(
        search_result_page_urls.SEARCH_RESULT_PAGE_PRODUCT_PROMOTION_ACTIVE,
        path_params={"promotion_id": promotion_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductPromotion,
    )


def delete_search_result_page_product_promotion(
    client: Any,
    promotion_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Remove one promotion; ``204``, and nothing here restores it.
    ``DELETE /admin/settings/page_settings/search_result_page/product_promotion/{promotion_id}``"""
    return client.send_delete_request(
        search_result_page_urls.SEARCH_RESULT_PAGE_PRODUCT_PROMOTION,
        path_params={"promotion_id": promotion_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
