"""Country tax endpoints, under ``/api/{api_version}/admin/tax/country-taxes``; no ``HEAD``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.tax_country_taxes import tax_country_taxes_urls
from webcommander.resources.tax_country_taxes.tax_country_taxes_dto import (
    CountryTax,
    CountryTaxPage,
)

__all__ = [
    "list_tax_country_taxes",
    "create_tax_country_tax",
    "get_tax_country_tax",
    "update_tax_country_tax",
    "delete_tax_country_tax",
]

CountryTaxPayload = Mapping[str, Any] | str | Dto


def list_tax_country_taxes(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CountryTaxPage]:
    """List the country taxes — ``GET /admin/tax/country-taxes``, newest first. ``limit`` is 1 to
    100 with the cap echoed, ``offset`` or ``page`` move the window, ``sort`` takes ``id`` or
    ``name``."""
    return client.send_get_request(
        tax_country_taxes_urls.TAX_COUNTRY_TAXES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CountryTaxPage,
    )


def create_tax_country_tax(
    client: Any,
    payload: CountryTaxPayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CountryTax]:
    """Create a country tax — ``POST /admin/tax/country-taxes``, answered ``201``. The body is
    wrapped in ``country_tax`` and needs ``country_code``, a field no read sends.
    ``transaction_no`` is sent as ``X-Transaction-No`` and files the row under that number."""
    require_payload(payload)
    return client.send_post_request(
        tax_country_taxes_urls.TAX_COUNTRY_TAXES,
        json_body=payload,
        headers=None
        if transaction_no is None
        else {tax_country_taxes_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CountryTax,
    )


def get_tax_country_tax(
    client: Any,
    country_tax_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CountryTax]:
    """Retrieve one country tax — ``GET /admin/tax/country-taxes/{country_tax_id}``, with an
    ``ETag``; only the row path and the update carry ``state_rules``."""
    return client.send_get_request(
        tax_country_taxes_urls.TAX_COUNTRY_TAX,
        path_params={"country_tax_id": country_tax_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CountryTax,
    )


def update_tax_country_tax(
    client: Any,
    country_tax_id: int | str,
    payload: CountryTaxPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CountryTax]:
    """Update one country tax — ``PUT /admin/tax/country-taxes/{country_tax_id}``; a merge,
    wrapped in ``country_tax``, answered ``200`` with an ``ETag``."""
    require_payload(payload)
    return client.send_put_request(
        tax_country_taxes_urls.TAX_COUNTRY_TAX,
        path_params={"country_tax_id": country_tax_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CountryTax,
    )


def delete_tax_country_tax(
    client: Any,
    country_tax_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one country tax — ``DELETE /admin/tax/country-taxes/{country_tax_id}``; ``204``."""
    return client.send_delete_request(
        tax_country_taxes_urls.TAX_COUNTRY_TAX,
        path_params={"country_tax_id": country_tax_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
