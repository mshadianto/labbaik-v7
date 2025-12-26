"""
LABBAIK AI - Partner API
=========================
REST API backend for travel agent partners.
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

__all__ = [
    "PartnerAPI",
    "APIKey",
    "APIKeyStatus",
    "get_partner_api",
    "generate_api_key",
    "handle_api_request",
    "API_ENDPOINTS",
]
