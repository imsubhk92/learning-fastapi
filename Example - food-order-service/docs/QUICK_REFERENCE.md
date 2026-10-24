# FastAPI quick revision

| Remember | In this application |
| --- | --- |
| FastAPI = API layer | Routes, dependencies, validation integration, OpenAPI |
| Starlette = web/ASGI toolkit | HTTP context, routing, middleware, WebSockets, lifespan |
| Pydantic = data contracts | Input checks, enum values, serialization, JSON Schema |
| Uvicorn = ASGI server | Listens on port 8001 and invokes `main:app` |
| `async def` | Short direct work or cooperative I/O; blocking calls still block |
| Normal `def` route/dependency | FastAPI adapts execution through a thread pool |
| Direct sync helper call | Runs wherever it is called; no automatic offload |
| CPU parallelism | Needs suitable execution resources; async syntax does not supply them |
| WSGI versus ASGI | Sync request/response interface versus async event interface |
| HTTP versus HTTPS | Application protocol versus that protocol protected by TLS |
| WS versus WSS | WebSocket without/with TLS |
| `Annotated` | Type plus validation/documentation metadata |
| `Depends` | Supplies dependencies; not a client request field |
| Lifespan | Startup/shutdown resources once per app worker |
| 201 + Location | Created order and where to read it |
| 204 | No response body |
| 404 | Valid identifier, resource absent |
| 422 | Request fails parsing/validation |
| Strict count | JSON `2` accepted; `"2"`, `true`, 0, 101 rejected |
| Enum validation | Recognized value; not a transition/permission check |
| `extra="forbid"` | Reject unknown input fields |
| `model_validate` / `model_dump` | Validate input / produce Python data |
| `model_copy(update=...)` | Updates are not revalidated automatically |
| `response_model` | Documents and constrains output; not record authorization |
| `/docs`, `/redoc`, `/openapi.json` | Swagger UI, ReDoc, underlying HTTP contract |
| WebSocket protocol | Initial snapshot; text `refresh` or `close` |
| In-memory repository | One worker; resets on reload/restart; unbounded total records |
| BackgroundTasks | Best effort inside the server process; not durable jobs |
| CORS | Browser cross-origin HTTP policy; not authentication |
| AI compatibility | Typed Python service boundaries; no built-in model or factuality guarantee |
| Company evidence | OpenAI samples and Meta research project supported; Swiggy unverified |

```bash
uv sync --extra dev --locked
uv run --locked python -m uvicorn main:app --reload --port 8001
uv run --locked --extra dev pytest
uv run --locked --extra dev ruff check .
uv run --locked --extra dev ruff format --check .
```

All details and primary references are in the [chapter index](README.md).
