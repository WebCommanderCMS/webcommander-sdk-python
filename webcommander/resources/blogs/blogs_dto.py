"""Typed views over the blog and blog comment bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class BlogCategoryReference(Dto):
    """A category a blog is filed under; a write names it ``{"id": …}``, a bare number ``500``."""

    id: int | None = None
    name: str | None = None
    is_disposable: bool | None = None
    is_in_trash: bool | None = None


class BlogImage(Dto):
    """The cover image, ``{}`` when there is none."""

    title: str | None = None
    alternative_text: str | None = None
    file_name: str | None = None
    link: str | None = None


class BlogImageInput(Dto):
    """The cover image a write uploads; without ``base64`` the stored image is left as it was."""

    file_name: str | None = None
    base64: str | None = None
    title: str | None = None
    alternative_text: str | None = None


class BlogAuthor(Dto):
    """``created_by``; ``{}`` on a row the store recorded no author for."""

    id: int | None = None
    name: str | None = None


class BlogAudienceMember(Dto):
    """One customer, by ``internal_id``, or one customer group a restricted blog is shown to."""

    id: int | None = None
    name: str | None = None


class BlogAudience(Dto):
    """``selected_customers`` once it names anyone; the store sends ``[]`` when it names no one."""

    customers: list[BlogAudienceMember | None] | None = None
    groups: list[BlogAudienceMember | None] | None = None


class BlogAudienceInput(Dto):
    """The audience a write names: customer ``internal_id`` values and customer group ids. A
    ``customer_id`` is dropped without a refusal."""

    customers: list[int | None] | None = None
    groups: list[int | None] | None = None


class BlogMetaTag(Dto):
    """One ``meta_tag`` entry, the same two fields on a write and a read."""

    name: str | None = None
    value: str | None = None


class BlogSeoConfigs(Dto):
    """``seo_configs``, an object holding the ``meta_tag`` list."""

    meta_tag: list[BlogMetaTag | None] | None = None


class ResourceMeta(Dto):
    """The one ``group_meta`` entry: what the collection is, whether it is writable and where."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The ``group_meta`` block the listing, a row read and a ``PATCH`` answer carry."""

    blogs: ResourceMeta | None = None


class Blog(Dto):
    """One blog, the same eighteen fields on a listing row, a row read and every write's answer.
    ``url`` is the title's slug on the create; a later write naming ``title`` takes a sent one."""

    ENVELOPE_KEY = "blog"

    id: int | None = None
    #: A UUID string the store assigns; a create naming it is ``400 unknown_field``.
    uuid: str | None = None
    title: str | None = None
    url: str | None = None
    content: str | None = None
    date: str | None = None
    is_published: bool | None = None
    visibility: str | None = None
    visible_to: str | None = None
    categories: list[BlogCategoryReference | None] | None = None
    created_on: str | None = None
    last_updated_on: str | None = None
    is_disposable: bool | None = None
    is_in_trash: bool | None = None
    image: BlogImage | None = None
    created_by: BlogAuthor | None = None
    selected_customers: BlogAudience | None = None
    seo_configs: BlogSeoConfigs | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None


class BlogInput(Dto):
    """The writable form of :class:`Blog`, for the create, the replace and the patch. ``title``
    is required by the first two and ``visibility`` by the replace."""

    ENVELOPE_KEY = "blog"

    title: str | None = None
    content: str | None = None
    date: str | None = None
    is_published: bool | None = None
    visibility: str | None = None
    visible_to: str | None = None
    categories: list[BlogCategoryReference | None] | None = None
    image: BlogImageInput | None = None
    seo_configs: BlogSeoConfigs | None = None
    selected_customers: BlogAudienceInput | None = None


class Pagination(Dto):
    """The ten-key ``pagination`` block; ``limit`` is the size the store applied, capped at 20."""

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


class BlogPage(Dto):
    """One page of the listing: the rows, ``group_meta``, the paging block and any schema."""

    blogs: list[Blog | None] | None = None
    group_meta: GroupMeta | None = None
    pagination: Pagination | None = None
    field_metadata: Any = None


class BlogCount(Dto):
    """The count sub-path's body, ``{"blogs": {"count": N}}``."""

    ENVELOPE_KEY = "blogs"

    count: int | None = None


class BlogComment(Dto):
    """One comment, the same twelve fields in the listing and on its own path. ``post_title``
    is the blog's current title; no write on this surface adds to ``replies``."""

    id: int | None = None
    status: str | None = None
    name: str | None = None
    email: str | None = None
    post_title: str | None = None
    content: str | None = None
    spam: bool | None = None
    likes: int | None = None
    total_reply: int | None = None
    created_on: str | None = None
    last_updated_on: str | None = None
    replies: list[Any] | None = None


class BlogCommentList(Dto):
    """The comments sub-path's body: the blog's ``id`` beside every comment it holds, unpaged."""

    id: int | None = None
    comments: list[BlogComment | None] | None = None


class BlogCommentEnvelope(Dto):
    """One comment's body, from its own path and from each comment write: the blog's ``id``
    beside the ``comment``."""

    id: int | None = None
    comment: BlogComment | None = None


class BlogCommentDraft(Dto):
    """The comment a create sends: ``content`` required, at most 1000 characters; ``name``, 2
    to 100 once trimmed, and ``email`` may be left out."""

    content: str | None = None
    name: str | None = None
    email: str | None = None


class BlogCommentInput(Dto):
    """The comment create's body, ``{"blog": {"comment": {...}}}``."""

    ENVELOPE_KEY = "blog"

    comment: BlogCommentDraft | None = None
