"""Inventory location endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.inventory_locations import inventory_locations_urls
from webcommander.resources.inventory_locations.inventory_locations_dto import (
    InventoryLocation,
    InventoryLocationPage,
    InventoryLocationStock,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_inventory_locations",
    "head_inventory_locations",
    "create_inventory_location",
    "get_inventory_location",
    "head_inventory_location",
    "update_inventory_location",
    "patch_inventory_location",
    "delete_inventory_location",
    "get_inventory_location_stock",
    "set_inventory_location_default",
    "update_inventory_location_status",
]

InventoryLocationPayload = Mapping[str, Any] | str | Dto


def list_inventory_locations(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[InventoryLocationPage]:
    """List the locations — ``GET /admin/inventory_locations``. Accepts ``q``, ``limit`` (1 to
    100, default 20) and ``offset``; any other name, ``page`` included, is ``400``."""
    return client.send_get_request(
        inventory_locations_urls.INVENTORY_LOCATIONS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=InventoryLocationPage,
    )


def head_inventory_locations(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/inventory_locations``; no body."""
    return client.send_api_request(
        "HEAD",
        inventory_locations_urls.INVENTORY_LOCATIONS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_inventory_location(
    client: Any,
    payload: InventoryLocationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[InventoryLocation]:
    """Create a location — ``POST /admin/inventory_locations``, answered ``201``. The body is a bare
    record, and ``default: true`` takes the flag off the row that held it."""
    require_payload(payload)
    return client.send_post_request(
        inventory_locations_urls.INVENTORY_LOCATIONS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=InventoryLocation,
    )


def get_inventory_location(
    client: Any,
    inventory_location_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[InventoryLocation]:
    """Retrieve one location — ``GET /admin/inventory_locations/{inventory_location_id}``."""
    return client.send_get_request(
        inventory_locations_urls.INVENTORY_LOCATION,
        path_params={"inventory_location_id": inventory_location_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=InventoryLocation,
    )


def head_inventory_location(
    client: Any,
    inventory_location_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one location is there; no body.
    ``HEAD /admin/inventory_locations/{inventory_location_id}``"""
    return client.send_api_request(
        "HEAD",
        inventory_locations_urls.INVENTORY_LOCATION,
        path_params={"inventory_location_id": inventory_location_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_inventory_location(
    client: Any,
    inventory_location_id: int | str,
    payload: InventoryLocationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[InventoryLocation]:
    """Replace one location — ``PUT /admin/inventory_locations/{inventory_location_id}``. A replace,
    not a merge: an omitted ``address`` is cleared and an omitted ``active`` reads ``true``."""
    require_payload(payload)
    return client.send_put_request(
        inventory_locations_urls.INVENTORY_LOCATION,
        path_params={"inventory_location_id": inventory_location_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=InventoryLocation,
    )


def patch_inventory_location(
    client: Any,
    inventory_location_id: int | str,
    payload: InventoryLocationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[InventoryLocation]:
    """Merge fields into one location — ``PATCH /admin/inventory_locations/{inventory_location_id}``.
    A bare record of at least one field; what it omits keeps its stored value."""
    require_payload(payload)
    return client.send_patch_request(
        inventory_locations_urls.INVENTORY_LOCATION,
        path_params={"inventory_location_id": inventory_location_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=InventoryLocation,
    )


def delete_inventory_location(
    client: Any,
    inventory_location_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete a location — ``DELETE /admin/inventory_locations/{inventory_location_id}``; ``204``.
    The row holding ``default`` is ``409``: move the flag to another row first."""
    return client.send_delete_request(
        inventory_locations_urls.INVENTORY_LOCATION,
        path_params={"inventory_location_id": inventory_location_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_inventory_location_stock(
    client: Any,
    inventory_location_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[InventoryLocationStock]:
    """What one location holds; read-only, paged by ``limit`` and ``offset`` as the listing is.
    ``GET /admin/inventory_locations/{inventory_location_id}/stock``"""
    return client.send_get_request(
        inventory_locations_urls.INVENTORY_LOCATION_STOCK,
        path_params={"inventory_location_id": inventory_location_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=InventoryLocationStock,
    )


def set_inventory_location_default(
    client: Any,
    inventory_location_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[InventoryLocation]:
    """Make one location the default; takes no body, and takes the flag off the row that held it.
    ``PUT /admin/inventory_locations/{inventory_location_id}/default``"""
    return client.send_put_request(
        inventory_locations_urls.INVENTORY_LOCATION_DEFAULT,
        path_params={"inventory_location_id": inventory_location_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=InventoryLocation,
    )


def update_inventory_location_status(
    client: Any,
    inventory_location_id: int | str,
    payload: InventoryLocationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[InventoryLocation]:
    """Activate or deactivate one location; ``active`` is the only field accepted.
    ``PUT /admin/inventory_locations/{inventory_location_id}/status``"""
    require_payload(payload)
    return client.send_put_request(
        inventory_locations_urls.INVENTORY_LOCATION_STATUS,
        path_params={"inventory_location_id": inventory_location_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=InventoryLocation,
    )
