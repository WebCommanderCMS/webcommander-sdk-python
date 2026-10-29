"""Custom tax profile endpoints, under ``/api/{api_version}/admin/tax/custom-profiles``.
No ``HEAD``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.tax_custom_profiles import tax_custom_profiles_urls
from webcommander.resources.tax_custom_profiles.tax_custom_profiles_dto import (
    CustomProfile,
    CustomProfilePage,
)

__all__ = [
    "list_tax_custom_profiles",
    "create_tax_custom_profile",
    "get_tax_custom_profile",
    "update_tax_custom_profile",
    "delete_tax_custom_profile",
]

CustomProfilePayload = Mapping[str, Any] | str | Dto


def list_tax_custom_profiles(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomProfilePage]:
    """List the custom profiles — ``GET /admin/tax/custom-profiles``, newest first. ``limit`` is
    1 to 100 with the cap echoed, ``offset`` or ``page`` move the window, ``sort`` takes ``id``
    or ``name``."""
    return client.send_get_request(
        tax_custom_profiles_urls.TAX_CUSTOM_PROFILES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomProfilePage,
    )


def create_tax_custom_profile(
    client: Any,
    payload: CustomProfilePayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomProfile]:
    """Create a custom profile — ``POST /admin/tax/custom-profiles``, answered ``201``. The body
    is wrapped in ``custom_profile`` and needs ``name``. ``transaction_no`` is sent as
    ``X-Transaction-No`` and files the profile under that number."""
    require_payload(payload)
    return client.send_post_request(
        tax_custom_profiles_urls.TAX_CUSTOM_PROFILES,
        json_body=payload,
        headers=None
        if transaction_no is None
        else {tax_custom_profiles_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomProfile,
    )


def get_tax_custom_profile(
    client: Any,
    custom_profile_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomProfile]:
    """Retrieve one custom profile, with an ``ETag``; only this form carries ``rules``.
    ``GET /admin/tax/custom-profiles/{custom_profile_id}``"""
    return client.send_get_request(
        tax_custom_profiles_urls.TAX_CUSTOM_PROFILE,
        path_params={"custom_profile_id": custom_profile_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomProfile,
    )


def update_tax_custom_profile(
    client: Any,
    custom_profile_id: int | str,
    payload: CustomProfilePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CustomProfile]:
    """Replace one custom profile — ``PUT /admin/tax/custom-profiles/{custom_profile_id}``. An
    omitted ``name`` is kept; an omitted ``description`` or ``tax_code`` comes back ``null``."""
    require_payload(payload)
    return client.send_put_request(
        tax_custom_profiles_urls.TAX_CUSTOM_PROFILE,
        path_params={"custom_profile_id": custom_profile_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CustomProfile,
    )


def delete_tax_custom_profile(
    client: Any,
    custom_profile_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one custom profile; ``204``, no body.
    ``DELETE /admin/tax/custom-profiles/{custom_profile_id}``"""
    return client.send_delete_request(
        tax_custom_profiles_urls.TAX_CUSTOM_PROFILE,
        path_params={"custom_profile_id": custom_profile_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
