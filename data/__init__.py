"""
LABBAIK AI v6.0 - Data Package
==============================
Data models, schemas, and knowledge base.
"""

from data.models import (
    # Base
    BaseEntity,
    TimestampMixin,
    
    # User
    User,
    UserRole,
    SubscriptionTier,
    UserCreate,
    UserUpdate,
    UserSession,
    
    # Chat
    ChatMessage,
    ChatConversation,
    MessageRole,
    
    # Booking
    Booking,
    BookingCreate,
    BookingStatus,
    TravelerInfo,
    FlightInfo,
    HotelInfo,
    HotelStarRating,
    PackageType,
    
    # Cost
    CostSimulationInput,
    CostBreakdown,
    CostSimulationResult,
    
    # Partner
    Partner,
    PartnerType,
    PartnerStatus,
    
    # Subscription
    SubscriptionPlan,
    UserSubscription,
    
    # Notification
    Notification,
    NotificationType,
)

# Knowledge base
try:
    from data.knowledge.umrah_guide import (
        get_all_guides,
        get_arabic_phrases,
        get_faq,
        get_packing_list,
        search_knowledge,
        ARABIC_PHRASES,
        FAQ_DATA,
        PACKING_LIST,
    )
except ImportError:
    # Knowledge base may not be loaded yet
    get_all_guides = None
    get_arabic_phrases = None
    get_faq = None
    get_packing_list = None
    search_knowledge = None

__all__ = [
    # Base
    "BaseEntity",
    "TimestampMixin",
    
    # User
    "User",
    "UserRole",
    "SubscriptionTier",
    "UserCreate",
    "UserUpdate",
    "UserSession",
    
    # Chat
    "ChatMessage",
    "ChatConversation",
    "MessageRole",
    
    # Booking
    "Booking",
    "BookingCreate",
    "BookingStatus",
    "TravelerInfo",
    "FlightInfo",
    "HotelInfo",
    "HotelStarRating",
    "PackageType",
    
    # Cost
    "CostSimulationInput",
    "CostBreakdown",
    "CostSimulationResult",
    
    # Partner
    "Partner",
    "PartnerType",
    "PartnerStatus",
    
    # Subscription
    "SubscriptionPlan",
    "UserSubscription",
    
    # Notification
    "Notification",
    "NotificationType",
    
    # Knowledge
    "get_all_guides",
    "get_arabic_phrases",
    "get_faq",
    "get_packing_list",
    "search_knowledge",
]
