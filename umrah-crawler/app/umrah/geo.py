"""
Umrah Geo Utilities
====================
Distance calculations and scoring for Masjid al-Haram & Masjid Nabawi.
"""

from math import radians, sin, cos, asin, sqrt

# Masjid al-Haram (Makkah) - approximate center
HARAM_LAT = 21.422487
HARAM_LON = 39.826206

# Masjid Nabawi (Madinah) - approximate center
NABAWI_LAT = 24.467227
NABAWI_LON = 39.611133

# City center coordinates for search
CITY_GEO = {
    "MAKKAH": {"lat": 21.3891, "lon": 39.8579},
    "MADINAH": {"lat": 24.5247, "lon": 39.5692},
}


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula.

    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates

    Returns:
        Distance in meters
    """
    R = 6371000.0  # Earth radius in meters

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))


def umrah_distance_score(city: str, lat: float, lon: float) -> dict:
    """
    Calculate distance score from hotel to Haram/Nabawi.

    Args:
        city: MAKKAH or MADINAH
        lat: Hotel latitude
        lon: Hotel longitude

    Returns:
        Dict with distance_m, walk_min, distance_score (0-100)
    """
    if city.upper() == "MAKKAH":
        d = haversine_m(lat, lon, HARAM_LAT, HARAM_LON)
    else:
        d = haversine_m(lat, lon, NABAWI_LAT, NABAWI_LON)

    # Heuristic walking time: ~80 m/min (4.8 km/h)
    walk_min = d / 80.0

    # Score 0-100: closer = higher score
    # -1 point per 50 meters
    score = max(0, 100 - (d / 50.0))

    return {
        "distance_m": round(d),
        "walk_min": round(walk_min, 1),
        "distance_score": round(score, 1),
    }
