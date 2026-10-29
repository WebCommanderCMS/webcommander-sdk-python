"""Email endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.email import email_urls
from webcommander.resources.email.email_dto import EmailSendResult
from webcommander.resources.required_bodies import require_payload

__all__ = ["send_email"]

EmailPayload = Mapping[str, Any] | str | Dto


def send_email(
    client: Any,
    payload: EmailPayload,
    *,
    plugin_uuid: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[EmailSendResult]:
    """Send an email — ``POST /admin/email/send``, answered ``200`` once every message is sent. A
    bare body: ``recipients`` and ``subject``, with ``htmlContent`` or a template ``identifier``
    and its ``data``. ``plugin_uuid`` is sent as the header a template send needs and switches the
    call to plugin auth, so an admin token is ``401``. Past 500 addresses a day per sender the
    store answers ``429`` until 00:00 UTC; a body over 1048576 bytes is ``413``. A send the mail
    server fails is ``502``, ``status`` ``failed``, each address in ``rejected``."""
    require_payload(payload)
    return client.send_post_request(
        email_urls.EMAIL_SEND,
        json_body=payload,
        headers=None if plugin_uuid is None else {email_urls.PLUGIN_UUID_HEADER: plugin_uuid},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=EmailSendResult,
    )
