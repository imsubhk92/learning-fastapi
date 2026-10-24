"""Entry point: python -m uvicorn main:app --reload --port 8001.

Read this file, then app/routers/orders.py, app/models.py, app/repository.py.
The factory gives each test its own application and storage.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import Settings
from app.middleware import RequestContextMiddleware
from app.repository import OrderRepository
from app.routers import orders, realtime, system

VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Create resources at startup and release them at shutdown, once per worker."""
    app.state.orders = OrderRepository()
    try:
        yield  # Uvicorn serves requests while execution is paused here.
    finally:
        # A database pool or HTTP client would be closed here in a later lesson.
        del app.state.orders


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build an isolated ASGI app without opening connections at import time."""
    settings = settings if settings is not None else Settings.from_env()
    application = FastAPI(
        title="Uber Eats API Services",
        description=(
            "A fictional food-order learning service, unaffiliated with Uber. "
            "Demonstrates validation, dependencies, CRUD, and WebSockets. "
            "Storage is temporary and local to one worker; there is no authentication."
        ),
        version=VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        openapi_tags=[
            {"name": "service", "description": "Service metadata and liveness."},
            {"name": "orders", "description": "Validated in-memory order operations."},
        ],
    )
    application.add_middleware(RequestContextMiddleware)
    application.include_router(system.router)
    application.include_router(orders.router)
    application.include_router(realtime.router)
    if settings.enable_debug_route:
        application.include_router(system.debug_router)
    return application


app = create_app()


if __name__ == "__main__":
    import uvicorn

    # Loopback binding and reload are for local development only.
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
