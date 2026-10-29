"""Path templates for the price display settings endpoints."""

from __future__ import annotations

PRICE_DISPLAY_SETTINGS = "/api/{api_version}/admin/settings/price_display_settings"
PRICE_DISPLAY_SETTINGS_SECTION = (
    "/api/{api_version}/admin/settings/price_display_settings/{section}"
)
