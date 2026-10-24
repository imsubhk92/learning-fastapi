# 8. Company examples: evidence and limits

Checked **25 October 2026**. Public examples show specific usage; they do not
automatically establish a company's internal production architecture, scale,
or reason for selecting a framework.

| Company | Primary evidence located | What we can say | What we cannot establish |
| --- | --- | --- | --- |
| OpenAI | Official ChatKit customer-support sample constructs a FastAPI app and uses dependencies and streaming responses | FastAPI is used in that public OpenAI example | That all of OpenAI or ChatGPT's production backend uses FastAPI |
| Meta / FAIR | Chameleon's model-viewer backend constructs a FastAPI app and exposes HTTP and WebSocket routes | A Meta research project uses FastAPI for its model-viewing service | Company-wide adoption, current production use, or throughput |
| Swiggy | No directly supporting first-party FastAPI source located in this review | The requested adoption claim remains unverified | That Swiggy does or does not use FastAPI internally, or why |

OpenAI's [ChatKit customer-support source](https://github.com/openai/openai-chatkit-advanced-samples/blob/main/examples/customer-support/backend/app/main.py)
contains a FastAPI application, a dependency-injected server, and an HTTP
streaming response. Its older
[retrieval-plugin local server](https://github.com/openai/chatgpt-retrieval-plugin/blob/main/local_server/main.py)
is another bounded example. Sample code is evidence of that project, not a
statement about private infrastructure.

Meta's [Chameleon model service](https://github.com/facebookresearch/chameleon/blob/main/chameleon/viewer/backend/models/service.py)
uses FastAPI and WebSockets for model output. The
[repository README](https://github.com/facebookresearch/chameleon/blob/main/README.md)
identifies it as a Meta/FAIR project; the repository is archived. A maintainer
[explained the WebSocket choice](https://github.com/facebookresearch/chameleon/issues/25)
as allowing incremental output rather than waiting for the entire result.
That explanation is specific to transport behavior, not a complete account of
the framework selection decision.

For Swiggy, searches of its engineering publication and company/developer
material did not establish the requested claim. Lack of a located source is
not evidence of non-use. A claim from a tutorial, technology logo list or an
OpenAI-compatible API would not by itself prove internal FastAPI adoption.

## Why a team might choose FastAPI

The following is **our technical inference**, not a quote from these companies:
typed boundaries can reduce API contract work, generated docs help consumers,
async I/O suits remote model/data calls, and Starlette's streaming/WebSocket
support suits incremental interactions. Python also makes existing data/model
code easy to place behind an API. These benefits match the patterns visible in
the examples, but do not establish the teams' original motivations.

A useful interview answer is: “FastAPI suits a typed Python API with concurrent
I/O. OpenAI publishes FastAPI-based examples, and Meta's Chameleon used it in a
research viewer. I would verify a specific company's adoption and workload
before making broader claims.”

Avoid using company names as a substitute for reasoning about requirements,
failure modes, cost, data ownership and the team's existing systems.
