"""
LABBAIK AI - Job Scheduler V1.3
===============================
Enhanced job scheduler with:
- FX auto-refresh (ECB)
- Transport JSON-first scraping
- Health checks & observability
- Snapshot management
"""

import os
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import text

from app.db import get_session

# V1.3 Providers
from app.providers.fx_ecb import get_fx_service, FXService
from app.providers.haramain_v13 import fetch_haramain_schedule, fetch_all_routes as fetch_haramain_all
from app.providers.saptco_v13 import fetch_saptco_schedule, fetch_all_routes as fetch_saptco_all
from app.providers.transport_engine import FetchMethod

# V1.3 Services
from app.services.healthcheck import (
    daily_healthcheck, write_metric, record_provider_scrape, record_fx_update
)

# Legacy providers (still used)
from app.providers.amadeus import refresh_amadeus_offers
from app.providers.xotelo import refresh_xotelo_prices
from app.providers.makcorps import refresh_makcorps_prices

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")


# =============================================================================
# JOB TYPES V1.3
# =============================================================================

JOB_TYPES = {
    # Transport (V1.3 - JSON first)
    "transport_haramain_v13": "Haramain train schedule (JSON-first)",
    "transport_saptco_v13": "SAPTCO bus schedule (JSON-first)",

    # FX (V1.3)
    "fx_ecb_refresh": "ECB exchange rate refresh",

    # Legacy transport
    "transport_haramain": "Haramain train (legacy)",
    "transport_saptco": "SAPTCO bus (legacy)",

    # Prices
    "prices_xotelo": "Xotelo price refresh",
    "prices_makcorps": "Makcorps price refresh",
    "offers_amadeus": "Amadeus availability",

    # V1.3 Maintenance
    "healthcheck_daily": "Daily health check",
    "snapshot_save": "Save transport snapshots",
    "cleanup_old_data": "Cleanup old records",
}


# =============================================================================
# QUEUE FUNCTIONS
# =============================================================================

async def enqueue_job(
    job_type: str,
    payload: dict = None,
    run_at: datetime = None,
    priority: int = 5
):
    """
    Add a job to the queue.

    Args:
        job_type: Type of job (see JOB_TYPES)
        payload: Job-specific data
        run_at: When to run (default: now)
        priority: 1-10, lower = higher priority
    """
    run_at = run_at or datetime.utcnow()
    payload = payload or {}

    async with get_session() as session:
        q = text("""
            INSERT INTO crawl_jobs(type, payload, run_at, priority)
            VALUES (:t, :p::jsonb, :r, :pr)
            ON CONFLICT DO NOTHING
        """)
        await session.execute(q, {
            "t": job_type,
            "p": json.dumps(payload),
            "r": run_at,
            "pr": priority
        })
        await session.commit()

    logger.debug(f"Enqueued job: {job_type}")


async def dequeue_and_run(batch: int = 10):
    """Process queued jobs."""
    async with get_session() as session:
        jobs = (await session.execute(text("""
            SELECT job_id, type, payload
            FROM crawl_jobs
            WHERE status='queued' AND run_at <= now()
            ORDER BY priority ASC, run_at ASC
            LIMIT :b
            FOR UPDATE SKIP LOCKED
        """), {"b": batch})).mappings().all()

        for job in jobs:
            await session.execute(
                text("UPDATE crawl_jobs SET status='running', started_at=now() WHERE job_id=:id"),
                {"id": job["job_id"]}
            )
        await session.commit()

    # Run jobs outside transaction lock
    for job in jobs:
        job_id = job["job_id"]
        job_type = job["type"]
        payload = job["payload"] or {}
        start_time = datetime.utcnow()

        try:
            result = await run_job(job_type, payload)

            async with get_session() as session:
                await session.execute(
                    text("""
                        UPDATE crawl_jobs
                        SET status='done', last_error=NULL, finished_at=now()
                        WHERE job_id=:id
                    """),
                    {"id": job_id}
                )
                await session.commit()

            # Record success metric
            elapsed_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            record_provider_scrape(job_type, success=True, latency_ms=elapsed_ms)

            logger.info(f"Job done: {job_type} ({elapsed_ms:.0f}ms)")

        except Exception as e:
            async with get_session() as session:
                await session.execute(
                    text("""
                        UPDATE crawl_jobs
                        SET status='failed', last_error=:err, finished_at=now()
                        WHERE job_id=:id
                    """),
                    {"id": job_id, "err": str(e)[:500]}
                )
                await session.commit()

            # Record failure metric
            elapsed_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            record_provider_scrape(job_type, success=False, error=str(e), latency_ms=elapsed_ms)

            logger.error(f"Job failed: {job_type} - {e}")


async def run_job(job_type: str, payload: dict) -> dict:
    """
    Execute a job by type.

    Args:
        job_type: Job type string
        payload: Job parameters

    Returns:
        Job result dict
    """
    # V1.3 Transport (JSON-first)
    if job_type == "transport_haramain_v13":
        results = await fetch_haramain_all()
        total_rows = sum(r.rows.__len__() for r in results.values())
        write_metric("HARAMAIN", "transport_rows", float(total_rows))
        return {"routes": len(results), "total_rows": total_rows}

    elif job_type == "transport_saptco_v13":
        results = await fetch_saptco_all()
        total_rows = sum(r.rows.__len__() for r in results.values())
        write_metric("SAPTCO", "transport_rows", float(total_rows))
        return {"routes": len(results), "total_rows": total_rows}

    # V1.3 FX
    elif job_type == "fx_ecb_refresh":
        fx = await get_fx_service()
        success = await fx.refresh()
        source = fx.source
        rate_count = len(fx.rates)
        record_fx_update(source, rate_count, age_hours=0)
        return {"success": success, "source": source, "currencies": rate_count}

    # V1.3 Health Check
    elif job_type == "healthcheck_daily":
        result = await daily_healthcheck()
        return result

    # Legacy Transport
    elif job_type == "transport_haramain":
        from app.providers.haramain import fetch_haramain_timetable
        await fetch_haramain_timetable()
        return {"status": "done"}

    elif job_type == "transport_saptco":
        from app.providers.saptco import fetch_saptco_schedule
        await fetch_saptco_schedule()
        return {"status": "done"}

    # Prices
    elif job_type == "prices_xotelo":
        await refresh_xotelo_prices(payload)
        return {"status": "done", "city": payload.get("city")}

    elif job_type == "prices_makcorps":
        await refresh_makcorps_prices(payload)
        return {"status": "done", "city": payload.get("city")}

    elif job_type == "offers_amadeus":
        await refresh_amadeus_offers(payload)
        return {"status": "done", "city": payload.get("city")}

    # Maintenance
    elif job_type == "cleanup_old_data":
        return await cleanup_old_records(payload.get("days", 30))

    elif job_type == "snapshot_save":
        return await save_transport_snapshots()

    else:
        raise ValueError(f"Unknown job type: {job_type}")


# =============================================================================
# MAINTENANCE JOBS
# =============================================================================

async def cleanup_old_records(days: int = 30) -> dict:
    """
    Clean up old records to save space.

    Args:
        days: Delete records older than this

    Returns:
        Counts of deleted records
    """
    cutoff = datetime.utcnow() - timedelta(days=days)
    deleted = {}

    async with get_session() as session:
        # Clean old transport schedules
        result = await session.execute(text("""
            DELETE FROM transport_schedule
            WHERE fetched_at < :cutoff
        """), {"cutoff": cutoff})
        deleted["transport_schedule"] = result.rowcount

        # Clean old provider metrics
        result = await session.execute(text("""
            DELETE FROM provider_metrics
            WHERE ts < :cutoff
        """), {"cutoff": cutoff})
        deleted["provider_metrics"] = result.rowcount

        # Clean old itinerary legs
        result = await session.execute(text("""
            DELETE FROM itinerary_legs
            WHERE fetched_at < :cutoff
        """), {"cutoff": cutoff})
        deleted["itinerary_legs"] = result.rowcount

        # Clean done/failed jobs
        result = await session.execute(text("""
            DELETE FROM crawl_jobs
            WHERE status IN ('done', 'failed') AND run_at < :cutoff
        """), {"cutoff": cutoff})
        deleted["crawl_jobs"] = result.rowcount

        await session.commit()

    logger.info(f"Cleanup completed: {deleted}")
    return deleted


async def save_transport_snapshots() -> dict:
    """
    Save current transport data as snapshots for fallback.

    Returns:
        Snapshot summary
    """
    from app.providers.transport_engine import get_transport_engine

    engine = get_transport_engine()
    saved = {}

    async with get_session() as session:
        for route in ["MAKKAH_MADINAH", "MADINAH_MAKKAH"]:
            for operator in ["HARAMAIN", "SAPTCO"]:
                snapshot = engine.get_snapshot(route)
                if snapshot:
                    await session.execute(text("""
                        INSERT INTO transport_snapshots(operator, route, snapshot_data, snapshot_date)
                        VALUES (:op, :r, :data::jsonb, :d)
                        ON CONFLICT (operator, route)
                        DO UPDATE SET snapshot_data = EXCLUDED.snapshot_data, snapshot_date = EXCLUDED.snapshot_date
                    """), {
                        "op": operator,
                        "r": route,
                        "data": json.dumps(snapshot),
                        "d": datetime.utcnow().date()
                    })
                    saved[f"{operator}_{route}"] = True

        await session.commit()

    logger.info(f"Snapshots saved: {list(saved.keys())}")
    return {"saved": list(saved.keys())}


# =============================================================================
# BOOTSTRAP & SCHEDULER
# =============================================================================

async def bootstrap_jobs_v13():
    """Create initial V1.3 jobs."""

    # FX refresh (2x daily)
    await enqueue_job("fx_ecb_refresh", {}, priority=2)

    # Transport V1.3 (every 6 hours)
    await enqueue_job("transport_haramain_v13", {}, priority=3)
    await enqueue_job("transport_saptco_v13", {}, priority=3)

    # Price scans (2x daily per city)
    for city in ["MAKKAH", "MADINAH"]:
        await enqueue_job("prices_xotelo", {"city": city}, priority=5)
        await enqueue_job("prices_makcorps", {"city": city}, priority=5)

    # Availability (1x daily)
    for city in ["MAKKAH", "MADINAH"]:
        await enqueue_job("offers_amadeus", {"city": city, "days_ahead": 60}, priority=6)

    # Health check (daily)
    await enqueue_job("healthcheck_daily", {}, priority=1)

    # Cleanup (weekly)
    await enqueue_job("cleanup_old_data", {"days": 30}, priority=10)

    logger.info("V1.3 jobs bootstrapped")


def start_scheduler_v13():
    """Start the V1.3 scheduler with enhanced intervals."""

    # Job runner (every 2 minutes)
    scheduler.add_job(
        dequeue_and_run,
        "interval",
        minutes=2,
        id="job_runner",
        replace_existing=True
    )

    # FX refresh (every 12 hours)
    scheduler.add_job(
        lambda: asyncio.create_task(enqueue_job("fx_ecb_refresh", {}, priority=2)),
        "interval",
        hours=12,
        id="fx_refresh_scheduler",
        replace_existing=True
    )

    # Transport refresh (every 6 hours)
    scheduler.add_job(
        lambda: asyncio.create_task(enqueue_job("transport_haramain_v13", {})),
        "interval",
        hours=6,
        id="haramain_scheduler",
        replace_existing=True
    )
    scheduler.add_job(
        lambda: asyncio.create_task(enqueue_job("transport_saptco_v13", {})),
        "interval",
        hours=6,
        id="saptco_scheduler",
        replace_existing=True
    )

    # Daily health check (at 06:00 Jakarta time)
    scheduler.add_job(
        lambda: asyncio.create_task(enqueue_job("healthcheck_daily", {}, priority=1)),
        "cron",
        hour=6,
        minute=0,
        id="daily_healthcheck",
        replace_existing=True
    )

    # Weekly cleanup (Sunday 03:00)
    scheduler.add_job(
        lambda: asyncio.create_task(enqueue_job("cleanup_old_data", {"days": 30})),
        "cron",
        day_of_week="sun",
        hour=3,
        minute=0,
        id="weekly_cleanup",
        replace_existing=True
    )

    # Save snapshots (every 24 hours)
    scheduler.add_job(
        lambda: asyncio.create_task(enqueue_job("snapshot_save", {})),
        "interval",
        hours=24,
        id="snapshot_save",
        replace_existing=True
    )

    scheduler.start()
    logger.info("V1.3 scheduler started")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    async def main():
        await bootstrap_jobs_v13()
        start_scheduler_v13()

        logger.info("V1.3 Job scheduler running...")
        while True:
            await asyncio.sleep(3600)

    asyncio.run(main())
