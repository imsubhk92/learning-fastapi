"""Start the API first, then: python examples/websocket_client.py."""

import asyncio

from websockets.asyncio.client import connect


async def main() -> None:
    async with connect("ws://127.0.0.1:8001/ws/orders/3", open_timeout=5) as socket:
        print("Initial:", await socket.recv())
        await socket.send("refresh")
        print("Refreshed:", await socket.recv())
        await socket.send("close")
        await socket.wait_closed()
        print("Closed:", socket.close_code)


if __name__ == "__main__":
    asyncio.run(main())
