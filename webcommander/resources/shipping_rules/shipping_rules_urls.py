"""Path templates for the shipping rule endpoints."""

from __future__ import annotations

SHIPPING_RULES = "/api/{api_version}/admin/shipping_rules"
SHIPPING_RULES_COUNT = "/api/{api_version}/admin/shipping_rules/count"
SHIPPING_RULE = "/api/{api_version}/admin/shipping_rules/{shipping_rule_id}"

#: Files the record under a transaction number; a differing ``transaction_no`` beside the wrapper is ``400 header_body_mismatch``, one inside is not compared.
TRANSACTION_NO_HEADER = "X-Transaction-No"
