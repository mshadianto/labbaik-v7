"""
LABBAIK AI v7.5 - Price Cache Manager
======================================
Multi-level caching for aggregated prices.
"""

import logging
import hashlib
import json
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import OrderedDict
import threading

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Single cache entry."""
    key: str
    value: Any
    created_at: datetime
    expires_at: datetime
    hits: int = 0


class PriceCacheManager:
    """
    In-memory cache for aggregated prices with TTL support.
    Uses LRU eviction when capacity is reached.
    """

    DEFAULT_TTL_SECONDS = 300  # 5 minutes
    MAX_ENTRIES = 1000

    def __init__(
        self,
        default_ttl: int = DEFAULT_TTL_SECONDS,
        max_entries: int = MAX_ENTRIES
    ):
        self.default_ttl = default_ttl
        self.max_entries = max_entries
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.RLock()
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }

    def build_key(
        self,
        city: str = None,
        offer_type: str = None,
        check_in: Any = None,
        check_out: Any = None,
        min_price: float = None,
        max_price: float = None,
        min_stars: int = None,
        sources: List[str] = None,
        **kwargs
    ) -> str:
        """Build cache key from search parameters."""
        key_parts = [
            f"city:{city or 'all'}",
            f"type:{offer_type or 'all'}",
            f"checkin:{check_in or 'any'}",
            f"checkout:{check_out or 'any'}",
            f"price:{min_price or 0}-{max_price or 'max'}",
            f"stars:{min_stars or 0}+",
            f"sources:{','.join(sorted(sources)) if sources else 'all'}"
        ]

        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        Returns None if not found or expired.
        """
        with self._lock:
            entry = self._cache.get(key)

            if entry is None:
                self._stats["misses"] += 1
                return None

            # Check expiration
            if datetime.now() > entry.expires_at:
                del self._cache[key]
                self._stats["misses"] += 1
                return None

            # Move to end (most recently used)
            self._cache.move_to_end(key)
            entry.hits += 1
            self._stats["hits"] += 1

            return entry.value

    def set(
        self,
        key: str,
        value: Any,
        ttl: int = None
    ) -> None:
        """
        Set value in cache with TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: default_ttl)
        """
        ttl = ttl or self.default_ttl

        with self._lock:
            # Evict oldest if at capacity
            while len(self._cache) >= self.max_entries:
                self._cache.popitem(last=False)
                self._stats["evictions"] += 1

            now = datetime.now()
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=now,
                expires_at=now + timedelta(seconds=ttl)
            )
            self._cache[key] = entry

    def delete(self, key: str) -> bool:
        """Delete a specific key from cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def invalidate_all(self) -> int:
        """Clear all cache entries. Returns number of entries cleared."""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count

    def invalidate_by_pattern(self, pattern: str) -> int:
        """
        Invalidate all keys matching pattern.
        Pattern is a simple substring match on the original key params.
        """
        # Since we hash keys, we need to track original params
        # For now, just clear all - can be enhanced later
        return self.invalidate_all()

    def cleanup_expired(self) -> int:
        """Remove all expired entries. Returns count of removed entries."""
        with self._lock:
            now = datetime.now()
            expired_keys = [
                key for key, entry in self._cache.items()
                if now > entry.expires_at
            ]

            for key in expired_keys:
                del self._cache[key]

            return len(expired_keys)

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_requests = self._stats["hits"] + self._stats["misses"]
            hit_rate = (self._stats["hits"] / total_requests * 100) if total_requests > 0 else 0

            return {
                "entries": len(self._cache),
                "max_entries": self.max_entries,
                "hits": self._stats["hits"],
                "misses": self._stats["misses"],
                "evictions": self._stats["evictions"],
                "hit_rate": round(hit_rate, 2)
            }

    def get_entry_info(self, key: str) -> Optional[Dict[str, Any]]:
        """Get info about a specific cache entry."""
        with self._lock:
            entry = self._cache.get(key)
            if not entry:
                return None

            now = datetime.now()
            return {
                "key": key,
                "created_at": entry.created_at.isoformat(),
                "expires_at": entry.expires_at.isoformat(),
                "ttl_remaining": (entry.expires_at - now).total_seconds(),
                "hits": entry.hits,
                "expired": now > entry.expires_at
            }


class SourceCacheManager:
    """
    Specialized cache for source-specific data.
    Maintains separate caches per data source with different TTLs.
    """

    # Default TTLs per source (seconds)
    SOURCE_TTLS = {
        "amadeus": 7200,     # 2 hours (API rate limited)
        "xotelo": 3600,      # 1 hour
        "makcorps": 7200,    # 2 hours (low quota)
        "traveloka": 21600,  # 6 hours (scraped)
        "tiket": 21600,      # 6 hours (scraped)
        "pegipegi": 21600,   # 6 hours (scraped)
        "partner": 3600,     # 1 hour (fresh from partners)
        "demo": 86400,       # 24 hours (static)
    }

    def __init__(self):
        self._caches: Dict[str, PriceCacheManager] = {}

    def get_cache(self, source: str) -> PriceCacheManager:
        """Get or create cache for a specific source."""
        if source not in self._caches:
            ttl = self.SOURCE_TTLS.get(source, 3600)
            self._caches[source] = PriceCacheManager(default_ttl=ttl)
        return self._caches[source]

    def get(self, source: str, key: str) -> Optional[Any]:
        """Get value from source-specific cache."""
        return self.get_cache(source).get(key)

    def set(self, source: str, key: str, value: Any) -> None:
        """Set value in source-specific cache."""
        self.get_cache(source).set(key, value)

    def invalidate_source(self, source: str) -> int:
        """Invalidate all entries for a specific source."""
        if source in self._caches:
            return self._caches[source].invalidate_all()
        return 0

    def get_all_stats(self) -> Dict[str, Dict]:
        """Get stats for all source caches."""
        return {
            source: cache.get_stats()
            for source, cache in self._caches.items()
        }


# Singleton instances
_price_cache: Optional[PriceCacheManager] = None
_source_cache: Optional[SourceCacheManager] = None


def get_price_cache() -> PriceCacheManager:
    """Get singleton price cache."""
    global _price_cache
    if _price_cache is None:
        _price_cache = PriceCacheManager()
    return _price_cache


def get_source_cache() -> SourceCacheManager:
    """Get singleton source cache."""
    global _source_cache
    if _source_cache is None:
        _source_cache = SourceCacheManager()
    return _source_cache
