"""Discount profile endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.discount_profiles import discount_profiles_urls
from webcommander.resources.discount_profiles.discount_profiles_dto import (
    DiscountProfile,
    DiscountProfileCoupons,
    DiscountProfilePage,
)
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_discount_profiles",
    "create_discount_profile",
    "get_discount_profile",
    "update_discount_profile",
    "delete_discount_profile",
    "create_discount_profile_coupons",
    "assign_discount_coupon_customer",
]

DiscountProfilePayload = Mapping[str, Any] | str | Dto


def list_discount_profiles(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DiscountProfilePage]:
    """List the profiles, newest ``id`` first — ``GET /admin/discount_profiles``. ``limit`` is
    capped at 20."""
    return client.send_get_request(
        discount_profiles_urls.DISCOUNT_PROFILES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DiscountProfilePage,
    )


def create_discount_profile(
    client: Any,
    payload: DiscountProfilePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DiscountProfile]:
    """Create a profile — ``POST /admin/discount_profiles``, answered ``201``. The body is a bare
    record: ``name``, ``discount_details_type`` and the details block it names are required."""
    require_payload(payload)
    return client.send_post_request(
        discount_profiles_urls.DISCOUNT_PROFILES,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DiscountProfile,
    )


def get_discount_profile(
    client: Any,
    discount_profile_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DiscountProfile]:
    """Retrieve one profile — ``GET /admin/discount_profiles/{discount_profile_id}``.
    ``field_metadata`` adds the field schema beside the row."""
    return client.send_get_request(
        discount_profiles_urls.DISCOUNT_PROFILE,
        path_params={"discount_profile_id": discount_profile_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DiscountProfile,
    )


def update_discount_profile(
    client: Any,
    discount_profile_id: int | str,
    payload: DiscountProfilePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DiscountProfile]:
    """Replace one profile; a flag, date or limit the body omits is reset.
    ``PUT /admin/discount_profiles/{discount_profile_id}``"""
    require_payload(payload)
    return client.send_put_request(
        discount_profiles_urls.DISCOUNT_PROFILE,
        path_params={"discount_profile_id": discount_profile_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DiscountProfile,
    )


def delete_discount_profile(
    client: Any,
    discount_profile_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one profile and its coupons; ``204``, no body.
    ``DELETE /admin/discount_profiles/{discount_profile_id}``"""
    return client.send_delete_request(
        discount_profiles_urls.DISCOUNT_PROFILE,
        path_params={"discount_profile_id": discount_profile_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_discount_profile_coupons(
    client: Any,
    discount_profile_id: int | str,
    payload: DiscountProfilePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DiscountProfileCoupons]:
    """Generate codes on a profile that has ``is_apply_coupon_code``; ``{"requested_codes": n}``.
    ``POST /admin/discount_profiles/{discount_profile_id}/create-coupons``, answered ``201``"""
    require_payload(payload)
    return client.send_post_request(
        discount_profiles_urls.DISCOUNT_PROFILE_CREATE_COUPONS,
        path_params={"discount_profile_id": discount_profile_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DiscountProfileCoupons,
    )


def assign_discount_coupon_customer(
    client: Any,
    payload: DiscountProfilePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Assign a generated code to a customer — ``POST /admin/discount_coupons/assign-customer``,
    ``201``. The body is ``{"code", "email"}``; the answer is a verdict, so ``.dto`` is ``None``."""
    require_payload(payload)
    return client.send_post_request(
        discount_profiles_urls.DISCOUNT_COUPONS_ASSIGN_CUSTOMER,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
