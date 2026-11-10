"""Shipping rate endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.shipping_rates import shipping_rates_urls
from webcommander.resources.shipping_rates.shipping_rates_dto import (
    ShippingRate,
    ShippingRateCount,
    ShippingRateListing,
)

__all__ = [
    "list_shipping_rates",
    "head_shipping_rates",
    "count_shipping_rates",
    "head_shipping_rates_count",
    "create_shipping_rate",
    "get_shipping_rate",
    "head_shipping_rate",
    "update_shipping_rate",
    "patch_shipping_rate",
    "delete_shipping_rate",
]

ShippingRatePayload = Mapping[str, Any] | str | Dto


def list_shipping_rates(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRateListing]:
    """List the rates, newest first — ``GET /admin/shipping_rates``. ``search`` (part of the
    name), ``method`` (such as ``flat_rate`` or ``ship_by_weight``) and ``handling_cost``
    (``with_handling`` or ``without_handling``) filter; ``sort`` is ``id``, ``name``, ``method``,
    ``created_at``, ``updated_at`` or ``transaction_no`` with ``order`` ``asc`` or ``desc``;
    ``limit`` is 1 to 100 and defaults to 20, ``offset`` pages. An unknown value is ``400``."""
    return client.send_get_request(
        shipping_rates_urls.SHIPPING_RATES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRateListing,
    )


def head_shipping_rates(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/shipping_rates``; no body."""
    return client.send_api_request(
        "HEAD",
        shipping_rates_urls.SHIPPING_RATES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def count_shipping_rates(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRateCount]:
    """How many rates match — ``GET /admin/shipping_rates/count``, a bare ``{"total": N}``. The
    listing's filters narrow it."""
    return client.send_get_request(
        shipping_rates_urls.SHIPPING_RATES_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRateCount,
    )


def head_shipping_rates_count(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the count is reachable — ``HEAD /admin/shipping_rates/count``; no body."""
    return client.send_api_request(
        "HEAD",
        shipping_rates_urls.SHIPPING_RATES_COUNT,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_shipping_rate(
    client: Any,
    payload: ShippingRatePayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRate]:
    """Create a rate — ``POST /admin/shipping_rates``, answered ``201`` with a ``Location``. The
    body is wrapped in ``shipping_rate`` and needs ``name``, unique without regard to case
    (``409``), and ``method``. A flat rate needs ``shipping_cost``; ``ship_by_price``,
    ``ship_by_quantity``, ``ship_by_weight`` and ``ship_by_variation`` take their costs per row in
    ``conditions`` and refuse a rate-level ``shipping_cost``. ``free_shipping`` always saves
    ``calculate_for_entire_order`` false. ``shipping_rule_id`` attaches the rate to a rule that
    has none (``409`` otherwise). An unknown field, an ``id`` or an unwrapped body is ``400``.
    ``transaction_no`` is sent as ``X-Transaction-No``."""
    require_payload(payload)
    return client.send_post_request(
        shipping_rates_urls.SHIPPING_RATES,
        json_body=payload,
        headers=None
        if transaction_no is None
        else {shipping_rates_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRate,
    )


def get_shipping_rate(
    client: Any,
    shipping_rate_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRate]:
    """Retrieve one rate by its ``id`` — ``GET /admin/shipping_rates/{shipping_rate_id}``, the row
    under ``shipping_rate``. An id that is not plain digits, or unknown, is ``404``."""
    return client.send_get_request(
        shipping_rates_urls.SHIPPING_RATE,
        path_params={"shipping_rate_id": shipping_rate_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRate,
    )


def head_shipping_rate(
    client: Any,
    shipping_rate_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether a rate exists — ``HEAD /admin/shipping_rates/{shipping_rate_id}``; 200 with no
    body, 404 for an unknown id."""
    return client.send_api_request(
        "HEAD",
        shipping_rates_urls.SHIPPING_RATE,
        path_params={"shipping_rate_id": shipping_rate_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_shipping_rate(
    client: Any,
    shipping_rate_id: int | str,
    payload: ShippingRatePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRate]:
    """Replace one rate — ``PUT /admin/shipping_rates/{shipping_rate_id}``. Every field is
    required: ``name``, ``method``, ``calculate_for_entire_order``, ``price_entered_with_tax``,
    the costs the method uses and ``additional_rule``; a ``handling_cost`` or ``additional_rule``
    the rate does not use is sent as ``None``. A field left out is ``400`` naming it."""
    require_payload(payload)
    return client.send_put_request(
        shipping_rates_urls.SHIPPING_RATE,
        path_params={"shipping_rate_id": shipping_rate_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRate,
    )


def patch_shipping_rate(
    client: Any,
    shipping_rate_id: int | str,
    payload: ShippingRatePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRate]:
    """Change only the fields sent — ``PATCH /admin/shipping_rates/{shipping_rate_id}``; the
    costs, rows and boxes not sent are kept. An empty ``shipping_rate`` changes nothing and is
    ``200``."""
    require_payload(payload)
    return client.send_patch_request(
        shipping_rates_urls.SHIPPING_RATE,
        path_params={"shipping_rate_id": shipping_rate_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRate,
    )


def delete_shipping_rate(
    client: Any,
    shipping_rate_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one rate — ``DELETE /admin/shipping_rates/{shipping_rate_id}``, ``204``. A rate a
    rule uses is ``409`` until the rule lets it go."""
    return client.send_delete_request(
        shipping_rates_urls.SHIPPING_RATE,
        path_params={"shipping_rate_id": shipping_rate_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
