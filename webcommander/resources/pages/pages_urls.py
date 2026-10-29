"""Path templates for the page endpoints."""

from __future__ import annotations

PAGES = "/api/{api_version}/admin/pages"
PAGES_COUNT = "/api/{api_version}/admin/pages/count"
PAGE = "/api/{api_version}/admin/pages/{page_id}"
PAGE_URL = "/api/{api_version}/admin/pages/{page_id}/url"
PAGE_LANDING = "/api/{api_version}/admin/pages/{page_id}/landing"
PAGE_DELETE_BLOCKERS = "/api/{api_version}/admin/pages/{page_id}/delete-blockers"
PAGE_DUPLICATE = "/api/{api_version}/admin/pages/{page_id}/duplicate"

#: Carries the ``ETag`` a read answered; a stale one makes the write ``412``.
IF_MATCH_HEADER = "If-Match"
