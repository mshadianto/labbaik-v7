"""
LABBAIK AI - Optimized Database Service
========================================
Cost-optimized database operations for Neon free tier.
Implements caching, batching, and demo mode fallback.
"""

import os
import time
import logging
import hashlib
from typing import Optional, List, Dict, Any, Callable
from functools import wraps
from datetime import datetime, timedelta
from collections import OrderedDict
import threading

logger = logging.getLogger(__name__)


# =============================================================================
# QUERY CACHE
# =============================================================================

class QueryCache:
    """Thread-safe LRU cache for database queries."""

    def __init__(self, max_size: int = 500, default_ttl: int = 300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict = OrderedDict()
        self._lock = threading.RLock()
        self._stats = {"hits": 0, "misses": 0}

    def _make_key(self, query: str, params: tuple = None) -> str:
        """Create cache key from query and params."""
        key_str = f"{query}:{params}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, query: str, params: tuple = None) -> Optional[Any]:
        """Get cached result."""
        key = self._make_key(query, params)

        with self._lock:
            if key not in self._cache:
                self._stats["misses"] += 1
                return None

            entry = self._cache[key]
            if datetime.now() > entry["expires"]:
                del self._cache[key]
                self._stats["misses"] += 1
                return None

            self._cache.move_to_end(key)
            self._stats["hits"] += 1
            return entry["value"]

    def set(self, query: str, params: tuple, value: Any, ttl: int = None):
        """Cache query result."""
        key = self._make_key(query, params)
        ttl = ttl or self.default_ttl

        with self._lock:
            while len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)

            self._cache[key] = {
                "value": value,
                "expires": datetime.now() + timedelta(seconds=ttl)
            }

    def invalidate(self, pattern: str = None):
        """Invalidate cache entries."""
        with self._lock:
            if pattern is None:
                self._cache.clear()
            # Pattern matching would need original query storage

    @property
    def hit_rate(self) -> float:
        total = self._stats["hits"] + self._stats["misses"]
        return (self._stats["hits"] / total * 100) if total > 0 else 0


# Singleton cache instance
_query_cache: Optional[QueryCache] = None

def get_query_cache() -> QueryCache:
    global _query_cache
    if _query_cache is None:
        _query_cache = QueryCache()
    return _query_cache


# =============================================================================
# CACHING DECORATORS
# =============================================================================

def cached_query(ttl: int = 300, cache_key: str = None):
    """
    Decorator to cache database query results.

    Usage:
        @cached_query(ttl=3600)
        def get_packages(city: str):
            return db.fetch_all("SELECT * FROM packages WHERE city = %s", (city,))
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_query_cache()

            # Build cache key from function name and args
            key_parts = [func.__name__] + [str(a) for a in args]
            key_parts += [f"{k}={v}" for k, v in sorted(kwargs.items())]
            key = "|".join(key_parts)

            # Try cache first
            cached = cache.get(key, None)
            if cached is not None:
                logger.debug(f"Cache hit: {func.__name__}")
                return cached

            # Execute query
            result = func(*args, **kwargs)

            # Cache result
            cache.set(key, None, result, ttl)

            return result
        return wrapper
    return decorator


def demo_fallback(demo_func: Callable):
    """
    Decorator to fallback to demo data when USE_DEMO_MODE is enabled.

    Usage:
        @demo_fallback(lambda city: load_demo_hotels(city))
        def get_hotels(city: str):
            return db.fetch_all("SELECT * FROM hotels WHERE city = %s", (city,))
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check demo mode
            if os.getenv("USE_DEMO_MODE", "").lower() == "true":
                logger.info(f"Demo mode: {func.__name__}")
                return demo_func(*args, **kwargs)

            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"DB error, falling back to demo: {e}")
                return demo_func(*args, **kwargs)

        return wrapper
    return decorator


# =============================================================================
# OPTIMIZED DATABASE WRAPPER
# =============================================================================

class OptimizedDB:
    """
    Database wrapper with compute-saving optimizations.

    Features:
    - Query caching with TTL
    - Slow query logging
    - Connection reuse
    - Demo mode fallback
    """

    SLOW_QUERY_THRESHOLD = 1.0  # seconds

    def __init__(self, db=None):
        self._db = db
        self._cache = get_query_cache()
        self._slow_queries: List[Dict] = []

    @property
    def db(self):
        """Lazy load database connection."""
        if self._db is None:
            from services.database import get_db
            self._db = get_db()
        return self._db

    def fetch_cached(
        self,
        query: str,
        params: tuple = None,
        ttl: int = 300,
        force_refresh: bool = False
    ) -> List[Dict]:
        """
        Fetch with automatic caching.

        Args:
            query: SQL query
            params: Query parameters
            ttl: Cache TTL in seconds
            force_refresh: Bypass cache
        """
        if not force_refresh:
            cached = self._cache.get(query, params)
            if cached is not None:
                return cached

        # Execute with timing
        start = time.time()
        result = self.db.fetch_all(query, params)
        elapsed = time.time() - start

        # Log slow queries
        if elapsed > self.SLOW_QUERY_THRESHOLD:
            self._log_slow_query(query, params, elapsed)

        # Cache result
        self._cache.set(query, params, result, ttl)

        return result

    def fetch_one_cached(
        self,
        query: str,
        params: tuple = None,
        ttl: int = 300
    ) -> Optional[Dict]:
        """Fetch single row with caching."""
        cached = self._cache.get(query, params)
        if cached is not None:
            return cached[0] if cached else None

        result = self.db.fetch_one(query, params)
        self._cache.set(query, params, [result] if result else [], ttl)

        return result

    def _log_slow_query(self, query: str, params: tuple, elapsed: float):
        """Log slow query for analysis."""
        entry = {
            "query": query[:200],
            "params": str(params)[:100] if params else None,
            "elapsed": round(elapsed, 3),
            "timestamp": datetime.now().isoformat()
        }
        self._slow_queries.append(entry)

        # Keep only last 100 slow queries
        if len(self._slow_queries) > 100:
            self._slow_queries = self._slow_queries[-100:]

        logger.warning(f"Slow query ({elapsed:.2f}s): {query[:100]}...")

    def get_slow_queries(self) -> List[Dict]:
        """Get list of slow queries for debugging."""
        return self._slow_queries.copy()

    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        return {
            "hit_rate": round(self._cache.hit_rate, 2),
            "hits": self._cache._stats["hits"],
            "misses": self._cache._stats["misses"],
            "size": len(self._cache._cache)
        }

    def invalidate_cache(self):
        """Clear all cached queries."""
        self._cache.invalidate()


# =============================================================================
# BATCH QUERY HELPERS
# =============================================================================

def batch_fetch(
    db,
    ids: List[str],
    query_template: str,
    batch_size: int = 100
) -> List[Dict]:
    """
    Fetch records in batches to avoid large IN clauses.

    Usage:
        results = batch_fetch(
            db,
            package_ids,
            "SELECT * FROM packages WHERE id = ANY(%s)",
            batch_size=50
        )
    """
    results = []

    for i in range(0, len(ids), batch_size):
        batch = ids[i:i + batch_size]
        batch_results = db.fetch_all(query_template, (batch,))
        results.extend(batch_results)

    return results


# =============================================================================
# COMPUTE BUDGET CHECKER
# =============================================================================

class ComputeBudget:
    """
    Track and limit database compute usage.
    """

    def __init__(self, daily_limit: int = 1000):
        self.daily_limit = daily_limit
        self._query_count = 0
        self._last_reset = datetime.now().date()

    def _check_reset(self):
        """Reset counter if new day."""
        today = datetime.now().date()
        if today > self._last_reset:
            self._query_count = 0
            self._last_reset = today

    def can_query(self) -> bool:
        """Check if we're within budget."""
        self._check_reset()
        return self._query_count < self.daily_limit

    def record_query(self):
        """Record a query execution."""
        self._check_reset()
        self._query_count += 1

    @property
    def remaining(self) -> int:
        """Get remaining queries for today."""
        self._check_reset()
        return max(0, self.daily_limit - self._query_count)

    @property
    def usage_percent(self) -> float:
        """Get usage percentage."""
        self._check_reset()
        return (self._query_count / self.daily_limit) * 100


# Singleton
_compute_budget: Optional[ComputeBudget] = None

def get_compute_budget() -> ComputeBudget:
    global _compute_budget
    if _compute_budget is None:
        _compute_budget = ComputeBudget()
    return _compute_budget


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "QueryCache",
    "get_query_cache",
    "cached_query",
    "demo_fallback",
    "OptimizedDB",
    "batch_fetch",
    "ComputeBudget",
    "get_compute_budget",
]
