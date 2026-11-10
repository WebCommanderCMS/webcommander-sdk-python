"""Tax settings — ``/api/{api_version}/admin/settings/tax``; flat, no sections."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.tax_settings import tax_settings_urls
from webcommander.resources.tax_settings.tax_settings_dto import TaxSettings

__all__ = ["get_tax_settings", "put_tax_settings", "patch_tax_settings", "head_tax_settings"]

TaxSettingsPayload = Mapping[str, Any] | str | Dto


def get_tax_settings(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxSettings]:
    """Read the tax settings — ``GET /admin/settings/tax``; nine keys under ``tax_settings``."""
    return client.send_get_request(
        tax_settings_urls.TAX_SETTINGS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxSettings,
    )


def put_tax_settings(
    client: Any,
    payload: TaxSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxSettings]:
    """Write the tax settings — ``PUT /admin/settings/tax``; a merge, wrapped in
    ``tax_settings``."""
    require_payload(payload)
    return client.send_put_request(
        tax_settings_urls.TAX_SETTINGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxSettings,
    )


def patch_tax_settings(
    client: Any,
    payload: TaxSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxSettings]:
    """Write one field or several — ``PATCH /admin/settings/tax``, wrapped in ``tax_settings``."""
    require_payload(payload)
    return client.send_patch_request(
        tax_settings_urls.TAX_SETTINGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxSettings,
    )


def head_tax_settings(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the tax settings are reachable — ``HEAD /admin/settings/tax``; no body."""
    return client.send_api_request(
        "HEAD",
        tax_settings_urls.TAX_SETTINGS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
