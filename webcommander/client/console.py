"""Rendering one exchange for a human at a terminal."""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from typing import Any, Mapping
from urllib.parse import urlencode, urlsplit

from webcommander.client.api_response import CONTENT_TYPE_HEADER, JSON_MEDIA_TYPE, ApiResponse
from webcommander.config.sdk_config import PRINT_FORMAT_COMPACT
from webcommander.errors import neutralise_controls
from webcommander.redaction import redact_mapping, redact_value

__all__ = [
    "render_exchange",
    "render_json_value",
    "build_curl_command",
    "resolve_box_glyphs",
    "summarise_payload",
]

_UNICODE_BOX_GLYPHS = {
    "top": "┌",
    "bottom": "└",
    "tee": "├",
    "v": "│",
    "h": "─",
    "ellipsis": "…",
}
_ASCII_BOX_GLYPHS = {
    "top": "+",
    "bottom": "+",
    "tee": "+",
    "v": "|",
    "h": "-",
    "ellipsis": "...",
}

_DUMB_TERMINAL = "dumb"

_ANSI_ESCAPE = "\x1b"
_ANSI_ESCAPE_START = "\x1b["
_ANSI_RESET = "\x1b[0m"

_POSIX_SHELL_LABEL = "POSIX shell"

_MULTIPART_PREFIX = "<multipart: "
_UNNAMED_FILE = "file"
_PAYLOAD_FILES_KEY = "files"
_PAYLOAD_FORM_KEY = "form"

#: Characters JSON leaves unescaped that a terminal acts on.
_JSON_DISPLAY_UNSAFE = re.compile(r"[\x7f-\x9f\u2028\u2029]")

_JSON_DOCUMENT_START = ("{", "[")


def render_json_value(value: Any, *, compact: bool = False) -> str:
    """Render an already-redacted value for display, indented or ``compact`` on one line, with
    ``ensure_ascii=False``; binary values are summarised at any depth, never dumped."""
    if value is None:
        return "<empty>"
    if isinstance(value, (bytes, bytearray, memoryview)):
        return _summarise_binary(value)
    if isinstance(value, str):
        if _json_document(value) is not None:
            return neutralise_controls(value, keep_newlines=not compact)
        if compact:
            return neutralise_controls(json.dumps(value, ensure_ascii=False)[1:-1])
        return neutralise_controls(value, keep_newlines=True)
    try:
        if compact:
            rendered = json.dumps(
                value, separators=(",", ":"), ensure_ascii=False, default=_json_default
            )
            return neutralise_controls(rendered)
        rendered = json.dumps(value, indent=2, ensure_ascii=False, default=_json_default)
        return neutralise_controls(rendered, keep_newlines=True)
    except Exception:  # a raise here would turn a completed call into an error
        return neutralise_controls(str(value), keep_newlines=True)


def _json_document(text: str) -> Any:
    """The object or array a string is, or ``None``: parsed rather than pattern-matched, so a
    string merely opening with a brace keeps the plain-string escaping."""
    if not text.lstrip().startswith(_JSON_DOCUMENT_START):
        return None
    try:
        parsed = json.loads(text)
    except (ValueError, RecursionError):
        return None
    return parsed if isinstance(parsed, (dict, list)) else None


def _summarise_binary(value: Any) -> str:
    length = value.nbytes if isinstance(value, memoryview) else len(value)
    return f"<{length} bytes>"


def _json_default(value: Any) -> Any:
    """Render what ``json`` cannot serialise without raising: bytes are summarised, since
    ``default=str`` would dump them, and a frozen mapping is unwrapped into a ``dict``."""
    if isinstance(value, (bytes, bytearray, memoryview)):
        return _summarise_binary(value)
    if isinstance(value, Mapping):
        return dict(value)
    return str(value)


def render_exchange(
    response: Any,
    body: Any,
    files: Any,
    config: Any,
    *,
    form_encoded: bool = False,
) -> str:
    """Render one request/response exchange for the console; ``files`` is summarised by name.
    ``response`` may be the client's ``_FailedExchange``, so only five attributes are read."""
    info = response.request_info
    payload = summarise_payload(body, files)

    if config.print_format == PRINT_FORMAT_COMPACT:
        parts = [
            "wc",
            info.client_name,
            info.http_method,
            info.url,
            str(response.status_code),
            f"{info.attempt_count}/{info.max_attempts}",
            f"{info.elapsed_seconds}s",
        ]
        if config.print_request_payload:
            parts.append(f"payload={render_json_value(redact_value(payload), compact=True)}")
        if config.print_response_body:
            parts.append(f"response={render_json_value(redact_value(response.map), compact=True)}")
        return _truncate(_encode_for_console(" | ".join(parts)), config.print_max_chars)

    glyphs = resolve_box_glyphs()
    colour = _Colour(config.print_color and _stdout_supports_colour(), glyphs)
    lines: list[str] = [
        colour.dim(
            f"WebCommander  {info.http_method}  {response.status_code}  {info.elapsed_seconds}s"
        )
    ]

    if config.print_api_info:
        for label, value in (
            ("client", info.client_name),
            ("api version", info.api_version),
            ("method", info.http_method),
            ("endpoint", info.url),
            ("params", render_json_value(dict(info.query_params), compact=True)),
        ):
            row = neutralise_controls(str(value))
            lines.append(f"{label:<12}: {row}")
        lines.append(
            f"{'status':<12}: " + colour.status(f"{response.status_code}", response.succeeded)
        )
        lines.append(f"{'attempt':<12}: {info.attempt_count} / {info.max_attempts}")
        lines.append(f"{'elapsed':<12}: {info.elapsed_seconds}s")

    if config.print_headers:
        lines.append(colour.section("request headers"))
        lines.extend(_header_rows(info.headers))
        lines.append(colour.section("response headers"))
        lines.extend(_header_rows(redact_mapping(response.headers)))

    if config.print_request_payload and payload is not None:
        lines.append(colour.section("payload"))
        lines.extend(render_json_value(redact_value(payload)).splitlines())

    if config.print_response_body:
        lines.append(colour.section("response"))
        lines.extend(render_json_value(redact_value(response.map)).splitlines())

    if config.print_curl:
        lines.append(colour.section(f"curl ({_POSIX_SHELL_LABEL})"))
        lines.extend(
            build_curl_command(
                response, payload, files, config, form_encoded=form_encoded
            ).splitlines()
        )

    return _truncate(_encode_for_console("\n".join(lines)), config.print_max_chars)


def build_curl_command(
    response: ApiResponse,
    payload: Any,
    files: Any,
    config: Any,
    *,
    form_encoded: bool = False,
) -> str:
    """Build a copy-pasteable ``curl`` for the call, token redacted and every fragment quoted
    with :mod:`shlex` for a POSIX shell, not ``cmd.exe``; a JSON body prints on one line."""
    info = response.request_info
    url = neutralise_controls(info.url)
    if info.query_params:
        # ``safe="*"`` keeps a redacted parameter readable as ``api_key=***``.
        separator = "&" if urlsplit(url).query else "?"
        url = f"{url}{separator}{urlencode(info.query_params, doseq=True, safe='*')}"

    # Every fragment is POSIX-quoted: unquoted, a body value can inject a command.
    parts = [f"curl -X {shlex.quote(info.http_method)} {shlex.quote(url)}"]
    if not config.verify_ssl:
        parts.append("  -k")
    for name, shown in _header_pairs(info.headers):
        parts.append(f"  -H {shlex.quote(f'{name}: {shown}')}")

    entries = _multipart_entries(files)
    body = _form_part(payload)
    # Neutralised as well as quoted: ``report\x1b[2K.csv`` would erase the line above.
    for field_name, filename in entries:
        fragment = f"{neutralise_controls(field_name)}=@{neutralise_controls(filename)}"
        parts.append(f"  -F {shlex.quote(fragment)}")
    if entries:
        for key, value in _form_fields(body):
            parts.append(f"  -F {shlex.quote(_form_fragment(key, value))}")
    elif body is not None:
        fields = _form_fields(body) if form_encoded else []
        if fields:
            for key, value in fields:
                parts.append(f"  --data-urlencode {shlex.quote(_form_fragment(key, value))}")
        else:
            rendered = _curl_body_text(redact_value(body))
            if not form_encoded and not _names_the_content_type(info.headers):
                parts.append(f"  -H {shlex.quote(f'{CONTENT_TYPE_HEADER}: {JSON_MEDIA_TYPE}')}")
            parts.append(f"  --data-raw {shlex.quote(rendered)}")
    return " \\\n".join(parts)


def _header_pairs(headers: Mapping[str, Any]) -> list[tuple[str, str]]:
    """Each header's name and value as display text, sorted by name."""
    return [
        (neutralise_controls(str(key)), neutralise_controls(str(value)))
        for key, value in sorted(headers.items(), key=lambda item: str(item[0]))
    ]


def _form_fragment(key: Any, value: Any) -> str:
    return f"{neutralise_controls(str(key))}={neutralise_controls(str(value))}"


def _curl_body_text(body: Any) -> str:
    """The ``--data-raw`` text for a redacted body: a JSON document collapsed onto one line."""
    if isinstance(body, str):
        document = _json_document(body)
        if document is not None:
            return _collapse_json_document(body, document)
    return render_json_value(body, compact=True)


def _collapse_json_document(text: str, document: Any) -> str:
    """Re-serialise a parsed document onto one line, escaping terminal-unsafe characters as JSON
    escapes so the argument stays a document a parser accepts."""
    try:
        rendered = json.dumps(document, ensure_ascii=False, allow_nan=False)
    except (ValueError, RecursionError):
        return neutralise_controls(text)
    return _JSON_DISPLAY_UNSAFE.sub(lambda match: f"\\u{ord(match.group()):04x}", rendered)


def _names_the_content_type(headers: Mapping[str, Any]) -> bool:
    return any(str(name).lower() == CONTENT_TYPE_HEADER.lower() for name in headers)


def resolve_box_glyphs() -> dict[str, str]:
    """Pick box-drawing characters the console can print; a cp1252 console cannot encode them."""
    try:
        "".join(_UNICODE_BOX_GLYPHS.values()).encode(_stdout_encoding())
    except (LookupError, UnicodeEncodeError):
        return dict(_ASCII_BOX_GLYPHS)
    return dict(_UNICODE_BOX_GLYPHS)


def _stdout_encoding() -> str:
    return getattr(sys.stdout, "encoding", None) or "ascii"


def _encode_for_console(text: str) -> str:
    """Make a rendered block printable on the stream it is headed for, escaping what its
    encoding cannot carry: the client's ``print`` is unguarded."""
    encoding = _stdout_encoding()
    try:
        text.encode(encoding)
        return text
    except UnicodeEncodeError:
        return text.encode(encoding, "backslashreplace").decode(encoding, "replace")
    except LookupError:
        return text


def _stdout_supports_colour() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM") == _DUMB_TERMINAL:
        return False
    try:
        return bool(sys.stdout.isatty())
    except (AttributeError, ValueError):
        return False


class _Colour:
    """ANSI helpers that no-op when colour is off or stdout is not a TTY."""

    def __init__(self, enabled: bool, glyphs: dict[str, str]) -> None:
        self._enabled = enabled
        self._glyphs = glyphs

    def dim(self, text: str) -> str:
        return f"\x1b[2m{text}{_ANSI_RESET}" if self._enabled else text

    def section(self, label: str) -> str:
        prefix = self._glyphs["h"] + self._glyphs["h"] + f" {label} "
        return self.dim(prefix + self._glyphs["h"] * max(4, 62 - len(prefix)))

    def status(self, text: str, succeeded: bool) -> str:
        if not self._enabled:
            return text
        colour = "32" if succeeded else "31"
        return f"\x1b[{colour}m{text}{_ANSI_RESET}"


def _header_rows(headers: Mapping[str, Any]) -> list[str]:
    """One line per redacted header, sorted by name."""
    return [f"{name:<14}: {shown}" for name, shown in _header_pairs(headers)]


def summarise_payload(body: Any, files: Any) -> Any:
    """Describe what was sent without reading any upload: the body, a ``<multipart: ...>``
    summary, or both under ``files`` and ``form``, the form kept a structure for redaction."""
    entries = _multipart_entries(files)
    if not entries:
        return body
    names = ", ".join(f"{field}={filename}" for field, filename in entries)
    summary = f"{_MULTIPART_PREFIX}{names}>"
    if body is None:
        return summary
    return {_PAYLOAD_FILES_KEY: summary, _PAYLOAD_FORM_KEY: body}


def _multipart_entries(files: Any) -> list[tuple[str, str]]:
    """One ``(field name, filename)`` pair per file in a re-readable ``files`` shape; a one-shot
    container is not walked, since describing it would consume the upload."""
    if isinstance(files, Mapping):
        return [_multipart_entry(str(key), value) for key, value in files.items()]
    if isinstance(files, (list, tuple)):
        if all(isinstance(entry, (list, tuple)) and len(entry) == 2 for entry in files):
            return [_multipart_entry(str(entry[0]), entry[1]) for entry in files]
        return [_multipart_entry(_UNNAMED_FILE, files)]
    if hasattr(files, "read"):
        return [_multipart_entry(_UNNAMED_FILE, files)]
    return []


def _multipart_entry(field_name: str, value: Any) -> tuple[str, str]:
    """One entry's field name and filename; a tuple's own filename wins, being the one sent."""
    filename = None
    handle = value
    if isinstance(value, (list, tuple)) and value:
        if isinstance(value[0], str):
            filename = value[0]
        handle = value[1] if len(value) > 1 else None
    return field_name, str(filename or getattr(handle, "name", None) or _UNNAMED_FILE)


def _form_part(payload: Any) -> Any:
    """The form body inside a :func:`summarise_payload` result, or the payload."""
    if (
        isinstance(payload, Mapping)
        and set(payload) == {_PAYLOAD_FILES_KEY, _PAYLOAD_FORM_KEY}
        and str(payload.get(_PAYLOAD_FILES_KEY)).startswith(_MULTIPART_PREFIX)
    ):
        return payload[_PAYLOAD_FORM_KEY]
    return payload


def _form_fields(body: Any) -> list[tuple[str, Any]]:
    """Redacted ``(name, value)`` pairs of a form body, a mapping or a sequence of pairs."""
    if isinstance(body, Mapping):
        return list(redact_value(body).items())
    if (
        isinstance(body, (list, tuple))
        and body
        and all(isinstance(entry, (list, tuple)) and len(entry) == 2 for entry in body)
    ):
        return [(entry[0], entry[1]) for entry in redact_value(body)]
    return []


def _truncate(text: str, max_chars: int) -> str:
    """Cut a rendered block to ``max_chars`` (``0`` is unlimited), notice included; a ceiling too
    small for the notice still gets it."""
    if not max_chars or len(text) <= max_chars:
        return text
    ellipsis = resolve_box_glyphs()["ellipsis"]
    reserved = len(f"{ellipsis} +{len(text)} chars")
    if _ANSI_ESCAPE in text:
        reserved += len(_ANSI_RESET)
    cut = min(len(text), max(0, max_chars - reserved))
    if cut >= len(text):
        return text
    sliced = _close_colour_run(text[:cut])
    return f"{sliced}{ellipsis} +{len(text) - cut} chars"


def _close_colour_run(text: str) -> str:
    """Repair an ANSI sequence a cut landed inside, which would leave the terminal dim."""
    if _ANSI_ESCAPE not in text:
        return text
    marker = text.rfind(_ANSI_ESCAPE)
    if "m" not in text[marker:]:
        text = text[:marker]
    last = text.rfind(_ANSI_ESCAPE_START)
    if last != -1 and not text.startswith(_ANSI_RESET, last):
        return text + _ANSI_RESET
    return text
