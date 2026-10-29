"""Typed views over the city listing."""

from __future__ import annotations

from webcommander.dto import Dto


class CityState(Dto):
    """The state a city row carries. ``id`` is the one a country's ``states`` listing answers;
    ``default`` follows the ``administration`` section's ``default_state``."""

    id: int | None = None
    code: str | None = None
    name: str | None = None
    active: bool | None = None
    default: bool | None = None


class CityCountry(Dto):
    """The country a city row carries; ``id`` is the one the ``countries`` listing answers."""

    id: int | None = None
    code: str | None = None
    name: str | None = None


class City(Dto):
    """One listing row."""

    id: int | None = None
    name: str | None = None
    post_code: str | None = None
    state: CityState | None = None
    country: CityCountry | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block: ``total`` is the number of rows that matched, ``limit``
    the page size applied and ``offset`` the start."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class CityPage(Dto):
    """One page of the city listing: the rows, and the block that says where they sit."""

    cities: list[City | None] | None = None
    pagination: Pagination | None = None
