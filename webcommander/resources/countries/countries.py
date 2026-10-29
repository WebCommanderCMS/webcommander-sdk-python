"""Country endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.resources.countries import countries_urls
from webcommander.resources.countries.countries_dto import (
    Country,
    CountryPage,
    CountryState,
    CountryStatePage,
)

__all__ = [
    "list_countries",
    "head_countries",
    "get_country",
    "head_country",
    "list_country_states",
    "head_country_states",
    "get_country_state",
    "head_country_state",
]


def list_countries(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CountryPage]:
    """List the countries — ``GET /admin/countries``, ``id`` ascending. ``limit`` is 1 to 100 or
    ``all``, default 20; ``code``, ``name`` and ``id`` match exactly, ``search`` a substring of
    ``name`` or ``code``; ``active``; ``sort`` ``id``, ``name`` or ``code`` with ``order``."""
    return client.send_get_request(
        countries_urls.COUNTRIES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CountryPage,
    )


def head_countries(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/countries``; no body, and the
    ``ETag`` the listing's first page carries."""
    return client.send_api_request(
        "HEAD",
        countries_urls.COUNTRIES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_country(
    client: Any,
    country_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Country]:
    """Retrieve one country — ``GET /admin/countries/{country_id}``. The slot takes the numeric
    ``id``, the ISO ``code`` or the ``name``, in any case."""
    return client.send_get_request(
        countries_urls.COUNTRY,
        path_params={"country_id": country_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Country,
    )


def head_country(
    client: Any,
    country_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one country is there; no body, and the ``ETag`` its read carries.
    ``HEAD /admin/countries/{country_id}``"""
    return client.send_api_request(
        "HEAD",
        countries_urls.COUNTRY,
        path_params={"country_id": country_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def list_country_states(
    client: Any,
    country_id: int | str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CountryStatePage]:
    """List one country's states, beside the short parent country; the same query names as
    :func:`list_countries`. ``GET /admin/countries/{country_id}/states``"""
    return client.send_get_request(
        countries_urls.COUNTRY_STATES,
        path_params={"country_id": country_id},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CountryStatePage,
    )


def head_country_states(
    client: Any,
    country_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one country's states are reachable; no body, and the ``ETag`` the state
    listing's first page carries. ``HEAD /admin/countries/{country_id}/states``"""
    return client.send_api_request(
        "HEAD",
        countries_urls.COUNTRY_STATES,
        path_params={"country_id": country_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_country_state(
    client: Any,
    country_id: int | str,
    state_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CountryState]:
    """Retrieve one state of one country; ``state_id`` takes the state's ``id``, ``code`` or
    ``name``, in any case. ``GET /admin/countries/{country_id}/states/{state_id}``"""
    return client.send_get_request(
        countries_urls.COUNTRY_STATE,
        path_params={"country_id": country_id, "state_id": state_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CountryState,
    )


def head_country_state(
    client: Any,
    country_id: int | str,
    state_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one state of one country is there; no body, and the ``ETag`` its read
    carries. ``HEAD /admin/countries/{country_id}/states/{state_id}``"""
    return client.send_api_request(
        "HEAD",
        countries_urls.COUNTRY_STATE,
        path_params={"country_id": country_id, "state_id": state_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
