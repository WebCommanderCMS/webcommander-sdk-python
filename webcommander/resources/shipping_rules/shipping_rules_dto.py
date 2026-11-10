"""Typed views over the shipping rule bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class ShippingReference(Dto):
    """An ``{id, name}`` pair: the rule's class, rate, zones and profiles. A write names a class,
    a rate or a zone by its id, bare or as ``{"id": ...}``; ``name`` is read-only."""

    id: int | None = None
    name: str | None = None


class ShippingRule(Dto):
    """One rule, the same ten keys on a listing row, the row read and every write's answer.
    ``shipping_class`` and ``shipping_rate`` are ``None`` when unset, ``zones`` and ``profiles``
    empty lists."""

    ENVELOPE_KEY = "shipping_rule"

    id: int | None = None
    name: str | None = None
    description: str | None = None
    shipping_class: ShippingReference | None = None
    shipping_rate: ShippingReference | None = None
    zones: list[ShippingReference | None] | None = None
    profiles: list[ShippingReference | None] | None = None
    transaction_no: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class ShippingRuleInput(Dto):
    """The writable fields, wrapped in ``shipping_rule``, for the create, the ``PUT`` replace and
    the ``PATCH``. ``zones`` is the whole list of zones, each once; ``profile_id`` adds the new
    rule to a profile on a create. ``PUT`` needs ``name``, ``description``, ``shipping_class``,
    ``shipping_rate`` and ``zones``. Fields left ``None`` are not sent: to clear a class or a rate,
    pass a mapping holding ``None``."""

    ENVELOPE_KEY = "shipping_rule"

    name: str | None = None
    description: str | None = None
    shipping_class: int | ShippingReference | None = None
    shipping_rate: int | ShippingReference | None = None
    zones: list[int | ShippingReference] | None = None
    profile_id: int | None = None
    transaction_no: str | None = None
    suggest_name: bool | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block; ``limit`` is the size the store applied."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class ShippingRuleListing(Dto):
    """One page of the listing, newest first."""

    shipping_rules: list[ShippingRule | None] | None = None
    pagination: Pagination | None = None


class ShippingRuleCount(Dto):
    """The count sub-path's body, a bare ``{"total": N}``."""

    total: int | None = None
