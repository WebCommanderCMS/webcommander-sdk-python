"""Path templates for the country endpoints."""

from __future__ import annotations

COUNTRIES = "/api/{api_version}/admin/countries"
COUNTRY = "/api/{api_version}/admin/countries/{country_id}"
COUNTRY_STATES = "/api/{api_version}/admin/countries/{country_id}/states"
COUNTRY_STATE = "/api/{api_version}/admin/countries/{country_id}/states/{state_id}"
