"""
LABBAIK AI - Intelligence Services V1.2
=======================================
Name normalization, pricing, risk scoring, peak season,
amenity extraction, geo clustering, and itinerary building.
"""

# V1.1 - Core Intelligence
from .name_norm import (
    normalize_name,
    alt_forms,
    match_hotel_name,
    similarity_score,
    normalize_city,
    identify_hotel_chain,
)
from .pricing import (
    to_sar,
    to_idr,
    get_fx_rate,
    format_price,
    format_price_dual,
    format_price_range,
    compare_prices,
    get_pricing_service,
)
from .risk_score import (
    compute_risk_score,
    get_risk_level,
    format_risk_badge,
    format_risk_color,
    RiskLevel,
    RiskScore,
    get_risk_calculator,
)

# V1.2 - Peak Season Calendar
from .season_calendar import (
    season_weight,
    is_peak_season,
    get_booking_recommendation,
    get_season_calendar,
    SeasonType,
    SeasonPeriod,
)

# V1.2 - Amenity Intelligence
from .amenities import (
    extract_signals,
    signals_to_dict,
    get_highlight_amenities,
    filter_hotels_by_amenity,
    rank_hotels_by_amenities,
    AmenitySignals,
)

# V1.2 - Geo Clustering & Dedup
from .geo_cluster import (
    haversine_distance,
    find_clusters,
    merge_hotel_data,
    deduplicate_hotels,
    is_duplicate_candidate,
    HotelCluster,
)

# V1.2 - Itinerary Builder
from .itinerary import (
    build_itinerary,
    compare_transport,
    itinerary_to_dict,
    get_itinerary_builder,
    TransportMode,
    Itinerary,
)

__all__ = [
    # V1.1 - Name Normalization
    "normalize_name",
    "alt_forms",
    "match_hotel_name",
    "similarity_score",
    "normalize_city",
    "identify_hotel_chain",

    # V1.1 - Pricing
    "to_sar",
    "to_idr",
    "get_fx_rate",
    "format_price",
    "format_price_dual",
    "format_price_range",
    "compare_prices",
    "get_pricing_service",

    # V1.1 - Risk Score
    "compute_risk_score",
    "get_risk_level",
    "format_risk_badge",
    "format_risk_color",
    "RiskLevel",
    "RiskScore",
    "get_risk_calculator",

    # V1.2 - Peak Season
    "season_weight",
    "is_peak_season",
    "get_booking_recommendation",
    "get_season_calendar",
    "SeasonType",
    "SeasonPeriod",

    # V1.2 - Amenities
    "extract_signals",
    "signals_to_dict",
    "get_highlight_amenities",
    "filter_hotels_by_amenity",
    "rank_hotels_by_amenities",
    "AmenitySignals",

    # V1.2 - Geo Clustering
    "haversine_distance",
    "find_clusters",
    "merge_hotel_data",
    "deduplicate_hotels",
    "is_duplicate_candidate",
    "HotelCluster",

    # V1.2 - Itinerary
    "build_itinerary",
    "compare_transport",
    "itinerary_to_dict",
    "get_itinerary_builder",
    "TransportMode",
    "Itinerary",
]

__version__ = "1.2.0"
