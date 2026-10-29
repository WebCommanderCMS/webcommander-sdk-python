"""Blog and blog comment endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.blogs import blogs_urls
from webcommander.resources.blogs.blogs_dto import (
    Blog,
    BlogCommentEnvelope,
    BlogCommentList,
    BlogCount,
    BlogPage,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_blogs",
    "count_blogs",
    "create_blog",
    "get_blog",
    "update_blog",
    "patch_blog",
    "delete_blog",
    "list_blog_comments",
    "create_blog_comment",
    "get_blog_comment",
    "approve_blog_comment",
    "mark_blog_comment_spam",
]

BlogPayload = Mapping[str, Any] | str | Dto


def list_blogs(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[BlogPage]:
    """List the blogs, latest ``date`` first — ``GET /admin/blogs``. ``limit`` is capped at 20;
    ``ids``, ``category`` and ``visibility`` filter, and an unknown name is ``400``."""
    return client.send_get_request(
        blogs_urls.BLOGS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=BlogPage,
    )


def count_blogs(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[BlogCount]:
    """How many blogs are live — ``GET /admin/blogs/count``; ``.data`` is
    ``{"blogs": {"count": N}}``, narrowed by the listing's filters and not by its paging."""
    return client.send_get_request(
        blogs_urls.BLOGS_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=BlogCount,
    )


def create_blog(
    client: Any,
    payload: BlogPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Blog]:
    """Create a blog — ``POST /admin/blogs``, answered ``201``. The body is ``{"blog": {...}}``
    with ``title`` required, unique among live and trashed blogs alike."""
    require_payload(payload)
    return client.send_post_request(
        blogs_urls.BLOGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Blog,
    )


def get_blog(
    client: Any,
    blog_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Blog]:
    """Retrieve one blog — ``GET /admin/blogs/{blog_id}``; ``field_metadata=true`` adds the
    field schema beside it, and a trashed blog is ``404``."""
    return client.send_get_request(
        blogs_urls.BLOG,
        path_params={"blog_id": blog_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Blog,
    )


def update_blog(
    client: Any,
    blog_id: int | str,
    payload: BlogPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Blog]:
    """Replace one blog — ``PUT /admin/blogs/{blog_id}``. ``title`` and ``visibility`` are
    required; every other field left out is reset, except the image and ``url``."""
    require_payload(payload)
    return client.send_put_request(
        blogs_urls.BLOG,
        path_params={"blog_id": blog_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Blog,
    )


def patch_blog(
    client: Any,
    blog_id: int | str,
    payload: BlogPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Blog]:
    """Change only the fields sent — ``PATCH /admin/blogs/{blog_id}``, in the ``blog``
    wrapper; the answer carries ``group_meta`` beside the row."""
    require_payload(payload)
    return client.send_patch_request(
        blogs_urls.BLOG,
        path_params={"blog_id": blog_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Blog,
    )


def delete_blog(
    client: Any,
    blog_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Move one blog to the trash — ``DELETE /admin/blogs/{blog_id}``; ``204``. Its title stays
    taken, and its comments stay readable."""
    return client.send_delete_request(
        blogs_urls.BLOG,
        path_params={"blog_id": blog_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def list_blog_comments(
    client: Any,
    blog_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[BlogCommentList]:
    """Every comment on one blog, oldest first and unpaged; no query parameter has an effect.
    ``GET /admin/blogs/{blog_id}/comments``"""
    return client.send_get_request(
        blogs_urls.BLOG_COMMENTS,
        path_params={"blog_id": blog_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=BlogCommentList,
    )


def create_blog_comment(
    client: Any,
    blog_id: int | str,
    payload: BlogPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[BlogCommentEnvelope]:
    """Add a comment, ``pending`` — ``POST /admin/blogs/{blog_id}/comments``, answered ``201``.
    The body is ``{"blog": {"comment": {...}}}``; without that wrapper it is ``404``."""
    require_payload(payload)
    return client.send_post_request(
        blogs_urls.BLOG_COMMENTS,
        path_params={"blog_id": blog_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=BlogCommentEnvelope,
    )


def get_blog_comment(
    client: Any,
    blog_id: int | str,
    blog_comment_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[BlogCommentEnvelope]:
    """Retrieve one comment; the top-level ``id`` is the blog's, the comment's is inside.
    ``GET /admin/blogs/{blog_id}/comments/{blog_comment_id}``"""
    return client.send_get_request(
        blogs_urls.BLOG_COMMENT,
        path_params={"blog_id": blog_id, "blog_comment_id": blog_comment_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=BlogCommentEnvelope,
    )


def approve_blog_comment(
    client: Any,
    blog_id: int | str,
    blog_comment_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[BlogCommentEnvelope]:
    """Approve one comment; takes no body, answers ``201`` and leaves ``spam`` as it was.
    ``POST /admin/blogs/{blog_id}/comments/{blog_comment_id}/approve``"""
    return client.send_post_request(
        blogs_urls.BLOG_COMMENT_APPROVE,
        path_params={"blog_id": blog_id, "blog_comment_id": blog_comment_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=BlogCommentEnvelope,
    )


def mark_blog_comment_spam(
    client: Any,
    blog_id: int | str,
    blog_comment_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[BlogCommentEnvelope]:
    """Mark one comment as spam, setting ``status`` and ``spam``; takes no body, answers ``201``.
    ``POST /admin/blogs/{blog_id}/comments/{blog_comment_id}/mark-spam``"""
    return client.send_post_request(
        blogs_urls.BLOG_COMMENT_MARK_SPAM,
        path_params={"blog_id": blog_id, "blog_comment_id": blog_comment_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=BlogCommentEnvelope,
    )
