"""
LABBAIK AI v7.5 - Partner Price Feed API
=========================================
REST API for travel agent partners to submit price feeds.

Partners can:
- Submit new price feeds
- Update existing feeds
- View their submitted feeds
- Check feed approval status
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from dataclasses import dataclass

from services.price_aggregation.models import (
    PartnerPriceFeed, AggregatedOffer, SourceType, OfferType,
    convert_idr_to_sar
)
from services.price_aggregation.repository import get_aggregated_price_repository
from services.partner_api.api_service import get_partner_api, APIKey

logger = logging.getLogger(__name__)


@dataclass
class PriceFeedRequest:
    """Price feed submission request."""
    package_name: str
    price_idr: float
    duration_days: int
    departure_city: str

    # Optional fields
    description: str = None
    hotel_makkah: str = None
    hotel_makkah_stars: int = None
    hotel_madinah: str = None
    hotel_madinah_stars: int = None
    departure_dates: List[str] = None
    airline: str = None
    flight_class: str = "economy"
    room_type: str = "quad"
    inclusions: List[str] = None
    exclusions: List[str] = None
    quota: int = 0
    valid_from: str = None
    valid_until: str = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PriceFeedRequest":
        """Create from dictionary."""
        return cls(
            package_name=data.get("package_name", ""),
            price_idr=float(data.get("price_idr", 0)),
            duration_days=int(data.get("duration_days", 9)),
            departure_city=data.get("departure_city", "Jakarta"),
            description=data.get("description"),
            hotel_makkah=data.get("hotel_makkah"),
            hotel_makkah_stars=data.get("hotel_makkah_stars"),
            hotel_madinah=data.get("hotel_madinah"),
            hotel_madinah_stars=data.get("hotel_madinah_stars"),
            departure_dates=data.get("departure_dates", []),
            airline=data.get("airline"),
            flight_class=data.get("flight_class", "economy"),
            room_type=data.get("room_type", "quad"),
            inclusions=data.get("inclusions", []),
            exclusions=data.get("exclusions", []),
            quota=int(data.get("quota", 0)),
            valid_from=data.get("valid_from"),
            valid_until=data.get("valid_until"),
        )


@dataclass
class PriceFeedResponse:
    """Price feed API response."""
    success: bool
    message: str
    feed_id: str = None
    data: Dict[str, Any] = None
    errors: List[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "success": self.success,
            "message": self.message
        }
        if self.feed_id:
            result["feed_id"] = self.feed_id
        if self.data:
            result["data"] = self.data
        if self.errors:
            result["errors"] = self.errors
        return result


class PartnerPriceFeedService:
    """
    Service for partner price feed operations.

    Partners can submit their Umrah package prices
    which will be included in price aggregation.
    """

    # Price validation ranges
    MIN_PRICE_IDR = 10_000_000  # 10 juta
    MAX_PRICE_IDR = 500_000_000  # 500 juta
    MIN_DURATION_DAYS = 5
    MAX_DURATION_DAYS = 45

    def __init__(self):
        self._repository = None
        self._partner_api = None

    @property
    def repository(self):
        if self._repository is None:
            self._repository = get_aggregated_price_repository()
        return self._repository

    @property
    def partner_api(self):
        if self._partner_api is None:
            self._partner_api = get_partner_api()
        return self._partner_api

    def submit_feed(
        self,
        partner_id: str,
        request: PriceFeedRequest
    ) -> PriceFeedResponse:
        """
        Submit a new price feed.

        Args:
            partner_id: Partner's user ID
            request: Price feed request data

        Returns:
            PriceFeedResponse with result
        """
        # Validate request
        errors = self._validate_request(request)
        if errors:
            return PriceFeedResponse(
                success=False,
                message="Validation failed",
                errors=errors
            )

        try:
            # Create partner feed object
            feed = PartnerPriceFeed(
                partner_id=partner_id,
                feed_name=request.package_name,
                feed_type="package",
                price_idr=request.price_idr,
                price_sar=convert_idr_to_sar(request.price_idr),
                price_per_person_idr=request.price_idr,  # Assume per person
                package_name=request.package_name,
                description=request.description,
                hotel_makkah=request.hotel_makkah,
                hotel_makkah_stars=request.hotel_makkah_stars,
                hotel_madinah=request.hotel_madinah,
                hotel_madinah_stars=request.hotel_madinah_stars,
                duration_days=request.duration_days,
                departure_city=request.departure_city,
                departure_dates=request.departure_dates or [],
                airline=request.airline,
                flight_class=request.flight_class,
                room_type=request.room_type,
                inclusions=request.inclusions or [],
                exclusions=request.exclusions or [],
                quota=request.quota,
                booked=0,
                is_available=True,
                valid_from=date.fromisoformat(request.valid_from) if request.valid_from else None,
                valid_until=date.fromisoformat(request.valid_until) if request.valid_until else None,
                status="pending",
                submitted_at=datetime.now()
            )

            # Save to database
            feed_id = self.repository.create_partner_feed(feed)

            logger.info(f"Partner {partner_id} submitted price feed: {feed_id}")

            return PriceFeedResponse(
                success=True,
                message="Price feed submitted successfully. Pending approval.",
                feed_id=feed_id,
                data={
                    "package_name": request.package_name,
                    "price_idr": request.price_idr,
                    "status": "pending"
                }
            )

        except Exception as e:
            logger.error(f"Failed to submit price feed: {e}")
            return PriceFeedResponse(
                success=False,
                message="Failed to submit price feed",
                errors=[str(e)]
            )

    def update_feed(
        self,
        partner_id: str,
        feed_id: str,
        request: PriceFeedRequest
    ) -> PriceFeedResponse:
        """
        Update an existing price feed.

        Partners can only update their own feeds in pending status.
        """
        # Validate request
        errors = self._validate_request(request)
        if errors:
            return PriceFeedResponse(
                success=False,
                message="Validation failed",
                errors=errors
            )

        try:
            # Get existing feed
            feed = self.repository.get_partner_feed(feed_id)

            if not feed:
                return PriceFeedResponse(
                    success=False,
                    message="Price feed not found"
                )

            if feed.partner_id != partner_id:
                return PriceFeedResponse(
                    success=False,
                    message="Not authorized to update this feed"
                )

            if feed.status == "approved":
                return PriceFeedResponse(
                    success=False,
                    message="Cannot update approved feed. Submit a new one."
                )

            # Update feed
            feed.package_name = request.package_name
            feed.price_idr = request.price_idr
            feed.price_sar = convert_idr_to_sar(request.price_idr)
            feed.duration_days = request.duration_days
            feed.departure_city = request.departure_city
            feed.hotel_makkah = request.hotel_makkah
            feed.hotel_makkah_stars = request.hotel_makkah_stars
            feed.hotel_madinah = request.hotel_madinah
            feed.hotel_madinah_stars = request.hotel_madinah_stars
            feed.airline = request.airline
            feed.inclusions = request.inclusions or []
            feed.exclusions = request.exclusions or []
            feed.quota = request.quota

            if request.valid_from:
                feed.valid_from = date.fromisoformat(request.valid_from)
            if request.valid_until:
                feed.valid_until = date.fromisoformat(request.valid_until)

            self.repository.update_partner_feed(feed)

            return PriceFeedResponse(
                success=True,
                message="Price feed updated successfully",
                feed_id=feed_id
            )

        except Exception as e:
            logger.error(f"Failed to update price feed: {e}")
            return PriceFeedResponse(
                success=False,
                message="Failed to update price feed",
                errors=[str(e)]
            )

    def get_feeds(
        self,
        partner_id: str,
        status: str = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get price feeds for a partner."""
        try:
            feeds = self.repository.get_partner_feeds(
                partner_id=partner_id,
                status=status,
                limit=limit
            )

            return [self._feed_to_dict(feed) for feed in feeds]

        except Exception as e:
            logger.error(f"Failed to get partner feeds: {e}")
            return []

    def get_feed(
        self,
        partner_id: str,
        feed_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a specific price feed."""
        try:
            feed = self.repository.get_partner_feed(feed_id)

            if not feed or feed.partner_id != partner_id:
                return None

            return self._feed_to_dict(feed)

        except Exception as e:
            logger.error(f"Failed to get feed: {e}")
            return None

    def delete_feed(
        self,
        partner_id: str,
        feed_id: str
    ) -> PriceFeedResponse:
        """Delete a price feed (only pending feeds)."""
        try:
            feed = self.repository.get_partner_feed(feed_id)

            if not feed:
                return PriceFeedResponse(
                    success=False,
                    message="Price feed not found"
                )

            if feed.partner_id != partner_id:
                return PriceFeedResponse(
                    success=False,
                    message="Not authorized to delete this feed"
                )

            if feed.status == "approved":
                return PriceFeedResponse(
                    success=False,
                    message="Cannot delete approved feed"
                )

            self.repository.delete_partner_feed(feed_id)

            return PriceFeedResponse(
                success=True,
                message="Price feed deleted"
            )

        except Exception as e:
            logger.error(f"Failed to delete feed: {e}")
            return PriceFeedResponse(
                success=False,
                message="Failed to delete price feed",
                errors=[str(e)]
            )

    def _validate_request(self, request: PriceFeedRequest) -> List[str]:
        """Validate price feed request."""
        errors = []

        # Required fields
        if not request.package_name:
            errors.append("package_name is required")

        if not request.price_idr or request.price_idr <= 0:
            errors.append("price_idr must be positive")

        if not request.departure_city:
            errors.append("departure_city is required")

        # Price range validation
        if request.price_idr < self.MIN_PRICE_IDR:
            errors.append(f"price_idr minimum is {self.MIN_PRICE_IDR:,.0f}")

        if request.price_idr > self.MAX_PRICE_IDR:
            errors.append(f"price_idr maximum is {self.MAX_PRICE_IDR:,.0f}")

        # Duration validation
        if request.duration_days < self.MIN_DURATION_DAYS:
            errors.append(f"duration_days minimum is {self.MIN_DURATION_DAYS}")

        if request.duration_days > self.MAX_DURATION_DAYS:
            errors.append(f"duration_days maximum is {self.MAX_DURATION_DAYS}")

        # Hotel stars validation
        if request.hotel_makkah_stars and not (1 <= request.hotel_makkah_stars <= 5):
            errors.append("hotel_makkah_stars must be between 1 and 5")

        if request.hotel_madinah_stars and not (1 <= request.hotel_madinah_stars <= 5):
            errors.append("hotel_madinah_stars must be between 1 and 5")

        # Date validation
        if request.valid_from and request.valid_until:
            try:
                from_date = date.fromisoformat(request.valid_from)
                until_date = date.fromisoformat(request.valid_until)
                if from_date > until_date:
                    errors.append("valid_from must be before valid_until")
            except ValueError:
                errors.append("Invalid date format. Use YYYY-MM-DD")

        return errors

    def _feed_to_dict(self, feed: PartnerPriceFeed) -> Dict[str, Any]:
        """Convert feed to dictionary for API response."""
        return {
            "id": feed.id,
            "package_name": feed.package_name,
            "description": feed.description,
            "price_idr": feed.price_idr,
            "price_sar": feed.price_sar,
            "duration_days": feed.duration_days,
            "departure_city": feed.departure_city,
            "departure_dates": feed.departure_dates,
            "hotel_makkah": feed.hotel_makkah,
            "hotel_makkah_stars": feed.hotel_makkah_stars,
            "hotel_madinah": feed.hotel_madinah,
            "hotel_madinah_stars": feed.hotel_madinah_stars,
            "airline": feed.airline,
            "flight_class": feed.flight_class,
            "room_type": feed.room_type,
            "inclusions": feed.inclusions,
            "exclusions": feed.exclusions,
            "quota": feed.quota,
            "booked": feed.booked,
            "available": feed.quota - feed.booked if feed.quota else 0,
            "is_available": feed.is_available,
            "valid_from": feed.valid_from.isoformat() if feed.valid_from else None,
            "valid_until": feed.valid_until.isoformat() if feed.valid_until else None,
            "status": feed.status,
            "submitted_at": feed.submitted_at.isoformat() if feed.submitted_at else None,
            "approved_at": feed.approved_at.isoformat() if feed.approved_at else None,
            "rejection_reason": feed.rejection_reason
        }


# Admin functions for feed approval
class PriceFeedAdminService:
    """Admin service for approving/rejecting price feeds."""

    def __init__(self):
        self._repository = None

    @property
    def repository(self):
        if self._repository is None:
            self._repository = get_aggregated_price_repository()
        return self._repository

    def get_pending_feeds(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all pending price feeds."""
        feeds = self.repository.get_partner_feeds(status="pending", limit=limit)
        return [self._feed_to_dict(feed) for feed in feeds]

    def approve_feed(
        self,
        feed_id: str,
        approved_by: str
    ) -> PriceFeedResponse:
        """Approve a price feed."""
        try:
            success = self.repository.approve_partner_feed(feed_id, approved_by)

            if success:
                logger.info(f"Price feed {feed_id} approved by {approved_by}")
                return PriceFeedResponse(
                    success=True,
                    message="Price feed approved",
                    feed_id=feed_id
                )
            else:
                return PriceFeedResponse(
                    success=False,
                    message="Failed to approve feed"
                )

        except Exception as e:
            logger.error(f"Failed to approve feed: {e}")
            return PriceFeedResponse(
                success=False,
                message=str(e)
            )

    def reject_feed(
        self,
        feed_id: str,
        rejected_by: str,
        reason: str
    ) -> PriceFeedResponse:
        """Reject a price feed."""
        try:
            success = self.repository.reject_partner_feed(
                feed_id, rejected_by, reason
            )

            if success:
                logger.info(f"Price feed {feed_id} rejected: {reason}")
                return PriceFeedResponse(
                    success=True,
                    message="Price feed rejected",
                    feed_id=feed_id
                )
            else:
                return PriceFeedResponse(
                    success=False,
                    message="Failed to reject feed"
                )

        except Exception as e:
            logger.error(f"Failed to reject feed: {e}")
            return PriceFeedResponse(
                success=False,
                message=str(e)
            )

    def _feed_to_dict(self, feed: PartnerPriceFeed) -> Dict[str, Any]:
        """Convert feed to dictionary."""
        return {
            "id": feed.id,
            "partner_id": feed.partner_id,
            "package_name": feed.package_name,
            "price_idr": feed.price_idr,
            "duration_days": feed.duration_days,
            "departure_city": feed.departure_city,
            "hotel_makkah": feed.hotel_makkah,
            "hotel_makkah_stars": feed.hotel_makkah_stars,
            "hotel_madinah": feed.hotel_madinah,
            "hotel_madinah_stars": feed.hotel_madinah_stars,
            "status": feed.status,
            "submitted_at": feed.submitted_at.isoformat() if feed.submitted_at else None,
        }


# Singletons
_price_feed_service: Optional[PartnerPriceFeedService] = None
_price_feed_admin: Optional[PriceFeedAdminService] = None


def get_price_feed_service() -> PartnerPriceFeedService:
    """Get singleton price feed service."""
    global _price_feed_service
    if _price_feed_service is None:
        _price_feed_service = PartnerPriceFeedService()
    return _price_feed_service


def get_price_feed_admin() -> PriceFeedAdminService:
    """Get singleton admin service."""
    global _price_feed_admin
    if _price_feed_admin is None:
        _price_feed_admin = PriceFeedAdminService()
    return _price_feed_admin
