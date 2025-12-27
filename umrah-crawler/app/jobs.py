import os
import json
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import text

from app.db import get_session
from app.providers.haramain import fetch_haramain_timetable
from app.providers.saptco import fetch_saptco_schedule
from app.providers.amadeus import refresh_amadeus_offers
from app.providers.xotelo import refresh_xotelo_prices
from app.providers.makcorps import refresh_makcorps_prices
from app.providers.agoda import refresh_agoda_snapshot, refresh_agoda_all_cities

scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")


async def enqueue_job(job_type: str, payload: dict, run_at: datetime | None = None):
    """Add a job to the queue."""
    run_at = run_at or datetime.utcnow()
    async with get_session() as session:
        q = text("""INSERT INTO crawl_jobs(type, payload, run_at) VALUES (:t, :p::jsonb, :r)""")
        await session.execute(q, {"t": job_type, "p": json.dumps(payload), "r": run_at})
        await session.commit()


async def dequeue_and_run(batch: int = 10):
    """Process queued jobs."""
    async with get_session() as session:
        jobs = (await session.execute(text("""
          SELECT job_id, type, payload
          FROM crawl_jobs
          WHERE status='queued' AND run_at <= now()
          ORDER BY run_at ASC
          LIMIT :b
          FOR UPDATE SKIP LOCKED
        """), {"b": batch})).mappings().all()

        for job in jobs:
            await session.execute(
                text("UPDATE crawl_jobs SET status='running' WHERE job_id=:id"),
                {"id": job["job_id"]}
            )
        await session.commit()

    # Run outside lock
    for job in jobs:
        try:
            t = job["type"]
            p = job["payload"]

            if t == "transport_haramain":
                await fetch_haramain_timetable()
            elif t == "transport_saptco":
                await fetch_saptco_schedule()
            elif t == "prices_xotelo":
                await refresh_xotelo_prices(p)
            elif t == "prices_makcorps":
                await refresh_makcorps_prices(p)
            elif t == "offers_amadeus":
                await refresh_amadeus_offers(p)
            elif t == "agoda_snapshot":
                await refresh_agoda_snapshot(p)
            elif t == "agoda_all_cities":
                await refresh_agoda_all_cities(p)
            else:
                raise ValueError(f"unknown job type: {t}")

            async with get_session() as session:
                await session.execute(
                    text("UPDATE crawl_jobs SET status='done', last_error=NULL WHERE job_id=:id"),
                    {"id": job["job_id"]}
                )
                await session.commit()

        except Exception as e:
            async with get_session() as session:
                await session.execute(
                    text("UPDATE crawl_jobs SET status='failed', last_error=:err WHERE job_id=:id"),
                    {"id": job["job_id"], "err": str(e)}
                )
                await session.commit()


async def bootstrap_jobs():
    """Create initial jobs for crawling."""
    # Transport refresh (daily)
    await enqueue_job("transport_haramain", {})
    await enqueue_job("transport_saptco", {})

    # Price scan 2x daily for each city
    await enqueue_job("prices_xotelo", {"city": "MAKKAH"})
    await enqueue_job("prices_makcorps", {"city": "MAKKAH"})
    await enqueue_job("prices_xotelo", {"city": "MADINAH"})
    await enqueue_job("prices_makcorps", {"city": "MADINAH"})

    # Availability confirm (expensive) - 1x/day
    await enqueue_job("offers_amadeus", {"city": "MAKKAH", "days_ahead": 60})
    await enqueue_job("offers_amadeus", {"city": "MADINAH", "days_ahead": 60})

    # Agoda snapshot - 1x/day for each city
    await enqueue_job("agoda_snapshot", {"city": "MAKKAH", "days_ahead": 30})
    await enqueue_job("agoda_snapshot", {"city": "MADINAH", "days_ahead": 30})


def start_scheduler():
    """Start the background job scheduler."""
    scheduler.add_job(dequeue_and_run, "interval", minutes=3, id="runner")
    scheduler.start()


if __name__ == "__main__":
    async def main():
        await bootstrap_jobs()
        start_scheduler()
        while True:
            await asyncio.sleep(3600)

    asyncio.run(main())
