"""Typed views over the trash bodies."""

from __future__ import annotations

from webcommander.dto import Dto


class TrashItem(Dto):
    """One trashed row, and the ``item`` a restore answers. ``type`` is the snake_case name
    ``types`` answers; ``removed_at`` is when the row was trashed, in UTC; ``url`` is the record's
    own path, ``None`` for a ``blog_post``. A restore and a bulk delete send no ``removed_at``."""

    ENVELOPE_KEY = "item"

    type: str | None = None
    id: int | None = None
    name: str | None = None
    removed_at: str | None = None
    url: str | None = None


class Pagination(Dto):
    """The five-key ``pagination`` block; there is no next-page link, so step ``offset``."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    has_previous: bool | None = None
    has_next: bool | None = None


class TrashPage(Dto):
    """One page of the listing: the rows and where they sit."""

    items: list[TrashItem | None] | None = None
    pagination: Pagination | None = None


class TrashType(Dto):
    """One type the trash holds, as a path's ``{trash_type}`` takes it."""

    type: str | None = None


class TrashTypeList(Dto):
    """The ``types`` body: every type, alphabetical."""

    types: list[TrashType | None] | None = None


class TrashBulkError(Dto):
    """One item a bulk call could not act on: an error ``code`` such as ``not_found`` or
    ``not_in_trash``, and why in words."""

    type: str | None = None
    id: int | None = None
    code: str | None = None
    message: str | None = None


class TrashBulkRestoreResult(Dto):
    """The bulk restore's body: the rows restored, and an entry per failed item."""

    restored: list[TrashItem | None] | None = None
    failed: list[TrashBulkError | None] | None = None


class TrashBulkDeleteResult(Dto):
    """The bulk delete's body: the rows deleted, each ``type``, ``id`` and ``name``, and an entry
    per failed item."""

    deleted: list[TrashItem | None] | None = None
    failed: list[TrashBulkError | None] | None = None


class TrashBulkItemInput(Dto):
    """One item of a bulk body; ``type`` in any letter case, ``id`` a number."""

    type: str | None = None
    id: int | None = None


class TrashBulkInput(Dto):
    """The bulk body, ``{"items": [...]}``, 1 to 100 items; no envelope."""

    items: list[TrashBulkItemInput | None] | None = None
