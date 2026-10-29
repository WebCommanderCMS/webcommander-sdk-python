"""Reaching an endpoint module as ``client.<resource>``: an explicit registry of name to module
path, so a typo raises, and :class:`BoundResource`, which applies the client to each function."""

from __future__ import annotations

import difflib
import functools
import importlib.util
import keyword
from importlib import import_module
from typing import Any

from webcommander.errors import SdkAttributeError, SdkUsageError

__all__ = [
    "BoundResource",
    "register_resource_module",
    "resolve_resource_module",
    "registered_resource_names",
]

_RESOURCE_MODULES: dict[str, str] = {
    "admin_customers": "webcommander.resources.customers.admin_customers",
    "aliases": "webcommander.resources.aliases.aliases",
    "animation_effects": "webcommander.resources.settings.animation_effects.animation_effects",
    "blog_categories": "webcommander.resources.blog_categories.blog_categories",
    "blogs": "webcommander.resources.blogs.blogs",
    "carts": "webcommander.resources.carts.carts",
    "categories": "webcommander.resources.categories.categories",
    "category_page": "webcommander.resources.settings.page_settings.category_page",
    "checkout_page": "webcommander.resources.settings.page_settings.checkout_page",
    "cities": "webcommander.resources.cities.cities",
    "common_settings": "webcommander.resources.common_settings.common_settings",
    "countries": "webcommander.resources.countries.countries",
    "currencies": "webcommander.resources.currencies.currencies",
    "customer_groups": "webcommander.resources.customer_groups.customer_groups",
    "customer_portal": "webcommander.resources.settings.customer_portal.customer_portal",
    "discount_profiles": "webcommander.resources.discount_profiles.discount_profiles",
    "ecommerce_settings": "webcommander.resources.settings.ecommerce_settings.ecommerce_settings",
    "email": "webcommander.resources.email.email",
    "inventory_locations": "webcommander.resources.inventory_locations.inventory_locations",
    "order_custom_fields": "webcommander.resources.order_custom_fields.order_custom_fields",
    "order_flags": "webcommander.resources.order_flags.order_flags",
    "orders": "webcommander.resources.orders.orders",
    "pages": "webcommander.resources.pages.pages",
    "payment_gateways": "webcommander.resources.payment_gateways.payment_gateways",
    "price_display_settings": (
        "webcommander.resources.settings.price_display_settings.price_display_settings"
    ),
    "product_listing": "webcommander.resources.settings.product_listing.product_listing",
    "product_page": "webcommander.resources.settings.page_settings.product_page",
    "products": "webcommander.resources.products.products",
    "search_result_page": "webcommander.resources.settings.page_settings.search_result_page",
    "search_settings": "webcommander.resources.settings.search_settings.search_settings",
    "seo_configuration": "webcommander.resources.settings.seo_configuration.seo_configuration",
    "shipping_classes": "webcommander.resources.shipping_classes.shipping_classes",
    "shipping_methods": "webcommander.resources.shipping_methods.shipping_methods",
    "shipping_settings": "webcommander.resources.settings.shipping_settings.shipping_settings",
    "shopping_cart": "webcommander.resources.settings.page_settings.shopping_cart",
    "site_settings": "webcommander.resources.settings.site_settings.site_settings",
    "tax_codes": "webcommander.resources.tax_codes.tax_codes",
    "tax_country_taxes": "webcommander.resources.tax_country_taxes.tax_country_taxes",
    "tax_custom_profiles": "webcommander.resources.tax_custom_profiles.tax_custom_profiles",
    "tax_profiles": "webcommander.resources.tax_profiles.tax_profiles",
    "tax_rules": "webcommander.resources.tax_rules.tax_rules",
    "tax_settings": "webcommander.resources.tax_settings.tax_settings",
    "tax_zones": "webcommander.resources.tax_zones.tax_zones",
    "transactions": "webcommander.resources.transactions.transactions",
    "trash": "webcommander.resources.trash.trash",
    "variations": "webcommander.resources.variations.variations",
}


def register_resource_module(resource_name: str, module_path: str) -> None:
    """Make a resource module reachable as ``client.<resource_name>``, from its importable path
    as a string; an unreachable name or a clashing re-registration raises ``SdkUsageError``."""
    if (
        not isinstance(resource_name, str)
        or resource_name.startswith("_")
        or not resource_name.isidentifier()
        or keyword.iskeyword(resource_name)
    ):
        raise SdkUsageError(f"cannot register {resource_name!r}: not a public identifier")
    if resource_name in _client_attribute_names():
        raise SdkUsageError(
            f"cannot register resource {resource_name!r}: WebCommanderClient "
            "already has an attribute of that name, and it would win every "
            "lookup — pick another name"
        )
    registered = _RESOURCE_MODULES.get(resource_name)
    if registered is not None and registered != module_path:
        raise SdkUsageError(
            f"cannot register resource {resource_name!r} against {module_path!r}: "
            f"it is already registered against {registered!r}, and clients built "
            f"before the change would keep the old one — pick another name"
        )
    if not _module_exists(module_path):
        raise SdkUsageError(
            f"cannot register resource {resource_name!r}: nothing importable at "
            f"{module_path!r} — check the module path"
        )
    _RESOURCE_MODULES[resource_name] = module_path


def _module_exists(module_path: str) -> bool:
    """Whether ``module_path`` names something importable; ``find_spec`` needs the guard
    because it *raises* when a parent package is missing."""
    try:
        return importlib.util.find_spec(module_path) is not None
    except (ImportError, AttributeError, ValueError, TypeError):
        return False


def _client_attribute_names() -> frozenset[str]:
    """Every attribute name :class:`WebCommanderClient` already answers by itself; the
    import is deferred, since at module scope it would cycle."""
    from webcommander.client.web_commander_client import WebCommanderClient

    return frozenset(dir(WebCommanderClient))


def registered_resource_names() -> tuple[str, ...]:
    """Every registered resource name, sorted — those reachable on a client."""
    return tuple(sorted(_RESOURCE_MODULES))


def resolve_resource_module(resource_name: str) -> Any:
    """Import the module registered under a resource name; an unknown one raises
    :class:`~webcommander.errors.SdkAttributeError`, an ``AttributeError``, so ``hasattr`` works."""
    module_path = _RESOURCE_MODULES.get(resource_name)
    if module_path is None:
        available = ", ".join(registered_resource_names()) or "none registered yet"
        raise SdkAttributeError(f"no resource {resource_name!r}; available: {available}")
    try:
        return import_module(module_path)
    except ImportError as error:
        # ``ImportError`` only: a ``SyntaxError`` is a real bug, not a missing name.
        raise SdkAttributeError(
            f"resource {resource_name!r} could not be imported from {module_path!r}",
            detail=str(error),
            cause=error,
        ) from None


class BoundResource:
    """A resource module with the client pre-applied as each function's first argument."""

    def __init__(self, client: Any, module: Any) -> None:
        self._client = client
        self._module = module

    def __getattr__(self, name: str) -> Any:
        """Bind one endpoint function with the client already applied, or say what this
        module offers, with a ``difflib`` suggestion when the name is close."""
        if name.startswith("_"):
            # Before the resolver: ``copy`` asks a half-built instance for ``__setstate__``.
            raise AttributeError(name)
        available = self._public_function_names()
        if name not in available:
            suggestion = difflib.get_close_matches(name, available, n=1)
            hint = f"; did you mean {suggestion[0]}?" if suggestion else ""
            raise SdkAttributeError(
                f"{self._module.__name__.rsplit('.', 1)[-1]} has no {name!r}{hint}"
            )
        target = getattr(self._module, name, None)
        if not callable(target):
            # ``partial`` on a non-callable raises ``TypeError``, which ``hasattr`` does not catch.
            raise SdkAttributeError(
                f"{self._module.__name__.rsplit('.', 1)[-1]} lists {name!r} in "
                f"__all__ but it is "
                f"{'not defined' if target is None else 'not callable'}, so it is "
                f"not an endpoint"
            )
        return functools.partial(target, self._client)

    def __deepcopy__(self, memo: dict[int, Any]) -> "BoundResource":
        """Copy the façade, sharing the client and the module — without this
        ``copy.deepcopy`` dies on the ``RLock`` inside the client's logger."""
        clone = BoundResource(self._client, self._module)
        memo[id(self)] = clone
        return clone

    def _public_function_names(self) -> list[str]:
        """The endpoint names, read from ``__all__`` so imported names are not offered."""
        declared = getattr(self._module, "__all__", None)
        if isinstance(declared, (list, tuple, set, frozenset)):
            return sorted(str(entry) for entry in declared)
        # A bare string is a forgotten list, read as no declaration rather than as characters.
        return sorted(
            attribute
            for attribute in dir(self._module)
            if not attribute.startswith("_") and callable(getattr(self._module, attribute))
        )

    def __dir__(self) -> list[str]:
        return self._public_function_names()
