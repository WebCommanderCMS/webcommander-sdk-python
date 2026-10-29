"""Typed views over the order flag bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class OrderFlag(Dto):
    """One order flag, the same five fields on the listing row and on the row path.
    ``type`` reads ``order`` on every row and is not writable."""

    ENVELOPE_KEY = "order_flag"

    id: int | None = None
    name: str | None = None
    color: str | None = None
    description: str | None = None
    type: str | None = None


class OrderFlagInput(Dto):
    """The writable form of :class:`OrderFlag`; ``name`` and a hex ``color`` are required.
    The update is a replace: a field left unset is blanked by the store."""

    ENVELOPE_KEY = "order_flag"

    name: str | None = None
    color: str | None = None
    description: str | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block; ``limit`` is the size applied, not the one asked."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_next: bool | None = None
    has_previous: bool | None = None


class OrderFlagPage(Dto):
    """One page of the listing: the rows, and the block that says where they sit."""

    order_flags: list[OrderFlag] | None = None
    pagination: Pagination | None = None
