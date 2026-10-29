"""Path templates for the email endpoints."""

from __future__ import annotations

EMAIL_SEND = "/api/{api_version}/admin/email/send"

#: Names the plugin that owns the template ``identifier``; a ``plugin_uuid`` body field is ignored.
PLUGIN_UUID_HEADER = "plugin_uuid"
