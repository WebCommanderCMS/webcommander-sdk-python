"""Category page settings endpoints — a facade over two sections, under
``/api/{api_version}/admin/settings/page_settings/category_page``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.page_settings import category_page_urls
from webcommander.resources.settings.page_settings.category_page_dto import CategoryPage

__all__ = [
    "get_category_page",
    "patch_category_page",
    "head_category_page",
    "get_category_page_section",
    "patch_category_page_section",
]

CategoryPagePayload = Mapping[str, Any] | str | Dto


def get_category_page(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CategoryPage]:
    """Read the whole area — ``GET /admin/settings/page_settings/category_page``."""
    return client.send_get_request(
        category_page_urls.CATEGORY_PAGE,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CategoryPage,
    )


def patch_category_page(
    client: Any,
    payload: CategoryPagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CategoryPage]:
    """Write fields in one section or both — ``PATCH /admin/settings/page_settings/category_page``.
    The body must be wrapped in ``category_page``."""
    require_payload(payload)
    return client.send_patch_request(
        category_page_urls.CATEGORY_PAGE,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CategoryPage,
    )


def head_category_page(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/page_settings/category_page``."""
    return client.send_api_request(
        "HEAD",
        category_page_urls.CATEGORY_PAGE,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_category_page_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CategoryPage]:
    """Read one section — ``GET /admin/settings/page_settings/category_page/{section}``.
    ``.data`` is under the section's own key, with no ``group_meta``."""
    return client.send_get_request(
        category_page_urls.CATEGORY_PAGE_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CategoryPage,
    )


def patch_category_page_section(
    client: Any,
    section: str,
    payload: CategoryPagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CategoryPage]:
    """Write fields in one section, wrapped in the section's own key.
    ``PATCH /admin/settings/page_settings/category_page/{section}``"""
    require_payload(payload)
    return client.send_patch_request(
        category_page_urls.CATEGORY_PAGE_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CategoryPage,
    )
