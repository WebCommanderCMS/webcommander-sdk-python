"""Path templates for the search settings endpoints."""

from __future__ import annotations

SEARCH_SETTINGS = "/api/{api_version}/admin/settings/search_settings"
SEARCH_SETTINGS_SECTION = "/api/{api_version}/admin/settings/search_settings/{section}"
SEARCH_SETTINGS_REINDEX_STATUS = "/api/{api_version}/admin/settings/search_settings/reindex_status"
