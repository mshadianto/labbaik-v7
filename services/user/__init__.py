"""
LABBAIK AI - User Management Service
=====================================
User registration, roles, and access control.
"""

from services.user.user_service import (
    UserRole,
    UserStatus,
    User,
    UserService,
    get_user_service,
    get_current_user,
    set_current_user,
    is_logged_in,
)

from services.user.user_repository import (
    UserRepository,
    get_user_repository,
)

from services.user.access_control import (
    Feature,
    has_role_access,
    has_feature_access,
    check_access,
    require_access,
    gate_feature,
    render_access_denied,
    check_rate_limit,
    get_chat_limit,
    check_chat_limit,
    render_chat_limit_reached,
    increment_usage,
    check_page_access,
    get_page_access_role,
    PAGE_ACCESS,
)

__all__ = [
    # User models
    "UserRole",
    "UserStatus",
    "User",
    "UserService",
    "get_user_service",
    "get_current_user",
    "set_current_user",
    "is_logged_in",
    # Repository
    "UserRepository",
    "get_user_repository",
    # Access control
    "Feature",
    "has_role_access",
    "has_feature_access",
    "check_access",
    "require_access",
    "gate_feature",
    "render_access_denied",
    "check_rate_limit",
    "get_chat_limit",
    "check_chat_limit",
    "render_chat_limit_reached",
    "increment_usage",
    "check_page_access",
    "get_page_access_role",
    "PAGE_ACCESS",
]
