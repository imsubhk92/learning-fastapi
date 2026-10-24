# Learning FastAPI: food-order service

A small backend for learning FastAPI through working code. This is a fictional
Uber Eats themed example, with no affiliation to Uber. Start with the
[revision guide](docs/README.md) and [review of the original app](docs/REVIEW.md).

## Run locally

Requires Python 3.11+. From this directory, use an isolated environment:

```bash
uv sync --extra dev --locked
uv run --locked python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

Or use Python and pip without uv:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

`python main.py` also starts the development server on port 8001. Stop with
Ctrl+C. Swagger UI: <http://127.0.0.1:8001/docs>, ReDoc:
<http://127.0.0.1:8001/redoc>, schema: <http://127.0.0.1:8001/openapi.json>.
The documentation pages fetch their JavaScript/CSS from CDNs by default; the
schema and API do not require those assets.

## What the service does

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Welcome message |
| GET | `/health` | Process liveness |
| GET | `/about` | Metadata and storage limitations |
| GET | `/orders` | Filter by `status`, paginate with `limit` and `offset` |
| GET | `/orders/status` | Current totals and counts by status |
| GET | `/orders/active` | Pending and preparing orders |
| POST | `/orders` | Create an order; 201 and `Location` header |
| GET | `/orders/{order_id}` | Read an order; 404 when missing |
| PATCH | `/orders/{order_id}` | Update status only |
| DELETE | `/orders/{order_id}` | Delete; 204 with an empty body |
| WebSocket | `/ws/orders/{order_id}` | Snapshot on connect and on `refresh` |

```bash
curl -i http://127.0.0.1:8001/health
curl 'http://127.0.0.1:8001/orders?status=pending&limit=10&offset=0'
curl -i -X POST http://127.0.0.1:8001/orders \
  -H 'Content-Type: application/json' \
  -d '{"item":"Paneer Tikka","count":2}'
curl -i -X PATCH http://127.0.0.1:8001/orders/4 \
  -H 'Content-Type: application/json' -d '{"status":"preparing"}'
curl -i -X DELETE http://127.0.0.1:8001/orders/4
```

On a fresh process the three seed orders have IDs 1, 2, 3; the first POST returns
ID 4. Use the actual returned ID after that. See [HTTP examples](docs/02-http-api.md)
for invalid inputs and [WebSockets](docs/05-starlette.md) for the message protocol.

## Read the code in this order

1. [main.py](main.py): app factory, metadata, lifespan, router registration.
2. [orders.py](app/routers/orders.py): typed routes, status codes, errors.
3. [models.py](app/models.py): Pydantic contracts and validation.
4. [dependencies.py](app/dependencies.py): `Depends` and resource access.
5. [repository.py](app/repository.py): the intentionally small storage layer.
6. [middleware.py](app/middleware.py): ASGI events, request IDs, header timing.
7. [realtime.py](app/routers/realtime.py): WebSocket connection lifecycle.
8. [tests](tests): executable examples of expected and rejected requests.

## Verify changes

```bash
uv run --locked --extra dev pytest
uv run --locked --extra dev ruff check .
uv run --locked --extra dev ruff format --check .
uv run --locked --extra dev python scripts/smoke_check.py
uv run --locked python examples/async_lab.py
```

With an activated pip environment, use `python -m pytest`, `ruff check .`,
`ruff format --check .`, and `python examples/async_lab.py`.

The [smoke script](scripts/smoke_check.py) starts Uvicorn on a temporary loopback
port, checks HTTP and WebSockets over real connections, and stops the process.

The only direct runtime dependencies are FastAPI, Pydantic, Uvicorn, and
`websockets` (the WebSocket protocol implementation for Uvicorn). HTTPX2, pytest,
and Ruff are development extras. Starlette and other required libraries arrive
as transitive dependencies. We avoid the optional `standard`/cloud bundles.
`pyproject.toml` is the source of dependency intent; `uv.lock` pins resolved
versions. The original `requirement.txt` filename still works with pip and now
points to this project; pip installs within the version ranges, not from uv.lock.

## Deliberate limits

This is a local learning service with unauthenticated reads and writes. Data
resets on restart or reload, memory grows with created orders, and each worker
would have a different data set. Run **one worker**. Pagination limits response
size; it does not make the underlying in-memory scan bounded. PATCH validates
the status enum but does not enforce business transitions.

Authentication, durable storage, distributed events, rate limiting, and model
inference are discussed in the guide and exercises. They are not implemented.
See [scaling](docs/06-scaling.md) before changing storage or adding workers.

The debug example is absent by default. Enable it deliberately for local study:

```bash
APP_ENABLE_DEBUG_ROUTE=true uv run --locked python -m uvicorn main:app --port 8001
```

`/debug/request-info` returns method, path, query **keys**, and only `accept` /
`content-type` headers. It does not return credentials or query values and is
excluded from OpenAPI. This flag does not enable FastAPI traceback debugging.

## Revision and practice

The [learning index](docs/README.md) links the basic-to-advanced chapters,
[official feature map](docs/09-feature-map.md),
[company evidence](docs/08-company-evidence.md), and
[practical exercises with answer guidance](docs/10-practice.md).
Material being available is not an assessment of your learning progress.
