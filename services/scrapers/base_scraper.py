"""
LABBAIK AI v7.5 - Base Scraper
==============================
Abstract base class for OTA scrapers.
"""

import logging
import random
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from dataclasses import dataclass

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from services.price_aggregation.models import AggregatedOffer, SourceType, OfferType
from services.scrapers.rate_limiter import get_rate_limiter, RateLimiter

logger = logging.getLogger(__name__)


@dataclass
class ScraperConfig:
    """Configuration for a scraper."""
    name: str
    base_url: str
    enabled: bool = True
    timeout: int = 30
    max_retries: int = 3
    user_agent_rotate: bool = True


class BaseScraper(ABC):
    """
    Abstract base class for OTA scrapers.

    Implements common functionality:
    - HTTP session management
    - User-agent rotation
    - Rate limiting integration
    - Error handling
    - Response parsing
    """

    # Common user agents for rotation
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]

    def __init__(self, config: ScraperConfig):
        self.config = config
        self.rate_limiter = get_rate_limiter()
        self._session: Optional[requests.Session] = None

    @property
    def session(self) -> requests.Session:
        """Get or create HTTP session with retry logic."""
        if self._session is None:
            self._session = requests.Session()

            # Configure retries
            retry_strategy = Retry(
                total=self.config.max_retries,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET", "POST"]
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self._session.mount("http://", adapter)
            self._session.mount("https://", adapter)

            # Set default headers
            self._session.headers.update(self._get_default_headers())

        return self._session

    def _get_default_headers(self) -> Dict[str, str]:
        """Get default HTTP headers."""
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
        }

        if self.config.user_agent_rotate:
            headers["User-Agent"] = random.choice(self.USER_AGENTS)
        else:
            headers["User-Agent"] = self.USER_AGENTS[0]

        return headers

    def _rotate_user_agent(self) -> None:
        """Rotate to a new random user agent."""
        if self._session and self.config.user_agent_rotate:
            self._session.headers["User-Agent"] = random.choice(self.USER_AGENTS)

    @abstractmethod
    def scrape_packages(
        self,
        departure_city: str = "Jakarta",
        check_in: date = None,
        check_out: date = None,
        **kwargs
    ) -> List[AggregatedOffer]:
        """
        Scrape umrah packages from the OTA.

        Args:
            departure_city: Departure city (Jakarta, Surabaya, etc.)
            check_in: Check-in/departure date
            check_out: Check-out/return date
            **kwargs: Additional source-specific parameters

        Returns:
            List of AggregatedOffer objects
        """
        pass

    @abstractmethod
    def scrape_hotels(
        self,
        city: str,
        check_in: date = None,
        check_out: date = None,
        **kwargs
    ) -> List[AggregatedOffer]:
        """
        Scrape hotels from the OTA.

        Args:
            city: City name (Makkah, Madinah)
            check_in: Check-in date
            check_out: Check-out date
            **kwargs: Additional source-specific parameters

        Returns:
            List of AggregatedOffer objects
        """
        pass

    def _make_request(
        self,
        url: str,
        method: str = "GET",
        params: Dict = None,
        data: Dict = None,
        json_data: Dict = None,
        headers: Dict = None
    ) -> Optional[requests.Response]:
        """
        Make an HTTP request with rate limiting and error handling.

        Returns:
            Response object or None on failure
        """
        source = self.config.name

        # Check rate limit
        if not self.rate_limiter.can_request(source):
            self.rate_limiter.wait_if_needed(source)

        # Rotate user agent periodically
        self._rotate_user_agent()

        try:
            # Wait for rate limit
            self.rate_limiter.wait_if_needed(source)

            # Make request
            if method.upper() == "GET":
                response = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.config.timeout
                )
            elif method.upper() == "POST":
                response = self.session.post(
                    url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=headers,
                    timeout=self.config.timeout
                )
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return None

            # Record request
            self.rate_limiter.record_request(source)

            # Check response
            response.raise_for_status()

            # Record success
            self.rate_limiter.record_success(source)

            return response

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout scraping {source}: {url}")
            self.rate_limiter.record_failure(source)
            return None

        except requests.exceptions.HTTPError as e:
            logger.warning(f"HTTP error scraping {source}: {e}")
            self.rate_limiter.record_failure(source)
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error scraping {source}: {e}")
            self.rate_limiter.record_failure(source)
            return None

    def _parse_price(self, price_str: str, currency: str = "IDR") -> float:
        """
        Parse price string to float.

        Handles formats like:
        - "Rp 25.000.000"
        - "25,000,000"
        - "IDR 25000000"
        """
        if not price_str:
            return 0.0

        # Remove currency symbols and text
        clean = price_str.replace("Rp", "").replace("IDR", "").replace("SAR", "")
        clean = clean.replace(",", "").replace(".", "").replace(" ", "")

        try:
            return float(clean)
        except ValueError:
            logger.warning(f"Failed to parse price: {price_str}")
            return 0.0

    def _parse_duration(self, duration_str: str) -> int:
        """
        Parse duration string to days.

        Handles formats like:
        - "9 Hari"
        - "9D8N"
        - "9 Days / 8 Nights"
        """
        if not duration_str:
            return 0

        import re

        # Try to find number of days
        patterns = [
            r"(\d+)\s*[Hh]ari",
            r"(\d+)\s*[Dd]ays?",
            r"(\d+)[Dd]",
        ]

        for pattern in patterns:
            match = re.search(pattern, duration_str)
            if match:
                return int(match.group(1))

        return 0

    def _parse_stars(self, stars_str: str) -> int:
        """
        Parse stars from string.

        Handles formats like:
        - "5 Star"
        - "★★★★★"
        - "Bintang 5"
        """
        if not stars_str:
            return 3

        import re

        # Count star characters
        star_count = stars_str.count("★") + stars_str.count("⭐")
        if star_count > 0:
            return min(5, star_count)

        # Look for number
        match = re.search(r"(\d)", stars_str)
        if match:
            return min(5, max(1, int(match.group(1))))

        return 3

    def _create_offer(
        self,
        name: str,
        price_idr: float,
        offer_type: OfferType,
        city: str = None,
        **kwargs
    ) -> AggregatedOffer:
        """Create an AggregatedOffer with common fields set."""
        return AggregatedOffer(
            source_type=SourceType.SCRAPER,
            source_name=self.config.name,
            offer_type=offer_type,
            name=name,
            city=city or "",
            price_idr=price_idr,
            currency_original="IDR",
            scraped_at=datetime.now(),
            **kwargs
        )

    def close(self) -> None:
        """Close HTTP session."""
        if self._session:
            self._session.close()
            self._session = None

    def is_enabled(self) -> bool:
        """Check if scraper is enabled."""
        return self.config.enabled

    def get_source_name(self) -> str:
        """Get scraper source name."""
        return self.config.name

    def get_stats(self) -> Dict[str, Any]:
        """Get scraper statistics."""
        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "rate_limit": self.rate_limiter.get_stats(self.config.name)
        }
