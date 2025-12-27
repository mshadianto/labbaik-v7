"""
Amadeus Transfer Services
==========================
Airport-hotel transfer search and booking.
"""

import logging
from typing import Dict, Any, List

from app.amadeus.client import AmadeusClient

logger = logging.getLogger(__name__)


async def transfer_search(
    client: AmadeusClient,
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    pickup_dt_iso: str,
    passengers: int = 2,
    transfer_type: str = "PRIVATE",
) -> Dict[str, Any]:
    """
    Search transfer offers between two locations.

    Args:
        client: AmadeusClient instance
        start_lat: Start location latitude (e.g., airport)
        start_lon: Start location longitude
        end_lat: End location latitude (e.g., hotel)
        end_lon: End location longitude
        pickup_dt_iso: Pickup datetime ISO format (e.g., "2026-01-09T10:00:00")
        passengers: Number of passengers
        transfer_type: PRIVATE or SHARED

    Returns:
        Transfer offers response
    """
    body = {
        "startLocationCode": None,
        "endLocationCode": None,
        "startAddress": {
            "latitude": start_lat,
            "longitude": start_lon,
        },
        "endAddress": {
            "latitude": end_lat,
            "longitude": end_lon,
        },
        "transferType": transfer_type,
        "startDateTime": pickup_dt_iso,
        "passengers": passengers,
    }

    logger.info(f"Transfer search: ({start_lat}, {start_lon}) -> ({end_lat}, {end_lon})")
    return await client.request("POST", "/v1/shopping/transfer-offers", json=body)


async def transfer_booking(
    client: AmadeusClient,
    offer: Dict[str, Any],
    passengers: List[Dict[str, Any]],
    contact: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Book a transfer offer.

    Args:
        client: AmadeusClient instance
        offer: Transfer offer from search results
        passengers: List of passenger details
        contact: Contact information

    Returns:
        Transfer order confirmation

    Example passenger:
        {
            "firstName": "JOHN",
            "lastName": "DOE",
            "phoneNumber": "+62812xxxxxxx",
            "email": "john@example.com"
        }

    Example contact:
        {
            "email": "john@example.com",
            "phone": "+62812xxxxxxx"
        }
    """
    body = {
        "data": {
            "offerId": offer["id"],
            "passengers": passengers,
            "contactInfo": contact,
        }
    }

    logger.info(f"Booking transfer for {len(passengers)} passengers...")
    return await client.request("POST", "/v1/ordering/transfer-orders", json=body)


# Common airport coordinates for reference
AIRPORTS = {
    "JED": {"name": "Jeddah (King Abdulaziz)", "lat": 21.6796, "lon": 39.1565},
    "MED": {"name": "Madinah (Prince Mohammed)", "lat": 24.5534, "lon": 39.7051},
}
