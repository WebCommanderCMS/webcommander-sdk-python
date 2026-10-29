"""Path templates for the order custom field endpoints."""

from __future__ import annotations

ORDER_CUSTOM_FIELDS = "/api/{api_version}/admin/order_custom_fields"
ORDER_CUSTOM_FIELDS_COUNT = "/api/{api_version}/admin/order_custom_fields/count"
ORDER_CUSTOM_FIELD = "/api/{api_version}/admin/order_custom_fields/{order_custom_field_id}"
ORDER_CUSTOM_FIELD_VALIDATE_TIMESLOT = (
    "/api/{api_version}/admin/order_custom_fields/{order_custom_field_id}/validate_timeslot"
)
