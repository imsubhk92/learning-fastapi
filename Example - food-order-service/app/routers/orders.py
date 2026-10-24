"""Translate validated HTTP requests into repository calls and status codes."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, Response, status

from app.dependencies import Repository
from app.models import (
    ErrorResponse,
    Order,
    OrderCreate,
    OrderPage,
    OrderStatus,
    OrderStatusUpdate,
    OrderSummary,
)

router = APIRouter(prefix="/orders", tags=["orders"])
OrderId = Annotated[int, Path(gt=0, description="Positive order identifier.")]
PageLimit = Annotated[int, Query(ge=1, le=100, description="Maximum records returned.")]
PageOffset = Annotated[int, Query(ge=0, description="Matching records to skip.")]
NOT_FOUND = {404: {"model": ErrorResponse, "description": "The order does not exist."}}


@router.get("", response_model=OrderPage, summary="List orders with filtering and pagination")
async def list_orders(
    repository: Repository,
    status: Annotated[OrderStatus | None, Query(description="Exact order status.")] = None,
    limit: PageLimit = 20,
    offset: PageOffset = 0,
) -> OrderPage:
    # A blocking SQL/HTTP call here would block the event loop. Read
    # docs/04-async-asgi.md before replacing this tiny in-memory operation.
    return repository.list_orders(status=status, limit=limit, offset=offset)


# Static paths must precede /{order_id} so 'status' is not interpreted as an ID.
@router.get("/status", response_model=OrderSummary, summary="Count current orders by status")
async def order_status(repository: Repository) -> OrderSummary:
    """Counts current records, not today's sales or a production business metric."""
    return repository.summary()


@router.get("/active", response_model=OrderPage, summary="List pending and preparing orders")
async def active_orders(
    repository: Repository,
    limit: PageLimit = 20,
    offset: PageOffset = 0,
) -> OrderPage:
    return repository.list_orders(active_only=True, limit=limit, offset=offset)


@router.post(
    "", response_model=Order, status_code=status.HTTP_201_CREATED, summary="Create an order"
)
async def create_order(payload: OrderCreate, repository: Repository, response: Response) -> Order:
    order = repository.create(payload)
    response.headers["Location"] = f"/orders/{order.id}"
    return order


@router.get("/{order_id}", response_model=Order, responses=NOT_FOUND, summary="Read one order")
async def get_order(order_id: OrderId, repository: Repository) -> Order:
    order = repository.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch(
    "/{order_id}",
    response_model=Order,
    responses=NOT_FOUND,
    summary="Change an order's status",
)
async def update_order(
    order_id: OrderId,
    payload: OrderStatusUpdate,
    repository: Repository,
) -> Order:
    """This teaching API permits any enum status; it has no workflow engine."""
    order = repository.update_status(order_id, payload.status)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=NOT_FOUND,
    summary="Delete an order",
)
async def delete_order(order_id: OrderId, repository: Repository) -> Response:
    if not repository.delete(order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    # 204 has no response body: neither {} nor the JSON value null.
    return Response(status_code=status.HTTP_204_NO_CONTENT)
