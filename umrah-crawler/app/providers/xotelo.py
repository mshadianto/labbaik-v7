"""Xotelo (RapidAPI) provider for hotel price intelligence."""
import os
import json
from sqlalchemy import text
from app.db import get_session
from app.utils.http import get

XOTELO_URL = "https://xotelo-hotel-prices.p.rapidapi.com/search"


async def refresh_xotelo_prices(payload: dict):
    """
    Refresh hotel prices from Xotelo API.

    Args:
        payload: Job payload with city
    """
    key = os.getenv("XOTELO_RAPIDAPI_KEY")
    if not key:
        return {"status": "no_api_key"}

    city = payload.get("city", "MAKKAH")

    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "xotelo-hotel-prices.p.rapidapi.com"
    }

    params = {"city": "Mecca" if city == "MAKKAH" else "Medina"}

    try:
        r = await get(XOTELO_URL, headers=headers, params=params)
        data = r.json()
    except Exception as e:
        return {"status": "error", "error": str(e)}

    hotels_processed = 0

    for h in (data.get("hotels", []) or [])[:200]:
        name = h.get("name")
        if not name:
            continue

        price = float(h.get("min_price", 0) or 0)

        async with get_session() as session:
            # Upsert hotel master by (city, name)
            hotel_id = (await session.execute(text("""
              INSERT INTO hotels_master(name, city)
              VALUES (:n, :c)
              ON CONFLICT (city, name) DO UPDATE SET updated_at=now()
              RETURNING hotel_id
            """), {"n": name, "c": city})).scalar_one()

            # Insert price offer
            await session.execute(text("""
              INSERT INTO offers(hotel_id, provider, query_id, price_total, availability_status, raw_payload)
              VALUES (:hid, 'xotelo', NULL, :p, 'unknown', :raw::jsonb)
            """), {"hid": hotel_id, "p": price, "raw": json.dumps(h)})

            # Update provider map
            provider_hotel_id = h.get("id") or h.get("hotel_id") or name
            await session.execute(text("""
              INSERT INTO provider_hotel_map(hotel_id, provider, provider_hotel_id, last_seen)
              VALUES (:hid, 'xotelo', :pid, now())
              ON CONFLICT (provider, provider_hotel_id) DO UPDATE SET last_seen=now()
            """), {"hid": hotel_id, "pid": str(provider_hotel_id)})

            await session.commit()
            hotels_processed += 1

    return {"status": "done", "city": city, "hotels_processed": hotels_processed}
