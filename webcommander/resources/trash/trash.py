"""Trash endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.trash import trash_urls
from webcommander.resources.trash.trash_dto import (
    TrashBulkDeleteResult,
    TrashBulkRestoreResult,
    TrashItem,
    TrashPage,
    TrashTypeList,
)

__all__ = [
    "list_trash",
    "head_trash",
    "list_trash_types",
    "head_trash_types",
    "restore_trash_item",
    "delete_trash_item",
    "bulk_restore_trash",
    "bulk_delete_trash",
]

TrashBulkPayload = Mapping[str, Any] | str | Dto


def list_trash(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TrashPage]:
    """List trashed rows, newest change first — ``GET /admin/trash``. ``type`` (a ``types`` value,
    any case, or a comma list), ``search`` or ``searchText``, ``sort`` ``name``, ``type``,
    ``updated`` or ``removed_at`` with ``order`` or ``dir``, ``limit`` or ``max`` (above 100 is
    ``400``), ``offset``, ``page``, ``removed_from`` and ``removed_to``; any other name is ``400``.
    A listing without ``type``, or of ``Customer``, can outlast the default ``timeout_seconds``."""
    return client.send_get_request(
        trash_urls.TRASH,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TrashPage,
    )


def head_trash(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the listing is reachable — ``HEAD /admin/trash``; no body. It takes the
    listing's query names and runs the same query, so pass a ``type`` as on the ``GET``."""
    return client.send_api_request(
        "HEAD",
        trash_urls.TRASH,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def list_trash_types(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TrashTypeList]:
    """List the types the trash holds — ``GET /admin/trash/types``, snake_case names such as
    ``category``, ``customer`` and ``blog_post``. Any query name is ``400``."""
    return client.send_get_request(
        trash_urls.TRASH_TYPES,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TrashTypeList,
    )


def head_trash_types(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the type list is reachable — ``HEAD /admin/trash/types``; no body."""
    return client.send_api_request(
        "HEAD",
        trash_urls.TRASH_TYPES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def restore_trash_item(
    client: Any,
    trash_type: str,
    trash_item_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TrashItem]:
    """Restore one trashed row — ``POST /admin/trash/{trash_type}/{trash_item_id}/restore``,
    answered ``200`` with the row under ``item``; sends no body. A live row is ``409``, an id the
    type does not hold ``404``."""
    return client.send_post_request(
        trash_urls.TRASH_ITEM_RESTORE,
        path_params={"trash_type": trash_type, "trash_item_id": trash_item_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TrashItem,
    )


def delete_trash_item(
    client: Any,
    trash_type: str,
    trash_item_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one trashed row for good — ``DELETE /admin/trash/{trash_type}/{trash_item_id}``;
    ``204``. A live row is ``409``; once purged, every read and a second delete are ``404``."""
    return client.send_delete_request(
        trash_urls.TRASH_ITEM,
        path_params={"trash_type": trash_type, "trash_item_id": trash_item_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def bulk_restore_trash(
    client: Any,
    payload: TrashBulkPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TrashBulkRestoreResult]:
    """Restore up to 100 rows — ``POST /admin/trash/bulk-restore`` with ``{"items": [{"type",
    "id"}]}``. ``200`` when every item is restored, ``207`` with the same body when any fails."""
    require_payload(payload)
    return client.send_post_request(
        trash_urls.TRASH_BULK_RESTORE,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TrashBulkRestoreResult,
    )


def bulk_delete_trash(
    client: Any,
    payload: TrashBulkPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TrashBulkDeleteResult]:
    """Delete up to 100 trashed rows for good — ``POST /admin/trash/bulk-delete``, the bulk
    restore's body. ``200`` when every item is deleted, ``207`` with the same body when any fails."""
    require_payload(payload)
    return client.send_post_request(
        trash_urls.TRASH_BULK_DELETE,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TrashBulkDeleteResult,
    )
