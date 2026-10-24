"""Pydantic v2 models define API contracts, not database tables.

Separate input and output models prevent clients from assigning server-owned IDs.
"""

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

ItemName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]
OrderCount = Annotated[int, Field(strict=True, ge=1, le=100)]


class OrderStatus(StrEnum):
    pending = "pending"
    preparing = "preparing"
    delivered = "delivered"
    cancelled = "cancelled"


class OrderCreate(BaseModel):
    """Only customer-editable fields; new orders always start pending."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"examples": [{"item": "Chicken Kadai", "count": 2}]},
    )
    item: ItemName
    count: OrderCount


class OrderStatusUpdate(BaseModel):
    """PATCH changes just status. Transition rules are a later exercise."""

    model_config = ConfigDict(extra="forbid")
    status: OrderStatus


class Order(BaseModel):
    """Immutable snapshots prevent accidental mutation of repository records."""

    model_config = ConfigDict(frozen=True)
    id: int = Field(gt=0)
    item: ItemName
    count: OrderCount
    status: OrderStatus


class OrderPage(BaseModel):
    orders: list[Order]
    total: int = Field(ge=0, description="Matching orders before pagination.")
    limit: int
    offset: int


class OrderSummary(BaseModel):
    total: int
    active: int
    by_status: dict[OrderStatus, int]


class ServiceInfo(BaseModel):
    service: str
    version: str
    description: str
    storage: Literal["in-memory; resets on restart; one worker only"]


class Welcome(BaseModel):
    message: str
    status: Literal["healthy"] = "healthy"


class Health(BaseModel):
    status: Literal["ok"] = "ok"


class ErrorResponse(BaseModel):
    detail: str


class RequestInfo(BaseModel):
    method: str
    path: str
    headers: dict[str, str]
    query_keys: list[str]


class OrderSnapshot(BaseModel):
    """WebSocket message contract; WebSocket routes are outside OpenAPI."""

    event: Literal["order_snapshot"] = "order_snapshot"
    order: Order
