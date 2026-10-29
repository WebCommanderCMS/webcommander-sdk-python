"""Tax zone endpoints, under ``/api/{api_version}/admin/tax_zones``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.tax_zones import tax_zones_urls
from webcommander.resources.tax_zones.tax_zones_dto import TaxZone, TaxZonePage

__all__ = [
    "list_tax_zones",
    "head_tax_zones",
    "create_tax_zone",
    "get_tax_zone",
    "head_tax_zone",
    "update_tax_zone",
    "delete_tax_zone",
]

TaxZonePayload = Mapping[str, Any] | str | Dto


def list_tax_zones(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxZonePage]:
    """List the tax zones — ``GET /admin/tax_zones``. ``limit`` is capped at 20."""
    return client.send_get_request(
        tax_zones_urls.TAX_ZONES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxZonePage,
    )


def head_tax_zones(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/tax_zones``; no body."""
    return client.send_api_request(
        "HEAD",
        tax_zones_urls.TAX_ZONES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_tax_zone(
    client: Any,
    payload: TaxZonePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxZone]:
    """Create a tax zone — ``POST /admin/tax_zones``, answered ``201``. The body is wrapped in
    ``tax_zone``, and ``countries`` and ``states`` take records such as ``[{"id": 12}]``."""
    require_payload(payload)
    return client.send_post_request(
        tax_zones_urls.TAX_ZONES,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxZone,
    )


def get_tax_zone(
    client: Any,
    tax_zone_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxZone]:
    """Retrieve one tax zone — ``GET /admin/tax_zones/{tax_zone_id}``."""
    return client.send_get_request(
        tax_zones_urls.TAX_ZONE,
        path_params={"tax_zone_id": tax_zone_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxZone,
    )


def head_tax_zone(
    client: Any,
    tax_zone_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one tax zone is there — ``HEAD /admin/tax_zones/{tax_zone_id}``; no body.
    An id no row holds is ``200`` too, so this does not prove the row exists."""
    return client.send_api_request(
        "HEAD",
        tax_zones_urls.TAX_ZONE,
        path_params={"tax_zone_id": tax_zone_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_tax_zone(
    client: Any,
    tax_zone_id: int | str,
    payload: TaxZonePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxZone]:
    """Update one tax zone — ``PUT /admin/tax_zones/{tax_zone_id}``. ``name`` is required, and an
    omitted ``countries``, ``states`` or ``post_code`` comes back empty, so send every list."""
    require_payload(payload)
    return client.send_put_request(
        tax_zones_urls.TAX_ZONE,
        path_params={"tax_zone_id": tax_zone_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxZone,
    )


def delete_tax_zone(
    client: Any,
    tax_zone_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one tax zone — ``DELETE /admin/tax_zones/{tax_zone_id}``; ``204``, no body."""
    return client.send_delete_request(
        tax_zones_urls.TAX_ZONE,
        path_params={"tax_zone_id": tax_zone_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
