"""A pull-based WebSocket lesson; not a broadcast or delivery system."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException, status

from app.dependencies import Repository
from app.models import OrderSnapshot

router = APIRouter()


@router.websocket("/ws/orders/{order_id}")
async def order_snapshots(websocket: WebSocket, order_id: int, repository: Repository) -> None:
    """Send a snapshot on connect and each 'refresh'; 'close' ends the connection."""
    if order_id <= 0 or repository.get(order_id) is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    await websocket.accept()
    try:
        while True:
            order = repository.get(order_id)
            if order is None:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return
            await websocket.send_json(OrderSnapshot(order=order).model_dump(mode="json"))
            message = await websocket.receive()
            if message["type"] == "websocket.disconnect":
                return
            if "text" not in message:
                await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
                return
            command = message["text"]
            if command == "close":
                await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)
                return
            if command != "refresh":
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return
    except WebSocketDisconnect:
        return  # A client leaving is an expected protocol event.
