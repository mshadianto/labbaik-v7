"""
LABBAIK AI - Package Calculator
================================
Utility untuk menghitung biaya paket umrah dan margin.
"""

import os
import yaml
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from functools import lru_cache

logger = logging.getLogger(__name__)

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "config",
    "package_builder.yaml"
)


@dataclass
class PackageScenario:
    """Skenario paket umrah."""
    name: str = "Skenario 1"

    # Duration
    duration_days: int = 9
    nights_makkah: int = 4
    nights_madinah: int = 4

    # Hotels
    hotel_makkah_category: str = "bintang_4"
    hotel_makkah_price: int = 2500000
    hotel_madinah_category: str = "bintang_4"
    hotel_madinah_price: int = 1800000

    # Flight
    airline_code: str = "SV"
    flight_class: str = "economy"
    flight_price: int = 12000000
    origin_code: str = "CGK"
    origin_surcharge: int = 0

    # Transport
    intercity_transport: str = "haramain_train"
    intercity_price: int = 800000
    airport_transfer: str = "bus_group"
    airport_transfer_price: int = 150000

    # Room
    room_type: str = "quad"
    room_occupancy: int = 4
    room_multiplier: float = 1.0

    # Meals
    meal_type: str = "full_board"
    meal_price_per_day: int = 250000

    # Group size
    group_size: int = 45

    # Fixed costs (per person)
    visa_cost: int = 2500000
    insurance_cost: int = 350000
    handling_cost: int = 500000

    # Optional costs
    include_equipment: bool = True
    equipment_cost: int = 300000
    include_guide: bool = True
    guide_cost: int = 3000000  # per group
    include_ziarah: bool = True
    ziarah_cost: int = 500000

    # Margin
    margin_type: str = "percentage"  # percentage or fixed
    margin_percentage: float = 15.0
    margin_fixed: int = 0

    # Season
    season_multiplier: float = 1.0


@dataclass
class PackageCostBreakdown:
    """Breakdown biaya paket."""
    # Per person costs
    hotel_makkah: int = 0
    hotel_madinah: int = 0
    hotel_total: int = 0

    flight: int = 0
    transport: int = 0
    meals: int = 0

    visa: int = 0
    insurance: int = 0
    handling: int = 0
    equipment: int = 0
    guide_share: int = 0
    ziarah: int = 0

    # Totals
    cost_per_person: int = 0
    margin_per_person: int = 0
    selling_price_per_person: int = 0

    # Group totals
    total_cost: int = 0
    total_margin: int = 0
    total_revenue: int = 0

    # Details
    details: Dict[str, Any] = field(default_factory=dict)


@lru_cache(maxsize=1)
def load_package_config() -> Dict[str, Any]:
    """Load package builder configuration."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load package config: {e}")
        return {}


def get_config() -> Dict[str, Any]:
    """Get package builder config."""
    config = load_package_config()
    return config.get("package_builder", {})


def get_hotels(city: str) -> List[Dict[str, Any]]:
    """Get hotel options for a city."""
    config = get_config()
    hotels = config.get("hotels", {})
    return hotels.get(city.lower(), [])


def get_airlines() -> List[Dict[str, Any]]:
    """Get airline options."""
    config = get_config()
    return config.get("flights", {}).get("airlines", [])


def get_origins() -> List[Dict[str, Any]]:
    """Get departure city options."""
    config = get_config()
    return config.get("flights", {}).get("origins", [])


def get_transport_options(route: str = "makkah_madinah") -> List[Dict[str, Any]]:
    """Get transport options."""
    config = get_config()
    return config.get("transport", {}).get(route, [])


def get_room_types() -> List[Dict[str, Any]]:
    """Get room type options."""
    config = get_config()
    return config.get("room_types", [])


def get_meal_options() -> List[Dict[str, Any]]:
    """Get meal options."""
    config = get_config()
    return config.get("meals", [])


def get_fixed_costs() -> List[Dict[str, Any]]:
    """Get fixed cost items."""
    config = get_config()
    return config.get("fixed_costs", [])


def get_margin_presets() -> List[Dict[str, Any]]:
    """Get margin presets."""
    config = get_config()
    return config.get("margin_presets", [])


def get_durations() -> List[Dict[str, Any]]:
    """Get duration options."""
    config = get_config()
    return config.get("durations", [])


def calculate_package(scenario: PackageScenario) -> PackageCostBreakdown:
    """
    Calculate package costs and selling price.

    Args:
        scenario: Package scenario with all parameters

    Returns:
        PackageCostBreakdown with all calculated values
    """
    breakdown = PackageCostBreakdown()

    # Hotel costs (per person, based on room sharing)
    hotel_makkah_total = scenario.hotel_makkah_price * scenario.nights_makkah
    hotel_madinah_total = scenario.hotel_madinah_price * scenario.nights_madinah

    # Apply room multiplier and divide by occupancy
    breakdown.hotel_makkah = int(
        (hotel_makkah_total * scenario.room_multiplier * scenario.season_multiplier)
        / scenario.room_occupancy
    )
    breakdown.hotel_madinah = int(
        (hotel_madinah_total * scenario.room_multiplier * scenario.season_multiplier)
        / scenario.room_occupancy
    )
    breakdown.hotel_total = breakdown.hotel_makkah + breakdown.hotel_madinah

    # Flight (per person)
    breakdown.flight = scenario.flight_price + scenario.origin_surcharge

    # Transport (per person)
    breakdown.transport = scenario.intercity_price + scenario.airport_transfer_price

    # Meals (per person)
    total_days = scenario.duration_days
    breakdown.meals = scenario.meal_price_per_day * total_days

    # Fixed costs (per person)
    breakdown.visa = scenario.visa_cost
    breakdown.insurance = scenario.insurance_cost
    breakdown.handling = scenario.handling_cost

    # Optional costs
    if scenario.include_equipment:
        breakdown.equipment = scenario.equipment_cost

    if scenario.include_guide:
        breakdown.guide_share = int(scenario.guide_cost / scenario.group_size)

    if scenario.include_ziarah:
        breakdown.ziarah = scenario.ziarah_cost

    # Calculate total cost per person
    breakdown.cost_per_person = (
        breakdown.hotel_total +
        breakdown.flight +
        breakdown.transport +
        breakdown.meals +
        breakdown.visa +
        breakdown.insurance +
        breakdown.handling +
        breakdown.equipment +
        breakdown.guide_share +
        breakdown.ziarah
    )

    # Calculate margin
    if scenario.margin_type == "percentage":
        breakdown.margin_per_person = int(
            breakdown.cost_per_person * (scenario.margin_percentage / 100)
        )
    else:
        breakdown.margin_per_person = scenario.margin_fixed

    # Selling price
    breakdown.selling_price_per_person = (
        breakdown.cost_per_person + breakdown.margin_per_person
    )

    # Group totals
    breakdown.total_cost = breakdown.cost_per_person * scenario.group_size
    breakdown.total_margin = breakdown.margin_per_person * scenario.group_size
    breakdown.total_revenue = breakdown.selling_price_per_person * scenario.group_size

    # Store details for display
    breakdown.details = {
        "scenario_name": scenario.name,
        "duration": f"{scenario.duration_days} hari",
        "hotel_makkah": f"{scenario.nights_makkah} malam",
        "hotel_madinah": f"{scenario.nights_madinah} malam",
        "room_type": scenario.room_type,
        "airline": scenario.airline_code,
        "flight_class": scenario.flight_class,
        "origin": scenario.origin_code,
        "transport": scenario.intercity_transport,
        "meal": scenario.meal_type,
        "group_size": scenario.group_size,
        "margin_percentage": scenario.margin_percentage,
    }

    return breakdown


def format_currency(amount: int) -> str:
    """Format number as Indonesian Rupiah."""
    return f"Rp {amount:,.0f}".replace(",", ".")


def compare_scenarios(scenarios: List[PackageScenario]) -> List[Dict[str, Any]]:
    """
    Compare multiple package scenarios.

    Args:
        scenarios: List of package scenarios

    Returns:
        List of comparison results
    """
    results = []

    for scenario in scenarios:
        breakdown = calculate_package(scenario)
        results.append({
            "name": scenario.name,
            "cost": breakdown.cost_per_person,
            "margin": breakdown.margin_per_person,
            "selling_price": breakdown.selling_price_per_person,
            "margin_percent": scenario.margin_percentage,
            "group_revenue": breakdown.total_revenue,
            "group_margin": breakdown.total_margin,
            "breakdown": breakdown,
            "scenario": scenario,
        })

    return results


def generate_price_tiers(
    base_scenario: PackageScenario,
    margin_percentages: List[float] = [10, 15, 20, 25]
) -> List[Dict[str, Any]]:
    """
    Generate price tiers with different margins.

    Args:
        base_scenario: Base scenario
        margin_percentages: List of margin percentages

    Returns:
        List of price tier results
    """
    tiers = []

    for margin in margin_percentages:
        scenario = PackageScenario(
            **{k: v for k, v in base_scenario.__dict__.items()}
        )
        scenario.margin_percentage = margin
        breakdown = calculate_package(scenario)

        tiers.append({
            "margin_percent": margin,
            "cost": breakdown.cost_per_person,
            "margin": breakdown.margin_per_person,
            "selling_price": breakdown.selling_price_per_person,
        })

    return tiers
