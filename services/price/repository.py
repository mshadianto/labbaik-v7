"""
LABBAIK AI v6.0 - Price Intelligence Repository
================================================
Repository untuk data harga dari n8n Price Intelligence System.
Data di-update otomatis setiap 6 jam.

Extends existing BaseRepository pattern.
"""

from __future__ import annotations
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from dataclasses import dataclass
from enum import Enum

from services.database.repository import BaseRepository, get_db, DatabaseConnection

logger = logging.getLogger(__name__)


# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class PricePackage:
    """Model untuk paket umrah."""
    id: str
    source_id: str
    package_name: str
    price_idr: float
    duration_days: int
    departure_city: str
    airline: Optional[str] = None
    hotel_makkah: Optional[str] = None
    hotel_makkah_stars: Optional[int] = None
    hotel_madinah: Optional[str] = None
    hotel_madinah_stars: Optional[int] = None
    includes: Optional[List[str]] = None
    is_available: bool = True
    source_url: Optional[str] = None
    scraped_at: Optional[datetime] = None
    source_name: Optional[str] = None  # From JOIN


@dataclass
class PriceHotel:
    """Model untuk harga hotel."""
    id: str
    source_id: str
    hotel_name: str
    city: str
    star_rating: int
    distance_to_haram: str
    distance_meters: int
    rating_score: float
    room_type: str
    room_capacity: int
    price_per_night_idr: float
    includes_breakfast: bool
    meal_plan: Optional[str] = None
    check_in_date: Optional[date] = None
    is_available: bool = True
    view_type: Optional[str] = None
    source_url: Optional[str] = None
    scraped_at: Optional[datetime] = None


@dataclass
class PriceFlight:
    """Model untuk harga penerbangan."""
    id: str
    source_id: str
    airline: str
    airline_code: str
    flight_code: str
    origin_city: str
    origin_airport: str
    destination_city: str
    destination_airport: str
    departure_date: date
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    is_direct: bool = True
    transit_cities: Optional[List[str]] = None
    price_idr: float = 0
    ticket_class: str = "economy"
    fare_type: str = "estimated"
    is_available: bool = True
    source_url: Optional[str] = None
    scraped_at: Optional[datetime] = None


# =============================================================================
# PRICE REPOSITORY
# =============================================================================

class PriceRepository:
    """
    Repository untuk mengakses data harga dari database.
    Data diupdate oleh n8n workflow setiap 6 jam.
    """
    
    def __init__(self, db: DatabaseConnection = None):
        self.db = db or get_db()
    
    # ==================== PACKAGES ====================
    
    def get_all_packages(
        self, 
        limit: int = 50,
        min_price: float = None,
        max_price: float = None,
        duration_days: int = None
    ) -> List[Dict]:
        """
        Ambil semua paket umrah dengan filter opsional.
        
        Args:
            limit: Maksimum hasil
            min_price: Harga minimum
            max_price: Harga maksimum
            duration_days: Filter durasi spesifik
        
        Returns:
            List of package dictionaries
        """
        query = """
            SELECT 
                p.*,
                s.source_name,
                s.source_code
            FROM prices_packages p
            LEFT JOIN scraping_sources s ON p.source_id = s.id
            WHERE p.is_available = true
        """
        params = []
        
        if min_price is not None:
            query += " AND p.price_idr >= %s"
            params.append(min_price)
        
        if max_price is not None:
            query += " AND p.price_idr <= %s"
            params.append(max_price)
        
        if duration_days is not None:
            query += " AND p.duration_days = %s"
            params.append(duration_days)
        
        query += " ORDER BY p.price_idr ASC LIMIT %s"
        params.append(limit)
        
        return self.db.fetch_all(query, tuple(params))
    
    def get_cheapest_packages(self, limit: int = 5) -> List[Dict]:
        """Ambil paket termurah."""
        return self.get_all_packages(limit=limit)
    
    def get_package_by_id(self, package_id: str) -> Optional[Dict]:
        """Ambil detail paket berdasarkan ID."""
        query = """
            SELECT 
                p.*,
                s.source_name,
                s.source_code
            FROM prices_packages p
            LEFT JOIN scraping_sources s ON p.source_id = s.id
            WHERE p.id = %s
        """
        return self.db.fetch_one(query, (package_id,))
    
    # ==================== HOTELS ====================
    
    def get_all_hotels(
        self,
        city: str = None,
        min_stars: int = None,
        max_distance: int = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Ambil semua hotel dengan filter opsional.
        
        Args:
            city: Filter kota (Makkah/Madinah)
            min_stars: Minimal bintang hotel
            max_distance: Maksimal jarak ke masjid (meter)
            limit: Maksimum hasil
        
        Returns:
            List of hotel dictionaries
        """
        query = """
            SELECT * FROM prices_hotels
            WHERE is_available = true
        """
        params = []
        
        if city:
            query += " AND city = %s"
            params.append(city)
        
        if min_stars:
            query += " AND star_rating >= %s"
            params.append(min_stars)
        
        if max_distance:
            query += " AND distance_meters <= %s"
            params.append(max_distance)
        
        query += " ORDER BY star_rating DESC, price_per_night_idr ASC LIMIT %s"
        params.append(limit)
        
        return self.db.fetch_all(query, tuple(params))
    
    def get_hotels_near_haram(self, city: str = 'Makkah', max_distance: int = 500) -> List[Dict]:
        """Ambil hotel dekat Masjidil Haram/Nabawi."""
        return self.get_all_hotels(city=city, max_distance=max_distance)
    
    def get_cheapest_hotels(self, city: str, limit: int = 5) -> List[Dict]:
        """Ambil hotel termurah di kota tertentu."""
        query = """
            SELECT * FROM prices_hotels
            WHERE is_available = true AND city = %s
            ORDER BY price_per_night_idr ASC
            LIMIT %s
        """
        return self.db.fetch_all(query, (city, limit))
    
    # ==================== FLIGHTS ====================
    
    def get_all_flights(
        self,
        origin: str = None,
        destination: str = None,
        direct_only: bool = False,
        departure_date: date = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Ambil semua penerbangan dengan filter opsional.
        
        Args:
            origin: Kode bandara asal (CGK, SUB)
            destination: Kode bandara tujuan (JED, MED)
            direct_only: Hanya penerbangan langsung
            departure_date: Tanggal keberangkatan spesifik
            limit: Maksimum hasil
        
        Returns:
            List of flight dictionaries
        """
        query = """
            SELECT * FROM prices_flights
            WHERE is_available = true
              AND departure_date >= CURRENT_DATE
        """
        params = []
        
        if origin:
            query += " AND origin_airport = %s"
            params.append(origin)
        
        if destination:
            query += " AND destination_airport = %s"
            params.append(destination)
        
        if direct_only:
            query += " AND is_direct = true"
        
        if departure_date:
            query += " AND departure_date = %s"
            params.append(departure_date)
        
        query += " ORDER BY departure_date ASC, price_idr ASC LIMIT %s"
        params.append(limit)
        
        return self.db.fetch_all(query, tuple(params))
    
    def get_direct_flights(self, origin: str = None, destination: str = None) -> List[Dict]:
        """Ambil penerbangan langsung."""
        return self.get_all_flights(origin=origin, destination=destination, direct_only=True)
    
    def get_cheapest_flights(self, origin: str, destination: str, limit: int = 5) -> List[Dict]:
        """Ambil penerbangan termurah untuk rute tertentu."""
        query = """
            SELECT * FROM prices_flights
            WHERE is_available = true
              AND origin_airport = %s
              AND destination_airport = %s
              AND departure_date >= CURRENT_DATE
            ORDER BY price_idr ASC
            LIMIT %s
        """
        return self.db.fetch_all(query, (origin, destination, limit))
    
    # ==================== STATISTICS ====================
    
    def get_price_summary(self) -> Dict:
        """
        Ambil ringkasan harga untuk dashboard.
        
        Returns:
            Dictionary dengan statistik harga
        """
        summary = {}
        
        # Package stats
        pkg_query = """
            SELECT 
                COUNT(*) as total,
                MIN(price_idr) as min_price,
                MAX(price_idr) as max_price,
                AVG(price_idr)::integer as avg_price
            FROM prices_packages
            WHERE is_available = true
        """
        summary['packages'] = self.db.fetch_one(pkg_query)
        
        # Hotel stats by city
        hotel_query = """
            SELECT 
                city,
                COUNT(*) as total,
                MIN(price_per_night_idr) as min_price,
                MAX(price_per_night_idr) as max_price,
                AVG(price_per_night_idr)::integer as avg_price
            FROM prices_hotels
            WHERE is_available = true
            GROUP BY city
        """
        summary['hotels'] = self.db.fetch_all(hotel_query)
        
        # Flight stats by route
        flight_query = """
            SELECT 
                origin_city || ' → ' || destination_city as route,
                COUNT(*) as total,
                MIN(price_idr) as min_price,
                AVG(price_idr)::integer as avg_price
            FROM prices_flights
            WHERE is_available = true AND departure_date >= CURRENT_DATE
            GROUP BY origin_city, destination_city
        """
        summary['flights'] = self.db.fetch_all(flight_query)
        
        # Last update
        update_query = """
            SELECT MAX(scraped_at) as last_update
            FROM (
                SELECT MAX(scraped_at) as scraped_at FROM prices_packages
                UNION ALL SELECT MAX(scraped_at) FROM prices_hotels
                UNION ALL SELECT MAX(scraped_at) FROM prices_flights
            ) t
        """
        result = self.db.fetch_one(update_query)
        summary['last_update'] = result.get('last_update') if result else None
        
        return summary
    
    def get_last_update(self) -> Optional[datetime]:
        """Get waktu update terakhir."""
        query = """
            SELECT MAX(scraped_at) as last_update
            FROM (
                SELECT MAX(scraped_at) as scraped_at FROM prices_packages
                UNION ALL SELECT MAX(scraped_at) FROM prices_hotels
                UNION ALL SELECT MAX(scraped_at) FROM prices_flights
            ) t
        """
        result = self.db.fetch_one(query)
        return result.get('last_update') if result else None
    
    # ==================== FOR COST SIMULATOR ====================
    
    def get_price_ranges(self) -> Dict:
        """
        Ambil range harga untuk Cost Simulator.
        
        Returns:
            Dictionary dengan min/max/avg untuk setiap kategori
        """
        ranges = {}
        
        # Package range
        pkg = self.db.fetch_one("""
            SELECT 
                MIN(price_idr) as min,
                MAX(price_idr) as max,
                AVG(price_idr)::integer as avg
            FROM prices_packages WHERE is_available = true
        """)
        ranges['package'] = pkg or {'min': 23000000, 'max': 55000000, 'avg': 35000000}
        
        # Hotel Makkah range
        hotel_makkah = self.db.fetch_one("""
            SELECT 
                MIN(price_per_night_idr) as min,
                MAX(price_per_night_idr) as max,
                AVG(price_per_night_idr)::integer as avg
            FROM prices_hotels WHERE is_available = true AND city = 'Makkah'
        """)
        ranges['hotel_makkah'] = hotel_makkah or {'min': 500000, 'max': 5000000, 'avg': 1500000}
        
        # Hotel Madinah range
        hotel_madinah = self.db.fetch_one("""
            SELECT 
                MIN(price_per_night_idr) as min,
                MAX(price_per_night_idr) as max,
                AVG(price_per_night_idr)::integer as avg
            FROM prices_hotels WHERE is_available = true AND city = 'Madinah'
        """)
        ranges['hotel_madinah'] = hotel_madinah or {'min': 400000, 'max': 3000000, 'avg': 1200000}
        
        # Flight range
        flight = self.db.fetch_one("""
            SELECT 
                MIN(price_idr) as min,
                MAX(price_idr) as max,
                AVG(price_idr)::integer as avg
            FROM prices_flights 
            WHERE is_available = true AND departure_date >= CURRENT_DATE
        """)
        ranges['flight'] = flight or {'min': 10000000, 'max': 20000000, 'avg': 15000000}
        
        return ranges


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_price_idr(price: float) -> str:
    """Format harga ke format Indonesia (Rp X.XXX.XXX)."""
    return f"Rp {price:,.0f}".replace(",", ".")


def format_duration(minutes: int) -> str:
    """Format durasi dalam jam dan menit."""
    hours = minutes // 60
    mins = minutes % 60
    if mins:
        return f"{hours}j {mins}m"
    return f"{hours} jam"


# =============================================================================
# CACHED FUNCTIONS (untuk Streamlit)
# =============================================================================

def get_price_repo() -> PriceRepository:
    """Get PriceRepository instance."""
    return PriceRepository()


# Streamlit cached versions
try:
    import streamlit as st
    
    @st.cache_data(ttl=300)  # Cache 5 menit
    def get_cached_packages(limit: int = 50, min_price: float = None, max_price: float = None):
        """Get packages dengan cache Streamlit."""
        repo = get_price_repo()
        return repo.get_all_packages(limit=limit, min_price=min_price, max_price=max_price)
    
    @st.cache_data(ttl=300)
    def get_cached_hotels(city: str = None, min_stars: int = None, max_distance: int = None):
        """Get hotels dengan cache Streamlit."""
        repo = get_price_repo()
        return repo.get_all_hotels(city=city, min_stars=min_stars, max_distance=max_distance)
    
    @st.cache_data(ttl=300)
    def get_cached_flights(origin: str = None, destination: str = None, direct_only: bool = False):
        """Get flights dengan cache Streamlit."""
        repo = get_price_repo()
        return repo.get_all_flights(origin=origin, destination=destination, direct_only=direct_only)
    
    @st.cache_data(ttl=600)  # Cache 10 menit
    def get_cached_price_summary():
        """Get price summary dengan cache."""
        repo = get_price_repo()
        return repo.get_price_summary()
    
    @st.cache_data(ttl=600)
    def get_cached_price_ranges():
        """Get price ranges untuk simulator dengan cache."""
        repo = get_price_repo()
        return repo.get_price_ranges()

except ImportError:
    # Fallback jika tidak ada Streamlit (untuk testing)
    def get_cached_packages(*args, **kwargs):
        return get_price_repo().get_all_packages(*args, **kwargs)
    
    def get_cached_hotels(*args, **kwargs):
        return get_price_repo().get_all_hotels(*args, **kwargs)
    
    def get_cached_flights(*args, **kwargs):
        return get_price_repo().get_all_flights(*args, **kwargs)
    
    def get_cached_price_summary():
        return get_price_repo().get_price_summary()
    
    def get_cached_price_ranges():
        return get_price_repo().get_price_ranges()
