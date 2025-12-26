"""Data normalization utilities."""
import re
from typing import Optional


def normalize_hotel_name(name: str) -> str:
    """
    Normalize hotel name for matching.

    Args:
        name: Raw hotel name

    Returns:
        Normalized lowercase name
    """
    if not name:
        return ""

    # Lowercase
    name = name.lower().strip()

    # Remove common suffixes
    suffixes = ["hotel", "hotels", "suites", "suite", "residence", "resort", "inn"]
    for suffix in suffixes:
        name = re.sub(rf'\b{suffix}\b', '', name)

    # Remove special characters
    name = re.sub(r'[^\w\s]', '', name)

    # Normalize whitespace
    name = re.sub(r'\s+', ' ', name).strip()

    return name


def normalize_city(city: str) -> str:
    """
    Normalize city name to standard format.

    Args:
        city: City name (various formats)

    Returns:
        Normalized city (MAKKAH or MADINAH)
    """
    city_lower = city.lower().strip()

    makkah_variants = ["makkah", "mecca", "mekka", "mekkah", "makka"]
    madinah_variants = ["madinah", "medina", "medinah", "madina"]

    if any(v in city_lower for v in makkah_variants):
        return "MAKKAH"
    elif any(v in city_lower for v in madinah_variants):
        return "MADINAH"

    return city.upper()


def extract_star_rating(text: str) -> Optional[int]:
    """
    Extract star rating from text.

    Args:
        text: Text containing star rating

    Returns:
        Star rating (1-5) or None
    """
    if not text:
        return None

    # Look for patterns like "5 star", "5-star", "5*"
    match = re.search(r'(\d)\s*[-\s]?\s*(?:star|stars|\*)', text.lower())
    if match:
        rating = int(match.group(1))
        if 1 <= rating <= 5:
            return rating

    return None
