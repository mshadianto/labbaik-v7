"""
LABBAIK AI v7.5 - Price Normalizer
===================================
Normalizes prices and offers from different sources.
"""

import re
import logging
from typing import Optional, Dict, Any
from datetime import datetime

from services.price_aggregation.models import (
    AggregatedOffer, SourceType, OfferType, AvailabilityStatus,
    SAR_TO_IDR, convert_sar_to_idr, convert_idr_to_sar
)

logger = logging.getLogger(__name__)


class PriceNormalizer:
    """
    Normalizes offers from different sources into a common format.
    Handles currency conversion, name normalization, and data cleaning.
    """

    # Hotel chain mappings for standardization
    HOTEL_CHAINS = {
        "hilton": "Hilton",
        "marriott": "Marriott",
        "sheraton": "Sheraton",
        "swissotel": "Swissôtel",
        "pullman": "Pullman",
        "sofitel": "Sofitel",
        "raffles": "Raffles",
        "fairmont": "Fairmont",
        "movenpick": "Mövenpick",
        "intercontinental": "InterContinental",
        "hyatt": "Hyatt",
        "conrad": "Conrad",
        "rotana": "Rotana",
    }

    # Arabic to Latin transliteration
    ARABIC_MAPPING = {
        "الهلتون": "hilton",
        "ماريوت": "marriott",
        "سويسوتيل": "swissotel",
        "بولمان": "pullman",
        "فندق": "hotel",
        "مكة": "makkah",
        "مكه": "makkah",
        "المدينة": "madinah",
        "المنورة": "madinah",
    }

    def normalize(self, offer: AggregatedOffer) -> AggregatedOffer:
        """
        Normalize an offer to standard format.
        Modifies the offer in place and returns it.
        """
        # Normalize name
        offer.name_normalized = self.normalize_name(offer.name)

        # Ensure both SAR and IDR prices
        self._normalize_prices(offer)

        # Normalize city names
        offer.city = self.normalize_city(offer.city)

        # Validate and clean stars
        if offer.stars:
            offer.stars = max(1, min(5, offer.stars))

        # Ensure availability status is set
        if not offer.availability_status:
            offer.availability_status = AvailabilityStatus.AVAILABLE if offer.is_available else AvailabilityStatus.SOLD_OUT

        # Compute offer hash if not set
        if not offer.offer_hash:
            offer.offer_hash = offer.compute_hash()

        # Set scraped timestamp
        if not offer.scraped_at:
            offer.scraped_at = datetime.now()

        return offer

    def normalize_name(self, name: str) -> str:
        """
        Normalize hotel/package name for comparison.
        - Lowercase
        - Remove extra whitespace
        - Transliterate Arabic
        - Remove common prefixes/suffixes
        """
        if not name:
            return ""

        normalized = name.strip()

        # Transliterate Arabic characters
        for arabic, latin in self.ARABIC_MAPPING.items():
            normalized = normalized.replace(arabic, latin)

        # Lowercase
        normalized = normalized.lower()

        # Remove extra whitespace
        normalized = " ".join(normalized.split())

        # Remove common prefixes
        prefixes_to_remove = ["hotel ", "فندق ", "the ", "al "]
        for prefix in prefixes_to_remove:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):]

        # Remove common suffixes
        suffixes_to_remove = [" hotel", " makkah", " mecca", " madinah", " medina"]
        for suffix in suffixes_to_remove:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)]

        # Clean special characters but keep spaces and basic punctuation
        normalized = re.sub(r'[^\w\s\-&]', '', normalized)

        return normalized.strip()

    def normalize_city(self, city: str) -> str:
        """Normalize city name to standard format."""
        if not city:
            return ""

        city_lower = city.lower().strip()

        # Makkah variations
        if city_lower in ["makkah", "mecca", "makka", "mekka", "مكة", "مكه"]:
            return "Makkah"

        # Madinah variations
        if city_lower in ["madinah", "medina", "madina", "المدينة", "المنورة"]:
            return "Madinah"

        # Jeddah variations
        if city_lower in ["jeddah", "jedda", "jidda", "جدة"]:
            return "Jeddah"

        return city.title()

    def _normalize_prices(self, offer: AggregatedOffer) -> None:
        """Ensure both SAR and IDR prices are set."""
        if offer.price_idr and not offer.price_sar:
            offer.price_sar = convert_idr_to_sar(offer.price_idr)
        elif offer.price_sar and not offer.price_idr:
            offer.price_idr = convert_sar_to_idr(offer.price_sar)

        # Normalize per-night prices
        if offer.price_per_night_idr and not offer.price_per_night_sar:
            offer.price_per_night_sar = convert_idr_to_sar(offer.price_per_night_idr)
        elif offer.price_per_night_sar and not offer.price_per_night_idr:
            offer.price_per_night_idr = convert_sar_to_idr(offer.price_per_night_sar)

    def normalize_from_api(
        self,
        raw_data: Dict[str, Any],
        source_name: str
    ) -> Optional[AggregatedOffer]:
        """
        Normalize raw API response to AggregatedOffer.
        Source-specific parsing logic.
        """
        try:
            if source_name == "amadeus":
                return self._normalize_amadeus(raw_data)
            elif source_name == "xotelo":
                return self._normalize_xotelo(raw_data)
            elif source_name == "makcorps":
                return self._normalize_makcorps(raw_data)
            else:
                logger.warning(f"Unknown source: {source_name}")
                return None
        except Exception as e:
            logger.error(f"Failed to normalize from {source_name}: {e}")
            return None

    def _normalize_amadeus(self, data: Dict) -> Optional[AggregatedOffer]:
        """Normalize Amadeus API response."""
        hotel = data.get("hotel", {})
        offer_data = data.get("offers", [{}])[0] if data.get("offers") else {}

        price_info = offer_data.get("price", {})
        total = float(price_info.get("total", 0))
        currency = price_info.get("currency", "SAR")

        # Convert to SAR if needed
        if currency == "USD":
            price_sar = total * 3.75
        elif currency == "EUR":
            price_sar = total * 4.10
        else:
            price_sar = total

        return AggregatedOffer(
            source_type=SourceType.API,
            source_name="amadeus",
            source_offer_id=hotel.get("hotelId"),
            offer_type=OfferType.HOTEL,
            name=hotel.get("name", ""),
            city=self.normalize_city(hotel.get("cityCode", "")),
            stars=self._estimate_stars_from_rating(hotel.get("rating")),
            price_sar=price_sar,
            price_idr=convert_sar_to_idr(price_sar),
            currency_original=currency,
            raw_data=data
        )

    def _normalize_xotelo(self, data: Dict) -> Optional[AggregatedOffer]:
        """Normalize Xotelo API response."""
        return AggregatedOffer(
            source_type=SourceType.API,
            source_name="xotelo",
            source_offer_id=data.get("id"),
            offer_type=OfferType.HOTEL,
            name=data.get("name", ""),
            city=self.normalize_city(data.get("city", "")),
            stars=int(data.get("stars", 3)),
            price_sar=float(data.get("price", 0)),
            distance_to_haram_m=int(float(data.get("distance", 0)) * 1000),
            raw_data=data
        )

    def _normalize_makcorps(self, data: Dict) -> Optional[AggregatedOffer]:
        """Normalize MakCorps API response."""
        return AggregatedOffer(
            source_type=SourceType.API,
            source_name="makcorps",
            source_offer_id=data.get("hotel_id"),
            offer_type=OfferType.HOTEL,
            name=data.get("hotel_name", ""),
            city=self.normalize_city(data.get("city", "")),
            stars=int(data.get("star_rating", 3)),
            price_sar=float(data.get("price_sar", 0)),
            raw_data=data
        )

    def _estimate_stars_from_rating(self, rating: Any) -> int:
        """Estimate hotel stars from rating string/number."""
        if not rating:
            return 3

        if isinstance(rating, (int, float)):
            return min(5, max(1, int(rating)))

        rating_str = str(rating).lower()

        if "luxury" in rating_str or "5" in rating_str:
            return 5
        elif "superior" in rating_str or "4" in rating_str:
            return 4
        elif "standard" in rating_str or "3" in rating_str:
            return 3
        elif "economy" in rating_str or "budget" in rating_str or "2" in rating_str:
            return 2

        return 3


class OfferDeduplicator:
    """
    Deduplicates similar offers from different sources.
    Uses name similarity and location matching.
    """

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        self.normalizer = PriceNormalizer()

    def deduplicate(
        self,
        offers: list[AggregatedOffer],
        keep_all_sources: bool = True
    ) -> list[AggregatedOffer]:
        """
        Remove duplicate offers.

        Args:
            offers: List of offers to deduplicate
            keep_all_sources: If True, keep one offer per source for same hotel

        Returns:
            Deduplicated list of offers
        """
        if not offers:
            return []

        # Group by normalized name + city
        groups: Dict[str, list[AggregatedOffer]] = {}

        for offer in offers:
            key = f"{offer.name_normalized}|{offer.city}"

            if key not in groups:
                groups[key] = []
            groups[key].append(offer)

        result = []

        for key, group in groups.items():
            if keep_all_sources:
                # Keep best offer from each source
                by_source: Dict[str, AggregatedOffer] = {}
                for offer in group:
                    source = offer.source_name
                    if source not in by_source or offer.price_idr < by_source[source].price_idr:
                        by_source[source] = offer
                result.extend(by_source.values())
            else:
                # Keep only the cheapest overall
                cheapest = min(group, key=lambda x: x.price_idr or float('inf'))
                result.append(cheapest)

        return result

    def find_similar(
        self,
        offer: AggregatedOffer,
        candidates: list[AggregatedOffer]
    ) -> list[AggregatedOffer]:
        """Find similar offers to a given offer."""
        similar = []

        for candidate in candidates:
            if candidate.city != offer.city:
                continue

            similarity = self._calculate_similarity(offer, candidate)
            if similarity >= self.similarity_threshold:
                similar.append(candidate)

        return similar

    def _calculate_similarity(
        self,
        offer1: AggregatedOffer,
        offer2: AggregatedOffer
    ) -> float:
        """Calculate similarity score between two offers (0-1)."""
        # Name similarity (60% weight)
        name_sim = self._string_similarity(
            offer1.name_normalized,
            offer2.name_normalized
        )

        # Stars match (20% weight)
        stars_sim = 1.0 if offer1.stars == offer2.stars else 0.5

        # Price similarity (20% weight) - within 20% is similar
        price_diff = abs(offer1.price_idr - offer2.price_idr)
        max_price = max(offer1.price_idr, offer2.price_idr, 1)
        price_sim = max(0, 1 - (price_diff / max_price / 0.2))

        return (name_sim * 0.6) + (stars_sim * 0.2) + (price_sim * 0.2)

    def _string_similarity(self, s1: str, s2: str) -> float:
        """Calculate string similarity using simple ratio."""
        if not s1 or not s2:
            return 0.0

        if s1 == s2:
            return 1.0

        # Simple word overlap
        words1 = set(s1.split())
        words2 = set(s2.split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)
