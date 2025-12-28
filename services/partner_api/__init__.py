"""
LABBAIK AI v7.5 - Partner API
==============================
REST API backend for travel agent partners.

Features:
- API key management
- Package management
- Booking management
- Price feed submission (v7.5)
"""

from services.partner_api.api_service import (
    PartnerAPI,
    APIKey,
    APIKeyStatus,
    get_partner_api,
    generate_api_key,
)

from services.partner_api.api_endpoints import (
    handle_api_request,
    API_ENDPOINTS,
)

from services.partner_api.price_feed import (
    PartnerPriceFeedService,
    PriceFeedAdminService,
    PriceFeedRequest,
    PriceFeedResponse,
    get_price_feed_service,
    get_price_feed_admin,
)

__all__ = [
    # API Service
    "PartnerAPI",
    "APIKey",
    "APIKeyStatus",
    "get_partner_api",
    "generate_api_key",
    "handle_api_request",
    "API_ENDPOINTS",
    # Price Feed (v7.5)
    "PartnerPriceFeedService",
    "PriceFeedAdminService",
    "PriceFeedRequest",
    "PriceFeedResponse",
    "get_price_feed_service",
    "get_price_feed_admin",
]
