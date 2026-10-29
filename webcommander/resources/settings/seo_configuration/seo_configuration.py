"""SEO configuration endpoints, under ``/api/{api_version}/admin/settings/seo_configuration``.
A facade over three sections and two collections, ``document_root`` and ``redirects``."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.customers.admin_customers_dto import Page
from webcommander.resources.required_bodies import require_files, require_payload
from webcommander.resources.settings.seo_configuration import seo_configuration_urls
from webcommander.resources.settings.seo_configuration.seo_configuration_dto import (
    DocumentRootFile,
    Redirect,
    SeoConfiguration,
)

__all__ = [
    "get_seo_configuration",
    "patch_seo_configuration",
    "put_seo_configuration",
    "head_seo_configuration",
    "get_seo_configuration_section",
    "patch_seo_configuration_section",
    "put_seo_configuration_section",
    "get_seo_configuration_document_root",
    "head_seo_configuration_document_root",
    "upload_seo_configuration_document_root",
    "delete_seo_configuration_document_root_file",
    "get_seo_configuration_redirects",
    "head_seo_configuration_redirects",
    "create_seo_configuration_redirect",
    "get_seo_configuration_redirect",
    "head_seo_configuration_redirect",
    "patch_seo_configuration_redirect",
    "delete_seo_configuration_redirect",
]

SeoConfigurationPayload = Mapping[str, Any] | str | Dto


def get_seo_configuration(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SeoConfiguration]:
    """Read the whole area — ``GET /admin/settings/seo_configuration``."""
    return client.send_get_request(
        seo_configuration_urls.SEO_CONFIGURATION,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SeoConfiguration,
    )


def patch_seo_configuration(
    client: Any,
    payload: SeoConfigurationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SeoConfiguration]:
    """Write fields in one or more sections — ``PATCH /admin/settings/seo_configuration``.
    The body is wrapped in ``seo_configuration`` and partial at both levels."""
    require_payload(payload)
    return client.send_patch_request(
        seo_configuration_urls.SEO_CONFIGURATION,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SeoConfiguration,
    )


def put_seo_configuration(
    client: Any,
    payload: SeoConfigurationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SeoConfiguration]:
    """Replace the sections a body names — ``PUT /admin/settings/seo_configuration``.
    A named section's omitted fields are reset to their defaults, so send each one whole."""
    require_payload(payload)
    return client.send_put_request(
        seo_configuration_urls.SEO_CONFIGURATION,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SeoConfiguration,
    )


def head_seo_configuration(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/seo_configuration``; no body."""
    return client.send_api_request(
        "HEAD",
        seo_configuration_urls.SEO_CONFIGURATION,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_seo_configuration_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SeoConfiguration]:
    """Read one section — ``GET /admin/settings/seo_configuration/{section}``.
    ``.data`` is under the section's own key, with no ``group_meta``."""
    return client.send_get_request(
        seo_configuration_urls.SEO_CONFIGURATION_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SeoConfiguration,
    )


def patch_seo_configuration_section(
    client: Any,
    section: str,
    payload: SeoConfigurationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SeoConfiguration]:
    """Write fields in one section — ``PATCH /admin/settings/seo_configuration/{section}``.
    The body must be wrapped in the section's own key."""
    require_payload(payload)
    return client.send_patch_request(
        seo_configuration_urls.SEO_CONFIGURATION_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SeoConfiguration,
    )


def put_seo_configuration_section(
    client: Any,
    section: str,
    payload: SeoConfigurationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[SeoConfiguration]:
    """Replace one section — ``PUT /admin/settings/seo_configuration/{section}``; an omitted field
    is reset to its default, so send the section back whole."""
    require_payload(payload)
    return client.send_put_request(
        seo_configuration_urls.SEO_CONFIGURATION_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=SeoConfiguration,
    )


def get_seo_configuration_document_root(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page[DocumentRootFile]]:
    """List the files served from the document root; ``limit`` is a ceiling of 100.
    ``GET /admin/settings/seo_configuration/document_root``"""
    return client.send_get_request(
        seo_configuration_urls.SEO_CONFIGURATION_DOCUMENT_ROOT,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page.of(DocumentRootFile),
    )


def head_seo_configuration_document_root(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the document root listing is reachable; no body.
    ``HEAD /admin/settings/seo_configuration/document_root``"""
    return client.send_api_request(
        "HEAD",
        seo_configuration_urls.SEO_CONFIGURATION_DOCUMENT_ROOT,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def upload_seo_configuration_document_root(
    client: Any,
    files: Mapping[str, Any] | Sequence[tuple[str, Any]],
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[DocumentRootFile]:
    """Add a file to the document root; the part is ``file``, and a ``str`` is contents, not a path.
    ``POST /admin/settings/seo_configuration/document_root``"""
    require_files(files, "invalid_request")
    return client.send_post_request(
        seo_configuration_urls.SEO_CONFIGURATION_DOCUMENT_ROOT,
        files=files,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=DocumentRootFile,
    )


def delete_seo_configuration_document_root_file(
    client: Any,
    config_key: str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Stop serving one file; ``config_key`` is the store's id, not the file name.
    ``DELETE /admin/settings/seo_configuration/document_root/{config_key}``"""
    return client.send_delete_request(
        seo_configuration_urls.SEO_CONFIGURATION_DOCUMENT_ROOT_FILE,
        path_params={"config_key": config_key},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_seo_configuration_redirects(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Page[Redirect]]:
    """List the redirects — ``GET /admin/settings/seo_configuration/redirects``; the rows are
    under ``items``, and ``limit`` is a ceiling of 100."""
    return client.send_get_request(
        seo_configuration_urls.SEO_CONFIGURATION_REDIRECTS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Page.of(Redirect),
    )


def head_seo_configuration_redirects(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the redirects listing is reachable; no body.
    ``HEAD /admin/settings/seo_configuration/redirects``"""
    return client.send_api_request(
        "HEAD",
        seo_configuration_urls.SEO_CONFIGURATION_REDIRECTS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def create_seo_configuration_redirect(
    client: Any,
    payload: SeoConfigurationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Redirect]:
    """Add a redirect — ``POST /admin/settings/seo_configuration/redirects``; ``source_url`` and
    ``destination_url`` are both required."""
    require_payload(payload)
    return client.send_post_request(
        seo_configuration_urls.SEO_CONFIGURATION_REDIRECTS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Redirect,
    )


def get_seo_configuration_redirect(
    client: Any,
    redirect_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Redirect]:
    """Read one redirect — ``GET /admin/settings/seo_configuration/redirects/{redirect_id}``."""
    return client.send_get_request(
        seo_configuration_urls.SEO_CONFIGURATION_REDIRECT,
        path_params={"redirect_id": redirect_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Redirect,
    )


def head_seo_configuration_redirect(
    client: Any,
    redirect_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether one redirect is there; no body, and ``404`` for an unknown id.
    ``HEAD /admin/settings/seo_configuration/redirects/{redirect_id}``"""
    return client.send_api_request(
        "HEAD",
        seo_configuration_urls.SEO_CONFIGURATION_REDIRECT,
        path_params={"redirect_id": redirect_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def patch_seo_configuration_redirect(
    client: Any,
    redirect_id: int | str,
    payload: SeoConfigurationPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[Redirect]:
    """Change one redirect; partial, so a field left out stands.
    ``PATCH /admin/settings/seo_configuration/redirects/{redirect_id}``"""
    require_payload(payload)
    return client.send_patch_request(
        seo_configuration_urls.SEO_CONFIGURATION_REDIRECT,
        path_params={"redirect_id": redirect_id},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=Redirect,
    )


def delete_seo_configuration_redirect(
    client: Any,
    redirect_id: int | str,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Remove one redirect; ``204``, and nothing here restores it.
    ``DELETE /admin/settings/seo_configuration/redirects/{redirect_id}``"""
    return client.send_delete_request(
        seo_configuration_urls.SEO_CONFIGURATION_REDIRECT,
        path_params={"redirect_id": redirect_id},
        raise_on_error=raise_on_error,
        response_format=response_format,
    )
