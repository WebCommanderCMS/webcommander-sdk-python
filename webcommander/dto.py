"""The typed view over a body — what every DTO is built from."""

from __future__ import annotations

import types
import typing
from types import MappingProxyType
from typing import Any, ClassVar, Mapping, TypeVar, get_args, get_origin, get_type_hints
from weakref import WeakKeyDictionary, ref

from webcommander.errors import SdkUsageError
from webcommander.redaction import REDACTED, redact_snapshot, should_redact

__all__ = ["Dto"]

DtoSubclass = TypeVar("DtoSubclass", bound="Dto")


class _Schema:
    """One DTO subclass's declaration, captured at class creation and kept off the class."""

    __slots__ = ("envelope_key", "top_level", "_cls", "_fields")

    def __init__(self, cls: type) -> None:
        self.envelope_key: str | None = getattr(cls, "ENVELOPE_KEY", None)
        self.top_level: tuple[str, ...] = tuple(getattr(cls, "TOP_LEVEL", ()) or ())
        self._cls = ref(cls)
        self._fields: Mapping[str, Any] | None = None

    @property
    def fields(self) -> Mapping[str, Any]:
        """The canonical field-to-type mapping, resolved once; :meth:`Dto.fields` copies it."""
        if self._fields is None:
            self._fields = MappingProxyType(
                {
                    name: _unwrap_optional(annotation)
                    for name, annotation in get_type_hints(self._cls()).items()
                    if not name.startswith("_") and get_origin(annotation) is not ClassVar
                }
            )
        return self._fields


_SCHEMAS: "WeakKeyDictionary[type, _Schema]" = WeakKeyDictionary()


def _unwrap_optional(annotation: Any) -> Any:
    """``X`` for an annotation written ``X | None``, else the annotation itself."""
    if get_origin(annotation) in (typing.Union, types.UnionType):
        rest = [arg for arg in get_args(annotation) if arg is not type(None)]
        if len(rest) == 1:
            return rest[0]
        return rest
    return annotation


class Dto:
    """Base for every typed view in this SDK."""

    ENVELOPE_KEY: ClassVar[str | None] = None
    TOP_LEVEL: ClassVar[tuple[str, ...]] = ()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Capture this subclass's declaration as the class is created, before anyone reaches it."""
        super().__init_subclass__(**kwargs)
        _SCHEMAS[cls] = _Schema(cls)

    @classmethod
    def fields(cls) -> Mapping[str, Any]:
        """This type's fields, in declaration order, mapped to the type each holds."""
        return MappingProxyType(dict(_SCHEMAS[cls].fields))

    def __init__(self, /, **values: Any) -> None:
        """Build one; every field optional, an unknown name refused."""
        fields = _SCHEMAS[type(self)].fields
        unknown = sorted(set(values) - set(fields))
        if unknown:
            available = ", ".join(fields) or "no fields"
            raise SdkUsageError(
                f"{type(self).__name__} has no field {', '.join(unknown)}; it holds {available}"
            )
        for name in fields:
            setattr(self, name, values.get(name))

    @classmethod
    def from_map(cls: type[DtoSubclass], body: Mapping[str, Any]) -> DtoSubclass:
        """Read a decoded body — ``response.map``, or one record out of it — into this
        type, unwrapping :attr:`ENVELOPE_KEY` when present."""
        if not isinstance(body, Mapping):
            raise SdkUsageError(
                f"{cls.__name__}.from_map expects a decoded mapping body, got "
                f"{type(body).__name__} — a binary or empty body has no DTO"
            )

        schema = _SCHEMAS[cls]
        source: dict[str, Any] = dict(body)
        if schema.envelope_key is not None:
            inner = source.get(schema.envelope_key)
            if isinstance(inner, Mapping):
                beside = {k: v for k, v in source.items() if k != schema.envelope_key}
                source = {**dict(inner), **beside}

        return cls(
            **{
                name: _read(source.get(name), declared)
                for name, declared in schema.fields.items()
                if name in source
            }
        )

    def to_map(self) -> dict[str, Any]:
        """Return the body this DTO stands for, envelope included."""
        schema = _SCHEMAS[type(self)]
        record: dict[str, Any] = {}
        beside: dict[str, Any] = {}
        for name in schema.fields:
            value = getattr(self, name, None)
            if value is None:
                continue
            (beside if name in schema.top_level else record)[name] = _write(value)

        body = {schema.envelope_key: record} if schema.envelope_key else dict(record)
        body.update(beside)
        return body

    def __eq__(self, other: Any) -> bool:
        """Equal when the same type carries the same field values."""
        if type(other) is not type(self):
            return NotImplemented
        return all(
            getattr(self, name, None) == getattr(other, name, None)
            for name in _SCHEMAS[type(self)].fields
        )

    def __repr__(self) -> str:
        """A ``repr`` with secrets masked and unset fields omitted."""
        shown = []
        for name in _SCHEMAS[type(self)].fields:
            value = getattr(self, name, None)
            if value is None:
                continue
            rendered = repr(REDACTED) if should_redact(name) else _render_value(value)
            shown.append(f"{name}={rendered}")
        return f"{type(self).__name__}({', '.join(shown)})"


_SCHEMAS[Dto] = _Schema(Dto)


def _render_value(value: Any) -> str:
    """One field value for :meth:`Dto.__repr__`; a nested DTO recurses, the rest is snapshotted."""
    if isinstance(value, Dto):
        return repr(value)
    if isinstance(value, list):
        return "[" + ", ".join(_render_value(item) for item in value) + "]"
    if isinstance(value, tuple):
        items = ", ".join(_render_value(item) for item in value)
        return f"({items},)" if len(value) == 1 else f"({items})"
    return repr(redact_snapshot(value))


def _read(value: Any, declared: Any) -> Any:
    """One value as its declared type, or ``None`` when it is not that type. Nothing is
    converted; the value is still in ``response.map``, untouched."""
    if value is None:
        return None

    origin = get_origin(declared)
    if origin in (list, tuple):
        if not isinstance(value, (list, tuple)):
            return None
        (item_type,) = get_args(declared) or (Any,)
        # Unwrapped as a field is, or an ``Address | None`` entry would never be an ``Address``.
        return [_read(item, _unwrap_optional(item_type)) for item in value]

    if isinstance(declared, type) and issubclass(declared, Dto):
        return declared.from_map(value) if isinstance(value, Mapping) else None

    if declared is Any or isinstance(declared, list):
        return value

    if declared is float:
        return (
            float(value)
            if isinstance(value, (int, float)) and not isinstance(value, bool)
            else None
        )
    if declared is int:
        return value if isinstance(value, int) and not isinstance(value, bool) else None
    if declared is bool:
        return value if isinstance(value, bool) else None

    return value if isinstance(value, declared) else None


def _write(value: Any) -> Any:
    """One value as the API receives it: a nested DTO becomes its record, a list is
    walked for nested DTOs, and everything else is itself."""
    if isinstance(value, Dto):
        record = value.to_map()
        envelope_key = _SCHEMAS[type(value)].envelope_key
        return record[envelope_key] if envelope_key else record
    if isinstance(value, (list, tuple)):
        return [_write(item) for item in value]
    if isinstance(value, Mapping):
        return {key: _write(item) for key, item in value.items()}
    return value
