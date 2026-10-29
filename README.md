# WebCommander Python SDK

A Python client for the WebCommander v4 REST API.

## Requirements

- Python 3.10 or newer (3.10 to 3.13 supported)
- `requests>=2.32.4`, `urllib3>=1.21.1` and `portalocker>=2.8.0`, installed with the package
- OAuth2 client credentials for a WebCommander store

## Installation

```bash
pip install webcommander
```

Check the install:

```bash
python -c "import webcommander; print(webcommander.__version__)"
```

## Quick start

The SDK reads no credentials from the environment. Your code builds an `AuthConfig` from
wherever the credentials live and registers it once:

```python
import os

from webcommander import AuthConfig, build_client, register_instances

register_instances([
    AuthConfig(
        client_name="default",
        base_url=os.environ["WC_BASE_URL"],
        client_id=os.environ["WC_CLIENT_ID"],
        client_secret=os.environ["WC_CLIENT_SECRET"],
        redirect_uri=os.environ["WC_REDIRECT_URI"],
        auth_string=os.environ["WC_AUTH_STRING"],
    ),
])

with build_client() as client:
    response = client.admin_customers.get_customers({"limit": 20})
    if response.succeeded:
        for customer in response.map["customers"]:
            print(customer["customer_id"], customer["email"])
    else:
        print(response.status_code, response.get_error_messages())
```

The client authenticates on the first call, caches the token and renews it before it expires.
To load a `.env` file, call `load_dotenv()` yourself before building the `AuthConfig`.

## Configuration

Credentials are an `AuthConfig`. Behaviour is set with keyword arguments to `build_client`.
Every setting has a default; `raise_on_error` defaults to `False` and `response_format` to
`"map"`:

```python
client = build_client(
    timeout_seconds=30.0,
    max_retries=3,
    raise_on_error=True,
    response_format="map",
    log_level="INFO",
)
```

Register several `AuthConfig` blocks to talk to several stores; the first is the default:

```python
build_client()                    # the first registered instance
build_client(instance="staging")  # by client_name
build_client(instance=1)          # by position
```

Configuration is frozen once built. A closed client raises `SdkUsageError` on the next call.

## Usage

### Bound and explicit calls

Every endpoint function takes the client as its first argument. You can call it through the
client's resource accessor or import it:

```python
from webcommander.resources.customers.admin_customers import get_customer

client.admin_customers.get_customer(1192)   # bound
get_customer(client, 1192)                  # explicit, same function
```

For an endpoint the SDK does not wrap, use the client's generic senders:
`client.send_get_request`, `send_post_request`, `send_put_request`, `send_patch_request`,
`send_delete_request` and `send_api_request`.

### Payload forms

A payload can be a mapping, the same body as a JSON string, or a typed input from the
resource's `*_dto.py` module. A mapping and the equivalent DTO send identical bytes; a JSON
string is sent as written.

```python
from webcommander.resources.customers.admin_customers_dto import CustomerInput

client.admin_customers.create_customer({"customer": {"first_name": "Jane", "email": "jane@example.com"}})
client.admin_customers.create_customer('{"customer": {"first_name": "Jane", "email": "jane@example.com"}}')
client.admin_customers.create_customer(CustomerInput(first_name="Jane", email="jane@example.com"))
```

### Response forms

Every response carries the body in three forms, whatever is configured:

```python
response = client.admin_customers.get_customers({"limit": 20})

response.map["customers"][0]["email"]   # the decoded body: dict, list, str or bytes
response.json                           # the store's own body text
response.dto.items[0].email             # the typed view
response.data                           # whichever form response_format selects ("map" by default)
```

### Pagination

`iter_records` follows `pagination.next_page` for you and yields each record:

```python
from webcommander import iter_records

for customer in iter_records(client, "/api/{api_version}/admin/customers", "customers",
                             query_params={"limit": 20}):
    print(customer["customer_id"])
```

`iter_pages` yields one response per page instead.

## Error handling

By default a failed call returns a response rather than raising. A call fails on a non-2xx
status, or on a `2xx` whose body carries a falsy `isSuccess`, which the store sends for a
path it cannot route.

```python
response = client.admin_customers.get_customer(999999)
if not response.succeeded:
    print(response.status_code, response.error_type, response.get_error_messages())
```

Pass `raise_on_error=True` to `build_client` or to one call to raise `SdkError` instead:

```python
from webcommander import SdkError

try:
    client.admin_customers.get_customer(999999, raise_on_error=True)
except SdkError as error:
    print(error.status_code, error.error_type.value)   # 404 not_found
    print(error.get_error_messages())                  # ['Customer Not Found']
    print(error.explain())
```

Every exception the SDK raises is an `SdkError` subclass.

## Resources

The client exposes 46 resources with 349 operations. The method, path and behaviour of each
one are in the [API reference](https://newlify.mintlify.app).

| Resource | Client accessor | Operations |
|---|---|---:|
| Customers | `client.admin_customers` | 15 |
| Aliases | `client.aliases` | 4 |
| Animation effects settings | `client.animation_effects` | 5 |
| Blog categories | `client.blog_categories` | 5 |
| Blogs | `client.blogs` | 12 |
| Carts | `client.carts` | 7 |
| Categories | `client.categories` | 10 |
| Category page settings | `client.category_page` | 5 |
| Checkout page settings | `client.checkout_page` | 5 |
| Cities | `client.cities` | 2 |
| Common settings | `client.common_settings` | 6 |
| Countries | `client.countries` | 8 |
| Currencies | `client.currencies` | 11 |
| Customer groups | `client.customer_groups` | 9 |
| Customer portal settings | `client.customer_portal` | 5 |
| Discount profiles | `client.discount_profiles` | 7 |
| Ecommerce settings | `client.ecommerce_settings` | 5 |
| Email | `client.email` | 1 |
| Inventory locations | `client.inventory_locations` | 11 |
| Order custom fields | `client.order_custom_fields` | 4 |
| Order flags | `client.order_flags` | 7 |
| Orders | `client.orders` | 25 |
| Pages | `client.pages` | 15 |
| Payment gateways | `client.payment_gateways` | 8 |
| Price display settings | `client.price_display_settings` | 5 |
| Product listing settings | `client.product_listing` | 3 |
| Product page settings | `client.product_page` | 5 |
| Products | `client.products` | 10 |
| Search result page settings | `client.search_result_page` | 13 |
| Search settings | `client.search_settings` | 9 |
| SEO configuration | `client.seo_configuration` | 18 |
| Shipping classes | `client.shipping_classes` | 9 |
| Shipping methods | `client.shipping_methods` | 9 |
| Shipping settings | `client.shipping_settings` | 3 |
| Shopping cart settings | `client.shopping_cart` | 5 |
| Site settings | `client.site_settings` | 5 |
| Tax codes | `client.tax_codes` | 7 |
| Tax country taxes | `client.tax_country_taxes` | 5 |
| Tax custom profiles | `client.tax_custom_profiles` | 5 |
| Tax profiles | `client.tax_profiles` | 7 |
| Tax rules | `client.tax_rules` | 7 |
| Tax settings | `client.tax_settings` | 2 |
| Tax zones | `client.tax_zones` | 7 |
| Transactions | `client.transactions` | 6 |
| Trash | `client.trash` | 8 |
| Variations | `client.variations` | 12 |

`client.list_resource_names()` returns every accessor name,
`help(client.admin_customers.get_customers)` prints an endpoint's docstring, and
`dir(client.admin_customers)` lists a resource's functions.

## Documentation

- API reference: <https://newlify.mintlify.app>

## License

MIT. See [LICENSE](LICENSE).
