"""Start a temporary real server, check HTTP/WebSockets, and always stop it.

Run from the project root: uv run --locked --extra dev python scripts/smoke_check.py
The OS chooses a loopback port; this does not deploy or leave a server running.
"""

import asyncio
import json
import os
import socket
import subprocess
import sys
import time

import httpx2
from websockets.asyncio.client import connect


async def check_websocket(port: int) -> None:
    async with connect(f"ws://127.0.0.1:{port}/ws/orders/3", open_timeout=3) as websocket:
        initial = json.loads(await asyncio.wait_for(websocket.recv(), timeout=3))
        assert initial["order"]["id"] == 3
        await websocket.send("refresh")
        assert json.loads(await asyncio.wait_for(websocket.recv(), timeout=3)) == initial
        await websocket.send("close")
        await asyncio.wait_for(websocket.wait_closed(), timeout=3)
        assert websocket.close_code == 1000


def main() -> None:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env={**os.environ, "APP_ENABLE_DEBUG_ROUTE": "false"},
    )
    try:
        with httpx2.Client(
            base_url=f"http://127.0.0.1:{port}", timeout=3, trust_env=False
        ) as client:
            for _ in range(60):
                if process.poll() is not None:
                    assert process.stdout is not None
                    raise RuntimeError(process.stdout.read())
                try:
                    health = client.get("/health")
                    if health.status_code == 200:
                        break
                except httpx2.TransportError:
                    pass
                time.sleep(0.05)
            else:
                raise RuntimeError("Server did not become ready")
            assert health.json() == {"status": "ok"}
            created = client.post("/orders", json={"item": "Smoke test dish", "count": 2})
            assert created.status_code == 201
            location = created.headers["location"]
            assert client.get(location).json() == created.json()
            assert client.patch(location, json={"status": "preparing"}).status_code == 200
            assert client.get("/orders/status").json()["total"] == 4
            assert client.post("/orders", json={"item": "Dal", "count": True}).status_code == 422
            assert client.get("/orders/999").status_code == 404
            assert client.get("/debug/request-info").status_code == 404
            assert "/orders" in client.get("/openapi.json").json()["paths"]
            assert "swagger-ui" in client.get("/docs").text
            assert "redoc" in client.get("/redoc").text
            asyncio.run(check_websocket(port))
            deleted = client.delete(location)
            assert deleted.status_code == 204 and deleted.content == b""
            assert client.get(location).status_code == 404
        print("Live Uvicorn checks passed: HTTP CRUD, errors, docs, debug default, WebSocket.")
    finally:
        process.terminate()
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(timeout=5)
        print(f"Temporary server stopped (exit {process.returncode}).")


if __name__ == "__main__":
    main()
