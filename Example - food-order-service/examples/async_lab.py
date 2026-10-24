"""Run without a server: python examples/async_lab.py.

Sleep simulates waiting; these timings are not an API performance benchmark.
"""

import asyncio
import time
from collections.abc import Awaitable, Callable


async def cooperative_wait() -> None:
    await asyncio.sleep(0.05)


async def blocking_wait() -> None:
    # Deliberately wrong in async code: the entire event loop stops here.
    time.sleep(0.05)  # noqa: ASYNC251


async def measure(label: str, operation: Callable[[], Awaitable[None]], limit: int) -> None:
    semaphore = asyncio.Semaphore(limit)

    async def bounded() -> None:
        async with semaphore:
            await operation()

    started = time.perf_counter()
    await asyncio.gather(*(bounded() for _ in range(6)))
    print(f"{label}: {time.perf_counter() - started:.3f}s")


async def main() -> None:
    await measure("await sleep, 6 tasks allowed", cooperative_wait, 6)
    await measure("await sleep, 2 tasks allowed", cooperative_wait, 2)
    await measure("blocking sleep inside async def", blocking_wait, 6)


if __name__ == "__main__":
    asyncio.run(main())
