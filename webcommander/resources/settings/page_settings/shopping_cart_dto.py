"""Typed views over the shopping cart settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class CartPage(Dto):
    """The ``cart_page`` section — what the cart page offers a shopper; three booleans."""

    ENVELOPE_KEY = "cart_page"

    show_product_thumbnail: bool | None = None
    enable_clear_cart: bool | None = None
    save_cart: bool | None = None


class FlyingCart(Dto):
    """The ``flying_cart`` section — the slide-out cart and what it offers; three booleans."""

    ENVELOPE_KEY = "flying_cart"

    enabled: bool | None = None
    enable_clear_cart: bool | None = None
    save_cart: bool | None = None


class SectionMeta(Dto):
    """One entry of ``group_meta``: what a section is, whether it can be written and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends."""

    cart_page: SectionMeta | None = None
    flying_cart: SectionMeta | None = None


class ShoppingCart(Dto):
    """The shopping cart settings, as the facade's body or as one section's body."""

    ENVELOPE_KEY = "shopping_cart"

    cart_page: CartPage | None = None
    flying_cart: FlyingCart | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
