"""Domain alias endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.aliases import aliases_urls
from webcommander.resources.aliases.aliases_dto import Alias, AliasPage
from webcommander.resources.required_bodies import require_payload

__all__ = [
    "list_aliases",
    "head_aliases",
    "create_alias",
    "delete_alias",
]

AliasPayload = Mapping[str, Any] | str | Dto


def list_aliases(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AliasPage]:
    """List the aliases — ``GET /admin/aliases``, a created row listed last. Takes ``limit``
    (capped at 20), ``offset``, ``page`` and ``field_metadata``; any other name is 400."""
    return client.send_get_request(
        aliases_urls.ALIASES,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AliasPage,
    )


def head_aliases(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the collection answers — ``HEAD /admin/aliases``; 200 with no body."""
    return client.send_api_request(
        "HEAD",
        aliases_urls.ALIASES,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_alias(
    client: Any,
    payload: AliasPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Alias]:
    """Create an alias — ``POST /admin/aliases``, ``{"alias": "<hostname>"}`` bare, 201 with the
    row under ``alias``. A hostname taken in any letter case is 409."""
    require_payload(payload)
    return client.send_post_request(
        aliases_urls.ALIASES,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Alias,
    )


def delete_alias(
    client: Any,
    alias_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Delete one alias — ``DELETE /admin/aliases/{alias_id}``, 204 and hard; an unknown id is
    404. The row path has no read, so a delete shows only as the id leaving the listing."""
    return client.send_delete_request(
        aliases_urls.ALIAS,
        path_params={"alias_id": alias_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
