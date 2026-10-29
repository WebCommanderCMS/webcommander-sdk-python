"""Path templates for the transaction-number endpoints."""

from __future__ import annotations

TRANSACTIONS = "/api/{api_version}/admin/transactions"
TRANSACTION = "/api/{api_version}/admin/transactions/{transaction_no}"
TRANSACTION_ITEMS = "/api/{api_version}/admin/transactions/{transaction_no}/items"
