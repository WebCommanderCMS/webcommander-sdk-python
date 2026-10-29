"""Path templates for the currency endpoints."""

from __future__ import annotations

CURRENCIES = "/api/{api_version}/admin/currencies"
CURRENCIES_COUNT = "/api/{api_version}/admin/currencies/count"
CURRENCY = "/api/{api_version}/admin/currencies/{currency_id}"
CURRENCY_BASE = "/api/{api_version}/admin/currencies/{currency_id}/base"

#: Files a new currency under this transaction number, the only way: a body field is ``400``.
TRANSACTION_NO_HEADER = "X-Transaction-No"
