"""The refusals the endpoint functions share: a body the endpoint needs and was not given."""

from __future__ import annotations

from typing import Any

from webcommander.errors import SdkUsageError


def require_payload(payload: Any) -> None:
    if payload is None:
        raise SdkUsageError("payload is required")


def require_files(files: Any, store_error: str) -> None:
    if files is None:
        raise SdkUsageError(
            "files is required: this endpoint's whole body is the upload, and "
            "None sends no multipart body at all, which the store answers 400 "
            f"{store_error} with field 'file', code 'required'"
        )
    # Only sized containers are checked for emptiness: testing a generator would consume it.
    if hasattr(files, "__len__") and len(files) == 0:
        raise SdkUsageError(
            f"files must name the file to upload, got the empty "
            f"{type(files).__name__} {files!r} — an empty container sends no "
            f"multipart body at all, which the store answers 400 {store_error} "
            f"with field 'file', code 'required'. Pass {{'file': handle}}"
        )
