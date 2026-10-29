"""Customer group endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.customer_groups import customer_groups_urls
from webcommander.resources.customer_groups.customer_groups_dto import (
    CustomerGroup,
    CustomerGroupAssignment,
    CustomerGroupCount,
    CustomerGroupMember,
    CustomerGroupPage,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_customer_groups",
    "count_customer_groups",
    "create_customer_group",
    "get_customer_group",
    "patch_customer_group",
    "delete_customer_group",
    "update_customer_group_customers",
    "get_customer_group_customer",
    "assign_customer_group",
]

CustomerGroupPayload = Mapping[str, Any] | str | Dto


def list_customer_groups(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerGroupPage]:
    """List the groups, by ``name`` — ``GET /admin/customer_groups``. ``limit`` 1 to 100, default
    20; ``search_text`` or ``name`` match a name, ``status`` takes ``A``, ``I`` or their words."""
    return client.send_get_request(
        customer_groups_urls.CUSTOMER_GROUPS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerGroupPage,
    )


def count_customer_groups(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerGroupCount]:
    """How many groups match — ``GET /admin/customer_groups/count``; ``{"total": N}``, narrowed
    by the listing's ``search_text``, ``name`` and ``status`` and not by its paging."""
    return client.send_get_request(
        customer_groups_urls.CUSTOMER_GROUPS_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerGroupCount,
    )


def create_customer_group(
    client: Any,
    payload: CustomerGroupPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerGroup]:
    """Create a group — ``POST /admin/customer_groups``, answered ``201``. The body is
    ``{"customer_group": {...}}`` with ``name`` required, unique in any letter case."""
    require_payload(payload)
    return client.send_post_request(
        customer_groups_urls.CUSTOMER_GROUPS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerGroup,
    )


def get_customer_group(
    client: Any,
    customer_group_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerGroup]:
    """Retrieve one group with ``customer_count`` and its ``customers``; ``field_metadata=true``
    adds the schema. ``GET /admin/customer_groups/{customer_group_id}``"""
    return client.send_get_request(
        customer_groups_urls.CUSTOMER_GROUP,
        path_params={"customer_group_id": customer_group_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerGroup,
    )


def patch_customer_group(
    client: Any,
    customer_group_id: int | str,
    payload: CustomerGroupPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerGroup]:
    """Change only the fields sent, nested ones included, in the ``customer_group`` wrapper; ``PUT``
    is ``405``. ``PATCH /admin/customer_groups/{customer_group_id}``"""
    require_payload(payload)
    return client.send_patch_request(
        customer_groups_urls.CUSTOMER_GROUP,
        path_params={"customer_group_id": customer_group_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerGroup,
    )


def delete_customer_group(
    client: Any,
    customer_group_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one group and its memberships — ``DELETE /admin/customer_groups/{customer_group_id}``;
    ``204``, and the members stay as customers."""
    return client.send_delete_request(
        customer_groups_urls.CUSTOMER_GROUP,
        path_params={"customer_group_id": customer_group_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_customer_group_customers(
    client: Any,
    customer_group_id: int | str,
    payload: CustomerGroupPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerGroup]:
    """Replace the member list with ``{"customers": [customer_id, ...]}``; ``[]`` empties it.
    ``PATCH /admin/customer_groups/{customer_group_id}/customers``"""
    require_payload(payload)
    return client.send_patch_request(
        customer_groups_urls.CUSTOMER_GROUP_CUSTOMERS,
        path_params={"customer_group_id": customer_group_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerGroup,
    )


def get_customer_group_customer(
    client: Any,
    customer_group_id: int | str,
    customer_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerGroupMember]:
    """Read one member by its ``customer_id``; a customer outside the group is ``404``.
    ``GET /admin/customer_groups/{customer_group_id}/customers/{customer_id}``"""
    return client.send_get_request(
        customer_groups_urls.CUSTOMER_GROUP_CUSTOMER,
        path_params={"customer_group_id": customer_group_id, "customer_id": customer_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerGroupMember,
    )


def assign_customer_group(
    client: Any,
    payload: CustomerGroupPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerGroupAssignment]:
    """Add one customer to one group, keeping the other members — ``POST
    /admin/customer_groups/assign``; ``201`` with ``added`` ``false`` for an existing member."""
    require_payload(payload)
    return client.send_post_request(
        customer_groups_urls.CUSTOMER_GROUPS_ASSIGN,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerGroupAssignment,
    )
