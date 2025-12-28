"""
LABBAIK AI v7.5 - Price Aggregation Module
===========================================
Multi-source price aggregation system.

Data Sources:
- APIs: Amadeus, Xotelo, MakCorps
- Scrapers: Traveloka, Tiket.com, PegiPegi (future)
- Partners: REST API for travel agent partners

Usage:
    from services.price_aggregation import (
        get_price_aggregator,
        create_price_aggregator,
        AggregatedOffer,
        OfferType,
        SourceType
    )

    # Get singleton aggregator
    aggregator = get_price_aggregator()

    # Aggregate prices
    result = aggregator.aggregate(
        city="Makkah",
        offer_type="hotel",
        min_stars=4,
        sort_by="price"
    )

    for offer in result["offers"]:
        print(f"{offer.name}: Rp {offer.price_idr:,.0f}")
"""

# Models
from services.price_aggregation.models import (
    AggregatedOffer,
    PriceHistoryEntry,
    PartnerPriceFeed,
    ScrapingJob,
    PriceAlert,
    DataSourceStats,
    PriceTrend,
    SourceType,
    OfferType,
    AvailabilityStatus,
    TrendDirection,
    SAR_TO_IDR,
    convert_sar_to_idr,
    convert_idr_to_sar,
)

# Normalizer & Deduplicator
from services.price_aggregation.normalizer import (
    PriceNormalizer,
    OfferDeduplicator,
)

# Cache
from services.price_aggregation.cache_manager import (
    PriceCacheManager,
    SourceCacheManager,
    get_price_cache,
    get_source_cache,
)

# Repository
from services.price_aggregation.repository import (
    AggregatedPriceRepository,
    get_aggregated_price_repository,
)

# Aggregator
from services.price_aggregation.aggregator import (
    PriceAggregator,
    get_price_aggregator,
    create_price_aggregator,
)

# Scheduler
from services.price_aggregation.scheduler import (
    PriceAggregationScheduler,
    get_price_scheduler,
    start_price_scheduler,
    stop_price_scheduler,
)

__all__ = [
    # Models
    "AggregatedOffer",
    "PriceHistoryEntry",
    "PartnerPriceFeed",
    "ScrapingJob",
    "PriceAlert",
    "DataSourceStats",
    "PriceTrend",
    "SourceType",
    "OfferType",
    "AvailabilityStatus",
    "TrendDirection",
    "SAR_TO_IDR",
    "convert_sar_to_idr",
    "convert_idr_to_sar",
    # Normalizer
    "PriceNormalizer",
    "OfferDeduplicator",
    # Cache
    "PriceCacheManager",
    "SourceCacheManager",
    "get_price_cache",
    "get_source_cache",
    # Repository
    "AggregatedPriceRepository",
    "get_aggregated_price_repository",
    # Aggregator
    "PriceAggregator",
    "get_price_aggregator",
    "create_price_aggregator",
    # Scheduler
    "PriceAggregationScheduler",
    "get_price_scheduler",
    "start_price_scheduler",
    "stop_price_scheduler",
]
