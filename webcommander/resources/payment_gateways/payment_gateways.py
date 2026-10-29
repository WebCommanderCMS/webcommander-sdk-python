"""Payment gateway endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.payment_gateways import payment_gateways_urls
from webcommander.resources.payment_gateways.payment_gateways_dto import (
    PaymentGateway,
    PaymentGatewayCount,
    PaymentGatewayPage,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_payment_gateways",
    "head_payment_gateways",
    "count_payment_gateways",
    "head_payment_gateways_count",
    "get_payment_gateway",
    "head_payment_gateway",
    "update_payment_gateway",
    "patch_payment_gateway",
]

PaymentGatewayPayload = Mapping[str, Any] | str | Dto


def list_payment_gateways(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PaymentGatewayPage]:
    """List the store's gateways by ascending ``id`` — ``GET /admin/payment_gateways``, rows
    without ``settings``. ``limit`` is 1 to 100, default 20; ``0`` or above 100 is ``400``
    ``out_of_range``. ``offset`` or ``page``; ``search`` a substring of the name; ``exclude`` a
    comma list of codes; ``promotional`` and ``added`` filter. Other names, ``sort`` included,
    are ignored."""
    return client.send_get_request(
        payment_gateways_urls.PAYMENT_GATEWAYS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PaymentGatewayPage,
    )


def head_payment_gateways(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/payment_gateways``; no body."""
    return client.send_api_request(
        "HEAD",
        payment_gateways_urls.PAYMENT_GATEWAYS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def count_payment_gateways(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PaymentGatewayCount]:
    """How many gateways match — ``GET /admin/payment_gateways/count``, a bare ``{"total": N}``.
    The listing's filters narrow it; ``limit`` is checked as on the listing, ``0`` or above 100
    ``400`` ``out_of_range``, but changes nothing."""
    return client.send_get_request(
        payment_gateways_urls.PAYMENT_GATEWAYS_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PaymentGatewayCount,
    )


def head_payment_gateways_count(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the count is reachable — ``HEAD /admin/payment_gateways/count``; no body."""
    return client.send_api_request(
        "HEAD",
        payment_gateways_urls.PAYMENT_GATEWAYS_COUNT,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_payment_gateway(
    client: Any,
    payment_gateway_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PaymentGateway]:
    """Retrieve one gateway with its ``settings``; secrets read ``********`` when set.
    ``GET /admin/payment_gateways/{payment_gateway_id}``"""
    return client.send_get_request(
        payment_gateways_urls.PAYMENT_GATEWAY,
        path_params={"payment_gateway_id": payment_gateway_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PaymentGateway,
    )


def head_payment_gateway(
    client: Any,
    payment_gateway_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one gateway is there; no body. ``HEAD /admin/payment_gateways/{payment_gateway_id}``"""
    return client.send_api_request(
        "HEAD",
        payment_gateways_urls.PAYMENT_GATEWAY,
        path_params={"payment_gateway_id": payment_gateway_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_payment_gateway(
    client: Any,
    payment_gateway_id: int | str,
    payload: PaymentGatewayPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PaymentGateway]:
    """Write one gateway — ``PUT /admin/payment_gateways/{payment_gateway_id}``. A bare record
    merged like the ``PATCH``: the fields left out keep their value."""
    require_payload(payload)
    return client.send_put_request(
        payment_gateways_urls.PAYMENT_GATEWAY,
        path_params={"payment_gateway_id": payment_gateway_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PaymentGateway,
    )


def patch_payment_gateway(
    client: Any,
    payment_gateway_id: int | str,
    payload: PaymentGatewayPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[PaymentGateway]:
    """Change only the fields sent — ``PATCH /admin/payment_gateways/{payment_gateway_id}``.
    A bare record; an empty body is ``400``."""
    require_payload(payload)
    return client.send_patch_request(
        payment_gateways_urls.PAYMENT_GATEWAY,
        path_params={"payment_gateway_id": payment_gateway_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=PaymentGateway,
    )
