"""Blog category endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.blog_categories import blog_categories_urls
from webcommander.resources.blog_categories.blog_categories_dto import (
    BlogCategory,
    BlogCategoryPage,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_blog_categories",
    "create_blog_category",
    "get_blog_category",
    "update_blog_category",
    "delete_blog_category",
]

BlogCategoryPayload = Mapping[str, Any] | str | Dto


def list_blog_categories(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[BlogCategoryPage]:
    """List the categories, ordered by ``name`` — ``GET /admin/blog_categories``. ``limit`` (capped
    at 20), ``offset``, ``page``, ``sort``, ``dir``, ``field_metadata``; other names are ``400``."""
    return client.send_get_request(
        blog_categories_urls.BLOG_CATEGORIES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=BlogCategoryPage,
    )


def create_blog_category(
    client: Any,
    payload: BlogCategoryPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[BlogCategory]:
    """Create a category — ``POST /admin/blog_categories``, wrapped in ``blog_category``, ``201``.
    ``name`` is required and unique; a ``url`` another row holds is stored with ``-1`` appended."""
    require_payload(payload)
    return client.send_post_request(
        blog_categories_urls.BLOG_CATEGORIES,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=BlogCategory,
    )


def get_blog_category(
    client: Any,
    blog_category_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[BlogCategory]:
    """Retrieve one category — ``GET /admin/blog_categories/{blog_category_id}``."""
    return client.send_get_request(
        blog_categories_urls.BLOG_CATEGORY,
        path_params={"blog_category_id": blog_category_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=BlogCategory,
    )


def update_blog_category(
    client: Any,
    blog_category_id: int | str,
    payload: BlogCategoryPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[BlogCategory]:
    """Update a category — ``PUT /admin/blog_categories/{blog_category_id}``, wrapped as the create
    is. ``name`` is required; an omitted ``description`` is blanked, ``url`` and ``image`` kept."""
    require_payload(payload)
    return client.send_put_request(
        blog_categories_urls.BLOG_CATEGORY,
        path_params={"blog_category_id": blog_category_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=BlogCategory,
    )


def delete_blog_category(
    client: Any,
    blog_category_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete a category — ``DELETE /admin/blog_categories/{blog_category_id}``; ``204``, and
    the blogs linked to it are kept."""
    return client.send_delete_request(
        blog_categories_urls.BLOG_CATEGORY,
        path_params={"blog_category_id": blog_category_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
