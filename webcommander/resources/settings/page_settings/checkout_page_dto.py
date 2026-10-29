"""Typed views over the checkout page settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class AddressField(Dto):
    """One entry of an address section's ``fields`` — a form field and how it is drawn."""

    key: str | None = None
    label: str | None = None
    active: bool | None = None
    required: bool | None = None
    order: int | None = None
    group: str | None = None


class AddressForm(Dto):
    """An address section: the facade sends ``active_fields``, the section endpoint ``fields``."""

    active_fields: list[str] | None = None
    # No default: a class attribute would shadow ``Dto.fields()``.
    fields: list[AddressField | None]


class BillingAddress(AddressForm):
    """The ``billing_address`` section — read, never written: ``group_meta`` marks it read-only."""

    ENVELOPE_KEY = "billing_address"


class ShippingAddress(AddressForm):
    """The ``shipping_address`` section — read, never written: ``group_meta`` marks it read-only."""

    ENVELOPE_KEY = "shipping_address"


class SignUp(Dto):
    """The ``allow_sign_up`` block — whether an account may, or must, be created at checkout."""

    enabled: bool | None = None
    required: bool | None = None


class GuestCheckout(Dto):
    """The ``checkout_as_guest`` block — ordering without an account, and the one-click sign-up."""

    enabled: bool | None = None
    quick_signup: bool | None = None


class CustomerCheckout(Dto):
    """The ``customer_checkout`` section; leaving all three sign-in routes off is ``400``."""

    ENVELOPE_KEY = "customer_checkout"

    allow_sign_in: bool | None = None
    allow_sign_up: SignUp | None = None
    checkout_as_guest: GuestCheckout | None = None
    newsletter_subscription: bool | None = None
    multiple_shipping_methods: bool | None = None


class DeliveryOptions(Dto):
    """The ``delivery_options`` section; leaving all four choices off is ``400``."""

    ENVELOPE_KEY = "delivery_options"

    enable_shipping: bool | None = None
    enable_store_pickup: bool | None = None
    enable_shipping_quote: bool | None = None
    enable_delivery_service: bool | None = None


class OrderSummary(Dto):
    """The ``order_summary`` section — what the checkout's summary panel shows."""

    ENVELOPE_KEY = "order_summary"

    show_product_thumbnail: bool | None = None
    show_quantity: bool | None = None
    enable_payment_expand_view: bool | None = None
    order_confirm_captcha: bool | None = None


class OrderComment(Dto):
    """The ``comment`` block — whether an order may carry a comment, and whether staff are told."""

    enabled: bool | None = None
    send_notification: bool | None = None


class TermsReference(Dto):
    """The ``terms_and_condition.ref`` block; the body carries the one key matching ``type``."""

    page: Any = None
    link: str | None = None
    text: str | None = None


class TermsAndCondition(Dto):
    """The ``terms_and_condition`` block — whether terms must be accepted, and where they live."""

    enabled: bool | None = None
    text: str | None = None
    link_label: str | None = None
    type: str | None = None
    ref: TermsReference | None = None


class Others(Dto):
    """The ``others`` section — the checkout page's logo, login link, own HTML and two blocks."""

    ENVELOPE_KEY = "others"

    show_logo: bool | None = None
    login_url: str | None = None
    custom_html: str | None = None
    comment: OrderComment | None = None
    terms_and_condition: TermsAndCondition | None = None


class SectionMeta(Dto):
    """One entry of ``group_meta``: what a section is, whether it can be written and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends."""

    billing_address: SectionMeta | None = None
    shipping_address: SectionMeta | None = None
    customer_checkout: SectionMeta | None = None
    delivery_options: SectionMeta | None = None
    order_summary: SectionMeta | None = None
    others: SectionMeta | None = None


class CheckoutPage(Dto):
    """The checkout page settings, as the facade's body or as one section's body."""

    ENVELOPE_KEY = "checkout_page"

    billing_address: BillingAddress | None = None
    shipping_address: ShippingAddress | None = None
    customer_checkout: CustomerCheckout | None = None
    delivery_options: DeliveryOptions | None = None
    order_summary: OrderSummary | None = None
    others: Others | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
