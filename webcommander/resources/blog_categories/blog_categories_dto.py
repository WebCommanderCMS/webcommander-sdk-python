"""Typed views over the blog category bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class BlogCategoryImage(Dto):
    """A category's ``image``, ``{}`` until one is uploaded."""

    title: str | None = None
    alternative_text: str | None = None
    file_name: str | None = None
    link: str | None = None


class BlogCategorySeoConfig(Dto):
    """One ``seo_configs`` entry; no write here sets the list, so a created category's is empty."""

    id: int | None = None
    value: str | None = None
    type: str | None = None
    config_key: str | None = None


class BlogCategory(Dto):
    """One blog category: a listing row, a row path's body and every write's answer, the same eleven
    fields each time. The row never lists the blogs it holds."""

    ENVELOPE_KEY = "blog_category"

    id: int | None = None
    #: A UUID string the store assigns; a create or update naming another one keeps the stored one.
    uuid: str | None = None
    name: str | None = None
    url: str | None = None
    description: str | None = None
    is_disposable: bool | None = None
    is_in_trash: bool | None = None
    image: BlogCategoryImage | None = None
    created_on: str | None = None
    last_updated_on: str | None = None
    seo_configs: list[BlogCategorySeoConfig] | None = None


class BlogCategoryImageInput(Dto):
    """An image upload; ``title`` and ``alternative_text`` are stored only beside a ``base64``."""

    file_name: str | None = None
    base64: str | None = None
    title: str | None = None
    alternative_text: str | None = None


class BlogCategoryBlog(Dto):
    """A blog the category is linked to, by ``id``."""

    id: int | None = None


class BlogCategoryInput(Dto):
    """The writable form of :class:`BlogCategory`, inside the wrapper both writes require. An update
    blanks an unset ``description`` and keeps the ``url``, the ``image`` and the blog links."""

    ENVELOPE_KEY = "blog_category"

    name: str | None = None
    url: str | None = None
    description: str | None = None
    image: BlogCategoryImageInput | None = None
    blogs: list[BlogCategoryBlog] | None = None


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


class BlogCategoryPage(Dto):
    """One page of the listing. ``field_metadata`` is accepted and adds no key."""

    blog_categories: list[BlogCategory] | None = None
    pagination: Pagination | None = None
