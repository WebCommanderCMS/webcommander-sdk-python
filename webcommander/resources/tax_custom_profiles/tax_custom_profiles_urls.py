"""Path templates for the custom tax profile endpoints."""

from __future__ import annotations

TAX_CUSTOM_PROFILES = "/api/{api_version}/admin/tax/custom-profiles"
TAX_CUSTOM_PROFILE = "/api/{api_version}/admin/tax/custom-profiles/{custom_profile_id}"

#: Files a new profile under this transaction number; a differing ``transaction_no`` beside the wrapper is ``400 header_body_mismatch``, one inside is not compared.
TRANSACTION_NO_HEADER = "X-Transaction-No"
