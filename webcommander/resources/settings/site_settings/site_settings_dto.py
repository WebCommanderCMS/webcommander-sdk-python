"""Typed views over the site settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class Region(Dto):
    """A country or a state as a read sends it; a write may send a bare id, code or name instead."""

    id: int | None = None
    code: str | None = None
    name: str | None = None


class AutoSuggestAddresses(Dto):
    """The ``auto_suggest.addresses`` block."""

    enabled: bool | None = None
    validate: bool | None = None


class AutoSuggest(Dto):
    """The ``auto_suggest`` block — address and suburb suggestions."""

    addresses: AutoSuggestAddresses | None = None
    suburbs_cities: bool | None = None


class Captcha(Dto):
    """The ``captcha`` block; both private keys read back as ``***``."""

    enabled: bool | None = None
    minimum_score: float | None = None
    private_key: str | None = None
    private_key_turnstile: str | None = None
    private_key_v3: str | None = None
    public_key: str | None = None
    public_key_turnstile: str | None = None
    public_key_v3: str | None = None
    type: str | None = None
    use_own: bool | None = None
    version: str | None = None


class Administration(Dto):
    """The ``administration`` section — units, precision, default region and error pages."""

    ENVELOPE_KEY = "administration"

    auto_suggest: AutoSuggest | None = None
    captcha: Captcha | None = None
    default_country: Region | None = None
    default_state: Region | None = None
    ecommerce_enabled: bool | None = None
    max_precision: int | None = None
    page_403: str | None = None
    page_404: str | None = None
    unit_length: str | None = None
    unit_weight: str | None = None


class BrandColors(Dto):
    """The ``brand_kit.colors`` block — six roles, each a hex colour the store validates."""

    accent: str | None = None
    background: str | None = None
    primary: str | None = None
    secondary: str | None = None
    surface: str | None = None
    text: str | None = None


class BrandKit(Dto):
    """The ``brand_kit`` section — the site-wide palette."""

    ENVELOPE_KEY = "brand_kit"

    colors: BrandColors | None = None
    enabled: bool | None = None
    palette_name: str | None = None


class DateTimeFormat(Dto):
    """The three fields every ``date_time`` audience block carries."""

    date_format: str | None = None
    time_format: str | None = None
    time_zone: str | None = None


class AdminDateTime(DateTimeFormat):
    """The ``date_time.admin`` block, the only one carrying ``first_day_of_week``."""

    first_day_of_week: str | None = None


class SeparableDateTime(DateTimeFormat):
    """The ``date_time.email`` and ``date_time.user`` blocks, each with a ``separate`` flag."""

    separate: bool | None = None


class DateTime(Dto):
    """The ``date_time`` section — formats and zones for admin, email and the storefront."""

    ENVELOPE_KEY = "date_time"

    admin: AdminDateTime | None = None
    email: SeparableDateTime | None = None
    hide_time_zone: bool | None = None
    user: SeparableDateTime | None = None


class Maintenance(Dto):
    """The ``maintenance`` block — whether the storefront is closed and what it says."""

    enabled: bool | None = None
    message: str | None = None


class SecurityCode(Dto):
    """The ``security_code`` block — the site lock; ``code`` reads back masked once set."""

    code: str | None = None
    enabled: bool | None = None
    number_only: bool | None = None


class SslKeyFile(Dto):
    """The ``ssl.key_file`` block — what is stored for the private key, never the key itself."""

    file_name: str | None = None
    uploaded: bool | None = None


class SslCertificateFile(SslKeyFile):
    """The ``ssl.certificate_file`` block, with the certificate's subject and expiry."""

    expires_at: str | None = None
    subject: str | None = None


class Ssl(Dto):
    """The ``ssl`` block; its read form and its write form share no key."""

    certificate_file: SslCertificateFile | None = None
    key_file: SslKeyFile | None = None


class DomainSettings(Dto):
    """The ``domain_settings`` section; ``aliases`` is read-only here."""

    ENVELOPE_KEY = "domain_settings"

    aliases: list[str] | None = None
    https_enabled: bool | None = None
    maintenance: Maintenance | None = None
    security_code: SecurityCode | None = None
    ssl: Ssl | None = None
    website_address: str | None = None


class EmailProvider(Dto):
    """One entry of ``available`` — a provider the store can send through."""

    key: str | None = None
    label: str | None = None
    type: str | None = None
    connect_url: str | None = None


class ReplyTo(Dto):
    """A ``reply`` block — where replies go when not to the sender address."""

    different: bool | None = None
    to_email: str | None = None
    to_name: str | None = None


class DefaultDomain(Dto):
    """One entry of ``default.domains`` — a platform sending domain and the sender used on it."""

    configure: bool | None = None
    domain: str | None = None
    email_prefix: str | None = None
    reply: ReplyTo | None = None
    sender_name: str | None = None


class DefaultEmail(Dto):
    """The ``default`` block — the platform's own sending domains."""

    domains: list[DefaultDomain] | None = None


class OauthProvider(Dto):
    """The ``gmail`` and ``office365`` blocks, each set through its interactive ``connect_url``."""

    connect_url: str | None = None


class SendGrid(Dto):
    """The ``sendgrid`` block; ``api_key`` reads back as ``***``, so never echo it into a write."""

    api_key: str | None = None
    reply: ReplyTo | None = None
    sender_email: str | None = None
    sender_name: str | None = None


class SmtpAuthentication(Dto):
    """The ``smtp.authentication`` block; ``password`` reads back as ``***``."""

    enabled: bool | None = None
    password: str | None = None
    username: str | None = None


class Smtp(Dto):
    """The ``smtp`` block — the server the store sends through and who it sends as."""

    authentication: SmtpAuthentication | None = None
    encryption: str | None = None
    host: str | None = None
    port: int | None = None
    sender_email: str | None = None
    sender_name: str | None = None


class EmailSettings(Dto):
    """The ``email_settings`` section — each mail provider and its credentials."""

    ENVELOPE_KEY = "email_settings"

    available: list[EmailProvider] | None = None
    default: DefaultEmail | None = None
    gmail: OauthProvider | None = None
    office365: OauthProvider | None = None
    sendgrid: SendGrid | None = None
    service_provider: str | None = None
    smtp: Smtp | None = None


class MediaImage(Dto):
    """The ``image`` record of a media section — the stored file and where it is served."""

    content_type: str | None = None
    file_name: str | None = None
    height: int | None = None
    size_bytes: int | None = None
    url: str | None = None
    width: int | None = None


class Favicon(Dto):
    """The ``favicon`` section — ``kind: "media"``, read and never written."""

    ENVELOPE_KEY = "favicon"

    enabled: bool | None = None
    image: MediaImage | None = None


class StoreLogoVariants(Dto):
    """The ``store_logo.variants`` block — the logos for dark backgrounds and the sticky header."""

    # Both read null while the main logo is used; a set variant's shape has not been measured.
    dark_background: Any = None
    sticky_header: Any = None


class StoreLogo(Dto):
    """The ``store_logo`` section — ``kind: "media"``, read and never written."""

    ENVELOPE_KEY = "store_logo"

    image: MediaImage | None = None
    variants: StoreLogoVariants | None = None


class StoreAddress(Dto):
    """The ``store_details.address`` block — where the business is."""

    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    country: Region | None = None
    post_code: str | None = None
    state: Region | None = None


class StoreContact(Dto):
    """The ``store_details.contact`` block — the three numbers the store publishes."""

    fax: str | None = None
    mobile: str | None = None
    phone: str | None = None


class StoreDetails(Dto):
    """The ``store_details`` section — ``kind: "resource"``, every field writable."""

    ENVELOPE_KEY = "store_details"

    abn: str | None = None
    address: StoreAddress | None = None
    company_name: str | None = None
    contact: StoreContact | None = None
    email: str | None = None


class SectionMeta(Dto):
    """One entry of ``group_meta``: what a section is, whether it can be written and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends."""

    administration: SectionMeta | None = None
    brand_kit: SectionMeta | None = None
    date_time: SectionMeta | None = None
    domain_settings: SectionMeta | None = None
    email_settings: SectionMeta | None = None
    favicon: SectionMeta | None = None
    store_details: SectionMeta | None = None
    store_logo: SectionMeta | None = None


class SiteSettings(Dto):
    """The site settings, as the facade's body or as one section's body."""

    ENVELOPE_KEY = "site_settings"

    administration: Administration | None = None
    brand_kit: BrandKit | None = None
    date_time: DateTime | None = None
    domain_settings: DomainSettings | None = None
    email_settings: EmailSettings | None = None
    favicon: Favicon | None = None
    store_details: StoreDetails | None = None
    store_logo: StoreLogo | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
