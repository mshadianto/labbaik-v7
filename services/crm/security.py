"""
LABBAIK AI - CRM Security Module
==================================
Input validation, sanitization, and security utilities.
"""

import re
import html
import logging
from typing import Optional, Dict, Any, Set

logger = logging.getLogger(__name__)

# =============================================================================
# WHITELISTED COLUMNS FOR DYNAMIC UPDATES (Prevent SQL Injection)
# =============================================================================

ALLOWED_LEAD_COLUMNS: Set[str] = {
    "name", "phone", "email", "whatsapp", "source", "status", "priority",
    "interested_package", "budget_min", "budget_max", "preferred_month",
    "group_size", "notes", "last_contact_date", "next_followup_date", "assigned_to"
}

ALLOWED_JAMAAH_COLUMNS: Set[str] = {
    "full_name", "nik", "passport_number", "passport_expiry",
    "phone", "whatsapp", "email", "address", "city", "province",
    "birth_date", "birth_place", "gender", "blood_type",
    "emergency_name", "emergency_phone", "emergency_relation",
    "health_notes", "special_needs", "umrah_count", "last_umrah_date",
    "referred_by", "is_active"
}

ALLOWED_BOOKING_COLUMNS: Set[str] = {
    "package_name", "package_type", "departure_date", "return_date",
    "duration_days", "package_price", "discount_amount", "discount_reason",
    "total_price", "payment_status", "amount_paid", "amount_remaining",
    "status", "group_code", "room_type", "roommate_preference",
    "notes", "internal_notes", "confirmed_by", "confirmed_at", "cancelled_at"
}

ALLOWED_DOCUMENT_COLUMNS: Set[str] = {
    "doc_type", "doc_name", "file_url", "status", "rejection_reason",
    "verified_by", "verified_at", "expiry_date"
}


def validate_column_names(updates: Dict[str, Any], allowed_columns: Set[str]) -> Dict[str, Any]:
    """
    Filter updates to only include whitelisted column names.
    Prevents SQL injection via dynamic column names.
    """
    safe_updates = {}
    for key, value in updates.items():
        if key in allowed_columns:
            safe_updates[key] = value
        else:
            logger.warning(f"Blocked unauthorized column update attempt: {key}")
    return safe_updates


# =============================================================================
# INPUT VALIDATION
# =============================================================================

def validate_phone(phone: str) -> Optional[str]:
    """Validate and normalize Indonesian phone number."""
    if not phone:
        return None

    # Remove spaces, dashes, and other characters
    cleaned = re.sub(r'[\s\-\.\(\)]', '', phone)

    # Check for valid Indonesian phone format
    # Accepts: 08xx, +628xx, 628xx
    pattern = r'^(\+62|62|0)8[1-9][0-9]{7,10}$'

    if re.match(pattern, cleaned):
        # Normalize to 08xx format
        if cleaned.startswith('+62'):
            return '0' + cleaned[3:]
        elif cleaned.startswith('62'):
            return '0' + cleaned[2:]
        return cleaned

    return None


def validate_email(email: str) -> Optional[str]:
    """Validate email format."""
    if not email:
        return None

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email.strip()):
        return email.strip().lower()

    return None


def validate_nik(nik: str) -> Optional[str]:
    """Validate Indonesian NIK (16 digits)."""
    if not nik:
        return None

    cleaned = re.sub(r'\D', '', nik)
    if len(cleaned) == 16:
        return cleaned

    return None


def validate_passport(passport: str) -> Optional[str]:
    """Validate passport number format."""
    if not passport:
        return None

    # Indonesian passport: 1 letter + 7 digits (e.g., A1234567)
    # Also accept other formats with alphanumeric 6-12 chars
    cleaned = re.sub(r'[\s\-]', '', passport.upper())
    pattern = r'^[A-Z0-9]{6,12}$'

    if re.match(pattern, cleaned):
        return cleaned

    return None


def validate_uuid(uuid_str: str) -> bool:
    """Validate UUID format."""
    if not uuid_str:
        return False

    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(pattern, uuid_str.lower()))


def validate_positive_integer(value: Any, max_value: int = None) -> Optional[int]:
    """Validate positive integer."""
    try:
        num = int(value)
        if num < 0:
            return None
        if max_value and num > max_value:
            return None
        return num
    except (TypeError, ValueError):
        return None


# =============================================================================
# XSS PREVENTION / HTML ESCAPING
# =============================================================================

def escape_html(text: str) -> str:
    """Escape HTML special characters to prevent XSS."""
    if text is None:
        return ""
    return html.escape(str(text))


def sanitize_for_display(text: str, max_length: int = 500) -> str:
    """Sanitize text for safe HTML display."""
    if text is None:
        return ""

    # Escape HTML
    safe_text = escape_html(str(text))

    # Truncate if too long
    if len(safe_text) > max_length:
        safe_text = safe_text[:max_length] + "..."

    return safe_text


def sanitize_dict_for_display(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize all string values in a dictionary for display."""
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_for_display(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict_for_display(value)
        else:
            sanitized[key] = value
    return sanitized


# =============================================================================
# RATE LIMITING (Simple in-memory implementation)
# =============================================================================

from datetime import datetime, timedelta
from collections import defaultdict

_rate_limit_store: Dict[str, list] = defaultdict(list)


def check_rate_limit(key: str, max_requests: int = 10, window_seconds: int = 60) -> bool:
    """
    Check if action is within rate limit.
    Returns True if allowed, False if rate limited.
    """
    now = datetime.now()
    window_start = now - timedelta(seconds=window_seconds)

    # Clean old entries
    _rate_limit_store[key] = [t for t in _rate_limit_store[key] if t > window_start]

    # Check limit
    if len(_rate_limit_store[key]) >= max_requests:
        logger.warning(f"Rate limit exceeded for key: {key}")
        return False

    # Record this request
    _rate_limit_store[key].append(now)
    return True


# =============================================================================
# LOGGING SANITIZATION
# =============================================================================

SENSITIVE_FIELDS = {"password", "token", "api_key", "secret", "nik", "passport_number"}


def sanitize_for_logging(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize sensitive data before logging."""
    sanitized = {}
    for key, value in data.items():
        if any(sensitive in key.lower() for sensitive in SENSITIVE_FIELDS):
            sanitized[key] = "***REDACTED***"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_for_logging(value)
        else:
            sanitized[key] = value
    return sanitized
