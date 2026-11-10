"""Path templates for the dashboard section endpoints."""

from __future__ import annotations

DASHBOARD_SECTION = "/api/{api_version}/admin/dashboard/sections/{section}"

#: The five ``{section}`` path values, the tabs of the Dashboard's ``section_tabs`` section.
DASHBOARD_SECTIONS = ("ecommerce", "content", "bookings", "courses", "blog")
