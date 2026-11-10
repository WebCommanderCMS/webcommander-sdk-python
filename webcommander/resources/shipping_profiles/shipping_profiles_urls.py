"""Path templates for the shipping profile endpoints."""

from __future__ import annotations

SHIPPING_PROFILES = "/api/{api_version}/admin/shipping_profiles"
SHIPPING_PROFILES_COUNT = "/api/{api_version}/admin/shipping_profiles/count"
SHIPPING_PROFILES_WIZARD = "/api/{api_version}/admin/shipping_profiles/wizard"
SHIPPING_PROFILE = "/api/{api_version}/admin/shipping_profiles/{shipping_profile_id}"

#: Files the record under a transaction number; it wins over a ``transaction_no`` in the body.
TRANSACTION_NO_HEADER = "X-Transaction-No"
