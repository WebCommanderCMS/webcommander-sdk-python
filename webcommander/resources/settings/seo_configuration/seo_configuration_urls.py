"""Path templates for the SEO configuration settings endpoints."""

from __future__ import annotations

SEO_CONFIGURATION = "/api/{api_version}/admin/settings/seo_configuration"
SEO_CONFIGURATION_SECTION = "/api/{api_version}/admin/settings/seo_configuration/{section}"
SEO_CONFIGURATION_DOCUMENT_ROOT = (
    "/api/{api_version}/admin/settings/seo_configuration/document_root"
)
SEO_CONFIGURATION_DOCUMENT_ROOT_FILE = (
    "/api/{api_version}/admin/settings/seo_configuration/document_root/{config_key}"
)
SEO_CONFIGURATION_REDIRECTS = "/api/{api_version}/admin/settings/seo_configuration/redirects"
SEO_CONFIGURATION_REDIRECT = (
    "/api/{api_version}/admin/settings/seo_configuration/redirects/{redirect_id}"
)
