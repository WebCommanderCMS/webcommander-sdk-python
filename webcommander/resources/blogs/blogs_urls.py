"""Path templates for the blog endpoints."""

from __future__ import annotations

BLOGS = "/api/{api_version}/admin/blogs"
BLOGS_COUNT = "/api/{api_version}/admin/blogs/count"
BLOG = "/api/{api_version}/admin/blogs/{blog_id}"
BLOG_COMMENTS = "/api/{api_version}/admin/blogs/{blog_id}/comments"
BLOG_COMMENT = "/api/{api_version}/admin/blogs/{blog_id}/comments/{blog_comment_id}"
BLOG_COMMENT_APPROVE = "/api/{api_version}/admin/blogs/{blog_id}/comments/{blog_comment_id}/approve"
BLOG_COMMENT_MARK_SPAM = (
    "/api/{api_version}/admin/blogs/{blog_id}/comments/{blog_comment_id}/mark-spam"
)
