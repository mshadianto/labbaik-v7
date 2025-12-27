"""
LABBAIK AI - Itinerary Service V1.3
===================================
Real ETA calculation: hotel → station/terminal → departure.
Uses OSRM for walking routes, integrates with transport schedules.
"""

import logging
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

import httpx

logger = logging.getLogger(__name__)

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class GeoPoint:
    """Geographic point."""
    lat: float
    lon: float
    name: str = ""

    def is_valid(self) -> bool:
        return (
            self.lat is not None and
            self.lon is not None and
            -90 <= self.lat <= 90 and
            -180 <= self.lon <= 180
        )


@dataclass
class WalkingRoute:
    """Walking route from OSRM."""
    distance_m: int
    duration_min: int
    geometry: Optional[str] = None  # Polyline for map display


@dataclass
class TransportPOI:
    """Transport point of interest (station/terminal)."""
    id: str
    name: str
    name_ar: str
    city: str
    poi_type: str  # 'TRAIN_STATION', 'BUS_TERMINAL'
    lat: float
    lon: float
    address: str = ""


@dataclass
class ItineraryLeg:
    """Single leg of an itinerary."""
    leg_type: str  # 'WALK', 'TRAIN', 'BUS', 'TAXI'
    from_name: str
    to_name: str
    distance_m: Optional[int] = None
    duration_min: Optional[int] = None
    depart_time: Optional[datetime] = None
    arrive_time: Optional[datetime] = None
    price_sar: Optional[float] = None
    notes: List[str] = field(default_factory=list)


@dataclass
class Itinerary:
    """Complete itinerary from hotel to destination."""
    from_hotel: Dict
    to_city: str
    mode: str  # 'TRAIN', 'BUS'
    legs: List[ItineraryLeg] = field(default_factory=list)
    total_duration_min: int = 0
    total_price_sar: float = 0
    recommended_buffer_min: int = 60
    departure_poi: Optional[TransportPOI] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "from_hotel": self.from_hotel,
            "to_city": self.to_city,
            "mode": self.mode,
            "legs": [asdict(leg) for leg in self.legs],
            "total_duration_min": self.total_duration_min,
            "total_price_sar": self.total_price_sar,
            "recommended_buffer_min": self.recommended_buffer_min,
            "departure_poi": asdict(self.departure_poi) if self.departure_poi else None,
            "notes": self.notes,
        }


# =============================================================================
# TRANSPORT POIs (Stations/Terminals)
# =============================================================================

# Hardcoded POIs (also in database, but kept here for fallback)
TRANSPORT_POIS: List[TransportPOI] = [
    # Makkah
    TransportPOI(
        id="haramain_makkah",
        name="Makkah Haramain Station",
        name_ar="محطة مكة المكرمة",
        city="MAKKAH",
        poi_type="TRAIN_STATION",
        lat=21.4106,
        lon=39.8739,
        address="Al Rusayfah, Makkah"
    ),
    TransportPOI(
        id="saptco_makkah",
        name="SAPTCO Makkah Terminal",
        name_ar="محطة سابتكو مكة",
        city="MAKKAH",
        poi_type="BUS_TERMINAL",
        lat=21.4225,
        lon=39.8262,
        address="Al Aziziyah, Makkah"
    ),

    # Madinah
    TransportPOI(
        id="haramain_madinah",
        name="Madinah Haramain Station",
        name_ar="محطة المدينة المنورة",
        city="MADINAH",
        poi_type="TRAIN_STATION",
        lat=24.5530,
        lon=39.7045,
        address="Knowledge Economic City, Madinah"
    ),
    TransportPOI(
        id="saptco_madinah",
        name="SAPTCO Madinah Terminal",
        name_ar="محطة سابتكو المدينة",
        city="MADINAH",
        poi_type="BUS_TERMINAL",
        lat=24.4672,
        lon=39.6024,
        address="Central Area, Madinah"
    ),
]


def get_pois_by_city(city: str) -> List[TransportPOI]:
    """Get all POIs for a city."""
    return [p for p in TRANSPORT_POIS if p.city.upper() == city.upper()]


def get_poi_by_type(city: str, poi_type: str) -> Optional[TransportPOI]:
    """Get specific POI by type."""
    for p in TRANSPORT_POIS:
        if p.city.upper() == city.upper() and p.poi_type == poi_type:
            return p
    return None


# =============================================================================
# DISTANCE & ROUTING
# =============================================================================

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in meters."""
    R = 6371000  # Earth radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2 +
        math.cos(phi1) * math.cos(phi2) *
        math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


async def get_walking_route(
    from_lat: float,
    from_lon: float,
    to_lat: float,
    to_lon: float,
    osrm_url: str = "https://router.project-osrm.org"
) -> Optional[WalkingRoute]:
    """
    Get walking route from OSRM.

    Args:
        from_lat, from_lon: Start coordinates
        to_lat, to_lon: End coordinates
        osrm_url: OSRM server URL

    Returns:
        WalkingRoute or None if failed
    """
    url = (
        f"{osrm_url}/route/v1/foot/"
        f"{from_lon},{from_lat};{to_lon},{to_lat}"
        f"?overview=simplified&geometries=polyline"
    )

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()

            if data.get("code") != "Ok":
                return None

            route = data.get("routes", [{}])[0]
            distance = route.get("distance", 0)  # meters
            duration = route.get("duration", 0)  # seconds
            geometry = route.get("geometry")

            return WalkingRoute(
                distance_m=int(distance),
                duration_min=int(duration / 60) + 1,  # Round up
                geometry=geometry
            )

    except Exception as e:
        logger.warning(f"OSRM request failed: {e}")
        # Fallback: estimate based on haversine distance
        # Assume walking speed of 5 km/h with 1.3x detour factor
        straight_dist = haversine_distance(from_lat, from_lon, to_lat, to_lon)
        walking_dist = straight_dist * 1.3
        walking_time = walking_dist / (5000 / 60)  # 5 km/h in m/min

        return WalkingRoute(
            distance_m=int(walking_dist),
            duration_min=int(walking_time) + 1
        )


async def nearest_poi(
    city: str,
    poi_type: str,
    hotel_lat: float,
    hotel_lon: float
) -> Optional[Tuple[TransportPOI, WalkingRoute]]:
    """
    Find nearest POI and calculate walking route.

    Args:
        city: 'MAKKAH' or 'MADINAH'
        poi_type: 'TRAIN_STATION' or 'BUS_TERMINAL'
        hotel_lat, hotel_lon: Hotel coordinates

    Returns:
        (poi, walking_route) or None
    """
    poi = get_poi_by_type(city, poi_type)
    if not poi:
        return None

    route = await get_walking_route(
        hotel_lat, hotel_lon,
        poi.lat, poi.lon
    )

    if route:
        return (poi, route)
    return None


# =============================================================================
# ITINERARY BUILDER
# =============================================================================

class ItineraryBuilder:
    """Build complete itineraries with real ETAs."""

    def __init__(self):
        self._buffer_rules = {
            "TRAIN": 60,   # 1 hour before departure
            "BUS": 40,     # 40 min before departure
        }
        self._peak_season_extra = 30  # Extra buffer during peak

    async def build(
        self,
        hotel: Dict,
        to_city: str,
        mode: str = "TRAIN",
        travel_date: Optional[datetime] = None,
        is_peak_season: bool = False
    ) -> Itinerary:
        """
        Build complete itinerary from hotel to destination city.

        Args:
            hotel: Hotel dict with lat, lon, city, name
            to_city: Destination city
            mode: 'TRAIN' or 'BUS'
            travel_date: Optional travel date
            is_peak_season: Whether it's peak season (extra buffer)

        Returns:
            Complete Itinerary object
        """
        hotel_lat = hotel.get("lat") or hotel.get("latitude")
        hotel_lon = hotel.get("lon") or hotel.get("longitude")
        hotel_city = hotel.get("city", "").upper()
        hotel_name = hotel.get("name", "Hotel")

        if not hotel_lat or not hotel_lon:
            return self._fallback_itinerary(hotel, to_city, mode)

        # Determine POI type based on mode
        poi_type = "TRAIN_STATION" if mode == "TRAIN" else "BUS_TERMINAL"

        # Get nearest POI and walking route
        poi_result = await nearest_poi(hotel_city, poi_type, hotel_lat, hotel_lon)

        if not poi_result:
            return self._fallback_itinerary(hotel, to_city, mode)

        poi, walk_route = poi_result

        # Build legs
        legs = []

        # Leg 1: Walk to station/terminal
        legs.append(ItineraryLeg(
            leg_type="WALK",
            from_name=hotel_name,
            to_name=poi.name,
            distance_m=walk_route.distance_m,
            duration_min=walk_route.duration_min,
            notes=["Jalan kaki ke stasiun/terminal"]
        ))

        # Leg 2: Transport (train/bus)
        transport_duration = 120 if mode == "TRAIN" else 300  # 2h train, 5h bus
        transport_price = 75 if mode == "TRAIN" else 80  # Approximate

        dest_poi = get_poi_by_type(to_city.upper(), poi_type)
        dest_name = dest_poi.name if dest_poi else to_city

        legs.append(ItineraryLeg(
            leg_type=mode,
            from_name=poi.name,
            to_name=dest_name,
            duration_min=transport_duration,
            price_sar=transport_price,
            notes=[
                f"Haramain Train" if mode == "TRAIN" else "SAPTCO Bus",
                f"Durasi ~{transport_duration // 60} jam"
            ]
        ))

        # Calculate totals
        total_duration = walk_route.duration_min + transport_duration
        total_price = transport_price

        # Calculate buffer
        base_buffer = self._buffer_rules.get(mode, 60)
        buffer = base_buffer + walk_route.duration_min
        if is_peak_season:
            buffer += self._peak_season_extra

        # Build notes
        notes = [
            f"Buffer = waktu jalan ({walk_route.duration_min} min) + check-in ({base_buffer} min)",
        ]
        if is_peak_season:
            notes.append(f"Peak season: tambah {self._peak_season_extra} min extra buffer")

        return Itinerary(
            from_hotel={
                "name": hotel_name,
                "city": hotel_city,
                "lat": hotel_lat,
                "lon": hotel_lon,
            },
            to_city=to_city.upper(),
            mode=mode,
            legs=legs,
            total_duration_min=total_duration,
            total_price_sar=total_price,
            recommended_buffer_min=buffer,
            departure_poi=poi,
            notes=notes
        )

    def _fallback_itinerary(
        self,
        hotel: Dict,
        to_city: str,
        mode: str
    ) -> Itinerary:
        """Create fallback itinerary when coordinates unavailable."""
        hotel_city = hotel.get("city", "").upper()
        hotel_name = hotel.get("name", "Hotel")

        # Use static estimates
        walk_time = 30  # Assume 30 min walk
        transport_duration = 120 if mode == "TRAIN" else 300
        transport_price = 75 if mode == "TRAIN" else 80

        poi_type = "TRAIN_STATION" if mode == "TRAIN" else "BUS_TERMINAL"
        poi = get_poi_by_type(hotel_city, poi_type)

        legs = [
            ItineraryLeg(
                leg_type="WALK",
                from_name=hotel_name,
                to_name=poi.name if poi else "Stasiun",
                duration_min=walk_time,
                notes=["Estimasi (koordinat hotel tidak tersedia)"]
            ),
            ItineraryLeg(
                leg_type=mode,
                from_name=poi.name if poi else "Stasiun",
                to_name=to_city,
                duration_min=transport_duration,
                price_sar=transport_price,
            )
        ]

        return Itinerary(
            from_hotel={"name": hotel_name, "city": hotel_city},
            to_city=to_city.upper(),
            mode=mode,
            legs=legs,
            total_duration_min=walk_time + transport_duration,
            total_price_sar=transport_price,
            recommended_buffer_min=90,  # Conservative buffer
            departure_poi=poi,
            notes=["Estimasi buffer (koordinat hotel tidak tersedia)"]
        )


# Singleton
_builder: Optional[ItineraryBuilder] = None


def get_itinerary_builder() -> ItineraryBuilder:
    """Get or create ItineraryBuilder singleton."""
    global _builder
    if _builder is None:
        _builder = ItineraryBuilder()
    return _builder


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

async def build_itinerary_real(
    hotel: Dict,
    to_city: str,
    mode: str = "TRAIN",
    is_peak_season: bool = False
) -> Dict:
    """
    Build itinerary and return as dictionary.

    Args:
        hotel: Hotel dict with lat, lon, city, name
        to_city: Destination city
        mode: 'TRAIN' or 'BUS'
        is_peak_season: Whether peak season

    Returns:
        Itinerary as dictionary
    """
    builder = get_itinerary_builder()
    itinerary = await builder.build(
        hotel=hotel,
        to_city=to_city,
        mode=mode,
        is_peak_season=is_peak_season
    )
    return itinerary.to_dict()


async def compare_transport_options(
    hotel: Dict,
    to_city: str,
    is_peak_season: bool = False
) -> Dict:
    """
    Compare train vs bus options for the same route.

    Returns comparison dict.
    """
    builder = get_itinerary_builder()

    train_itin = await builder.build(hotel, to_city, "TRAIN", is_peak_season=is_peak_season)
    bus_itin = await builder.build(hotel, to_city, "BUS", is_peak_season=is_peak_season)

    return {
        "train": {
            "total_duration_min": train_itin.total_duration_min,
            "total_price_sar": train_itin.total_price_sar,
            "recommended_buffer_min": train_itin.recommended_buffer_min,
        },
        "bus": {
            "total_duration_min": bus_itin.total_duration_min,
            "total_price_sar": bus_itin.total_price_sar,
            "recommended_buffer_min": bus_itin.recommended_buffer_min,
        },
        "recommendation": {
            "fastest": "TRAIN",
            "cheapest": "BUS" if bus_itin.total_price_sar < train_itin.total_price_sar else "TRAIN",
            "best_value": "TRAIN",  # Generally train is best value for Makkah-Madinah
        },
        "notes": [
            "Train lebih cepat (~2 jam vs ~5 jam bus)",
            "Bus lebih murah tapi perjalanan lebih lama",
            "Train lebih nyaman untuk keluarga/lansia"
        ]
    }
