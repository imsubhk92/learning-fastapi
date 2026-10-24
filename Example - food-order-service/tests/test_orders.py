"""Behavior checks: clients, not implementation details, define the contract."""

import asyncio

import httpx2 as httpx
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from main import create_app


def test_create_read_update_delete(client: TestClient) -> None:
    created = client.post("/orders", json={"item": "  Paneer Tikka  ", "count": 2})
    assert created.status_code == 201
    order = created.json()
    assert order == {"id": 4, "item": "Paneer Tikka", "count": 2, "status": "pending"}
    assert created.headers["location"] == "/orders/4"
    assert client.get(created.headers["location"]).json() == order

    updated = client.patch("/orders/4", json={"status": "preparing"})
    assert updated.status_code == 200
    assert updated.json() == {**order, "status": "preparing"}
    assert client.get("/orders/4").json() == updated.json()

    deleted = client.delete("/orders/4")
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get("/orders/4").status_code == 404
    # IDs are not reused when an order is deleted.
    assert client.post("/orders", json={"item": "Dal", "count": 1}).json()["id"] == 5


def test_filter_pagination_and_static_routes(client: TestClient) -> None:
    page = client.get("/orders?limit=1&offset=1").json()
    assert [order["id"] for order in page["orders"]] == [2]
    assert (page["total"], page["limit"], page["offset"]) == (3, 1, 1)
    pending = client.get("/orders?status=pending").json()
    assert [order["id"] for order in pending["orders"]] == [3]
    assert pending["total"] == 1
    assert client.get("/orders?offset=100").json()["orders"] == []
    active = client.get("/orders/active").json()
    assert [order["id"] for order in active["orders"]] == [2, 3]
    assert client.get("/oders/active").status_code == 404
    assert client.get("/orders/status").json() == {
        "total": 3,
        "active": 2,
        "by_status": {"pending": 1, "preparing": 1, "delivered": 1, "cancelled": 0},
    }


def test_summary_changes_with_mutations(client: TestClient) -> None:
    client.post("/orders", json={"item": "Dal", "count": 1})
    assert client.get("/orders/status").json()["active"] == 3
    client.patch("/orders/4", json={"status": "cancelled"})
    assert client.get("/orders/status").json()["by_status"]["cancelled"] == 1
    assert client.get("/orders/active").json()["total"] == 2
    client.delete("/orders/4")
    assert client.get("/orders/status").json()["total"] == 3


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"item": "Dal"},
        {"item": " ", "count": 1},
        {"item": "x" * 121, "count": 1},
        {"item": "Dal", "count": 0},
        {"item": "Dal", "count": 101},
        {"item": "Dal", "count": "2"},
        {"item": "Dal", "count": True},
        {"item": "Dal", "count": 1.5},
        {"item": "Dal", "count": None},
        {"item": "Dal", "count": 1, "id": 99},
        {"item": "Dal", "count": 1, "status": "delivered"},
    ],
)
def test_invalid_create_does_not_change_storage(client: TestClient, payload: dict) -> None:
    response = client.post("/orders", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][0] == "body"
    assert client.get("/orders/status").json()["total"] == 3


@pytest.mark.parametrize(
    "query",
    [
        "limit=0",
        "limit=101",
        "offset=-1",
        "status=unknown",
        "limit=abc",
    ],
)
def test_invalid_queries(client: TestClient, query: str) -> None:
    assert client.get(f"/orders?{query}").status_code == 422


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_missing_and_invalid_ids(client: TestClient, method: str) -> None:
    kwargs = {"json": {"status": "preparing"}} if method == "patch" else {}
    response = client.request(method, "/orders/999", **kwargs)
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}
    assert client.request(method, "/orders/0", **kwargs).status_code == 422
    assert client.request(method, "/orders/abc", **kwargs).status_code == 422


@pytest.mark.parametrize(
    "payload", [{}, {"status": None}, {"status": "lost"}, {"status": "pending", "count": 5}]
)
def test_invalid_patch(client: TestClient, payload: dict) -> None:
    assert client.patch("/orders/1", json=payload).status_code == 422
    assert client.get("/orders/1").json()["status"] == "delivered"


def test_malformed_json_and_unsupported_method(client: TestClient) -> None:
    assert (
        client.post(
            "/orders",
            content="{",
            headers={
                "Content-Type": "application/json",
            },
        ).status_code
        == 422
    )
    assert client.put("/orders/1", json={}).status_code == 405


def test_concurrent_creates_have_unique_ids() -> None:
    """Exercise overlapping requests on one loop; this is not a load benchmark."""

    async def scenario() -> None:
        app = create_app(Settings())
        # HTTPX's ASGITransport does not start lifespan automatically.
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                responses = await asyncio.gather(
                    *[
                        client.post("/orders", json={"item": f"Dish {i}", "count": 1})
                        for i in range(25)
                    ]
                )
                assert all(response.status_code == 201 for response in responses)
                assert len({response.json()["id"] for response in responses}) == 25
                assert (await client.get("/orders/status")).json()["total"] == 28

    asyncio.run(scenario())
