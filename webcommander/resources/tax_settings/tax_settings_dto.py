"""Typed views over the tax settings bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class TaxSettings(Dto):
    """The nine keys the settings facade sends, flat; the ``PUT`` takes
    :class:`TaxSettingsInput`'s ``settings`` wrapper instead."""

    ENVELOPE_KEY = "tax_settings"

    configuration_type: str | None = None
    system_default_tax: bool | None = None
    default_country: str | None = None
    custom_tax_profile_id: int | None = None
    default_tax_profile: int | None = None
    show_price_with_tax: bool | None = None
    is_price_with_tax: bool | None = None
    default_tax_code: str | None = None
    tax_message: str | None = None


class TaxSettingsInput(Dto):
    """The body the settings ``PUT`` takes, wrapped in ``settings``; a merge.
    ``default_tax_profile`` and ``configuration_type`` must name values the store holds."""

    ENVELOPE_KEY = "settings"

    configuration_type: str | None = None
    system_default_tax: bool | None = None
    default_country: str | None = None
    custom_tax_profile_id: int | None = None
    default_tax_profile: int | None = None
    show_price_with_tax: bool | None = None
    is_price_with_tax: bool | None = None
    default_tax_code: str | None = None
    tax_message: str | None = None
