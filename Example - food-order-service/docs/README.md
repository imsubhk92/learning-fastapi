# FastAPI revision guide

Prepared on **25 October 2026**, using the official sources linked in each chapter.
The runnable app targets FastAPI 0.162 and Pydantic v2; use `uv.lock` for the
tested dependency set. Upstream documentation changes, so check your installed
version before copying examples from another tutorial.

## Learning route

| Order | Chapter | You should be able to explain |
| --- | --- | --- |
| 1 | [Foundations and framework choice](01-foundations.md) | FastAPI, Starlette, Pydantic, Uvicorn; choosing Flask or Django instead |
| 2 | [HTTP, contracts and API docs](02-http-api.md) | Path/query/body/header, CRUD, 404/422, Swagger UI, ReDoc, OpenAPI |
| 3 | [Pydantic in depth](03-pydantic.md) | Constraints, coercion, strict types, nested models, serialization, validators |
| 4 | [Async, WSGI and ASGI](04-async-asgi.md) | Event loop, blocking I/O, thread pools, concurrency versus parallelism |
| 5 | [Starlette and protocols](05-starlette.md) | Routing, middleware, lifespan, HTTP/HTTPS, WebSockets, CORS |
| 6 | [Scaling and operations](06-scaling.md) | Workers, state, pools, deployment, reliability, measuring limits |
| 7 | [AI and data services](07-ai-data.md) | Model serving, RAG, streaming, data contracts, resource limits |
| 8 | [Company evidence](08-company-evidence.md) | What public OpenAI/Meta code proves; what remains unverified for Swiggy |
| 9 | [Official feature map](09-feature-map.md) | Where to find the wider basic and advanced documentation |
| 10 | [Practical exercises](10-practice.md) | Implement, test, diagnose and defend architecture choices |

For a quick revision, use the [cheat sheet](QUICK_REFERENCE.md). For the exact
changes to the original application, see the [review](REVIEW.md).

## How to study with the app

1. Run the commands in the [project README](../README.md), then open `/docs`.
2. Send one valid POST and one invalid POST. Predict each status code first.
3. Follow the request from a router through `Depends` to the repository.
4. Read the corresponding test, then change one rule and update the behavior.
5. Explain the tradeoff out loud before checking the exercise answer guidance.

Code labeled **standalone** can be run separately. Code labeled **design sketch**
needs integration and is not an existing endpoint. The feature map distinguishes
implemented examples from topics documented for later work. It is a curated map
of the official tutorial and advanced guide, not a claim that this small service
implements every FastAPI capability.

## Your learning record

This review validates the application; it does not assess your personal mastery.
All exercises begin **unassessed**. Record `covered`, `attempted`, `assessed`, or
`deferred` with evidence rather than treating a read chapter as a passed exercise.

| Topic | Initial learner status | Evidence to collect |
| --- | --- | --- |
| HTTP and validation | Unassessed | Predict responses; write a failing test and fix it |
| Dependencies and lifespan | Unassessed | Replace storage in a test; explain resource cleanup |
| Async and blocking | Unassessed | Run the lab; diagnose a blocking endpoint |
| WebSockets and streaming | Unassessed | Observe a refresh after an HTTP mutation |
| Scaling and AI architecture | Unassessed | Explain worker memory, timeouts, and queue decisions |

Primary starting points: [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/),
[advanced guide](https://fastapi.tiangolo.com/advanced/),
[Starlette](https://starlette.dev/), and
[Pydantic](https://docs.pydantic.dev/latest/).
