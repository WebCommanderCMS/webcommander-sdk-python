"""Path templates for the country tax endpoints."""

from __future__ import annotations

TAX_COUNTRY_TAXES = "/api/{api_version}/admin/tax/country-taxes"
TAX_COUNTRY_TAX = "/api/{api_version}/admin/tax/country-taxes/{country_tax_id}"

#: Files a new country tax under this transaction number; it beats a ``transaction_no`` body field.
TRANSACTION_NO_HEADER = "X-Transaction-No"
