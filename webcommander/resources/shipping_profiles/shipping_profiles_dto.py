"""Typed views over the shipping profile bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class ShippingReference(Dto):
    """An ``{id, name}`` pair: a rule's rate, and a zone named in the wizard, where a write sends
    ``{"id": ...}`` for an existing zone or ``{"name": ...}`` to create one."""

    id: int | None = None
    name: str | None = None


class ShippingProfileRule(Dto):
    """A rule on a profile; ``shipping_rate`` is ``None`` on a rule that has no rate."""

    id: int | None = None
    name: str | None = None
    shipping_rate: ShippingReference | None = None


class ShippingProfile(Dto):
    """One profile, the same ten keys on a listing row, the row read and every write's answer.
    ``rule_preference`` reads ``product_assigned_rule``, ``lowest_shipping_cost_rule`` or
    ``highest_shipping_cost_rule``; exactly one profile has ``default`` true."""

    ENVELOPE_KEY = "shipping_profile"

    id: int | None = None
    name: str | None = None
    description: str | None = None
    rule_preference: str | None = None
    default: bool | None = None
    rules_count: int | None = None
    shipping_rules: list[ShippingProfileRule | None] | None = None
    transaction_no: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class ShippingProfileInput(Dto):
    """The writable fields, wrapped in ``shipping_profile``, for the create, the ``PUT`` replace
    and the ``PATCH``. ``shipping_rules`` is the whole list of rule ids, each rule once; ``PUT``
    needs ``name``, ``description``, ``rule_preference`` and ``shipping_rules``. ``default`` takes
    only ``true`` or ``false``. Fields left ``None`` are not sent: to clear one, pass a mapping."""

    ENVELOPE_KEY = "shipping_profile"

    name: str | None = None
    description: str | None = None
    rule_preference: str | None = None
    default: bool | None = None
    shipping_rules: list[int] | None = None
    transaction_no: str | None = None
    suggest_name: bool | None = None


class ShippingProfileWizardRate(Dto):
    """The rate a wizard rule creates; the fields of a rate write, ``name`` and ``method``
    required."""

    name: str | None = None
    method: str | None = None
    calculate_for_entire_order: bool | None = None
    price_entered_with_tax: bool | None = None
    shipping_cost: Any = None
    handling_cost: Any = None
    conditions: list[Any] | None = None
    additional_rule: Any = None
    transaction_no: str | None = None


class ShippingProfileWizardRule(Dto):
    """A rule the wizard creates beside its rate: ``name`` is required, ``shipping_class`` is a
    class id, and ``zones`` name existing zones by ``{"id": ...}`` or new ones by
    ``{"name": ...}``."""

    name: str | None = None
    description: str | None = None
    shipping_class: int | None = None
    shipping_rate: ShippingProfileWizardRate | None = None
    zones: list[ShippingReference] | None = None


class ShippingProfileWizardInput(Dto):
    """The wizard's body, wrapped in ``shipping_profile``: the profile fields and the rules, each
    with its rate, to create under it."""

    ENVELOPE_KEY = "shipping_profile"

    name: str | None = None
    description: str | None = None
    rule_preference: str | None = None
    shipping_rules: list[ShippingProfileWizardRule] | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block; ``limit`` is the size the store applied."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class ShippingProfileListing(Dto):
    """One page of the listing, newest first."""

    shipping_profiles: list[ShippingProfile | None] | None = None
    pagination: Pagination | None = None


class ShippingProfileCount(Dto):
    """The count sub-path's body, a bare ``{"total": N}``."""

    total: int | None = None
