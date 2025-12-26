from fastapi import FastAPI, Query
from datetime import date
from app.db import init_db, get_session
from app.crud import (
    search_hotels, get_hotel_offers, get_calendar, get_transport
)

app = FastAPI(title="Umrah Hotel & Transport API")


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/health")
async def health():
    return {"ok": True}


@app.get("/search_hotels")
async def api_search_hotels(
    city: str = Query(..., pattern="^(MAKKAH|MADINAH)$"),
    checkin: date = Query(...),
    checkout: date = Query(...),
    adults: int = 2,
    children: int = 0,
    max_hotels: int = 50,
):
    async with get_session() as session:
        return await search_hotels(session, city, checkin, checkout, adults, children, max_hotels)


@app.get("/hotel/{hotel_id}/offers")
async def api_hotel_offers(hotel_id: str, limit: int = 50):
    async with get_session() as session:
        return await get_hotel_offers(session, hotel_id, limit)


@app.get("/availability/calendar")
async def api_calendar(
    hotel_id: str,
    start: date,
    end: date,
    provider: str | None = None
):
    async with get_session() as session:
        return await get_calendar(session, hotel_id, start, end, provider)


@app.get("/transport/makkah-madinah")
async def api_transport(mode: str = Query("TRAIN", pattern="^(TRAIN|BUS)$"), limit: int = 50):
    async with get_session() as session:
        return await get_transport(session, "MAKKAH", "MADINAH", mode, limit)
