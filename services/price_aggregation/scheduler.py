"""
LABBAIK AI v7.5 - Price Aggregation Scheduler
==============================================
Background job scheduler for periodic price refresh.

Jobs:
- API refresh: Every 2 hours
- OTA scraping: Every 6 hours
- Partner sync: Every 1 hour
- Cache cleanup: Every 4 hours
- Price history snapshot: Every 4 hours
"""

import logging
import threading
import time
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class JobStatus(str, Enum):
    """Job execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ScheduledJob:
    """Scheduled job definition."""
    name: str
    func: Callable
    interval_hours: float
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0
    fail_count: int = 0
    last_status: JobStatus = JobStatus.PENDING
    last_error: Optional[str] = None
    last_duration_seconds: float = 0


class PriceAggregationScheduler:
    """
    Background scheduler for price aggregation jobs.

    Runs periodic jobs to:
    - Refresh API data
    - Scrape OTA sites
    - Sync partner feeds
    - Clean up cache
    - Record price history
    """

    def __init__(
        self,
        enable_api_refresh: bool = True,
        enable_scraping: bool = True,
        enable_partner_sync: bool = True,
        enable_cache_cleanup: bool = True,
        enable_history_snapshot: bool = True,
    ):
        self.jobs: Dict[str, ScheduledJob] = {}
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._lock = threading.RLock()

        # Job configurations
        self.config = {
            "api_refresh": {
                "enabled": enable_api_refresh,
                "interval_hours": 2.0,
            },
            "ota_scraping": {
                "enabled": enable_scraping,
                "interval_hours": 6.0,
            },
            "partner_sync": {
                "enabled": enable_partner_sync,
                "interval_hours": 1.0,
            },
            "cache_cleanup": {
                "enabled": enable_cache_cleanup,
                "interval_hours": 4.0,
            },
            "history_snapshot": {
                "enabled": enable_history_snapshot,
                "interval_hours": 4.0,
            },
        }

        # Statistics
        self._stats = {
            "started_at": None,
            "total_runs": 0,
            "total_failures": 0,
        }

    def register_job(
        self,
        name: str,
        func: Callable,
        interval_hours: float,
        enabled: bool = True
    ) -> None:
        """Register a new scheduled job."""
        with self._lock:
            self.jobs[name] = ScheduledJob(
                name=name,
                func=func,
                interval_hours=interval_hours,
                enabled=enabled,
                next_run=datetime.now() + timedelta(hours=interval_hours)
            )
            logger.info(f"Registered job: {name} (every {interval_hours}h)")

    def register_default_jobs(self) -> None:
        """Register default price aggregation jobs."""

        # API Refresh Job
        if self.config["api_refresh"]["enabled"]:
            self.register_job(
                name="api_refresh",
                func=self._job_api_refresh,
                interval_hours=self.config["api_refresh"]["interval_hours"]
            )

        # OTA Scraping Job
        if self.config["ota_scraping"]["enabled"]:
            self.register_job(
                name="ota_scraping",
                func=self._job_ota_scraping,
                interval_hours=self.config["ota_scraping"]["interval_hours"]
            )

        # Partner Sync Job
        if self.config["partner_sync"]["enabled"]:
            self.register_job(
                name="partner_sync",
                func=self._job_partner_sync,
                interval_hours=self.config["partner_sync"]["interval_hours"]
            )

        # Cache Cleanup Job
        if self.config["cache_cleanup"]["enabled"]:
            self.register_job(
                name="cache_cleanup",
                func=self._job_cache_cleanup,
                interval_hours=self.config["cache_cleanup"]["interval_hours"]
            )

        # History Snapshot Job
        if self.config["history_snapshot"]["enabled"]:
            self.register_job(
                name="history_snapshot",
                func=self._job_history_snapshot,
                interval_hours=self.config["history_snapshot"]["interval_hours"]
            )

    def _job_api_refresh(self) -> Dict[str, Any]:
        """Refresh data from APIs (Amadeus, Xotelo, MakCorps)."""
        logger.info("Running API refresh job...")

        try:
            from services.price_aggregation import get_price_aggregator

            aggregator = get_price_aggregator()

            # Refresh for both cities
            result = {
                "makkah": 0,
                "madinah": 0,
                "errors": []
            }

            for city in ["Makkah", "Madinah"]:
                try:
                    agg_result = aggregator.aggregate(
                        city=city,
                        offer_type="hotel",
                        force_refresh=True,
                        limit=50
                    )
                    result[city.lower()] = agg_result.get("total_returned", 0)
                except Exception as e:
                    result["errors"].append(f"{city}: {str(e)}")

            logger.info(f"API refresh complete: {result}")
            return result

        except Exception as e:
            logger.error(f"API refresh failed: {e}")
            raise

    def _job_ota_scraping(self) -> Dict[str, Any]:
        """Scrape OTA sites for package prices."""
        logger.info("Running OTA scraping job...")

        try:
            from services.scrapers import get_scraper_manager

            manager = get_scraper_manager()

            # Scrape packages from Jakarta
            result = manager.scrape_all_packages(
                departure_city="Jakarta",
                parallel=True
            )

            # Save to aggregator
            if result.get("offers"):
                from services.price_aggregation import get_price_aggregator
                aggregator = get_price_aggregator()
                aggregator._save_to_database(result["offers"])

            logger.info(f"OTA scraping complete: {len(result.get('offers', []))} offers")
            return {
                "offers_found": len(result.get("offers", [])),
                "source_stats": result.get("source_stats", {}),
                "errors": result.get("errors")
            }

        except Exception as e:
            logger.error(f"OTA scraping failed: {e}")
            raise

    def _job_partner_sync(self) -> Dict[str, Any]:
        """Sync approved partner price feeds."""
        logger.info("Running partner sync job...")

        try:
            from services.price_aggregation import get_price_aggregator

            aggregator = get_price_aggregator()

            # Fetch partner feeds through aggregator
            partner_offers, partner_stats = aggregator._fetch_from_partners()

            # Save to database
            if partner_offers:
                aggregator._save_to_database(partner_offers)

            logger.info(f"Partner sync complete: {len(partner_offers)} offers")
            return {
                "offers_synced": len(partner_offers),
                "stats": partner_stats
            }

        except Exception as e:
            logger.error(f"Partner sync failed: {e}")
            raise

    def _job_cache_cleanup(self) -> Dict[str, Any]:
        """Clean up expired cache entries."""
        logger.info("Running cache cleanup job...")

        try:
            from services.price_aggregation import get_price_cache

            cache = get_price_cache()

            # Cleanup expired entries
            expired_count = cache.cleanup_expired()

            # Get stats
            stats = cache.get_stats()

            logger.info(f"Cache cleanup complete: {expired_count} expired entries removed")
            return {
                "expired_removed": expired_count,
                "current_entries": stats.get("entries", 0),
                "hit_rate": stats.get("hit_rate", 0)
            }

        except Exception as e:
            logger.error(f"Cache cleanup failed: {e}")
            raise

    def _job_history_snapshot(self) -> Dict[str, Any]:
        """Record price history snapshot."""
        logger.info("Running history snapshot job...")

        try:
            from services.price_aggregation.repository import get_aggregated_price_repository

            repository = get_aggregated_price_repository()

            # Get all current offers
            offers = repository.search(limit=500)

            # Record history for each
            recorded = 0
            for offer in offers:
                if offer.id:
                    try:
                        repository.record_price_history(
                            offer_id=offer.id,
                            price_sar=offer.price_sar,
                            price_idr=offer.price_idr,
                            availability_status=offer.availability_status.value if offer.availability_status else "unknown",
                            rooms_left=offer.rooms_left,
                            source_name=offer.source_name
                        )
                        recorded += 1
                    except Exception:
                        pass

            logger.info(f"History snapshot complete: {recorded} records")
            return {"recorded": recorded}

        except Exception as e:
            logger.error(f"History snapshot failed: {e}")
            raise

    def run_job(self, job_name: str) -> Dict[str, Any]:
        """Manually run a specific job."""
        with self._lock:
            job = self.jobs.get(job_name)
            if not job:
                raise ValueError(f"Job not found: {job_name}")

            return self._execute_job(job)

    def _execute_job(self, job: ScheduledJob) -> Dict[str, Any]:
        """Execute a job and update its status."""
        if not job.enabled:
            job.last_status = JobStatus.SKIPPED
            return {"status": "skipped", "reason": "Job disabled"}

        start_time = datetime.now()
        job.last_status = JobStatus.RUNNING

        try:
            result = job.func()

            end_time = datetime.now()
            job.last_run = end_time
            job.next_run = end_time + timedelta(hours=job.interval_hours)
            job.run_count += 1
            job.last_status = JobStatus.COMPLETED
            job.last_duration_seconds = (end_time - start_time).total_seconds()
            job.last_error = None

            self._stats["total_runs"] += 1

            return {
                "status": "completed",
                "duration_seconds": job.last_duration_seconds,
                "result": result
            }

        except Exception as e:
            end_time = datetime.now()
            job.last_run = end_time
            job.next_run = end_time + timedelta(hours=job.interval_hours)
            job.fail_count += 1
            job.last_status = JobStatus.FAILED
            job.last_duration_seconds = (end_time - start_time).total_seconds()
            job.last_error = str(e)

            self._stats["total_runs"] += 1
            self._stats["total_failures"] += 1

            logger.error(f"Job {job.name} failed: {e}")

            return {
                "status": "failed",
                "duration_seconds": job.last_duration_seconds,
                "error": str(e)
            }

    def _run_scheduler(self) -> None:
        """Background scheduler loop."""
        logger.info("Scheduler thread started")

        while self._running:
            now = datetime.now()

            with self._lock:
                for job in self.jobs.values():
                    if job.enabled and job.next_run and now >= job.next_run:
                        logger.info(f"Executing scheduled job: {job.name}")
                        self._execute_job(job)

            # Sleep for 60 seconds before checking again
            time.sleep(60)

        logger.info("Scheduler thread stopped")

    def start(self) -> None:
        """Start the background scheduler."""
        if self._running:
            logger.warning("Scheduler already running")
            return

        self._running = True
        self._stats["started_at"] = datetime.now().isoformat()

        # Register default jobs if none registered
        if not self.jobs:
            self.register_default_jobs()

        # Start background thread
        self._thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._thread.start()

        logger.info("Price aggregation scheduler started")

    def stop(self) -> None:
        """Stop the background scheduler."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Price aggregation scheduler stopped")

    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self._running

    def get_jobs(self) -> List[Dict[str, Any]]:
        """Get list of all registered jobs."""
        with self._lock:
            return [
                {
                    "name": job.name,
                    "enabled": job.enabled,
                    "interval_hours": job.interval_hours,
                    "last_run": job.last_run.isoformat() if job.last_run else None,
                    "next_run": job.next_run.isoformat() if job.next_run else None,
                    "run_count": job.run_count,
                    "fail_count": job.fail_count,
                    "last_status": job.last_status.value,
                    "last_error": job.last_error,
                    "last_duration_seconds": job.last_duration_seconds
                }
                for job in self.jobs.values()
            ]

    def get_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        return {
            "is_running": self._running,
            "started_at": self._stats["started_at"],
            "total_runs": self._stats["total_runs"],
            "total_failures": self._stats["total_failures"],
            "jobs_count": len(self.jobs),
            "enabled_jobs": sum(1 for j in self.jobs.values() if j.enabled)
        }

    def enable_job(self, job_name: str) -> bool:
        """Enable a job."""
        with self._lock:
            if job_name in self.jobs:
                self.jobs[job_name].enabled = True
                return True
            return False

    def disable_job(self, job_name: str) -> bool:
        """Disable a job."""
        with self._lock:
            if job_name in self.jobs:
                self.jobs[job_name].enabled = False
                return True
            return False


# Singleton
_scheduler: Optional[PriceAggregationScheduler] = None


def get_price_scheduler() -> PriceAggregationScheduler:
    """Get singleton scheduler."""
    global _scheduler
    if _scheduler is None:
        _scheduler = PriceAggregationScheduler()
    return _scheduler


def start_price_scheduler() -> PriceAggregationScheduler:
    """Start the price aggregation scheduler."""
    scheduler = get_price_scheduler()
    if not scheduler.is_running():
        scheduler.start()
    return scheduler


def stop_price_scheduler() -> None:
    """Stop the price aggregation scheduler."""
    scheduler = get_price_scheduler()
    scheduler.stop()
