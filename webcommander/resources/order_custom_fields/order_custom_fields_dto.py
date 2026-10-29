"""Typed views over the order custom field bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class OrderCustomField(Dto):
    """One order custom field. A listing row carries the twelve fields up to ``max_length``;
    the row path adds the nine after it, and ``field_metadata`` when that is asked for."""

    ENVELOPE_KEY = "order_custom_field"

    id: int | None = None
    field_type: str | None = None
    label: str | None = None
    name: str | None = None
    is_active: bool | None = None
    order_no: int | None = None
    created_on: str | None = None
    last_updated_on: str | None = None
    is_required: bool | None = None
    input_format: str | None = None
    has_max_length: bool | None = None
    max_length: int | None = None
    hover_text: str | None = None
    placeholder: str | None = None
    default_value: str | None = None
    html_class: str | None = None
    options: list[str | None] | None = None
    is_allowed_for_shipping: bool | None = None
    is_allowed_for_delivery: bool | None = None
    is_allowed_for_store_pickup: bool | None = None
    is_allowed_for_pre_order: bool | None = None
    field_metadata: Any = None


class Pagination(Dto):
    """The ten-key ``pagination`` block; ``limit`` is the size the store applied, capped at 20."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    count: int | None = None
    current_page: int | None = None
    total_pages: int | None = None
    has_next: bool | None = None
    has_previous: bool | None = None
    previous_page: str | None = None
    next_page: str | None = None


class ResourceMeta(Dto):
    """The listing's one ``group_meta`` entry: ``kind`` ``resource``, ``writable`` ``false``."""

    kind: str | None = None
    writable: bool | None = None
    href: str | None = None


class GroupMeta(Dto):
    """The listing's ``group_meta`` block, keyed by the collection's own name."""

    order_custom_fields: ResourceMeta | None = None


class OrderCustomFieldPage(Dto):
    """One page of the listing: the rows, where they sit, ``group_meta`` and any schema."""

    order_custom_fields: list[OrderCustomField | None] | None = None
    pagination: Pagination | None = None
    group_meta: GroupMeta | None = None
    field_metadata: Any = None


class OrderCustomFieldTimeslotInput(Dto):
    """The ``validate_timeslot`` body; no envelope. ``selected_date`` is required, ``dd/MM/yyyy``;
    an ``order_limit`` above 0 makes both hours required and ``field_name`` read, as text."""

    selected_date: str | None = None
    field_name: str | None = None
    weekday_id: int | None = None
    start_hour: int | None = None
    end_hour: int | None = None
    order_limit: int | None = None
