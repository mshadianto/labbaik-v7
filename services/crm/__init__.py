"""
LABBAIK AI - CRM Services
==========================
Services for Lead Management, Booking, Payments, and Operations.
"""

from .models import (
    Lead, LeadActivity, Jamaah, Booking, Payment,
    Document, Quote, Invoice, Broadcast, CompetitorPrice
)
from .repository import CRMRepository
from .config import get_crm_config
from .security import (
    validate_phone, validate_email, validate_nik, validate_passport,
    validate_uuid, escape_html, sanitize_for_display,
    ALLOWED_LEAD_COLUMNS, ALLOWED_JAMAAH_COLUMNS,
    ALLOWED_BOOKING_COLUMNS, ALLOWED_DOCUMENT_COLUMNS
)

__all__ = [
    "Lead", "LeadActivity", "Jamaah", "Booking", "Payment",
    "Document", "Quote", "Invoice", "Broadcast", "CompetitorPrice",
    "CRMRepository", "get_crm_config",
    # Security utilities
    "validate_phone", "validate_email", "validate_nik", "validate_passport",
    "validate_uuid", "escape_html", "sanitize_for_display",
    "ALLOWED_LEAD_COLUMNS", "ALLOWED_JAMAAH_COLUMNS",
    "ALLOWED_BOOKING_COLUMNS", "ALLOWED_DOCUMENT_COLUMNS"
]
