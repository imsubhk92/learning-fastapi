# Application review and upgrade

Reviewed **25 October 2026**. Scope: the supplied `main.py` and `requirement.txt`,
local refactoring, learning documentation and verification. This directory did
not contain a Git repository or project/ancestor `AGENTS.md` at review time.
The original files are preserved as
[original main.py](review/original-main.py.txt) and
[original dependency snapshot](review/original-requirement.txt).

## Findings and resulting changes

| Priority | Original finding | Result |
| --- | --- | --- |
| High if exposed | Debug endpoint returned all headers and query values, including possible credentials | Off by default; explicit flag; allowlisted headers and query keys only |
| Medium | All seed order IDs were 1 | Unique seed IDs and a monotonic process-local counter |
| Medium | `total_today` was an arbitrary hardcoded numeric literal | Current totals and status counts computed from stored records |
| Medium | `/oders/active` was misspelled and returned `{}` | `/orders/active` returns pending/preparing records with pagination |
| Medium | No body contracts, typed response schemas or meaningful input boundaries | Separate Pydantic models, strict count bounds, trimmed item names, enums, forbidden extra input |
| Medium | No create/read-one/update/delete behavior to practice | CRUD routes with 201/Location, 404 errors and bodyless 204 |
| Medium | Dependency snapshot mixed app dependencies with optional CLI/cloud and unrelated extras | Four direct runtime dependencies in pyproject; separate development extras; resolved uv.lock |
| Learning/maintenance | Routes and behavior were concentrated in one file with limited explanation | Small routers, injected repository, app factory and lifespan with purpose-focused comments |
| Learning/maintenance | No verification suite | Behavior tests for contracts, errors, isolation, dependency overrides, concurrency and sockets |
| Learning/maintenance | No revision path | Basic-to-advanced chapters, official feature map, practical exercises and quick reference |

The original HTTP dependency bundle contained unused packages; required
transitive dependencies are retained by the resolver. The new environment
uses current compatible Starlette with HTTPX2 for its test client, avoiding its
deprecated HTTPX fallback. No global Python packages were removed or modified.

## Contract changes to be aware of

- `/oders/active` is removed; clients should use `/orders/active`.
- Seed IDs are 1, 2, 3 rather than three copies of 1.
- `/orders` retains the `orders` key and adds `total`, `limit`, and `offset`.
- `/orders/status` returns `total`, `active`, and `by_status`; fabricated date,
  city and daily-total information is removed.
- `/about` reports actual app metadata and temporary storage behavior; it no
  longer implies a configured cloud region or team.
- Debug inspection now requires `APP_ENABLE_DEBUG_ROUTE=true` and returns a
  narrower response. It never enables traceback debug mode.
- New inputs reject unknown fields and invalid counts/statuses with 422.
- New WebSocket behavior is an explicitly documented pull protocol.

## Intentionally unfinished production concerns

The app is a local teaching service, not a production order platform. It has
no user identity, permissions, durable storage, payment/order workflow,
cross-process state or event fan-out. Record counts can grow without a total
cap. Models validate shape, while status transitions remain permissive.

The repository is appropriate only for short calls on one event loop; moving
it to threads or adding I/O requires redesign. Request timing measures time to
headers, not total transfer time. TestClient contract checks do not validate
real network behavior or deployment capacity; local server smoke checks are
recorded separately below. No public deployment or paid AI calls are part of
this work.

## Verification record

Validated locally with **Python 3.13.9**, FastAPI 0.162.0, Pydantic 2.14.1,
Starlette 1.10.0, Uvicorn 0.54.0, and the resolved `uv.lock` environment.
Python 3.11+ is the declared requirement; other Python versions were not run.

| Check | Result |
| --- | --- |
| `python -m pytest -W error` | **47 passed**, no warnings |
| Ruff lint and format checks | Passed |
| `uv lock --check --offline` | Passed; project metadata and lock agree |
| Real Uvicorn via `scripts/smoke_check.py` | Passed HTTP CRUD, status totals, 404/422, disabled debug route, OpenAPI/docs HTML and WebSocket handshake/snapshot/refresh/normal close |
| Async demonstration | Ran successfully; cooperative waits overlap, the limit restricts overlap, blocking waits accumulate |
| Local Markdown references | **44** links resolve; fences balanced; **3** Python snippets parse |
| External documentation links | **103/105** returned HTTP 200; ASGI and Flask returned 429 to the automated HEAD check, and were independently readable through source browsing |

The smoke script uses an OS-selected loopback port and terminates its server
in `finally`. No development server was left running. The documentation HTML
checks do not establish that CDN assets render in an offline browser. The tests
are local verification, not deployment, security-audit or load-test evidence.
