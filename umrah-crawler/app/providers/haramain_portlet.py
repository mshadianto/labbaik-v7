"""
LABBAIK AI - Haramain Portlet Provider V1.3
============================================
Real Haramain train schedule fetcher using Liferay portlet endpoint.

Endpoint discovered from: sar.hhr.sa/timetable
Action: sendTicketData (returns JSON schedule)
"""

import json
import re
import logging
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

import httpx

from .haramain_station_map import (
    HARAMAIN_STATIONS,
    get_station_id,
    get_station_name,
    get_route_ids,
)

logger = logging.getLogger(__name__)

# =============================================================================
# CONSTANTS
# =============================================================================

BASE_URL = "https://sar.hhr.sa/timetable"
PORTLET_ID = "HhrFlatTimetables"

# Default headers
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
    "Referer": BASE_URL,
}


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class HaramainTrip:
    """Single Haramain train trip."""
    departure_time: datetime
    arrival_time: datetime
    duration_min: int
    from_city: str
    to_city: str
    train_class: str = "ECONOMY"
    price_sar: Optional[float] = None
    availability: str = "AVAILABLE"
    train_number: Optional[str] = None
    raw_data: Dict = field(default_factory=dict)


@dataclass
class FetchResult:
    """Result of a fetch operation."""
    success: bool
    trips: List[HaramainTrip] = field(default_factory=list)
    raw_response: Optional[str] = None
    error: Optional[str] = None
    source_url: str = ""
    http_status: int = 0


# =============================================================================
# HELPERS
# =============================================================================

def _format_date_dmy(d: date) -> str:
    """Format date as dd/MM/yyyy for Haramain API."""
    return d.strftime("%d/%m/%Y")


def _parse_time(time_str: str, base_date: date) -> Optional[datetime]:
    """
    Parse time string to datetime.

    Handles formats like:
    - "08:30"
    - "08:30:00"
    - "8:30 AM"
    - "2025-12-29T08:30:00"
    """
    if not time_str:
        return None

    time_str = time_str.strip()

    # Try ISO format first
    if "T" in time_str:
        try:
            return datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        except ValueError:
            pass

    # Try various time formats
    for fmt in ["%H:%M", "%H:%M:%S", "%I:%M %p", "%I:%M%p"]:
        try:
            t = datetime.strptime(time_str, fmt)
            return datetime.combine(base_date, t.time())
        except ValueError:
            continue

    # Try extracting HH:MM from string
    match = re.search(r"(\d{1,2}):(\d{2})", time_str)
    if match:
        h, m = int(match.group(1)), int(match.group(2))
        return datetime.combine(base_date, datetime.min.time().replace(hour=h, minute=m))

    return None


def _parse_duration(duration_val: Any) -> Optional[int]:
    """
    Parse duration to minutes.

    Handles:
    - Integer (minutes)
    - "2h 30m"
    - "02:30"
    - "150 min"
    """
    if duration_val is None:
        return None

    if isinstance(duration_val, (int, float)):
        return int(duration_val)

    if isinstance(duration_val, str):
        s = duration_val.lower().strip()

        # "2h 30m" or "2hr 30min"
        h_match = re.search(r"(\d+)\s*(h|hr|hour)", s)
        m_match = re.search(r"(\d+)\s*(m|min|minute)", s)

        total = 0
        if h_match:
            total += int(h_match.group(1)) * 60
        if m_match:
            total += int(m_match.group(1))

        if total > 0:
            return total

        # "02:30" format (HH:MM)
        if ":" in s:
            parts = s.split(":")
            if len(parts) >= 2:
                try:
                    return int(parts[0]) * 60 + int(parts[1])
                except ValueError:
                    pass

        # "150" or "150 min"
        num_match = re.search(r"(\d+)", s)
        if num_match:
            return int(num_match.group(1))

    return None


def _try_extract_json(text: str) -> Optional[Dict]:
    """
    Try to extract JSON from response text.

    Liferay portlets sometimes embed JSON in HTML or wrap it.
    """
    if not text:
        return None

    text = text.strip()

    # Try direct JSON parse
    if text.startswith(("{", "[")):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

    # Look for JSON in script tags
    # Pattern: var data = {...};
    patterns = [
        r"var\s+(?:data|result|response|timetable)\s*=\s*(\{[^;]+\});",
        r"var\s+(?:data|result|response|timetable)\s*=\s*(\[[^\]]+\]);",
        r"JSON\.parse\s*\(\s*'([^']+)'\s*\)",
        r"<script[^>]*>\s*(\{[\s\S]*?\})\s*</script>",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue

    # Look for any JSON-like structure
    json_match = re.search(r"(\{[^{}]*\"[^{}]+\})", text)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    return None


# =============================================================================
# RESPONSE PARSER
# =============================================================================

def parse_schedule_response(
    data: Any,
    from_city: str,
    to_city: str,
    dep_date: date
) -> List[HaramainTrip]:
    """
    Parse Haramain schedule response.

    Handles various response formats from the portlet.
    """
    trips = []

    if data is None:
        return trips

    # Find the list of items
    items = None

    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        # Try common keys
        for key in ["data", "results", "items", "timetables", "trips",
                    "journeys", "schedules", "trains", "list"]:
            if isinstance(data.get(key), list):
                items = data[key]
                break

        # Try nested structures
        if items is None:
            for outer_key in ["data", "result", "response", "body"]:
                if isinstance(data.get(outer_key), dict):
                    inner = data[outer_key]
                    for inner_key in ["items", "timetables", "trips", "journeys"]:
                        if isinstance(inner.get(inner_key), list):
                            items = inner[inner_key]
                            break
                    if items:
                        break

    if not items:
        logger.warning(f"No schedule items found in response. Keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
        return trips

    logger.info(f"Found {len(items)} schedule items")

    for item in items:
        if not isinstance(item, dict):
            continue

        try:
            # Extract departure time (try multiple field names)
            dep_time_str = (
                item.get("departureTime") or
                item.get("depTime") or
                item.get("departure_time") or
                item.get("timeFrom") or
                item.get("depart") or
                item.get("fromTime") or
                item.get("startTime")
            )

            # Extract arrival time
            arr_time_str = (
                item.get("arrivalTime") or
                item.get("arrTime") or
                item.get("arrival_time") or
                item.get("timeTo") or
                item.get("arrive") or
                item.get("toTime") or
                item.get("endTime")
            )

            # Parse times
            dep_time = _parse_time(dep_time_str, dep_date) if dep_time_str else None
            arr_time = _parse_time(arr_time_str, dep_date) if arr_time_str else None

            # Handle overnight trips
            if dep_time and arr_time and arr_time < dep_time:
                arr_time += timedelta(days=1)

            # Extract duration
            duration_val = (
                item.get("duration") or
                item.get("durationMin") or
                item.get("duration_min") or
                item.get("travelTime") or
                item.get("journeyTime")
            )
            duration_min = _parse_duration(duration_val)

            # Calculate duration from times if not provided
            if not duration_min and dep_time and arr_time:
                duration_min = int((arr_time - dep_time).total_seconds() / 60)

            # Skip invalid entries
            if not dep_time:
                continue

            # Extract other fields
            train_class = (
                item.get("class") or
                item.get("seatClass") or
                item.get("travelClass") or
                item.get("classType") or
                "ECONOMY"
            )
            if isinstance(train_class, str):
                train_class = train_class.upper()
                if train_class in ["BUSINESS", "FIRST"]:
                    train_class = "BUSINESS"
                else:
                    train_class = "ECONOMY"

            price = item.get("price") or item.get("fare") or item.get("priceSar")
            if price:
                try:
                    price = float(str(price).replace(",", "").replace("SAR", "").strip())
                except ValueError:
                    price = None

            availability = "AVAILABLE"
            if item.get("soldOut") or item.get("isSoldOut") or item.get("sold_out"):
                availability = "SOLD_OUT"
            elif item.get("seatsLeft", 99) < 5:
                availability = "LIMITED"

            train_number = item.get("trainNumber") or item.get("train_number") or item.get("trainNo")

            trip = HaramainTrip(
                departure_time=dep_time,
                arrival_time=arr_time or (dep_time + timedelta(minutes=duration_min or 120)),
                duration_min=duration_min or 120,
                from_city=from_city,
                to_city=to_city,
                train_class=train_class,
                price_sar=price,
                availability=availability,
                train_number=train_number,
                raw_data=item
            )
            trips.append(trip)

        except Exception as e:
            logger.debug(f"Failed to parse item: {e}")
            continue

    return trips


# =============================================================================
# MAIN FETCH FUNCTION
# =============================================================================

async def fetch_haramain_portlet(
    from_city: str = "MAKKAH",
    to_city: str = "MADINAH",
    departure_date: Optional[date] = None,
    language: str = "en_US",
    cookies: Optional[str] = None,
    timeout: float = 30.0
) -> FetchResult:
    """
    Fetch Haramain train schedule from portlet endpoint.

    Args:
        from_city: Departure city (MAKKAH or MADINAH)
        to_city: Arrival city
        departure_date: Date to fetch (default: today)
        language: Language code (en_US or ar_SA)
        cookies: Optional cookie string from browser
        timeout: Request timeout in seconds

    Returns:
        FetchResult with trips and metadata
    """
    from_city = from_city.upper()
    to_city = to_city.upper()
    departure_date = departure_date or date.today()

    # Get station IDs
    try:
        from_id = get_station_id(from_city)
        to_id = get_station_id(to_city)
    except ValueError as e:
        return FetchResult(success=False, error=str(e))

    # Build request parameters
    params = {
        "p_p_id": PORTLET_ID,
        "p_p_lifecycle": "0",
        f"_{PORTLET_ID}_javax.portlet.action": "sendTicketData",
        f"_{PORTLET_ID}_businessPartner": "+",
        f"_{PORTLET_ID}_formDate": str(int(datetime.now().timestamp() * 1000)),
        f"_{PORTLET_ID}_idFromStation": str(from_id),
        f"_{PORTLET_ID}_idToStation": str(to_id),
        f"_{PORTLET_ID}_departureDate": _format_date_dmy(departure_date),
        f"_{PORTLET_ID}_language": language,
        f"_{PORTLET_ID}_datePattern": "dd/MM/yyyy",
    }

    # Build headers
    headers = dict(DEFAULT_HEADERS)
    if cookies:
        headers["Cookie"] = cookies

    # Build full URL for logging
    source_url = f"{BASE_URL}?{from_city}→{to_city}@{_format_date_dmy(departure_date)}"

    logger.info(f"Fetching Haramain: {from_city} → {to_city} on {departure_date}")

    try:
        async with httpx.AsyncClient(
            timeout=timeout,
            headers=headers,
            follow_redirects=True
        ) as client:
            resp = await client.get(BASE_URL, params=params)

        logger.debug(f"Response status: {resp.status_code}, length: {len(resp.text)}")

        # Try to parse response
        data = None

        # Try JSON first
        content_type = resp.headers.get("content-type", "")
        if "json" in content_type:
            try:
                data = resp.json()
            except json.JSONDecodeError:
                pass

        # Try extracting JSON from response
        if data is None:
            data = _try_extract_json(resp.text)

        # Parse schedule
        trips = []
        if data:
            trips = parse_schedule_response(data, from_city, to_city, departure_date)

        if trips:
            logger.info(f"Parsed {len(trips)} trips from Haramain")
            return FetchResult(
                success=True,
                trips=trips,
                source_url=source_url,
                http_status=resp.status_code,
                raw_response=resp.text[:1000] if len(resp.text) > 1000 else resp.text
            )
        else:
            # Return partial success with raw response for debugging
            return FetchResult(
                success=False,
                trips=[],
                source_url=source_url,
                http_status=resp.status_code,
                raw_response=resp.text[:2000] if len(resp.text) > 2000 else resp.text,
                error="No trips parsed from response"
            )

    except httpx.TimeoutException:
        return FetchResult(success=False, error="Request timeout", source_url=source_url)
    except httpx.HTTPError as e:
        return FetchResult(success=False, error=f"HTTP error: {e}", source_url=source_url)
    except Exception as e:
        logger.exception(f"Fetch failed: {e}")
        return FetchResult(success=False, error=str(e), source_url=source_url)


async def fetch_haramain_all_dates(
    from_city: str = "MAKKAH",
    to_city: str = "MADINAH",
    days_ahead: List[int] = None,
    cookies: Optional[str] = None
) -> Dict[str, FetchResult]:
    """
    Fetch Haramain schedule for multiple dates.

    Args:
        from_city: Departure city
        to_city: Arrival city
        days_ahead: List of days ahead to fetch (default: [1, 3, 7, 14])
        cookies: Optional cookie string

    Returns:
        Dict of date_str -> FetchResult
    """
    if days_ahead is None:
        days_ahead = [1, 3, 7, 14]

    results = {}
    today = date.today()

    for days in days_ahead:
        target_date = today + timedelta(days=days)
        date_str = target_date.isoformat()

        result = await fetch_haramain_portlet(
            from_city=from_city,
            to_city=to_city,
            departure_date=target_date,
            cookies=cookies
        )
        results[date_str] = result

    return results


# =============================================================================
# DATABASE STORAGE
# =============================================================================

async def store_haramain_trips(trips: List[HaramainTrip], db_session=None) -> int:
    """
    Store trips to database.

    Args:
        trips: List of HaramainTrip objects
        db_session: Optional database session

    Returns:
        Number of trips stored
    """
    if not trips:
        return 0

    if db_session is None:
        logger.info(f"Would store {len(trips)} Haramain trips (no db session)")
        return len(trips)

    stored = 0
    from sqlalchemy import text

    for trip in trips:
        try:
            await db_session.execute(text("""
                INSERT INTO transport_schedule
                (mode, operator, route, depart_time_local, arrive_time_local,
                 duration_min, price_sar, class, availability, source_method)
                VALUES ('TRAIN', 'HARAMAIN', :route, :dep, :arr, :dur, :price, :cls, :avail, 'JSON')
                ON CONFLICT DO NOTHING
            """), {
                "route": f"{trip.from_city}_{trip.to_city}",
                "dep": trip.departure_time,
                "arr": trip.arrival_time,
                "dur": trip.duration_min,
                "price": trip.price_sar,
                "cls": trip.train_class,
                "avail": trip.availability,
            })
            stored += 1
        except Exception as e:
            logger.error(f"Failed to store trip: {e}")

    await db_session.commit()
    return stored


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def trips_to_display(trips: List[HaramainTrip]) -> List[Dict]:
    """Format trips for UI display."""
    return [
        {
            "departure": trip.departure_time.strftime("%H:%M") if trip.departure_time else "~",
            "arrival": trip.arrival_time.strftime("%H:%M") if trip.arrival_time else "~",
            "duration": f"{trip.duration_min} min",
            "class": trip.train_class,
            "price": f"SAR {trip.price_sar:.0f}" if trip.price_sar else "~",
            "availability": trip.availability,
            "route": f"{trip.from_city} → {trip.to_city}",
        }
        for trip in trips
    ]
