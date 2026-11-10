"""Typed views over the gift card bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class GiftCard(Dto):
    """One gift card. ``code`` is what an order preview's ``gift-card`` call takes; a card can be
    applied only while ``is_active`` and ``is_paid``, with a ``balance`` above zero, before its
    ``available_to`` date and with ``email`` equal to the previewed customer's email."""

    id: int | None = None
    code: str | None = None
    balance: float | None = None
    initial_amount: float | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    message: str | None = None
    is_active: bool | None = None
    is_paid: bool | None = None
    available_to: str | None = None
    external_reference: str | None = None
    product_name: str | None = None
    created_on: str | None = None


class Pagination(Dto):
    """The listing's ten-key ``pagination`` block; ``limit`` is the size the store applied, at
    most 20."""

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


class GiftCardPage(Dto):
    """One page of the listing, newest first."""

    gift_cards: list[GiftCard | None] | None = None
    pagination: Pagination | None = None
