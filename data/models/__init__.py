"""
LABBAIK AI v6.0 - Data Models
============================
Pydantic models for data validation and serialization.
"""

from __future__ import annotations
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict
import uuid


# =============================================================================
# BASE MODELS
# =============================================================================

class BaseEntity(BaseModel):
    """Base model with common fields."""
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        populate_by_name=True
    )
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# USER MODELS
# =============================================================================

class UserRole(str, Enum):
    """User roles."""
    GUEST = "guest"
    USER = "user"
    PREMIUM = "premium"
    PARTNER = "partner"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class SubscriptionTier(str, Enum):
    """Subscription tiers."""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9]{10,15}$")
    
    @validator("name")
    def validate_name(cls, v):
        return v.strip().title()


class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str = Field(..., min_length=8)
    
    @validator("password")
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Model for updating user."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9]{10,15}$")
    avatar_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class User(UserBase, BaseEntity):
    """Full user model."""
    role: UserRole = UserRole.USER
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    avatar_url: Optional[str] = None
    is_verified: bool = False
    is_active: bool = True
    last_login: Optional[datetime] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)
    
    # Gamification
    points: int = 0
    level: int = 1
    badges: List[str] = Field(default_factory=list)
    
    def has_permission(self, required_role: UserRole) -> bool:
        """Check if user has required role or higher."""
        role_hierarchy = [
            UserRole.GUEST, UserRole.USER, UserRole.PREMIUM,
            UserRole.PARTNER, UserRole.ADMIN, UserRole.SUPERADMIN
        ]
        return role_hierarchy.index(self.role) >= role_hierarchy.index(required_role)


class UserSession(BaseModel):
    """User session model."""
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# CHAT MODELS
# =============================================================================

class MessageRole(str, Enum):
    """Chat message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Single chat message."""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def to_api_format(self) -> Dict[str, str]:
        """Convert to API format."""
        return {"role": self.role.value, "content": self.content}


class ChatConversation(BaseEntity):
    """Chat conversation container."""
    user_id: str
    title: Optional[str] = None
    messages: List[ChatMessage] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    is_archived: bool = False
    
    def add_message(self, role: MessageRole, content: str) -> ChatMessage:
        """Add a message to the conversation."""
        message = ChatMessage(role=role, content=content)
        self.messages.append(message)
        self.update_timestamp()
        return message
    
    def get_context_messages(self, max_messages: int = 10) -> List[ChatMessage]:
        """Get recent messages for context."""
        return self.messages[-max_messages:]
    
    @property
    def message_count(self) -> int:
        """Get total message count."""
        return len(self.messages)


# =============================================================================
# BOOKING MODELS
# =============================================================================

class BookingStatus(str, Enum):
    """Booking status."""
    DRAFT = "draft"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PAID = "paid"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    REFUNDED = "refunded"


class HotelStarRating(int, Enum):
    """Hotel star ratings."""
    BUDGET = 2
    STANDARD = 3
    SUPERIOR = 4
    DELUXE = 5


class PackageType(str, Enum):
    """Umrah package types."""
    REGULER = "reguler"
    PLUS = "plus"
    VIP = "vip"
    BACKPACKER = "backpacker"
    MANDIRI = "mandiri"


class TravelerInfo(BaseModel):
    """Traveler information."""
    name: str = Field(..., min_length=2, max_length=100)
    passport_number: Optional[str] = None
    passport_expiry: Optional[date] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = Field(None, pattern=r"^(male|female)$")
    nationality: str = "ID"
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    special_needs: Optional[str] = None
    
    @validator("passport_expiry")
    def validate_passport_expiry(cls, v):
        if v and v < date.today():
            raise ValueError("Passport has expired")
        return v


class FlightInfo(BaseModel):
    """Flight information."""
    airline: str
    flight_number: str
    departure_city: str
    departure_airport: str
    departure_time: datetime
    arrival_city: str
    arrival_airport: str
    arrival_time: datetime
    class_type: str = "economy"


class HotelInfo(BaseModel):
    """Hotel information."""
    name: str
    city: str  # makkah or madinah
    star_rating: HotelStarRating
    address: Optional[str] = None
    distance_to_haram: Optional[str] = None
    check_in: date
    check_out: date
    room_type: str = "standard"
    
    @property
    def nights(self) -> int:
        """Calculate number of nights."""
        return (self.check_out - self.check_in).days


class BookingCreate(BaseModel):
    """Model for creating a booking."""
    user_id: str
    partner_id: Optional[str] = None
    package_type: PackageType
    departure_city: str
    departure_date: date
    return_date: date
    travelers: List[TravelerInfo]
    hotel_makkah: Optional[HotelInfo] = None
    hotel_madinah: Optional[HotelInfo] = None
    notes: Optional[str] = None
    
    @validator("return_date")
    def validate_return_date(cls, v, values):
        if "departure_date" in values and v <= values["departure_date"]:
            raise ValueError("Return date must be after departure date")
        return v
    
    @property
    def total_days(self) -> int:
        """Calculate total trip days."""
        return (self.return_date - self.departure_date).days


class Booking(BookingCreate, BaseEntity):
    """Full booking model."""
    booking_number: str = Field(default_factory=lambda: f"LBK-{uuid.uuid4().hex[:8].upper()}")
    status: BookingStatus = BookingStatus.DRAFT
    
    # Pricing
    base_price: float = 0
    taxes: float = 0
    fees: float = 0
    discount: float = 0
    total_price: float = 0
    currency: str = "IDR"
    
    # Flight details
    outbound_flight: Optional[FlightInfo] = None
    return_flight: Optional[FlightInfo] = None
    
    # Payment
    paid_amount: float = 0
    payment_status: str = "unpaid"
    
    # Timestamps
    confirmed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    
    def calculate_total(self):
        """Calculate total price."""
        self.total_price = self.base_price + self.taxes + self.fees - self.discount
    
    @property
    def traveler_count(self) -> int:
        """Get number of travelers."""
        return len(self.travelers)
    
    @property
    def balance_due(self) -> float:
        """Get remaining balance."""
        return self.total_price - self.paid_amount


# =============================================================================
# COST SIMULATION MODELS
# =============================================================================

class CostSimulationInput(BaseModel):
    """Input for cost simulation."""
    departure_city: str
    departure_date: date
    return_date: date
    traveler_count: int = Field(..., ge=1, le=50)
    hotel_makkah_star: HotelStarRating = HotelStarRating.STANDARD
    hotel_madinah_star: HotelStarRating = HotelStarRating.STANDARD
    days_makkah: int = Field(..., ge=1)
    days_madinah: int = Field(..., ge=1)
    package_type: PackageType = PackageType.REGULER
    include_visa: bool = True
    include_insurance: bool = True
    include_mutawif: bool = True
    
    @property
    def total_days(self) -> int:
        return (self.return_date - self.departure_date).days


class CostBreakdown(BaseModel):
    """Cost breakdown details."""
    flight_cost: float
    hotel_makkah_cost: float
    hotel_madinah_cost: float
    visa_cost: float
    insurance_cost: float
    mutawif_cost: float
    handling_fee: float
    other_costs: float = 0
    
    @property
    def subtotal(self) -> float:
        return (
            self.flight_cost +
            self.hotel_makkah_cost +
            self.hotel_madinah_cost +
            self.visa_cost +
            self.insurance_cost +
            self.mutawif_cost +
            self.handling_fee +
            self.other_costs
        )


class CostSimulationResult(BaseModel):
    """Cost simulation result."""
    input: CostSimulationInput
    breakdown: CostBreakdown
    total_per_person: float
    total_all: float
    currency: str = "IDR"
    seasonal_multiplier: float = 1.0
    season_type: str = "regular"
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    notes: List[str] = Field(default_factory=list)
    disclaimer: str = ""


# =============================================================================
# PARTNER MODELS
# =============================================================================

class PartnerType(str, Enum):
    """Partner types."""
    TRAVEL_AGENT = "travel_agent"
    HOTEL = "hotel"
    AIRLINE = "airline"
    TRANSPORT = "transport"
    GUIDE = "guide"


class PartnerStatus(str, Enum):
    """Partner status."""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


class Partner(BaseEntity):
    """Partner model."""
    name: str
    type: PartnerType
    status: PartnerStatus = PartnerStatus.PENDING
    
    # Contact
    email: EmailStr
    phone: str
    website: Optional[str] = None
    
    # Business info
    company_name: str
    license_number: Optional[str] = None
    address: str
    city: str
    
    # Commission
    commission_rate: float = Field(default=0.1, ge=0, le=1)  # 0-100%
    
    # Stats
    total_bookings: int = 0
    total_revenue: float = 0
    rating: float = Field(default=0, ge=0, le=5)
    review_count: int = 0


# =============================================================================
# SUBSCRIPTION MODELS
# =============================================================================

class SubscriptionPlan(BaseModel):
    """Subscription plan model."""
    id: str
    name: str
    tier: SubscriptionTier
    price_monthly: float
    price_yearly: float
    currency: str = "IDR"
    features: List[str]
    limits: Dict[str, int]
    is_active: bool = True


class UserSubscription(BaseEntity):
    """User subscription model."""
    user_id: str
    plan_id: str
    tier: SubscriptionTier
    status: str = "active"
    billing_cycle: str = "monthly"
    price: float
    currency: str = "IDR"
    starts_at: datetime
    expires_at: datetime
    auto_renew: bool = True
    
    @property
    def is_active(self) -> bool:
        return self.status == "active" and self.expires_at > datetime.utcnow()
    
    @property
    def days_remaining(self) -> int:
        if self.expires_at < datetime.utcnow():
            return 0
        return (self.expires_at - datetime.utcnow()).days


# =============================================================================
# NOTIFICATION MODELS
# =============================================================================

class NotificationType(str, Enum):
    """Notification types."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    BOOKING = "booking"
    PAYMENT = "payment"
    PROMOTION = "promotion"


class Notification(BaseEntity):
    """Notification model."""
    user_id: str
    type: NotificationType
    title: str
    message: str
    link: Optional[str] = None
    is_read: bool = False
    read_at: Optional[datetime] = None
    
    def mark_read(self):
        self.is_read = True
        self.read_at = datetime.utcnow()
