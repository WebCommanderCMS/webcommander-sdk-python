"""URL assembly for WebCommander paths."""

from __future__ import annotations

import re
from typing import Any, Mapping
from urllib.parse import quote, urlsplit

from webcommander.errors import SdkUsageError
from webcommander.redaction import REDACTED

_PLACEHOLDER_PATTERN = re.compile(r"\{([a-z_][a-z0-9_]*)\}")
_QUERY_OR_FRAGMENT_PATTERN = re.compile(r"[?#]")
_ABSOLUTE_URL_PREFIXES = ("http://", "https://")

#: One ``name=***`` pair, anchored on delimiters so it matches a whole name and value.
_REDACTED_PARAMETER = re.compile(r"[?#&]([^?#&=]*)=" + re.escape(REDACTED) + r"(?=[&#]|$)")

#: Implied ports, so ``https://host`` and ``https://host:443`` are one origin.
IMPLIED_PORTS = {"http": 80, "https": 443}


def find_path_param_names(path_template: str) -> tuple[str, ...]:
    """The ``{name}`` placeholders in a template, first-seen and deduplicated; only the
    part before the first ``?`` or ``#`` is scanned."""
    template, _ = _split_path_template(path_template)
    return tuple(dict.fromkeys(_PLACEHOLDER_PATTERN.findall(template)))


def substitute_path_params(
    path_template: str,
    path_params: Mapping[str, Any] | None = None,
) -> str:
    """Fill ``{name}`` placeholders in a path template, percent-encoding every value; a dot-only
    value is refused, as a dot segment would reach another endpoint. The query is left as given."""
    template, query_and_fragment = _split_path_template(path_template)
    expected = find_path_param_names(path_template)
    supplied = dict(path_params or {})

    problems: list[str] = []
    missing = [name for name in expected if name not in supplied]
    if missing:
        problems.append(f"missing path params: {', '.join(sorted(missing))}")
    unknown = [name for name in supplied if name not in expected]
    if unknown:
        problems.append(f"unknown path params: {', '.join(sorted(unknown))}")
    given = [name for name in expected if name in supplied]
    blank = [name for name in given if _blank_path_param(supplied[name])]
    if blank:
        problems.append(f"blank path params: {', '.join(sorted(blank))}")
    wrong_typed = [
        name for name in given if name not in blank and not _usable_path_param(supplied[name])
    ]
    if wrong_typed:
        described = (f"{name} ({type(supplied[name]).__name__})" for name in wrong_typed)
        problems.append(f"wrong-typed path params: {', '.join(sorted(described))}")
    dot_only = [
        name
        for name in given
        if name not in blank
        and name not in wrong_typed
        and _is_dot_only(_path_param_text(supplied[name]))
    ]
    if dot_only:
        problems.append(f"dot-only path params: {', '.join(sorted(dot_only))}")
    if problems:
        raise SdkUsageError(f"{path_template} -> " + "; ".join(problems))

    def fill(match: re.Match[str]) -> str:
        name = match.group(1)
        try:
            return quote(_path_param_text(supplied[name]), safe="")
        except UnicodeEncodeError as error:
            raise SdkUsageError(
                f"{path_template} -> path param {name} cannot be encoded; it is not "
                f"text this SDK can put in a URL",
                detail=str(error),
                cause=error,
            ) from None

    substituted = _PLACEHOLDER_PATTERN.sub(fill, template)
    if "{" in substituted or "}" in substituted:
        raise SdkUsageError(f"{path_template} -> malformed placeholder, unresolved: {substituted}")
    return substituted + query_and_fragment


def build_url(base_url: str, path: str) -> str:
    """Join a base URL and a path."""
    _reject_a_redacted_value(path)
    _reject_a_fragment(path)
    if path.lower().startswith(_ABSOLUTE_URL_PREFIXES):
        _require_same_origin(base_url, path)
        return path
    return base_url.rstrip("/") + ("" if path.startswith("/") else "/") + path


def check_request_url(url: Any) -> str:
    """Validate one assembled request target and return it unchanged."""
    if not isinstance(url, str):
        raise SdkUsageError(
            f"url: expected an absolute http(s) URL as text, got {type(url).__name__}"
        )
    if not url.strip():
        raise SdkUsageError("url: expected an absolute http(s) URL, got a blank one")
    if not url.lower().startswith(_ABSOLUTE_URL_PREFIXES):
        # The scheme is named, not the URL: the rest is somebody's path and query.
        raise SdkUsageError(
            f"url: expected an absolute URL beginning http:// or https://, got a "
            f"{_scheme_label(url)} one; build it with build_url, which joins it to the "
            f"configured base URL"
        )
    _reject_a_fragment(url, "url")
    _reject_userinfo(url, "url")
    return url


def _reject_userinfo(url: str, label: str) -> None:
    """Refuse an absolute URL carrying a ``user:password@``; neither the URL nor its host is
    echoed, as the userinfo holds a password."""
    parts = urlsplit(url)
    if parts.username or parts.password:
        raise SdkUsageError(
            f"{label}: the absolute URL carries embedded credentials, which would replace "
            f"the bearer token; strip the userinfo"
        )


def _scheme_label(url: str) -> str:
    """Name the scheme of a URL that was refused, without echoing the rest of it."""
    scheme = urlsplit(url).scheme
    return f"{scheme.lower()!r}" if scheme else "relative"


def _reject_a_redacted_value(path: str) -> None:
    """Refuse a URL that came from a printed copy rather than a response; scoped to a
    parameter whose *entire* value is the marker."""
    found = _REDACTED_PARAMETER.search(path)
    if found is None:
        return
    raise SdkUsageError(
        "path: a query value is the redaction marker; use the URL from the response",
        detail=f"the parameter is {found.group(1)!r}",
    )


def _reject_a_fragment(path: str, label: str = "path") -> None:
    """Refuse a request path or continuation URL carrying a ``#``: a fragment is never sent, so the
    call would silently differ from the one written. The text is never echoed."""
    if "#" not in path:
        return
    raise SdkUsageError(f"{label}: a fragment is never sent; drop it")


def _require_same_origin(base_url: str, url: str) -> None:
    """Refuse an absolute URL off ``base_url``'s origin: a foreign host would receive the bearer
    token, and ``http://`` would send it in the clear. Only the two origins are named."""
    _reject_userinfo(url, "path")
    origin = _split_origin(url)
    configured = _split_origin(base_url)
    if origin != configured:
        raise SdkUsageError(
            "path: absolute URL is not on the configured origin",
            detail=f"supplied {_render_origin(origin)}, configured {_render_origin(configured)}",
        )


def _split_origin(url: str) -> tuple[str, str, int | None]:
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    try:
        port = parts.port
    except ValueError as error:
        raise SdkUsageError(
            "path: the URL carries a port this SDK cannot read; a URL passed back from a "
            "response body must name a numeric port or none",
            detail=str(error),
            cause=error,
        ) from None
    return scheme, (parts.hostname or "").lower(), port or IMPLIED_PORTS.get(scheme)


def _render_origin(origin: tuple[str, str, int | None]) -> str:
    """One origin as ``scheme://host:port``, the port spelled out so both sides compare."""
    scheme, host, port = origin
    return f"{scheme}://{host}:{port}" if port is not None else f"{scheme}://{host}"


def _split_path_template(path_template: str) -> tuple[str, str]:
    """Split off the query and fragment, which hold data rather than slots."""
    boundary = _QUERY_OR_FRAGMENT_PATTERN.search(path_template)
    if boundary is None:
        return path_template, ""
    return path_template[: boundary.start()], path_template[boundary.start() :]


def _path_param_text(value: Any) -> str:
    """One value for its segment, a ``str`` stripped."""
    return value.strip() if isinstance(value, str) else str(value)


def _is_dot_only(text: str) -> bool:
    stripped = text.strip()
    return bool(stripped) and set(stripped) == {"."}


def _blank_path_param(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _usable_path_param(value: Any) -> bool:
    """Whether a value can stand as one path segment; ``bool`` is refused despite being an ``int``,
    and ``bytes`` too, which ``str()`` would render as ``b'1192'``."""
    return isinstance(value, (str, int)) and not isinstance(value, bool)
