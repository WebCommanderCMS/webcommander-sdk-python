"""Typed views over the shipping settings body."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class ProfileReference(Dto):
    """What a reference field holds: the stored id and the name it resolves to, or ``null``."""

    id: int | None = None
    name: str | None = None


class AreaMeta(Dto):
    """The single ``group_meta`` entry: what the area is and whether it can be written."""

    kind: str | None = None
    writable: bool | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block — a single :class:`AreaMeta`, keyed by the area itself."""

    shipping_settings: AreaMeta | None = None


class ShippingSettings(Dto):
    """The shipping settings: seven fields flat under ``shipping_settings``, and ``group_meta``.
    A write may send a reference as an id, which is a mapping body rather than this type."""

    ENVELOPE_KEY = "shipping_settings"

    default_shipping_profile: ProfileReference | None = None
    enable_shipping_default_tax: bool | None = None
    default_delivery_profile: ProfileReference | None = None
    enable_delivery_default_tax: bool | None = None
    shipping_tax_profile: ProfileReference | None = None
    enable_shipping_class: bool | None = None
    enable_flat_view_class: bool | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
