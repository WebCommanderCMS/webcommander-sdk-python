"""Order custom field endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.order_custom_fields import order_custom_fields_urls
from webcommander.resources.order_custom_fields.order_custom_fields_dto import (
    OrderCustomField,
    OrderCustomFieldPage,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_order_custom_fields",
    "count_order_custom_fields",
    "get_order_custom_field",
    "validate_order_custom_field_timeslot",
]

OrderCustomFieldTimeslotPayload = Mapping[str, Any] | str | Dto


def list_order_custom_fields(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderCustomFieldPage]:
    """List the fields — ``GET /admin/order_custom_fields``. ``limit`` caps at 20; ``sort`` takes
    ``id``, ``label``, ``name``, ``type``, ``orderNo``, ``isActive``, ``created`` or ``updated``."""
    return client.send_get_request(
        order_custom_fields_urls.ORDER_CUSTOM_FIELDS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderCustomFieldPage,
    )


def count_order_custom_fields(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """How many fields the store holds — ``GET /admin/order_custom_fields/count``.
    ``.map`` is ``{"count": N}``; ``filterBy`` narrows it as it narrows the listing."""
    return client.send_get_request(
        order_custom_fields_urls.ORDER_CUSTOM_FIELDS_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_order_custom_field(
    client: Any,
    order_custom_field_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderCustomField]:
    """Retrieve one field, with nine fields its listing row leaves out; ``field_metadata`` adds
    the schema beside it. ``GET /admin/order_custom_fields/{order_custom_field_id}``"""
    return client.send_get_request(
        order_custom_fields_urls.ORDER_CUSTOM_FIELD,
        path_params={"order_custom_field_id": order_custom_field_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderCustomField,
    )


def validate_order_custom_field_timeslot(
    client: Any,
    order_custom_field_id: int | str,
    payload: OrderCustomFieldTimeslotPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Check a timeslot against an order limit; ``201 {"valid", "message"}``, and nothing stored.
    ``POST /admin/order_custom_fields/{order_custom_field_id}/validate_timeslot``"""
    require_payload(payload)
    return client.send_post_request(
        order_custom_fields_urls.ORDER_CUSTOM_FIELD_VALIDATE_TIMESLOT,
        path_params={"order_custom_field_id": order_custom_field_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
