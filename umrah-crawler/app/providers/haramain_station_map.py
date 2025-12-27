"""
LABBAIK AI - Haramain Station ID Mapping
=========================================
Station IDs discovered from sar.hhr.sa portlet.

Evidence from URL: idFromStation=1 (Makkah), idToStation=5 (Madinah)
"""

# Station ID mapping (discovered from portlet params)
HARAMAIN_STATIONS = {
    "MAKKAH": 1,
    "MADINAH": 5,
    # Future: add JEDDAH, KAEC when IDs discovered
    # "JEDDAH": ?,
    # "KAEC": ?,  # King Abdullah Economic City
}

# Reverse lookup
STATION_NAMES = {v: k for k, v in HARAMAIN_STATIONS.items()}

# Route combinations
ROUTES = {
    "MAKKAH_MADINAH": {"from_id": 1, "to_id": 5},
    "MADINAH_MAKKAH": {"from_id": 5, "to_id": 1},
}


def get_station_id(city: str) -> int:
    """Get station ID for a city."""
    city = city.upper().strip()
    if city not in HARAMAIN_STATIONS:
        raise ValueError(f"Unknown station: {city}. Known: {list(HARAMAIN_STATIONS.keys())}")
    return HARAMAIN_STATIONS[city]


def get_station_name(station_id: int) -> str:
    """Get city name for a station ID."""
    return STATION_NAMES.get(station_id, f"STATION_{station_id}")


def get_route_ids(route: str) -> tuple:
    """Get (from_id, to_id) for a route string."""
    route = route.upper().strip()
    if route in ROUTES:
        r = ROUTES[route]
        return r["from_id"], r["to_id"]

    # Try parsing "CITY1_CITY2" format
    parts = route.split("_")
    if len(parts) == 2:
        return get_station_id(parts[0]), get_station_id(parts[1])

    raise ValueError(f"Unknown route: {route}")
