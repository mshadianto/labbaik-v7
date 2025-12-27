"""
Agoda City IDs for RapidAPI search-overnight endpoint.
=======================================================
Resolved 2024-12-27 using tools/resolve_agoda_id.py

Format: "1_<cityId>" (prefix 1_ required for RapidAPI)

Results:
- Makkah: 718 total hotels
- Madinah: 999 total hotels
"""

# Confirmed working IDs for RapidAPI search-overnight
AGODA_CITY_IDS = {
    "MAKKAH": "1_78591",   # Mecca, Saudi Arabia (718 hotels)
    "MADINAH": "1_23028",  # Medina, Saudi Arabia (999 hotels)
}

# Web URL cityIds (without prefix, for reference)
AGODA_WEB_CITY_IDS = {
    "MAKKAH": "78591",
    "MADINAH": "23028",
}


def get_agoda_city_id(city: str) -> str:
    """Get Agoda city ID for RapidAPI endpoint."""
    key = city.upper().replace("MECCA", "MAKKAH").replace("MEDINA", "MADINAH")
    return AGODA_CITY_IDS.get(key, AGODA_CITY_IDS.get("MAKKAH"))
