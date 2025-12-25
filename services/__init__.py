"""
LABBAIK AI v6.0 - Services Package
=================================
Business logic services.
"""

from services.ai.chat_service import (
    GroqChatService,
    OpenAIChatService,
    UnifiedChatService,
)
from services.ai.rag_service import (
    RAGService,
    LocalEmbeddingService,
    ChromaVectorStore,
)
from services.ai.base import (
    ChatMessage,
    ChatCompletionRequest,
    ChatCompletionResponse,
    AIServiceFactory,
)

# Database services
from services.database.repository import (
    DatabaseConnection,
    get_db,
    BaseRepository,
    UserRepository,
    ChatRepository,
    BookingRepository,
)

# Cost services
from services.cost.calculator import (
    calculate_umrah_cost,
    compare_packages,
    compare_seasons,
    get_season_type,
)

# ============================================
# PRICE INTELLIGENCE SERVICES (NEW)
# ============================================
try:
    from services.price.repository import (
        PriceRepository,
        PricePackage,
        PriceHotel,
        PriceFlight,
        get_price_repo,
        get_cached_packages,
        get_cached_hotels,
        get_cached_flights,
        get_cached_price_summary,
        get_cached_price_ranges,
        format_price_idr,
        format_duration,
    )
    from services.price.monitoring import (
        PriceMonitor,
        render_health_indicator,
        render_monitoring_dashboard,
        render_last_update_badge,
        get_cached_health_status,
    )
except ImportError:
    PriceRepository = None
    PricePackage = None
    PriceHotel = None
    PriceFlight = None
    get_price_repo = None
    get_cached_packages = None
    get_cached_hotels = None
    get_cached_flights = None
    get_cached_price_summary = None
    get_cached_price_ranges = None
    format_price_idr = None
    format_duration = None
    PriceMonitor = None
    render_health_indicator = None
    render_monitoring_dashboard = None
    render_last_update_badge = None
    get_cached_health_status = None

# Auth services - may not exist yet
try:
    from services.auth.auth_service import (
        AuthService,
        get_auth_service,
        PasswordService,
        TokenService,
        AuthResult,
    )
except ImportError:
    AuthService = None
    get_auth_service = None

# Notification services
try:
    from services.notification.notification_service import (
        NotificationService as NotifService,
        get_notification_service,
        EmailSender,
        NotificationMessage,
        NotificationResult,
    )
except ImportError:
    NotifService = None
    get_notification_service = None

# Data services (new centralized layer)
try:
    from services.data_service import (
        Database,
        DataStore,
        UserService,
        TripService,
        BookingService,
        ChatService,
        SimulationService,
        NotificationService,
        AnalyticsService,
        init_database,
        db,
        store,
    )
except ImportError:
    Database = None
    DataStore = None
    UserService = None
    TripService = None
    BookingService = None
    ChatService = None
    SimulationService = None
    NotificationService = None
    AnalyticsService = None
    init_database = None
    db = None
    store = None

# State manager
try:
    from services.state_manager import (
        StateManager,
        StateKeys,
        state_manager,
        init_state,
    )
except ImportError:
    StateManager = None
    StateKeys = None
    state_manager = None
    init_state = None

# Visitor Analytics
try:
    from services.analytics.visitor_analytics import (
        VisitorAnalytics,
        get_analytics,
        track_visitor,
        track_page_view,
        get_demo_stats,
    )
except ImportError:
    VisitorAnalytics = None
    get_analytics = None
    track_visitor = None
    track_page_view = None
    get_demo_stats = None

__all__ = [
    # AI Services
    "GroqChatService",
    "OpenAIChatService",
    "UnifiedChatService",
    "RAGService",
    "LocalEmbeddingService",
    "ChromaVectorStore",
    "ChatMessage",
    "ChatCompletionRequest",
    "ChatCompletionResponse",
    "AIServiceFactory",
    
    # Database
    "DatabaseConnection",
    "get_db",
    "BaseRepository",
    "UserRepository",
    "ChatRepository",
    "BookingRepository",
    
    # Cost
    "calculate_umrah_cost",
    "compare_packages",
    "compare_seasons",
    "get_season_type",
    
    # Price Intelligence (NEW)
    "PriceRepository",
    "PricePackage",
    "PriceHotel",
    "PriceFlight",
    "get_price_repo",
    "get_cached_packages",
    "get_cached_hotels",
    "get_cached_flights",
    "get_cached_price_summary",
    "get_cached_price_ranges",
    "format_price_idr",
    "format_duration",
    "PriceMonitor",
    "render_health_indicator",
    "render_monitoring_dashboard",
    "render_last_update_badge",
    "get_cached_health_status",
    
    # Auth
    "AuthService",
    "get_auth_service",
    "PasswordService",
    "TokenService",
    "AuthResult",
    
    # Notification (old)
    "NotifService",
    "get_notification_service",
    "EmailSender",
    "NotificationMessage",
    "NotificationResult",
    
    # Data services (new)
    "Database",
    "DataStore",
    "UserService",
    "TripService",
    "BookingService",
    "ChatService",
    "SimulationService",
    "NotificationService",
    "AnalyticsService",
    "init_database",
    "db",
    "store",
    
    # State manager
    "StateManager",
    "StateKeys",
    "state_manager",
    "init_state",
    
    # Visitor Analytics
    "VisitorAnalytics",
    "get_analytics",
    "track_visitor",
    "track_page_view",
    "get_demo_stats",
]