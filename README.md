# FastAPI with Python: Learning and Interview Preparation

A learning workspace combining five fundamentals modules, an example backend,
and interview revision material. Start with the food-order service for tested
application patterns, then use the lessons and questions to explore each topic.

The project now has three parts:

| Location | Contents | How to use it |
| --- | --- | --- |
| [Fundamentals](Fundamentals/) | Five modules, each with a topic outline and three Python scripts | Work through the concepts in order; check the lesson review notes below |
| [Example - food-order-service](Example%20-%20food-order-service/README.md) | Typed API, tests, examples, and a basic-to-advanced revision guide | Run the application and inspect its implementation |
| [Interview Questions](Interview%20Questions/README.md) | 170 question headings across ten topic sections | Rehearse answers and verify snippets against the working example and official docs |

```text
learning-fastapi/
├── README.md
├── Fundamentals/
│   ├── 01 FastAPI Basics/
│   ├── 02 API Development/
│   ├── 03 Advanced FastAPI Features/
│   ├── 04 Testing and Documentation/
│   └── 05 Deployment and Scaling/
├── Example - food-order-service/
│   ├── main.py
│   ├── app/
│   ├── tests/
│   ├── examples/
│   ├── scripts/
│   ├── docs/
│   ├── pyproject.toml
│   └── uv.lock
└── Interview Questions/
    └── README.md
```

## Run the example application

The example declares **Python 3.11+**. Its dependency configuration and entry
point live inside `Example - food-order-service/`; run the following from the
repository root:

```bash
cd "Example - food-order-service"
uv sync --locked --extra dev
uv run --locked python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

Alternatively, with Python and pip, starting from the repository root:

```bash
cd "Example - food-order-service"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

Stop the server with Ctrl+C. If you copied or moved a virtual environment with
the project, recreate it if its commands still reference the old location.

| URL | Purpose |
| --- | --- |
| <http://127.0.0.1:8001/health> | Process liveness |
| <http://127.0.0.1:8001/orders> | List orders |
| <http://127.0.0.1:8001/docs> | Swagger UI |
| <http://127.0.0.1:8001/redoc> | ReDoc |
| <http://127.0.0.1:8001/openapi.json> | Generated HTTP API schema |

See the [service README](Example%20-%20food-order-service/README.md) for curl
examples, all endpoints, configuration, and code-reading order.

### What is implemented

- Typed order creation, reads, status updates, and deletion.
- Pydantic input validation, response models, filtering, and pagination.
- Dependency injection, an app factory, and lifespan resource handling.
- Request IDs, response-header timing, and opt-in restricted debug inspection.
- A WebSocket snapshot protocol with `refresh` and `close` commands.
- Behavioral tests and a temporary real-server smoke-check script.

The service uses in-memory storage that resets on restart/reload. Run **one
worker**: multiple workers would have independent records and ID counters.
Authentication, durable storage, business transition rules, and real AI
inference are future extensions. The example is a local learning service.

### Verify the example

From `Example - food-order-service/`:

```bash
uv run --locked --extra dev python -m pytest -W error
uv run --locked --extra dev python -m ruff check .
uv run --locked --extra dev python -m ruff format --check .
uv run --locked --extra dev python scripts/smoke_check.py
uv run --locked python examples/async_lab.py
```

The smoke script starts a temporary Uvicorn server on a loopback port and stops
it when checks finish. The async lab demonstrates cooperative versus blocking
waits; its timings are not a framework benchmark.

`pyproject.toml` declares the example's dependencies, and `uv.lock` records the
resolved versions. The four direct runtime dependencies are FastAPI, Pydantic,
Uvicorn, and `websockets`; development extras add HTTPX2, pytest, and Ruff.
There is no shared dependency manifest for all the fundamentals scripts.

## Fundamentals roadmap

Each module contains a short README outline and three standalone `.py` lessons.
The scripts already exist; you do not need to copy code from hypothetical
`fastapi_basics.md` or other files named in the previous root README.

| Order | Module | Topics |
| --- | --- | --- |
| 1 | [FastAPI Basics](Fundamentals/01%20FastAPI%20Basics/README.md) | Setup, first API, endpoints, responses, request visualization |
| 2 | [API Development](Fundamentals/02%20API%20Development/README.md) | Path/query parameters, Pydantic validation, response metrics |
| 3 | [Advanced FastAPI Features](Fundamentals/03%20Advanced%20FastAPI%20Features/README.md) | Authentication, authorization, middleware, async programming, performance metrics |
| 4 | [Testing and Documentation](Fundamentals/04%20Testing%20and%20Documentation/README.md) | Endpoint tests, generated documentation, coverage visualization |
| 5 | [Deployment and Scaling](Fundamentals/05%20Deployment%20and%20Scaling/README.md) | Docker/cloud simulations and a small concurrent-request demonstration |

### Working with the lesson scripts

Review each script before running it. Most start a short-lived local server on
port **8000**, issue HTTP requests, and save a Matplotlib PNG to the current
working directory. Their launch code binds to `0.0.0.0`; run one at a time in
an appropriate local environment and avoid port conflicts. The food-order
example uses port **8001**.

The lesson imports require additional packages outside the example's dependency
set, such as `requests` and `matplotlib`. The authentication lesson also imports
`jose` and `passlib`; `EmailStr` needs email validation support, and the coverage
lesson invokes `pytest-cov`. Their setup comments are not a tested lock file.
Use a separate lesson environment and resolve the issues below before treating
the scripts as reference implementations. No external dataset is required by
the current scripts; they use small synthetic records.

## Revision and interview practice

The example's guide covers the requested basic-to-advanced topics:

| Revision topic | Reading |
| --- | --- |
| FastAPI versus Flask/Django and framework responsibilities | [Foundations](Example%20-%20food-order-service/docs/01-foundations.md) |
| HTTP contracts, OpenAPI, Swagger UI, and ReDoc | [HTTP and API documentation](Example%20-%20food-order-service/docs/02-http-api.md) |
| Pydantic validation and serialization | [Pydantic](Example%20-%20food-order-service/docs/03-pydantic.md) |
| Async/await, blocking I/O, concurrency, WSGI versus ASGI | [Async and ASGI](Example%20-%20food-order-service/docs/04-async-asgi.md) |
| Starlette routing, middleware, lifespan, HTTP/HTTPS, WebSockets | [Starlette and protocols](Example%20-%20food-order-service/docs/05-starlette.md) |
| Workers, shared state, deployment, and scaling | [Scaling](Example%20-%20food-order-service/docs/06-scaling.md) |
| AI and data-centric API design | [AI and data services](Example%20-%20food-order-service/docs/07-ai-data.md) |
| Evidence and limits for OpenAI, Meta, and Swiggy examples | [Company evidence](Example%20-%20food-order-service/docs/08-company-evidence.md) |
| Wider framework capabilities and official references | [Feature map](Example%20-%20food-order-service/docs/09-feature-map.md) |

For quick revision, use the [cheat sheet](Example%20-%20food-order-service/docs/QUICK_REFERENCE.md).
For implementation and architecture exercises, use
[practical tasks with answer guidance](Example%20-%20food-order-service/docs/10-practice.md).
The [full guide index](Example%20-%20food-order-service/docs/README.md) provides
the recommended reading order.

The [interview bank](Interview%20Questions/README.md) covers basics, routing,
databases, model serving, testing, deployment, security, integrations,
performance, and monitoring. Treat its snippets as discussion material to
review and adapt; they have not all been executed or checked for compatibility
in this review. Reading material and passing app tests do not establish personal
interview readiness. Track your exercises as attempted, assessed, or deferred.

## Review status and next improvements

Reviewed **25 October 2026** after the folder reorganization:

| Area | Current evidence |
| --- | --- |
| Food-order application | **47 tests passed** with warnings treated as errors; Ruff lint and formatting passed from its new directory |
| Environment setup | Locked dependency sync succeeded from the example's new directory |
| Fundamentals | All **15 scripts** parse; code reviewed for the issues below, without running their server/plot workflows |
| Interview bank | **170 numbered question headings** across **10 sections** counted; answers/snippets are not fully validated |
| Deployment | Lesson scripts simulate Docker/cloud configuration; no actual container build or cloud deployment was validated |

The added fundamentals lessons need these corrections before they can share
the example application's verification status:

| Finding | Why it matters / next correction |
| --- | --- |
| Several handlers return `(payload, 201)` or `(payload, 404)` | An isolated check of the [basic endpoints lesson](Fundamentals/01%20FastAPI%20Basics/02%20Basic%20Endpoints%20and%20Responses/basic_endpoints.py) returned HTTP 200 with a JSON array. Declare the status code or raise an HTTP exception, then correct the lesson assertions. |
| The [authentication lesson](Fundamentals/03%20Advanced%20FastAPI%20Features/01%20Authentication%20and%20Authorization/authentication_authorization.py) declares query credentials while its client posts JSON | Align the login request contract and tests; replace the placeholder signing secret and define token expiry before using it beyond a local exercise. |
| The [Pydantic lesson](Fundamentals/02%20API%20Development/02%20Data%20Validation%20with%20Pydantic/data_validation_pydantic.py) uses `.dict()` and optional email validation | Align the examples with the service's Pydantic v2 style (`model_dump`) and explicitly declare lesson dependencies. |
| Deployment lessons print configuration and test localhost | Their Python 3.8 / older package examples do not match the service's Python 3.11+ configuration. Build and test actual deployment artifacts separately before claiming deployment readiness. |

The request/latency plots and 15-request scaling demonstration illustrate
measurement mechanics. They do not establish capacity, throughput, or a
production performance baseline. For the earlier application findings and
preserved source snapshots, see the
[application review](Example%20-%20food-order-service/docs/REVIEW.md).

## Official references

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Starlette documentation](https://starlette.dev/)
- [Pydantic documentation](https://docs.pydantic.dev/latest/)
- [Uvicorn documentation](https://uvicorn.dev/)
- [pytest documentation](https://docs.pytest.org/)
- [Docker documentation](https://docs.docker.com/)
