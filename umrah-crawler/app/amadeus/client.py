"""
Amadeus HTTP Client
====================
Async HTTP client with rate limiting, retry, and auto token refresh.
"""

import asyncio
import logging
import httpx
from typing import Any, Dict, Optional

from app.amadeus.auth import AmadeusAuth

logger = logging.getLogger(__name__)


class AmadeusClient:
    """Amadeus API client with rate limiting and retry."""

    def __init__(self, auth: AmadeusAuth, max_concurrency: int = 3):
        """
        Initialize Amadeus client.

        Args:
            auth: AmadeusAuth instance for token management
            max_concurrency: Max concurrent requests (default: 3)
        """
        self.auth = auth
        self.sem = asyncio.Semaphore(max_concurrency)

    async def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: float = 35.0,
    ) -> Dict[str, Any]:
        """
        Make authenticated request to Amadeus API.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (e.g., /v3/shopping/hotel-offers)
            params: Query parameters
            json: JSON body
            timeout: Request timeout in seconds

        Returns:
            JSON response dict

        Raises:
            httpx.HTTPError: On request failure after retries
        """
        token = await self.auth.token()
        url = f"{self.auth.base}{path}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        async with self.sem:
            for attempt in range(1, 4):
                try:
                    async with httpx.AsyncClient(timeout=timeout) as c:
                        r = await c.request(
                            method, url, headers=headers, params=params, json=json
                        )

                    # Auto refresh on 401 (expired token)
                    if r.status_code == 401 and attempt == 1:
                        logger.warning("Token expired, refreshing...")
                        self.auth.invalidate()
                        token = await self.auth.token()
                        headers["Authorization"] = f"Bearer {token}"
                        continue

                    # Retry on rate limit or server errors
                    if r.status_code in (429, 500, 502, 503, 504) and attempt < 3:
                        wait = 1.2 * attempt
                        logger.warning(f"HTTP {r.status_code}, retry in {wait}s...")
                        await asyncio.sleep(wait)
                        continue

                    r.raise_for_status()
                    return r.json()

                except httpx.HTTPError as e:
                    if attempt >= 3:
                        logger.error(f"Request failed after 3 attempts: {e}")
                        raise
                    await asyncio.sleep(1.2 * attempt)

        # Should not reach here
        raise RuntimeError("Request failed unexpectedly")
