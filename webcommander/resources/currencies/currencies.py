"""Currency endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.currencies import currencies_urls
from webcommander.resources.currencies.currencies_dto import (
    Currency,
    CurrencyBaseChange,
    CurrencyCount,
    CurrencyPage,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_currencies",
    "head_currencies",
    "count_currencies",
    "head_currencies_count",
    "create_currency",
    "get_currency",
    "head_currency",
    "update_currency",
    "patch_currency",
    "delete_currency",
    "set_base_currency",
]

CurrencyPayload = Mapping[str, Any] | str | Dto


def list_currencies(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CurrencyPage]:
    """List the currencies by ascending ``id`` — ``GET /admin/currencies``. ``search`` matches
    ``name`` or ``code``, ``active`` filters, ``sort`` and ``dir`` order, ``limit`` is 1 to 100."""
    return client.send_get_request(
        currencies_urls.CURRENCIES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CurrencyPage,
    )


def head_currencies(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/currencies``; no body."""
    return client.send_api_request(
        "HEAD",
        currencies_urls.CURRENCIES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def count_currencies(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CurrencyCount]:
    """How many currencies match — ``GET /admin/currencies/count``, a bare ``{"total": N}``.
    ``search`` and ``active`` narrow it as they narrow the listing; ``limit`` is ignored."""
    return client.send_get_request(
        currencies_urls.CURRENCIES_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CurrencyCount,
    )


def head_currencies_count(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the count is reachable — ``HEAD /admin/currencies/count``; no body."""
    return client.send_api_request(
        "HEAD",
        currencies_urls.CURRENCIES_COUNT,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_currency(
    client: Any,
    payload: CurrencyPayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Currency]:
    """Create a currency — ``POST /admin/currencies``, answered ``201``. A bare record: ``name``,
    ``code`` and ``symbol`` are required, and ``name`` and ``code`` must be free.
    ``transaction_no`` is sent as ``X-Transaction-No`` and files the currency under that number."""
    require_payload(payload)
    return client.send_post_request(
        currencies_urls.CURRENCIES,
        json_body=payload,
        headers=None
        if transaction_no is None
        else {currencies_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Currency,
    )


def get_currency(
    client: Any,
    currency_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Currency]:
    """Retrieve one currency, with an ``ETag``; ``field_metadata`` adds the schema beside it.
    ``GET /admin/currencies/{currency_id}``"""
    return client.send_get_request(
        currencies_urls.CURRENCY,
        path_params={"currency_id": currency_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Currency,
    )


def head_currency(
    client: Any,
    currency_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one currency is there; no body, the ``ETag`` its ``GET`` carries.
    ``HEAD /admin/currencies/{currency_id}``"""
    return client.send_api_request(
        "HEAD",
        currencies_urls.CURRENCY,
        path_params={"currency_id": currency_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_currency(
    client: Any,
    currency_id: int | str,
    payload: CurrencyPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Currency]:
    """Replace one currency — ``PUT /admin/currencies/{currency_id}``. ``name``, ``code`` and
    ``symbol`` are required and every field left out is reset to its default; not the base."""
    require_payload(payload)
    return client.send_put_request(
        currencies_urls.CURRENCY,
        path_params={"currency_id": currency_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Currency,
    )


def patch_currency(
    client: Any,
    currency_id: int | str,
    payload: CurrencyPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Currency]:
    """Change only the fields sent — ``PATCH /admin/currencies/{currency_id}``. An empty body is
    ``400``, and the base currency is read-only here as on ``PUT``."""
    require_payload(payload)
    return client.send_patch_request(
        currencies_urls.CURRENCY,
        path_params={"currency_id": currency_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Currency,
    )


def delete_currency(
    client: Any,
    currency_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete a currency — ``DELETE /admin/currencies/{currency_id}``; ``204``. The base
    currency is ``409``: make another currency the base first."""
    return client.send_delete_request(
        currencies_urls.CURRENCY,
        path_params={"currency_id": currency_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def set_base_currency(
    client: Any,
    currency_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CurrencyBaseChange]:
    """Make an active currency the store's base; takes no body. Every rate is divided by the new
    base's old rate. ``PUT /admin/currencies/{currency_id}/base``"""
    return client.send_put_request(
        currencies_urls.CURRENCY_BASE,
        path_params={"currency_id": currency_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CurrencyBaseChange,
    )
