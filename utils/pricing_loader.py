"""
LABBAIK AI - Pricing Configuration Loader
==========================================
Reads pricing data from config/pricing.yaml (Single Source of Truth).
Provides utilities for batch detection and pricing display.
"""

import os
import yaml
import logging
from datetime import datetime, date
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from functools import lru_cache

logger = logging.getLogger(__name__)

# Path to pricing config
CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "config",
    "pricing.yaml"
)


@dataclass
class BatchInfo:
    """Batch information dataclass for type safety."""
    id: str
    name: str
    tagline: str
    day_start: int
    day_end: Optional[int]
    max_partners: Optional[int]
    setup_fee: int
    setup_fee_display: str
    status: str
    status_duration_months: Optional[int]
    commission_rate: float
    commission_display: str
    commission_locked: bool
    setup_type: str
    setup_type_display: str
    benefits: List[str]
    highlight: bool
    badge_color: str

    @property
    def is_lifetime(self) -> bool:
        return self.status_duration_months is None

    @property
    def is_free(self) -> bool:
        return self.setup_fee == 0


@lru_cache(maxsize=1)
def _load_pricing_yaml() -> Dict[str, Any]:
    """Load and cache pricing YAML file."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Pricing config not found: {CONFIG_PATH}")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Error parsing pricing YAML: {e}")
        return {}


def reload_pricing_config():
    """Force reload pricing config (clears cache)."""
    _load_pricing_yaml.cache_clear()


def get_pricing_config() -> Dict[str, Any]:
    """Get full pricing configuration."""
    return _load_pricing_yaml()


def get_pioneer_config() -> Dict[str, Any]:
    """Get Pioneer 2026 program configuration."""
    config = get_pricing_config()
    return config.get("pioneer_2026", {})


def get_program_start_date() -> date:
    """Get program start date."""
    config = get_pioneer_config()
    start_str = config.get("start_date", "2025-01-01")
    return datetime.strptime(start_str, "%Y-%m-%d").date()


def get_current_day() -> int:
    """Get current day number since program start."""
    start = get_program_start_date()
    today = date.today()
    delta = today - start
    return max(0, delta.days)


def get_all_batches() -> List[BatchInfo]:
    """Get all batch configurations as BatchInfo objects."""
    config = get_pioneer_config()
    batches_config = config.get("batches", {})

    batches = []
    for batch_id, batch_data in batches_config.items():
        try:
            batch = BatchInfo(
                id=batch_id,
                name=batch_data.get("name", ""),
                tagline=batch_data.get("tagline", ""),
                day_start=batch_data.get("day_start", 0),
                day_end=batch_data.get("day_end"),
                max_partners=batch_data.get("max_partners"),
                setup_fee=batch_data.get("setup_fee", 0),
                setup_fee_display=batch_data.get("setup_fee_display", ""),
                status=batch_data.get("status", ""),
                status_duration_months=batch_data.get("status_duration_months"),
                commission_rate=batch_data.get("commission_rate", 0.0),
                commission_display=batch_data.get("commission_display", ""),
                commission_locked=batch_data.get("commission_locked", False),
                setup_type=batch_data.get("setup_type", "self_service"),
                setup_type_display=batch_data.get("setup_type_display", ""),
                benefits=batch_data.get("benefits", []),
                highlight=batch_data.get("highlight", False),
                badge_color=batch_data.get("badge_color", "#888888"),
            )
            batches.append(batch)
        except Exception as e:
            logger.error(f"Error parsing batch {batch_id}: {e}")

    # Sort by day_start
    batches.sort(key=lambda b: b.day_start)
    return batches


def get_batch_by_name(batch_id: str) -> Optional[BatchInfo]:
    """Get specific batch by ID (e.g., 'batch_1')."""
    batches = get_all_batches()
    for batch in batches:
        if batch.id == batch_id:
            return batch
    return None


def get_current_batch() -> Optional[BatchInfo]:
    """Get the currently active batch based on today's date."""
    current_day = get_current_day()
    batches = get_all_batches()

    for batch in batches:
        day_end = batch.day_end if batch.day_end is not None else float('inf')
        if batch.day_start <= current_day <= day_end:
            return batch

    # If past all batches, return the last one
    if batches:
        return batches[-1]

    return None


def get_batch_for_day(day: int) -> Optional[BatchInfo]:
    """Get batch for a specific day number."""
    batches = get_all_batches()

    for batch in batches:
        day_end = batch.day_end if batch.day_end is not None else float('inf')
        if batch.day_start <= day <= day_end:
            return batch

    return None


def get_faq() -> List[Dict[str, str]]:
    """Get FAQ list for partnership page."""
    config = get_pioneer_config()
    return config.get("faq", [])


def get_contact_info() -> Dict[str, str]:
    """Get contact information for partnership."""
    config = get_pioneer_config()
    return config.get("contact", {})


def format_currency(amount: int, currency: str = "Rp") -> str:
    """Format number as Indonesian currency."""
    if amount == 0:
        return "GRATIS"
    return f"{currency} {amount:,.0f}".replace(",", ".")


def get_batch_countdown(batch: BatchInfo) -> Optional[int]:
    """Get days remaining for a batch (None if ongoing)."""
    if batch.day_end is None:
        return None

    current_day = get_current_day()
    remaining = batch.day_end - current_day

    return max(0, remaining)


def is_batch_available(batch: BatchInfo, current_partners: int = 0) -> bool:
    """Check if a batch is still available for registration."""
    current_day = get_current_day()

    # Check day range
    day_end = batch.day_end if batch.day_end is not None else float('inf')
    if not (batch.day_start <= current_day <= day_end):
        return False

    # Check partner limit
    if batch.max_partners is not None:
        if current_partners >= batch.max_partners:
            return False

    return True
