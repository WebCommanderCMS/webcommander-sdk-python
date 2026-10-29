"""Typed views over the customer group bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class CustomerGroupShippingProfile(Dto):
    """The shipping profile a group names; a write sends the bare ``id``, not this record."""

    id: int | None = None
    name: str | None = None


class CustomerGroupBackgroundImage(Dto):
    """The stored image; a write sends a base64 or ``data:`` URI string, and ``null`` removes it."""

    url: str | None = None
    width: int | None = None
    height: int | None = None


class CustomerGroupAmountSetting(Dto):
    """An ``enabled`` switch and its ``amount``: ``minimum_purchase``, ``max_purchase`` and
    ``credit_limit`` all take this shape."""

    enabled: bool | None = None
    amount: float | None = None


class CustomerGroupPaymentTerms(Dto):
    """``terms`` is written ``NET_30``, ``NET_60`` or ``NET_90`` and reads back in lower case."""

    enabled: bool | None = None
    terms: str | None = None


class CustomerGroupOnAccountPurchase(Dto):
    enabled: bool | None = None
    max_purchase: CustomerGroupAmountSetting | None = None
    credit_limit: CustomerGroupAmountSetting | None = None
    payment_terms: CustomerGroupPaymentTerms | None = None


class CustomerGroupPurchasePreference(Dto):
    minimum_purchase: CustomerGroupAmountSetting | None = None
    on_account_purchase: CustomerGroupOnAccountPurchase | None = None


class CustomerGroupTaxConfiguration(Dto):
    """``base_price_rounding`` is ``nearest``, ``up`` or ``down``."""

    override_store_tax: bool | None = None
    tax_exempt: bool | None = None
    tax_message: str | None = None
    show_prices_with_tax_included: bool | None = None
    prices_entered_with_tax_included: bool | None = None
    base_price_rounding: str | None = None


class CustomerGroupProductDisplay(Dto):
    """``price_display_method`` is ``lowest`` or ``highest``."""

    overwrite_default: bool | None = None
    variation_display_type: str | None = None
    display_parent_image: bool | None = None
    activate_colour_variation_image: bool | None = None
    show_selected_variation_value: bool | None = None
    strike_through_out_of_stock: bool | None = None
    single_click_variation_loading: bool | None = None
    price_display_method: str | None = None


class CustomerGroupMember(Dto):
    """One member, by its ``customer_id``: an entry of ``customers`` and the membership read."""

    ENVELOPE_KEY = "customer"

    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class CustomerGroup(Dto):
    """One group. A listing row and a create, patch or assign answer carry the thirteen fields
    up to ``updated_at``; the row read and the membership write add the last two."""

    ENVELOPE_KEY = "customer_group"

    id: int | None = None
    name: str | None = None
    description: str | None = None
    status: str | None = None
    default_tax_code: str | None = None
    add_as_new_customer_default_group: bool | None = None
    shipping_profile: CustomerGroupShippingProfile | None = None
    background_image: CustomerGroupBackgroundImage | None = None
    purchase_preference: CustomerGroupPurchasePreference | None = None
    tax_configuration: CustomerGroupTaxConfiguration | None = None
    product_display: CustomerGroupProductDisplay | None = None
    created_at: str | None = None
    updated_at: str | None = None
    customer_count: int | None = None
    customers: list[CustomerGroupMember | None] | None = None
    field_metadata: Any = None


class Pagination(Dto):
    """The five-key ``pagination`` block; ``limit`` is the page size applied."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class CustomerGroupPage(Dto):
    customer_groups: list[CustomerGroup | None] | None = None
    pagination: Pagination | None = None
    field_metadata: Any = None


class CustomerGroupCount(Dto):
    """The count sub-path's body, a bare ``{"total": N}``."""

    total: int | None = None


class CustomerGroupAssignment(Dto):
    """The assign answer: ``added`` is ``false`` when the customer was already a member."""

    status: str | None = None
    customer_id: int | None = None
    email: str | None = None
    group: CustomerGroup | None = None
    added: bool | None = None


class CustomerGroupInput(Dto):
    """The writable form of :class:`CustomerGroup`, for the create and the patch. ``status`` takes
    ``A``, ``I``, ``active`` or ``inactive``; ``shipping_profile`` is a bare id."""

    ENVELOPE_KEY = "customer_group"

    name: str | None = None
    description: str | None = None
    status: str | None = None
    default_tax_code: str | None = None
    add_as_new_customer_default_group: bool | None = None
    shipping_profile: int | None = None
    background_image: str | None = None
    purchase_preference: CustomerGroupPurchasePreference | None = None
    tax_configuration: CustomerGroupTaxConfiguration | None = None
    product_display: CustomerGroupProductDisplay | None = None


class CustomerGroupCustomersInput(Dto):
    """The membership body: the whole member list, replacing the stored one; ``[]`` empties it."""

    customers: list[int | str] | None = None


class CustomerGroupAssignInput(Dto):
    """The assign body, both ids bare: ``customer`` is a ``customer_id``."""

    customer: int | str | None = None
    group: int | str | None = None
