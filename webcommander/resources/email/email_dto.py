"""Typed views over the email send bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class EmailInput(Dto):
    """The send body, bare and camelCase as the store takes it; ``html_content`` and other
    unknown keys are ignored. ``recipients``, ``cc`` and ``bcc`` hold at most 100 addresses
    together. Send ``htmlContent`` or a plugin template's ``identifier``, not both."""

    recipients: list[str | None] | None = None
    cc: list[str | None] | None = None
    bcc: list[str | None] | None = None
    subject: str | None = None
    htmlContent: str | None = None
    contentType: str | None = None
    identifier: str | None = None
    # The template's variables, an object of any shape.
    data: Any = None


class EmailRejection(Dto):
    """One address the store could not send to, and why, such as ``send_failed``."""

    email: str | None = None
    reason: str | None = None


class EmailSendResult(Dto):
    """The send's verdict: each list holds the addresses trimmed, a repeat in any case once."""

    status: str | None = None
    accepted: list[str | None] | None = None
    rejected: list[EmailRejection | None] | None = None
    cc: list[str | None] | None = None
    bcc: list[str | None] | None = None
