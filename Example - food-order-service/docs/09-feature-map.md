# 9. Map of the official FastAPI features

This curated map covers the main families in the
[tutorial](https://fastapi.tiangolo.com/tutorial/) and
[advanced guide](https://fastapi.tiangolo.com/advanced/). It keeps the executable
service small while giving you a revision path across the wider framework.
**Implemented** means code in this repository. **Notes** means explained here.
**Extension** means official reading or a future exercise, not a working feature
in this service. It is not an exhaustive reproduction of upstream documentation.

## Request, response and schema features

| Feature and primary reference | Status and local study point |
| --- | --- |
| [First steps and automatic docs](https://fastapi.tiangolo.com/tutorial/first-steps/) | Implemented: `main.py`; [HTTP notes](02-http-api.md) |
| [Path parameters and enums](https://fastapi.tiangolo.com/tutorial/path-params/) | Implemented: positive order IDs and status enum |
| [Query parameters](https://fastapi.tiangolo.com/tutorial/query-params/) | Implemented: status, limit, offset |
| [String query validation](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/) / [numeric bounds](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/) | Implemented numeric bounds; Extension: search strings/patterns |
| [Query parameter models](https://fastapi.tiangolo.com/tutorial/query-param-models/) | Extension: group larger filter sets into one validated model |
| [Request bodies](https://fastapi.tiangolo.com/tutorial/body/) / [fields](https://fastapi.tiangolo.com/tutorial/body-fields/) | Implemented: `OrderCreate`, count bounds, item trimming |
| [Multiple bodies](https://fastapi.tiangolo.com/tutorial/body-multiple-params/) / [nested models](https://fastapi.tiangolo.com/tutorial/body-nested-models/) | Extension: multi-item order payload |
| [Examples](https://fastapi.tiangolo.com/tutorial/schema-extra-example/) / [extra data types](https://fastapi.tiangolo.com/tutorial/extra-data-types/) | Implemented model example; Extension: UUID, date/time, Decimal, bytes policies |
| [Headers](https://fastapi.tiangolo.com/tutorial/header-params/) / [cookies](https://fastapi.tiangolo.com/tutorial/cookie-params/) | Implemented selected request inspection; Extension: typed parameter declarations and parameter models |
| [Response models](https://fastapi.tiangolo.com/tutorial/response-model/) / [extra models](https://fastapi.tiangolo.com/tutorial/extra-models/) | Implemented separate create, update, output and page contracts |
| [Status codes](https://fastapi.tiangolo.com/tutorial/response-status-code/) / [errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) | Implemented 200, 201, 204, 404, 422 behavior |
| [Operation metadata](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/) / [docs metadata](https://fastapi.tiangolo.com/tutorial/metadata/) | Implemented title, version, tags, summaries, examples, docs URLs |
| [JSON encoder](https://fastapi.tiangolo.com/tutorial/encoder/) / [updates](https://fastapi.tiangolo.com/tutorial/body-updates/) | Implemented model dump and status-only PATCH; Extension: `exclude_unset` for multi-field partial updates |
| [Forms](https://fastapi.tiangolo.com/tutorial/request-forms/) / [form models](https://fastapi.tiangolo.com/tutorial/request-form-models/) | Extension: form parsing, not the JSON contract used here |
| [Uploads](https://fastapi.tiangolo.com/tutorial/request-files/) / [forms with files](https://fastapi.tiangolo.com/tutorial/request-forms-and-files/) | Extension: `UploadFile`, multipart parser, size/type/storage policies |
| [Strict Content-Type checking](https://fastapi.tiangolo.com/advanced/strict-content-type/) | Notes: send the proper content type; core app uses the installed framework default |

Uploads/forms require optional parser dependencies when used. An upload object
does not by itself provide a business file-size limit, malware checking or safe
storage. JSON bodies and multipart bodies use different media types.

## Dependencies, security and application composition

| Feature and primary reference | Status and local study point |
| --- | --- |
| [Dependency injection](https://fastapi.tiangolo.com/tutorial/dependencies/) | Implemented: repository injection shared by HTTP and WebSocket |
| [Classes](https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/) / [sub-dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/) | Extension: reusable filters or a current-user dependency graph |
| [Decorator dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/) / [global dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/) | Extension: enforce a common request prerequisite |
| [Dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/) / [advanced dependencies](https://fastapi.tiangolo.com/advanced/advanced-dependencies/) | Notes: request sessions versus app lifespan; cleanup/streaming lifetime matters |
| [Security](https://fastapi.tiangolo.com/tutorial/security/) / [current user](https://fastapi.tiangolo.com/tutorial/security/get-current-user/) | Notes only: no authentication implemented |
| [OAuth2/JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) / [scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/) / [HTTP Basic](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/) | Extension: verified credentials and authorization, not just header extraction |
| [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/) / [advanced middleware](https://fastapi.tiangolo.com/advanced/middleware/) | Implemented pure ASGI request IDs and timing; [Starlette chapter](05-starlette.md) |
| [CORS](https://fastapi.tiangolo.com/tutorial/cors/) | Notes: exact browser origins; deliberately disabled without a separate frontend |
| [SQL databases](https://fastapi.tiangolo.com/tutorial/sql-databases/) | Extension: replace temporary storage; transactions, migrations, pooling |
| [Multiple files and routers](https://fastapi.tiangolo.com/tutorial/bigger-applications/) | Implemented order, service and WebSocket routers |
| [Settings](https://fastapi.tiangolo.com/advanced/settings/) | Implemented one environment flag using a dataclass; Extension: `pydantic-settings` as configuration grows |
| [Dataclasses](https://fastapi.tiangolo.com/advanced/dataclasses/) / [advanced Python types](https://fastapi.tiangolo.com/advanced/advanced-python-types/) | Implemented settings dataclass, Annotated, enums, union and Literal types |

## Protocols, responses and integration

| Feature and primary reference | Status and local study point |
| --- | --- |
| [Custom responses](https://fastapi.tiangolo.com/advanced/custom-response/) / [return response directly](https://fastapi.tiangolo.com/advanced/response-directly/) | Implemented empty 204; Extension: files, redirects, HTML, streaming |
| [Additional response schemas](https://fastapi.tiangolo.com/advanced/additional-responses/) / [additional status codes](https://fastapi.tiangolo.com/advanced/additional-status-codes/) | Implemented documented 404; Extension: alternate success branches |
| [Response headers](https://fastapi.tiangolo.com/advanced/response-headers/) / [cookies](https://fastapi.tiangolo.com/advanced/response-cookies/) | Implemented Location and request context headers; Extension: cookie policies |
| [WebSockets](https://fastapi.tiangolo.com/advanced/websockets/) | Implemented snapshot/refresh/close protocol, not broadcasts |
| [SSE](https://fastapi.tiangolo.com/tutorial/server-sent-events/) / [JSON Lines](https://fastapi.tiangolo.com/tutorial/stream-json-lines/) / [stream data](https://fastapi.tiangolo.com/advanced/stream-data/) | Notes and Extension: [AI/data chapter](07-ai-data.md) |
| [Background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) | Notes: in-process best effort versus durable jobs |
| [Lifespan](https://fastapi.tiangolo.com/advanced/events/) | Implemented startup/shutdown resource handling |
| [Raw Request](https://fastapi.tiangolo.com/advanced/using-request-directly/) | Implemented metadata and constrained debug inspection |
| [Sub-app mounts](https://fastapi.tiangolo.com/advanced/sub-applications/) / [proxy deployment](https://fastapi.tiangolo.com/advanced/behind-a-proxy/) | Notes and Extension: application boundaries, root path, trusted forwarded headers |
| [Templates](https://fastapi.tiangolo.com/advanced/templates/) / [static files](https://fastapi.tiangolo.com/tutorial/static-files/) | Extension: useful for a web UI, unnecessary for this JSON service |
| [OpenAPI callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/) / [webhooks](https://fastapi.tiangolo.com/advanced/openapi-webhooks/) | Extension: document outbound interactions; actual delivery/retry is separate |
| [SDK generation](https://fastapi.tiangolo.com/advanced/generate-clients/) | Extension: schema-driven clients still require compatibility management |
| [WSGI integration](https://fastapi.tiangolo.com/advanced/wsgi/) / [GraphQL](https://fastapi.tiangolo.com/how-to/graphql/) | Extension: adapters or optional integrations when needed |
| [Extending OpenAPI](https://fastapi.tiangolo.com/how-to/extending-openapi/) / [self-host docs assets](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/) | Extension: contract customization and documentation without CDN access |

## Testing and operations

| Feature and primary reference | Status and local study point |
| --- | --- |
| [Testing](https://fastapi.tiangolo.com/tutorial/testing/) | Implemented behavioral tests with isolated applications |
| [WebSocket tests](https://fastapi.tiangolo.com/advanced/testing-websockets/) / [lifespan tests](https://fastapi.tiangolo.com/advanced/testing-events/) | Implemented protocol cases and cleanup checks |
| [Dependency overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) / [async tests](https://fastapi.tiangolo.com/advanced/async-tests/) | Implemented override and async concurrent request scenarios |
| [HTTPS](https://fastapi.tiangolo.com/deployment/https/) / [deployment concepts](https://fastapi.tiangolo.com/deployment/concepts/) | Notes: [scaling chapter](06-scaling.md); no deployment performed |
| [Workers](https://fastapi.tiangolo.com/deployment/server-workers/) / [containers](https://fastapi.tiangolo.com/deployment/docker/) | Notes: multiple workers are unsuitable for the current in-memory store |
| [Version policy](https://fastapi.tiangolo.com/deployment/versions/) / [release notes](https://fastapi.tiangolo.com/release-notes/) | Use dependency ranges plus the checked lock file; reassess API changes on upgrades |

## How to add a feature without accumulating unnecessary dependencies

Write a concrete use case and expected failure behavior. Check whether the
framework already provides the needed primitive. Add a package only when it
supplies a required capability; keep test tools in development extras. Add a
behavior test and update the API contract and revision notes together. For
example, multi-item orders need nested models, but do not require an AI SDK,
task queue or admin dashboard.
