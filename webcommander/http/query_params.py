"""Query parameter normalisation."""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence

from webcommander.errors import SdkUsageError

#: One materialised query: ``(name, value)`` pairs in wire order, each part ``str`` or ``bytes``.
QueryPairs = tuple[tuple[str, "str | bytes"], ...]


class SortDirection(str, Enum):
    """Sort order for the ``dir`` and ``order`` query parameters."""

    ASC = "asc"
    DESC = "desc"


def build_query_params(params: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Normalise query parameter values for the wire; keys pass through untouched."""
    if params is None:
        return {}
    if not isinstance(params, Mapping):
        raise SdkUsageError(
            f"query params: expected a mapping of names to values, got "
            f"{type(params).__name__}; to send one name twice give it a list, as "
            f"in {{'limit': [5, 6]}}"
        )

    normalised: dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        normalised[key] = _normalise_query_value(value, key, 0)
    return normalised


def _normalise_query_value(value: Any, key: str, depth: int) -> Any:
    """Normalise one value, rejecting a nested mapping at whatever depth it sits, since
    ``requests`` encodes one inside a list as its first *key*."""
    if isinstance(value, Mapping):
        raise SdkUsageError(
            f"query param {key!r}: nested objects cannot be encoded in a query "
            f"string; flatten it or send it in the body"
        )
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Enum):
        return _normalise_query_value(value.value, key, depth)
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, bytearray)):
        if depth >= 1:
            raise SdkUsageError(
                f"query param {key!r}: a sequence inside a sequence has no "
                f"query-string encoding; flatten it to one list of scalars"
            )
        return [
            _normalise_query_value(entry, key, depth + 1) for entry in value if entry is not None
        ]
    return value


def materialise_query_params(params: Any) -> QueryPairs:
    """Freeze a normalised query into the wire pairs, from a mapping or already-made pairs."""
    if not params:
        return ()
    pairs: list[tuple[str, str | bytes]] = []
    for name, value in _query_entries(params):
        rendered = wire_text(name)
        values = (
            [value]
            if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Iterable)
            else list(value)
        )
        for item in values:
            if item is None:
                continue
            pairs.append((rendered, wire_value(item)))
    return tuple(pairs)


def group_query_pairs(pairs: QueryPairs) -> dict[str, Any]:
    """The materialised pairs as the mapping a request record reports: one entry per name, a
    repeated name collecting its values into a list. The wire order is kept."""
    grouped: dict[str, Any] = {}
    for name, value in pairs:
        if name not in grouped:
            grouped[name] = value
            continue
        held = grouped[name]
        grouped[name] = [*held, value] if isinstance(held, list) else [held, value]
    return grouped


def _query_entries(params: Any) -> list[tuple[Any, Any]]:
    if isinstance(params, Mapping):
        return list(params.items())
    if isinstance(params, Sequence) and not isinstance(params, (str, bytes, bytearray)):
        return [
            (entry[0], entry[1])
            for entry in params
            if isinstance(entry, (tuple, list)) and len(entry) == 2
        ]
    raise SdkUsageError(
        f"query params: expected a mapping of names to values or a sequence of "
        f"(name, value) pairs, got {type(params).__name__}"
    )


def wire_text(value: Any) -> str:
    """One name as its wire text, ``bytes`` decoded with a lossless fallback."""
    if isinstance(value, (bytes, bytearray)):
        return bytes(value).decode("utf-8", "surrogateescape")
    return value if isinstance(value, str) else str(value)


def wire_value(value: Any) -> str | bytes:
    """One value as wire ``str`` or ``bytes``; the one place a caller's object gives its text."""
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    return value if isinstance(value, str) else str(value)
