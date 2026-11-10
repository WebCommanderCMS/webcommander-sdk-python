"""Shipping rule endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.shipping_rules import shipping_rules_urls
from webcommander.resources.shipping_rules.shipping_rules_dto import (
    ShippingRule,
    ShippingRuleCount,
    ShippingRuleListing,
)

__all__ = [
    "list_shipping_rules",
    "head_shipping_rules",
    "count_shipping_rules",
    "head_shipping_rules_count",
    "create_shipping_rule",
    "get_shipping_rule",
    "head_shipping_rule",
    "update_shipping_rule",
    "patch_shipping_rule",
    "delete_shipping_rule",
]

ShippingRulePayload = Mapping[str, Any] | str | Dto


def list_shipping_rules(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRuleListing]:
    """List the rules, newest first — ``GET /admin/shipping_rules``. ``search`` (part of the
    name), ``shipping_class_id``, ``zone_id``, ``method`` (the method of the rule's rate) and
    ``handling_cost`` (``with_handling`` or ``without_handling``) filter, each rule listed once;
    ``sort`` is ``id``, ``name``, ``description``, ``created_at``, ``updated_at`` or
    ``transaction_no`` with ``order`` ``asc`` or ``desc``; ``limit`` is 1 to 100 and defaults to
    20, ``offset`` pages. An unknown value or an id that names no record is ``400``."""
    return client.send_get_request(
        shipping_rules_urls.SHIPPING_RULES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRuleListing,
    )


def head_shipping_rules(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/shipping_rules``; no body."""
    return client.send_api_request(
        "HEAD",
        shipping_rules_urls.SHIPPING_RULES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def count_shipping_rules(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRuleCount]:
    """How many rules match — ``GET /admin/shipping_rules/count``, a bare ``{"total": N}``. The
    listing's filters narrow it."""
    return client.send_get_request(
        shipping_rules_urls.SHIPPING_RULES_COUNT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRuleCount,
    )


def head_shipping_rules_count(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the count is reachable — ``HEAD /admin/shipping_rules/count``; no body."""
    return client.send_api_request(
        "HEAD",
        shipping_rules_urls.SHIPPING_RULES_COUNT,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_shipping_rule(
    client: Any,
    payload: ShippingRulePayload,
    *,
    transaction_no: str | None = None,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRule]:
    """Create a rule — ``POST /admin/shipping_rules``, answered ``201`` with a ``Location``. The
    body is wrapped in ``shipping_rule`` and needs ``name``, unique without regard to case
    (``409``). A class, a rate and every zone must exist, ``zones`` without a repeat; a
    ``profile_id`` adds the rule to that profile. An unknown field, an ``id`` or an unwrapped body
    is ``400``. ``transaction_no`` is sent as ``X-Transaction-No``."""
    require_payload(payload)
    return client.send_post_request(
        shipping_rules_urls.SHIPPING_RULES,
        json_body=payload,
        headers=None
        if transaction_no is None
        else {shipping_rules_urls.TRANSACTION_NO_HEADER: transaction_no},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRule,
    )


def get_shipping_rule(
    client: Any,
    shipping_rule_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRule]:
    """Retrieve one rule by its ``id`` — ``GET /admin/shipping_rules/{shipping_rule_id}``, the row
    under ``shipping_rule``. An id that is not plain digits, or unknown, is ``404``."""
    return client.send_get_request(
        shipping_rules_urls.SHIPPING_RULE,
        path_params={"shipping_rule_id": shipping_rule_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRule,
    )


def head_shipping_rule(
    client: Any,
    shipping_rule_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether a rule exists — ``HEAD /admin/shipping_rules/{shipping_rule_id}``; 200 with no
    body, 404 for an unknown id."""
    return client.send_api_request(
        "HEAD",
        shipping_rules_urls.SHIPPING_RULE,
        path_params={"shipping_rule_id": shipping_rule_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_shipping_rule(
    client: Any,
    shipping_rule_id: int | str,
    payload: ShippingRulePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRule]:
    """Replace one rule — ``PUT /admin/shipping_rules/{shipping_rule_id}``. ``name``,
    ``description``, ``shipping_class``, ``shipping_rate`` and ``zones`` are all required; the
    first three may be ``None`` and ``zones`` ``[]``. The rate and the zones themselves stay."""
    require_payload(payload)
    return client.send_put_request(
        shipping_rules_urls.SHIPPING_RULE,
        path_params={"shipping_rule_id": shipping_rule_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRule,
    )


def patch_shipping_rule(
    client: Any,
    shipping_rule_id: int | str,
    payload: ShippingRulePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ShippingRule]:
    """Change only the fields sent — ``PATCH /admin/shipping_rules/{shipping_rule_id}``.
    ``zones`` is the full list, so ``[]`` takes every zone off; ``shipping_rate`` and
    ``shipping_class`` ``None`` take the rate or the class off. The records themselves stay."""
    require_payload(payload)
    return client.send_patch_request(
        shipping_rules_urls.SHIPPING_RULE,
        path_params={"shipping_rule_id": shipping_rule_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ShippingRule,
    )


def delete_shipping_rule(
    client: Any,
    shipping_rule_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one rule — ``DELETE /admin/shipping_rules/{shipping_rule_id}``, ``204``. Its rate
    and zones stay. A rule on a profile is ``409`` until it is taken off."""
    return client.send_delete_request(
        shipping_rules_urls.SHIPPING_RULE,
        path_params={"shipping_rule_id": shipping_rule_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
