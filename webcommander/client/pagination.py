"""Walking a paginated listing without hand-rolling the loop."""

from __future__ import annotations

from typing import Any, Iterator, Mapping
from urllib.parse import urljoin

from webcommander.client.api_response import ApiResponse, comparison_url
from webcommander.errors import SdkError, SdkUsageError

__all__ = ["iter_pages", "iter_records"]

_PAGINATION_KEY = "pagination"
_NEXT_PAGE_KEY = "next_page"


def iter_pages(
    client: Any,
    path: str,
    *,
    query_params: Mapping[str, Any] | None = None,
    max_pages: int | None = None,
    raise_on_error: bool = True,
) -> Iterator[ApiResponse]:
    """Yield one :class:`ApiResponse` per page, following ``pagination.next_page``. ``query_params``
    applies to the first request only; a revisited ``next_page`` is an error, not a loop."""
    if max_pages is not None and (
        not isinstance(max_pages, int) or isinstance(max_pages, bool) or max_pages < 1
    ):
        raise SdkUsageError(f"max_pages: expected a positive integer or None, got {max_pages!r}")

    # Unredacted URLs: the printable copies are redacted, so two links can look alike.
    visited: set[str] = set()
    pages_yielded = 0
    response = client.send_get_request(
        path, query_params=query_params, raise_on_error=raise_on_error
    )
    current_url = comparison_url(response.request_info)
    if current_url:
        visited.add(current_url)
    while True:
        yield response
        pages_yielded += 1
        if not response.succeeded:
            return
        if max_pages is not None and pages_yielded >= max_pages:
            return
        next_page = _read_next_page(response.map)
        if next_page is None:
            return
        candidate = urljoin(current_url, next_page) if current_url else next_page
        if candidate in visited:
            # Neither the link nor the comparison key is echoed.
            endpoint = response.request_info.endpoint_template or "the listing"
            raise SdkError(
                f"pagination loop: next_page repeats after {pages_yielded} page(s) of {endpoint}"
            )
        response = client.send_get_request(next_page, raise_on_error=raise_on_error)
        visited.add(candidate)
        fetched = comparison_url(response.request_info)
        if fetched:
            current_url = fetched
            visited.add(fetched)


def iter_records(
    client: Any,
    path: str,
    record_key: str,
    *,
    query_params: Mapping[str, Any] | None = None,
    max_pages: int | None = None,
) -> Iterator[Any]:
    """Yield each record of a listing across every page; ``record_key`` names the envelope key
    holding them, since an envelope can carry more than one list."""
    if not isinstance(record_key, str) or not record_key.strip():
        raise SdkUsageError(
            f"record_key: expected the envelope key holding the records, "
            f"like 'customers', got {record_key!r}"
        )
    for page in iter_pages(
        client,
        path,
        query_params=query_params,
        max_pages=max_pages,
        raise_on_error=True,
    ):
        body = page.map
        records = body.get(record_key) if isinstance(body, Mapping) else None
        if not isinstance(records, list):
            available = (
                ", ".join(sorted(str(key) for key in body))
                if isinstance(body, Mapping)
                else f"a {type(body).__name__} body"
            )
            raise SdkUsageError(
                f"record_key {record_key!r}: this page has no list under that "
                f"key; it carries {available}"
            )
        yield from records


def _read_next_page(data: Any) -> str | None:
    if not isinstance(data, Mapping):
        return None
    pagination = data.get(_PAGINATION_KEY)
    if not isinstance(pagination, Mapping):
        return None
    next_page = pagination.get(_NEXT_PAGE_KEY)
    if isinstance(next_page, str) and next_page.strip():
        return next_page
    return None
