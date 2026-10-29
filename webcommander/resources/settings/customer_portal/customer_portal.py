"""Customer portal endpoints, under ``/api/{api_version}/admin/settings/customer_portal``.
The area is a facade over six sections; a section is a path value."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.customer_portal import customer_portal_urls
from webcommander.resources.settings.customer_portal.customer_portal_dto import CustomerPortal

__all__ = [
    "get_customer_portal",
    "patch_customer_portal",
    "head_customer_portal",
    "get_customer_portal_section",
    "patch_customer_portal_section",
]

CustomerPortalPayload = Mapping[str, Any] | str | Dto


def get_customer_portal(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerPortal]:
    """Read the whole area — ``GET /admin/settings/customer_portal``, every section inlined."""
    return client.send_get_request(
        customer_portal_urls.CUSTOMER_PORTAL,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerPortal,
    )


def patch_customer_portal(
    client: Any,
    payload: CustomerPortalPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerPortal]:
    """Write fields in one or more sections — ``PATCH /admin/settings/customer_portal``.
    The body must be wrapped in ``customer_portal``, and name only writable sections."""
    require_payload(payload)
    return client.send_patch_request(
        customer_portal_urls.CUSTOMER_PORTAL,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerPortal,
    )


def head_customer_portal(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/customer_portal``; no body."""
    return client.send_api_request(
        "HEAD",
        customer_portal_urls.CUSTOMER_PORTAL,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_customer_portal_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerPortal]:
    """Read one section — ``GET /admin/settings/customer_portal/{section}``.
    ``.data`` is under the section's own key, with no ``group_meta``."""
    return client.send_get_request(
        customer_portal_urls.CUSTOMER_PORTAL_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerPortal,
    )


def patch_customer_portal_section(
    client: Any,
    section: str,
    payload: CustomerPortalPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomerPortal]:
    """Write fields in one section — ``PATCH /admin/settings/customer_portal/{section}``.
    Name only a writable section: ``group_meta``, not the ``Allow`` header, decides which."""
    require_payload(payload)
    return client.send_patch_request(
        customer_portal_urls.CUSTOMER_PORTAL_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomerPortal,
    )
