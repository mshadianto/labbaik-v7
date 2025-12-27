"""
Amadeus Hotel Search
=====================
Search hotels in Makkah & Madinah with distance scoring.

Amadeus Hotel API Flow:
1. GET /v1/reference-data/locations/hotels/by-geocode - Get hotel IDs
2. GET /v3/shopping/hotel-offers - Get offers by hotel IDs
"""

import logging
from typing import List, Dict, Any, Optional

from app.amadeus.client import AmadeusClient
from app.umrah.geo import CITY_GEO, umrah_distance_score

logger = logging.getLogger(__name__)


async def get_hotels_by_geocode(
    client: AmadeusClient,
    latitude: float,
    longitude: float,
    radius_km: int = 5,
) -> List[Dict[str, Any]]:
    """
    Step 1: Get hotel list by geocode.

    Returns list of hotels with hotelId, name, geoCode.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius_km,
        "radiusUnit": "KM",
    }

    data = await client.request("GET", "/v1/reference-data/locations/hotels/by-geocode", params=params)
    return data.get("data", [])


async def get_hotel_offers(
    client: AmadeusClient,
    hotel_ids: List[str],
    checkin: str,
    checkout: str,
    adults: int = 2,
) -> Dict[str, Any]:
    """
    Step 2: Get offers for specific hotels.
    """
    # Amadeus limits to ~20 hotel IDs per request for offers
    ids_str = ",".join(hotel_ids[:20])

    params = {
        "hotelIds": ids_str,
        "checkInDate": checkin,
        "checkOutDate": checkout,
        "adults": adults,
        "roomQuantity": 1,
    }

    return await client.request("GET", "/v3/shopping/hotel-offers", params=params)


async def hotel_search_by_city(
    client: AmadeusClient,
    city: str,
    checkin: str,
    checkout: str,
    adults: int = 2,
    radius_km: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search hotels by city using 2-step flow.

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

    # Step 1: Get hotel IDs by geocode
    logger.info(f"Fetching hotels near ({geo['lat']}, {geo['lon']})...")
    hotel_list = await get_hotels_by_geocode(client, geo["lat"], geo["lon"], radius_km)

    if not hotel_list:
        logger.warning(f"No hotels found for {city_upper}")
        return []

    hotel_ids = [h.get("hotelId") for h in hotel_list if h.get("hotelId")]
    logger.info(f"Found {len(hotel_ids)} hotels, fetching offers...")

    # Build hotel info map from geocode response
    hotel_info = {}
    for h in hotel_list:
        hid = h.get("hotelId")
        if hid:
            geo_code = h.get("geoCode", {})
            hotel_info[hid] = {
                "name": h.get("name"),
                "lat": geo_code.get("latitude"),
                "lon": geo_code.get("longitude"),
            }

    # Step 2: Get offers (in batches of 20)
    hotels = []
    for i in range(0, min(len(hotel_ids), 100), 20):  # Limit to 100 hotels
        batch = hotel_ids[i:i+20]
        try:
            data = await get_hotel_offers(client, batch, checkin, checkout, adults)

            for item in data.get("data", []):
                hotel = item.get("hotel", {})
                offers = item.get("offers", []) or []
                hotel_id = hotel.get("hotelId")

                # Get coordinates from geocode response or offer response
                info = hotel_info.get(hotel_id, {})
                lat = hotel.get("latitude") or info.get("lat")
                lon = hotel.get("longitude") or info.get("lon")
                name = hotel.get("name") or info.get("name")

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
                    "hotel_id": hotel_id,
                    "name": name,
                    "lat": lat,
                    "lon": lon,
                    "best_price_total": best_price,
                    "currency": best_currency,
                    "has_cancellation_policy_hint": refundable_hint,
                    "distance": dist,
                    "raw_offers_count": len(offers),
                })

        except Exception as e:
            logger.warning(f"Failed to get offers for batch {i}: {e}")
            continue

    # Sort by distance (nearest first), then by price
    def rank_key(h):
        d = (h.get("distance") or {}).get("distance_m", 10**9)
        p = h.get("best_price_total") if h.get("best_price_total") is not None else 10**9
        return (d, p)

    hotels.sort(key=rank_key)

    logger.info(f"Amadeus hotel search: {city_upper} found {len(hotels)} hotels with offers")
    return hotels
