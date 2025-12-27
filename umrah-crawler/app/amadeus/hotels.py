"""
Amadeus Hotel Search
=====================
Search hotels in Makkah & Madinah with distance scoring.
"""

import logging
from typing import List, Dict, Any, Optional

from app.amadeus.client import AmadeusClient
from app.umrah.geo import CITY_GEO, umrah_distance_score

logger = logging.getLogger(__name__)


async def hotel_search_by_city(
    client: AmadeusClient,
    city: str,
    checkin: str,
    checkout: str,
    adults: int = 2,
    radius_km: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search hotels by city using geocode search.

    Args:
        client: AmadeusClient instance
        city: MAKKAH or MADINAH
        checkin: Check-in date (YYYY-MM-DD)
        checkout: Check-out date (YYYY-MM-DD)
        adults: Number of adults
        radius_km: Search radius in kilometers

    Returns:
        List of hotel dicts sorted by distance + price
    """
    city_upper = city.upper()
    geo = CITY_GEO.get(city_upper)

    if not geo:
        raise ValueError(f"Unknown city: {city}. Use MAKKAH or MADINAH.")

    params = {
        "latitude": geo["lat"],
        "longitude": geo["lon"],
        "radius": radius_km,
        "radiusUnit": "KM",
        "checkInDate": checkin,
        "checkOutDate": checkout,
        "adults": adults,
    }

    # Hotel offers by geocode
    # Note: endpoint may vary (/v2 or /v3 depending on Amadeus environment)
    try:
        data = await client.request("GET", "/v3/shopping/hotel-offers", params=params)
    except Exception as e:
        logger.warning(f"v3 failed, trying v2: {e}")
        data = await client.request("GET", "/v2/shopping/hotel-offers", params=params)

    hotels = []

    for item in data.get("data", []):
        hotel = item.get("hotel", {})
        offers = item.get("offers", []) or []

        lat = hotel.get("latitude")
        lon = hotel.get("longitude")

        # Find best price from all offers
        best_price: Optional[float] = None
        best_currency: Optional[str] = None
        refundable_hint = False

        for off in offers:
            price_info = off.get("price") or {}
            price_str = price_info.get("total")
            currency = price_info.get("currency")

            if price_str is not None:
                try:
                    p = float(price_str)
                    if best_price is None or p < best_price:
                        best_price = p
                        best_currency = currency
                except (ValueError, TypeError):
                    pass

            # Check cancellation policy
            policies = off.get("policies") or {}
            if policies.get("cancellation"):
                refundable_hint = True

        # Calculate distance score
        dist = None
        if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
            dist = umrah_distance_score(city_upper, float(lat), float(lon))

        hotels.append({
            "city": city_upper,
            "hotel_id": hotel.get("hotelId"),
            "name": hotel.get("name"),
            "lat": lat,
            "lon": lon,
            "best_price_total": best_price,
            "currency": best_currency,
            "has_cancellation_policy_hint": refundable_hint,
            "distance": dist,
            "raw_offers_count": len(offers),
        })

    # Sort by distance (nearest first), then by price
    def rank_key(h):
        d = (h.get("distance") or {}).get("distance_m", 10**9)
        p = h.get("best_price_total") if h.get("best_price_total") is not None else 10**9
        return (d, p)

    hotels.sort(key=rank_key)

    logger.info(f"Amadeus hotel search: {city_upper} found {len(hotels)} hotels")
    return hotels
