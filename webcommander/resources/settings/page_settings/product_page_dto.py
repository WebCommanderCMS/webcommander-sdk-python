"""Typed views over the product page settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class ActionButtons(Dto):
    """The ``actions_buttons`` block — which buttons a product page carries."""

    show_product_action_buttons: bool | None = None
    display_add_to_cart_button: bool | None = None
    display_buy_now_button: bool | None = None
    display_on_hover: bool | None = None
    display_add_to_compare_button: bool | None = None
    display_add_to_wishlist_button: bool | None = None


class ProductDetails(Dto):
    """The ``details`` block — which parts of the product's description are shown."""

    display_description: bool | None = None
    display_sale_percentage: bool | None = None
    use_strike_through_on_previous_price: bool | None = None
    display_tax_with_expect_to_pay_price: bool | None = None


class SocialSharing(Dto):
    """The ``social_sharing`` block — share buttons, their networks and the title beside them."""

    enable_share_on_social_media: bool | None = None
    facebook: bool | None = None
    twitter: bool | None = None
    pinterest: bool | None = None
    messenger: bool | None = None
    linkedin: bool | None = None
    email: bool | None = None
    snapchat: bool | None = None
    telegram: bool | None = None
    reddit: bool | None = None
    instagram: bool | None = None
    youtube: bool | None = None
    tiktok: bool | None = None
    threads: bool | None = None
    whatsapp: bool | None = None
    bluesky: bool | None = None
    mastodon: bool | None = None
    copy_link: bool | None = None
    display_title: bool | None = None
    title: str | None = None


class SetProductProperties(Dto):
    """The ``set_product_properties`` block — which physical properties a product page lists."""

    display_height: bool | None = None
    display_width: bool | None = None
    display_length: bool | None = None
    display_weight: bool | None = None
    display_add_to_gift_registry: bool | None = None


class Configuration(Dto):
    """The ``configuration`` section — what the product page itself shows, in four blocks."""

    ENVELOPE_KEY = "configuration"

    actions_buttons: ActionButtons | None = None
    details: ProductDetails | None = None
    social_sharing: SocialSharing | None = None
    set_product_properties: SetProductProperties | None = None


class LabelsAndDisplay(Dto):
    """The ``labels_and_display`` block — how a variation is labelled and drawn."""

    disable_variation_label_for_price: bool | None = None
    display_product_image_as_variation_icons: bool | None = None
    display_selected_variation_value: bool | None = None
    enable_colour_type_variation_image_display: bool | None = None
    use_strike_through_for_out_of_stock_variations: bool | None = None
    enable_single_click_variation_loading: bool | None = None


class VariationType(Dto):
    """One variation type, by ``id`` and ``name``; take the ids from ``field_metadata``."""

    id: int | None = None
    name: str | None = None


class VariationLayout(Dto):
    """The ``layout`` block — how variations are laid out and which price is shown."""

    select_variation_view: bool | None = None
    select_variation_view_type: str | None = None
    display_variation_combinations: bool | None = None
    variation_combinations: list[VariationType | None] | None = None
    variation_price_display_mode: bool | None = None
    variation_price_display_type: str | None = None


class Variations(Dto):
    """The ``variations`` section — how a product's variations are labelled and laid out."""

    ENVELOPE_KEY = "variations"

    labels_and_display: LabelsAndDisplay | None = None
    layout: VariationLayout | None = None


class ImageDisplay(Dto):
    """The ``image_display`` block — how product images are laid out and zoomed."""

    enable_image_slider: bool | None = None
    product_thumbnail_vertical_view: bool | None = None
    product_image_view: bool | None = None
    product_image_view_type: str | None = None
    image_zoom_type: bool | None = None
    zoom_type: str | None = None


class ProductVideo(Dto):
    """The ``video`` block — the video preview and where its thumbnail sits."""

    enable_video_preview: bool | None = None
    display_video_thumbnail_in_first_order: bool | None = None


class ImageAndVideo(Dto):
    """The ``image_and_video`` section — one field of its own beside two blocks."""

    ENVELOPE_KEY = "image_and_video"

    allow_single_file_upload_per_product: bool | None = None
    image_display: ImageDisplay | None = None
    video: ProductVideo | None = None


class ProductListing(Dto):
    """The fields a product listing on this page carries, shared by two sections."""

    number_of_products: int | None = None
    allow_viewers_to_change_display_mode: bool | None = None
    grid_view: bool | None = None
    list_view: bool | None = None
    tabular_view: bool | None = None
    select_display_type: str | None = None
    maximum_number_of_columns_per_row: int | None = None
    maximum_number_of_columns_per_row_list: int | None = None
    short_description: bool | None = None
    display_on_hover: bool | None = None
    display_add_to_cart_button: bool | None = None
    display_add_to_compare_button: bool | None = None
    display_add_to_wishlist_button: bool | None = None
    price: bool | None = None
    show_expect_to_pay_price: bool | None = None
    display_rating: bool | None = None
    display_review_count: bool | None = None


class UpSell(ProductListing):
    """The ``up_sell`` section — the up-sell listing."""

    ENVELOPE_KEY = "up_sell"


class RelatedProducts(ProductListing):
    """The ``related_products`` section — the related-products listing."""

    ENVELOPE_KEY = "related_products"


class ReviewCapabilities(Dto):
    """The ``capabilities`` block — what the review plugin offers; read-only."""

    available: bool | None = None


class ReviewAndRatings(Dto):
    """The ``review_and_ratings`` section — where reviews show and which version renders them."""

    ENVELOPE_KEY = "review_and_ratings"

    capabilities: ReviewCapabilities | None = None
    enable_review_in_tab: bool | None = None
    enable_new_version: bool | None = None


class QuickView(Dto):
    """The ``quick_view`` section — the quick-view popup and what it shows."""

    ENVELOPE_KEY = "quick_view"

    product_quick_view: bool | None = None
    display_product_name: bool | None = None
    display_sku: bool | None = None
    display_product_rating: bool | None = None
    display_product_stock: bool | None = None
    display_product_variation: bool | None = None
    display_product_image: bool | None = None
    display_variation_image: bool | None = None
    display_product_summary: bool | None = None
    display_add_to_cart_button: bool | None = None
    display_add_to_compare_button: bool | None = None
    display_add_to_wishlist_button: bool | None = None


class SectionMeta(Dto):
    """One entry of ``group_meta``; the plugin-backed one adds ``plugin`` and ``available``."""

    kind: str | None = None
    writable: bool | None = None
    plugin: str | None = None
    available: bool | None = None
    ui_label: str | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends."""

    configuration: SectionMeta | None = None
    variations: SectionMeta | None = None
    image_and_video: SectionMeta | None = None
    up_sell: SectionMeta | None = None
    related_products: SectionMeta | None = None
    review_and_ratings: SectionMeta | None = None
    quick_view: SectionMeta | None = None


class ProductPage(Dto):
    """The product page settings; a section arrives under the facade's key too, one level in.
    ``to_map()`` renders the body both ``PATCH`` endpoints take."""

    ENVELOPE_KEY = "product_page"

    configuration: Configuration | None = None
    variations: Variations | None = None
    image_and_video: ImageAndVideo | None = None
    up_sell: UpSell | None = None
    related_products: RelatedProducts | None = None
    review_and_ratings: ReviewAndRatings | None = None
    quick_view: QuickView | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
