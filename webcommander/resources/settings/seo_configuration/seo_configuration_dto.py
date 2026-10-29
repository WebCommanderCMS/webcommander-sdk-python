"""Typed views over the SEO configuration settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class SeoTemplates(Dto):
    """One content type's block of ``global_store_settings``; its tokens differ per block."""

    disable_indexing: bool | None = None
    title_template: list[str | None] | None = None
    description_template: list[str | None] | None = None


class GlobalStoreSettings(Dto):
    """The ``global_store_settings`` section — the store name, separator and template blocks."""

    ENVELOPE_KEY = "global_store_settings"

    store_name: str | None = None
    title_separator: str | None = None
    pages: SeoTemplates | None = None
    products: SeoTemplates | None = None
    categories: SeoTemplates | None = None


class CustomCodeBlock(Dto):
    """The ``header`` or ``footer`` block of ``custom_code``; ``code`` is served on every page."""

    enabled: bool | None = None
    code: str | None = None


class CustomCode(Dto):
    """The ``custom_code`` section — the two blocks whose ``code`` reaches every storefront page."""

    ENVELOPE_KEY = "custom_code"

    header: CustomCodeBlock | None = None
    footer: CustomCodeBlock | None = None


class Redirect(Dto):
    """One redirect row; a listing sends rows under ``items`` with no envelope."""

    ENVELOPE_KEY = "redirect"

    id: int | None = None
    source_url: str | None = None
    destination_url: str | None = None


class RedirectsPreview(Dto):
    """The ``redirects`` rows inlined in ``url_settings``, with no ``pagination``."""

    items: list[Redirect | None] | None = None


class UrlSettings(Dto):
    """The ``url_settings`` section — URL rewriting on rename, and the redirects it leaves."""

    ENVELOPE_KEY = "url_settings"

    regenerate_url_on_item_update: bool | None = None
    auto_redirect_on_url_change: bool | None = None
    redirects: RedirectsPreview | None = None


class DocumentRootFile(Dto):
    """One file served from the document root; ``config_key`` is the id the delete takes."""

    ENVELOPE_KEY = "document_root_file"

    config_key: str | None = None
    file_name: str | None = None
    file_path: str | None = None


class DocumentRootPreview(Dto):
    """The ``document_root`` rows the facade inlines, with no ``pagination``."""

    items: list[DocumentRootFile | None] | None = None


class SectionMeta(Dto):
    """One ``group_meta`` entry; ``redirects`` nests inside the ``url_settings`` one."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None
    redirects: SectionMeta | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends."""

    global_store_settings: SectionMeta | None = None
    custom_code: SectionMeta | None = None
    document_root: SectionMeta | None = None
    url_settings: SectionMeta | None = None


class SeoConfiguration(Dto):
    """The SEO configuration, as the facade's body or as one section's body."""

    ENVELOPE_KEY = "seo_configuration"

    global_store_settings: GlobalStoreSettings | None = None
    custom_code: CustomCode | None = None
    document_root: DocumentRootPreview | None = None
    url_settings: UrlSettings | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
