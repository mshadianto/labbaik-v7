"""Amadeus API provider for hotel offers."""
import os
import json
from datetime import date, timedelta
from sqlalchemy import text
from app.db import get_session
from app.utils.http import post, get

AMADEUS_TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
AMADEUS_HOTEL_OFFERS = "https://test.api.amadeus.com/v3/shopping/hotel-offers"


async def _get_token() -> str:
    """Get OAuth2 access token from Amadeus."""
    cid = os.getenv("AMADEUS_CLIENT_ID")
    sec = os.getenv("AMADEUS_CLIENT_SECRET")

    r = await post(
        AMADEUS_TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "client_credentials", "client_id": cid, "client_secret": sec},
    )
    return r.json()["access_token"]


async def refresh_amadeus_offers(payload: dict):
    """
    Refresh hotel offers from Amadeus API.

    Args:
        payload: Job payload with city and days_ahead
    """
    city = payload.get("city", "MAKKAH")
    days_ahead = int(payload.get("days_ahead", 60))
    token = await _get_token()

    # Default occupancy
    adults, children = 2, 0
    checkin = date.today() + timedelta(days=7)
    checkout = checkin + timedelta(days=2)

    # Get hotel IDs mapped to Amadeus
    async with get_session() as session:
        hotel_ids = (await session.execute(text("""
          SELECT provider_hotel_id FROM provider_hotel_map
          WHERE provider='amadeus'
          AND hotel_id IN (SELECT hotel_id FROM hotels_master WHERE city=:c)
          LIMIT 80
        """), {"c": city})).scalars().all()

    if not hotel_ids:
        return {"status": "no_hotels", "city": city}

    headers = {"Authorization": f"Bearer {token}"}

    # Create search query record
    async with get_session() as session:
        qid = (await session.execute(text("""
          INSERT INTO search_queries(city, checkin, checkout, adults, children, currency)
          VALUES (:c, :ci, :co, :a, :ch, 'SAR') RETURNING query_id
        """), {"c": city, "ci": checkin, "co": checkout, "a": adults, "ch": children})).scalar_one()
        await session.commit()

    offers_count = 0

    for hid in hotel_ids:
        try:
            params = {
                "hotelIds": hid,
                "adults": adults,
                "checkInDate": str(checkin),
                "checkOutDate": str(checkout)
            }
            resp = await get(AMADEUS_HOTEL_OFFERS, headers=headers, params=params)
            data = resp.json()

            offers = data.get("data", [])
            for item in offers:
                offer_list = item.get("offers", []) or []
                for off in offer_list:
                    price = off.get("price", {})
                    total = float(price.get("total", 0) or 0)

                    # Resolve hotel_id via provider map
                    async with get_session() as session:
                        hotel_id = (await session.execute(text("""
                          SELECT hotel_id FROM provider_hotel_map
                          WHERE provider='amadeus' AND provider_hotel_id=:pid
                          LIMIT 1
                        """), {"pid": hid})).scalar()

                        if hotel_id:
                            await session.execute(text("""
                              INSERT INTO offers(hotel_id, provider, query_id, room_name, board_type, refundability,
                                                 price_total, availability_status, raw_payload)
                              VALUES (:hotel_id, 'amadeus', :qid, :room, :board, :ref,
                                      :total, :status, :raw::jsonb)
                            """), {
                                "hotel_id": hotel_id,
                                "qid": qid,
                                "room": (off.get("room", {}) or {}).get("typeEstimated", {}).get("category"),
                                "board": off.get("boardType"),
                                "ref": off.get("policies", {}).get("cancellations", [{}])[0].get("type"),
                                "total": total,
                                "status": off.get("availability", "unknown"),
                                "raw": json.dumps(off),
                            })
                            await session.commit()
                            offers_count += 1

        except Exception as e:
            # Log error but continue with next hotel
            print(f"Error fetching {hid}: {e}")
            continue

    return {"status": "done", "city": city, "offers_inserted": offers_count}
