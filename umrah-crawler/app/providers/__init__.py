"""
LABBAIK AI - Data Providers V1.3.1
==================================
Hotel, transport, and FX data providers.
"""

# Legacy providers
from app.providers.amadeus import refresh_amadeus_offers
from app.providers.xotelo import refresh_xotelo_prices
from app.providers.makcorps import refresh_makcorps_prices
from app.providers.haramain import fetch_haramain_timetable
from app.providers.saptco import fetch_saptco_schedule

# V1.3.1 Agoda (RapidAPI)
from app.providers.agoda import (
    fetch_agoda_hotels,
    refresh_agoda_snapshot,
    refresh_agoda_all_cities,
    AgodaHotel,
    AGODA_CITY_IDS,
)

# V1.3 Transport (JSON-first)
from app.providers.transport_engine import (
    TransportEngine,
    TransportRow,
    FetchResult,
    FetchMethod,
    get_transport_engine,
)
from app.providers.haramain_v13 import (
    fetch_haramain_schedule,
    fetch_all_routes as fetch_haramain_all_routes,
)
from app.providers.saptco_v13 import (
    fetch_saptco_schedule as fetch_saptco_schedule_v13,
    fetch_all_routes as fetch_saptco_all_routes,
    compare_bus_vs_train,
)

# V1.3 FX
from app.providers.fx_ecb import (
    FXService,
    get_fx_service,
    to_sar,
    to_idr,
    format_price_dual,
)

__all__ = [
    # Legacy
    "refresh_amadeus_offers",
    "refresh_xotelo_prices",
    "refresh_makcorps_prices",
    "fetch_haramain_timetable",
    "fetch_saptco_schedule",

    # V1.3.1 Agoda
    "fetch_agoda_hotels",
    "refresh_agoda_snapshot",
    "refresh_agoda_all_cities",
    "AgodaHotel",
    "AGODA_CITY_IDS",

    # V1.3 Transport Engine
    "TransportEngine",
    "TransportRow",
    "FetchResult",
    "FetchMethod",
    "get_transport_engine",

    # V1.3 Haramain
    "fetch_haramain_schedule",
    "fetch_haramain_all_routes",

    # V1.3 SAPTCO
    "fetch_saptco_schedule_v13",
    "fetch_saptco_all_routes",
    "compare_bus_vs_train",

    # V1.3 FX
    "FXService",
    "get_fx_service",
    "to_sar",
    "to_idr",
    "format_price_dual",
]
