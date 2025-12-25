"""
LABBAIK AI v6.0 - Cost Calculator Service
=========================================
Service for calculating Umrah trip costs.
"""

from datetime import date, datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging

from core.constants import CostConstants, INDONESIA_CITIES
from data.models import (
    CostSimulationInput,
    CostBreakdown,
    CostSimulationResult,
    HotelStarRating,
    PackageType,
)

logger = logging.getLogger(__name__)


# =============================================================================
# SEASON DETERMINATION
# =============================================================================

def get_season_type(departure_date: date) -> tuple[str, float]:
    """
    Determine season type and multiplier based on departure date.
    
    Args:
        departure_date: Trip departure date
    
    Returns:
        Tuple of (season_type, multiplier)
    """
    month = departure_date.month
    
    # Ramadan periods (approximate - should use Hijri calendar)
    # This is simplified; real implementation should use Islamic calendar
    ramadan_months = [3, 4]  # March-April 2025 approximate
    
    # School holiday periods (Indonesia)
    school_holiday_months = [6, 7, 12]
    
    # Peak periods
    peak_months = [1]  # Around Maulid Nabi
    
    if month in ramadan_months:
        return "peak", CostConstants.SEASONAL_MULTIPLIERS["peak"]
    elif month in school_holiday_months:
        return "high", CostConstants.SEASONAL_MULTIPLIERS["high"]
    elif month in peak_months:
        return "high", CostConstants.SEASONAL_MULTIPLIERS["high"]
    elif month in [2, 5, 8, 9, 10, 11]:
        return "regular", CostConstants.SEASONAL_MULTIPLIERS["regular"]
    else:
        return "low", CostConstants.SEASONAL_MULTIPLIERS["low"]


def get_flight_cost(departure_city: str) -> float:
    """
    Get flight cost for departure city.
    
    Args:
        departure_city: City name
    
    Returns:
        Flight cost in IDR
    """
    return CostConstants.FLIGHT_COSTS.get(
        departure_city, 
        CostConstants.FLIGHT_COSTS["Jakarta"]  # Default to Jakarta
    )


def get_hotel_cost_per_night(city: str, star_rating: int) -> float:
    """
    Get hotel cost per night.
    
    Args:
        city: City name (makkah/madinah)
        star_rating: Hotel star rating (2-5)
    
    Returns:
        Cost per night in IDR
    """
    rating_enum = HotelStarRating(star_rating)
    
    if city.lower() == "makkah":
        return CostConstants.HOTEL_RATES_MAKKAH.get(rating_enum, 1_500_000)
    else:
        return CostConstants.HOTEL_RATES_MADINAH.get(rating_enum, 1_200_000)


# =============================================================================
# COST CALCULATOR
# =============================================================================

def calculate_umrah_cost(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate total Umrah trip cost.
    
    Args:
        input_data: Cost simulation input data
    
    Returns:
        Cost simulation result as dictionary
    """
    # Parse input
    if isinstance(input_data, CostSimulationInput):
        sim_input = input_data
    else:
        # Convert dict to model
        sim_input = CostSimulationInput(
            departure_city=input_data.get("departure_city", "Jakarta"),
            departure_date=input_data.get("departure_date", date.today()),
            return_date=input_data.get("return_date", date.today()),
            traveler_count=input_data.get("traveler_count", 1),
            hotel_makkah_star=HotelStarRating(input_data.get("hotel_makkah_star", 3)),
            hotel_madinah_star=HotelStarRating(input_data.get("hotel_madinah_star", 3)),
            days_makkah=input_data.get("days_makkah", 5),
            days_madinah=input_data.get("days_madinah", 4),
            package_type=PackageType(input_data.get("package_type", "reguler")),
            include_visa=input_data.get("include_visa", True),
            include_insurance=input_data.get("include_insurance", True),
            include_mutawif=input_data.get("include_mutawif", True),
        )
    
    # Get season info
    season_type, season_multiplier = get_season_type(sim_input.departure_date)
    
    # Calculate individual costs
    flight_cost = get_flight_cost(sim_input.departure_city)
    
    hotel_makkah_cost = (
        get_hotel_cost_per_night("makkah", sim_input.hotel_makkah_star.value) 
        * sim_input.days_makkah
    )
    
    hotel_madinah_cost = (
        get_hotel_cost_per_night("madinah", sim_input.hotel_madinah_star.value) 
        * sim_input.days_madinah
    )
    
    visa_cost = CostConstants.VISA_COST if sim_input.include_visa else 0
    insurance_cost = CostConstants.TRAVEL_INSURANCE if sim_input.include_insurance else 0
    
    mutawif_cost = (
        CostConstants.MUTAWIF_FEE_PER_DAY * sim_input.total_days
        if sim_input.include_mutawif else 0
    )
    
    handling_fee = CostConstants.HANDLING_FEE
    
    # Apply season multiplier to variable costs
    hotel_makkah_cost *= season_multiplier
    hotel_madinah_cost *= season_multiplier
    flight_cost *= season_multiplier
    
    # Package type adjustments
    package_multipliers = {
        PackageType.BACKPACKER: 0.85,
        PackageType.REGULER: 1.0,
        PackageType.PLUS: 1.25,
        PackageType.VIP: 1.75,
        PackageType.MANDIRI: 0.9,
    }
    
    package_mult = package_multipliers.get(sim_input.package_type, 1.0)
    
    # Create breakdown
    breakdown = CostBreakdown(
        flight_cost=flight_cost * package_mult,
        hotel_makkah_cost=hotel_makkah_cost * package_mult,
        hotel_madinah_cost=hotel_madinah_cost * package_mult,
        visa_cost=visa_cost,
        insurance_cost=insurance_cost,
        mutawif_cost=mutawif_cost,
        handling_fee=handling_fee,
        other_costs=0,
    )
    
    # Calculate totals
    total_per_person = breakdown.subtotal
    total_all = total_per_person * sim_input.traveler_count
    
    # Generate notes
    notes = []
    
    if season_type == "peak":
        notes.append("⚠️ Periode Ramadan - harga lebih tinggi dari biasanya")
    elif season_type == "high":
        notes.append("📈 Musim liburan - harga di atas rata-rata")
    
    if sim_input.package_type == PackageType.VIP:
        notes.append("✨ Paket VIP termasuk layanan premium")
    elif sim_input.package_type == PackageType.BACKPACKER:
        notes.append("💡 Paket Backpacker - hemat namun tetap nyaman")
    
    if sim_input.traveler_count >= 10:
        notes.append("👥 Diskon grup mungkin tersedia - konsultasikan dengan travel agent")
    
    # Build result
    result = CostSimulationResult(
        input=sim_input,
        breakdown=breakdown,
        total_per_person=total_per_person,
        total_all=total_all,
        currency="IDR",
        seasonal_multiplier=season_multiplier,
        season_type=season_type,
        generated_at=datetime.utcnow(),
        notes=notes,
        disclaimer="Estimasi biaya dapat berbeda dengan harga aktual dari travel agent."
    )
    
    # Convert to dict for UI
    return {
        "input": {
            "departure_city": sim_input.departure_city,
            "departure_date": str(sim_input.departure_date),
            "return_date": str(sim_input.return_date),
            "traveler_count": sim_input.traveler_count,
            "days_makkah": sim_input.days_makkah,
            "days_madinah": sim_input.days_madinah,
            "package_type": sim_input.package_type.value,
        },
        "breakdown": {
            "flight_cost": breakdown.flight_cost,
            "hotel_makkah_cost": breakdown.hotel_makkah_cost,
            "hotel_madinah_cost": breakdown.hotel_madinah_cost,
            "visa_cost": breakdown.visa_cost,
            "insurance_cost": breakdown.insurance_cost,
            "mutawif_cost": breakdown.mutawif_cost,
            "handling_fee": breakdown.handling_fee,
            "other_costs": breakdown.other_costs,
            "subtotal": breakdown.subtotal,
        },
        "total_per_person": total_per_person,
        "total_all": total_all,
        "currency": "IDR",
        "seasonal_multiplier": season_multiplier,
        "season_type": season_type,
        "notes": notes,
        "disclaimer": result.disclaimer,
    }


# =============================================================================
# COST COMPARISON
# =============================================================================

def compare_packages(
    base_input: Dict[str, Any],
    package_types: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Compare costs across different package types.
    
    Args:
        base_input: Base cost simulation input
        package_types: List of package types to compare
    
    Returns:
        List of cost results for each package
    """
    if package_types is None:
        package_types = ["backpacker", "reguler", "plus", "vip"]
    
    results = []
    
    for pkg_type in package_types:
        input_copy = base_input.copy()
        input_copy["package_type"] = pkg_type
        
        result = calculate_umrah_cost(input_copy)
        result["package_type"] = pkg_type
        results.append(result)
    
    return sorted(results, key=lambda x: x["total_per_person"])


def compare_seasons(
    base_input: Dict[str, Any],
    months: List[int] = None
) -> List[Dict[str, Any]]:
    """
    Compare costs across different months/seasons.
    
    Args:
        base_input: Base cost simulation input
        months: List of months to compare (1-12)
    
    Returns:
        List of cost results for each month
    """
    if months is None:
        months = [1, 3, 6, 9]  # Sample months across seasons
    
    results = []
    year = date.today().year
    
    for month in months:
        input_copy = base_input.copy()
        
        # Create departure date for that month
        departure = date(year if month >= date.today().month else year + 1, month, 15)
        days = base_input.get("days_makkah", 5) + base_input.get("days_madinah", 4)
        return_date = date.fromordinal(departure.toordinal() + days + 1)
        
        input_copy["departure_date"] = departure
        input_copy["return_date"] = return_date
        
        result = calculate_umrah_cost(input_copy)
        result["month"] = month
        result["month_name"] = departure.strftime("%B")
        results.append(result)
    
    return sorted(results, key=lambda x: x["total_per_person"])
