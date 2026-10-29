"""Search settings endpoints, under ``/api/{api_version}/admin/settings/search_settings``.
Writing ``synonyms`` triggers a reindex that cannot be undone."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.search_settings import search_settings_urls
from webcommander.resources.settings.search_settings.search_settings_dto import (
    ReindexStatus,
    SearchSettings,
)

__all__ = [
    "get_search_settings",
    "patch_search_settings",
    "put_search_settings",
    "head_search_settings",
    "get_search_settings_section",
    "patch_search_settings_section",
    "put_search_settings_section",
    "get_search_settings_reindex_status",
    "head_search_settings_reindex_status",
]

SearchSettingsPayload = Mapping[str, Any] | str | Dto


def get_search_settings(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SearchSettings]:
    """Read the whole area — ``GET /admin/settings/search_settings``, every section inlined."""
    return client.send_get_request(
        search_settings_urls.SEARCH_SETTINGS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SearchSettings,
    )


def patch_search_settings(
    client: Any,
    payload: SearchSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SearchSettings]:
    """Write fields in one or more sections — ``PATCH /admin/settings/search_settings``.
    The body must be wrapped in ``search_settings``."""
    require_payload(payload)
    return client.send_patch_request(
        search_settings_urls.SEARCH_SETTINGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SearchSettings,
    )


def put_search_settings(
    client: Any,
    payload: SearchSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SearchSettings]:
    """Replace the whole area — ``PUT /admin/settings/search_settings``; what a body leaves out is
    reset, ``synonyms`` included."""
    require_payload(payload)
    return client.send_put_request(
        search_settings_urls.SEARCH_SETTINGS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SearchSettings,
    )


def head_search_settings(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/search_settings``; no body."""
    return client.send_api_request(
        "HEAD",
        search_settings_urls.SEARCH_SETTINGS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_search_settings_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SearchSettings]:
    """Read one section — ``GET /admin/settings/search_settings/{section}``.
    ``.data`` is under the section's own key, with no ``group_meta``."""
    return client.send_get_request(
        search_settings_urls.SEARCH_SETTINGS_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SearchSettings,
    )


def patch_search_settings_section(
    client: Any,
    section: str,
    payload: SearchSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SearchSettings]:
    """Write fields in one section — ``PATCH /admin/settings/search_settings/{section}``.
    The body takes the section's own key and nothing else."""
    require_payload(payload)
    return client.send_patch_request(
        search_settings_urls.SEARCH_SETTINGS_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SearchSettings,
    )


def put_search_settings_section(
    client: Any,
    section: str,
    payload: SearchSettingsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SearchSettings]:
    """Replace one section — ``PUT /admin/settings/search_settings/{section}``; what the body
    leaves out is reset, so send the whole section."""
    require_payload(payload)
    return client.send_put_request(
        search_settings_urls.SEARCH_SETTINGS_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SearchSettings,
    )


def get_search_settings_reindex_status(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[ReindexStatus]:
    """Read where the reindex stands; read-only and bare, with no wrapper and no ``group_meta``.
    ``GET /admin/settings/search_settings/reindex_status``"""
    return client.send_get_request(
        search_settings_urls.SEARCH_SETTINGS_REINDEX_STATUS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=ReindexStatus,
    )


def head_search_settings_reindex_status(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the reindex status is reachable; no body.
    ``HEAD /admin/settings/search_settings/reindex_status``"""
    return client.send_api_request(
        "HEAD",
        search_settings_urls.SEARCH_SETTINGS_REINDEX_STATUS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
