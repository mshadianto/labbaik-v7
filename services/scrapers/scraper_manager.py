"""
LABBAIK AI v7.5 - Scraper Manager
==================================
Orchestrator for all OTA scrapers.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor, as_completed

from services.price_aggregation.models import AggregatedOffer
from services.scrapers.base_scraper import BaseScraper
from services.scrapers.rate_limiter import get_rate_limiter
from services.scrapers.traveloka_scraper import TravelokaScraper, create_traveloka_scraper
from services.scrapers.tiket_scraper import TiketScraper, create_tiket_scraper

logger = logging.getLogger(__name__)


class ScraperManager:
    """
    Orchestrator for all OTA scrapers.

    Features:
    - Manages multiple scrapers
    - Parallel scraping with thread pool
    - Rate limiting coordination
    - Error handling and fallbacks
    - Statistics tracking
    """

    def __init__(
        self,
        enable_traveloka: bool = True,
        enable_tiket: bool = True,
        enable_pegipegi: bool = False,  # Not implemented yet
        max_workers: int = 3
    ):
        self.scrapers: Dict[str, BaseScraper] = {}
        self.max_workers = max_workers
        self.rate_limiter = get_rate_limiter()

        # Initialize scrapers
        if enable_traveloka:
            self.scrapers["traveloka"] = create_traveloka_scraper(enabled=True)

        if enable_tiket:
            self.scrapers["tiket"] = create_tiket_scraper(enabled=True)

        # PegiPegi can be added later
        # if enable_pegipegi:
        #     self.scrapers["pegipegi"] = create_pegipegi_scraper(enabled=True)

        # Statistics
        self._stats = {
            "total_scrapes": 0,
            "successful_scrapes": 0,
            "failed_scrapes": 0,
            "total_offers_found": 0,
            "last_scrape_at": None
        }

    def scrape_all_packages(
        self,
        departure_city: str = "Jakarta",
        check_in: date = None,
        check_out: date = None,
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Scrape packages from all enabled scrapers.

        Args:
            departure_city: Departure city
            check_in: Departure date
            check_out: Return date
            parallel: Run scrapers in parallel

        Returns:
            Dictionary with offers and stats per source
        """
        logger.info(f"Starting package scrape from {departure_city}")

        start_time = datetime.now()
        all_offers: List[AggregatedOffer] = []
        source_stats = {}
        errors = []

        enabled_scrapers = {
            name: scraper
            for name, scraper in self.scrapers.items()
            if scraper.is_enabled() and not self.rate_limiter.is_blocked(name)
        }

        if not enabled_scrapers:
            logger.warning("No scrapers enabled or all blocked")
            return {
                "offers": [],
                "source_stats": {},
                "errors": ["No scrapers available"],
                "duration_ms": 0
            }

        if parallel and len(enabled_scrapers) > 1:
            # Parallel scraping
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(
                        scraper.scrape_packages,
                        departure_city,
                        check_in,
                        check_out
                    ): name
                    for name, scraper in enabled_scrapers.items()
                }

                for future in as_completed(futures):
                    name = futures[future]
                    try:
                        offers = future.result()
                        all_offers.extend(offers)
                        source_stats[name] = len(offers)
                        self._stats["successful_scrapes"] += 1
                    except Exception as e:
                        logger.error(f"Scraper {name} failed: {e}")
                        errors.append(f"{name}: {str(e)}")
                        source_stats[name] = 0
                        self._stats["failed_scrapes"] += 1
        else:
            # Sequential scraping
            for name, scraper in enabled_scrapers.items():
                try:
                    offers = scraper.scrape_packages(
                        departure_city,
                        check_in,
                        check_out
                    )
                    all_offers.extend(offers)
                    source_stats[name] = len(offers)
                    self._stats["successful_scrapes"] += 1
                except Exception as e:
                    logger.error(f"Scraper {name} failed: {e}")
                    errors.append(f"{name}: {str(e)}")
                    source_stats[name] = 0
                    self._stats["failed_scrapes"] += 1

        # Update stats
        self._stats["total_scrapes"] += len(enabled_scrapers)
        self._stats["total_offers_found"] += len(all_offers)
        self._stats["last_scrape_at"] = datetime.now().isoformat()

        duration_ms = (datetime.now() - start_time).total_seconds() * 1000

        logger.info(
            f"Package scrape complete: {len(all_offers)} offers "
            f"from {len(source_stats)} sources in {duration_ms:.0f}ms"
        )

        return {
            "offers": all_offers,
            "source_stats": source_stats,
            "errors": errors if errors else None,
            "duration_ms": round(duration_ms, 2)
        }

    def scrape_all_hotels(
        self,
        city: str,
        check_in: date = None,
        check_out: date = None,
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Scrape hotels from all enabled scrapers.

        Note: Most scrapers currently don't implement hotel scraping.
        """
        logger.info(f"Starting hotel scrape for {city}")

        start_time = datetime.now()
        all_offers: List[AggregatedOffer] = []
        source_stats = {}
        errors = []

        enabled_scrapers = {
            name: scraper
            for name, scraper in self.scrapers.items()
            if scraper.is_enabled() and not self.rate_limiter.is_blocked(name)
        }

        if parallel and len(enabled_scrapers) > 1:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(
                        scraper.scrape_hotels,
                        city,
                        check_in,
                        check_out
                    ): name
                    for name, scraper in enabled_scrapers.items()
                }

                for future in as_completed(futures):
                    name = futures[future]
                    try:
                        offers = future.result()
                        all_offers.extend(offers)
                        source_stats[name] = len(offers)
                    except Exception as e:
                        logger.error(f"Hotel scraper {name} failed: {e}")
                        errors.append(f"{name}: {str(e)}")
                        source_stats[name] = 0
        else:
            for name, scraper in enabled_scrapers.items():
                try:
                    offers = scraper.scrape_hotels(city, check_in, check_out)
                    all_offers.extend(offers)
                    source_stats[name] = len(offers)
                except Exception as e:
                    logger.error(f"Hotel scraper {name} failed: {e}")
                    errors.append(f"{name}: {str(e)}")
                    source_stats[name] = 0

        duration_ms = (datetime.now() - start_time).total_seconds() * 1000

        return {
            "offers": all_offers,
            "source_stats": source_stats,
            "errors": errors if errors else None,
            "duration_ms": round(duration_ms, 2)
        }

    def scrape_source(
        self,
        source_name: str,
        departure_city: str = "Jakarta",
        check_in: date = None,
        check_out: date = None
    ) -> List[AggregatedOffer]:
        """Scrape from a specific source."""
        scraper = self.scrapers.get(source_name)

        if not scraper:
            logger.warning(f"Scraper not found: {source_name}")
            return []

        if not scraper.is_enabled():
            logger.warning(f"Scraper disabled: {source_name}")
            return []

        if self.rate_limiter.is_blocked(source_name):
            logger.warning(f"Scraper blocked: {source_name}")
            return []

        try:
            return scraper.scrape_packages(departure_city, check_in, check_out)
        except Exception as e:
            logger.error(f"Scrape failed for {source_name}: {e}")
            return []

    def enable_scraper(self, source_name: str) -> bool:
        """Enable a scraper."""
        if source_name in self.scrapers:
            self.scrapers[source_name].config.enabled = True
            return True
        return False

    def disable_scraper(self, source_name: str) -> bool:
        """Disable a scraper."""
        if source_name in self.scrapers:
            self.scrapers[source_name].config.enabled = False
            return True
        return False

    def get_available_scrapers(self) -> List[str]:
        """Get list of available scraper names."""
        return list(self.scrapers.keys())

    def get_enabled_scrapers(self) -> List[str]:
        """Get list of enabled scraper names."""
        return [
            name for name, scraper in self.scrapers.items()
            if scraper.is_enabled()
        ]

    def get_stats(self) -> Dict[str, Any]:
        """Get scraper statistics."""
        scraper_stats = {}

        for name, scraper in self.scrapers.items():
            scraper_stats[name] = {
                "enabled": scraper.is_enabled(),
                "rate_limit": self.rate_limiter.get_stats(name)
            }

        return {
            "manager": self._stats,
            "scrapers": scraper_stats
        }

    def reset_rate_limits(self, source_name: str = None) -> None:
        """Reset rate limits for a source or all sources."""
        self.rate_limiter.reset(source_name)

    def close_all(self) -> None:
        """Close all scraper sessions."""
        for scraper in self.scrapers.values():
            try:
                scraper.close()
            except Exception as e:
                logger.warning(f"Error closing scraper: {e}")


# Singleton
_scraper_manager: Optional[ScraperManager] = None


def get_scraper_manager() -> ScraperManager:
    """Get singleton scraper manager."""
    global _scraper_manager
    if _scraper_manager is None:
        _scraper_manager = ScraperManager()
    return _scraper_manager


def create_scraper_manager(
    enable_traveloka: bool = True,
    enable_tiket: bool = True,
    enable_pegipegi: bool = False,
    max_workers: int = 3
) -> ScraperManager:
    """Create a configured scraper manager."""
    return ScraperManager(
        enable_traveloka=enable_traveloka,
        enable_tiket=enable_tiket,
        enable_pegipegi=enable_pegipegi,
        max_workers=max_workers
    )
