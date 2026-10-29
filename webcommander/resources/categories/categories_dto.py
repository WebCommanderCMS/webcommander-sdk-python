"""Typed views over the category bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class CategoryReference(Dto):
    """Another record a category points at, read as ``{id, name}``; a write needs only ``id``."""

    id: int | None = None
    name: str | None = None


class CategoryGeneral(Dto):
    """The ``general`` section as read. ``filter_profile`` belongs to a filter plugin and reads
    ``null`` without one; a write naming an ``id`` there is then ``400``, a ``null`` accepted."""

    name: str | None = None
    title: str | None = None
    sku: str | None = None
    url: str | None = None
    heading: str | None = None
    parent_category: CategoryReference | None = None
    filter_profile: Any = None
    layout: CategoryReference | None = None
    summary: str | None = None


class CategoryDescription(Dto):
    """The ``description`` section, the same one field read and written."""

    content: str | None = None


class CategoryImagesMedia(Dto):
    """The ``images_media`` section as read: the two stored images' URLs and the image's alt
    text, each ``""`` when unset."""

    image_url: str | None = None
    image_alt: str | None = None
    background_image_url: str | None = None


class CategorySelectedCustomers(Dto):
    """Who ``available_for: "selected"`` admits, each customer and group read as ``{id, name}``."""

    customers: list[CategoryReference | None] | None = None
    groups: list[CategoryReference | None] | None = None


class CategoryAvailabilityVisibility(Dto):
    """The ``availability_visibility`` section as read; ``password`` is never echoed."""

    available: bool | None = None
    visible: bool | None = None
    available_for: str | None = None
    selected_customers: CategorySelectedCustomers | None = None
    available_on_date_range: bool | None = None
    available_from_date: str | None = None
    available_to_date: str | None = None
    password_protected: bool | None = None
    custom_sorting: bool | None = None
    default_sorting: str | None = None
    disable_tracking: bool | None = None


class CategoryTaxShipping(Dto):
    """The ``tax_shipping`` section, the same eight fields read and written. Naming a
    ``shipping_profile`` sets ``enable_shipping``, and ``enable_shipping: false`` clears it."""

    tax_exempt: bool | None = None
    tax_profile: CategoryReference | None = None
    tax_message: str | None = None
    show_price_with_tax: bool | None = None
    prices_entered_with_tax: bool | None = None
    base_price_rounding: str | None = None
    enable_shipping: bool | None = None
    shipping_profile: CategoryReference | None = None


class CategoryProduct(Dto):
    """One assigned product, as ``assign_products`` reads it."""

    id: int | None = None
    name: str | None = None
    sku: str | None = None


class CategoryAssignProducts(Dto):
    """The ``assign_products`` section as read."""

    products: list[CategoryProduct | None] | None = None


class SectionMeta(Dto):
    """One ``group_meta`` entry; ``href`` is the section's path, the row's id a placeholder."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block the listing, a row read and every whole-row write send."""

    general: SectionMeta | None = None
    description: SectionMeta | None = None
    images_media: SectionMeta | None = None
    availability_visibility: SectionMeta | None = None
    tax_shipping: SectionMeta | None = None
    assign_products: SectionMeta | None = None


class Category(Dto):
    """One category: a listing row, a row read, a whole-row write's answer, or a section's
    answer, which carries that one section alone under ``category``."""

    ENVELOPE_KEY = "category"

    general: CategoryGeneral | None = None
    description: CategoryDescription | None = None
    images_media: CategoryImagesMedia | None = None
    availability_visibility: CategoryAvailabilityVisibility | None = None
    tax_shipping: CategoryTaxShipping | None = None
    assign_products: CategoryAssignProducts | None = None
    id: int | None = None
    #: The number the category was filed under, ``null`` when none.
    transaction_no: str | None = None
    disposable: bool | None = None
    in_trash: bool | None = None
    parent_in_trash: bool | None = None
    created_by: str | None = None
    created_on: str | None = None
    last_updated_by: str | None = None
    last_updated_on: str | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None


class Pagination(Dto):
    """The listing's ten-key ``pagination`` block; ``limit`` is the size the store applied."""

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


class CategoryPage(Dto):
    """One page of the listing, with the ``field_metadata`` block when it was asked for."""

    categories: list[Category | None] | None = None
    group_meta: GroupMeta | None = None
    pagination: Pagination | None = None
    field_metadata: Any = None


class CategoryCount(Dto):
    """The count sub-path's ``{"categories": {"count": N}}``."""

    ENVELOPE_KEY = "categories"

    count: int | None = None


class CategoryGeneralInput(Dto):
    """The writable ``general`` fields. ``name`` is required on a create and is kept by a
    ``PUT`` that omits it; a reference takes ``CategoryReference(id=...)``."""

    name: str | None = None
    title: str | None = None
    sku: str | None = None
    url: str | None = None
    heading: str | None = None
    parent_category: CategoryReference | None = None
    layout: CategoryReference | None = None
    summary: str | None = None


class CategoryImage(Dto):
    """One image upload: a file name and its bytes as base64."""

    filename: str | None = None
    base64: str | None = None


class CategoryImagesMediaInput(Dto):
    """The writable ``images_media`` fields; each image reads back as its ``*_url``, and neither a
    ``null`` nor an empty string removes a stored image."""

    image: CategoryImage | None = None
    image_alt: str | None = None
    background_image: CategoryImage | None = None


class CategorySelectedCustomersInput(Dto):
    """The ids ``available_for: "selected"`` admits; an id no customer or group holds is
    dropped without a refusal."""

    customers: list[int | None] | None = None
    groups: list[int | None] | None = None


class CategoryAvailabilityVisibilityInput(Dto):
    """The writable ``availability_visibility`` fields: the read fields, plus the write-only
    ``password``, with ``selected_customers`` taking ids."""

    available: bool | None = None
    visible: bool | None = None
    available_for: str | None = None
    selected_customers: CategorySelectedCustomersInput | None = None
    available_on_date_range: bool | None = None
    available_from_date: str | None = None
    available_to_date: str | None = None
    password_protected: bool | None = None
    password: str | None = None
    custom_sorting: bool | None = None
    default_sorting: str | None = None
    disable_tracking: bool | None = None


class CategoryAssignProductsInput(Dto):
    """The product ids to assign; a write replaces the whole assignment."""

    products: list[int | None] | None = None


class CategoryInput(Dto):
    """The body every write takes, ``{"category": {<section>: {...}}}``: a create, a ``PUT``, a
    ``PATCH`` and a section ``PATCH`` alike, the last reading only its own section."""

    ENVELOPE_KEY = "category"

    general: CategoryGeneralInput | None = None
    description: CategoryDescription | None = None
    images_media: CategoryImagesMediaInput | None = None
    availability_visibility: CategoryAvailabilityVisibilityInput | None = None
    tax_shipping: CategoryTaxShipping | None = None
    assign_products: CategoryAssignProductsInput | None = None
    transaction_no: str | None = None
