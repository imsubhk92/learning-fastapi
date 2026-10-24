import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect


def test_snapshot_refresh_and_close(client: TestClient) -> None:
    with client.websocket_connect("/ws/orders/3") as websocket:
        initial = websocket.receive_json()
        assert initial["event"] == "order_snapshot"
        assert initial["order"]["status"] == "pending"
        assert client.patch("/orders/3", json={"status": "preparing"}).status_code == 200
        websocket.send_text("refresh")
        assert websocket.receive_json()["order"]["status"] == "preparing"
        websocket.send_text("close")
        with pytest.raises(WebSocketDisconnect) as closed:
            websocket.receive_json()
        assert closed.value.code == 1000


@pytest.mark.parametrize("order_id", [0, -1, 999])
def test_reject_missing_order(client: TestClient, order_id: int) -> None:
    with pytest.raises(WebSocketDisconnect) as closed:
        with client.websocket_connect(f"/ws/orders/{order_id}"):
            pass
    assert closed.value.code == 1008


@pytest.mark.parametrize("binary", [False, True])
def test_reject_unsupported_messages(client: TestClient, binary: bool) -> None:
    with client.websocket_connect("/ws/orders/1") as websocket:
        websocket.receive_json()
        if binary:
            websocket.send_bytes(b"refresh")
        else:
            websocket.send_text("unknown")
        with pytest.raises(WebSocketDisconnect) as closed:
            websocket.receive_json()
        assert closed.value.code == (1003 if binary else 1008)


def test_deleted_order_closes_on_refresh(client: TestClient) -> None:
    with client.websocket_connect("/ws/orders/1") as websocket:
        websocket.receive_json()
        client.delete("/orders/1")
        websocket.send_text("refresh")
        with pytest.raises(WebSocketDisconnect) as closed:
            websocket.receive_json()
        assert closed.value.code == 1008
