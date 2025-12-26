"""
LABBAIK AI - Subscription Service
==================================
Premium subscription management.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import secrets
import streamlit as st


class SubscriptionPlan(str, Enum):
    """Available subscription plans"""
    FREE = "free"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    LIFETIME = "lifetime"

    @property
    def display_name(self) -> str:
        names = {
            "free": "Gratis",
            "monthly": "Bulanan",
            "quarterly": "3 Bulan",
            "yearly": "Tahunan",
            "lifetime": "Selamanya"
        }
        return names.get(self.value, self.value)

    @property
    def price_idr(self) -> int:
        """Price in IDR"""
        prices = {
            "free": 0,
            "monthly": 99000,
            "quarterly": 249000,  # Save 48k
            "yearly": 799000,    # Save 389k
            "lifetime": 1999000
        }
        return prices.get(self.value, 0)

    @property
    def duration_days(self) -> int:
        """Duration in days"""
        durations = {
            "free": 0,
            "monthly": 30,
            "quarterly": 90,
            "yearly": 365,
            "lifetime": 36500  # 100 years
        }
        return durations.get(self.value, 0)

    @property
    def savings_percent(self) -> int:
        """Savings compared to monthly"""
        if self == SubscriptionPlan.QUARTERLY:
            return 16  # (99*3 - 249) / (99*3) * 100
        elif self == SubscriptionPlan.YEARLY:
            return 33  # (99*12 - 799) / (99*12) * 100
        elif self == SubscriptionPlan.LIFETIME:
            return 83  # Compared to 2 years
        return 0


class SubscriptionStatus(str, Enum):
    """Subscription status"""
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PENDING = "pending"  # Waiting for payment
    TRIAL = "trial"


@dataclass
class Subscription:
    """Subscription model"""
    id: Optional[int] = None
    user_id: int = 0
    plan: SubscriptionPlan = SubscriptionPlan.FREE
    status: SubscriptionStatus = SubscriptionStatus.PENDING

    # Dates
    started_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    # Payment info
    payment_method: Optional[str] = None  # midtrans, manual, promo
    payment_id: Optional[str] = None
    amount_paid: int = 0

    # Promo
    promo_code: Optional[str] = None
    discount_percent: int = 0

    # Tracking
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def is_active(self) -> bool:
        """Check if subscription is currently active"""
        if self.status != SubscriptionStatus.ACTIVE:
            return False
        if self.expires_at and self.expires_at < datetime.now():
            return False
        return True

    @property
    def days_remaining(self) -> int:
        """Days remaining in subscription"""
        if not self.expires_at:
            return 0
        delta = self.expires_at - datetime.now()
        return max(0, delta.days)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plan": self.plan.value,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "amount_paid": self.amount_paid,
            "days_remaining": self.days_remaining,
            "is_active": self.is_active,
        }


class SubscriptionService:
    """Subscription management service"""

    def __init__(self):
        from services.subscription.subscription_repository import get_subscription_repository
        self.repo = get_subscription_repository()

    def get_user_subscription(self, user_id: int) -> Optional[Subscription]:
        """Get active subscription for user"""
        return self.repo.get_active_subscription(user_id)

    def is_premium(self, user_id: int) -> bool:
        """Check if user has active premium subscription"""
        sub = self.get_user_subscription(user_id)
        return sub is not None and sub.is_active

    def create_subscription(
        self,
        user_id: int,
        plan: SubscriptionPlan,
        payment_method: str = "manual",
        payment_id: str = None,
        promo_code: str = None
    ) -> tuple[bool, str, Optional[Subscription]]:
        """Create new subscription"""

        # Calculate price with promo
        price = plan.price_idr
        discount = 0

        if promo_code:
            discount = self._validate_promo(promo_code)
            if discount > 0:
                price = int(price * (100 - discount) / 100)

        # Create subscription
        now = datetime.now()
        sub = Subscription(
            user_id=user_id,
            plan=plan,
            status=SubscriptionStatus.PENDING,
            started_at=now,
            expires_at=now + timedelta(days=plan.duration_days),
            payment_method=payment_method,
            payment_id=payment_id,
            amount_paid=price,
            promo_code=promo_code,
            discount_percent=discount,
        )

        saved = self.repo.create(sub)
        if saved:
            return True, "Subscription created", saved

        return False, "Failed to create subscription", None

    def activate_subscription(self, subscription_id: int) -> bool:
        """Activate a pending subscription (after payment confirmed)"""
        sub = self.repo.get_by_id(subscription_id)
        if not sub:
            return False

        sub.status = SubscriptionStatus.ACTIVE
        sub.updated_at = datetime.now()

        # Update user role to premium
        from services.user import get_user_service, UserRole
        user_service = get_user_service()
        user = user_service.get_user(sub.user_id)
        if user:
            user.role = UserRole.PREMIUM
            user_service.repo.update(user)

        return self.repo.update(sub)

    def cancel_subscription(self, subscription_id: int) -> bool:
        """Cancel a subscription"""
        sub = self.repo.get_by_id(subscription_id)
        if not sub:
            return False

        sub.status = SubscriptionStatus.CANCELLED
        sub.cancelled_at = datetime.now()
        sub.updated_at = datetime.now()

        return self.repo.update(sub)

    def check_expired_subscriptions(self):
        """Check and expire old subscriptions (run periodically)"""
        expired = self.repo.get_expired_subscriptions()
        for sub in expired:
            sub.status = SubscriptionStatus.EXPIRED

            # Downgrade user role
            from services.user import get_user_service, UserRole
            user_service = get_user_service()
            user = user_service.get_user(sub.user_id)
            if user and user.role == UserRole.PREMIUM:
                user.role = UserRole.FREE
                user_service.repo.update(user)

            self.repo.update(sub)

    def _validate_promo(self, code: str) -> int:
        """Validate promo code and return discount percent"""
        # Promo codes
        promos = {
            "UMRAH2025": 20,
            "LABBAIK50": 50,
            "FIRSTTIME": 30,
            "RAMADAN": 25,
        }
        return promos.get(code.upper(), 0)

    def get_subscription_stats(self) -> Dict[str, Any]:
        """Get subscription statistics"""
        return self.repo.get_stats()


# Singleton
_subscription_service: Optional[SubscriptionService] = None


def get_subscription_service() -> SubscriptionService:
    """Get singleton SubscriptionService instance"""
    global _subscription_service
    if _subscription_service is None:
        _subscription_service = SubscriptionService()
    return _subscription_service
