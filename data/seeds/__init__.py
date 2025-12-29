"""
LABBAIK AI - Seed Data Module
=============================
Test datasets for Labbaik features.

Available datasets:
- umrah_packages.json: 25 Umrah packages from various travel agents
- hotels.json: 40 hotels in Makkah & Madinah
- flights.json: 30 flight routes from Indonesia to Saudi Arabia
- travel_agents.json: 15 travel agents with muthawwif data
- users.json: 15 test users with different roles
- faq_knowledge.json: 50 FAQs and glossary for Umrah

Usage:
    from data.seeds import load_packages, load_hotels, load_all_seeds

    # Load specific dataset
    packages = load_packages()

    # Load all seeds to database
    from data.seeds.seed_loader import SeedLoader
    loader = SeedLoader()
    loader.load_all()
"""

import json
from pathlib import Path
from typing import Dict, Any, List

SEEDS_DIR = Path(__file__).parent


def _load_json(filename: str) -> Dict[str, Any]:
    """Load JSON file from seeds directory."""
    filepath = SEEDS_DIR / filename
    if not filepath.exists():
        return {}

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_packages() -> List[Dict]:
    """Load Umrah packages dataset."""
    data = _load_json("umrah_packages.json")
    return data.get("packages", [])


def load_hotels() -> List[Dict]:
    """Load hotels dataset."""
    data = _load_json("hotels.json")
    return data.get("hotels", [])


def load_flights() -> List[Dict]:
    """Load flights dataset."""
    data = _load_json("flights.json")
    return data.get("flights", [])


def load_travel_agents() -> List[Dict]:
    """Load travel agents dataset."""
    data = _load_json("travel_agents.json")
    return data.get("travel_agents", [])


def load_users() -> List[Dict]:
    """Load users dataset."""
    data = _load_json("users.json")
    return data.get("users", [])


def load_faqs() -> List[Dict]:
    """Load FAQ dataset."""
    data = _load_json("faq_knowledge.json")
    return data.get("faqs", [])


def load_glossary() -> List[Dict]:
    """Load glossary dataset."""
    data = _load_json("faq_knowledge.json")
    return data.get("glossary", [])


def get_package_by_id(package_id: str) -> Dict:
    """Get package by ID."""
    packages = load_packages()
    for pkg in packages:
        if pkg.get("id") == package_id:
            return pkg
    return {}


def get_hotel_by_id(hotel_id: str) -> Dict:
    """Get hotel by ID."""
    hotels = load_hotels()
    for hotel in hotels:
        if hotel.get("id") == hotel_id:
            return hotel
    return {}


def search_packages(
    max_price: int = None,
    min_stars: int = None,
    departure_city: str = None,
    category: str = None
) -> List[Dict]:
    """Search packages with filters."""
    packages = load_packages()
    results = []

    for pkg in packages:
        # Price filter
        if max_price and pkg.get("price_idr", 0) > max_price:
            continue

        # Stars filter (check hotel_makkah)
        if min_stars:
            makkah_stars = pkg.get("hotel_makkah", {}).get("stars", 0)
            if isinstance(pkg.get("hotel_makkah"), dict):
                makkah_stars = pkg["hotel_makkah"].get("stars", 0)
            if makkah_stars < min_stars:
                continue

        # Departure city filter
        if departure_city and pkg.get("departure_city", "").lower() != departure_city.lower():
            continue

        # Category filter
        if category and pkg.get("category", "").lower() != category.lower():
            continue

        results.append(pkg)

    return results


def search_hotels(
    city: str = None,
    min_stars: int = None,
    max_distance: int = None
) -> List[Dict]:
    """Search hotels with filters."""
    hotels = load_hotels()
    results = []

    for hotel in hotels:
        # City filter
        if city and hotel.get("city", "").lower() != city.lower():
            continue

        # Stars filter
        if min_stars and hotel.get("stars", 0) < min_stars:
            continue

        # Distance filter
        if max_distance and hotel.get("distance_to_haram_m", 0) > max_distance:
            continue

        results.append(hotel)

    return results


__all__ = [
    "load_packages",
    "load_hotels",
    "load_flights",
    "load_travel_agents",
    "load_users",
    "load_faqs",
    "load_glossary",
    "get_package_by_id",
    "get_hotel_by_id",
    "search_packages",
    "search_hotels",
]
