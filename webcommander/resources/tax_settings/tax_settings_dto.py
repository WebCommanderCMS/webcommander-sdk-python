"""Typed views over the tax settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class TaxRegion(Dto):
    """The country tax the store charges by default, as ``tax_region`` reads it."""

    country_tax_id: int | None = None
    country_code: str | None = None
    country_name: str | None = None


class TaxProfileReference(Dto):
    """A custom tax profile as a read names it: its id and name, or ``null``."""

    id: int | None = None
    name: str | None = None


class TaxSettingsAreaMeta(Dto):
    """One ``group_meta`` entry: what the area is, whether it can be written, and its path."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class TaxSettingsGroupMeta(Dto):
    """The ``group_meta`` block: the settings area and the two tax collections beside it."""

    tax_settings: TaxSettingsAreaMeta | None = None
    tax_profiles: TaxSettingsAreaMeta | None = None
    tax_rules: TaxSettingsAreaMeta | None = None


class TaxSettings(Dto):
    """The nine keys under ``tax_settings``, with ``group_meta`` and, when asked for,
    ``field_metadata``."""

    ENVELOPE_KEY = "tax_settings"

    tax_rate_for_customers: str | None = None
    tax_region: TaxRegion | None = None
    custom_tax_profile: TaxProfileReference | None = None
    is_price_shown_with_tax: bool | None = None
    prices_in_catalog: str | None = None
    calculated_by: str | None = None
    is_out_of_region_tax_free: bool | None = None
    tax_message: str | None = None
    base_price_rounding: str | None = None
    group_meta: TaxSettingsGroupMeta | None = None
    field_metadata: Any = None


class TaxRegionInput(Dto):
    """``tax_region`` as a write takes it: a ``country_code`` (with an optional ``state_code``)
    or a ``country_tax_id``."""

    country_tax_id: int | None = None
    country_code: str | None = None
    state_code: str | None = None


class TaxSettingsInput(Dto):
    """The body ``PUT`` and ``PATCH`` take, wrapped in ``tax_settings``; both merge.
    The profile is written as ``custom_tax_profile_id``; ``calculated_by`` is read-only."""

    ENVELOPE_KEY = "tax_settings"

    tax_rate_for_customers: str | None = None
    tax_region: TaxRegionInput | None = None
    custom_tax_profile_id: int | None = None
    is_price_shown_with_tax: bool | None = None
    prices_in_catalog: str | None = None
    is_out_of_region_tax_free: bool | None = None
    tax_message: str | None = None
    base_price_rounding: str | None = None
