"""Connect routes to resources using FastAPI dependency injection.

HTTPConnection is Starlette's shared base for Request and WebSocket, so this
dependency works with both protocols. FastAPI resolves it via Depends().
"""

from typing import Annotated

from fastapi import Depends
from starlette.requests import HTTPConnection

from app.repository import OrderRepository


async def get_repository(connection: HTTPConnection) -> OrderRepository:
    return connection.app.state.orders


Repository = Annotated[OrderRepository, Depends(get_repository)]
