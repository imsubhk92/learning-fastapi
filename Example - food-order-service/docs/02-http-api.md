# 2. HTTP, contracts, errors and generated documentation

## Trace one request

For `POST /orders`, Uvicorn receives HTTP and invokes the ASGI app. Middleware
creates a request ID. FastAPI finds the route, resolves `Repository` through
`Depends`, and validates the JSON against `OrderCreate`. The handler creates an
order, sets `Location`, and returns it. The response contract describes the
returned JSON. Invalid input produces a 422 before the handler runs.
[Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/),
[response models](https://fastapi.tiangolo.com/tutorial/response-model/).

| Input location | Example in this app | Meaning |
| --- | --- | --- |
| Path | `/orders/3` | Identifies a particular order; positive integer |
| Query | `/orders?status=pending&limit=10` | Filtering and pagination |
| JSON body | `{"item":"Dal","count":2}` | Structured creation payload |
| Header | `Content-Type: application/json` | Describes body representation |
| Framework object | `Request`, `Response` | Access HTTP context or set response headers |
| Dependency | `repository: Repository` | Inject an application resource; not client input |

`Annotated[int, Query(ge=1, le=100)]` combines a Python type with validation and
documentation metadata. Query strings arrive as text, so `limit=2` parses to
an integer. The JSON `count` field intentionally uses strict validation:
`"count":"2"` is rejected. These are two different input policies.

## Methods and status codes

| Operation | Behavior here | Useful distinction |
| --- | --- | --- |
| GET | Read only; 200 | Reads should not perform business mutations |
| POST | Create; 201 and `Location` | Retrying may create another order |
| PATCH | Set status; 200 | Partial update; this endpoint only accepts status |
| DELETE | Delete; 204 empty body | First delete succeeds; another returns 404 |
| PUT | Not implemented; 405 | Commonly used for replacement rather than this partial update |

HTTP idempotence concerns the intended effect, not identical response codes.
Deleting an already deleted resource does not recreate it. POST retries need a
separate idempotency design if duplicate orders are unacceptable.

### Try rejected requests

With the server running, these examples should return 422:

```bash
curl -i -X POST http://127.0.0.1:8001/orders \
  -H 'Content-Type: application/json' -d '{"item":"  ","count":0}'
curl -i -X POST http://127.0.0.1:8001/orders \
  -H 'Content-Type: application/json' -d '{"item":"Dal","count":"2"}'
curl -i 'http://127.0.0.1:8001/orders?limit=101'
curl -i http://127.0.0.1:8001/orders/abc
```

`GET /orders/999` returns 404 with `{"detail":"Order not found"}`. A 422
response instead contains a list of validation errors with locations such as
`["body","count"]` or `["query","limit"]`. Those client errors are different
from an unexpected application exception, which should become a 500. Do not
catch every exception and return 200 with an error message.

Static `/orders/status` and `/orders/active` routes are declared before
`/orders/{order_id}`. Route order matters: otherwise a static word can be
matched as an ID. See [path matching](https://fastapi.tiangolo.com/tutorial/path-params/).

## OpenAPI, Swagger UI and ReDoc

These are related but distinct:

| URL | What it provides | How to use it |
| --- | --- | --- |
| `/openapi.json` | Machine-readable API contract | Inspect paths, schemas, required fields, responses and operation IDs |
| `/docs` | Swagger UI rendered from that contract | Expand POST, try the example, inspect the result |
| `/redoc` | ReDoc rendered from that contract | Read the API and schema as reference documentation |

FastAPI generates the contract from routes and models. Summaries, descriptions,
tags, examples and response declarations improve that contract. Our tests
check the schemas and successful/404/422 responses; they do not merely check
that the HTML endpoint returns 200.
[Metadata and documentation URLs](https://fastapi.tiangolo.com/tutorial/metadata/).

OpenAPI documents the HTTP endpoints; our WebSocket protocol is documented
separately. Custom responses or exception handlers must still agree with the
documented response shape. Generated docs do not enforce authentication or
business authorization.

## Pagination and compatibility

`total` means matching records **before** pagination. For the three seed orders,
`?limit=1&offset=1` returns ID 2 with `total=3`. Filtering occurs before slicing.
Offset pagination is easy to learn; changing data can shift later pages. Large,
frequently changing collections often need an indexed cursor design.

The old GET `/orders` response still contains `orders`, now with pagination
metadata. `/orders/status` replaces a fabricated `total_today` with current
record counts. The typo `/oders/active` is removed; use `/orders/active`.
These are intentional learning-project contract changes, recorded in the
[review](REVIEW.md). There is no claim of compatibility for unknown clients.
