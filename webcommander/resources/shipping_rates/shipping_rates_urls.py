"""Path templates for the shipping rate endpoints."""

from __future__ import annotations

SHIPPING_RATES = "/api/{api_version}/admin/shipping_rates"
SHIPPING_RATES_COUNT = "/api/{api_version}/admin/shipping_rates/count"
SHIPPING_RATE = "/api/{api_version}/admin/shipping_rates/{shipping_rate_id}"

#: Files the record under a transaction number; it wins over a ``transaction_no`` in the body.
TRANSACTION_NO_HEADER = "X-Transaction-No"
