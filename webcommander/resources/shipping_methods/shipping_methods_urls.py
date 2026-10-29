"""Path templates for the shipping method endpoints."""

from __future__ import annotations

SHIPPING_METHODS = "/api/{api_version}/admin/shipping_methods"
SHIPPING_METHODS_COUNT = "/api/{api_version}/admin/shipping_methods/count"
SHIPPING_METHOD = "/api/{api_version}/admin/shipping_methods/{shipping_method_id}"
SHIPPING_METHOD_DEFAULT = "/api/{api_version}/admin/shipping_methods/{shipping_method_id}/default"
