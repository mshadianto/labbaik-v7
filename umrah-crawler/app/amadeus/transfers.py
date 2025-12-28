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
    start_location_code: str,
    end_lat: float,
    end_lon: float,
    end_name: str,
    end_city: str,
    pickup_dt_iso: str,
    passengers: int = 2,
    transfer_type: str = "PRIVATE",
    end_zip: str = "24231",
    end_country: str = "SA",
) -> Dict[str, Any]:
    """
    Search transfer offers from airport to destination.

    Args:
        client: AmadeusClient instance
        start_location_code: Airport IATA code (e.g., JED, MED)
        end_lat: Destination latitude (e.g., hotel or Haram)
        end_lon: Destination longitude
        end_name: Destination name (e.g., "Masjid al-Haram")
        end_city: Destination city (e.g., "Mecca", "Medina")
        pickup_dt_iso: Pickup datetime ISO format (e.g., "2026-01-09T10:00:00")
        passengers: Number of passengers
        transfer_type: PRIVATE or SHARED
        end_zip: Destination postal code (default: 24231 for Makkah)
        end_country: Destination country code (default: SA)

    Returns:
        Transfer offers response
    """
    body = {
        "startLocationCode": start_location_code,
        "endAddressLine": end_name,
        "endCityName": end_city,
        "endZipCode": end_zip,
        "endCountryCode": end_country,
        "endName": end_name,
        "endGeoCode": f"{end_lat},{end_lon}",
        "transferType": transfer_type,
        "startDateTime": pickup_dt_iso,
        "passengers": passengers,
    }

    logger.info(f"Transfer search: {start_location_code} -> {end_name} ({end_city})")
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

# City info for transfer destinations
CITY_INFO = {
    "MAKKAH": {
        "name": "Masjid al-Haram",
        "city": "Mecca",
        "zip": "24231",
        "lat": 21.422487,
        "lon": 39.826206,
        "airport": "JED",
    },
    "MADINAH": {
        "name": "Masjid an-Nabawi",
        "city": "Medina",
        "zip": "42311",
        "lat": 24.467227,
        "lon": 39.611133,
        "airport": "MED",
    },
}


async def transfer_search_to_city(
    client: AmadeusClient,
    city: str,
    pickup_dt_iso: str,
    passengers: int = 2,
    transfer_type: str = "PRIVATE",
) -> Dict[str, Any]:
    """
    Convenience function: Search transfers from airport to city center (Haram/Nabawi).

    Args:
        client: AmadeusClient instance
        city: MAKKAH or MADINAH
        pickup_dt_iso: Pickup datetime ISO format
        passengers: Number of passengers
        transfer_type: PRIVATE or SHARED

    Returns:
        Transfer offers response
    """
    city_upper = city.upper()
    info = CITY_INFO.get(city_upper)

    if not info:
        raise ValueError(f"Unknown city: {city}. Use MAKKAH or MADINAH.")

    return await transfer_search(
        client=client,
        start_location_code=info["airport"],
        end_lat=info["lat"],
        end_lon=info["lon"],
        end_name=info["name"],
        end_city=info["city"],
        pickup_dt_iso=pickup_dt_iso,
        passengers=passengers,
        transfer_type=transfer_type,
        end_zip=info["zip"],
        end_country="SA",
    )
