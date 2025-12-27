"""
Amadeus Flight Services
========================
Flight search, pricing, and booking.
"""

import logging
from typing import Dict, Any, Optional, List

from app.amadeus.client import AmadeusClient

logger = logging.getLogger(__name__)


async def flight_offers_search(
    client: AmadeusClient,
    origin: str,
    dest: str,
    depart: str,
    ret: Optional[str] = None,
    adults: int = 2,
    currency: str = "SAR",
    max_results: int = 25,
) -> Dict[str, Any]:
    """
    Search flight offers.

    Args:
        client: AmadeusClient instance
        origin: Origin airport code (e.g., CGK, JKT)
        dest: Destination airport code (e.g., JED, MED)
        depart: Departure date (YYYY-MM-DD)
        ret: Return date (YYYY-MM-DD) for round trip, None for one-way
        adults: Number of adults
        currency: Price currency (default: SAR)
        max_results: Maximum number of offers (default: 25)

    Returns:
        Amadeus flight offers response
    """
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": dest,
        "departureDate": depart,
        "adults": adults,
        "currencyCode": currency,
        "max": max_results,
    }

    if ret:
        params["returnDate"] = ret

    logger.info(f"Flight search: {origin} -> {dest}, {depart}" + (f" -> {ret}" if ret else ""))
    return await client.request("GET", "/v2/shopping/flight-offers", params=params)


async def flight_offers_price(
    client: AmadeusClient,
    offer: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Get confirmed price for a flight offer.

    Args:
        client: AmadeusClient instance
        offer: Flight offer from search results

    Returns:
        Priced flight offer response
    """
    body = {
        "data": {
            "type": "flight-offers-pricing",
            "flightOffers": [offer],
        }
    }

    logger.info("Pricing flight offer...")
    return await client.request("POST", "/v1/shopping/flight-offers/pricing", json=body)


async def flight_create_order(
    client: AmadeusClient,
    priced_offer: Dict[str, Any],
    travelers: List[Dict[str, Any]],
    contacts: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Create flight booking order.

    Args:
        client: AmadeusClient instance
        priced_offer: Response from flight_offers_price
        travelers: List of traveler details
        contacts: Contact information

    Returns:
        Flight order confirmation

    Example travelers:
        [{
            "id": "1",
            "dateOfBirth": "1985-01-01",
            "name": {"firstName": "JOHN", "lastName": "DOE"},
            "gender": "MALE",
            "contact": {
                "emailAddress": "john@example.com",
                "phones": [{
                    "deviceType": "MOBILE",
                    "countryCallingCode": "62",
                    "number": "812xxxxxxx"
                }]
            },
            "documents": [{
                "documentType": "PASSPORT",
                "number": "X1234567",
                "expiryDate": "2030-01-01",
                "issuanceCountry": "ID",
                "nationality": "ID",
                "holder": True
            }]
        }]

    Example contacts:
        {
            "addresseeName": {"firstName": "JOHN", "lastName": "DOE"},
            "companyName": "Travel Agency",
            "purpose": "STANDARD",
            "phones": [{
                "deviceType": "MOBILE",
                "countryCallingCode": "62",
                "number": "812xxxxxxx"
            }],
            "emailAddress": "john@example.com",
            "address": {
                "lines": ["Jakarta"],
                "postalCode": "10110",
                "cityName": "Jakarta",
                "countryCode": "ID"
            }
        }
    """
    # Extract flight offer from pricing response
    flight_offer = priced_offer["data"]["flightOffers"][0]

    body = {
        "data": {
            "type": "flight-order",
            "flightOffers": [flight_offer],
            "travelers": travelers,
            "contacts": [contacts],
        }
    }

    logger.info(f"Creating flight order for {len(travelers)} travelers...")
    return await client.request("POST", "/v1/booking/flight-orders", json=body)
