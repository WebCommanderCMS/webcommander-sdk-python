"""Transaction-number endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.resources.transactions import transactions_urls
from webcommander.resources.transactions.transactions_dto import (
    Transaction,
    TransactionItemPage,
    TransactionPage,
)

__all__ = [
    "list_transactions",
    "head_transactions",
    "get_transaction",
    "head_transaction",
    "list_transaction_items",
    "head_transaction_items",
]


def list_transactions(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TransactionPage]:
    """List the numbers in ascending order — ``GET /admin/transactions``. ``limit`` (or ``max``)
    from 1, default 20, held to 200; ``offset``, ``page``; ``transaction_no`` matches
    exactly and case-sensitively. ``search``, ``q``, ``sort`` and ``order`` change nothing."""
    return client.send_get_request(
        transactions_urls.TRANSACTIONS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TransactionPage,
    )


def head_transactions(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/transactions``; no body."""
    return client.send_api_request(
        "HEAD",
        transactions_urls.TRANSACTIONS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_transaction(
    client: Any,
    transaction_no: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Transaction]:
    """Count the records one number tagged, by type — ``GET /admin/transactions/{transaction_no}``.
    Matched exactly and case-sensitively; a number holding ``/`` is refused by the server, ``400``
    HTML, as an encoded slash."""
    return client.send_get_request(
        transactions_urls.TRANSACTION,
        path_params={"transaction_no": transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Transaction,
    )


def head_transaction(
    client: Any,
    transaction_no: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one number has records — ``HEAD /admin/transactions/{transaction_no}``; no
    body."""
    return client.send_api_request(
        "HEAD",
        transactions_urls.TRANSACTION,
        path_params={"transaction_no": transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def list_transaction_items(
    client: Any,
    transaction_no: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TransactionItemPage]:
    """List the records a number tagged, newest first —
    ``GET /admin/transactions/{transaction_no}/items``. ``type`` is optional: left out, every
    type is listed; sent, it takes one or more of the 15 ``by_type`` names, comma-separated.
    ``limit`` (or ``max``) 1 to 200, ``offset``, ``page``, ``detail`` ``slim`` or ``full``. A
    ``slim`` item is ``type``, ``id``, ``stamp``, ``trashed`` and the fields of its type, such as
    ``name``, ``sku`` and ``url`` for a product. A number or a type with no records answers
    ``200`` with ``items`` empty and ``total`` ``0``, not ``404``."""
    return client.send_get_request(
        transactions_urls.TRANSACTION_ITEMS,
        path_params={"transaction_no": transaction_no},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TransactionItemPage,
    )


def head_transaction_items(
    client: Any,
    transaction_no: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the records under a number are reachable; no body. ``type`` is optional here
    too. ``HEAD /admin/transactions/{transaction_no}/items``"""
    return client.send_api_request(
        "HEAD",
        transactions_urls.TRANSACTION_ITEMS,
        path_params={"transaction_no": transaction_no},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
