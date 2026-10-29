"""Typed views over the search settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class ExcludedRecord(Dto):
    """One entry of an ``excluded`` list as a read sends it; a write takes bare ids or these."""

    id: int | None = None
    name: str | None = None


class SearchableContentGroup(Dto):
    """One content type the site search covers, its heading and the rows held out of it."""

    enabled: bool | None = None
    display_heading: str | None = None
    excluded: list[ExcludedRecord] | None = None


class ProductCategoriesContent(SearchableContentGroup):
    """The ``product_categories`` block — the only content group carrying a fourth field."""

    hide_parent_category: bool | None = None


class SearchableContent(Dto):
    """The ``searchable_content`` section — the search box's text and the content it reaches."""

    ENVELOPE_KEY = "searchable_content"

    placeholder_text: str | None = None
    product: SearchableContentGroup | None = None
    product_categories: ProductCategoriesContent | None = None
    blog: SearchableContentGroup | None = None
    other_pages: SearchableContentGroup | None = None


class SearchFieldPriority(Dto):
    """One row of ``search_fields.fields`` — a product field and where it ranks, 1 to 10."""

    field: str | None = None
    priority: int | None = None


class SearchFields(Dto):
    """The ``search_fields`` section — how a query is matched, and against which fields."""

    ENVELOPE_KEY = "search_fields"

    match_keywords_exactly: bool | None = None
    match_full_sentences: bool | None = None
    # No default: a class attribute would shadow ``Dto.fields()``.
    fields: list[SearchFieldPriority | None]


class SynonymGroup(Dto):
    """One group of ``synonyms.groups`` — at least two words a query treats as each other."""

    keywords: list[str] | None = None


class Synonyms(Dto):
    """The ``synonyms`` section; writing it triggers a reindex."""

    ENVELOPE_KEY = "synonyms"

    groups: list[SynonymGroup] | None = None


class SectionMeta(Dto):
    """One entry of ``group_meta``: what a section is, whether it can be written and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block, which only the facade sends."""

    searchable_content: SectionMeta | None = None
    search_fields: SectionMeta | None = None
    synonyms: SectionMeta | None = None


class ReindexStatus(Dto):
    """The bare ``reindex_status`` body — where the Elasticsearch reindex stands."""

    state: str | None = None
    started_at: Any = None
    finished_at: Any = None
    error: Any = None


class SearchSettings(Dto):
    """The search settings, as the facade's body or as one section's body."""

    ENVELOPE_KEY = "search_settings"

    searchable_content: SearchableContent | None = None
    search_fields: SearchFields | None = None
    synonyms: Synonyms | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None
