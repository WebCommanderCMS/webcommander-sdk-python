"""City endpoints, under ``/api/{api_version}/app``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.resources.cities import cities_urls
from webcommander.resources.cities.cities_dto import CityPage

__all__ = [
    "list_cities",
    "head_cities",
]


def list_cities(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[CityPage]:
    """List the cities, by state, post code and name unless ``sort`` says otherwise —
    ``GET /app/cities``. ``limit`` is the page size, 1 to 100 and 100 when absent; ``offset`` the
    start. ``country`` takes a country id or two-letter code, ``state`` a state id or, beside
    ``country``, a state code; ``post_code`` matches exactly and ``search`` a substring of
    ``name`` in any case. ``sort`` is ``state``, ``name`` or ``post_code``, ``order`` ``asc`` or
    ``desc``."""
    return client.send_get_request(
        cities_urls.CITIES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=CityPage,
    )


def head_cities(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the listing is reachable — ``HEAD /app/cities``; the listing's headers, its
    ``ETag`` among them, and no body."""
    return client.send_api_request(
        "HEAD",
        cities_urls.CITIES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
