"""Animation effects endpoints, under ``/api/{api_version}/admin/settings/animation_effects``.
The area is a facade over five sections; a section is a path value."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.dto import Dto
from webcommander.resources.required_bodies import require_payload
from webcommander.resources.settings.animation_effects import animation_effects_urls
from webcommander.resources.settings.animation_effects.animation_effects_dto import (
    AnimationEffects,
)

__all__ = [
    "get_animation_effects",
    "patch_animation_effects",
    "head_animation_effects",
    "get_animation_effects_section",
    "patch_animation_effects_section",
]

AnimationEffectsPayload = Mapping[str, Any] | str | Dto


def get_animation_effects(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AnimationEffects]:
    """Read the whole area — ``GET /admin/settings/animation_effects``, every section inlined."""
    return client.send_get_request(
        animation_effects_urls.ANIMATION_EFFECTS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AnimationEffects,
    )


def patch_animation_effects(
    client: Any,
    payload: AnimationEffectsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AnimationEffects]:
    """Write fields in one or more sections — ``PATCH /admin/settings/animation_effects``.
    The body must be wrapped in ``animation_effects``."""
    require_payload(payload)
    return client.send_patch_request(
        animation_effects_urls.ANIMATION_EFFECTS,
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AnimationEffects,
    )


def head_animation_effects(
    client: Any,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse:
    """Ask whether the area is reachable — ``HEAD /admin/settings/animation_effects``; no body."""
    return client.send_api_request(
        "HEAD",
        animation_effects_urls.ANIMATION_EFFECTS,
        raise_on_error=raise_on_error,
        response_format=response_format,
    )


def get_animation_effects_section(
    client: Any,
    section: str,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AnimationEffects]:
    """Read one section — ``GET /admin/settings/animation_effects/{section}``.
    ``.data`` is under the section's own key, with no ``group_meta``."""
    return client.send_get_request(
        animation_effects_urls.ANIMATION_EFFECTS_SECTION,
        path_params={"section": section},
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AnimationEffects,
    )


def patch_animation_effects_section(
    client: Any,
    section: str,
    payload: AnimationEffectsPayload,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[AnimationEffects]:
    """Write fields in one section — ``PATCH /admin/settings/animation_effects/{section}``.
    The body takes the section's own key and nothing else."""
    require_payload(payload)
    return client.send_patch_request(
        animation_effects_urls.ANIMATION_EFFECTS_SECTION,
        path_params={"section": section},
        json_body=payload,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=AnimationEffects,
    )
