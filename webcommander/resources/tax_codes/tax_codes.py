"""Tax code endpoints, under ``/api/{api_version}/admin/tax_codes``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.tax_codes import tax_codes_urls
from webcommander.resources.tax_codes.tax_codes_dto import TaxCode, TaxCodePage

__all__ = [
    "list_tax_codes",
    "head_tax_codes",
    "create_tax_code",
    "get_tax_code",
    "head_tax_code",
    "update_tax_code",
    "delete_tax_code",
]

TaxCodePayload = Mapping[str, Any] | str | Dto


def list_tax_codes(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxCodePage]:
    """List the tax codes — ``GET /admin/tax_codes``. ``limit`` is capped at 100."""
    return client.send_get_request(
        tax_codes_urls.TAX_CODES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxCodePage,
    )


def head_tax_codes(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/tax_codes``; no body."""
    return client.send_api_request(
        "HEAD",
        tax_codes_urls.TAX_CODES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_tax_code(
    client: Any,
    payload: TaxCodePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxCode]:
    """Create a tax code — ``POST /admin/tax_codes``, answered ``201``. The body is wrapped in
    ``tax_code``; ``name`` is required, and ``default`` is not writable."""
    require_payload(payload)
    return client.send_post_request(
        tax_codes_urls.TAX_CODES,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxCode,
    )


def get_tax_code(
    client: Any,
    tax_code_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxCode]:
    """Retrieve one tax code — ``GET /admin/tax_codes/{tax_code_id}``."""
    return client.send_get_request(
        tax_codes_urls.TAX_CODE,
        path_params={"tax_code_id": tax_code_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxCode,
    )


def head_tax_code(
    client: Any,
    tax_code_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one tax code is there — ``HEAD /admin/tax_codes/{tax_code_id}``; no body.
    An id no row holds is ``200`` too; use :func:`get_tax_code` to learn whether it exists."""
    return client.send_api_request(
        "HEAD",
        tax_codes_urls.TAX_CODE,
        path_params={"tax_code_id": tax_code_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_tax_code(
    client: Any,
    tax_code_id: int | str,
    payload: TaxCodePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxCode]:
    """Update one tax code — ``PUT /admin/tax_codes/{tax_code_id}``, wrapped in ``tax_code``.
    ``priority`` and ``resolver_type`` omitted reset to ``0`` and ``flat``, so send both."""
    require_payload(payload)
    return client.send_put_request(
        tax_codes_urls.TAX_CODE,
        path_params={"tax_code_id": tax_code_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxCode,
    )


def delete_tax_code(
    client: Any,
    tax_code_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one tax code — ``DELETE /admin/tax_codes/{tax_code_id}``; ``204``, no body."""
    return client.send_delete_request(
        tax_codes_urls.TAX_CODE,
        path_params={"tax_code_id": tax_code_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
