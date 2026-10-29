"""Category endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.categories import categories_urls
from webcommander.resources.categories.categories_dto import (
    Category,
    CategoryCount,
    CategoryPage,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_categories",
    "count_categories",
    "check_category_name",
    "create_category",
    "get_category",
    "update_category",
    "patch_category",
    "delete_category",
    "get_category_section",
    "patch_category_section",
]

CategoryPayload = Mapping[str, Any] | str | Dto


def list_categories(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CategoryPage]:
    """List the categories, newest update first — ``GET /admin/categories``; ``limit`` caps at 20.
    ``name``/``searchText``/``parent`` filter, ``sort``/``dir`` order; unknown names are ignored."""
    return client.send_get_request(
        categories_urls.CATEGORIES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CategoryPage,
    )


def count_categories(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CategoryCount]:
    """Count the categories — ``GET /admin/categories/count``; the listing's ``name``,
    ``searchText`` and ``parent`` narrow it, and trashed rows are not counted."""
    return client.send_get_request(
        categories_urls.CATEGORIES_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CategoryCount,
    )


def check_category_name(
    client: Any,
    name: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether a name is free — ``GET /admin/categories/check-name``; read ``available``.
    Exact and case-insensitive over every level and the trash; a create refuses a top-level name."""
    return client.send_get_request(
        categories_urls.CATEGORIES_CHECK_NAME,
        query_params={"name": name},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_category(
    client: Any,
    payload: CategoryPayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Category]:
    """Create a category — ``POST /admin/categories``, answered ``201``. The body is wrapped in
    ``category`` and needs ``general.name``; a top-level row's name, trash included, is ``409``.
    ``transaction_no`` is sent as ``X-Transaction-No`` and files the category under that number."""
    require_payload(payload)
    return client.send_post_request(
        categories_urls.CATEGORIES,
        json_body=payload,
        headers=None
        if transaction_no is None
        else {categories_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Category,
    )


def get_category(
    client: Any,
    category_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Category]:
    """Retrieve one category — ``GET /admin/categories/{category_id}``; a trashed one still
    reads ``200`` with ``in_trash: true``. ``field_metadata`` adds the field schema."""
    return client.send_get_request(
        categories_urls.CATEGORY,
        path_params={"category_id": category_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Category,
    )


def update_category(
    client: Any,
    category_id: int | str,
    payload: CategoryPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Category]:
    """Replace one category — ``PUT /admin/categories/{category_id}``. Omitted fields reset but
    ``name``, ``sku``, ``url``, images and ``tax_shipping``, though its two profiles reset."""
    require_payload(payload)
    return client.send_put_request(
        categories_urls.CATEGORY,
        path_params={"category_id": category_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Category,
    )


def patch_category(
    client: Any,
    category_id: int | str,
    payload: CategoryPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Category]:
    """Merge fields into one category — ``PATCH /admin/categories/{category_id}``, across as many
    sections as the body names; what it omits keeps its stored value."""
    require_payload(payload)
    return client.send_patch_request(
        categories_urls.CATEGORY,
        path_params={"category_id": category_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Category,
    )


def delete_category(
    client: Any,
    category_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Move one category to the trash — ``DELETE /admin/categories/{category_id}``; ``204``.
    It leaves the listing and the count, and still reads ``200`` and holds its name."""
    return client.send_delete_request(
        categories_urls.CATEGORY,
        path_params={"category_id": category_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_category_section(
    client: Any,
    category_id: int | str,
    section: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Category]:
    """Read one section — ``GET /admin/categories/{category_id}/{section}``, ``section`` being
    one of ``CATEGORY_SECTIONS``; the answer is ``{"category": {<section>: {...}}}``."""
    return client.send_get_request(
        categories_urls.CATEGORY_SECTION,
        path_params={"category_id": category_id, "section": section},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Category,
    )


def patch_category_section(
    client: Any,
    category_id: int | str,
    section: str,
    payload: CategoryPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Category]:
    """Merge fields into one section, wrapped as ``{"category": {<section>: {...}}}``; any other
    section in the body is ignored. ``PATCH /admin/categories/{category_id}/{section}``"""
    require_payload(payload)
    return client.send_patch_request(
        categories_urls.CATEGORY_SECTION,
        path_params={"category_id": category_id, "section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Category,
    )
