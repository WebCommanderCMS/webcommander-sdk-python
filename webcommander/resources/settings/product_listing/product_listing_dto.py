"""Typed views over the product listing body."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class InteractionButtons(Dto):
    """The ``add to cart`` and ``view details`` buttons on a listing tile."""

    enabled: bool | None = None
    add_to_cart: bool | None = None
    show_view_details: bool | None = None
    show_on_hover: bool | None = None


class ListingPrice(Dto):
    """Which prices a listing tile shows."""

    enabled: bool | None = None
    expect_to_pay: bool | None = None
    expect_to_pay_with_tax: bool | None = None


class Reviews(Dto):
    """The rating stars on a listing tile and the count beside them."""

    show_rating: bool | None = None
    show_review_count: bool | None = None


class VariationCombination(Dto):
    """Which variation types a listing tile combines, from the store's own variation names."""

    enabled: bool | None = None
    types: list[str] | None = None


class ProductInformation(Dto):
    """The ``product_information`` section — what each product shows on a listing tile."""

    interaction_buttons: InteractionButtons | None = None
    show_summary: bool | None = None
    show_sale_percentage: bool | None = None
    show_stock_availability: bool | None = None
    show_parent_category: bool | None = None
    show_loyalty_points: bool | None = None
    price: ListingPrice | None = None
    reviews: Reviews | None = None
    variation_combination: VariationCombination | None = None
    show_variations_as_products: bool | None = None


class Pagination(Dto):
    """Where the pager sits and how many products a page holds."""

    position: str | None = None
    per_page: int | None = None
    allow_user_per_page: bool | None = None


class LoadMore(Dto):
    """How many products each press of *load more* adds. Bounded ``1``–``999999``."""

    per_load: int | None = None


class Load(Dto):
    """The ``load`` section — whether a listing pages or loads more; ``type`` selects the block."""

    enabled: bool | None = None
    type: str | None = None
    pagination: Pagination | None = None
    load_more: LoadMore | None = None


class Sorting(Dto):
    """The ``sorting`` section — the order a listing arrives in."""

    enabled: bool | None = None
    sort_by: str | None = None


class SortableOptions(Dto):
    """Which orders a shopper may pick from."""

    alphabetic: bool | None = None
    featured: bool | None = None
    new: bool | None = None
    top_selling: bool | None = None
    price: bool | None = None
    created_date: bool | None = None


class SortableItems(Dto):
    """The ``sortable_items`` section — whether a shopper may re-sort a listing, and by what."""

    enabled: bool | None = None
    options: SortableOptions | None = None


class SectionMeta(Dto):
    """The one entry of ``group_meta``: what the area is, whether it is writable and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block — a single entry for the whole area, not one per section."""

    product_listing: SectionMeta | None = None


class ProductListing(Dto):
    """The product listing settings, all four sections inlined under ``product_listing``.
    ``to_map()`` renders the body the ``PATCH`` takes; a section type carries no envelope."""

    ENVELOPE_KEY = "product_listing"

    product_information: ProductInformation | None = None
    load: Load | None = None
    sorting: Sorting | None = None
    sortable_items: SortableItems | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
