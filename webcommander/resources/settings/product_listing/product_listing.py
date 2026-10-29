"""Product listing endpoints, under ``/api/{api_version}/admin/settings/product_listing``.
A section here is a body key, not a path value: one ``PATCH`` on the facade writes all four."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.product_listing import product_listing_urls
from webcommander.resources.settings.product_listing.product_listing_dto import ProductListing

__all__ = [
    "get_product_listing",
    "patch_product_listing",
    "head_product_listing",
]

ProductListingPayload = Mapping[str, Any] | str | Dto


def get_product_listing(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductListing]:
    """Read the whole area — ``GET /admin/settings/product_listing``, every section inlined."""
    return client.send_get_request(
        product_listing_urls.PRODUCT_LISTING,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductListing,
    )


def patch_product_listing(
    client: Any,
    payload: ProductListingPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ProductListing]:
    """Write fields in one or more sections — ``PATCH /admin/settings/product_listing``.
    The body must be wrapped in ``product_listing``; this is the only way to write a section."""
    require_payload(payload)
    return client.send_patch_request(
        product_listing_urls.PRODUCT_LISTING,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ProductListing,
    )


def head_product_listing(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/product_listing``; no body."""
    return client.send_api_request(
        "HEAD",
        product_listing_urls.PRODUCT_LISTING,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
