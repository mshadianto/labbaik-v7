"""
LABBAIK AI - Risk Score Service
===============================
Hotel availability risk scoring and sold-out prediction.
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Tuple
from enum import Enum


class RiskLevel(str, Enum):
    """Risk level categories."""
    LOW = "low"           # 0-30: Plenty of availability
    MEDIUM = "medium"     # 31-60: Some pressure
    HIGH = "high"         # 61-80: Book soon
    CRITICAL = "critical" # 81-100: Almost sold out


class AvailabilityStatus(str, Enum):
    """Availability status from providers."""
    AVAILABLE = "available"
    LIMITED = "limited"           # < 5 rooms
    LAST_ROOMS = "last_rooms"     # 1-2 rooms
    SOLD_OUT = "sold_out"
    UNKNOWN = "unknown"


@dataclass
class AvailabilitySnapshot:
    """Point-in-time availability data."""
    hotel_id: str
    provider: str
    checkin: date
    checkout: date
    status: AvailabilityStatus
    rooms_left: Optional[int] = None
    min_price: Optional[float] = None
    fetched_at: datetime = field(default_factory=datetime.now)


@dataclass
class PriceTrend:
    """Price trend analysis."""
    direction: str  # "up", "down", "stable"
    change_percent: float
    avg_price_7d: Optional[float] = None
    avg_price_30d: Optional[float] = None


@dataclass
class RiskScore:
    """Computed risk score for a hotel."""
    hotel_id: str
    city: str
    score: int  # 0-100
    level: RiskLevel
    reasons: List[str]
    trend: PriceTrend
    recommendation: str
    computed_at: datetime = field(default_factory=datetime.now)


class RiskScoreCalculator:
    """Calculate sold-out risk scores for hotels."""

    # Weights for different factors
    WEIGHTS = {
        "availability_status": 30,    # Current availability status
        "rooms_left": 25,             # Number of rooms remaining
        "price_trend": 20,            # Price increase trend
        "days_until_checkin": 15,     # Urgency factor
        "seasonal_factor": 10,        # High season multiplier
    }

    # High-risk dates (Ramadan, Hajj, holidays)
    HIGH_SEASON_MONTHS = [3, 4, 6, 7, 12, 1]  # Approximate

    def __init__(self):
        self.snapshots: Dict[str, List[AvailabilitySnapshot]] = {}

    def add_snapshot(self, snapshot: AvailabilitySnapshot) -> None:
        """Add availability snapshot for tracking."""
        key = snapshot.hotel_id
        if key not in self.snapshots:
            self.snapshots[key] = []

        self.snapshots[key].append(snapshot)

        # Keep only last 60 days of snapshots
        cutoff = datetime.now() - timedelta(days=60)
        self.snapshots[key] = [
            s for s in self.snapshots[key]
            if s.fetched_at > cutoff
        ]

    def get_recent_snapshots(
        self,
        hotel_id: str,
        days: int = 30
    ) -> List[AvailabilitySnapshot]:
        """Get recent snapshots for a hotel."""
        if hotel_id not in self.snapshots:
            return []

        cutoff = datetime.now() - timedelta(days=days)
        return [
            s for s in self.snapshots[hotel_id]
            if s.fetched_at > cutoff
        ]

    def calculate_availability_score(
        self,
        snapshots: List[AvailabilitySnapshot]
    ) -> Tuple[int, List[str]]:
        """
        Calculate score based on availability status.

        Returns:
            (score 0-100, reasons)
        """
        if not snapshots:
            return 50, ["No recent availability data"]

        reasons = []
        latest = snapshots[-1]

        # Status-based scoring
        status_scores = {
            AvailabilityStatus.AVAILABLE: 10,
            AvailabilityStatus.LIMITED: 50,
            AvailabilityStatus.LAST_ROOMS: 80,
            AvailabilityStatus.SOLD_OUT: 100,
            AvailabilityStatus.UNKNOWN: 50,
        }

        base_score = status_scores.get(latest.status, 50)

        # Check status deterioration trend
        if len(snapshots) >= 3:
            recent_statuses = [s.status for s in snapshots[-3:]]
            if AvailabilityStatus.SOLD_OUT in recent_statuses:
                base_score = min(100, base_score + 20)
                reasons.append("Recently sold out")

        # Rooms left factor
        if latest.rooms_left is not None:
            if latest.rooms_left <= 2:
                base_score = min(100, base_score + 30)
                reasons.append(f"Only {latest.rooms_left} room(s) left!")
            elif latest.rooms_left <= 5:
                base_score = min(100, base_score + 15)
                reasons.append(f"Only {latest.rooms_left} rooms left")

        if latest.status == AvailabilityStatus.AVAILABLE:
            reasons.append("Currently available")
        elif latest.status == AvailabilityStatus.LIMITED:
            reasons.append("Limited availability")

        return min(100, base_score), reasons

    def calculate_price_trend(
        self,
        snapshots: List[AvailabilitySnapshot]
    ) -> Tuple[int, PriceTrend, List[str]]:
        """
        Calculate score based on price trends.

        Returns:
            (score 0-100, trend, reasons)
        """
        reasons = []

        prices = [s.min_price for s in snapshots if s.min_price]
        if len(prices) < 2:
            return 0, PriceTrend("stable", 0), []

        # Calculate averages
        recent_prices = prices[-7:] if len(prices) >= 7 else prices
        older_prices = prices[:-7] if len(prices) > 7 else prices[:len(prices)//2]

        avg_recent = sum(recent_prices) / len(recent_prices)
        avg_older = sum(older_prices) / len(older_prices) if older_prices else avg_recent

        # Calculate change
        if avg_older > 0:
            change_percent = ((avg_recent - avg_older) / avg_older) * 100
        else:
            change_percent = 0

        # Determine direction
        if change_percent > 5:
            direction = "up"
            score = min(50, int(change_percent * 2))
            reasons.append(f"Price increased {change_percent:.1f}%")
        elif change_percent < -5:
            direction = "down"
            score = 0
            reasons.append(f"Price dropped {abs(change_percent):.1f}%")
        else:
            direction = "stable"
            score = 10

        trend = PriceTrend(
            direction=direction,
            change_percent=round(change_percent, 1),
            avg_price_7d=round(avg_recent, 2),
            avg_price_30d=round(avg_older, 2) if avg_older != avg_recent else None
        )

        return score, trend, reasons

    def calculate_urgency_score(
        self,
        checkin_date: date
    ) -> Tuple[int, List[str]]:
        """
        Calculate urgency based on days until check-in.

        Returns:
            (score 0-100, reasons)
        """
        today = date.today()
        days_until = (checkin_date - today).days

        reasons = []

        if days_until <= 3:
            score = 90
            reasons.append("Check-in in 3 days or less!")
        elif days_until <= 7:
            score = 70
            reasons.append("Check-in within a week")
        elif days_until <= 14:
            score = 50
            reasons.append("Check-in within 2 weeks")
        elif days_until <= 30:
            score = 30
            reasons.append("Check-in within a month")
        elif days_until <= 60:
            score = 15
        else:
            score = 5

        return score, reasons

    def calculate_seasonal_score(
        self,
        checkin_date: date
    ) -> Tuple[int, List[str]]:
        """
        Calculate score based on seasonal demand.

        Returns:
            (score 0-100, reasons)
        """
        month = checkin_date.month
        reasons = []

        if month in [6, 7]:  # Hajj season (approximate)
            return 80, ["Hajj season - very high demand"]
        elif month in [3, 4]:  # Ramadan (approximate)
            return 70, ["Ramadan - high demand"]
        elif month in [12, 1]:  # Holiday season
            return 50, ["Holiday season"]
        elif month in [2, 11]:  # Shoulder season
            return 30, []
        else:
            return 10, ["Low season"]

    def compute_risk_score(
        self,
        hotel_id: str,
        city: str,
        checkin_date: date,
        checkout_date: date = None
    ) -> RiskScore:
        """
        Compute comprehensive risk score for a hotel.

        Args:
            hotel_id: Hotel identifier
            city: City (MAKKAH/MADINAH)
            checkin_date: Check-in date
            checkout_date: Check-out date (optional)

        Returns:
            RiskScore object
        """
        all_reasons = []

        # Get snapshots
        snapshots = self.get_recent_snapshots(hotel_id)

        # Calculate component scores
        avail_score, avail_reasons = self.calculate_availability_score(snapshots)
        all_reasons.extend(avail_reasons)

        price_score, price_trend, price_reasons = self.calculate_price_trend(snapshots)
        all_reasons.extend(price_reasons)

        urgency_score, urgency_reasons = self.calculate_urgency_score(checkin_date)
        all_reasons.extend(urgency_reasons)

        seasonal_score, seasonal_reasons = self.calculate_seasonal_score(checkin_date)
        all_reasons.extend(seasonal_reasons)

        # Weighted total
        total_score = int(
            (avail_score * self.WEIGHTS["availability_status"] / 100) +
            (price_score * self.WEIGHTS["price_trend"] / 100) +
            (urgency_score * self.WEIGHTS["days_until_checkin"] / 100) +
            (seasonal_score * self.WEIGHTS["seasonal_factor"] / 100)
        )

        # Normalize to 0-100
        total_score = min(100, max(0, total_score))

        # Determine risk level
        if total_score >= 81:
            level = RiskLevel.CRITICAL
            recommendation = "Book immediately! High risk of selling out."
        elif total_score >= 61:
            level = RiskLevel.HIGH
            recommendation = "Book soon - availability is limited."
        elif total_score >= 31:
            level = RiskLevel.MEDIUM
            recommendation = "Consider booking - demand is building."
        else:
            level = RiskLevel.LOW
            recommendation = "Low pressure - safe to compare options."

        return RiskScore(
            hotel_id=hotel_id,
            city=city.upper(),
            score=total_score,
            level=level,
            reasons=all_reasons[:5],  # Top 5 reasons
            trend=price_trend,
            recommendation=recommendation
        )


# Singleton instance
_risk_calculator: Optional[RiskScoreCalculator] = None


def get_risk_calculator() -> RiskScoreCalculator:
    """Get singleton RiskScoreCalculator instance."""
    global _risk_calculator
    if _risk_calculator is None:
        _risk_calculator = RiskScoreCalculator()
    return _risk_calculator


# Convenience functions
def compute_risk_score(
    hotel_id: str,
    city: str,
    checkin_date: date,
    checkout_date: date = None
) -> RiskScore:
    """Compute risk score for a hotel."""
    return get_risk_calculator().compute_risk_score(
        hotel_id, city, checkin_date, checkout_date
    )


def get_risk_level(score: int) -> RiskLevel:
    """Get risk level from score."""
    if score >= 81:
        return RiskLevel.CRITICAL
    elif score >= 61:
        return RiskLevel.HIGH
    elif score >= 31:
        return RiskLevel.MEDIUM
    else:
        return RiskLevel.LOW


def format_risk_badge(level: RiskLevel) -> str:
    """Format risk level as display badge."""
    badges = {
        RiskLevel.LOW: "Low Risk",
        RiskLevel.MEDIUM: "Medium Risk",
        RiskLevel.HIGH: "High Risk - Book Soon!",
        RiskLevel.CRITICAL: "CRITICAL - Almost Sold Out!",
    }
    return badges.get(level, "Unknown")


def format_risk_color(level: RiskLevel) -> str:
    """Get color for risk level display."""
    colors = {
        RiskLevel.LOW: "#4CAF50",      # Green
        RiskLevel.MEDIUM: "#FFC107",   # Yellow
        RiskLevel.HIGH: "#FF9800",     # Orange
        RiskLevel.CRITICAL: "#F44336", # Red
    }
    return colors.get(level, "#9E9E9E")


def get_booking_urgency_text(days_until: int) -> str:
    """Get urgency text based on days until check-in."""
    if days_until <= 0:
        return "Check-in today!"
    elif days_until == 1:
        return "Check-in tomorrow!"
    elif days_until <= 3:
        return f"Only {days_until} days left!"
    elif days_until <= 7:
        return f"{days_until} days until check-in"
    elif days_until <= 14:
        return "Less than 2 weeks"
    elif days_until <= 30:
        return "Within a month"
    else:
        return f"{days_until} days away"
