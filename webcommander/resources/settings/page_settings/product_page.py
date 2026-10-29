"""Product page settings endpoints — a facade over seven sections, under
``/api/{api_version}/admin/settings/page_settings/product_page``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.page_settings import product_page_urls
from webcommander.resources.settings.page_settings.product_page_dto import ProductPage

__all__ = [
    "get_product_page",
    "patch_product_page",
    "head_product_page",
    "get_product_page_section",
    "patch_product_page_section",
]

ProductPagePayload = Mapping[str, Any] | str | Dto


def get_product_page(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductPage]:
    """Read the whole area — ``GET /admin/settings/page_settings/product_page``."""
    return client.send_get_request(
        product_page_urls.PRODUCT_PAGE,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductPage,
    )


def patch_product_page(
    client: Any,
    payload: ProductPagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductPage]:
    """Write fields in one or more sections — ``PATCH /admin/settings/page_settings/product_page``.
    The body may be wrapped in ``product_page`` or bare."""
    require_payload(payload)
    return client.send_patch_request(
        product_page_urls.PRODUCT_PAGE,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductPage,
    )


def head_product_page(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/page_settings/product_page``."""
    return client.send_api_request(
        "HEAD",
        product_page_urls.PRODUCT_PAGE,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_product_page_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductPage]:
    """Read one section — ``GET /admin/settings/page_settings/product_page/{section}``.
    ``.data`` is under the facade's key, the section one level in, with no ``group_meta``."""
    return client.send_get_request(
        product_page_urls.PRODUCT_PAGE_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductPage,
    )


def patch_product_page_section(
    client: Any,
    section: str,
    payload: ProductPagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductPage]:
    """Write fields in one section, wrapped in the facade's key or the section's own.
    ``PATCH /admin/settings/page_settings/product_page/{section}``"""
    require_payload(payload)
    return client.send_patch_request(
        product_page_urls.PRODUCT_PAGE_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductPage,
    )
