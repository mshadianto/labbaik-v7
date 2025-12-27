"""
Amadeus OAuth2 Authentication
==============================
Token caching with auto-refresh.

Environment variables:
- AMADEUS_CLIENT_ID: API client ID
- AMADEUS_CLIENT_SECRET: API client secret
- AMADEUS_ENV: "test" or "production" (default: test)
"""

import os
import time
import logging
import httpx

logger = logging.getLogger(__name__)


class AmadeusAuth:
    """Amadeus OAuth2 authentication with token caching."""

    def __init__(self):
        self.client_id = os.getenv("AMADEUS_CLIENT_ID")
        self.client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
        self.env = os.getenv("AMADEUS_ENV", "test").lower()

        if self.env == "production":
            self.base = "https://api.amadeus.com"
        else:
            self.base = "https://test.api.amadeus.com"

        self._token = None
        self._exp = 0

        if not self.client_id or not self.client_secret:
            raise RuntimeError("Missing AMADEUS_CLIENT_ID / AMADEUS_CLIENT_SECRET")

        logger.info(f"AmadeusAuth initialized: env={self.env}, base={self.base}")

    async def token(self) -> str:
        """Get valid access token, refreshing if needed."""
        now = int(time.time())

        # Return cached token if still valid (with 60s buffer)
        if self._token and now < (self._exp - 60):
            return self._token

        url = f"{self.base}/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        async with httpx.AsyncClient(timeout=25) as c:
            r = await c.post(url, data=data)
            r.raise_for_status()
            j = r.json()

        self._token = j["access_token"]
        self._exp = now + int(j.get("expires_in", 1799))

        logger.info(f"Amadeus token refreshed, expires in {j.get('expires_in')}s")
        return self._token

    def invalidate(self):
        """Force token refresh on next request."""
        self._token = None
        self._exp = 0
