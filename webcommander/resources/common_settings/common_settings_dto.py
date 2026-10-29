"""Typed views over the common settings bodies."""

from __future__ import annotations

from typing import Any

from webcommander.dto import Dto


class Setting(Dto):
    """One entry of a settings group, for a write's lists; a read's entries have the same keys.
    Reads answer ``value`` as text, ``***`` for a masked one; a number written is stored as text."""

    config_key: str | None = None
    value: str | None = None


class CommonSettings(Dto):
    """What the read and both writes answer: ``settings``, group name to a list of
    ``{"config_key", "value"}`` mappings. The ``notifications`` group alone is a name to
    ``bool`` map, so the groups stay a plain mapping."""

    settings: Any = None


class CommonSettingsInput(Dto):
    """The list form both writes take: ``settings`` maps a group name to a list of
    :class:`Setting` entries, ``{"config_key", "value"}`` each. A group may instead be
    ``{config_key: value}`` or ``{name: {"config_key", "value"}}``; send those as a mapping
    or a JSON string. Keyed by group name, so ``settings`` is not a typed field."""

    settings: Any = None


class CustomerFieldConfigs(Dto):
    """The registration form's ``fields_configs``: six keys for each of the store's 20 fields.
    ``_order`` reads as text; ``_active`` and ``_required`` are booleans here, though the
    settings read answers them as text."""

    first_name_order: str | None = None
    first_name_key: str | None = None
    first_name_label: str | None = None
    first_name_placeholder: str | None = None
    first_name_active: bool | None = None
    first_name_required: bool | None = None
    last_name_order: str | None = None
    last_name_key: str | None = None
    last_name_label: str | None = None
    last_name_placeholder: str | None = None
    last_name_active: bool | None = None
    last_name_required: bool | None = None
    address_line_1_order: str | None = None
    address_line_1_key: str | None = None
    address_line_1_label: str | None = None
    address_line_1_placeholder: str | None = None
    address_line_1_active: bool | None = None
    address_line_1_required: bool | None = None
    address_line_2_order: str | None = None
    address_line_2_key: str | None = None
    address_line_2_label: str | None = None
    address_line_2_placeholder: str | None = None
    address_line_2_active: bool | None = None
    address_line_2_required: bool | None = None
    post_code_order: str | None = None
    post_code_key: str | None = None
    post_code_label: str | None = None
    post_code_placeholder: str | None = None
    post_code_active: bool | None = None
    post_code_required: bool | None = None
    city_order: str | None = None
    city_key: str | None = None
    city_label: str | None = None
    city_placeholder: str | None = None
    city_active: bool | None = None
    city_required: bool | None = None
    phone_order: str | None = None
    phone_key: str | None = None
    phone_label: str | None = None
    phone_placeholder: str | None = None
    phone_active: bool | None = None
    phone_required: bool | None = None
    mobile_order: str | None = None
    mobile_key: str | None = None
    mobile_label: str | None = None
    mobile_placeholder: str | None = None
    mobile_active: bool | None = None
    mobile_required: bool | None = None
    fax_order: str | None = None
    fax_key: str | None = None
    fax_label: str | None = None
    fax_placeholder: str | None = None
    fax_active: bool | None = None
    fax_required: bool | None = None
    email_order: str | None = None
    email_key: str | None = None
    email_label: str | None = None
    email_placeholder: str | None = None
    email_active: bool | None = None
    email_required: bool | None = None
    confirm_email_order: str | None = None
    confirm_email_key: str | None = None
    confirm_email_label: str | None = None
    confirm_email_placeholder: str | None = None
    confirm_email_active: bool | None = None
    confirm_email_required: bool | None = None
    password_order: str | None = None
    password_key: str | None = None
    password_label: str | None = None
    password_placeholder: str | None = None
    password_active: bool | None = None
    password_required: bool | None = None
    retype_password_order: str | None = None
    retype_password_key: str | None = None
    retype_password_label: str | None = None
    retype_password_placeholder: str | None = None
    retype_password_active: bool | None = None
    retype_password_required: bool | None = None
    country_order: str | None = None
    country_key: str | None = None
    country_label: str | None = None
    country_placeholder: str | None = None
    country_active: bool | None = None
    country_required: bool | None = None
    customer_type_order: str | None = None
    customer_type_key: str | None = None
    customer_type_label: str | None = None
    customer_type_placeholder: str | None = None
    customer_type_active: bool | None = None
    customer_type_required: bool | None = None
    sex_order: str | None = None
    sex_key: str | None = None
    sex_label: str | None = None
    sex_placeholder: str | None = None
    sex_active: bool | None = None
    sex_required: bool | None = None
    abn_order: str | None = None
    abn_key: str | None = None
    abn_label: str | None = None
    abn_placeholder: str | None = None
    abn_active: bool | None = None
    abn_required: bool | None = None
    abn_branch_order: str | None = None
    abn_branch_key: str | None = None
    abn_branch_label: str | None = None
    abn_branch_placeholder: str | None = None
    abn_branch_active: bool | None = None
    abn_branch_required: bool | None = None
    company_name_order: str | None = None
    company_name_key: str | None = None
    company_name_label: str | None = None
    company_name_placeholder: str | None = None
    company_name_active: bool | None = None
    company_name_required: bool | None = None
    date_of_birth_order: str | None = None
    date_of_birth_key: str | None = None
    date_of_birth_label: str | None = None
    date_of_birth_placeholder: str | None = None
    date_of_birth_active: bool | None = None
    date_of_birth_required: bool | None = None


class CustomerFields(Dto):
    """The registration form: ``fields`` lists the active fields' keys in their order, and
    ``fields_configs`` configures every field, inactive ones included."""

    fields: list[str | None] | None = None
    fields_configs: CustomerFieldConfigs | None = None
