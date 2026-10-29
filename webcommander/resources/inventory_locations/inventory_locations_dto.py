"""Typed views over the inventory location bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class InventoryLocation(Dto):
    """One inventory location: a listing row, a row path's body, and every write's answer."""

    ENVELOPE_KEY = "inventory_location"

    id: int | None = None
    name: str | None = None
    address: str | None = None
    active: bool | None = None
    default: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None


class InventoryLocationInput(Dto):
    """The writable form of :class:`InventoryLocation` for the create, the update and the patch; no
    envelope. Left unset, the update blanks ``address`` and turns ``active`` on; the patch keeps both."""

    name: str | None = None
    address: str | None = None
    active: bool | None = None
    default: bool | None = None


class InventoryLocationStatusInput(Dto):
    """The status sub-path's body; ``active`` is required and the only field accepted."""

    active: bool | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block of the listing and of the stock sub-path.
    ``limit`` is the page size applied: the one asked for, or 20."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class InventoryLocationPage(Dto):
    """One page of the listing: the rows, and the block that says where they sit."""

    inventory_locations: list[InventoryLocation] | None = None
    pagination: Pagination | None = None


class InventoryLocationStockProduct(Dto):
    """The product one stock item belongs to."""

    id: int | None = None
    name: str | None = None
    sku: str | None = None


class InventoryLocationStockItem(Dto):
    """One product's holding at one location; ``default_for_product`` is the product's own flag."""

    product: InventoryLocationStockProduct | None = None
    variation: Any = None
    available_stock: int | None = None
    low_stock_level: int | None = None
    default_for_product: bool | None = None


class InventoryLocationStock(Dto):
    """The stock sub-path's body: the location, its items and their pagination."""

    inventory_location: InventoryLocation | None = None
    items: list[InventoryLocationStockItem] | None = None
    pagination: Pagination | None = None
