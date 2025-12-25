"""
LABBAIK AI v6.0 - Cost Integration Layer
=========================================
Bridges the hybrid data fetcher with the cost calculator/simulator.
Provides live hotel pricing when available, falls back to static rates.
"""

import logging
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from services.umrah.data_fetcher import (
    HybridUmrahDataManager,
    HotelOffer,
    TransportOption,
    SAR_TO_IDR,
)

logger = logging.getLogger(__name__)


@dataclass
class LivePriceResult:
    """Result from live price lookup"""
    price_per_night_idr: float
    price_per_night_sar: float
    hotel_name: str
    hotel_stars: int
    distance_to_haram_km: float
    walking_time_minutes: int
    source: str
    is_live_data: bool = True


class CostIntegrationService:
    """
    Integration service that provides live pricing for cost calculations.

    Usage:
        service = CostIntegrationService()

        # Get live hotel price
        price = service.get_hotel_price(
            city="Makkah",
            star_rating=4,
            check_in="2025-03-01",
            check_out="2025-03-06"
        )

        # Get transport price
        transport = service.get_transport_price("Makkah", "Madinah")
    """

    # Static fallback prices (IDR per night) - same as existing simulator
    STATIC_HOTEL_PRICES = {
        "makkah": {
            2: 400_000,
            3: 700_000,
            4: 1_500_000,
            5: 3_500_000,
        },
        "madinah": {
            2: 350_000,
            3: 600_000,
            4: 1_200_000,
            5: 2_800_000,
        }
    }

    # Static transport prices (IDR)
    STATIC_TRANSPORT_PRICES = {
        "train": 420_000,  # ~100 SAR
        "bus": 210_000,    # ~50 SAR
        "private_car": 840_000,  # ~200 SAR
    }

    def __init__(self, data_manager: HybridUmrahDataManager = None):
        """
        Initialize with optional data manager.
        If not provided, will create one on first use.
        """
        self._data_manager = data_manager
        self._hotel_cache: Dict[str, List[HotelOffer]] = {}
        self._cache_timestamp: Dict[str, datetime] = {}
        self._cache_duration = timedelta(hours=1)  # In-memory cache

    @property
    def data_manager(self) -> HybridUmrahDataManager:
        """Lazy initialization of data manager"""
        if self._data_manager is None:
            from services.umrah import get_umrah_data_manager
            self._data_manager = get_umrah_data_manager()
        return self._data_manager

    def get_hotel_price(
        self,
        city: str,
        star_rating: int,
        check_in: str = None,
        check_out: str = None,
        prefer_close_to_haram: bool = True
    ) -> LivePriceResult:
        """
        Get hotel price for given city and star rating.

        Args:
            city: "Makkah" or "Madinah"
            star_rating: 2-5 stars
            check_in: Check-in date (YYYY-MM-DD)
            check_out: Check-out date (YYYY-MM-DD)
            prefer_close_to_haram: If True, prefer hotels closer to Haram

        Returns:
            LivePriceResult with pricing information
        """
        city_lower = city.lower()

        # Try to get live data
        try:
            hotels = self._get_cached_hotels(city, check_in, check_out)

            # Filter by star rating
            matching_hotels = [h for h in hotels if h.stars == star_rating]

            if not matching_hotels:
                # Try adjacent star ratings
                matching_hotels = [h for h in hotels if abs(h.stars - star_rating) <= 1]

            if matching_hotels:
                # Sort by distance if preferred
                if prefer_close_to_haram:
                    matching_hotels.sort(key=lambda x: x.distance_to_haram_km)

                best_hotel = matching_hotels[0]

                return LivePriceResult(
                    price_per_night_idr=best_hotel.price_per_night_idr,
                    price_per_night_sar=best_hotel.price_per_night_sar,
                    hotel_name=best_hotel.hotel_name,
                    hotel_stars=best_hotel.stars,
                    distance_to_haram_km=best_hotel.distance_to_haram_km,
                    walking_time_minutes=best_hotel.walking_time_minutes,
                    source=best_hotel.source,
                    is_live_data=best_hotel.source != "demo_fallback"
                )

        except Exception as e:
            logger.warning(f"Failed to get live hotel price: {e}")

        # Fallback to static prices
        static_price = self.STATIC_HOTEL_PRICES.get(city_lower, {}).get(
            star_rating, 1_000_000
        )

        return LivePriceResult(
            price_per_night_idr=static_price,
            price_per_night_sar=static_price / SAR_TO_IDR,
            hotel_name=f"Hotel Bintang {star_rating}",
            hotel_stars=star_rating,
            distance_to_haram_km=0.5,
            walking_time_minutes=8,
            source="static_fallback",
            is_live_data=False
        )

    def _get_cached_hotels(
        self,
        city: str,
        check_in: str = None,
        check_out: str = None
    ) -> List[HotelOffer]:
        """Get hotels from cache or fetch fresh data"""
        cache_key = f"{city}:{check_in}:{check_out}"

        # Check cache
        if cache_key in self._hotel_cache:
            cached_at = self._cache_timestamp.get(cache_key)
            if cached_at and datetime.now() - cached_at < self._cache_duration:
                return self._hotel_cache[cache_key]

        # Fetch fresh data
        hotels = self.data_manager.search_hotels(
            city=city,
            check_in=check_in,
            check_out=check_out,
            max_results=30
        )

        # Cache results
        self._hotel_cache[cache_key] = hotels
        self._cache_timestamp[cache_key] = datetime.now()

        return hotels

    def get_transport_price(
        self,
        from_city: str,
        to_city: str,
        transport_type: str = "train"
    ) -> Dict[str, Any]:
        """
        Get transport price between cities.

        Args:
            from_city: Origin city
            to_city: Destination city
            transport_type: "train", "bus", or "private_car"

        Returns:
            Dict with price_idr, price_sar, duration_hours, operator
        """
        try:
            options = self.data_manager.get_transport_options(from_city, to_city)

            # Find matching transport type
            for option in options:
                if option.type == transport_type:
                    return {
                        "price_idr": option.price_idr,
                        "price_sar": option.price_sar,
                        "duration_hours": option.duration_hours,
                        "operator": option.operator,
                        "schedule": option.schedule,
                        "source": option.source,
                        "is_live_data": True
                    }

            # Return first available if no match
            if options:
                option = options[0]
                return {
                    "price_idr": option.price_idr,
                    "price_sar": option.price_sar,
                    "duration_hours": option.duration_hours,
                    "operator": option.operator,
                    "schedule": option.schedule,
                    "source": option.source,
                    "is_live_data": True
                }

        except Exception as e:
            logger.warning(f"Failed to get live transport price: {e}")

        # Fallback to static prices
        static_price = self.STATIC_TRANSPORT_PRICES.get(transport_type, 420_000)

        return {
            "price_idr": static_price,
            "price_sar": static_price / SAR_TO_IDR,
            "duration_hours": 2.5 if transport_type == "train" else 5.0,
            "operator": transport_type.replace("_", " ").title(),
            "schedule": [],
            "source": "static_fallback",
            "is_live_data": False
        }

    def calculate_live_cost(
        self,
        departure_date: date,
        nights_makkah: int,
        nights_madinah: int,
        hotel_star_makkah: int,
        hotel_star_madinah: int,
        num_travelers: int = 1,
        include_transport: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate total cost using live data where available.

        Returns comprehensive breakdown with data source indicators.
        """
        check_in = departure_date.strftime("%Y-%m-%d")
        check_out = (departure_date + timedelta(days=nights_makkah + nights_madinah)).strftime("%Y-%m-%d")

        # Get hotel prices
        makkah_price = self.get_hotel_price(
            "Makkah", hotel_star_makkah, check_in, check_out
        )
        madinah_price = self.get_hotel_price(
            "Madinah", hotel_star_madinah, check_in, check_out
        )

        # Calculate hotel costs
        hotel_makkah_total = makkah_price.price_per_night_idr * nights_makkah
        hotel_madinah_total = madinah_price.price_per_night_idr * nights_madinah

        # Get transport price
        transport_info = self.get_transport_price("Makkah", "Madinah", "train") if include_transport else None
        transport_cost = transport_info["price_idr"] if transport_info else 0

        # Build result
        return {
            "hotels": {
                "makkah": {
                    "hotel_name": makkah_price.hotel_name,
                    "stars": makkah_price.hotel_stars,
                    "price_per_night_idr": makkah_price.price_per_night_idr,
                    "total_idr": hotel_makkah_total,
                    "nights": nights_makkah,
                    "distance_km": makkah_price.distance_to_haram_km,
                    "walking_min": makkah_price.walking_time_minutes,
                    "source": makkah_price.source,
                    "is_live": makkah_price.is_live_data
                },
                "madinah": {
                    "hotel_name": madinah_price.hotel_name,
                    "stars": madinah_price.hotel_stars,
                    "price_per_night_idr": madinah_price.price_per_night_idr,
                    "total_idr": hotel_madinah_total,
                    "nights": nights_madinah,
                    "distance_km": madinah_price.distance_to_haram_km,
                    "walking_min": madinah_price.walking_time_minutes,
                    "source": madinah_price.source,
                    "is_live": madinah_price.is_live_data
                }
            },
            "transport": transport_info,
            "totals": {
                "hotel_total_idr": hotel_makkah_total + hotel_madinah_total,
                "transport_idr": transport_cost,
                "accommodation_per_person_idr": (hotel_makkah_total + hotel_madinah_total) / num_travelers,
            },
            "data_quality": {
                "makkah_live": makkah_price.is_live_data,
                "madinah_live": madinah_price.is_live_data,
                "transport_live": transport_info.get("is_live_data", False) if transport_info else False,
            },
            "generated_at": datetime.now().isoformat()
        }

    def get_hotels_by_city(
        self,
        city: str,
        check_in: str = None,
        check_out: str = None,
        max_results: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get list of hotels for display in UI.

        Returns list of hotel dictionaries sorted by distance.
        """
        hotels = self._get_cached_hotels(city, check_in, check_out)

        return [h.to_dict() for h in hotels[:max_results]]


# Singleton instance
_cost_integration_service: Optional[CostIntegrationService] = None


def get_cost_integration_service() -> CostIntegrationService:
    """Get singleton instance of CostIntegrationService"""
    global _cost_integration_service

    if _cost_integration_service is None:
        _cost_integration_service = CostIntegrationService()

    return _cost_integration_service
