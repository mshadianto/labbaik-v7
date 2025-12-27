"""
LABBAIK AI - Itinerary Builder V1.2
===================================
Transport recommendations Makkah <-> Madinah with buffer times.
"""

from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum

from .season_calendar import is_peak_season, get_season_calendar


class TransportMode(str, Enum):
    """Transport modes between cities."""
    TRAIN = "TRAIN"        # Haramain High Speed
    BUS = "BUS"            # SAPTCO VIP
    PRIVATE_CAR = "PRIVATE_CAR"
    UBER = "UBER"


class City(str, Enum):
    """Cities."""
    MAKKAH = "MAKKAH"
    MADINAH = "MADINAH"
    JEDDAH = "JEDDAH"


@dataclass
class TransportOption:
    """A transport option between cities."""
    mode: TransportMode
    operator: str
    from_city: City
    to_city: City
    duration_min: int
    price_sar: float
    price_range: Tuple[float, float]  # min, max
    frequency: str  # e.g., "Every 30 min", "4x daily"
    station_from: str
    station_to: str
    booking_url: Optional[str] = None
    notes: List[str] = field(default_factory=list)


@dataclass
class BufferTime:
    """Recommended buffer times."""
    hotel_to_station_min: int
    checkin_buffer_min: int
    total_min: int
    peak_extra_min: int = 0
    notes: List[str] = field(default_factory=list)


@dataclass
class ItinerarySegment:
    """A segment of the itinerary."""
    from_location: str
    to_location: str
    transport: TransportOption
    buffer: BufferTime
    recommended_departure: Optional[str] = None
    total_time_min: int = 0


@dataclass
class Itinerary:
    """Complete itinerary."""
    from_city: City
    to_city: City
    segments: List[ItinerarySegment]
    total_duration_min: int
    total_price_sar: float
    is_peak_season: bool
    recommendations: List[str] = field(default_factory=list)


# =============================================================================
# TRANSPORT DATA
# =============================================================================

TRANSPORT_OPTIONS: Dict[str, List[TransportOption]] = {
    "MAKKAH_MADINAH": [
        TransportOption(
            mode=TransportMode.TRAIN,
            operator="Haramain High Speed Railway",
            from_city=City.MAKKAH,
            to_city=City.MADINAH,
            duration_min=120,  # 2 hours
            price_sar=200,
            price_range=(150, 350),
            frequency="Every 30-60 min",
            station_from="Makkah Station (Al Rusaifah)",
            station_to="Madinah Station (Knowledge Economic City)",
            booking_url="https://sar.hhr.sa",
            notes=[
                "Tercepat dan paling nyaman",
                "Booking online di hhr.sa atau app SAR",
                "Bawa paspor untuk verifikasi",
                "Bagasi: 2x23kg + kabin 7kg",
            ]
        ),
        TransportOption(
            mode=TransportMode.BUS,
            operator="SAPTCO VIP",
            from_city=City.MAKKAH,
            to_city=City.MADINAH,
            duration_min=360,  # 5-6 hours
            price_sar=120,
            price_range=(100, 150),
            frequency="6x daily",
            station_from="SAPTCO Makkah Terminal",
            station_to="SAPTCO Madinah Terminal",
            booking_url="https://www.saptco.com.sa",
            notes=[
                "Lebih murah dari kereta",
                "Bus VIP AC dengan WiFi",
                "Ada toilet di bus",
                "Istirahat di rest area",
            ]
        ),
        TransportOption(
            mode=TransportMode.PRIVATE_CAR,
            operator="Private/Rental",
            from_city=City.MAKKAH,
            to_city=City.MADINAH,
            duration_min=300,  # 5 hours
            price_sar=600,
            price_range=(500, 1000),
            frequency="On demand",
            station_from="Hotel pickup",
            station_to="Hotel dropoff",
            notes=[
                "Fleksibel, door-to-door",
                "Bisa berhenti untuk ziarah",
                "Nego harga dengan driver",
                "Sharing dengan jamaah lain",
            ]
        ),
        TransportOption(
            mode=TransportMode.UBER,
            operator="Uber/Careem",
            from_city=City.MAKKAH,
            to_city=City.MADINAH,
            duration_min=300,
            price_sar=450,
            price_range=(400, 600),
            frequency="On demand",
            station_from="Hotel pickup",
            station_to="Hotel dropoff",
            notes=[
                "Booking via app",
                "Harga transparan",
                "Bisa surge pricing",
            ]
        ),
    ],
    "JEDDAH_MAKKAH": [
        TransportOption(
            mode=TransportMode.TRAIN,
            operator="Haramain High Speed Railway",
            from_city=City.JEDDAH,
            to_city=City.MAKKAH,
            duration_min=30,
            price_sar=75,
            price_range=(50, 100),
            frequency="Every 30 min",
            station_from="Jeddah Station (Sulaymaniyah)",
            station_to="Makkah Station",
            booking_url="https://sar.hhr.sa",
            notes=["Sangat cepat", "Dari airport naik bus/taksi ke stasiun dulu"]
        ),
        TransportOption(
            mode=TransportMode.BUS,
            operator="SAPTCO",
            from_city=City.JEDDAH,
            to_city=City.MAKKAH,
            duration_min=90,
            price_sar=50,
            price_range=(40, 80),
            frequency="Every 30 min",
            station_from="Jeddah Airport / SAPTCO Terminal",
            station_to="Makkah Terminal",
            notes=["Bus langsung dari airport", "Murah dan nyaman"]
        ),
        TransportOption(
            mode=TransportMode.UBER,
            operator="Uber/Careem",
            from_city=City.JEDDAH,
            to_city=City.MAKKAH,
            duration_min=75,
            price_sar=200,
            price_range=(150, 300),
            frequency="On demand",
            station_from="Airport/Hotel",
            station_to="Hotel Makkah",
            notes=["Door-to-door", "Lebih mahal tapi praktis"]
        ),
    ],
    "JEDDAH_MADINAH": [
        TransportOption(
            mode=TransportMode.TRAIN,
            operator="Haramain High Speed Railway",
            from_city=City.JEDDAH,
            to_city=City.MADINAH,
            duration_min=120,
            price_sar=200,
            price_range=(150, 300),
            frequency="Every 60 min",
            station_from="Jeddah Station",
            station_to="Madinah Station",
            booking_url="https://sar.hhr.sa",
            notes=["Direct train", "2 jam perjalanan"]
        ),
    ],
}

# Reverse routes
TRANSPORT_OPTIONS["MADINAH_MAKKAH"] = [
    TransportOption(
        mode=opt.mode,
        operator=opt.operator,
        from_city=City.MADINAH,
        to_city=City.MAKKAH,
        duration_min=opt.duration_min,
        price_sar=opt.price_sar,
        price_range=opt.price_range,
        frequency=opt.frequency,
        station_from=opt.station_to,
        station_to=opt.station_from,
        booking_url=opt.booking_url,
        notes=opt.notes,
    )
    for opt in TRANSPORT_OPTIONS["MAKKAH_MADINAH"]
]


# Buffer times by mode
BUFFER_TIMES: Dict[TransportMode, BufferTime] = {
    TransportMode.TRAIN: BufferTime(
        hotel_to_station_min=45,
        checkin_buffer_min=45,
        total_min=90,
        peak_extra_min=30,
        notes=[
            "Stasiun kereta di luar kota",
            "Perlu taksi/Uber ke stasiun",
            "Check-in 30 menit sebelum",
            "Security check seperti airport",
        ]
    ),
    TransportMode.BUS: BufferTime(
        hotel_to_station_min=30,
        checkin_buffer_min=30,
        total_min=60,
        peak_extra_min=20,
        notes=[
            "Terminal biasanya dekat hotel",
            "Check-in 20 menit sebelum",
        ]
    ),
    TransportMode.PRIVATE_CAR: BufferTime(
        hotel_to_station_min=0,
        checkin_buffer_min=15,
        total_min=15,
        peak_extra_min=0,
        notes=[
            "Pickup dari hotel langsung",
            "Siap 15 menit sebelum jadwal",
        ]
    ),
    TransportMode.UBER: BufferTime(
        hotel_to_station_min=0,
        checkin_buffer_min=15,
        total_min=15,
        peak_extra_min=0,
        notes=["Order 10-15 menit sebelum berangkat"]
    ),
}


class ItineraryBuilder:
    """Build transport itineraries."""

    def __init__(self):
        self.transport_options = TRANSPORT_OPTIONS
        self.buffer_times = BUFFER_TIMES

    def get_transport_options(
        self,
        from_city: str,
        to_city: str
    ) -> List[TransportOption]:
        """
        Get available transport options between cities.

        Args:
            from_city: Origin city
            to_city: Destination city

        Returns:
            List of TransportOption
        """
        key = f"{from_city.upper()}_{to_city.upper()}"
        return self.transport_options.get(key, [])

    def get_buffer(
        self,
        mode: TransportMode,
        travel_date: date = None
    ) -> BufferTime:
        """
        Get buffer time for transport mode.

        Args:
            mode: Transport mode
            travel_date: Travel date (for peak season check)

        Returns:
            BufferTime with recommendations
        """
        buffer = self.buffer_times.get(mode, BufferTime(
            hotel_to_station_min=30,
            checkin_buffer_min=30,
            total_min=60
        ))

        # Add peak season buffer
        if travel_date and is_peak_season(travel_date):
            extra = buffer.peak_extra_min
            return BufferTime(
                hotel_to_station_min=buffer.hotel_to_station_min + extra // 2,
                checkin_buffer_min=buffer.checkin_buffer_min + extra // 2,
                total_min=buffer.total_min + extra,
                peak_extra_min=extra,
                notes=buffer.notes + [
                    f"Peak season: +{extra} menit buffer tambahan",
                    "Antisipasi keramaian di stasiun/terminal",
                ]
            )

        return buffer

    def build_itinerary(
        self,
        from_city: str,
        to_city: str,
        mode: str = "TRAIN",
        travel_date: date = None,
        hotel_name: str = None
    ) -> Itinerary:
        """
        Build complete itinerary.

        Args:
            from_city: Origin city
            to_city: Destination city
            mode: Preferred transport mode
            travel_date: Travel date
            hotel_name: Origin hotel name (optional)

        Returns:
            Itinerary object
        """
        from_city = City(from_city.upper())
        to_city = City(to_city.upper())

        if travel_date is None:
            travel_date = date.today()

        # Get transport options
        options = self.get_transport_options(from_city.value, to_city.value)

        # Find preferred mode
        preferred_mode = TransportMode(mode.upper())
        transport = next(
            (o for o in options if o.mode == preferred_mode),
            options[0] if options else None
        )

        if not transport:
            return Itinerary(
                from_city=from_city,
                to_city=to_city,
                segments=[],
                total_duration_min=0,
                total_price_sar=0,
                is_peak_season=is_peak_season(travel_date),
                recommendations=["Tidak ada data transport untuk rute ini"]
            )

        # Get buffer
        buffer = self.get_buffer(transport.mode, travel_date)

        # Build segment
        segment = ItinerarySegment(
            from_location=hotel_name or f"Hotel di {from_city.value}",
            to_location=f"Hotel di {to_city.value}",
            transport=transport,
            buffer=buffer,
            total_time_min=transport.duration_min + buffer.total_min
        )

        # Build recommendations
        recommendations = self._build_recommendations(
            transport, buffer, travel_date
        )

        peak = is_peak_season(travel_date)

        return Itinerary(
            from_city=from_city,
            to_city=to_city,
            segments=[segment],
            total_duration_min=segment.total_time_min,
            total_price_sar=transport.price_sar,
            is_peak_season=peak,
            recommendations=recommendations
        )

    def _build_recommendations(
        self,
        transport: TransportOption,
        buffer: BufferTime,
        travel_date: date
    ) -> List[str]:
        """Build travel recommendations."""
        recs = []

        # Mode-specific
        if transport.mode == TransportMode.TRAIN:
            recs.append("Booking kereta 1-2 minggu sebelum di hhr.sa")
            recs.append("Seat business class lebih nyaman untuk perjalanan 2 jam")

        elif transport.mode == TransportMode.BUS:
            recs.append("Beli tiket online di saptco.com.sa")
            recs.append("Bawa snack dan air untuk perjalanan 5-6 jam")

        elif transport.mode in [TransportMode.PRIVATE_CAR, TransportMode.UBER]:
            recs.append("Nego harga sebelum berangkat")
            recs.append("Bisa request berhenti untuk ziarah (Bir Ali, dll)")

        # Buffer
        recs.append(f"Total waktu perjalanan: ~{transport.duration_min + buffer.total_min} menit")
        recs.append(f"Siapkan buffer {buffer.total_min} menit sebelum keberangkatan")

        # Peak season
        if is_peak_season(travel_date):
            calendar = get_season_calendar()
            season = calendar.get_season(travel_date)
            if season:
                recs.append(f"PEAK SEASON ({season.name}): Booking dan berangkat lebih awal!")

        return recs

    def compare_options(
        self,
        from_city: str,
        to_city: str,
        travel_date: date = None
    ) -> List[dict]:
        """
        Compare all transport options.

        Args:
            from_city: Origin city
            to_city: Destination city
            travel_date: Travel date

        Returns:
            List of option comparisons
        """
        options = self.get_transport_options(from_city, to_city)
        if travel_date is None:
            travel_date = date.today()

        comparisons = []
        for opt in options:
            buffer = self.get_buffer(opt.mode, travel_date)
            total_time = opt.duration_min + buffer.total_min

            comparisons.append({
                "mode": opt.mode.value,
                "operator": opt.operator,
                "duration_min": opt.duration_min,
                "buffer_min": buffer.total_min,
                "total_time_min": total_time,
                "price_sar": opt.price_sar,
                "price_range": f"{opt.price_range[0]}-{opt.price_range[1]} SAR",
                "frequency": opt.frequency,
                "station_from": opt.station_from,
                "station_to": opt.station_to,
                "notes": opt.notes,
                "booking_url": opt.booking_url,
                "recommended": opt.mode == TransportMode.TRAIN,
            })

        # Sort by total time
        comparisons.sort(key=lambda x: x["total_time_min"])

        return comparisons


# Singleton
_builder: Optional[ItineraryBuilder] = None


def get_itinerary_builder() -> ItineraryBuilder:
    """Get singleton ItineraryBuilder."""
    global _builder
    if _builder is None:
        _builder = ItineraryBuilder()
    return _builder


# Convenience functions
def build_itinerary(
    from_city: str,
    to_city: str,
    mode: str = "TRAIN",
    travel_date: date = None
) -> Itinerary:
    """Build itinerary."""
    return get_itinerary_builder().build_itinerary(
        from_city, to_city, mode, travel_date
    )


def compare_transport(
    from_city: str,
    to_city: str,
    travel_date: date = None
) -> List[dict]:
    """Compare transport options."""
    return get_itinerary_builder().compare_options(
        from_city, to_city, travel_date
    )


def itinerary_to_dict(itinerary: Itinerary) -> dict:
    """Convert Itinerary to dict for JSON response."""
    segments = []
    for seg in itinerary.segments:
        segments.append({
            "from": seg.from_location,
            "to": seg.to_location,
            "transport": {
                "mode": seg.transport.mode.value,
                "operator": seg.transport.operator,
                "duration_min": seg.transport.duration_min,
                "price_sar": seg.transport.price_sar,
                "station_from": seg.transport.station_from,
                "station_to": seg.transport.station_to,
                "notes": seg.transport.notes,
                "booking_url": seg.transport.booking_url,
            },
            "buffer": {
                "hotel_to_station_min": seg.buffer.hotel_to_station_min,
                "checkin_buffer_min": seg.buffer.checkin_buffer_min,
                "total_min": seg.buffer.total_min,
                "notes": seg.buffer.notes,
            },
            "total_time_min": seg.total_time_min,
        })

    return {
        "ok": True,
        "from_city": itinerary.from_city.value,
        "to_city": itinerary.to_city.value,
        "segments": segments,
        "summary": {
            "total_duration_min": itinerary.total_duration_min,
            "total_price_sar": itinerary.total_price_sar,
            "is_peak_season": itinerary.is_peak_season,
        },
        "recommendations": itinerary.recommendations,
    }
