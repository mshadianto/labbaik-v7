"""
Amadeus API Integration for Umrah Crawler
==========================================
Hotels, Flights, and Transfers booking via Amadeus API.
"""

from app.amadeus.auth import AmadeusAuth
from app.amadeus.client import AmadeusClient
from app.amadeus.hotels import hotel_search_by_city
from app.amadeus.flights import (
    flight_offers_search,
    flight_offers_price,
    flight_create_order,
)
from app.amadeus.transfers import (
    transfer_search,
    transfer_booking,
)

__all__ = [
    "AmadeusAuth",
    "AmadeusClient",
    "hotel_search_by_city",
    "flight_offers_search",
    "flight_offers_price",
    "flight_create_order",
    "transfer_search",
    "transfer_booking",
]
