"""Tax rule endpoints, under ``/api/{api_version}/admin/tax_rules``.
``code`` and ``zones`` read as the rule's references, but no write sets either."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.tax_rules import tax_rules_urls
from webcommander.resources.tax_rules.tax_rules_dto import TaxRule, TaxRulePage

__all__ = [
    "list_tax_rules",
    "head_tax_rules",
    "create_tax_rule",
    "get_tax_rule",
    "head_tax_rule",
    "update_tax_rule",
    "delete_tax_rule",
]

TaxRulePayload = Mapping[str, Any] | str | Dto


def list_tax_rules(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxRulePage]:
    """List the tax rules — ``GET /admin/tax_rules``. ``limit`` is capped at 100."""
    return client.send_get_request(
        tax_rules_urls.TAX_RULES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxRulePage,
    )


def head_tax_rules(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection is reachable — ``HEAD /admin/tax_rules``; no body."""
    return client.send_api_request(
        "HEAD",
        tax_rules_urls.TAX_RULES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_tax_rule(
    client: Any,
    payload: TaxRulePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxRule]:
    """Create a tax rule — ``POST /admin/tax_rules``, answered ``201``. The body is wrapped in
    ``tax_rule``; only ``name`` and ``description`` are read."""
    require_payload(payload)
    return client.send_post_request(
        tax_rules_urls.TAX_RULES,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxRule,
    )


def get_tax_rule(
    client: Any,
    tax_rule_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxRule]:
    """Retrieve one tax rule — ``GET /admin/tax_rules/{tax_rule_id}``."""
    return client.send_get_request(
        tax_rules_urls.TAX_RULE,
        path_params={"tax_rule_id": tax_rule_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxRule,
    )


def head_tax_rule(
    client: Any,
    tax_rule_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one tax rule is there — ``HEAD /admin/tax_rules/{tax_rule_id}``; no body.
    An id no row holds is ``200`` too, so this does not prove the row exists."""
    return client.send_api_request(
        "HEAD",
        tax_rules_urls.TAX_RULE,
        path_params={"tax_rule_id": tax_rule_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def update_tax_rule(
    client: Any,
    tax_rule_id: int | str,
    payload: TaxRulePayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[TaxRule]:
    """Update one tax rule — ``PUT /admin/tax_rules/{tax_rule_id}``; a merge, wrapped in
    ``tax_rule``."""
    require_payload(payload)
    return client.send_put_request(
        tax_rules_urls.TAX_RULE,
        path_params={"tax_rule_id": tax_rule_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=TaxRule,
    )


def delete_tax_rule(
    client: Any,
    tax_rule_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one tax rule — ``DELETE /admin/tax_rules/{tax_rule_id}``; ``204``, no body."""
    return client.send_delete_request(
        tax_rules_urls.TAX_RULE,
        path_params={"tax_rule_id": tax_rule_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
