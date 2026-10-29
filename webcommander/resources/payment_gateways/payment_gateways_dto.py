"""Typed views over the payment gateway bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class PaymentGatewayReference(Dto):
    """An ``{id, name}`` pair: the gateway's ``zone``, and each audience member it names."""

    id: int | None = None
    name: str | None = None


class PaymentGatewayVisibility(Dto):
    """Who sees the gateway at checkout; the lists fill only under ``type`` ``selected``."""

    type: str | None = None
    customers: list[PaymentGatewayReference | None] | None = None
    customer_groups: list[PaymentGatewayReference | None] | None = None


class PaymentGatewayAllowedFor(Dto):
    """The delivery types the gateway is offered for; ``None`` on gateways without the choice."""

    shipping: bool | None = None
    delivery: bool | None = None
    store_pickup: bool | None = None


class PaymentGatewaySurcharge(Dto):
    """The surcharge block, ``None`` on gateways without one, and its write; ``percent_amount``
    reads ``None`` when no percentage is set."""

    type: str | None = None
    flat_amount: float | None = None
    percent_amount: float | None = None
    # A range's ``from`` is a Python keyword, so each range stays a mapping.
    ranges: list[Any] | None = None


class PaymentGatewayMessages(Dto):
    """The pending and completed messages; a message the gateway's form lacks reads ``None``."""

    pending: str | None = None
    completed: str | None = None


class PaymentGatewayPayPalStandard(Dto):
    """PayPal's ``standard`` credentials."""

    client_id: str | None = None
    client_secret: str | None = None


class PaymentGatewayPayPalClassic(Dto):
    """PayPal's ``classic`` account."""

    email_address: str | None = None


class PaymentGatewayToggle(Dto):
    """A one-key ``{"enabled": ...}`` switch."""

    enabled: bool | None = None


class PaymentGatewayCardProcessor(Dto):
    """The card gateway's processor; the client id and secret read ``********`` when set."""

    type: str | None = None
    mode: str | None = None
    merchant_code: str | None = None
    client_id: str | None = None
    client_secret: str | None = None
    wallet_payment: PaymentGatewayToggle | None = None


class PaymentGatewayCardLogo(Dto):
    """The card logos shown at checkout."""

    type: str | None = None
    cards: list[str] | None = None
    custom_image: Any = None


class PaymentGatewayGooglePay(Dto):
    """Express Checkout's Google Pay block."""

    enabled: bool | None = None
    payment_mode: str | None = None
    merchant_name: str | None = None
    merchant_id: str | None = None
    processor: str | None = None
    secret_key: str | None = None
    public_key: str | None = None
    free_shipping_condition_amount: float | None = None
    shipping_cost: float | None = None


class PaymentGatewayApplePay(Dto):
    """Express Checkout's Apple Pay block."""

    enabled: bool | None = None
    payment_mode: str | None = None
    merchant_identifier: str | None = None
    domain_name: str | None = None
    display_name: str | None = None
    processor: str | None = None
    secret_key: str | None = None
    public_key: str | None = None


class PaymentGatewayExpressPayPal(Dto):
    """Express Checkout's PayPal block."""

    show_installment_amount: bool | None = None


class PaymentGatewaySettings(Dto):
    """The row read's gateway-specific ``settings``, every key any gateway answers; each
    gateway fills its own few and offline gateways answer ``{}``."""

    version: str | None = None
    mode: str | None = None
    standard: PaymentGatewayPayPalStandard | None = None
    classic: PaymentGatewayPayPalClassic | None = None
    processor: PaymentGatewayCardProcessor | None = None
    card_logo: PaymentGatewayCardLogo | None = None
    google_pay: PaymentGatewayGooglePay | None = None
    apple_pay: PaymentGatewayApplePay | None = None
    paypal: PaymentGatewayExpressPayPal | None = None
    show_installment_amount: bool | None = None
    show_in_product_details: bool | None = None
    api_key: str | None = None
    default_term: int | None = None
    amount_per_100_points: float | None = None
    merchant_id: str | None = None
    merchant_secret_key: str | None = None
    image: Any = None


class PaymentGateway(Dto):
    """One gateway: a listing row, and the row path's and every write's body, which add
    ``settings``."""

    ENVELOPE_KEY = "payment_gateway"

    id: int | None = None
    code: str | None = None
    name: str | None = None
    added: bool | None = None
    enabled: bool | None = None
    default: bool | None = None
    promotional: bool | None = None
    zone: PaymentGatewayReference | None = None
    information: str | None = None
    visibility: PaymentGatewayVisibility | None = None
    allowed_for: PaymentGatewayAllowedFor | None = None
    surcharge: PaymentGatewaySurcharge | None = None
    messages: PaymentGatewayMessages | None = None
    settings: PaymentGatewaySettings | None = None


class PaymentGatewayVisibilityInput(Dto):
    """The visibility a write takes: customers and customer groups by id."""

    type: str | None = None
    customers: list[int] | None = None
    customer_groups: list[int] | None = None


class PaymentGatewayInput(Dto):
    """The writable fields, for the ``PUT`` and the ``PATCH``; no envelope. ``zone`` takes a
    zone's id or ``{"id": ...}``; ``code`` and ``promotional`` are read-only."""

    name: str | None = None
    added: bool | None = None
    enabled: bool | None = None
    default: bool | None = None
    zone: int | PaymentGatewayReference | None = None
    information: str | None = None
    visibility: PaymentGatewayVisibilityInput | None = None
    allowed_for: PaymentGatewayAllowedFor | None = None
    surcharge: PaymentGatewaySurcharge | None = None
    messages: PaymentGatewayMessages | None = None
    settings: PaymentGatewaySettings | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block; ``limit`` is the page size applied. ``has_previous``
    is ``True`` past the first page and ``False`` on a page past the end."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class PaymentGatewayPage(Dto):
    """One page of the listing: the rows, without ``settings``, and where they sit."""

    payment_gateways: list[PaymentGateway | None] | None = None
    pagination: Pagination | None = None


class PaymentGatewayCount(Dto):
    """The count sub-path's body, a bare ``{"total": N}``."""

    total: int | None = None
