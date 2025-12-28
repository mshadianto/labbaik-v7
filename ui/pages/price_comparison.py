"""
LABBAIK AI v7.5 - Price Comparison Page
========================================
Real-time price comparison from multiple sources.

Features:
- Multi-source price comparison table
- Source badges (API/OTA/Partner)
- Price trend indicators
- Best price highlighting
- Filtering by city, stars, price range, source
"""

import streamlit as st
from datetime import date, datetime, timedelta
from typing import Dict, List, Any, Optional

# Try to import price aggregation services
try:
    from services.price_aggregation import (
        get_price_aggregator,
        create_price_aggregator,
        AggregatedOffer,
        SourceType,
        OfferType,
    )
    HAS_PRICE_AGGREGATION = True
except ImportError:
    HAS_PRICE_AGGREGATION = False

# Try to import data manager for API integration
try:
    from services.umrah import get_umrah_data_manager
    HAS_DATA_MANAGER = True
except ImportError:
    HAS_DATA_MANAGER = False


# =============================================================================
# CONSTANTS
# =============================================================================

SOURCE_BADGES = {
    "amadeus": ("🌐 API", "#4CAF50"),
    "xotelo": ("🌐 API", "#4CAF50"),
    "makcorps": ("🌐 API", "#4CAF50"),
    "traveloka": ("🛒 OTA", "#2196F3"),
    "tiket": ("🛒 OTA", "#2196F3"),
    "pegipegi": ("🛒 OTA", "#2196F3"),
    "partner": ("🤝 Partner", "#FF9800"),
    "demo": ("📋 Demo", "#9E9E9E"),
}

CITIES = ["Semua Kota", "Makkah", "Madinah"]
OFFER_TYPES = {
    "Semua": None,
    "Hotel": "hotel",
    "Paket Umrah": "package",
}
SORT_OPTIONS = {
    "Harga Terendah": "price",
    "Harga Tertinggi": "price_desc",
    "Bintang Tertinggi": "stars",
    "Jarak Terdekat": "distance",
    "Terbaru": "updated",
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_price(price: float, currency: str = "IDR") -> str:
    """Format price with thousand separators."""
    if currency == "IDR":
        return f"Rp {price:,.0f}"
    else:
        return f"SAR {price:,.2f}"


def get_source_badge(source_name: str) -> tuple:
    """Get badge label and color for source."""
    return SOURCE_BADGES.get(source_name, ("❓ Unknown", "#757575"))


def get_star_display(stars: int) -> str:
    """Get star display string."""
    if not stars:
        return "-"
    return "⭐" * stars


def get_trend_indicator(trend: str, change_percent: float = 0) -> str:
    """Get price trend indicator."""
    if trend == "down":
        return f"📉 {abs(change_percent):.1f}%"
    elif trend == "up":
        return f"📈 +{change_percent:.1f}%"
    else:
        return "➡️ Stabil"


# =============================================================================
# MAIN PAGE RENDERER
# =============================================================================

def render_price_comparison_page():
    """Render the price comparison page."""
    st.title("🔍 Perbandingan Harga Real-time")
    st.caption("Bandingkan harga dari berbagai sumber: API, OTA, dan Partner")

    if not HAS_PRICE_AGGREGATION:
        st.error("❌ Module price_aggregation tidak tersedia")
        st.info("Pastikan semua dependencies terinstall dengan benar.")
        return

    # Sidebar filters
    with st.sidebar:
        st.subheader("🎯 Filter")

        # City filter
        city = st.selectbox("Kota", CITIES)
        if city == "Semua Kota":
            city = None

        # Offer type filter
        offer_type_label = st.selectbox("Tipe", list(OFFER_TYPES.keys()))
        offer_type = OFFER_TYPES[offer_type_label]

        # Star filter
        min_stars = st.slider("Minimal Bintang", 1, 5, 3)

        # Price range filter
        st.markdown("**Rentang Harga (Juta IDR)**")
        col1, col2 = st.columns(2)
        with col1:
            min_price_m = st.number_input("Min", value=10, min_value=0, step=5)
        with col2:
            max_price_m = st.number_input("Max", value=100, min_value=0, step=5)

        min_price = min_price_m * 1_000_000
        max_price = max_price_m * 1_000_000 if max_price_m > 0 else None

        # Source filter
        st.markdown("**Sumber Data**")
        use_api = st.checkbox("API (Amadeus, Xotelo)", value=True)
        use_ota = st.checkbox("OTA (Traveloka, Tiket)", value=True)
        use_partner = st.checkbox("Partner", value=True)

        sources = []
        if use_api:
            sources.extend(["amadeus", "xotelo", "makcorps"])
        if use_ota:
            sources.extend(["traveloka", "tiket", "pegipegi"])
        if use_partner:
            sources.append("partner")

        if not sources:
            sources = None  # Show all

        # Sort option
        sort_label = st.selectbox("Urutkan", list(SORT_OPTIONS.keys()))
        sort_by = SORT_OPTIONS[sort_label]

        # Refresh button
        st.divider()
        force_refresh = st.button("🔄 Refresh Data", use_container_width=True)

    # Main content
    try:
        # Initialize aggregator
        aggregator = get_price_aggregator()

        # Connect to data manager if available
        if HAS_DATA_MANAGER:
            try:
                data_manager = get_umrah_data_manager()
                aggregator.set_data_manager(data_manager)
            except Exception as e:
                st.warning(f"⚠️ Data manager tidak tersedia: {e}")

        # Show loading
        with st.spinner("Mengambil data harga dari berbagai sumber..."):
            result = aggregator.aggregate(
                city=city,
                offer_type=offer_type,
                min_price=min_price,
                max_price=max_price,
                min_stars=min_stars,
                sources=sources,
                sort_by=sort_by,
                limit=50,
                force_refresh=force_refresh
            )

        # Display stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Ditemukan", result["total_found"])
        with col2:
            st.metric("Ditampilkan", result["total_returned"])
        with col3:
            source_count = len(result.get("source_stats", {}))
            st.metric("Sumber Data", f"{source_count} sumber")
        with col4:
            duration = result.get("duration_ms", 0)
            st.metric("Waktu Proses", f"{duration:.0f} ms")

        # Source stats
        if result.get("source_stats"):
            with st.expander("📊 Detail Sumber Data"):
                for source, count in result["source_stats"].items():
                    badge_label, badge_color = get_source_badge(source)
                    st.markdown(
                        f"<span style='background-color:{badge_color};color:white;"
                        f"padding:2px 8px;border-radius:4px;font-size:12px;'>{badge_label}</span> "
                        f"**{source}**: {count} hasil",
                        unsafe_allow_html=True
                    )

        # Errors
        if result.get("errors"):
            with st.expander("⚠️ Peringatan"):
                for error in result["errors"]:
                    st.warning(error)

        st.divider()

        # Display offers
        offers = result.get("offers", [])

        if not offers:
            st.info("🔍 Tidak ada hasil yang cocok dengan filter Anda.")
            return

        # Render offers
        render_offers_table(offers, offer_type)

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {e}")
        st.info("Coba refresh halaman atau periksa koneksi database.")


def render_offers_table(offers: List[AggregatedOffer], offer_type: str = None):
    """Render offers as a comparison table."""

    # Find best price for highlighting
    best_price = min(o.price_idr for o in offers if o.price_idr > 0) if offers else 0

    # Group by type if showing all
    if offer_type is None:
        hotels = [o for o in offers if o.offer_type == OfferType.HOTEL]
        packages = [o for o in offers if o.offer_type == OfferType.PACKAGE]

        if hotels:
            st.subheader("🏨 Hotel")
            render_hotel_cards(hotels, best_price)

        if packages:
            st.subheader("📦 Paket Umrah")
            render_package_cards(packages, best_price)
    elif offer_type == "hotel":
        render_hotel_cards(offers, best_price)
    else:
        render_package_cards(offers, best_price)


def render_hotel_cards(hotels: List[AggregatedOffer], best_price: float):
    """Render hotel offer cards."""
    for idx, hotel in enumerate(hotels):
        is_best = hotel.price_idr == best_price and best_price > 0

        with st.container():
            # Card styling
            border_color = "#4CAF50" if is_best else "#E0E0E0"

            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                # Hotel name and stars
                stars_display = get_star_display(hotel.stars)
                st.markdown(f"**{hotel.name}** {stars_display}")

                # City and distance
                distance_text = ""
                if hotel.distance_to_haram_m:
                    if hotel.distance_to_haram_m < 1000:
                        distance_text = f"{hotel.distance_to_haram_m}m dari Haram"
                    else:
                        distance_text = f"{hotel.distance_to_haram_m/1000:.1f}km dari Haram"

                st.caption(f"📍 {hotel.city} | {distance_text}")

            with col2:
                # Source badge
                badge_label, badge_color = get_source_badge(hotel.source_name)
                st.markdown(
                    f"<span style='background-color:{badge_color};color:white;"
                    f"padding:2px 8px;border-radius:4px;font-size:11px;'>{badge_label}</span>",
                    unsafe_allow_html=True
                )

                # Per night price
                if hotel.price_per_night_idr:
                    st.caption(f"{format_price(hotel.price_per_night_idr)}/malam")

            with col3:
                # Price
                price_display = format_price(hotel.price_idr)
                if is_best:
                    st.markdown(f"### 🏆 {price_display}")
                    st.caption("Harga Terbaik!")
                else:
                    st.markdown(f"### {price_display}")

                # Availability
                if not hotel.is_available:
                    st.error("Sold Out")
                elif hotel.rooms_left and hotel.rooms_left < 5:
                    st.warning(f"Sisa {hotel.rooms_left} kamar!")

            st.divider()


def render_package_cards(packages: List[AggregatedOffer], best_price: float):
    """Render package offer cards."""
    for idx, pkg in enumerate(packages):
        is_best = pkg.price_idr == best_price and best_price > 0

        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                # Package name
                st.markdown(f"**{pkg.name}**")

                # Duration and departure
                details = []
                if pkg.duration_days:
                    details.append(f"📅 {pkg.duration_days} Hari")
                if pkg.departure_city:
                    details.append(f"✈️ dari {pkg.departure_city}")
                if pkg.airline:
                    details.append(f"🛫 {pkg.airline}")

                st.caption(" | ".join(details))

                # Hotels
                hotel_info = []
                if pkg.hotel_makkah:
                    stars = "⭐" * (pkg.hotel_makkah_stars or 4)
                    hotel_info.append(f"Makkah: {pkg.hotel_makkah} {stars}")
                if pkg.hotel_madinah:
                    stars = "⭐" * (pkg.hotel_madinah_stars or 4)
                    hotel_info.append(f"Madinah: {pkg.hotel_madinah} {stars}")

                if hotel_info:
                    st.caption(" | ".join(hotel_info))

            with col2:
                # Source badge
                badge_label, badge_color = get_source_badge(pkg.source_name)
                st.markdown(
                    f"<span style='background-color:{badge_color};color:white;"
                    f"padding:2px 8px;border-radius:4px;font-size:11px;'>{badge_label}</span>",
                    unsafe_allow_html=True
                )

                # Inclusions
                if pkg.inclusions:
                    inclusions_text = ", ".join(pkg.inclusions[:3])
                    if len(pkg.inclusions) > 3:
                        inclusions_text += f" +{len(pkg.inclusions) - 3} lainnya"
                    st.caption(f"✅ {inclusions_text}")

            with col3:
                # Price
                price_display = format_price(pkg.price_idr)
                if is_best:
                    st.markdown(f"### 🏆 {price_display}")
                    st.caption("Harga Terbaik!")
                else:
                    st.markdown(f"### {price_display}")

                # Availability
                if not pkg.is_available:
                    st.error("Sold Out")
                elif pkg.quota:
                    available = pkg.quota - (pkg.quota if hasattr(pkg, 'booked') else 0)
                    if available < 10:
                        st.warning(f"Sisa {available} seat!")

            st.divider()


def render_best_prices_widget():
    """Render best prices widget for sidebar."""
    st.subheader("💰 Harga Terbaik Hari Ini")

    if not HAS_PRICE_AGGREGATION:
        st.caption("Fitur tidak tersedia")
        return

    try:
        aggregator = get_price_aggregator()

        # Get best prices by source
        best_prices = aggregator.get_best_prices(offer_type="hotel")

        if not best_prices:
            st.caption("Belum ada data")
            return

        for offer in best_prices[:5]:
            badge_label, badge_color = get_source_badge(offer.source_name)
            st.markdown(
                f"**{offer.name[:25]}...**\n\n"
                f"{format_price(offer.price_idr)} - {offer.city}",
            )

    except Exception as e:
        st.caption(f"Error: {e}")


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [
    "render_price_comparison_page",
    "render_best_prices_widget",
]
