"""Path templates for the admin customer endpoints."""

from __future__ import annotations

ADMIN_CUSTOMERS = "/api/{api_version}/admin/customers"
ADMIN_CUSTOMER = "/api/{api_version}/admin/customers/{customer_id}"
ADMIN_CUSTOMERS_COUNT = "/api/{api_version}/admin/customers/count"
ADMIN_CUSTOMERS_CHECK_EMAIL = "/api/{api_version}/admin/customers/check-email"
ADMIN_CUSTOMERS_EXPORT = "/api/{api_version}/admin/customers/export"
ADMIN_CUSTOMERS_IMPORT = "/api/{api_version}/admin/customers/import"
ADMIN_CUSTOMERS_BULK_RESET_PASSWORD = "/api/{api_version}/admin/customers/bulk-reset-password"
ADMIN_CUSTOMER_ADDRESSES = "/api/{api_version}/admin/customers/{customer_id}/addresses"
ADMIN_CUSTOMER_RESET_PASSWORD = "/api/{api_version}/admin/customers/{customer_id}/reset-password"
ADMIN_CUSTOMER_CHANGE_PASSWORD = "/api/{api_version}/admin/customers/{customer_id}/change-password"
ADMIN_CUSTOMER_STORE_CREDIT_ADJUSTMENTS = (
    "/api/{api_version}/admin/customers/{customer_id}/store-credit/adjustments"
)

#: Files the new customer under this transaction number; it beats a ``transaction_no`` body field.
TRANSACTION_NO_HEADER = "X-Transaction-No"
