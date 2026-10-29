"""Typed views over the country and state bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class Country(Dto):
    """One country: a listing row, and the row path's body."""

    ENVELOPE_KEY = "country"

    id: int | None = None
    code: str | None = None
    name: str | None = None
    state_count: int | None = None
    active: bool | None = None
    default: bool | None = None


class CountryReference(Dto):
    """The short parent country a state listing and a state read carry beside the state."""

    id: int | None = None
    code: str | None = None
    name: str | None = None


class CountryState(Dto):
    """One state: a listing row, and the state path's body with its parent ``country`` beside it."""

    ENVELOPE_KEY = "state"

    id: int | None = None
    code: str | None = None
    name: str | None = None
    active: bool | None = None
    default: bool | None = None
    country: CountryReference | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block of both listings. ``limit`` is the page size applied:
    the one asked for, 20, or under ``limit=all`` the number of rows that arrived."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class CountryPage(Dto):
    """One page of the country listing: the rows, and the block that says where they sit."""

    countries: list[Country | None] | None = None
    pagination: Pagination | None = None


class CountryStatePage(Dto):
    """One page of a country's states, beside the short parent country."""

    country: CountryReference | None = None
    states: list[CountryState | None] | None = None
    pagination: Pagination | None = None
