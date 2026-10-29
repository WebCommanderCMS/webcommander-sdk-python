"""Typed views over the admin customer bodies."""

from __future__ import annotations

import threading
from typing import Any, ClassVar, Generic, Mapping, TypeVar, cast
from weakref import WeakKeyDictionary

from webcommander.dto import Dto

ItemT = TypeVar("ItemT", bound=Dto)

_SUBSCRIPTED_PAGES: "WeakKeyDictionary[type, type]" = WeakKeyDictionary()

_SUBSCRIPT_LOCK = threading.Lock()


class Reference(Dto):
    """A lookup value sent as an object — ``{"id": …, "name": "Australia", "code": "AU"}``,
    ``id`` being store data."""

    id: int | None = None
    name: str | None = None
    code: str | None = None


class Address(Dto):
    """One entry of a customer's ``addresses``."""

    id: int | None = None
    type: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    company_name: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    country: Reference | None = None
    state: Reference | None = None
    city: str | None = None
    post_code: str | None = None
    mobile: str | None = None
    phone: str | None = None
    fax: str | None = None


class CustomProperty(Dto):
    """One ``custom_properties`` entry. **A write replaces the whole list**, it never appends;
    omitting the field leaves it alone, and ``id`` keys on the label/description pair."""

    id: int | None = None
    label: str | None = None
    description: str | None = None


class Customer(Dto):
    """One customer, in either of the two forms the API sends."""

    ENVELOPE_KEY = "customer"

    customer_id: int | None = None
    internal_id: int | None = None
    #: A UUID string the store assigns; a create or update naming another one keeps the stored one.
    uuid: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    name: str | None = None
    email: str | None = None
    status: str | None = None
    gender: str | None = None
    company_name: str | None = None
    store_credit: float | None = None
    customer_groups: list[Reference | None] | None = None
    shipping_profile: Any = None
    addresses: list[Address | None] | None = None
    created_at: str | None = None
    updated_at: str | None = None

    abn: str | None = None
    abn_branch: str | None = None
    account_hold: bool | None = None
    active_billing_address: int | None = None
    active_shipping_address: int | None = None
    allow_credit_limit: bool | None = None
    background_image: str | None = None
    base_url: str | None = None
    count_referral_code_used: int | None = None
    credit_limit: float | None = None
    custom_properties: list[CustomProperty | None] | None = None
    customer_password_expired: bool | None = None
    default_tax_code: str | None = None
    email_verified: bool | None = None
    hide_price: bool | None = None
    how_do_you_know: str | None = None
    is_in_trash: bool | None = None
    newsletters: list[Any] | None = None
    note: str | None = None
    payment_term: Any = None
    profile_picture: Any = None
    referral_code: Any = None
    sms_subscribed: bool | None = None
    source: str | None = None
    timezone: str | None = None
    transaction_number: str | None = None
    used_referral_code: Any = None
    version: int | None = None


class CustomerInput(Dto):
    """The writable form of :class:`Customer`, for the five writes sending a ``customer`` envelope.
    Without ``status="active"`` a create is filed ``awaiting_verification`` and cannot sign in."""

    ENVELOPE_KEY = "customer"
    TOP_LEVEL = ("transaction_no",)

    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    email_verified: bool | None = None
    password: str | None = None
    old_password: str | None = None
    status: str | None = None
    company: bool | None = None
    company_name: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    state: int | str | None = None
    country: int | str | None = None
    post_code: str | None = None
    addresses: list[Address | None] | None = None
    custom_properties: list[CustomProperty | None] | None = None
    transaction_no: str | None = None


class StoreCreditAdjustment(Dto):
    """One movement of a customer's store credit, in either form the API sends."""

    ENVELOPE_KEY = "store_credit_adjustment"

    id: int | None = None
    customer_id: int | None = None
    internal_id: int | None = None
    action: str | None = None
    amount: float | None = None
    note: str | None = None
    created_at: str | None = None
    created_by: Any = None

    balance_before: float | None = None
    balance_after: float | None = None
    store_credit: float | None = None


class StoreCreditAdjustmentInput(Dto):
    """The writable form of :class:`StoreCreditAdjustment`. **No envelope**: the body is the
    record itself — ``{"action": "add", "amount": 25.0}`` — ``action`` carrying the sign."""

    action: str | None = None
    amount: float | None = None
    note: str | None = None


class Pagination(Dto):
    """The ``pagination`` block of a listing; ``limit`` is the size applied, not the one asked."""

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


class Page(Dto, Generic[ItemT]):
    """One page of a listing: the records, and the block that says where they sit."""

    ITEM_TYPE: ClassVar[type[Dto] | None] = None

    items: list[ItemT | None] | None = None
    pagination: Pagination | None = None

    def __class_getitem__(cls, item_type: Any) -> Any:
        """``Page[Customer]``: a type application to a checker, :meth:`of` at run time."""
        return cls.of(item_type)

    @classmethod
    def of(cls, item_type: type[ItemT]) -> type["Page[ItemT]"]:
        """Return the Page subclass reading its records as ``item_type``, one class per type."""
        with _SUBSCRIPT_LOCK:
            cached = _SUBSCRIPTED_PAGES.get(item_type)
            if cached is None:
                cached = type(
                    f"Page[{item_type.__name__}]",
                    (cls,),
                    {"ITEM_TYPE": item_type, "__module__": cls.__module__},
                )
                _SUBSCRIPTED_PAGES[item_type] = cached
            return cast("type[Page[ItemT]]", cached)

    @classmethod
    def from_map(cls, body: Mapping[str, Any]) -> "Page[ItemT]":
        """Read a listing envelope, finding the records by shape rather than by name."""
        records: list[Any] | None = None
        if isinstance(body, Mapping):
            lists = [value for value in body.values() if isinstance(value, list)]
            if len(lists) == 1:
                records = lists[0]

        page = cls()
        item_type = cls.ITEM_TYPE
        if records is not None and item_type is not None:
            page.items = cast(
                "list[ItemT | None]",
                [
                    item_type.from_map(record) if isinstance(record, Mapping) else None
                    for record in records
                ],
            )
        else:
            page.items = records

        block = body.get("pagination") if isinstance(body, Mapping) else None
        page.pagination = Pagination.from_map(block) if isinstance(block, Mapping) else None
        return page
