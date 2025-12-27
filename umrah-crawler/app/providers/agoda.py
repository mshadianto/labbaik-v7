"""
Agoda RapidAPI provider for hotel search and pricing.
======================================================
Uses search-overnight endpoint for Makkah & Madinah hotels.

Confirmed city IDs (2024-12-27):
- MAKKAH: 1_78591 (718 hotels)
- MADINAH: 1_23028 (999 hotels)
"""

import os
import json
import logging
from datetime import date, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from sqlalchemy import text

from app.db import get_session
from app.utils.http import get

logger = logging.getLogger(__name__)

# RapidAPI Agoda endpoint
AGODA_HOST = "agoda-com.p.rapidapi.com"
AGODA_URL = "https://agoda-com.p.rapidapi.com/hotels/search-overnight"

# Confirmed city IDs for RapidAPI
AGODA_CITY_IDS = {
    "MAKKAH": "1_78591",
    "MADINAH": "1_23028",
}


@dataclass
class AgodaHotel:
    """Parsed Agoda hotel data."""
    property_id: int
    name: str
    star_rating: float
    latitude: float
    longitude: float
    area: str
    city: str
    price_usd: Optional[float]
    price_display: Optional[str]
    currency: str
    raw_payload: Dict[str, Any]


def parse_hotel(prop: Dict[str, Any], city: str) -> Optional[AgodaHotel]:
    """Parse Agoda property response into AgodaHotel."""
    try:
        property_id = prop.get("propertyId")
        content = prop.get("content", {})
        summary = content.get("informationSummary", {})

        name = summary.get("defaultName") or summary.get("localeName")
        if not name:
            return None

        star_rating = float(summary.get("rating", 0) or 0)

        geo = summary.get("geoInfo", {})
        latitude = float(geo.get("latitude", 0) or 0)
        longitude = float(geo.get("longitude", 0) or 0)

        address = summary.get("address", {})
        area = address.get("area", {}).get("name", "")

        # Extract price
        price_usd = None
        price_display = None
        currency = "USD"

        pricing = prop.get("pricing", {})
        offers = pricing.get("offers", [])
        if offers:
            room_offers = offers[0].get("roomOffers", [])
            if room_offers:
                room = room_offers[0].get("room", {})
                pricing_list = room.get("pricing", [])
                if pricing_list:
                    price_info = pricing_list[0].get("price", {})
                    per_night = price_info.get("perNight", {})
                    exclusive = per_night.get("exclusive", {})
                    price_display = exclusive.get("display")
                    if price_display:
                        try:
                            price_usd = float(price_display)
                        except (ValueError, TypeError):
                            pass
                    currency = exclusive.get("currency", "USD")

        return AgodaHotel(
            property_id=property_id,
            name=name,
            star_rating=star_rating,
            latitude=latitude,
            longitude=longitude,
            area=area,
            city=city,
            price_usd=price_usd,
            price_display=price_display,
            currency=currency,
            raw_payload=prop,
        )
    except Exception as e:
        logger.warning(f"Failed to parse Agoda hotel: {e}")
        return None


async def fetch_agoda_hotels(
    city: str,
    checkin: Optional[date] = None,
    checkout: Optional[date] = None,
    adults: int = 2,
    rooms: int = 1,
) -> List[AgodaHotel]:
    """
    Fetch hotels from Agoda RapidAPI.

    Args:
        city: MAKKAH or MADINAH
        checkin: Check-in date (default: 30 days from now)
        checkout: Check-out date (default: checkin + 2 days)
        adults: Number of adults
        rooms: Number of rooms

    Returns:
        List of AgodaHotel objects
    """
    key = os.getenv("RAPIDAPI_KEY")
    if not key:
        logger.error("RAPIDAPI_KEY not set")
        return []

    city_upper = city.upper().replace("MECCA", "MAKKAH").replace("MEDINA", "MADINAH")
    city_id = AGODA_CITY_IDS.get(city_upper)
    if not city_id:
        logger.error(f"Unknown city: {city}")
        return []

    if not checkin:
        checkin = date.today() + timedelta(days=30)
    if not checkout:
        checkout = checkin + timedelta(days=2)

    headers = {
        "x-rapidapi-host": AGODA_HOST,
        "x-rapidapi-key": key,
        "accept": "application/json",
        "user-agent": "umrah-crawler/1.3",
    }

    params = {
        "id": city_id,
        "checkinDate": checkin.isoformat(),
        "checkoutDate": checkout.isoformat(),
        "adults": str(adults),
        "rooms": str(rooms),
    }

    try:
        resp = await get(AGODA_URL, headers=headers, params=params, timeout=45.0)
        data = resp.json()
    except Exception as e:
        logger.error(f"Agoda API request failed: {e}")
        return []

    # Extract properties
    properties = (
        data.get("data", {})
        .get("citySearch", {})
        .get("properties", [])
    )

    hotels = []
    for prop in properties:
        hotel = parse_hotel(prop, city_upper)
        if hotel:
            hotels.append(hotel)

    logger.info(f"Agoda: fetched {len(hotels)} hotels for {city_upper}")
    return hotels


async def refresh_agoda_snapshot(payload: dict) -> Dict[str, Any]:
    """
    Refresh Agoda hotel snapshot for a city.
    Stores hotels in hotels_master and offers in offers table.

    Args:
        payload: Job payload with city, days_ahead (optional)

    Returns:
        Status dict with counts
    """
    city = payload.get("city", "MAKKAH").upper()
    days_ahead = int(payload.get("days_ahead", 30))
    nights = int(payload.get("nights", 2))

    checkin = date.today() + timedelta(days=days_ahead)
    checkout = checkin + timedelta(days=nights)

    hotels = await fetch_agoda_hotels(city, checkin, checkout)

    if not hotels:
        return {"status": "no_hotels", "city": city}

    hotels_upserted = 0
    offers_inserted = 0

    # Create search query record
    async with get_session() as session:
        query_id = (await session.execute(text("""
            INSERT INTO search_queries(city, checkin, checkout, adults, children, currency)
            VALUES (:c, :ci, :co, 2, 0, 'USD')
            RETURNING query_id
        """), {"c": city, "ci": checkin, "co": checkout})).scalar_one()
        await session.commit()

    for hotel in hotels:
        try:
            async with get_session() as session:
                # Upsert hotel master
                hotel_id = (await session.execute(text("""
                    INSERT INTO hotels_master(name, city, star_rating, latitude, longitude, address)
                    VALUES (:name, :city, :star, :lat, :lng, :addr)
                    ON CONFLICT (city, name) DO UPDATE SET
                        star_rating = COALESCE(EXCLUDED.star_rating, hotels_master.star_rating),
                        latitude = COALESCE(EXCLUDED.latitude, hotels_master.latitude),
                        longitude = COALESCE(EXCLUDED.longitude, hotels_master.longitude),
                        updated_at = now()
                    RETURNING hotel_id
                """), {
                    "name": hotel.name,
                    "city": hotel.city,
                    "star": hotel.star_rating if hotel.star_rating > 0 else None,
                    "lat": hotel.latitude if hotel.latitude != 0 else None,
                    "lng": hotel.longitude if hotel.longitude != 0 else None,
                    "addr": hotel.area,
                })).scalar_one()

                hotels_upserted += 1

                # Insert offer if price available
                if hotel.price_usd:
                    await session.execute(text("""
                        INSERT INTO offers(hotel_id, provider, query_id, price_total,
                                          availability_status, raw_payload)
                        VALUES (:hid, 'agoda', :qid, :price, 'available', :raw::jsonb)
                    """), {
                        "hid": hotel_id,
                        "qid": query_id,
                        "price": hotel.price_usd,
                        "raw": json.dumps(hotel.raw_payload, default=str),
                    })
                    offers_inserted += 1

                # Update provider map
                await session.execute(text("""
                    INSERT INTO provider_hotel_map(hotel_id, provider, provider_hotel_id, last_seen)
                    VALUES (:hid, 'agoda', :pid, now())
                    ON CONFLICT (provider, provider_hotel_id) DO UPDATE SET
                        hotel_id = EXCLUDED.hotel_id,
                        last_seen = now()
                """), {
                    "hid": hotel_id,
                    "pid": str(hotel.property_id),
                })

                await session.commit()

        except Exception as e:
            logger.warning(f"Failed to upsert hotel {hotel.name}: {e}")
            continue

    logger.info(f"Agoda snapshot: {city} - {hotels_upserted} hotels, {offers_inserted} offers")

    return {
        "status": "done",
        "city": city,
        "checkin": str(checkin),
        "checkout": str(checkout),
        "hotels_upserted": hotels_upserted,
        "offers_inserted": offers_inserted,
    }


async def refresh_agoda_all_cities(payload: dict = None) -> Dict[str, Any]:
    """
    Refresh Agoda snapshot for all cities (Makkah + Madinah).

    Args:
        payload: Optional job payload with days_ahead

    Returns:
        Combined status dict
    """
    payload = payload or {}
    results = {}

    for city in ["MAKKAH", "MADINAH"]:
        city_payload = {**payload, "city": city}
        results[city] = await refresh_agoda_snapshot(city_payload)

    total_hotels = sum(r.get("hotels_upserted", 0) for r in results.values())
    total_offers = sum(r.get("offers_inserted", 0) for r in results.values())

    return {
        "status": "done",
        "cities": results,
        "total_hotels": total_hotels,
        "total_offers": total_offers,
    }
