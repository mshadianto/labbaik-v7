"""
LABBAIK AI - Amenity Intelligence V1.2
======================================
Extract shuttle, accessibility, family room, breakfast from amenities text.
"""

import re
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field


@dataclass
class AmenitySignals:
    """Extracted amenity signals from hotel data."""
    shuttle: bool = False
    shuttle_free: bool = False
    shuttle_haram: bool = False

    wheelchair_access: bool = False
    elevator: bool = False

    family_room: bool = False
    connecting_rooms: bool = False
    suite: bool = False

    breakfast: bool = False
    breakfast_free: bool = False
    restaurant: bool = False

    wifi: bool = False
    wifi_free: bool = False

    parking: bool = False
    parking_free: bool = False

    pool: bool = False
    gym: bool = False
    spa: bool = False

    laundry: bool = False
    room_service: bool = False
    concierge: bool = False

    prayer_room: bool = False
    quran: bool = False

    air_conditioning: bool = False
    minibar: bool = False
    safe: bool = False

    # Computed
    score: int = 0
    priority_score: int = 0  # Weighted for Umrah relevance
    raw_matches: List[str] = field(default_factory=list)


# =============================================================================
# EXTRACTION RULES
# =============================================================================

EXTRACTION_RULES: Dict[str, List[str]] = {
    # Shuttle & Transport
    "shuttle": [
        r"\bshuttle\b",
        r"\bhotel shuttle\b",
        r"\btransfer\b",
        r"\btransport(ation)?\b",
        r"\bpick[- ]?up\b",
    ],
    "shuttle_free": [
        r"\bfree shuttle\b",
        r"\bcomplimentary shuttle\b",
        r"\bshuttle.*free\b",
        r"\bfree.*transport\b",
    ],
    "shuttle_haram": [
        r"\bshuttle.*haram\b",
        r"\bto (al[- ])?haram\b",
        r"\bharam.*shuttle\b",
        r"\bmasjid(il)? haram\b",
        r"\bto mosque\b",
        r"\bmosque shuttle\b",
    ],

    # Accessibility
    "wheelchair_access": [
        r"\bwheelchair\b",
        r"\baccessib(le|ility)\b",
        r"\bdisabled\b",
        r"\bhandicap\b",
        r"\bbarrier[- ]?free\b",
        r"\bmobility\b",
    ],
    "elevator": [
        r"\belevator\b",
        r"\blift\b",
    ],

    # Room Types
    "family_room": [
        r"\bfamily room\b",
        r"\bfamily suite\b",
        r"\bfamily\b",
        r"\btriple room\b",
        r"\bquad room\b",
    ],
    "connecting_rooms": [
        r"\bconnecting room\b",
        r"\badjoining room\b",
    ],
    "suite": [
        r"\bsuite\b",
        r"\bjunior suite\b",
        r"\bexecutive suite\b",
    ],

    # Food & Dining
    "breakfast": [
        r"\bbreakfast\b",
        r"\bmorning meal\b",
    ],
    "breakfast_free": [
        r"\bfree breakfast\b",
        r"\bbreakfast included\b",
        r"\bcomplimentary breakfast\b",
        r"\bincl.*breakfast\b",
        r"\bbreakfast.*incl\b",
    ],
    "restaurant": [
        r"\brestaurant\b",
        r"\bdining\b",
        r"\bbuffet\b",
        r"\bcafe\b",
        r"\bcafeteria\b",
    ],

    # Internet
    "wifi": [
        r"\bwi[- ]?fi\b",
        r"\binternet\b",
        r"\bwireless\b",
    ],
    "wifi_free": [
        r"\bfree wi[- ]?fi\b",
        r"\bcomplimentary.*internet\b",
        r"\bwi[- ]?fi.*free\b",
    ],

    # Parking
    "parking": [
        r"\bparking\b",
        r"\bcar park\b",
        r"\bvalet\b",
    ],
    "parking_free": [
        r"\bfree parking\b",
        r"\bcomplimentary parking\b",
    ],

    # Facilities
    "pool": [
        r"\bpool\b",
        r"\bswimming\b",
    ],
    "gym": [
        r"\bgym\b",
        r"\bfitness\b",
        r"\bexercise\b",
        r"\bworkout\b",
    ],
    "spa": [
        r"\bspa\b",
        r"\bmassage\b",
        r"\bwellness\b",
        r"\bsauna\b",
    ],

    # Services
    "laundry": [
        r"\blaundry\b",
        r"\bdry clean\b",
        r"\bwashing\b",
    ],
    "room_service": [
        r"\broom service\b",
        r"\bin[- ]?room dining\b",
    ],
    "concierge": [
        r"\bconcierge\b",
        r"\b24[- ]?hour.*desk\b",
        r"\breception\b",
    ],

    # Religious
    "prayer_room": [
        r"\bprayer room\b",
        r"\bmusholla\b",
        r"\bmasjid\b",
        r"\bmosque\b",
    ],
    "quran": [
        r"\bquran\b",
        r"\bqur'?an\b",
        r"\bholy book\b",
    ],

    # Room Amenities
    "air_conditioning": [
        r"\bair[- ]?condition\b",
        r"\ba/?c\b",
        r"\bclimate control\b",
    ],
    "minibar": [
        r"\bminibar\b",
        r"\bmini[- ]?fridge\b",
        r"\brefrigerator\b",
    ],
    "safe": [
        r"\bsafe\b",
        r"\bsafety box\b",
        r"\bsecurity box\b",
    ],
}

# Priority weights for Umrah relevance
UMRAH_PRIORITY_WEIGHTS = {
    "shuttle_haram": 10,
    "shuttle_free": 8,
    "shuttle": 6,
    "wheelchair_access": 5,
    "elevator": 3,
    "breakfast_free": 5,
    "breakfast": 3,
    "family_room": 4,
    "connecting_rooms": 4,
    "wifi_free": 3,
    "wifi": 2,
    "prayer_room": 3,
    "quran": 2,
    "laundry": 2,
    "air_conditioning": 2,
    "restaurant": 2,
    "room_service": 1,
    "concierge": 1,
}


def extract_signals(text: str) -> AmenitySignals:
    """
    Extract amenity signals from text.

    Args:
        text: Combined amenities/description text

    Returns:
        AmenitySignals with detected features
    """
    if not text:
        return AmenitySignals()

    t = text.lower()
    signals = AmenitySignals()
    matches = []

    for key, patterns in EXTRACTION_RULES.items():
        found = False
        for pattern in patterns:
            if re.search(pattern, t):
                found = True
                matches.append(f"{key}:{pattern}")
                break

        if found and hasattr(signals, key):
            setattr(signals, key, True)

    # Calculate scores
    signals.score = sum(
        1 for k in EXTRACTION_RULES.keys()
        if hasattr(signals, k) and getattr(signals, k)
    )

    signals.priority_score = sum(
        UMRAH_PRIORITY_WEIGHTS.get(k, 1)
        for k in EXTRACTION_RULES.keys()
        if hasattr(signals, k) and getattr(signals, k)
    )

    signals.raw_matches = matches

    return signals


def signals_to_dict(signals: AmenitySignals) -> dict:
    """Convert AmenitySignals to dictionary."""
    return {
        "shuttle": signals.shuttle,
        "shuttle_free": signals.shuttle_free,
        "shuttle_haram": signals.shuttle_haram,
        "wheelchair_access": signals.wheelchair_access,
        "elevator": signals.elevator,
        "family_room": signals.family_room,
        "connecting_rooms": signals.connecting_rooms,
        "suite": signals.suite,
        "breakfast": signals.breakfast,
        "breakfast_free": signals.breakfast_free,
        "restaurant": signals.restaurant,
        "wifi": signals.wifi,
        "wifi_free": signals.wifi_free,
        "parking": signals.parking,
        "parking_free": signals.parking_free,
        "pool": signals.pool,
        "gym": signals.gym,
        "spa": signals.spa,
        "laundry": signals.laundry,
        "room_service": signals.room_service,
        "concierge": signals.concierge,
        "prayer_room": signals.prayer_room,
        "quran": signals.quran,
        "air_conditioning": signals.air_conditioning,
        "minibar": signals.minibar,
        "safe": signals.safe,
        "score": signals.score,
        "priority_score": signals.priority_score,
    }


def get_highlight_amenities(signals: AmenitySignals) -> List[str]:
    """
    Get highlighted amenities for display.

    Args:
        signals: Extracted signals

    Returns:
        List of highlight strings
    """
    highlights = []

    if signals.shuttle_haram:
        highlights.append("Shuttle ke Haram")
    elif signals.shuttle_free:
        highlights.append("Free Shuttle")
    elif signals.shuttle:
        highlights.append("Shuttle Available")

    if signals.wheelchair_access:
        highlights.append("Wheelchair Access")

    if signals.breakfast_free:
        highlights.append("Free Breakfast")
    elif signals.breakfast:
        highlights.append("Breakfast Available")

    if signals.family_room:
        highlights.append("Family Room")

    if signals.wifi_free:
        highlights.append("Free WiFi")

    if signals.prayer_room:
        highlights.append("Prayer Room")

    return highlights


def filter_hotels_by_amenity(
    hotels: List[dict],
    required: List[str]
) -> List[dict]:
    """
    Filter hotels by required amenities.

    Args:
        hotels: List of hotel dicts with 'amenity_signals'
        required: List of required amenity keys

    Returns:
        Filtered hotel list
    """
    result = []

    for hotel in hotels:
        signals = hotel.get("amenity_signals", {})
        if all(signals.get(r) for r in required):
            result.append(hotel)

    return result


def rank_hotels_by_amenities(
    hotels: List[dict],
    weights: Dict[str, int] = None
) -> List[dict]:
    """
    Rank hotels by amenity priority score.

    Args:
        hotels: List of hotel dicts
        weights: Custom weights (optional)

    Returns:
        Sorted hotel list (highest score first)
    """
    w = weights or UMRAH_PRIORITY_WEIGHTS

    def score(hotel):
        signals = hotel.get("amenity_signals", {})
        return sum(
            w.get(k, 1)
            for k, v in signals.items()
            if v is True
        )

    return sorted(hotels, key=score, reverse=True)
