"""
LABBAIK AI v7.5 - OTA Scrapers Module
======================================
Respectful scrapers for OTA websites.

Features:
- Conservative rate limiting (5 req/min)
- User-agent rotation
- Error handling with backoff
- Result caching

Usage:
    from services.scrapers import get_scraper_manager

    manager = get_scraper_manager()
    result = manager.scrape_all_packages(
        departure_city="Jakarta",
        check_in=date(2025, 3, 1)
    )

    for offer in result["offers"]:
        print(f"{offer.name}: Rp {offer.price_idr:,.0f}")
"""

# Rate Limiter
from services.scrapers.rate_limiter import (
    RateLimiter,
    RateLimitConfig,
    RateLimitState,
    get_rate_limiter,
)

# Base Scraper
from services.scrapers.base_scraper import (
    BaseScraper,
    ScraperConfig,
)

# Scrapers
from services.scrapers.traveloka_scraper import (
    TravelokaScraper,
    create_traveloka_scraper,
)

from services.scrapers.tiket_scraper import (
    TiketScraper,
    create_tiket_scraper,
)

# Manager
from services.scrapers.scraper_manager import (
    ScraperManager,
    get_scraper_manager,
    create_scraper_manager,
)

__all__ = [
    # Rate Limiter
    "RateLimiter",
    "RateLimitConfig",
    "RateLimitState",
    "get_rate_limiter",
    # Base
    "BaseScraper",
    "ScraperConfig",
    # Scrapers
    "TravelokaScraper",
    "create_traveloka_scraper",
    "TiketScraper",
    "create_tiket_scraper",
    # Manager
    "ScraperManager",
    "get_scraper_manager",
    "create_scraper_manager",
]
