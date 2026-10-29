"""Path templates for the payment gateway endpoints."""

from __future__ import annotations

PAYMENT_GATEWAYS = "/api/{api_version}/admin/payment_gateways"
PAYMENT_GATEWAYS_COUNT = "/api/{api_version}/admin/payment_gateways/count"
PAYMENT_GATEWAY = "/api/{api_version}/admin/payment_gateways/{payment_gateway_id}"
