"""
LABBAIK AI v7.5 - Rate Limiter for Scrapers
============================================
Respectful rate limiting for OTA scraping.
"""

import time
import threading
from typing import Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class RateLimitConfig:
    """Rate limit configuration per source."""
    requests_per_minute: int = 5
    requests_per_hour: int = 100
    min_delay_seconds: float = 2.0
    max_delay_seconds: float = 10.0
    backoff_factor: float = 2.0
    max_retries: int = 3


@dataclass
class RateLimitState:
    """Current rate limit state for a source."""
    request_times: list = field(default_factory=list)
    last_request: Optional[datetime] = None
    consecutive_failures: int = 0
    is_blocked: bool = False
    blocked_until: Optional[datetime] = None


class RateLimiter:
    """
    Rate limiter that respects source-specific limits.

    Features:
    - Per-minute and per-hour limits
    - Exponential backoff on failures
    - Automatic blocking on repeated failures
    - Thread-safe
    """

    DEFAULT_CONFIG = RateLimitConfig(
        requests_per_minute=5,
        requests_per_hour=100,
        min_delay_seconds=2.0,
        max_delay_seconds=10.0,
        backoff_factor=2.0,
        max_retries=3
    )

    # Source-specific configurations
    SOURCE_CONFIGS = {
        "traveloka": RateLimitConfig(
            requests_per_minute=5,
            requests_per_hour=60,
            min_delay_seconds=3.0,
            max_delay_seconds=15.0
        ),
        "tiket": RateLimitConfig(
            requests_per_minute=5,
            requests_per_hour=60,
            min_delay_seconds=3.0,
            max_delay_seconds=15.0
        ),
        "pegipegi": RateLimitConfig(
            requests_per_minute=5,
            requests_per_hour=60,
            min_delay_seconds=3.0,
            max_delay_seconds=15.0
        ),
    }

    def __init__(self):
        self._states: Dict[str, RateLimitState] = {}
        self._lock = threading.RLock()

    def get_config(self, source: str) -> RateLimitConfig:
        """Get rate limit config for a source."""
        return self.SOURCE_CONFIGS.get(source, self.DEFAULT_CONFIG)

    def _get_state(self, source: str) -> RateLimitState:
        """Get or create state for a source."""
        if source not in self._states:
            self._states[source] = RateLimitState()
        return self._states[source]

    def can_request(self, source: str) -> bool:
        """Check if a request can be made to source."""
        with self._lock:
            state = self._get_state(source)
            config = self.get_config(source)

            # Check if blocked
            if state.is_blocked:
                if state.blocked_until and datetime.now() < state.blocked_until:
                    return False
                # Unblock if time has passed
                state.is_blocked = False
                state.blocked_until = None
                state.consecutive_failures = 0

            now = datetime.now()

            # Clean old request times
            one_hour_ago = now - timedelta(hours=1)
            state.request_times = [t for t in state.request_times if t > one_hour_ago]

            # Check per-hour limit
            if len(state.request_times) >= config.requests_per_hour:
                logger.warning(f"Rate limit: {source} hourly limit reached")
                return False

            # Check per-minute limit
            one_minute_ago = now - timedelta(minutes=1)
            recent_requests = [t for t in state.request_times if t > one_minute_ago]
            if len(recent_requests) >= config.requests_per_minute:
                logger.debug(f"Rate limit: {source} minute limit reached")
                return False

            return True

    def wait_if_needed(self, source: str) -> float:
        """
        Wait if needed before making request.
        Returns the actual wait time in seconds.
        """
        with self._lock:
            state = self._get_state(source)
            config = self.get_config(source)

            if not self.can_request(source):
                # Calculate wait time
                if state.is_blocked and state.blocked_until:
                    wait_seconds = (state.blocked_until - datetime.now()).total_seconds()
                    if wait_seconds > 0:
                        logger.info(f"Waiting {wait_seconds:.1f}s for {source} unblock")
                        time.sleep(wait_seconds)
                        return wait_seconds
                else:
                    # Wait for rate limit reset
                    wait_seconds = config.min_delay_seconds * (state.consecutive_failures + 1)
                    wait_seconds = min(wait_seconds, config.max_delay_seconds)
                    logger.debug(f"Rate limiting: waiting {wait_seconds:.1f}s for {source}")
                    time.sleep(wait_seconds)
                    return wait_seconds

            # Minimum delay between requests
            if state.last_request:
                elapsed = (datetime.now() - state.last_request).total_seconds()
                if elapsed < config.min_delay_seconds:
                    wait_time = config.min_delay_seconds - elapsed
                    time.sleep(wait_time)
                    return wait_time

            return 0.0

    def record_request(self, source: str) -> None:
        """Record a request was made."""
        with self._lock:
            state = self._get_state(source)
            now = datetime.now()
            state.request_times.append(now)
            state.last_request = now

    def record_success(self, source: str) -> None:
        """Record successful request."""
        with self._lock:
            state = self._get_state(source)
            state.consecutive_failures = 0

    def record_failure(self, source: str) -> None:
        """Record failed request with backoff."""
        with self._lock:
            state = self._get_state(source)
            config = self.get_config(source)

            state.consecutive_failures += 1

            if state.consecutive_failures >= config.max_retries:
                # Block source temporarily
                backoff_minutes = min(60, 5 * (2 ** (state.consecutive_failures - config.max_retries)))
                state.is_blocked = True
                state.blocked_until = datetime.now() + timedelta(minutes=backoff_minutes)
                logger.warning(
                    f"Rate limit: {source} blocked for {backoff_minutes} minutes "
                    f"after {state.consecutive_failures} failures"
                )

    def get_delay(self, source: str) -> float:
        """Get recommended delay before next request."""
        with self._lock:
            state = self._get_state(source)
            config = self.get_config(source)

            # Base delay
            delay = config.min_delay_seconds

            # Add backoff for failures
            if state.consecutive_failures > 0:
                delay *= (config.backoff_factor ** state.consecutive_failures)

            return min(delay, config.max_delay_seconds)

    def is_blocked(self, source: str) -> bool:
        """Check if source is currently blocked."""
        with self._lock:
            state = self._get_state(source)
            if not state.is_blocked:
                return False
            if state.blocked_until and datetime.now() >= state.blocked_until:
                state.is_blocked = False
                state.blocked_until = None
                return False
            return True

    def get_stats(self, source: str = None) -> Dict:
        """Get rate limiting statistics."""
        with self._lock:
            if source:
                state = self._get_state(source)
                config = self.get_config(source)
                now = datetime.now()

                one_minute_ago = now - timedelta(minutes=1)
                recent = len([t for t in state.request_times if t > one_minute_ago])

                return {
                    "source": source,
                    "requests_last_minute": recent,
                    "requests_last_hour": len(state.request_times),
                    "consecutive_failures": state.consecutive_failures,
                    "is_blocked": state.is_blocked,
                    "blocked_until": state.blocked_until.isoformat() if state.blocked_until else None,
                    "limits": {
                        "per_minute": config.requests_per_minute,
                        "per_hour": config.requests_per_hour
                    }
                }
            else:
                return {
                    source: self.get_stats(source)
                    for source in self._states.keys()
                }

    def reset(self, source: str = None) -> None:
        """Reset rate limiter state."""
        with self._lock:
            if source:
                if source in self._states:
                    del self._states[source]
            else:
                self._states.clear()


# Singleton
_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Get singleton rate limiter."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter
