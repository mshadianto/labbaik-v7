"""MakCorps API provider for hotel data."""
import os
import json
from sqlalchemy import text
from app.db import get_session
from app.utils.http import get

MAKCORPS_URL = "https://api.makcorps.com/free/hotels"


async def refresh_makcorps_prices(payload: dict):
    """
    Refresh hotel prices from MakCorps API.

    Args:
        payload: Job payload with city

    Note: Free tier has limited calls (30/month)
    """
    city = payload.get("city", "MAKKAH")

    params = {"city": "Mecca" if city == "MAKKAH" else "Medina"}

    try:
        r = await get(MAKCORPS_URL, params=params)
        data = r.json()
    except Exception as e:
        return {"status": "error", "error": str(e)}

    hotels_processed = 0

    for h in (data.get("hotels", []) or [])[:100]:
        name = h.get("name")
        if not name:
            continue

        price = float(h.get("price", 0) or 0)
        address = h.get("address", "")

        async with get_session() as session:
            # Upsert hotel master
            hotel_id = (await session.execute(text("""
              INSERT INTO hotels_master(name, city, address_raw)
              VALUES (:n, :c, :a)
              ON CONFLICT (city, name) DO UPDATE SET
                address_raw = COALESCE(EXCLUDED.address_raw, hotels_master.address_raw),
                updated_at = now()
              RETURNING hotel_id
            """), {"n": name, "c": city, "a": address})).scalar_one()

            # Insert price offer
            await session.execute(text("""
              INSERT INTO offers(hotel_id, provider, query_id, price_total, availability_status, raw_payload)
              VALUES (:hid, 'makcorps', NULL, :p, 'unknown', :raw::jsonb)
            """), {"hid": hotel_id, "p": price, "raw": json.dumps(h)})

            # Update provider map
            provider_hotel_id = h.get("id") or name
            await session.execute(text("""
              INSERT INTO provider_hotel_map(hotel_id, provider, provider_hotel_id, last_seen)
              VALUES (:hid, 'makcorps', :pid, now())
              ON CONFLICT (provider, provider_hotel_id) DO UPDATE SET last_seen=now()
            """), {"hid": hotel_id, "pid": str(provider_hotel_id)})

            await session.commit()
            hotels_processed += 1

    return {"status": "done", "city": city, "hotels_processed": hotels_processed}
