"""Path templates for the discount profile endpoints."""

from __future__ import annotations

DISCOUNT_PROFILES = "/api/{api_version}/admin/discount_profiles"
DISCOUNT_PROFILE = "/api/{api_version}/admin/discount_profiles/{discount_profile_id}"
DISCOUNT_PROFILE_CREATE_COUPONS = (
    "/api/{api_version}/admin/discount_profiles/{discount_profile_id}/create-coupons"
)
DISCOUNT_COUPONS_ASSIGN_CUSTOMER = "/api/{api_version}/admin/discount_coupons/assign-customer"
