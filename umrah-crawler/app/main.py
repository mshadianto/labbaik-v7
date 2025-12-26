from fastapi import FastAPI, Query, HTTPException
from datetime import date
from app.db import init_db, get_session, is_db_configured
from app.crud import (
    search_hotels, get_hotel_offers, get_calendar, get_transport
)
from app.jobs import bootstrap_jobs, dequeue_and_run, start_scheduler

app = FastAPI(title="Umrah Hotel & Transport API")


@app.on_event("startup")
async def startup():
    await init_db()
    start_scheduler()


@app.get("/health")
async def health():
    return {
        "ok": True,
        "database": "connected" if is_db_configured() else "not_configured"
    }


@app.get("/search_hotels")
async def api_search_hotels(
    city: str = Query(..., pattern="^(MAKKAH|MADINAH)$"),
    checkin: date = Query(...),
    checkout: date = Query(...),
    adults: int = 2,
    children: int = 0,
    max_hotels: int = 50,
):
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    async with get_session() as session:
        return await search_hotels(session, city, checkin, checkout, adults, children, max_hotels)


@app.get("/hotel/{hotel_id}/offers")
async def api_hotel_offers(hotel_id: str, limit: int = 50):
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    async with get_session() as session:
        return await get_hotel_offers(session, hotel_id, limit)


@app.get("/availability/calendar")
async def api_calendar(
    hotel_id: str,
    start: date,
    end: date,
    provider: str | None = None
):
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    async with get_session() as session:
        return await get_calendar(session, hotel_id, start, end, provider)


@app.get("/transport/makkah-madinah")
async def api_transport(mode: str = Query("TRAIN", pattern="^(TRAIN|BUS)$"), limit: int = 50):
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    async with get_session() as session:
        return await get_transport(session, "MAKKAH", "MADINAH", mode, limit)


@app.post("/crawl/bootstrap")
async def api_bootstrap_jobs():
    """Bootstrap all crawl jobs for hotels and transport."""
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    await bootstrap_jobs()
    return {"status": "jobs_queued", "message": "Crawl jobs for Makkah and Madinah have been queued"}


@app.post("/crawl/run")
async def api_run_jobs(batch: int = 10):
    """Manually trigger job processing."""
    if not is_db_configured():
        raise HTTPException(status_code=503, detail="Database not configured")
    await dequeue_and_run(batch)
    return {"status": "processed", "batch_size": batch}
