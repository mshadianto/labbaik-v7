"""
LABBAIK AI v7.5 - Price Aggregation Models
============================================
Data models for aggregated prices from multiple sources.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Optional, Any
from enum import Enum
import hashlib
import json


class SourceType(str, Enum):
    """Price data source types."""
    API = "api"
    SCRAPER = "scraper"
    PARTNER = "partner"
    DEMO = "demo"
    CACHE = "cache"


class OfferType(str, Enum):
    """Offer types."""
    HOTEL = "hotel"
    PACKAGE = "package"
    FLIGHT = "flight"


class AvailabilityStatus(str, Enum):
    """Availability status."""
    AVAILABLE = "available"
    LIMITED = "limited"
    LAST_ROOMS = "last_rooms"
    SOLD_OUT = "sold_out"
    UNKNOWN = "unknown"


class TrendDirection(str, Enum):
    """Price trend direction."""
    UP = "up"
    DOWN = "down"
    STABLE = "stable"


@dataclass
class PriceTrend:
    """Price trend information."""
    direction: TrendDirection
    change_percent: float
    change_amount_idr: float
    previous_price_idr: float
    recorded_at: datetime


@dataclass
class AggregatedOffer:
    """
    Normalized offer from any source.
    This is the main model for aggregated prices.
    """
    # Identification
    id: Optional[str] = None
    offer_hash: str = ""
    source_type: SourceType = SourceType.DEMO
    source_name: str = "unknown"
    source_offer_id: Optional[str] = None

    # Offer Details
    offer_type: OfferType = OfferType.HOTEL
    name: str = ""
    name_normalized: str = ""
    city: str = ""

    # Hotel-specific
    stars: Optional[int] = None
    distance_to_haram_m: Optional[int] = None
    walking_time_minutes: Optional[int] = None
    amenities: List[str] = field(default_factory=list)

    # Package-specific
    duration_days: Optional[int] = None
    departure_city: Optional[str] = None
    airline: Optional[str] = None
    hotel_makkah: Optional[str] = None
    hotel_makkah_stars: Optional[int] = None
    hotel_madinah: Optional[str] = None
    hotel_madinah_stars: Optional[int] = None
    inclusions: List[str] = field(default_factory=list)

    # Pricing
    price_sar: float = 0.0
    price_idr: float = 0.0
    price_per_night_sar: Optional[float] = None
    price_per_night_idr: Optional[float] = None
    currency_original: str = "IDR"

    # Validity
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None

    # Availability
    is_available: bool = True
    availability_status: AvailabilityStatus = AvailabilityStatus.AVAILABLE
    rooms_left: Optional[int] = None
    quota: Optional[int] = None

    # Metadata
    source_url: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None
    confidence_score: float = 1.0

    # Timestamps
    scraped_at: datetime = field(default_factory=datetime.now)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Computed (not stored)
    price_trend: Optional[PriceTrend] = None
    rank: Optional[int] = None

    def __post_init__(self):
        """Generate offer hash if not provided."""
        if not self.offer_hash:
            self.offer_hash = self.compute_hash()

        if not self.name_normalized and self.name:
            self.name_normalized = self._normalize_name(self.name)

    def compute_hash(self) -> str:
        """Compute unique hash for this offer."""
        key_parts = [
            self.source_name,
            self.offer_type.value if isinstance(self.offer_type, OfferType) else self.offer_type,
            self.name_normalized or self._normalize_name(self.name),
            self.city,
            str(self.stars or ""),
            str(self.duration_days or ""),
        ]
        key_string = "|".join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()[:32]

    def _normalize_name(self, name: str) -> str:
        """Normalize name for comparison."""
        if not name:
            return ""
        # Lowercase, remove extra spaces
        normalized = " ".join(name.lower().split())
        # Remove common prefixes/suffixes
        for word in ["hotel", "hotel &", "&"]:
            normalized = normalized.replace(word, "").strip()
        return normalized

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage."""
        return {
            "offer_hash": self.offer_hash,
            "source_type": self.source_type.value if isinstance(self.source_type, SourceType) else self.source_type,
            "source_name": self.source_name,
            "source_offer_id": self.source_offer_id,
            "offer_type": self.offer_type.value if isinstance(self.offer_type, OfferType) else self.offer_type,
            "name": self.name,
            "name_normalized": self.name_normalized,
            "city": self.city,
            "stars": self.stars,
            "distance_to_haram_m": self.distance_to_haram_m,
            "walking_time_minutes": self.walking_time_minutes,
            "amenities": json.dumps(self.amenities) if self.amenities else None,
            "duration_days": self.duration_days,
            "departure_city": self.departure_city,
            "airline": self.airline,
            "hotel_makkah": self.hotel_makkah,
            "hotel_makkah_stars": self.hotel_makkah_stars,
            "hotel_madinah": self.hotel_madinah,
            "hotel_madinah_stars": self.hotel_madinah_stars,
            "inclusions": json.dumps(self.inclusions) if self.inclusions else None,
            "price_sar": self.price_sar,
            "price_idr": self.price_idr,
            "price_per_night_sar": self.price_per_night_sar,
            "price_per_night_idr": self.price_per_night_idr,
            "currency_original": self.currency_original,
            "check_in_date": self.check_in_date,
            "check_out_date": self.check_out_date,
            "valid_from": self.valid_from,
            "valid_until": self.valid_until,
            "is_available": self.is_available,
            "availability_status": self.availability_status.value if isinstance(self.availability_status, AvailabilityStatus) else self.availability_status,
            "rooms_left": self.rooms_left,
            "quota": self.quota,
            "source_url": self.source_url,
            "raw_data": json.dumps(self.raw_data) if self.raw_data else None,
            "confidence_score": self.confidence_score,
            "scraped_at": self.scraped_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AggregatedOffer":
        """Create from dictionary (database row)."""
        # Parse JSON fields
        amenities = data.get("amenities")
        if isinstance(amenities, str):
            amenities = json.loads(amenities)

        inclusions = data.get("inclusions")
        if isinstance(inclusions, str):
            inclusions = json.loads(inclusions)

        raw_data = data.get("raw_data")
        if isinstance(raw_data, str):
            raw_data = json.loads(raw_data)

        return cls(
            id=str(data.get("id")) if data.get("id") else None,
            offer_hash=data.get("offer_hash", ""),
            source_type=SourceType(data.get("source_type", "demo")),
            source_name=data.get("source_name", "unknown"),
            source_offer_id=data.get("source_offer_id"),
            offer_type=OfferType(data.get("offer_type", "hotel")),
            name=data.get("name", ""),
            name_normalized=data.get("name_normalized", ""),
            city=data.get("city", ""),
            stars=data.get("stars"),
            distance_to_haram_m=data.get("distance_to_haram_m"),
            walking_time_minutes=data.get("walking_time_minutes"),
            amenities=amenities or [],
            duration_days=data.get("duration_days"),
            departure_city=data.get("departure_city"),
            airline=data.get("airline"),
            hotel_makkah=data.get("hotel_makkah"),
            hotel_makkah_stars=data.get("hotel_makkah_stars"),
            hotel_madinah=data.get("hotel_madinah"),
            hotel_madinah_stars=data.get("hotel_madinah_stars"),
            inclusions=inclusions or [],
            price_sar=float(data.get("price_sar") or 0),
            price_idr=float(data.get("price_idr") or 0),
            price_per_night_sar=float(data.get("price_per_night_sar")) if data.get("price_per_night_sar") else None,
            price_per_night_idr=float(data.get("price_per_night_idr")) if data.get("price_per_night_idr") else None,
            currency_original=data.get("currency_original", "IDR"),
            check_in_date=data.get("check_in_date"),
            check_out_date=data.get("check_out_date"),
            valid_from=data.get("valid_from"),
            valid_until=data.get("valid_until"),
            is_available=data.get("is_available", True),
            availability_status=AvailabilityStatus(data.get("availability_status", "available")),
            rooms_left=data.get("rooms_left"),
            quota=data.get("quota"),
            source_url=data.get("source_url"),
            raw_data=raw_data,
            confidence_score=float(data.get("confidence_score") or 1.0),
            scraped_at=data.get("scraped_at") or datetime.now(),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


@dataclass
class PriceHistoryEntry:
    """Single price history entry."""
    id: Optional[str] = None
    aggregated_price_id: str = ""
    price_sar: float = 0.0
    price_idr: float = 0.0
    availability_status: str = "available"
    rooms_left: Optional[int] = None
    source_name: str = ""
    price_change_sar: Optional[float] = None
    price_change_percent: Optional[float] = None
    recorded_at: datetime = field(default_factory=datetime.now)


@dataclass
class PartnerPriceFeed:
    """Partner-submitted price feed."""
    id: Optional[str] = None
    partner_id: str = ""

    # Feed details
    feed_name: str = ""
    feed_type: str = "package"

    # Pricing
    price_idr: float = 0.0
    price_sar: Optional[float] = None
    price_per_person_idr: Optional[float] = None

    # Package details
    package_name: str = ""
    description: Optional[str] = None
    hotel_makkah: Optional[str] = None
    hotel_makkah_stars: Optional[int] = None
    hotel_madinah: Optional[str] = None
    hotel_madinah_stars: Optional[int] = None
    duration_days: Optional[int] = None
    departure_city: Optional[str] = None
    departure_dates: List[str] = field(default_factory=list)
    airline: Optional[str] = None
    flight_class: str = "economy"
    room_type: str = "quad"
    inclusions: List[str] = field(default_factory=list)
    exclusions: List[str] = field(default_factory=list)

    # Availability
    quota: int = 0
    booked: int = 0
    is_available: bool = True

    # Validity
    valid_from: Optional[date] = None
    valid_until: Optional[date] = None

    # Business
    commission_rate: float = 10.0
    markup_percent: Optional[float] = None

    # Approval
    status: str = "pending"
    submitted_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    rejection_reason: Optional[str] = None


@dataclass
class ScrapingJob:
    """Background scraping job."""
    id: Optional[str] = None
    job_type: str = ""
    job_name: Optional[str] = None
    status: str = "pending"
    priority: int = 0

    # Config
    config: Optional[Dict[str, Any]] = None
    target_sources: Optional[List[str]] = None

    # Results
    items_found: int = 0
    items_saved: int = 0
    items_updated: int = 0
    items_failed: int = 0
    errors: Optional[List[str]] = None
    result_summary: Optional[Dict[str, Any]] = None

    # Timing
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None

    triggered_by: str = "scheduler"


@dataclass
class PriceAlert:
    """User price alert subscription."""
    id: Optional[str] = None
    user_id: Optional[str] = None
    alert_name: Optional[str] = None

    # Criteria
    offer_type: str = "package"
    city: Optional[str] = None
    target_price_idr: Optional[float] = None
    max_price_idr: Optional[float] = None
    hotel_stars_min: Optional[int] = None
    hotel_stars_max: Optional[int] = None
    departure_city: Optional[str] = None
    check_in_from: Optional[date] = None
    check_in_to: Optional[date] = None
    duration_days_min: Optional[int] = None
    duration_days_max: Optional[int] = None

    # Notifications
    notify_email: bool = True
    notify_whatsapp: bool = False
    notify_push: bool = False

    # Triggers
    trigger_on_price_drop: bool = True
    trigger_on_new_offer: bool = False
    min_price_drop_percent: float = 5.0

    # Status
    is_active: bool = True
    last_triggered_at: Optional[datetime] = None
    trigger_count: int = 0


@dataclass
class DataSourceStats:
    """Data source health statistics."""
    source_name: str = ""
    source_type: str = ""

    # Stats
    total_offers: int = 0
    active_offers: int = 0
    avg_price_idr: Optional[float] = None
    min_price_idr: Optional[float] = None
    max_price_idr: Optional[float] = None

    # Health
    last_successful_fetch: Optional[datetime] = None
    last_failed_fetch: Optional[datetime] = None
    consecutive_failures: int = 0
    success_rate: Optional[float] = None
    avg_response_time_ms: Optional[int] = None

    # Quota
    daily_quota: Optional[int] = None
    daily_used: int = 0
    quota_reset_at: Optional[datetime] = None

    recorded_at: datetime = field(default_factory=datetime.now)


# SAR to IDR conversion rate
SAR_TO_IDR = 4250.0


def convert_sar_to_idr(amount_sar: float) -> float:
    """Convert SAR to IDR."""
    return round(amount_sar * SAR_TO_IDR)


def convert_idr_to_sar(amount_idr: float) -> float:
    """Convert IDR to SAR."""
    return round(amount_idr / SAR_TO_IDR, 2)
