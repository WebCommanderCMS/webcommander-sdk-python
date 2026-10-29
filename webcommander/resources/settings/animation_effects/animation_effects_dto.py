"""Typed views over the animation effects bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class CustomLoader(Dto):
    """The uploaded loader behind ``enable_custom_preloader``; read-only."""

    enabled: bool | None = None
    file_name: str | None = None
    file_url: str | None = None


class PreloaderPage(Dto):
    """One entry of ``preloader_custom_page`` as a read sends it; a write takes page ids."""

    id: int | None = None
    name: str | None = None


class PreloaderDesign(Dto):
    """The ``preloader_design`` section — the page-load loader, and when and where it shows."""

    ENVELOPE_KEY = "preloader_design"

    enable_preloader: bool | None = None
    enable_custom_preloader: bool | None = None
    preloader_preset: str | None = None
    preloader_size: int | None = None
    preloader_background_opacity: float | None = None
    background_preloader: str | None = None
    preloader_hide_condition: str | None = None
    preloader_show_time_condition: str | None = None
    preloader_hide_after_time: float | None = None
    preloader_page: str | None = None
    preloader_custom_page: list[PreloaderPage] | None = None
    custom_loader: CustomLoader | None = None


class WidgetTransition(Dto):
    """The ``widget_transition`` section — whether widgets fade in, and over how long."""

    ENVELOPE_KEY = "widget_transition"

    widget_smooth_render: bool | None = None
    widget_smooth_render_duration: int | None = None


class PageTransition(Dto):
    """The ``page_transition`` section — the animation between pages and when it plays."""

    ENVELOPE_KEY = "page_transition"

    page_transition_animation_type: str | None = None
    transition_animation_duration: float | None = None
    animation_before_entering_new_page: bool | None = None
    animation_after_entering_new_page: bool | None = None


class ImageLazyEffect(Dto):
    """The ``image_lazy_effect`` section — which pages lazy-load images, and the placeholder."""

    ENVELOPE_KEY = "image_lazy_effect"

    preloader_image_lazy_effect_preset: str | None = None
    product_details_page_image_lazy_effect: bool | None = None
    flying_cart_image_lazy_effect: bool | None = None
    product_list_image_lazy_effect: bool | None = None
    property_list_image_lazy_effect: bool | None = None
    property_details_page_image_lazy_effect: bool | None = None
    blog_list_image_lazy_effect: bool | None = None
    blog_details_page_image_lazy_effect: bool | None = None
    lazy_loader_size: int | None = None
    background_lazy_loader: str | None = None
    content_image_lazy_load_background: str | None = None


class PageSkeleton(Dto):
    """The ``page_skeleton`` section — one field."""

    ENVELOPE_KEY = "page_skeleton"

    checkout_page_skeleton: bool | None = None


class SectionMeta(Dto):
    """One entry of ``group_meta``: what a section is, whether it can be written and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends."""

    preloader_design: SectionMeta | None = None
    widget_transition: SectionMeta | None = None
    page_transition: SectionMeta | None = None
    image_lazy_effect: SectionMeta | None = None
    page_skeleton: SectionMeta | None = None


class AnimationEffects(Dto):
    """The animation effects settings, as the facade's body or as one section's body."""

    ENVELOPE_KEY = "animation_effects"

    preloader_design: PreloaderDesign | None = None
    widget_transition: WidgetTransition | None = None
    page_transition: PageTransition | None = None
    image_lazy_effect: ImageLazyEffect | None = None
    page_skeleton: PageSkeleton | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
