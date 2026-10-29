"""Path templates for the trash endpoints."""

from __future__ import annotations

TRASH = "/api/{api_version}/admin/trash"
TRASH_TYPES = "/api/{api_version}/admin/trash/types"
TRASH_ITEM = "/api/{api_version}/admin/trash/{trash_type}/{trash_item_id}"
TRASH_ITEM_RESTORE = "/api/{api_version}/admin/trash/{trash_type}/{trash_item_id}/restore"
TRASH_BULK_RESTORE = "/api/{api_version}/admin/trash/bulk-restore"
TRASH_BULK_DELETE = "/api/{api_version}/admin/trash/bulk-delete"
