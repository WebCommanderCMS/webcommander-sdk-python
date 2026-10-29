"""Typed views over the domain alias bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class Alias(Dto):
    """One alias: a listing row, or the record a create answers under ``alias``, the same four
    fields either way. ``alias`` is the hostname; the two stamps are set by the store."""

    ENVELOPE_KEY = "alias"

    id: int | None = None
    alias: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AliasInput(Dto):
    """The create body, ``{"alias": "<hostname>"}``. The field is bare: the same hostname
    wrapped in an ``alias`` record is ``400 invalid_hostname``."""

    alias: str | None = None


class Pagination(Dto):
    """The listing's five-key ``pagination`` block; ``limit`` is the size the store applied."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_next: bool | None = None
    has_previous: bool | None = None


class AliasPage(Dto):
    """One page of the listing. The resource serves no field schema: ``field_metadata`` adds
    no key."""

    aliases: list[Alias] | None = None
    pagination: Pagination | None = None
