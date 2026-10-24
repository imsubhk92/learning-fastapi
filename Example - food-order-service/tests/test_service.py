import re

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.dependencies import get_repository
from app.repository import OrderRepository
from main import create_app


def test_metadata_and_liveness(client: TestClient) -> None:
    assert client.get("/").json()["status"] == "healthy"
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/about").json()["version"] == "0.1.0"
    assert "one worker" in client.get("/about").json()["storage"]


def test_openapi_contract_and_documentation_pages(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    assert schema["openapi"].startswith("3.")
    assert schema["info"]["version"] == "0.1.0"
    assert "201" in schema["paths"]["/orders"]["post"]["responses"]
    assert "422" in schema["paths"]["/orders"]["post"]["responses"]
    assert "404" in schema["paths"]["/orders/{order_id}"]["get"]["responses"]
    assert "204" in schema["paths"]["/orders/{order_id}"]["delete"]["responses"]
    create_schema = schema["components"]["schemas"]["OrderCreate"]
    assert create_schema["additionalProperties"] is False
    assert create_schema["properties"]["count"]["minimum"] == 1
    assert not any(path.startswith(("/debug", "/ws")) for path in schema["paths"])
    operation_ids = [
        operation["operationId"] for path in schema["paths"].values() for operation in path.values()
    ]
    assert len(operation_ids) == len(set(operation_ids))
    assert "swagger-ui" in client.get("/docs").text
    assert "redoc" in client.get("/redoc").text


@pytest.mark.parametrize("path", ["/health", "/orders/999", "/orders/0", "/missing"])
def test_request_headers_on_success_and_handled_errors(client: TestClient, path: str) -> None:
    first = client.get(path, headers={"X-Request-ID": "untrusted-client-value"})
    second = client.get(path)
    assert re.fullmatch(r"[0-9a-f]{32}", first.headers["x-request-id"])
    assert first.headers["x-request-id"] != second.headers["x-request-id"]
    assert float(first.headers["x-response-time-ms"]) >= 0


def test_debug_disabled_by_default(client: TestClient) -> None:
    assert client.get("/debug/request-info").status_code == 404


def test_debug_does_not_echo_credentials_or_query_values() -> None:
    with TestClient(create_app(Settings(enable_debug_route=True))) as client:
        response = client.get(
            "/debug/request-info?token=secret-query",
            headers={
                "Authorization": "Bearer secret-auth",
                "Cookie": "session=secret-cookie",
                "X-Api-Key": "secret-key",
                "Accept": "application/json",
            },
        )
        assert response.status_code == 200
        assert "secret" not in response.text
        assert response.json()["headers"] == {"accept": "application/json"}
        assert response.json()["query_keys"] == ["token"]


def test_lifespan_isolates_apps_and_releases_resources() -> None:
    first_app = create_app(Settings())
    with TestClient(first_app) as first, TestClient(create_app(Settings())) as second:
        first.post("/orders", json={"item": "Dal", "count": 1})
        assert first.get("/orders/status").json()["total"] == 4
        assert second.get("/orders/status").json()["total"] == 3
    assert not hasattr(first_app.state, "orders")


def test_dependency_override() -> None:
    app = create_app(Settings())
    replacement = OrderRepository()
    replacement.delete(1)

    async def override() -> OrderRepository:
        return replacement

    app.dependency_overrides[get_repository] = override
    try:
        with TestClient(app) as client:
            assert client.get("/orders/status").json()["total"] == 2
    finally:
        app.dependency_overrides.clear()


def test_settings_reject_invalid_debug_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENABLE_DEBUG_ROUTE", "yes-please")
    with pytest.raises(ValueError, match="APP_ENABLE_DEBUG_ROUTE"):
        Settings.from_env()
    monkeypatch.setenv("APP_ENABLE_DEBUG_ROUTE", "true")
    assert Settings.from_env().enable_debug_route is True
