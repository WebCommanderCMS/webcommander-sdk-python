"""Path templates for the shipping class endpoints."""

from __future__ import annotations

SHIPPING_CLASSES = "/api/{api_version}/admin/shipping_classes"
SHIPPING_CLASSES_COUNT = "/api/{api_version}/admin/shipping_classes/count"
SHIPPING_CLASS = "/api/{api_version}/admin/shipping_classes/{shipping_class_id}"
SHIPPING_CLASS_DEFAULT = "/api/{api_version}/admin/shipping_classes/{shipping_class_id}/default"
