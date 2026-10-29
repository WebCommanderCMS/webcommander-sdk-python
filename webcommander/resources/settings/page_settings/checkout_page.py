"""Checkout page settings endpoints — a facade over six sections, under
``/api/{api_version}/admin/settings/page_settings/checkout_page``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.page_settings import checkout_page_urls
from webcommander.resources.settings.page_settings.checkout_page_dto import CheckoutPage

__all__ = [
    "get_checkout_page",
    "patch_checkout_page",
    "head_checkout_page",
    "get_checkout_page_section",
    "patch_checkout_page_section",
]

CheckoutPagePayload = Mapping[str, Any] | str | Dto


def get_checkout_page(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CheckoutPage]:
    """Read the whole area — ``GET /admin/settings/page_settings/checkout_page``.
    The two address sections arrive as their active field keys alone."""
    return client.send_get_request(
        checkout_page_urls.CHECKOUT_PAGE,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CheckoutPage,
    )


def patch_checkout_page(
    client: Any,
    payload: CheckoutPagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CheckoutPage]:
    """Write fields in one or more sections, wrapped in ``checkout_page``.
    ``PATCH /admin/settings/page_settings/checkout_page``"""
    require_payload(payload)
    return client.send_patch_request(
        checkout_page_urls.CHECKOUT_PAGE,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CheckoutPage,
    )


def head_checkout_page(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/page_settings/checkout_page``."""
    return client.send_api_request(
        "HEAD",
        checkout_page_urls.CHECKOUT_PAGE,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_checkout_page_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CheckoutPage]:
    """Read one section — ``GET /admin/settings/page_settings/checkout_page/{section}``.
    ``.data`` is under the section's own key, with no ``group_meta``."""
    return client.send_get_request(
        checkout_page_urls.CHECKOUT_PAGE_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CheckoutPage,
    )


def patch_checkout_page_section(
    client: Any,
    section: str,
    payload: CheckoutPagePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CheckoutPage]:
    """Write fields in one of the four writable sections, wrapped in the section's own key.
    ``PATCH /admin/settings/page_settings/checkout_page/{section}``"""
    require_payload(payload)
    return client.send_patch_request(
        checkout_page_urls.CHECKOUT_PAGE_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CheckoutPage,
    )
