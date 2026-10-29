"""Admin customer endpoints; every path below sits under ``/api/{api_version}``."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.errors import SdkUsageError
from webcommander.resources.customers import admin_customers_urls
from webcommander.resources.customers.admin_customers_dto import (
    Customer,
    Page,
    StoreCreditAdjustment,
)
from webcommander.resources.required_bodies import require_files, require_payload

__all__ = [
    "get_customers",
    "get_customer",
    "get_customer_count",
    "get_customer_email_exists",
    "get_customer_export",
    "create_customer",
    "update_customer",
    "delete_customer",
    "create_customer_addresses",
    "reset_customer_password",
    "change_customer_password",
    "bulk_reset_customer_passwords",
    "import_customers",
    "get_customer_store_credit_adjustments",
    "create_customer_store_credit_adjustment",
]

#: A body as the API's own mapping, as JSON text, or as an ``admin_customers_dto`` type.
CustomerPayload = Mapping[str, Any] | str | Dto


def get_customers(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page[Customer]]:
    """List customers — ``GET /admin/customers``; ``limit`` caps at 20."""
    return client.send_get_request(
        admin_customers_urls.ADMIN_CUSTOMERS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page.of(Customer),
    )


def get_customer(
    client: Any,
    customer_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Customer]:
    """Retrieve one customer — ``GET /admin/customers/{customer_id}``. Pass ``customer_id``,
    not ``internal_id``: the other id space answers 404, or someone else's customer."""
    return client.send_get_request(
        admin_customers_urls.ADMIN_CUSTOMER,
        path_params={"customer_id": customer_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Customer,
    )


def get_customer_count(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Count customers — ``GET /admin/customers/count``; ``.data`` is ``{"total": n}`` alone.
    ``email`` is a case-insensitive substring match; no other filter narrows it."""
    return client.send_get_request(
        admin_customers_urls.ADMIN_CUSTOMERS_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_customer_email_exists(
    client: Any,
    email: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Check an email — ``GET /admin/customers/check-email``. Read ``exists`` first: both ids
    are absent when free, and a trashed record still reports ``exists: true``."""
    _require_email(email)
    return client.send_get_request(
        admin_customers_urls.ADMIN_CUSTOMERS_CHECK_EMAIL,
        query_params={"email": email},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_customer_export(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Export every customer — ``GET /admin/customers/export``; ``.data`` is XLSX bytes. It never
    filters rows: a :func:`get_customers` filter sharing a column name drops that column."""
    return client.send_get_request(
        admin_customers_urls.ADMIN_CUSTOMERS_EXPORT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_customer(
    client: Any,
    payload: CustomerPayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Customer]:
    """Create a customer — ``POST /admin/customers``; keep the ``customer_id`` it answers.
    An email already registered is ``409``, a trashed record's included. ``transaction_no`` is
    sent as ``X-Transaction-No`` and files the customer under that number."""
    require_payload(payload)
    return client.send_post_request(
        admin_customers_urls.ADMIN_CUSTOMERS,
        json_body=payload,
        headers=None
        if transaction_no is None
        else {admin_customers_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Customer,
    )


def update_customer(
    client: Any,
    customer_id: int | str,
    payload: CustomerPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Customer]:
    """Update a customer — ``PUT /admin/customers/{customer_id}``, with a create's payload."""
    require_payload(payload)
    return client.send_put_request(
        admin_customers_urls.ADMIN_CUSTOMER,
        path_params={"customer_id": customer_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Customer,
    )


def delete_customer(
    client: Any,
    customer_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete a customer — ``DELETE /admin/customers/{customer_id}``; answers 204, no body.
    Soft: the record still reads with ``is_in_trash`` true, a second delete is ``404``."""
    return client.send_delete_request(
        admin_customers_urls.ADMIN_CUSTOMER,
        path_params={"customer_id": customer_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_customer_addresses(
    client: Any,
    customer_id: int | str,
    payload: CustomerPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Customer]:
    """Add addresses — ``POST /admin/customers/{customer_id}/addresses``, as
    ``{"customer": {"addresses": [...]}}``, each typed PRIMARY, SHIPPING or BILLING."""
    require_payload(payload)
    return client.send_post_request(
        admin_customers_urls.ADMIN_CUSTOMER_ADDRESSES,
        path_params={"customer_id": customer_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Customer,
    )


def reset_customer_password(
    client: Any,
    customer_id: int | str,
    payload: CustomerPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Set a password directly — ``POST /admin/customers/{customer_id}/reset-password``."""
    require_payload(payload)
    return client.send_post_request(
        admin_customers_urls.ADMIN_CUSTOMER_RESET_PASSWORD,
        path_params={"customer_id": customer_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def change_customer_password(
    client: Any,
    customer_id: int | str,
    payload: CustomerPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Change a password — ``POST /admin/customers/{customer_id}/change-password``. Needs ``email``,
    ``old_password`` and ``password``; a missing one is ``401``, not a validation failure."""
    require_payload(payload)
    return client.send_post_request(
        admin_customers_urls.ADMIN_CUSTOMER_CHANGE_PASSWORD,
        path_params={"customer_id": customer_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def bulk_reset_customer_passwords(
    client: Any,
    payload: CustomerPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Queue a reset for many customers — ``POST /admin/customers/bulk-reset-password``. The
    body is ``{"customer_ids": [...]}``; ``.data["skipped"]`` holds objects, not bare ids."""
    require_payload(payload)
    return client.send_post_request(
        admin_customers_urls.ADMIN_CUSTOMERS_BULK_RESET_PASSWORD,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def import_customers(
    client: Any,
    files: Mapping[str, Any] | Sequence[tuple[str, Any]],
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Upload customers — ``POST /admin/customers/import``; the part is ``file``, and a ``str`` is
    contents, not a path. A partly rejected upload still answers ``201``: read ``failed``."""
    require_files(files, "validation_failed")
    return client.send_post_request(
        admin_customers_urls.ADMIN_CUSTOMERS_IMPORT,
        files=files,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_customer_store_credit_adjustments(
    client: Any,
    customer_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page[StoreCreditAdjustment]]:
    """Store-credit history — ``GET /admin/customers/{customer_id}/store-credit/adjustments``.
    Newest first; ``limit`` is a ceiling of 20 and any other filter is accepted but ignored."""
    return client.send_get_request(
        admin_customers_urls.ADMIN_CUSTOMER_STORE_CREDIT_ADJUSTMENTS,
        path_params={"customer_id": customer_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page.of(StoreCreditAdjustment),
    )


def create_customer_store_credit_adjustment(
    client: Any,
    customer_id: int | str,
    payload: CustomerPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[StoreCreditAdjustment]:
    """Adjust store credit — ``POST /admin/customers/{customer_id}/store-credit/adjustments``.
    No envelope: the body is the record, such as ``{"action": "add", "amount": 25.0}``."""
    require_payload(payload)
    return client.send_post_request(
        admin_customers_urls.ADMIN_CUSTOMER_STORE_CREDIT_ADJUSTMENTS,
        path_params={"customer_id": customer_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=StoreCreditAdjustment,
    )


def _require_email(email: Any) -> None:
    if email is None or (isinstance(email, str) and not email.strip()):
        raise SdkUsageError(
            "email is required and identifies the lookup, so a None or blank "
            "one is refused here rather than sent as a different question"
        )
