"""Path templates for the inventory location endpoints."""

from __future__ import annotations

INVENTORY_LOCATIONS = "/api/{api_version}/admin/inventory_locations"
INVENTORY_LOCATION = "/api/{api_version}/admin/inventory_locations/{inventory_location_id}"
INVENTORY_LOCATION_STOCK = (
    "/api/{api_version}/admin/inventory_locations/{inventory_location_id}/stock"
)
INVENTORY_LOCATION_DEFAULT = (
    "/api/{api_version}/admin/inventory_locations/{inventory_location_id}/default"
)
INVENTORY_LOCATION_STATUS = (
    "/api/{api_version}/admin/inventory_locations/{inventory_location_id}/status"
)
