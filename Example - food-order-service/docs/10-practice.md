# 10. Practical exercises and answer guidance

All exercises start **unassessed**. Try the task before opening the answer.
Passing the repository's existing tests validates existing behavior; a new
feature needs checks that demonstrate its own expected behavior and failures.

## 1. Predict the contract — beginner

Predict the status and important body fields for each request, then verify with
`/docs`, curl, or a TestClient. Explain the difference, not only the status code.

| Request | Your prediction |
| --- | --- |
| POST `/orders`, `{"item":" Dal ","count":2}` | |
| POST `/orders`, `{"item":"Dal","count":"2"}` | |
| POST `/orders`, `{"item":"Dal","count":true}` | |
| GET `/orders/0` | |
| GET `/orders/999` | |
| GET `/orders?status=preparing&limit=1` | |
| DELETE `/orders/1` twice | |

<details>
<summary>Answer guidance</summary>

The valid POST returns 201, trimmed `item`, pending status and a server ID.
The strict-count POSTs return 422. ID zero violates the path constraint (422),
while an absent positive ID is a lookup failure (404). Filtering happens before
pagination; `total` counts matching records. The deletes return 204 with an empty
body, then 404; their final effect is still deletion.

</details>

## 2. Add a text filter — beginner to intermediate

Add optional `item_contains` to GET `/orders`. Define case handling, trimming,
minimum/maximum length and empty-match behavior. Filter before pagination.
Write checks for a match, no match, a boundary input, and `total` after filtering.
Verify that `/openapi.json` documents the parameter.

<details>
<summary>Review criteria</summary>

Keep HTTP validation in the router/model boundary and matching in the
repository. Do not create a global mutable filtered list. Preserve existing
status filtering and page metadata. Decide whether an empty search is invalid
or equivalent to no filter, and make the decision visible in docs and tests.

</details>

## 3. Enforce order transitions — intermediate

Define allowed transitions: pending → preparing/cancelled, preparing →
delivered/cancelled, and no change out of terminal states. Decide whether
setting the current status again succeeds. Return a documented 409 for a
conflict while keeping unknown enum values as 422. Implement this policy and
test valid transitions, invalid transitions, repeated requests and missing IDs.

<details>
<summary>Answer guidance</summary>

The enum answers “is this a recognized state?” A domain transition rule answers
“can this order move to that state now?” Preserve the distinction between 404,
409 and 422. When adding shared storage, the read/check/write must be protected
by an appropriate transaction or optimistic concurrency mechanism; a stale
read is not sufficient.

</details>

## 4. Diagnose a slow service — intermediate

A handler contains `async def` and then calls a blocking SDK that takes two
seconds. Unrelated health requests stall. Explain why and compare an async SDK,
a sync endpoint, and explicit thread offloading. Run
`python examples/async_lab.py` to connect the diagnosis to observable behavior.

<details>
<summary>Answer guidance</summary>

Async syntax does not adapt the SDK call. A cooperative client is a natural
fit; a sync endpoint is adapted by FastAPI, while an explicit thread call can
adapt just the blocking section. Each option still needs client deadlines,
capacity limits and thread-safety checks. A CPU-bound workload needs a separate
analysis; more await expressions do not remove computation.

</details>

## 5. Test resource ownership — intermediate

Use a repository dependency override to return a deterministic data set. Show
that another app instance is unaffected, that the override is cleaned up, and
that lifespan resources disappear after shutdown. Start with
`tests/test_service.py`, then explain what would change for an async database
session and a shared connection pool.

<details>
<summary>Review criteria</summary>

The pool lives for the app/worker; a request session is scoped to the request.
Tests must run lifespan when using lifespan-owned resources. Do not leak a
dependency override into later tests. In a background job, create resources
with a suitable job lifetime rather than using an already closed request session.

</details>

## 6. Observe the WebSocket contract — intermediate

Connect to order 3, read the snapshot, PATCH the order from a separate HTTP
request, and send `refresh`. Predict the outcome of binary data, an unknown
command, deleting the order, and disconnecting. Explain what a multi-worker
broadcast design would need beyond this socket endpoint.

<details>
<summary>Answer guidance</summary>

Refresh reads the new state. Binary input closes with 1003; unknown commands
and refresh after deletion close with 1008. This is a pull-based lesson, so a
PATCH alone sends no event. Multiple workers need shared state plus an event
transport, and clients need authorization, reconnection and delivery semantics.

</details>

## 7. Design a reliable AI endpoint — advanced

Design a prediction API with a fake provider first. Requirements: input bounds,
explicit output contract, five-second overall deadline, bounded concurrency,
overload behavior and deterministic timeout tests. Explain where the client is
created/closed and what happens if the caller disconnects. Separate provider
errors from schema validation errors and avoid logging prompts by default.

<details>
<summary>Answer guidance</summary>

Use lifespan for a shared async client/service, dependency injection for access,
an outer deadline including slot acquisition, and a per-process semaphore plus
an explicit admission policy. Test timeout, rejected input, provider failure
and successful output without paid calls. Coordinate limits if a provider quota
is global. A valid output schema is not a model-quality assessment.

</details>

## 8. Explain the scale incident — architect level

After moving from one to four workers, users see duplicate IDs and missing
orders, database connection errors increase, and loading a model crashes the
host. Explain each failure and propose an incremental migration. Define what
you would measure to decide whether to add more capacity.

<details>
<summary>Answer guidance</summary>

Each worker owns an independent store, ID counter, pool and model lifecycle.
Use shared durable storage with generated IDs and transactional rules; budget
total connections across replicas; measure model RAM/GPU memory before choosing
process counts. Consider dedicated inference workers when that resource needs
different scaling. Measure realistic p95/p99 latency, errors, memory, loop lag,
queue wait and dependencies before claiming improvement.

</details>

## Five-minute oral revision

1. What does FastAPI add above Starlette and Pydantic?
2. What actually yields when you write `await`?
3. Why is ASGI not the same as HTTPS?
4. What do OpenAPI, Swagger UI and ReDoc each do?
5. Why do we use separate create/update/output models?
6. What does `Depends` supply, and when is it resolved?
7. Why is `BackgroundTasks` not a durable job queue?
8. What makes this application unsafe to scale to multiple workers?
9. When would Django or Flask be the better fit?
10. Which company adoption claims are directly supported by the linked sources?

Record assessment evidence separately: your code/test output, the reasoning you
could explain unaided, and what remains deferred. No study time or readiness is
inferred from these notes being present.
