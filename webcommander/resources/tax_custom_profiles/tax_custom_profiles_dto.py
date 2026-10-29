"""Typed views over the custom tax profile bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class CustomProfileReference(Dto):
    """One profile a rule is filed under, on the rule's ``profiles``."""

    id: int | None = None
    name: str | None = None


class CustomProfileRule(Dto):
    """One entry of a custom profile's ``rules``, which only the row path sends."""

    id: int | None = None
    name: str | None = None
    description: str | None = None
    zones_count: int | None = None
    profiles: list[CustomProfileReference] | None = None
    created_on: str | None = None
    last_updated_on: str | None = None


class CustomProfile(Dto):
    """One custom tax profile; the row path adds ``rules`` to the eight keys a listing row, the
    create and the update answer carry."""

    ENVELOPE_KEY = "custom_profile"

    id: int | None = None
    name: str | None = None
    tax_code: str | None = None
    description: str | None = None
    is_default: bool | None = None
    rules_count: int | None = None
    created_on: str | None = None
    last_updated_on: str | None = None
    rules: list[CustomProfileRule] | None = None


class CustomProfileInput(Dto):
    """The writable form of :class:`CustomProfile`; ``name`` is the create's one requirement.
    The update is a replace, except that it keeps an omitted ``name``."""

    ENVELOPE_KEY = "custom_profile"
    TOP_LEVEL = ("transaction_no",)

    name: str | None = None
    tax_code: str | None = None
    description: str | None = None
    is_default: bool | None = None
    transaction_no: str | None = None


class ResourceMeta(Dto):
    """One ``group_meta`` entry: what the path is, whether it is writable and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block only the listing sends."""

    custom_profile: ResourceMeta | None = None
    rules: ResourceMeta | None = None


class Pagination(Dto):
    """The ten-key ``pagination`` block; ``limit`` is the size the store applied, capped at 100."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    count: int | None = None
    current_page: int | None = None
    total_pages: int | None = None
    has_next: bool | None = None
    has_previous: bool | None = None
    previous_page: str | None = None
    next_page: str | None = None


class CustomProfilePage(Dto):
    """One page of the custom profile listing: the rows, ``group_meta`` and the paging block."""

    custom_profiles: list[CustomProfile] | None = None
    group_meta: GroupMeta | None = None
    pagination: Pagination | None = None
