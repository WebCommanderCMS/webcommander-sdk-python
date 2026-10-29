"""Page endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.pages import pages_urls
from webcommander.resources.pages.pages_dto import (
    Page,
    PageCount,
    PageDeleteBlockers,
    PageListing,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_pages",
    "head_pages",
    "count_pages",
    "head_pages_count",
    "create_page",
    "get_page",
    "head_page",
    "update_page",
    "patch_page",
    "delete_page",
    "update_page_url",
    "set_landing_page",
    "get_page_delete_blockers",
    "head_page_delete_blockers",
    "duplicate_page",
]

PagePayload = Mapping[str, Any] | str | Dto


def list_pages(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PageListing]:
    """List the pages outside the trash, newest change first — ``GET /admin/pages``. ``search``,
    ``active``, ``has_layout``, ``visibility``, ``created_from``/``created_to``,
    ``updated_from``/``updated_to`` (``YYYY-MM-DD``), ``author``, ``store`` and ``not_in_store``
    filter; ``sort`` and ``order`` order; ``limit`` is 1 to 100 or ``all``. Unknown names are
    ``400``."""
    return client.send_get_request(
        pages_urls.PAGES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PageListing,
    )


def head_pages(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/pages``; no body."""
    return client.send_api_request(
        "HEAD",
        pages_urls.PAGES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def count_pages(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PageCount]:
    """How many pages match — ``GET /admin/pages/count``, a bare ``{"total": N}``. The listing's
    filters narrow it; ``sort``, ``order``, ``limit`` and ``offset`` are ignored."""
    return client.send_get_request(
        pages_urls.PAGES_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PageCount,
    )


def head_pages_count(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the count is reachable — ``HEAD /admin/pages/count``; no body."""
    return client.send_api_request(
        "HEAD",
        pages_urls.PAGES_COUNT,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_page(
    client: Any,
    payload: PagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page]:
    """Create a page — ``POST /admin/pages`` with ``{"page": {...}}``, answered ``201``.
    ``name`` and ``visibility`` are required; the URL is made from the name."""
    require_payload(payload)
    return client.send_post_request(
        pages_urls.PAGES,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page,
    )


def get_page(
    client: Any,
    page_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page]:
    """Retrieve one page, with an ``ETag``; a page in the trash still reads, ``in_trash`` true.
    ``GET /admin/pages/{page_id}``"""
    return client.send_get_request(
        pages_urls.PAGE,
        path_params={"page_id": page_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page,
    )


def head_page(
    client: Any,
    page_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one page is there; no body, the ``ETag`` its ``GET`` carries.
    ``HEAD /admin/pages/{page_id}``"""
    return client.send_api_request(
        "HEAD",
        pages_urls.PAGE,
        path_params={"page_id": page_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_page(
    client: Any,
    page_id: int | str,
    payload: PagePayload,
    *,
    if_match: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page]:
    """Replace one page — ``PUT /admin/pages/{page_id}``. ``name``, ``title``, ``subtitle``,
    ``url``, ``layout``, ``visibility``, ``body_class``, ``active``, ``disable_tracking`` and
    ``password_protection`` are required, a partial body is ``400``; ``subtitle``, ``layout`` and
    ``body_class`` take ``None``. ``if_match`` is sent as ``If-Match``: a stale ``ETag`` is
    ``412``, checked before the body."""
    require_payload(payload)
    return client.send_put_request(
        pages_urls.PAGE,
        path_params={"page_id": page_id},
        json_body=payload,
        headers=None if if_match is None else {pages_urls.IF_MATCH_HEADER: if_match},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page,
    )


def patch_page(
    client: Any,
    page_id: int | str,
    payload: PagePayload,
    *,
    if_match: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page]:
    """Change only the fields sent — ``PATCH /admin/pages/{page_id}``; an empty ``page`` is
    ``400`` and a page in the trash ``409``. ``if_match`` is sent as ``If-Match``."""
    require_payload(payload)
    return client.send_patch_request(
        pages_urls.PAGE,
        path_params={"page_id": page_id},
        json_body=payload,
        headers=None if if_match is None else {pages_urls.IF_MATCH_HEADER: if_match},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page,
    )


def delete_page(
    client: Any,
    page_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    if_match: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Move a page to the trash — ``DELETE /admin/pages/{page_id}``; ``204``. ``force`` ``true``
    purges it, from the trash or live; a second plain delete is ``400``. The landing page is
    ``409``. ``if_match`` is sent as ``If-Match``."""
    return client.send_delete_request(
        pages_urls.PAGE,
        path_params={"page_id": page_id},
        query_params=query_params,
        headers=None if if_match is None else {pages_urls.IF_MATCH_HEADER: if_match},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_page_url(
    client: Any,
    page_id: int | str,
    payload: PagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page]:
    """Move a page to a new URL — ``PUT /admin/pages/{page_id}/url`` with a bare
    ``{"url": ...}``; answers the page. A URL another page holds is ``409``."""
    require_payload(payload)
    return client.send_put_request(
        pages_urls.PAGE_URL,
        path_params={"page_id": page_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page,
    )


def set_landing_page(
    client: Any,
    page_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page]:
    """Make a page the store's landing page; takes no body. The previous landing page stops
    being it. ``PATCH /admin/pages/{page_id}/landing``"""
    return client.send_patch_request(
        pages_urls.PAGE_LANDING,
        path_params={"page_id": page_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page,
    )


def get_page_delete_blockers(
    client: Any,
    page_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PageDeleteBlockers]:
    """Whether a delete would pass and what blocks it, such as ``landing_page``.
    ``GET /admin/pages/{page_id}/delete-blockers``"""
    return client.send_get_request(
        pages_urls.PAGE_DELETE_BLOCKERS,
        path_params={"page_id": page_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PageDeleteBlockers,
    )


def head_page_delete_blockers(
    client: Any,
    page_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the delete check is reachable; no body.
    ``HEAD /admin/pages/{page_id}/delete-blockers``"""
    return client.send_api_request(
        "HEAD",
        pages_urls.PAGE_DELETE_BLOCKERS,
        path_params={"page_id": page_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def duplicate_page(
    client: Any,
    page_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page]:
    """Copy a page — ``POST /admin/pages/{page_id}/duplicate``, answered ``201``; a body field is
    ``400``. The copy is ``"<name> - Copy"`` at ``<url>-copy``, then ``- Copy 1`` at ``-copy-1``."""
    return client.send_post_request(
        pages_urls.PAGE_DUPLICATE,
        path_params={"page_id": page_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page,
    )
