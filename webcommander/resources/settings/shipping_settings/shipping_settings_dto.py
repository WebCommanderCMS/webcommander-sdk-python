"""Typed views over the shipping settings body."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class ProfileReference(Dto):
    """What a reference field holds: the stored id and the name it resolves to, or ``null``."""

    id: int | None = None
    name: str | None = None


class AreaMeta(Dto):
    """One ``group_meta`` entry: what the area is, whether it can be written, and its path."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block: the settings area and the two collections beside it."""

    shipping_settings: AreaMeta | None = None
    shipping_methods: AreaMeta | None = None
    shipping_classes: AreaMeta | None = None


class ShippingSettings(Dto):
    """The shipping settings: seven fields flat under ``shipping_settings``, and ``group_meta``.
    A write may send a reference as an id, which is a mapping body rather than this type."""

    ENVELOPE_KEY = "shipping_settings"

    default_shipping_profile: ProfileReference | None = None
    apply_store_tax_settings_to_shipping: bool | None = None
    default_delivery_profile: ProfileReference | None = None
    apply_store_tax_settings_to_delivery: bool | None = None
    shipping_tax_profile: ProfileReference | None = None
    enable_shipping_class: bool | None = None
    enable_class_in_flat_view: bool | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
