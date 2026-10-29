"""Tax settings — ``/api/{api_version}/admin/tax/settings``; flat, and no ``HEAD``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.tax_settings import tax_settings_urls
from webcommander.resources.tax_settings.tax_settings_dto import TaxSettings

__all__ = ["get_tax_settings", "put_tax_settings"]

TaxSettingsPayload = Mapping[str, Any] | str | Dto


def get_tax_settings(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxSettings]:
    """Read the tax settings — ``GET /admin/tax/settings``; nine keys under ``tax_settings``."""
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
    """Write the tax settings — ``PUT /admin/tax/settings``; a merge, wrapped in ``settings``, not
    the ``tax_settings`` the read answers under."""
    require_payload(payload)
    return client.send_put_request(
        tax_settings_urls.TAX_SETTINGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxSettings,
    )
