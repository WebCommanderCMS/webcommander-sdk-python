"""Path templates for the customer group endpoints."""

from __future__ import annotations

CUSTOMER_GROUPS = "/api/{api_version}/admin/customer_groups"
CUSTOMER_GROUPS_COUNT = "/api/{api_version}/admin/customer_groups/count"
CUSTOMER_GROUPS_ASSIGN = "/api/{api_version}/admin/customer_groups/assign"
CUSTOMER_GROUP = "/api/{api_version}/admin/customer_groups/{customer_group_id}"
CUSTOMER_GROUP_CUSTOMERS = "/api/{api_version}/admin/customer_groups/{customer_group_id}/customers"
CUSTOMER_GROUP_CUSTOMER = (
    "/api/{api_version}/admin/customer_groups/{customer_group_id}/customers/{customer_id}"
)
