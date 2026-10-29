"""Typed views over the search result page settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class ProductInteractionButtons(Dto):
    """The ``product_interaction_buttons`` block — which buttons each result carries."""

    enabled: bool | None = None
    display_add_to_cart_button: bool | None = None
    display_add_to_compare_button: bool | None = None
    display_add_to_wishlist_button: bool | None = None
    display_view_details_button: bool | None = None
    display_on_hover: bool | None = None
    display_quick_view_button: bool | None = None


class NumberOfSearchesPerResult(Dto):
    """The ``number_of_searches_per_result`` block — result pagination and the page size."""

    enabled: bool | None = None
    items_per_page: int | None = None


class SetProductDisplayPreferences(Dto):
    """The ``set_product_display_preferences`` block — how results load, and the pager's place."""

    enabled: bool | None = None
    display_mode: str | None = None
    select_pagination_position: str | None = None
    number_of_products_per_page: int | None = None
    allow_users_to_select_number_of_products: bool | None = None
    number_of_products_per_load: int | None = None


class SetProductSorting(Dto):
    """The ``set_product_sorting`` block — whether a default sort applies, and which."""

    enabled: bool | None = None
    default_sort: str | None = None


class ConfigureSortingOptions(Dto):
    """The ``configure_sorting_options`` block — which sort orders a shopper may switch to."""

    enabled: bool | None = None
    alphabetical: bool | None = None
    featured: bool | None = None
    new: bool | None = None
    top_selling: bool | None = None
    price: bool | None = None
    created_date: bool | None = None


class DisplayPrice(Dto):
    """The ``display_price`` block — whether a result shows a price, and which price."""

    enabled: bool | None = None
    display_expect_to_pay_price: bool | None = None
    show_tax_with_the_expect_to_pay_price: bool | None = None


class ProductInformation(Dto):
    """The ``product_information`` section — each search result and the list's behaviour."""

    ENVELOPE_KEY = "product_information"

    use_default_product_listing_configurations: bool | None = None
    product_interaction_buttons: ProductInteractionButtons | None = None
    display_content_page: bool | None = None
    number_of_searches_per_result: NumberOfSearchesPerResult | None = None
    display_short_description: bool | None = None
    display_variations_combination: bool | None = None
    set_product_display_preferences: SetProductDisplayPreferences | None = None
    set_product_sorting: SetProductSorting | None = None
    configure_sorting_options: ConfigureSortingOptions | None = None
    display_loyalty_points: bool | None = None
    display_price: DisplayPrice | None = None
    label_for_price: str | None = None


class Seo(Dto):
    """The ``seo`` section — two read-only markers; this page's SEO is configured elsewhere."""

    ENVELOPE_KEY = "seo"

    read_only: bool | None = None
    page_kind: str | None = None


class Reinitialise(Dto):
    """The ``reinitialise`` section — a read-only marker for an action on another resource."""

    ENVELOPE_KEY = "reinitialise"

    action: str | None = None


class ProductPromotionPreview(Dto):
    """The ``product_promotion`` marker the facade inlines in place of the rows."""

    read_only: bool | None = None


class ProductPromotion(Dto):
    """One promotion row; a listing sends rows under ``product_promotions`` with no envelope."""

    ENVELOPE_KEY = "product_promotion"

    id: int | None = None
    name: str | None = None
    rule: str | None = None
    position: str | None = None
    specific_keywords: str | None = None
    is_active: bool | None = None
    is_always_available: bool | None = None
    available_from_date: str | None = None
    available_to_date: str | None = None
    product_ids: list[int | None] | None = None
    created: str | None = None
    updated: str | None = None


class SectionMeta(Dto):
    """One entry of ``group_meta``; two of the four ``href`` values name another resource."""

    kind: str | None = None
    writable: bool | None = None
    ui_label: str | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends."""

    product_information: SectionMeta | None = None
    seo: SectionMeta | None = None
    product_promotion: SectionMeta | None = None
    reinitialise: SectionMeta | None = None


class SearchResultPage(Dto):
    """The search result page settings; a section arrives under the facade's key too, one level
    in."""

    ENVELOPE_KEY = "search_result_page"

    product_information: ProductInformation | None = None
    seo: Seo | None = None
    product_promotion: ProductPromotionPreview | None = None
    reinitialise: Reinitialise | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
