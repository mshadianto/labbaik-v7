"""Rate limiter for API requests."""
import asyncio
import time


class RateLimiter:
    """Async rate limiter to control request frequency."""

    def __init__(self, rps: float):
        """
        Initialize rate limiter.

        Args:
            rps: Requests per second limit
        """
        self.rps = max(rps, 0.1)
        self.min_interval = 1.0 / self.rps
        self._lock = asyncio.Lock()
        self._last = 0.0

    async def wait(self):
        """Wait if necessary to respect rate limit."""
        async with self._lock:
            now = time.time()
            delta = now - self._last
            if delta < self.min_interval:
                await asyncio.sleep(self.min_interval - delta)
            self._last = time.time()
