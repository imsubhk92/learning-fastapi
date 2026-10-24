"""Metadata and a development-only request inspection example."""

from fastapi import APIRouter, Request

from app.models import Health, RequestInfo, ServiceInfo, Welcome

router = APIRouter(tags=["service"])
debug_router = APIRouter(include_in_schema=False)


@router.get("/", response_model=Welcome, summary="Welcome")
async def read_root() -> Welcome:
    return Welcome(message="Welcome to the Uber Eats API Services learning project")


@router.get("/health", response_model=Health, summary="Process liveness")
async def health() -> Health:
    """Proves this process can answer HTTP; not a dependency readiness check."""
    return Health()


@router.get("/about", response_model=ServiceInfo, summary="Service metadata")
async def read_about(request: Request) -> ServiceInfo:
    return ServiceInfo(
        service=request.app.title,
        version=request.app.version,
        description="A fictional food-order API for learning FastAPI.",
        storage="in-memory; resets on restart; one worker only",
    )


@debug_router.get("/debug/request-info", response_model=RequestInfo)
async def request_info(request: Request) -> RequestInfo:
    """Allowlist headers; never return authorization, cookies, or query values."""
    return RequestInfo(
        method=request.method,
        path=request.url.path,
        headers={
            name: request.headers[name]
            for name in ("accept", "content-type")
            if name in request.headers
        },
        query_keys=list(request.query_params.keys()),
    )
