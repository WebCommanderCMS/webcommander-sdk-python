"""Typed views over the customer portal bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class CustomerGroup(Dto):
    """One entry of ``default_groups`` or ``approval_groups``; a write takes bare ids instead."""

    id: int | None = None
    name: str | None = None


class Portal(Dto):
    """The ``portal`` section — the one switch that turns the customer portal on."""

    ENVELOPE_KEY = "portal"

    enabled: bool | None = None


class RegistrationTerms(Dto):
    """The ``terms`` block; enabling it while ``reference`` is null is ``400``."""

    enabled: bool | None = None
    text: str | None = None
    anchor_text: str | None = None
    type: str | None = None
    reference: str | None = None


class FacebookLogin(Dto):
    """The ``facebook`` block; ``app_id`` is required when ``enabled``."""

    enabled: bool | None = None
    app_id: str | None = None


class GoogleLogin(Dto):
    """The ``google`` block; ``client_id`` is required when ``enabled``."""

    enabled: bool | None = None
    client_id: str | None = None


class B2bConfiguration(Dto):
    """The ``b2b_configuration`` block — what a new registrant is created as. Four booleans."""

    enabled: bool | None = None
    create_as_organisation: bool | None = None
    create_as_customer: bool | None = None
    organisation_selected: bool | None = None


class AlternateLogin(Dto):
    """The ``alternate_login`` block — third-party login and whether it offers an email field."""

    enabled: bool | None = None
    enable_email_field: bool | None = None


class Registration(Dto):
    """The ``registration`` section — who may register, as what, and what they must accept."""

    ENVELOPE_KEY = "registration"

    enabled: bool | None = None
    close_registration_message: str | None = None
    assign_default_group: bool | None = None
    default_groups: list[CustomerGroup] | None = None
    requires_approval: bool | None = None
    approval_groups: list[CustomerGroup] | None = None
    terms: RegistrationTerms | None = None
    facebook: FacebookLogin | None = None
    google: GoogleLogin | None = None
    b2b_configuration: B2bConfiguration | None = None
    alternate_login: AlternateLogin | None = None


class LoginCaptcha(Dto):
    """The ``captcha`` block — the challenge shown after failed logins."""

    enabled: bool | None = None
    fail_count: int | None = None


class Login(Dto):
    """The ``login`` section — whether customers may sign in and what the sign-in page offers."""

    ENVELOPE_KEY = "login"

    enabled: bool | None = None
    login_disabled_message: str | None = None
    awaiting_approval_message: str | None = None
    password_recovery: bool | None = None
    registration_link: bool | None = None
    captcha: LoginCaptcha | None = None
    enable_landing_page_after_successful_login: bool | None = None
    landing_page_after_successful_login: str | None = None


class AzureAdDataMapping(Dto):
    """The ``azure_ad.data_mapping`` block — the assertion attribute for each customer field."""

    address_line_1: str | None = None
    address_line_2: str | None = None
    post_code: str | None = None
    phone: str | None = None
    mobile: str | None = None
    country_id: int | None = None
    state: str | None = None
    city: str | None = None


class AzureAd(Dto):
    """The ``azure_ad`` block — the SAML provider."""

    data_mapping: AzureAdDataMapping | None = None
    identifier: str | None = None
    login_url: str | None = None
    reply_url_postfix: str | None = None


class AzureAdB2c(Dto):
    """The ``azure_ad_b2c`` block — the B2C provider, carrying ``client_secret``."""

    tenant_name: str | None = None
    policy_name: str | None = None
    client_id: str | None = None
    client_secret: str | None = None
    reply_url_prefix: str | None = None
    reply_url_postfix: str | None = None


class Sso(Dto):
    """The ``sso`` section; turning ``enabled`` on demands the whole ``azure_ad_b2c`` block."""

    ENVELOPE_KEY = "sso"

    enabled: bool | None = None
    require_site_access: bool | None = None
    service_provider: str | None = None
    azure_ad: AzureAd | None = None
    azure_ad_b2c: AzureAdB2c | None = None


class ProfileField(Dto):
    """One row of an address or account form on the profile page."""

    key: str | None = None
    active: bool | None = None
    order: int | None = None


class ProfileEntry(ProfileField):
    """One row of a named list on the profile page — a tab, a section or an entitlement."""

    label: str | None = None


class ProfileOverviewEntry(ProfileEntry):
    """One row of ``overview``; only some rows carry ``show_product_info``."""

    show_product_info: bool | None = None


class ManageMyAccount(Dto):
    """The ``manage_my_account`` block — the account screen's sections and form fields."""

    sections: list[ProfileEntry] | None = None
    account_information: list[ProfileField] | None = None
    billing_address: list[ProfileField] | None = None
    shipping_address: list[ProfileField] | None = None


class MyOrderFlags(Dto):
    """The ``my_orders.flags`` block — six booleans."""

    enable_due_payment: bool | None = None
    show_track_my_orders: bool | None = None
    display_track_in_column: bool | None = None
    show_order_channel: bool | None = None
    show_pay_now: bool | None = None
    allow_order_share: bool | None = None


class MyOrders(Dto):
    """The ``my_orders`` block — what the orders tab shows and which order lists it offers."""

    flags: MyOrderFlags | None = None
    sections: list[ProfileEntry] | None = None


class AssignToCustomer(Dto):
    """The ``assign_to_customer`` block — the assigned-pages tab and how it paginates."""

    items: list[ProfileEntry] | None = None
    show_pagination: str | None = None
    item_per_page: int | None = None


class ProfilePage(Dto):
    """The ``profile_page`` section — read, never written: ``group_meta`` marks it read-only."""

    ENVELOPE_KEY = "profile_page"

    page_html: str | None = None
    tabs: list[ProfileEntry] | None = None
    overview: list[ProfileOverviewEntry] | None = None
    manage_my_account: ManageMyAccount | None = None
    my_orders: MyOrders | None = None
    my_entitlements: list[ProfileEntry] | None = None
    assign_to_customer: AssignToCustomer | None = None


class RegistrationField(Dto):
    """One row of the registration form's field catalog."""

    key: str | None = None
    label: str | None = None
    default_label: str | None = None
    active: bool | None = None
    required: bool | None = None
    system: bool | None = None
    order: int | None = None
    placeholder: str | None = None


class RegistrationFields(Dto):
    """The ``registration_fields`` section, read and never written."""

    ENVELOPE_KEY = "registration_fields"

    # No default: a class attribute would shadow ``Dto.fields()``.
    fields: list[RegistrationField | None]


class SectionMeta(Dto):
    """One entry of ``group_meta``: what a section is, whether it can be written and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends."""

    portal: SectionMeta | None = None
    registration: SectionMeta | None = None
    login: SectionMeta | None = None
    sso: SectionMeta | None = None
    profile_page: SectionMeta | None = None
    registration_fields: SectionMeta | None = None


class CustomerPortal(Dto):
    """The customer portal settings, as the facade's body or as one section's body."""

    ENVELOPE_KEY = "customer_portal"

    portal: Portal | None = None
    registration: Registration | None = None
    login: Login | None = None
    sso: Sso | None = None
    profile_page: ProfilePage | None = None
    registration_fields: RegistrationFields | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
