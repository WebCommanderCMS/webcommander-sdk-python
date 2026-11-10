"""Gift card endpoints, under ``/api/{api_version}/admin``."""

from __future__ import annotations

from typing import Any, Mapping

from webcommander.client.api_response import ApiResponse
from webcommander.resources.gift_cards import gift_cards_urls
from webcommander.resources.gift_cards.gift_cards_dto import GiftCardPage

__all__ = ["list_gift_cards"]


def list_gift_cards(
    client: Any,
    query_params: Mapping[str, Any] | None = None,
    *,
    raise_on_error: bool | None = None,
    response_format: str | None = None,
) -> ApiResponse[GiftCardPage]:
    """List gift cards — ``GET /admin/gift_cards``, newest first. ``code`` matches a whole code and
    ``email`` a whole address, in any case; ``is_active`` takes ``true``, ``false``, ``1`` or
    ``0``, and ``limit`` caps at 20 with ``offset`` or ``page`` to move on. Any other name is
    ``400`` ``unknown_parameter``."""
    return client.send_get_request(
        gift_cards_urls.GIFT_CARDS,
        query_params=query_params,
        raise_on_error=raise_on_error,
        response_format=response_format,
        dto_type=GiftCardPage,
    )
