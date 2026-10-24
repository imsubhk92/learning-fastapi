"""Pure ASGI middleware observes HTTP without buffering response bodies."""

from time import perf_counter
from uuid import uuid4

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class RequestContextMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # These variables belong to THIS request. Instance state would be shared
        # by concurrent requests. Generate IDs rather than reflecting user input.
        request_id = uuid4().hex
        started = perf_counter()
        scope.setdefault("state", {})["request_id"] = request_id

        async def send_with_context(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers["X-Request-ID"] = request_id
                # Time to response headers, not total time to stream a body.
                headers["X-Response-Time-Ms"] = f"{(perf_counter() - started) * 1000:.3f}"
            await send(message)

        await self.app(scope, receive, send_with_context)
