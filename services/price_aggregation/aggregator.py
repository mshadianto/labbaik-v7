"""
LABBAIK AI v7.5 - Price Aggregator
===================================
Main orchestrator for multi-source price aggregation.
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor, as_completed

from services.price_aggregation.models import (
    AggregatedOffer, SourceType, OfferType, AvailabilityStatus,
    convert_sar_to_idr
)
from services.price_aggregation.normalizer import PriceNormalizer, OfferDeduplicator
from services.price_aggregation.cache_manager import get_price_cache, get_source_cache
from services.price_aggregation.repository import get_aggregated_price_repository
from services.price_aggregation.n8n_adapter import get_n8n_adapter

logger = logging.getLogger(__name__)


class PriceAggregator:
    """
    Main orchestrator for aggregating prices from multiple sources.

    Sources:
    1. Existing APIs (Amadeus, Xotelo, MakCorps) via HybridUmrahDataManager
    2. n8n Price Intelligence (hotels, flights, packages from n8n workflow)
    3. OTA Scrapers (Traveloka, Tiket, PegiPegi) - future
    4. Partner Price Feeds
    5. Database Cache (fallback)
    """

    def __init__(
        self,
        use_apis: bool = True,
        use_n8n: bool = True,
        use_scrapers: bool = False,
        use_partner_feeds: bool = True,
        use_cache: bool = True,
        save_to_db: bool = True
    ):
        self.use_apis = use_apis
        self.use_n8n = use_n8n
        self.use_scrapers = use_scrapers
        self.use_partner_feeds = use_partner_feeds
        self.use_cache = use_cache
        self.save_to_db = save_to_db

        self.normalizer = PriceNormalizer()
        self.deduplicator = OfferDeduplicator()
        self.price_cache = get_price_cache()
        self.source_cache = get_source_cache()

        # Lazy-load repository
        self._repository = None

        # Data manager will be set externally or created lazily
        self._data_manager = None
        self._scraper_manager = None
        self._n8n_adapter = None

    @property
    def repository(self):
        """Lazy-load repository."""
        if self._repository is None:
            self._repository = get_aggregated_price_repository()
        return self._repository

    def set_data_manager(self, manager):
        """Set the HybridUmrahDataManager instance."""
        self._data_manager = manager

    def set_scraper_manager(self, manager):
        """Set the ScraperManager instance."""
        self._scraper_manager = manager

    @property
    def n8n_adapter(self):
        """Lazy-load n8n adapter."""
        if self._n8n_adapter is None:
            self._n8n_adapter = get_n8n_adapter()
        return self._n8n_adapter

    def aggregate(
        self,
        city: str = None,
        offer_type: str = None,
        check_in: date = None,
        check_out: date = None,
        min_price: float = None,
        max_price: float = None,
        min_stars: int = None,
        sources: List[str] = None,
        sort_by: str = "price",
        limit: int = 50,
        force_refresh: bool = False
    ) -> Dict[str, Any]:
        """
        Aggregate prices from all configured sources.

        Args:
            city: Filter by city (Makkah/Madinah)
            offer_type: Filter by type (hotel/package)
            check_in: Check-in date
            check_out: Check-out date
            min_price: Minimum price in IDR
            max_price: Maximum price in IDR
            min_stars: Minimum hotel stars
            sources: List of source names to include
            sort_by: Sort field (price, stars, distance, updated)
            limit: Maximum results
            force_refresh: Force refresh from sources (bypass cache)

        Returns:
            Dictionary with offers, stats, and metadata
        """
        start_time = datetime.now()

        # Check cache first
        cache_key = self.price_cache.build_key(
            city=city,
            offer_type=offer_type,
            check_in=check_in,
            check_out=check_out,
            min_price=min_price,
            max_price=max_price,
            min_stars=min_stars,
            sources=sources
        )

        if self.use_cache and not force_refresh:
            cached = self.price_cache.get(cache_key)
            if cached:
                logger.info(f"Returning cached aggregation ({len(cached['offers'])} offers)")
                return cached

        all_offers: List[AggregatedOffer] = []
        source_stats = {}
        errors = []

        # 1. Fetch from existing APIs
        if self.use_apis and self._data_manager:
            try:
                api_offers, api_stats = self._fetch_from_apis(
                    city=city,
                    check_in=check_in,
                    check_out=check_out
                )
                all_offers.extend(api_offers)
                source_stats.update(api_stats)
            except Exception as e:
                logger.error(f"API fetch failed: {e}")
                errors.append(f"API: {str(e)}")

        # 2. Fetch from n8n Price Intelligence
        if self.use_n8n:
            try:
                n8n_offers, n8n_stats = self._fetch_from_n8n(
                    city=city,
                    offer_type=offer_type,
                    min_stars=min_stars
                )
                all_offers.extend(n8n_offers)
                source_stats.update(n8n_stats)
            except Exception as e:
                logger.error(f"n8n fetch failed: {e}")
                errors.append(f"n8n: {str(e)}")

        # 3. Fetch from OTA scrapers (future)
        if self.use_scrapers and self._scraper_manager:
            try:
                scraper_offers, scraper_stats = self._fetch_from_scrapers(
                    city=city,
                    check_in=check_in,
                    check_out=check_out
                )
                all_offers.extend(scraper_offers)
                source_stats.update(scraper_stats)
            except Exception as e:
                logger.error(f"Scraper fetch failed: {e}")
                errors.append(f"Scrapers: {str(e)}")

        # 3. Fetch from partner feeds
        if self.use_partner_feeds:
            try:
                partner_offers, partner_stats = self._fetch_from_partners(city=city)
                all_offers.extend(partner_offers)
                source_stats.update(partner_stats)
            except Exception as e:
                logger.error(f"Partner feed fetch failed: {e}")
                errors.append(f"Partners: {str(e)}")

        # 4. Fetch from database cache
        if len(all_offers) < limit:
            try:
                db_offers = self._fetch_from_database(
                    city=city,
                    offer_type=offer_type,
                    check_in=check_in,
                    check_out=check_out,
                    min_price=min_price,
                    max_price=max_price,
                    min_stars=min_stars,
                    sources=sources,
                    limit=limit
                )
                all_offers.extend(db_offers)
                source_stats["database"] = len(db_offers)
            except Exception as e:
                logger.error(f"Database fetch failed: {e}")
                errors.append(f"Database: {str(e)}")

        # Normalize all offers
        normalized_offers = []
        for offer in all_offers:
            try:
                normalized = self.normalizer.normalize(offer)
                normalized_offers.append(normalized)
            except Exception as e:
                logger.warning(f"Failed to normalize offer: {e}")

        # Deduplicate
        deduplicated = self.deduplicator.deduplicate(
            normalized_offers,
            keep_all_sources=True
        )

        # Apply filters
        filtered = self._apply_filters(
            deduplicated,
            city=city,
            offer_type=offer_type,
            min_price=min_price,
            max_price=max_price,
            min_stars=min_stars,
            sources=sources
        )

        # Sort
        sorted_offers = self._sort_offers(filtered, sort_by)

        # Limit
        final_offers = sorted_offers[:limit]

        # Save to database if enabled
        if self.save_to_db and final_offers:
            try:
                self._save_to_database(final_offers)
            except Exception as e:
                logger.error(f"Failed to save to database: {e}")
                errors.append(f"Save: {str(e)}")

        # Build response
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000

        result = {
            "offers": final_offers,
            "total_found": len(deduplicated),
            "total_returned": len(final_offers),
            "source_stats": source_stats,
            "cache_hit": False,
            "errors": errors if errors else None,
            "aggregated_at": datetime.now().isoformat(),
            "duration_ms": round(duration_ms, 2),
            "filters_applied": {
                "city": city,
                "offer_type": offer_type,
                "min_price": min_price,
                "max_price": max_price,
                "min_stars": min_stars,
                "sources": sources
            }
        }

        # Cache result
        if self.use_cache:
            self.price_cache.set(cache_key, result, ttl=300)

        logger.info(
            f"Aggregation complete: {len(final_offers)} offers "
            f"from {len(source_stats)} sources in {duration_ms:.0f}ms"
        )

        return result

    def _fetch_from_apis(
        self,
        city: str = None,
        check_in: date = None,
        check_out: date = None
    ) -> tuple[List[AggregatedOffer], Dict[str, int]]:
        """Fetch from existing APIs via HybridUmrahDataManager."""
        offers = []
        stats = {}

        if not self._data_manager:
            return offers, stats

        cities = [city] if city else ["Makkah", "Madinah"]
        check_in_str = check_in.strftime("%Y-%m-%d") if check_in else None
        check_out_str = check_out.strftime("%Y-%m-%d") if check_out else None

        for city_name in cities:
            try:
                # Use existing search_hotels method
                hotel_offers = self._data_manager.search_hotels(
                    city=city_name,
                    check_in=check_in_str,
                    check_out=check_out_str,
                    max_results=50
                )

                # Convert HotelOffer to AggregatedOffer
                for hotel in hotel_offers:
                    agg_offer = self._convert_hotel_offer(hotel)
                    if agg_offer:
                        offers.append(agg_offer)

                        # Track source stats
                        source = agg_offer.source_name
                        stats[source] = stats.get(source, 0) + 1

            except Exception as e:
                logger.error(f"Failed to fetch hotels for {city_name}: {e}")

        return offers, stats

    def _convert_hotel_offer(self, hotel_offer) -> Optional[AggregatedOffer]:
        """Convert HotelOffer from data_fetcher to AggregatedOffer."""
        try:
            # Determine source type
            source_name = hotel_offer.source
            if "amadeus" in source_name.lower():
                source_type = SourceType.API
                source_name = "amadeus"
            elif "xotelo" in source_name.lower():
                source_type = SourceType.API
                source_name = "xotelo"
            elif "makcorps" in source_name.lower():
                source_type = SourceType.API
                source_name = "makcorps"
            elif "demo" in source_name.lower():
                source_type = SourceType.DEMO
                source_name = "demo"
            else:
                source_type = SourceType.CACHE

            return AggregatedOffer(
                source_type=source_type,
                source_name=source_name,
                source_offer_id=hotel_offer.hotel_id,
                offer_type=OfferType.HOTEL,
                name=hotel_offer.hotel_name,
                city=hotel_offer.city,
                stars=hotel_offer.stars,
                distance_to_haram_m=int(hotel_offer.distance_to_haram_km * 1000),
                walking_time_minutes=hotel_offer.walking_time_minutes,
                amenities=hotel_offer.amenities,
                price_sar=hotel_offer.total_price_sar,
                price_idr=hotel_offer.total_price_idr,
                price_per_night_sar=hotel_offer.price_per_night_sar,
                price_per_night_idr=hotel_offer.price_per_night_idr,
                currency_original="SAR",
                is_available=hotel_offer.availability == "Available",
                scraped_at=datetime.fromisoformat(hotel_offer.scraped_at) if hotel_offer.scraped_at else datetime.now()
            )
        except Exception as e:
            logger.warning(f"Failed to convert hotel offer: {e}")
            return None

    def _fetch_from_n8n(
        self,
        city: str = None,
        offer_type: str = None,
        min_stars: int = None
    ) -> tuple[List[AggregatedOffer], Dict[str, int]]:
        """
        Fetch from n8n Price Intelligence tables.

        Sources:
        - prices_hotels: Hotel data from Booking.com simulation
        - prices_flights: Flight data from AviationStack simulation
        - prices_packages: Package data from travel agents
        """
        offers = []
        stats = {}

        try:
            n8n_offers, n8n_stats = self.n8n_adapter.fetch_all(
                city=city,
                offer_type=offer_type,
                min_stars=min_stars,
                limit=50
            )
            offers.extend(n8n_offers)
            stats.update(n8n_stats)

            logger.info(f"Fetched {len(offers)} offers from n8n Price Intelligence")

        except Exception as e:
            logger.error(f"Failed to fetch from n8n: {e}")

        return offers, stats

    def _fetch_from_scrapers(
        self,
        city: str = None,
        check_in: date = None,
        check_out: date = None
    ) -> tuple[List[AggregatedOffer], Dict[str, int]]:
        """Fetch from OTA scrapers (future implementation)."""
        offers = []
        stats = {}

        if not self._scraper_manager:
            return offers, stats

        # Will be implemented when scrapers are ready
        # scraper_results = self._scraper_manager.scrape_all(city, check_in, check_out)

        return offers, stats

    def _fetch_from_partners(
        self,
        city: str = None
    ) -> tuple[List[AggregatedOffer], Dict[str, int]]:
        """Fetch approved partner price feeds."""
        offers = []
        stats = {"partner": 0}

        try:
            partner_feeds = self.repository.get_approved_partner_feeds(city=city)

            for feed in partner_feeds:
                # Convert partner feed to AggregatedOffer
                agg_offer = AggregatedOffer(
                    source_type=SourceType.PARTNER,
                    source_name="partner",
                    source_offer_id=feed.id,
                    offer_type=OfferType.PACKAGE,
                    name=feed.package_name or feed.feed_name,
                    city=feed.departure_city or "Jakarta",
                    duration_days=feed.duration_days,
                    departure_city=feed.departure_city,
                    airline=feed.airline,
                    hotel_makkah=feed.hotel_makkah,
                    hotel_makkah_stars=feed.hotel_makkah_stars,
                    hotel_madinah=feed.hotel_madinah,
                    hotel_madinah_stars=feed.hotel_madinah_stars,
                    inclusions=feed.inclusions,
                    price_sar=feed.price_sar or 0,
                    price_idr=feed.price_idr,
                    currency_original="IDR",
                    quota=feed.quota,
                    is_available=feed.is_available and (feed.quota - feed.booked) > 0,
                    valid_from=datetime.combine(feed.valid_from, datetime.min.time()) if feed.valid_from else None,
                    valid_until=datetime.combine(feed.valid_until, datetime.max.time()) if feed.valid_until else None,
                    confidence_score=0.95
                )
                offers.append(agg_offer)
                stats["partner"] += 1

        except Exception as e:
            logger.error(f"Failed to fetch partner feeds: {e}")

        return offers, stats

    def _fetch_from_database(
        self,
        city: str = None,
        offer_type: str = None,
        check_in: date = None,
        check_out: date = None,
        min_price: float = None,
        max_price: float = None,
        min_stars: int = None,
        sources: List[str] = None,
        limit: int = 50
    ) -> List[AggregatedOffer]:
        """Fetch cached offers from database."""
        return self.repository.search(
            city=city,
            offer_type=offer_type,
            check_in=check_in,
            min_price=min_price,
            max_price=max_price,
            min_stars=min_stars,
            sources=sources,
            sort_by="updated",
            limit=limit
        )

    def _apply_filters(
        self,
        offers: List[AggregatedOffer],
        city: str = None,
        offer_type: str = None,
        min_price: float = None,
        max_price: float = None,
        min_stars: int = None,
        sources: List[str] = None
    ) -> List[AggregatedOffer]:
        """Apply filters to offers."""
        filtered = offers

        if city:
            filtered = [o for o in filtered if o.city.lower() == city.lower()]

        if offer_type:
            filtered = [o for o in filtered if o.offer_type.value == offer_type]

        if min_price is not None:
            filtered = [o for o in filtered if o.price_idr >= min_price]

        if max_price is not None:
            filtered = [o for o in filtered if o.price_idr <= max_price]

        if min_stars is not None:
            filtered = [o for o in filtered if o.stars and o.stars >= min_stars]

        if sources:
            filtered = [o for o in filtered if o.source_name in sources]

        return filtered

    def _sort_offers(
        self,
        offers: List[AggregatedOffer],
        sort_by: str
    ) -> List[AggregatedOffer]:
        """Sort offers by specified field."""
        if sort_by == "price":
            return sorted(offers, key=lambda x: x.price_idr or float('inf'))
        elif sort_by == "price_desc":
            return sorted(offers, key=lambda x: x.price_idr or 0, reverse=True)
        elif sort_by == "stars":
            return sorted(offers, key=lambda x: x.stars or 0, reverse=True)
        elif sort_by == "distance":
            return sorted(offers, key=lambda x: x.distance_to_haram_m or float('inf'))
        elif sort_by == "updated":
            return sorted(offers, key=lambda x: x.scraped_at or datetime.min, reverse=True)
        else:
            return offers

    def _save_to_database(self, offers: List[AggregatedOffer]) -> None:
        """Save offers to database."""
        saved, updated = self.repository.upsert_batch(offers)
        logger.info(f"Saved {saved} new, updated {updated} existing offers")

    def get_best_prices(
        self,
        city: str = None,
        offer_type: str = "hotel"
    ) -> List[AggregatedOffer]:
        """Get best price per source for comparison."""
        return self.repository.get_best_by_source(
            city=city,
            offer_type=offer_type
        )

    def get_price_history(
        self,
        offer_hash: str,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get price history for an offer."""
        # First find the offer
        offers = self.repository.search(limit=1)
        for offer in offers:
            if offer.offer_hash == offer_hash:
                history = self.repository.get_price_history(offer.id, days=days)
                return [
                    {
                        "price_idr": h.price_idr,
                        "price_sar": h.price_sar,
                        "recorded_at": h.recorded_at.isoformat(),
                        "source": h.source_name
                    }
                    for h in history
                ]
        return []

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "price_cache": self.price_cache.get_stats(),
            "source_cache": self.source_cache.get_all_stats()
        }

    def clear_cache(self) -> Dict[str, int]:
        """Clear all caches."""
        return {
            "price_cache_cleared": self.price_cache.invalidate_all(),
            "expired_cleaned": self.price_cache.cleanup_expired()
        }


# Singleton instance
_aggregator: Optional[PriceAggregator] = None


def get_price_aggregator() -> PriceAggregator:
    """Get singleton price aggregator."""
    global _aggregator
    if _aggregator is None:
        _aggregator = PriceAggregator()
    return _aggregator


def create_price_aggregator(
    data_manager=None,
    scraper_manager=None,
    **kwargs
) -> PriceAggregator:
    """Create a configured price aggregator."""
    aggregator = PriceAggregator(**kwargs)

    if data_manager:
        aggregator.set_data_manager(data_manager)

    if scraper_manager:
        aggregator.set_scraper_manager(scraper_manager)

    return aggregator
