"""
LABBAIK AI - SAPTCO Bus V1.3 Provider
=====================================
JSON-first scraping for SAPTCO bus services.
Fallback: HTML parse → snapshot.
"""

import logging
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup

from .transport_engine import (
    TransportEngine, TransportRow, FetchResult, FetchMethod,
    get_transport_engine
)

logger = logging.getLogger(__name__)

# =============================================================================
# ENDPOINT DISCOVERY
# =============================================================================

# SAPTCO official site
SAPTCO_WEB_URL = "https://www.saptco.com.sa"
SAPTCO_BOOKING_URL = "https://booking.saptco.com.sa"

# JSON API endpoints (discovered via Network tab - update when found)
SAPTCO_JSON_ENDPOINTS = [
    # Example format - replace with actual discovered endpoints:
    # "https://booking.saptco.com.sa/api/schedule",
    # "https://api.saptco.com.sa/v1/trips",
]

# Route codes
ROUTES = {
    "MAKKAH_MADINAH": {"from": "MKH", "to": "MED"},
    "MADINAH_MAKKAH": {"from": "MED", "to": "MKH"},
}

# Known schedule (static fallback)
# Based on typical SAPTCO bus schedule
KNOWN_SCHEDULE = {
    "MAKKAH_MADINAH": [
        {"depart": "06:00", "arrive": "11:00", "class": "VIP", "price": 120},
        {"depart": "08:00", "arrive": "13:00", "class": "STANDARD", "price": 80},
        {"depart": "10:00", "arrive": "15:00", "class": "VIP", "price": 120},
        {"depart": "12:00", "arrive": "17:00", "class": "STANDARD", "price": 80},
        {"depart": "14:00", "arrive": "19:00", "class": "VIP", "price": 120},
        {"depart": "16:00", "arrive": "21:00", "class": "STANDARD", "price": 80},
        {"depart": "18:00", "arrive": "23:00", "class": "VIP", "price": 120},
        {"depart": "20:00", "arrive": "01:00", "class": "STANDARD", "price": 80},
        {"depart": "22:00", "arrive": "03:00", "class": "STANDARD", "price": 80},
    ],
    "MADINAH_MAKKAH": [
        {"depart": "05:00", "arrive": "10:00", "class": "VIP", "price": 120},
        {"depart": "07:00", "arrive": "12:00", "class": "STANDARD", "price": 80},
        {"depart": "09:00", "arrive": "14:00", "class": "VIP", "price": 120},
        {"depart": "11:00", "arrive": "16:00", "class": "STANDARD", "price": 80},
        {"depart": "13:00", "arrive": "18:00", "class": "VIP", "price": 120},
        {"depart": "15:00", "arrive": "20:00", "class": "STANDARD", "price": 80},
        {"depart": "17:00", "arrive": "22:00", "class": "VIP", "price": 120},
        {"depart": "19:00", "arrive": "00:00", "class": "STANDARD", "price": 80},
        {"depart": "21:00", "arrive": "02:00", "class": "STANDARD", "price": 80},
    ]
}


# =============================================================================
# JSON MAPPER
# =============================================================================

def map_saptco_json(
    data: Any,
    operator: str,
    route: str,
    source_url: str
) -> List[TransportRow]:
    """
    Map SAPTCO JSON response to TransportRow objects.

    Adjust this based on actual API response structure.
    """
    rows = []

    # Handle various response formats
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = (
            data.get("trips") or
            data.get("schedules") or
            data.get("buses") or
            data.get("data") or
            data.get("results") or
            []
        )
        if isinstance(items, dict):
            items = [items]

    for item in items:
        try:
            depart_str = (
                item.get("departureTime") or
                item.get("departure") or
                item.get("depart")
            )
            arrive_str = (
                item.get("arrivalTime") or
                item.get("arrival") or
                item.get("arrive")
            )

            depart_time = _parse_time(depart_str) if depart_str else None
            arrive_time = _parse_time(arrive_str) if arrive_str else None

            duration = item.get("duration") or item.get("durationMin")
            if duration and isinstance(duration, str):
                duration = _parse_duration(duration)
            elif not duration and depart_time and arrive_time:
                duration = int((arrive_time - depart_time).total_seconds() / 60)
                if duration < 0:
                    duration += 24 * 60  # Handle overnight

            price = item.get("price") or item.get("fare") or item.get("priceSar")
            if price:
                price = float(str(price).replace(",", "").replace("SAR", "").strip())

            travel_class = (
                item.get("class") or
                item.get("busClass") or
                item.get("type") or
                "STANDARD"
            ).upper()

            if travel_class in ["ECONOMY", "REGULAR"]:
                travel_class = "STANDARD"

            availability = item.get("availability") or "AVAILABLE"
            if item.get("soldOut") or item.get("isFull"):
                availability = "SOLD_OUT"
            elif item.get("seatsLeft", 99) < 5:
                availability = "LIMITED"

            rows.append(TransportRow(
                operator=operator,
                mode="BUS",
                route=route,
                depart_time=depart_time,
                arrive_time=arrive_time,
                duration_min=duration,
                price_sar=price,
                travel_class=travel_class,
                availability=availability,
                source_url=source_url,
                source_method=FetchMethod.JSON,
                raw_payload=item
            ))

        except Exception as e:
            logger.warning(f"Failed to map SAPTCO item: {e}")
            continue

    return rows


def _parse_time(time_str: str) -> Optional[datetime]:
    """Parse time string to datetime."""
    if not time_str:
        return None

    today = datetime.now().date()

    for fmt in ["%H:%M", "%H:%M:%S", "%I:%M %p", "%I:%M%p"]:
        try:
            t = datetime.strptime(time_str.strip(), fmt)
            return datetime.combine(today, t.time())
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(time_str.replace("Z", "+00:00"))
    except ValueError:
        pass

    return None


def _parse_duration(duration_str: str) -> Optional[int]:
    """Parse duration string to minutes."""
    if not duration_str:
        return None

    total_min = 0

    h_match = re.search(r"(\d+)\s*(h|hr|hour)", duration_str, re.I)
    if h_match:
        total_min += int(h_match.group(1)) * 60

    m_match = re.search(r"(\d+)\s*(m|min|minute)", duration_str, re.I)
    if m_match:
        total_min += int(m_match.group(1))

    return total_min if total_min > 0 else None


# =============================================================================
# HTML PARSER
# =============================================================================

def parse_saptco_html(soup: BeautifulSoup) -> List[Dict]:
    """
    Parse SAPTCO HTML schedule page.

    Returns list of schedule dicts.
    """
    rows = []

    # Try common selectors
    schedule_items = soup.select(
        ".trip-item, .bus-schedule, .schedule-row, "
        "table.schedule tr, .route-item"
    )

    for item in schedule_items:
        try:
            depart = item.select_one(".departure, .depart, .time-depart, td:nth-child(1)")
            arrive = item.select_one(".arrival, .arrive, .time-arrive, td:nth-child(2)")
            price = item.select_one(".price, .fare, td:nth-child(3)")
            bus_class = item.select_one(".class, .bus-type, td:nth-child(4)")

            row = {}

            if depart:
                row["depart_time"] = _parse_time(depart.get_text(strip=True))
            if arrive:
                row["arrive_time"] = _parse_time(arrive.get_text(strip=True))
            if price:
                price_text = price.get_text(strip=True)
                price_num = re.search(r"[\d,.]+", price_text)
                if price_num:
                    row["price_sar"] = float(price_num.group().replace(",", ""))
            if bus_class:
                row["travel_class"] = bus_class.get_text(strip=True).upper()

            if row:
                rows.append(row)

        except Exception as e:
            logger.debug(f"Failed to parse SAPTCO HTML row: {e}")
            continue

    return rows


# =============================================================================
# MAIN FETCH FUNCTION
# =============================================================================

async def fetch_saptco_schedule(
    route: str = "MAKKAH_MADINAH",
    travel_date: Optional[datetime] = None
) -> FetchResult:
    """
    Fetch SAPTCO bus schedule.

    Strategy:
    1. Try JSON endpoints
    2. Fallback to HTML parsing
    3. Use cached snapshot / known schedule

    Args:
        route: 'MAKKAH_MADINAH' or 'MADINAH_MAKKAH'
        travel_date: Optional specific date

    Returns:
        FetchResult with schedule rows
    """
    engine = get_transport_engine()

    json_urls = list(SAPTCO_JSON_ENDPOINTS)

    result = await engine.fetch(
        operator="SAPTCO",
        route=route,
        json_endpoints=json_urls,
        html_url=SAPTCO_BOOKING_URL,
        html_parser=parse_saptco_html,
        json_mapper=map_saptco_json
    )

    # If all strategies failed, use known schedule
    if not result.success or not result.rows:
        logger.warning(f"Using known schedule for SAPTCO {route}")
        rows = _get_known_schedule_rows(route, travel_date)
        return FetchResult(
            success=True,
            method=FetchMethod.SNAPSHOT,
            rows=rows,
            source_url="known_schedule"
        )

    return result


def _get_known_schedule_rows(
    route: str,
    travel_date: Optional[datetime] = None
) -> List[TransportRow]:
    """Convert known schedule to TransportRow objects."""
    schedule = KNOWN_SCHEDULE.get(route, [])
    base_date = (travel_date or datetime.now()).date()

    rows = []
    for item in schedule:
        depart_time = None
        arrive_time = None

        if item.get("depart"):
            h, m = map(int, item["depart"].split(":"))
            depart_time = datetime.combine(
                base_date,
                datetime.min.time().replace(hour=h, minute=m)
            )

        if item.get("arrive"):
            h, m = map(int, item["arrive"].split(":"))
            arrive_time = datetime.combine(
                base_date,
                datetime.min.time().replace(hour=h, minute=m)
            )
            # Handle overnight (arrival next day)
            if depart_time and arrive_time < depart_time:
                arrive_time += timedelta(days=1)

        duration_min = None
        if depart_time and arrive_time:
            duration_min = int((arrive_time - depart_time).total_seconds() / 60)

        rows.append(TransportRow(
            operator="SAPTCO",
            mode="BUS",
            route=route,
            depart_time=depart_time,
            arrive_time=arrive_time,
            duration_min=duration_min,
            price_sar=float(item.get("price", 80)),
            travel_class=item.get("class", "STANDARD"),
            availability="AVAILABLE",
            source_url="known_schedule",
            source_method=FetchMethod.SNAPSHOT
        ))

    return rows


async def fetch_all_routes() -> Dict[str, FetchResult]:
    """Fetch schedule for all routes."""
    results = {}
    for route in ROUTES.keys():
        results[route] = await fetch_saptco_schedule(route)
    return results


# =============================================================================
# PRICE COMPARISON
# =============================================================================

def compare_bus_vs_train(
    bus_rows: List[TransportRow],
    train_rows: List[TransportRow]
) -> Dict:
    """
    Compare bus vs train options.

    Returns comparison dict for UI display.
    """
    bus_economy = [r for r in bus_rows if r.travel_class == "STANDARD"]
    bus_vip = [r for r in bus_rows if r.travel_class == "VIP"]
    train_economy = [r for r in train_rows if r.travel_class == "ECONOMY"]
    train_business = [r for r in train_rows if r.travel_class == "BUSINESS"]

    def avg_price(rows):
        prices = [r.price_sar for r in rows if r.price_sar]
        return sum(prices) / len(prices) if prices else 0

    def avg_duration(rows):
        durations = [r.duration_min for r in rows if r.duration_min]
        return sum(durations) / len(durations) if durations else 0

    return {
        "bus": {
            "standard": {
                "avg_price_sar": avg_price(bus_economy),
                "avg_duration_min": avg_duration(bus_economy),
                "trips_per_day": len(bus_economy),
            },
            "vip": {
                "avg_price_sar": avg_price(bus_vip),
                "avg_duration_min": avg_duration(bus_vip),
                "trips_per_day": len(bus_vip),
            }
        },
        "train": {
            "economy": {
                "avg_price_sar": avg_price(train_economy),
                "avg_duration_min": avg_duration(train_economy),
                "trips_per_day": len(train_economy),
            },
            "business": {
                "avg_price_sar": avg_price(train_business),
                "avg_duration_min": avg_duration(train_business),
                "trips_per_day": len(train_business),
            }
        },
        "recommendation": {
            "budget": "BUS_STANDARD" if avg_price(bus_economy) < avg_price(train_economy) else "TRAIN_ECONOMY",
            "fastest": "TRAIN_ECONOMY",  # Train is always faster
            "comfort": "TRAIN_BUSINESS",
        }
    }
