"""Path templates for the common settings endpoints."""

from __future__ import annotations

# Not under /admin: the store-wide settings reader and writer, and the registration form.
SETTINGS = "/api/{api_version}/settings"
CREATE_CUSTOMER_FIELDS = "/api/{api_version}/create-customer-fields"
