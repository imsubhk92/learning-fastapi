# 7. FastAPI for AI and data-centric services

## Where the fit comes from

Python services can expose validated inputs and outputs around existing model,
retrieval and data-processing code. Async handlers suit waiting on remote
inference, vector search and databases; CPU/GPU work still needs appropriate
execution capacity. FastAPI does not train models or turn synchronous data
processing into async I/O.
[Concurrency and machine-learning APIs](https://fastapi.tiangolo.com/async/).

Our working service uses typed order records. The same boundary pattern can
serve prediction requests, but no model, provider SDK, vector database or real
AI endpoint is installed in the core app.

| Data/AI workload | Useful FastAPI capability | Architecture question |
| --- | --- | --- |
| Remote LLM or embedding call | Async endpoint, dependency-injected shared client | What deadline, quota and concurrency bound apply? |
| Local model prediction | Pydantic input/output, lifespan resource loading | Where does CPU/GPU execution run and how many copies fit? |
| RAG query | Typed request, retrieval/model orchestration | Are document filters enforcing tenant permissions? |
| Batch ingestion | Validated acceptance endpoint and job status | Which queue makes the work durable? |
| Structured analytics API | Bounded filters, stable response models | How are expensive scans limited and results serialized? |
| Generated text streaming | SSE, JSON Lines or stream responses | What handles cancellation, slow readers and partial failure? |

## A bounded provider boundary

**Design sketch**, not a configured endpoint. This uses an abstract callable so
the pattern does not depend on a particular SDK or billable provider:

```python
import asyncio
from collections.abc import Awaitable, Callable

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class PredictionOutput(BaseModel):
    label: str
    model_version: str


class PredictionService:
    def __init__(self, predict: Callable[[str], Awaitable[PredictionOutput]]):
        self.predict = predict
        self.slots = asyncio.Semaphore(4)

    async def run(self, payload: PredictionInput) -> PredictionOutput:
        # The deadline includes waiting for a slot, not only the provider call.
        async with asyncio.timeout(5):
            async with self.slots:
                return await self.predict(payload.text)
```

Create that service and its reusable client in lifespan, and close the client
at shutdown. Inject the service into a router. Test with a fake async callable
that returns deterministic data or raises a timeout. Map the timeout to a
documented response such as 504, without exposing provider credentials.

The semaphore is per process. Four workers would have four separate limits;
global provider quotas need coordinated admission. A semaphore bounds active
calls, not the number of waiting requests. Admission limits and queue deadlines
are still needed under overload. Provider/client timeouts must also be set.

## Streaming choices

| Transport | Best starting question |
| --- | --- |
| Normal JSON response | Can the client wait for one complete result? |
| SSE over HTTP | Does the browser need one-way incremental events? |
| JSON Lines | Does the client consume a stream of structured records? |
| WebSocket | Does the interaction need bidirectional messages? |

The current FastAPI guide includes built-in SSE via `fastapi.sse` and typed
JSON Lines streaming. Older examples may use additional libraries or manual
`StreamingResponse` formatting. Match the APIs to the installed version before
copying them. Our app demonstrates a small WebSocket snapshot protocol only.
[SSE guide](https://fastapi.tiangolo.com/tutorial/server-sent-events/),
[JSON Lines guide](https://fastapi.tiangolo.com/tutorial/stream-json-lines/).

Streaming reduces time to the first chunk when work can be produced
incrementally; it does not remove total inference cost. Handle disconnects,
bounded buffering, proxy buffering/timeouts and whether an interrupted job
continues. After headers have started, later failures cannot simply change
the HTTP status to 500; define an event-level failure contract.

## Data contracts and model correctness

Validate list sizes, feature dimensions, value ranges, finite numeric values and
schema/model versions. DataFrames, NumPy arrays, timestamps and custom classes
need deliberate conversion to a documented representation. Avoid returning a
huge table merely because serialization is possible.

Pydantic validates a declared shape and its constraints. It does not establish
that a model answer is truthful, that a retrieved citation supports the answer,
or that the user can access the document. Those need evaluation and explicit
access checks. Treat model-generated tool arguments as untrusted input before
any consequential operation.

For RAG, keep ingestion and query lifecycles separate. Persist source metadata
and document ownership; enforce permissions during retrieval, not only after
generation. Measure retrieval relevance and grounded answers independently
from API latency. This is architecture guidance for future work, not evidence
that this learning application performs RAG.

Checkpoint: explain why increasing API workers can exhaust GPU memory, why a
valid `PredictionOutput` might be wrong, and what would make a five-minute
ingestion unsuitable for an in-process background task.
