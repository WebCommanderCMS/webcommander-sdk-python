"""Path templates for the shipping rate endpoints."""

from __future__ import annotations

SHIPPING_RATES = "/api/{api_version}/admin/shipping_rates"
SHIPPING_RATES_COUNT = "/api/{api_version}/admin/shipping_rates/count"
SHIPPING_RATE = "/api/{api_version}/admin/shipping_rates/{shipping_rate_id}"

#: Files the record under a transaction number; a differing ``transaction_no`` beside the wrapper is ``400 header_body_mismatch``, one inside is not compared.
TRANSACTION_NO_HEADER = "X-Transaction-No"
