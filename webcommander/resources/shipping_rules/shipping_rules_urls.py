"""Path templates for the shipping rule endpoints."""

from __future__ import annotations

SHIPPING_RULES = "/api/{api_version}/admin/shipping_rules"
SHIPPING_RULES_COUNT = "/api/{api_version}/admin/shipping_rules/count"
SHIPPING_RULE = "/api/{api_version}/admin/shipping_rules/{shipping_rule_id}"

#: Files the record under a transaction number; it wins over a ``transaction_no`` in the body.
TRANSACTION_NO_HEADER = "X-Transaction-No"
