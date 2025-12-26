"""
LABBAIK AI - User Service
==========================
User management, roles, and access control service.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
import hashlib
import secrets
import streamlit as st


class UserRole(str, Enum):
    """User access levels"""
    GUEST = "guest"           # Unregistered visitor
    FREE = "free"             # Registered free user
    PREMIUM = "premium"       # Paid premium user
    PARTNER = "partner"       # Travel agent partner
    ADMIN = "admin"           # Administrator

    @property
    def display_name(self) -> str:
        names = {
            "guest": "Tamu",
            "free": "Gratis",
            "premium": "Premium",
            "partner": "Mitra",
            "admin": "Admin"
        }
        return names.get(self.value, self.value)

    @property
    def permissions(self) -> List[str]:
        """Get permissions for each role"""
        base_perms = ["view_packages", "use_simulator", "view_crowd"]

        if self == UserRole.GUEST:
            return base_perms
        elif self == UserRole.FREE:
            return base_perms + ["save_simulation", "chat_ai", "view_guides"]
        elif self == UserRole.PREMIUM:
            return base_perms + [
                "save_simulation", "chat_ai", "view_guides",
                "unlimited_chat", "price_alerts", "group_tracking",
                "download_reports", "priority_support"
            ]
        elif self == UserRole.PARTNER:
            return base_perms + [
                "save_simulation", "chat_ai", "view_guides",
                "unlimited_chat", "price_alerts", "group_tracking",
                "download_reports", "priority_support",
                "manage_packages", "view_analytics", "manage_bookings"
            ]
        elif self == UserRole.ADMIN:
            return ["*"]  # All permissions
        return base_perms


class UserStatus(str, Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"  # Email verification pending


@dataclass
class User:
    """User model"""
    id: Optional[int] = None
    email: str = ""
    name: str = ""
    phone: Optional[str] = None
    password_hash: str = ""
    role: UserRole = UserRole.FREE
    status: UserStatus = UserStatus.PENDING

    # Profile info
    city: Optional[str] = None
    province: Optional[str] = None

    # Umrah preferences
    preferred_departure_city: Optional[str] = None
    budget_range: Optional[str] = None  # "low", "medium", "high", "premium"
    travel_style: Optional[str] = None  # "backpacker", "standard", "comfort", "luxury"

    # Tracking
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    login_count: int = 0

    # Analytics
    source: Optional[str] = None  # "organic", "referral", "ads", "social"
    referral_code: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None

    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        perms = self.role.permissions
        return "*" in perms or permission in perms

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "phone": self.phone,
            "role": self.role.value,
            "status": self.status.value,
            "city": self.city,
            "province": self.province,
            "preferred_departure_city": self.preferred_departure_city,
            "budget_range": self.budget_range,
            "travel_style": self.travel_style,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "login_count": self.login_count,
            "source": self.source,
            "referral_code": self.referral_code,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Create from dictionary"""
        return cls(
            id=data.get("id"),
            email=data.get("email", ""),
            name=data.get("name", ""),
            phone=data.get("phone"),
            password_hash=data.get("password_hash", ""),
            role=UserRole(data.get("role", "free")),
            status=UserStatus(data.get("status", "pending")),
            city=data.get("city"),
            province=data.get("province"),
            preferred_departure_city=data.get("preferred_departure_city"),
            budget_range=data.get("budget_range"),
            travel_style=data.get("travel_style"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else datetime.now(),
            last_login=datetime.fromisoformat(data["last_login"]) if data.get("last_login") else None,
            login_count=data.get("login_count", 0),
            source=data.get("source"),
            referral_code=data.get("referral_code"),
            utm_source=data.get("utm_source"),
            utm_medium=data.get("utm_medium"),
            utm_campaign=data.get("utm_campaign"),
        )


class UserService:
    """User management service"""

    def __init__(self):
        from services.user.user_repository import get_user_repository
        self.repo = get_user_repository()

    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return f"{salt}${hash_obj.hex()}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, stored_hash = password_hash.split('$')
            hash_obj = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return hash_obj.hex() == stored_hash
        except Exception:
            return False

    def register(
        self,
        email: str,
        password: str,
        name: str,
        phone: Optional[str] = None,
        **kwargs
    ) -> tuple[bool, str, Optional[User]]:
        """
        Register new user
        Returns: (success, message, user)
        """
        # Validate email
        if not email or "@" not in email:
            return False, "Email tidak valid", None

        # Check if email exists
        existing = self.repo.get_by_email(email)
        if existing:
            return False, "Email sudah terdaftar", None

        # Validate password
        if len(password) < 6:
            return False, "Password minimal 6 karakter", None

        # Create user
        user = User(
            email=email.lower().strip(),
            name=name.strip(),
            phone=phone,
            password_hash=self.hash_password(password),
            role=UserRole.FREE,
            status=UserStatus.ACTIVE,  # Auto-activate for now
            source=kwargs.get("source"),
            referral_code=kwargs.get("referral_code"),
            utm_source=kwargs.get("utm_source"),
            utm_medium=kwargs.get("utm_medium"),
            utm_campaign=kwargs.get("utm_campaign"),
            city=kwargs.get("city"),
            province=kwargs.get("province"),
            preferred_departure_city=kwargs.get("preferred_departure_city"),
            budget_range=kwargs.get("budget_range"),
            travel_style=kwargs.get("travel_style"),
        )

        # Save to database
        saved_user = self.repo.create(user)
        if saved_user:
            return True, "Pendaftaran berhasil!", saved_user

        return False, "Gagal menyimpan data", None

    def login(self, email: str, password: str) -> tuple[bool, str, Optional[User]]:
        """
        Login user
        Returns: (success, message, user)
        """
        user = self.repo.get_by_email(email.lower().strip())

        if not user:
            return False, "Email tidak ditemukan", None

        if user.status == UserStatus.SUSPENDED:
            return False, "Akun Anda dibekukan", None

        if not self.verify_password(password, user.password_hash):
            return False, "Password salah", None

        # Update login info
        user.last_login = datetime.now()
        user.login_count += 1
        self.repo.update(user)

        return True, "Login berhasil!", user

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.repo.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.repo.get_by_email(email.lower().strip())

    def update_profile(self, user: User, **kwargs) -> bool:
        """Update user profile"""
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.updated_at = datetime.now()
        return self.repo.update(user)

    def upgrade_to_premium(self, user: User) -> bool:
        """Upgrade user to premium"""
        user.role = UserRole.PREMIUM
        user.updated_at = datetime.now()
        return self.repo.update(user)

    def get_all_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Get all users (admin only)"""
        return self.repo.get_all(limit, offset)

    def get_user_stats(self) -> Dict[str, Any]:
        """Get user statistics for analytics"""
        return self.repo.get_stats()

    def search_users(self, query: str) -> List[User]:
        """Search users by name or email"""
        return self.repo.search(query)


# Singleton instance
_user_service: Optional[UserService] = None


def get_user_service() -> UserService:
    """Get singleton UserService instance"""
    global _user_service
    if _user_service is None:
        _user_service = UserService()
    return _user_service


# Session helpers
def get_current_user() -> Optional[User]:
    """Get current logged-in user from session"""
    if "user" in st.session_state:
        return st.session_state.user
    return None


def set_current_user(user: Optional[User]):
    """Set current user in session"""
    if user:
        st.session_state.user = user
        st.session_state.user_role = user.role
    else:
        if "user" in st.session_state:
            del st.session_state.user
        if "user_role" in st.session_state:
            del st.session_state.user_role


def is_logged_in() -> bool:
    """Check if user is logged in"""
    return "user" in st.session_state and st.session_state.user is not None


def require_login(func):
    """Decorator to require login for a function"""
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            st.warning("Silakan login terlebih dahulu")
            return None
        return func(*args, **kwargs)
    return wrapper


def require_role(required_role: UserRole):
    """Decorator to require specific role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user:
                st.warning("Silakan login terlebih dahulu")
                return None

            # Check role hierarchy
            role_hierarchy = [UserRole.GUEST, UserRole.FREE, UserRole.PREMIUM, UserRole.PARTNER, UserRole.ADMIN]
            user_level = role_hierarchy.index(user.role) if user.role in role_hierarchy else 0
            required_level = role_hierarchy.index(required_role) if required_role in role_hierarchy else 0

            if user_level < required_level:
                st.error(f"Fitur ini membutuhkan akses {required_role.display_name}")
                return None

            return func(*args, **kwargs)
        return wrapper
    return decorator
