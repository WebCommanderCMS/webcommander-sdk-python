"""Shipping profile endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.shipping_profiles import shipping_profiles_urls
from webcommander.resources.shipping_profiles.shipping_profiles_dto import (
    ShippingProfile,
    ShippingProfileCount,
    ShippingProfileListing,
)

__all__ = [
    "list_shipping_profiles",
    "head_shipping_profiles",
    "count_shipping_profiles",
    "head_shipping_profiles_count",
    "create_shipping_profile",
    "create_shipping_profile_wizard",
    "get_shipping_profile",
    "head_shipping_profile",
    "update_shipping_profile",
    "patch_shipping_profile",
    "delete_shipping_profile",
]

ShippingProfilePayload = Mapping[str, Any] | str | Dto


def list_shipping_profiles(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingProfileListing]:
    """List the profiles, newest first — ``GET /admin/shipping_profiles``. ``search`` (part of the
    name) and ``default`` (``true`` or ``false``) filter; ``sort`` is ``id``, ``name``,
    ``description``, ``rule_preference``, ``created_at``, ``updated_at`` or ``transaction_no`` with
    ``order`` ``asc`` or ``desc``; ``limit`` is 1 to 100 and defaults to 20, ``offset`` pages. An
    unknown value is ``400``; an unknown name is ignored."""
    return client.send_get_request(
        shipping_profiles_urls.SHIPPING_PROFILES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingProfileListing,
    )


def head_shipping_profiles(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/shipping_profiles``; no body."""
    return client.send_api_request(
        "HEAD",
        shipping_profiles_urls.SHIPPING_PROFILES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def count_shipping_profiles(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingProfileCount]:
    """How many profiles match — ``GET /admin/shipping_profiles/count``, a bare ``{"total": N}``.
    ``search`` and ``default`` narrow it."""
    return client.send_get_request(
        shipping_profiles_urls.SHIPPING_PROFILES_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingProfileCount,
    )


def head_shipping_profiles_count(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the count is reachable — ``HEAD /admin/shipping_profiles/count``; no body."""
    return client.send_api_request(
        "HEAD",
        shipping_profiles_urls.SHIPPING_PROFILES_COUNT,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_shipping_profile(
    client: Any,
    payload: ShippingProfilePayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingProfile]:
    """Create a profile — ``POST /admin/shipping_profiles``, answered ``201`` with a ``Location``.
    The body is wrapped in ``shipping_profile`` and needs ``name``, unique without regard to case
    (``409``); ``rule_preference`` defaults to ``product_assigned_rule``. An unknown field, an
    ``id`` or an unwrapped body is ``400``. ``transaction_no`` is sent as ``X-Transaction-No``."""
    require_payload(payload)
    return client.send_post_request(
        shipping_profiles_urls.SHIPPING_PROFILES,
        json_body=payload,
        headers=None
        if transaction_no is None
        else {shipping_profiles_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingProfile,
    )


def create_shipping_profile_wizard(
    client: Any,
    payload: ShippingProfilePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingProfile]:
    """Create a profile with its rules and their rates in one call —
    ``POST /admin/shipping_profiles/wizard``. A new profile name is ``201``; a name that exists
    adds the rules to that profile and is ``200``. Every rule's rate, class and zone is checked
    first, and one bad value saves nothing. A zone given as ``{"name": ...}`` is created."""
    require_payload(payload)
    return client.send_post_request(
        shipping_profiles_urls.SHIPPING_PROFILES_WIZARD,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingProfile,
    )


def get_shipping_profile(
    client: Any,
    shipping_profile_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingProfile]:
    """Retrieve one profile by its ``id`` — ``GET /admin/shipping_profiles/{shipping_profile_id}``,
    the row under ``shipping_profile``. An id that is not plain digits, or unknown, is ``404``."""
    return client.send_get_request(
        shipping_profiles_urls.SHIPPING_PROFILE,
        path_params={"shipping_profile_id": shipping_profile_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingProfile,
    )


def head_shipping_profile(
    client: Any,
    shipping_profile_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether a profile exists — ``HEAD /admin/shipping_profiles/{shipping_profile_id}``;
    200 with no body, 404 for an unknown id."""
    return client.send_api_request(
        "HEAD",
        shipping_profiles_urls.SHIPPING_PROFILE,
        path_params={"shipping_profile_id": shipping_profile_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_shipping_profile(
    client: Any,
    shipping_profile_id: int | str,
    payload: ShippingProfilePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingProfile]:
    """Replace one profile — ``PUT /admin/shipping_profiles/{shipping_profile_id}``. ``name``,
    ``description``, ``rule_preference`` and ``shipping_rules`` are all required (``description``
    may be ``None``); the rules not listed are taken off the profile and kept."""
    require_payload(payload)
    return client.send_put_request(
        shipping_profiles_urls.SHIPPING_PROFILE,
        path_params={"shipping_profile_id": shipping_profile_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingProfile,
    )


def patch_shipping_profile(
    client: Any,
    shipping_profile_id: int | str,
    payload: ShippingProfilePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingProfile]:
    """Change only the fields sent — ``PATCH /admin/shipping_profiles/{shipping_profile_id}``.
    ``shipping_rules`` is the full list, so ``[]`` takes every rule off. ``default`` true moves
    the store default to this profile; the default cannot be switched off directly (``409``)."""
    require_payload(payload)
    return client.send_patch_request(
        shipping_profiles_urls.SHIPPING_PROFILE,
        path_params={"shipping_profile_id": shipping_profile_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingProfile,
    )


def delete_shipping_profile(
    client: Any,
    shipping_profile_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one profile — ``DELETE /admin/shipping_profiles/{shipping_profile_id}``, ``204``.
    Its rules and zones stay. The store default is ``409`` until another profile holds the flag."""
    return client.send_delete_request(
        shipping_profiles_urls.SHIPPING_PROFILE,
        path_params={"shipping_profile_id": shipping_profile_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
