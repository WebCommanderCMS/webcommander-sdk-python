"""Order flag endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.order_flags import order_flags_urls
from webcommander.resources.order_flags.order_flags_dto import OrderFlag, OrderFlagPage
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_order_flags",
    "head_order_flags",
    "create_order_flag",
    "get_order_flag",
    "head_order_flag",
    "update_order_flag",
    "delete_order_flag",
]

OrderFlagPayload = Mapping[str, Any] | str | Dto


def list_order_flags(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderFlagPage]:
    """List the flags — ``GET /admin/order_flags``. ``limit`` is a ceiling of 20, and an unknown
    query parameter is ``400``; the response carries an ``ETag``."""
    return client.send_get_request(
        order_flags_urls.ORDER_FLAGS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderFlagPage,
    )


def head_order_flags(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/order_flags``; no ``ETag``."""
    return client.send_api_request(
        "HEAD",
        order_flags_urls.ORDER_FLAGS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_order_flag(
    client: Any,
    payload: OrderFlagPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderFlag]:
    """Create a flag — ``POST /admin/order_flags``, wrapped in ``order_flag``; ``name`` and a hex
    ``color`` are required, and a name another flag holds is ``409``."""
    require_payload(payload)
    return client.send_post_request(
        order_flags_urls.ORDER_FLAGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderFlag,
    )


def get_order_flag(
    client: Any,
    order_flag_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderFlag]:
    """Retrieve one flag — ``GET /admin/order_flags/{order_flag_id}``."""
    return client.send_get_request(
        order_flags_urls.ORDER_FLAG,
        path_params={"order_flag_id": order_flag_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderFlag,
    )


def head_order_flag(
    client: Any,
    order_flag_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one flag is there — ``HEAD /admin/order_flags/{order_flag_id}``; no body."""
    return client.send_api_request(
        "HEAD",
        order_flags_urls.ORDER_FLAG,
        path_params={"order_flag_id": order_flag_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_order_flag(
    client: Any,
    order_flag_id: int | str,
    payload: OrderFlagPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[OrderFlag]:
    """Replace one flag — ``PUT /admin/order_flags/{order_flag_id}``; ``PATCH`` is ``405``.
    A replace, not a merge: an omitted ``description`` comes back ``null``, so send every field."""
    require_payload(payload)
    return client.send_put_request(
        order_flags_urls.ORDER_FLAG,
        path_params={"order_flag_id": order_flag_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=OrderFlag,
    )


def delete_order_flag(
    client: Any,
    order_flag_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete a flag — ``DELETE /admin/order_flags/{order_flag_id}``; ``204``, and hard."""
    return client.send_delete_request(
        order_flags_urls.ORDER_FLAG,
        path_params={"order_flag_id": order_flag_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
