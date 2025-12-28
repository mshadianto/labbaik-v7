"""
LABBAIK AI - CRM Models
========================
Dataclass models for CRM entities.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from enum import Enum


class LeadStatus(Enum):
    NEW = "new"
    CONTACTED = "contacted"
    INTERESTED = "interested"
    NEGOTIATING = "negotiating"
    WON = "won"
    LOST = "lost"


class LeadPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class BookingStatus(Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(Enum):
    PENDING = "pending"
    DP_PAID = "dp_paid"
    PARTIAL = "partial"
    PAID = "paid"
    REFUNDED = "refunded"


class DocumentStatus(Enum):
    PENDING = "pending"
    UPLOADED = "uploaded"
    VERIFIED = "verified"
    REJECTED = "rejected"


@dataclass
class Lead:
    """Lead/Prospek model."""
    id: Optional[str] = None
    name: str = ""
    phone: str = ""
    email: Optional[str] = None
    whatsapp: Optional[str] = None

    source: str = "direct"
    status: str = "new"
    priority: str = "medium"

    interested_package: Optional[str] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    preferred_month: Optional[str] = None
    group_size: int = 1

    notes: Optional[str] = None
    last_contact_date: Optional[datetime] = None
    next_followup_date: Optional[datetime] = None

    assigned_to: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Computed fields
    activities: List["LeadActivity"] = field(default_factory=list)


@dataclass
class LeadActivity:
    """Lead activity/follow-up model."""
    id: Optional[str] = None
    lead_id: str = ""

    activity_type: str = "note"  # call, whatsapp, email, meeting, note
    description: Optional[str] = None
    outcome: Optional[str] = None

    created_by: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Jamaah:
    """Jamaah/Customer model."""
    id: Optional[str] = None

    # Personal
    full_name: str = ""
    nik: Optional[str] = None
    passport_number: Optional[str] = None
    passport_expiry: Optional[date] = None

    # Contact
    phone: str = ""
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None

    # Demographics
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None

    # Emergency
    emergency_name: Optional[str] = None
    emergency_phone: Optional[str] = None
    emergency_relation: Optional[str] = None

    # Health
    health_notes: Optional[str] = None
    special_needs: Optional[str] = None

    # Travel
    umrah_count: int = 0
    last_umrah_date: Optional[date] = None

    referred_by: Optional[str] = None
    is_active: bool = True

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Relations
    documents: List["Document"] = field(default_factory=list)
    bookings: List["Booking"] = field(default_factory=list)


@dataclass
class Booking:
    """Booking model."""
    id: Optional[str] = None
    booking_code: str = ""

    lead_id: Optional[str] = None
    jamaah_id: Optional[str] = None

    # Package
    package_name: str = ""
    package_type: Optional[str] = None
    departure_date: Optional[date] = None
    return_date: Optional[date] = None
    duration_days: Optional[int] = None

    # Pricing
    package_price: int = 0
    discount_amount: int = 0
    discount_reason: Optional[str] = None
    total_price: int = 0

    # Payment
    payment_status: str = "pending"
    amount_paid: int = 0
    amount_remaining: Optional[int] = None

    # Status
    status: str = "draft"

    # Group
    group_code: Optional[str] = None
    room_type: Optional[str] = None
    roommate_preference: Optional[str] = None

    # Notes
    notes: Optional[str] = None
    internal_notes: Optional[str] = None

    # Staff
    created_by: Optional[str] = None
    confirmed_by: Optional[str] = None

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    # Relations
    payments: List["Payment"] = field(default_factory=list)
    jamaah: Optional["Jamaah"] = None


@dataclass
class Payment:
    """Payment model."""
    id: Optional[str] = None
    booking_id: str = ""

    payment_type: str = "dp"  # dp, installment, final, additional
    installment_number: Optional[int] = None

    amount: int = 0
    payment_method: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None

    status: str = "pending"

    proof_url: Optional[str] = None

    due_date: Optional[date] = None
    paid_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    confirmed_by: Optional[str] = None

    notes: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Document:
    """Document model."""
    id: Optional[str] = None
    jamaah_id: str = ""
    booking_id: Optional[str] = None

    doc_type: str = ""
    doc_name: Optional[str] = None
    file_url: Optional[str] = None

    status: str = "pending"
    rejection_reason: Optional[str] = None

    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None

    expiry_date: Optional[date] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Quote:
    """Quote/Penawaran model."""
    id: Optional[str] = None
    quote_number: str = ""

    lead_id: Optional[str] = None

    package_config: Dict[str, Any] = field(default_factory=dict)

    base_price: Optional[int] = None
    discount_amount: int = 0
    final_price: Optional[int] = None

    valid_until: Optional[date] = None

    status: str = "draft"  # draft, sent, viewed, accepted, rejected, expired

    created_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    viewed_at: Optional[datetime] = None
    responded_at: Optional[datetime] = None


@dataclass
class Invoice:
    """Invoice model."""
    id: Optional[str] = None
    invoice_number: str = ""

    booking_id: Optional[str] = None
    jamaah_id: Optional[str] = None

    invoice_type: str = "dp"  # dp, installment, final, full

    subtotal: Optional[int] = None
    discount: int = 0
    tax: int = 0
    total: int = 0

    status: str = "unpaid"

    due_date: Optional[date] = None
    paid_at: Optional[datetime] = None

    created_at: Optional[datetime] = None


@dataclass
class Broadcast:
    """WhatsApp Broadcast model."""
    id: Optional[str] = None

    name: str = ""
    message_template: str = ""

    target_type: Optional[str] = None
    target_filter: Dict[str, Any] = field(default_factory=dict)

    total_recipients: int = 0
    sent_count: int = 0
    delivered_count: int = 0
    read_count: int = 0
    failed_count: int = 0

    status: str = "draft"

    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    created_by: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class CompetitorPrice:
    """Competitor price model."""
    id: Optional[str] = None

    competitor_name: str = ""
    competitor_url: Optional[str] = None

    package_name: Optional[str] = None
    package_type: Optional[str] = None
    duration_days: Optional[int] = None
    hotel_makkah: Optional[str] = None
    hotel_madinah: Optional[str] = None
    airline: Optional[str] = None

    price: int = 0
    currency: str = "IDR"

    source: Optional[str] = None
    scraped_at: Optional[datetime] = None

    created_at: Optional[datetime] = None


@dataclass
class CRMStats:
    """CRM Statistics model."""
    # Leads
    total_leads: int = 0
    new_leads: int = 0
    leads_by_status: Dict[str, int] = field(default_factory=dict)
    leads_by_source: Dict[str, int] = field(default_factory=dict)

    # Conversion
    conversion_rate: float = 0.0

    # Bookings
    total_bookings: int = 0
    bookings_by_status: Dict[str, int] = field(default_factory=dict)

    # Revenue
    total_revenue: int = 0
    total_paid: int = 0
    total_pending: int = 0

    # Jamaah
    total_jamaah: int = 0

    # Period
    period_start: Optional[date] = None
    period_end: Optional[date] = None
