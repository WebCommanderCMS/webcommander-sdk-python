"""Typed views over the category page settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class CategoryHeading(Dto):
    """The ``heading`` block — whether the category name shows, and at which heading level."""

    enabled: bool | None = None
    style: str | None = None


class Subcategory(Dto):
    """The ``subcategory`` block — whether subcategories are listed, and how that list pages."""

    enabled: bool | None = None
    display: bool | None = None
    load_type: str | None = None
    pagination_position: str | None = None
    per_page: int | None = None
    allow_user_per_page: bool | None = None
    per_load: int | None = None
    display_products: bool | None = None
    show_summary: bool | None = None


class CategoryInformation(Dto):
    """The ``category_information`` section — the category itself and its subcategory list."""

    ENVELOPE_KEY = "category_information"

    heading: CategoryHeading | None = None
    show_description: bool | None = None
    show_banner_image: bool | None = None
    show_image: bool | None = None
    subcategory: Subcategory | None = None


class InteractionButtons(Dto):
    """The ``interaction_buttons`` block — which buttons each product card carries."""

    enabled: bool | None = None
    add_to_cart: bool | None = None
    view_details: bool | None = None
    show_on_hover: bool | None = None
    add_to_wish_list: bool | None = None
    add_to_compare: bool | None = None
    quick_view: bool | None = None


class Price(Dto):
    """The ``price`` block — whether a card shows a price, and which price."""

    enabled: bool | None = None
    expect_to_pay: bool | None = None
    expect_to_pay_with_tax: bool | None = None
    strike_through_previous: bool | None = None


class VariationType(Dto):
    """One variation type, by ``id`` and ``name``; take the ids from ``field_metadata``."""

    id: int | None = None
    name: str | None = None


class VariationCombination(Dto):
    """The ``variation_combination`` block — combinations shown, and the types offered."""

    enabled: bool | None = None
    types: list[VariationType | None] | None = None


class Rating(Dto):
    """The ``rating`` block — whether the rating shows, and the review count beside it."""

    enabled: bool | None = None
    show_review_count: bool | None = None


class ViewSwitcher(Dto):
    """The ``view_switcher`` block — which display modes a shopper may switch between."""

    enabled: bool | None = None
    grid: bool | None = None
    list: bool | None = None
    tabular: bool | None = None


class ColumnsPerRow(Dto):
    """The ``columns_per_row`` block — columns per row for each mode, each with its own ``max``."""

    grid: int | None = None
    list: int | None = None


class DefaultDisplay(Dto):
    """The ``default_display`` block — the mode a listing opens in and how wide its rows are."""

    enabled: bool | None = None
    mode: str | None = None
    columns_per_row: ColumnsPerRow | None = None
    show_variation_options_label_in_tabular: bool | None = None


class ProductLoad(Dto):
    """The ``load`` block — how the product listing pages and where its control sits."""

    enabled: bool | None = None
    type: str | None = None
    pagination_position: str | None = None
    per_page: int | None = None
    allow_user_per_page: bool | None = None
    per_load: int | None = None


class DefaultSort(Dto):
    """The ``default_sort`` block — whether a default order applies, and which."""

    enabled: bool | None = None
    by: str | None = None


class SortOptions(Dto):
    """The ``sort_options`` block — which orders a shopper may switch to."""

    enabled: bool | None = None
    alphabetic: bool | None = None
    featured: bool | None = None
    new: bool | None = None
    top_selling: bool | None = None
    price: bool | None = None
    date: bool | None = None


class ProductInformation(Dto):
    """The ``product_information`` section — each product card and the listing's behaviour."""

    ENVELOPE_KEY = "product_information"

    use_global_defaults: bool | None = None
    interaction_buttons: InteractionButtons | None = None
    show_summary: bool | None = None
    show_sale_percentage: bool | None = None
    show_stock_availability: bool | None = None
    show_parent_category: bool | None = None
    price: Price | None = None
    variation_combination: VariationCombination | None = None
    rating: Rating | None = None
    view_switcher: ViewSwitcher | None = None
    default_display: DefaultDisplay | None = None
    load: ProductLoad | None = None
    default_sort: DefaultSort | None = None
    sort_options: SortOptions | None = None


class SectionMeta(Dto):
    """One entry of ``group_meta``: what a section is, whether it can be written and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends."""

    category_information: SectionMeta | None = None
    product_information: SectionMeta | None = None


class CategoryPage(Dto):
    """The category page settings, as the facade's body or as one section's body."""

    ENVELOPE_KEY = "category_page"

    category_information: CategoryInformation | None = None
    product_information: ProductInformation | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
