"""Tax profile endpoints, under ``/api/{api_version}/admin/tax_profiles``.
``default`` is exclusive and one-way, and the tax settings' ``default_tax_profile`` follows it."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.tax_profiles import tax_profiles_urls
from webcommander.resources.tax_profiles.tax_profiles_dto import TaxProfile, TaxProfilePage

__all__ = [
    "list_tax_profiles",
    "head_tax_profiles",
    "create_tax_profile",
    "get_tax_profile",
    "head_tax_profile",
    "update_tax_profile",
    "delete_tax_profile",
]

TaxProfilePayload = Mapping[str, Any] | str | Dto


def list_tax_profiles(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxProfilePage]:
    """List the tax profiles — ``GET /admin/tax_profiles``. ``limit`` is capped at 20."""
    return client.send_get_request(
        tax_profiles_urls.TAX_PROFILES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxProfilePage,
    )


def head_tax_profiles(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/tax_profiles``; no body."""
    return client.send_api_request(
        "HEAD",
        tax_profiles_urls.TAX_PROFILES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_tax_profile(
    client: Any,
    payload: TaxProfilePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxProfile]:
    """Create a tax profile — ``POST /admin/tax_profiles``, answered ``201``. The body is wrapped
    in ``tax_profile``."""
    require_payload(payload)
    return client.send_post_request(
        tax_profiles_urls.TAX_PROFILES,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxProfile,
    )


def get_tax_profile(
    client: Any,
    tax_profile_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxProfile]:
    """Retrieve one tax profile — ``GET /admin/tax_profiles/{tax_profile_id}``."""
    return client.send_get_request(
        tax_profiles_urls.TAX_PROFILE,
        path_params={"tax_profile_id": tax_profile_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxProfile,
    )


def head_tax_profile(
    client: Any,
    tax_profile_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one tax profile is there — ``HEAD /admin/tax_profiles/{tax_profile_id}``.
    An id no row holds is ``200`` too, so this does not prove the row exists."""
    return client.send_api_request(
        "HEAD",
        tax_profiles_urls.TAX_PROFILE,
        path_params={"tax_profile_id": tax_profile_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_tax_profile(
    client: Any,
    tax_profile_id: int | str,
    payload: TaxProfilePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxProfile]:
    """Update one tax profile — ``PUT /admin/tax_profiles/{tax_profile_id}``; a merge.
    ``default: true`` moves the flag off the row that held it; ``false`` does not clear it."""
    require_payload(payload)
    return client.send_put_request(
        tax_profiles_urls.TAX_PROFILE,
        path_params={"tax_profile_id": tax_profile_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxProfile,
    )


def delete_tax_profile(
    client: Any,
    tax_profile_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one tax profile — ``DELETE /admin/tax_profiles/{tax_profile_id}``; ``204``.
    The default row is deleted like any other, leaving ``default_tax_profile`` naming nothing."""
    return client.send_delete_request(
        tax_profiles_urls.TAX_PROFILE,
        path_params={"tax_profile_id": tax_profile_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
