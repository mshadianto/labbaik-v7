"""
LABBAIK AI v6.0 - Cost Simulator (Super WOW Edition)
====================================================
Advanced cost calculator with interactive charts,
package comparison, budget planner, and savings tips.
"""

import streamlit as st
from datetime import date, datetime, timedelta
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json

# =============================================================================
# DATA CLASSES & CONSTANTS
# =============================================================================

class Season(str, Enum):
    REGULAR = "regular"
    HIGH = "high"
    PEAK = "peak"       # Ramadan
    SUPER_PEAK = "super_peak"  # Haji season


@dataclass
class CostBreakdown:
    """Cost breakdown structure."""
    flight: int
    visa: int
    hotel_makkah: int
    hotel_madinah: int
    transport: int
    meals: int
    mutawif: int
    insurance: int
    misc: int
    seasonal_adj: int
    total: int


# Pricing data
FLIGHT_PRICES = {
    "Jakarta": {"economy": 8_000_000, "business": 25_000_000},
    "Surabaya": {"economy": 8_500_000, "business": 26_000_000},
    "Bandung": {"economy": 8_200_000, "business": 25_500_000},
    "Medan": {"economy": 9_000_000, "business": 27_000_000},
    "Makassar": {"economy": 9_500_000, "business": 28_000_000},
    "Semarang": {"economy": 8_300_000, "business": 25_800_000},
    "Yogyakarta": {"economy": 8_400_000, "business": 26_000_000},
    "Palembang": {"economy": 8_800_000, "business": 27_000_000},
    "Balikpapan": {"economy": 9_200_000, "business": 28_500_000},
    "Pekanbaru": {"economy": 8_600_000, "business": 26_500_000},
}

HOTEL_PRICES_PER_NIGHT = {
    "makkah": {
        2: 400_000,
        3: 700_000,
        4: 1_500_000,
        5: 3_500_000,
    },
    "madinah": {
        2: 350_000,
        3: 600_000,
        4: 1_200_000,
        5: 2_800_000,
    }
}

SEASONAL_MULTIPLIERS = {
    Season.REGULAR: 1.0,
    Season.HIGH: 1.15,
    Season.PEAK: 1.35,
    Season.SUPER_PEAK: 1.50,
}

VISA_COST = 1_500_000
INSURANCE_BASE = 500_000
MUTAWIF_COST = 2_000_000
TRANSPORT_COST = 1_500_000
MEALS_PER_DAY = {
    "none": 0,
    "basic": 150_000,
    "standard": 250_000,
    "premium": 400_000,
}


# =============================================================================
# CALCULATION FUNCTIONS
# =============================================================================

def get_season(departure_date: date) -> Tuple[Season, str]:
    """Determine season based on departure date."""
    month = departure_date.month
    
    if month == 3 or month == 4:
        return Season.PEAK, "🌙 Musim Ramadan - Harga tertinggi"
    elif month == 6 or month == 7:
        return Season.SUPER_PEAK, "🕋 Musim Haji - Harga sangat tinggi"
    elif month == 12 or month == 1:
        return Season.HIGH, "🎄 Musim Liburan - Harga tinggi"
    else:
        return Season.REGULAR, "✅ Musim Reguler - Harga normal"


def calculate_cost(
    departure_city: str,
    departure_date: date,
    duration: int,
    nights_makkah: int,
    nights_madinah: int,
    hotel_star_makkah: int,
    hotel_star_madinah: int,
    flight_class: str,
    meal_type: str,
    num_travelers: int,
    include_mutawif: bool,
    include_insurance: bool,
) -> CostBreakdown:
    """Calculate detailed cost breakdown."""
    
    # Flight
    flight_prices = FLIGHT_PRICES.get(departure_city, FLIGHT_PRICES["Jakarta"])
    flight = flight_prices.get(flight_class, flight_prices["economy"])
    
    # Visa
    visa = VISA_COST
    
    # Hotels
    hotel_makkah = HOTEL_PRICES_PER_NIGHT["makkah"].get(hotel_star_makkah, 700_000) * nights_makkah
    hotel_madinah = HOTEL_PRICES_PER_NIGHT["madinah"].get(hotel_star_madinah, 600_000) * nights_madinah
    
    # Transport
    transport = TRANSPORT_COST
    
    # Meals
    meals = MEALS_PER_DAY.get(meal_type, 0) * duration
    
    # Mutawif
    mutawif = MUTAWIF_COST if include_mutawif else 0
    
    # Insurance
    insurance = INSURANCE_BASE if include_insurance else 0
    
    # Misc (tips, zamzam, souvenirs, etc)
    misc = 2_000_000
    
    # Subtotal
    subtotal = flight + visa + hotel_makkah + hotel_madinah + transport + meals + mutawif + insurance + misc
    
    # Seasonal adjustment
    season, _ = get_season(departure_date)
    multiplier = SEASONAL_MULTIPLIERS.get(season, 1.0)
    seasonal_adj = int(subtotal * (multiplier - 1))
    
    # Total per person
    total = subtotal + seasonal_adj
    
    return CostBreakdown(
        flight=flight,
        visa=visa,
        hotel_makkah=hotel_makkah,
        hotel_madinah=hotel_madinah,
        transport=transport,
        meals=meals,
        mutawif=mutawif,
        insurance=insurance,
        misc=misc,
        seasonal_adj=seasonal_adj,
        total=total,
    )


def format_currency(amount: int) -> str:
    """Format as Indonesian Rupiah."""
    return f"Rp {amount:,.0f}".replace(",", ".")


# =============================================================================
# SESSION STATE
# =============================================================================

def init_simulator_state():
    """Initialize simulator session state."""
    
    if "sim_history" not in st.session_state:
        st.session_state.sim_history = []
    
    if "sim_saved" not in st.session_state:
        st.session_state.sim_saved = []


# =============================================================================
# RENDER COMPONENTS
# =============================================================================

def render_input_section() -> Dict:
    """Render input form and return parameters."""
    
    st.markdown("## 🎛️ Konfigurasi Trip")
    
    params = {}
    
    # Section 1: Basic info
    with st.expander("✈️ Keberangkatan", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            params["departure_city"] = st.selectbox(
                "Kota Keberangkatan",
                list(FLIGHT_PRICES.keys()),
                index=0
            )
            
            params["departure_date"] = st.date_input(
                "Tanggal Berangkat",
                min_value=date.today() + timedelta(days=30),
                value=date.today() + timedelta(days=60)
            )
        
        with col2:
            params["flight_class"] = st.radio(
                "Kelas Penerbangan",
                ["economy", "business"],
                format_func=lambda x: "✈️ Ekonomi" if x == "economy" else "💺 Business",
                horizontal=True
            )
            
            # Show season
            season, season_desc = get_season(params["departure_date"])
            if season == Season.REGULAR:
                st.success(season_desc)
            elif season == Season.HIGH:
                st.info(season_desc)
            elif season == Season.PEAK:
                st.warning(season_desc)
            else:
                st.error(season_desc)
    
    # Section 2: Duration
    with st.expander("📅 Durasi & Pembagian", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            params["duration"] = st.selectbox(
                "Total Durasi",
                [9, 10, 12, 14, 21],
                format_func=lambda x: f"{x} hari / {x-1} malam",
                index=1
            )
        
        with col2:
            params["num_travelers"] = st.number_input(
                "Jumlah Jamaah",
                min_value=1,
                max_value=50,
                value=1
            )
        
        max_nights = params["duration"] - 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            params["nights_makkah"] = st.slider(
                "🕋 Malam di Makkah",
                min_value=3,
                max_value=max_nights - 2,
                value=min(5, max_nights - 3)
            )
        
        with col2:
            params["nights_madinah"] = max_nights - params["nights_makkah"]
            st.info(f"🕌 {params['nights_madinah']} malam di Madinah")
    
    # Section 3: Accommodation
    with st.expander("🏨 Akomodasi", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            params["hotel_star_makkah"] = st.select_slider(
                "Hotel Makkah",
                options=[2, 3, 4, 5],
                value=4,
                format_func=lambda x: "⭐" * x
            )
            
            # Show hotel info
            price = HOTEL_PRICES_PER_NIGHT["makkah"][params["hotel_star_makkah"]]
            st.caption(f"{format_currency(price)}/malam")
        
        with col2:
            params["hotel_star_madinah"] = st.select_slider(
                "Hotel Madinah",
                options=[2, 3, 4, 5],
                value=4,
                format_func=lambda x: "⭐" * x
            )
            
            price = HOTEL_PRICES_PER_NIGHT["madinah"][params["hotel_star_madinah"]]
            st.caption(f"{format_currency(price)}/malam")
    
    # Section 4: Services
    with st.expander("🍽️ Layanan", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            params["meal_type"] = st.selectbox(
                "Paket Makan",
                ["none", "basic", "standard", "premium"],
                index=2,
                format_func=lambda x: {
                    "none": "❌ Tidak termasuk",
                    "basic": "🍚 Basic (Rp 150k/hari)",
                    "standard": "🍱 Standard (Rp 250k/hari)",
                    "premium": "🍽️ Premium (Rp 400k/hari)",
                }.get(x, x)
            )
        
        with col2:
            params["include_mutawif"] = st.checkbox("👨‍🏫 Mutawif (Rp 2 Juta)", value=True)
            params["include_insurance"] = st.checkbox("🛡️ Asuransi (Rp 500k)", value=True)
    
    return params


def render_cost_breakdown(cost: CostBreakdown, num_travelers: int):
    """Render detailed cost breakdown."""
    
    st.markdown("## 💰 Rincian Biaya")
    
    # Per person breakdown
    with st.container(border=True):
        st.markdown("### Per Orang")
        
        items = [
            ("✈️ Tiket Pesawat", cost.flight),
            ("📋 Visa Umrah", cost.visa),
            ("🕋 Hotel Makkah", cost.hotel_makkah),
            ("🕌 Hotel Madinah", cost.hotel_madinah),
            ("🚌 Transportasi", cost.transport),
            ("🍽️ Makan", cost.meals),
            ("👨‍🏫 Mutawif", cost.mutawif),
            ("🛡️ Asuransi", cost.insurance),
            ("🎁 Lain-lain", cost.misc),
        ]
        
        col1, col2 = st.columns([3, 2])
        
        for item, amount in items:
            if amount > 0:
                with col1:
                    st.markdown(item)
                with col2:
                    st.markdown(format_currency(amount))
        
        # Seasonal adjustment
        if cost.seasonal_adj > 0:
            st.markdown("---")
            with col1:
                st.markdown("📅 **Penyesuaian Musim**")
            with col2:
                st.markdown(f"+{format_currency(cost.seasonal_adj)}")
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("### Total per Orang")
        with col2:
            st.markdown(f"### {format_currency(cost.total)}")
    
    # Group total if multiple travelers
    if num_travelers > 1:
        with st.container(border=True):
            st.markdown("### 👥 Total Grup")
            
            group_total = cost.total * num_travelers
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Jamaah", f"{num_travelers} orang")
            
            with col2:
                st.metric("Total Biaya Grup", format_currency(group_total))


def render_cost_chart(cost: CostBreakdown):
    """Render cost distribution chart."""
    
    st.markdown("## 📊 Distribusi Biaya")
    
    # Prepare data for chart
    data = {
        "Komponen": ["Tiket", "Visa", "Hotel Makkah", "Hotel Madinah", "Transport", "Makan", "Mutawif", "Asuransi", "Lainnya"],
        "Biaya": [cost.flight, cost.visa, cost.hotel_makkah, cost.hotel_madinah, cost.transport, cost.meals, cost.mutawif, cost.insurance, cost.misc]
    }
    
    # Filter out zero values
    filtered_data = [(k, v) for k, v in zip(data["Komponen"], data["Biaya"]) if v > 0]
    
    # Simple bar representation
    total = sum([v for _, v in filtered_data])
    
    for item, amount in filtered_data:
        pct = amount / total * 100
        st.markdown(f"**{item}** ({pct:.1f}%)")
        st.progress(pct / 100)
        st.caption(format_currency(amount))


def render_comparison():
    """Render package comparison section."""
    
    st.markdown("## 🔄 Perbandingan Paket")
    st.caption("Bandingkan berbagai konfigurasi trip")
    
    # Quick comparison presets
    presets = {
        "Backpacker": {"hotel": 3, "meals": "none", "mutawif": False},
        "Reguler": {"hotel": 4, "meals": "standard", "mutawif": True},
        "Premium": {"hotel": 5, "meals": "premium", "mutawif": True},
    }
    
    cols = st.columns(3)
    
    for col, (name, config) in zip(cols, presets.items()):
        with col:
            # Calculate cost for this preset
            cost = calculate_cost(
                departure_city="Jakarta",
                departure_date=date.today() + timedelta(days=60),
                duration=10,
                nights_makkah=5,
                nights_madinah=4,
                hotel_star_makkah=config["hotel"],
                hotel_star_madinah=config["hotel"],
                flight_class="economy",
                meal_type=config["meals"],
                num_travelers=1,
                include_mutawif=config["mutawif"],
                include_insurance=True,
            )
            
            with st.container(border=True):
                st.markdown(f"### {name}")
                st.markdown(f"## {format_currency(cost.total)}")
                st.caption("per orang")
                
                st.markdown(f"🏨 Hotel Bintang {config['hotel']}")
                st.markdown(f"🍽️ Makan: {config['meals'].title()}")
                st.markdown(f"👨‍🏫 Mutawif: {'Ya' if config['mutawif'] else 'Tidak'}")


def render_savings_tips(cost: CostBreakdown):
    """Render money-saving tips."""
    
    st.markdown("## 💡 Tips Hemat")
    
    tips = []
    
    # Flight tips
    if cost.flight > 8_500_000:
        tips.append({
            "icon": "✈️",
            "title": "Pilih Penerbangan Ekonomi",
            "desc": "Hemat hingga Rp 17 Juta dengan memilih kelas ekonomi",
            "savings": "s/d Rp 17.000.000"
        })
    
    # Hotel tips
    if cost.hotel_makkah > 1_500_000 * 5:
        tips.append({
            "icon": "🏨",
            "title": "Downgrade Hotel",
            "desc": "Hotel bintang 3-4 masih nyaman dan lebih hemat",
            "savings": "s/d Rp 10.000.000"
        })
    
    # Season tips
    if cost.seasonal_adj > 0:
        tips.append({
            "icon": "📅",
            "title": "Pilih Musim Reguler",
            "desc": "Berangkat di bulan Mei, Sep, Oct, atau Nov untuk harga normal",
            "savings": f"s/d {format_currency(cost.seasonal_adj)}"
        })
    
    # Meals tips
    if cost.meals > 0:
        tips.append({
            "icon": "🍽️",
            "title": "Makan Mandiri",
            "desc": "Banyak pilihan makanan halal dengan harga terjangkau di sekitar hotel",
            "savings": f"s/d {format_currency(cost.meals)}"
        })
    
    # Group tips
    tips.append({
        "icon": "👥",
        "title": "Berangkat Rombongan",
        "desc": "Dapat diskon grup untuk 10+ jamaah",
        "savings": "5-15%"
    })
    
    if tips:
        for tip in tips:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {tip['icon']} {tip['title']}")
                    st.caption(tip['desc'])
                
                with col2:
                    st.success(f"💰 {tip['savings']}")
    else:
        st.success("✅ Konfigurasi Anda sudah cukup hemat!")


def render_budget_planner(cost: CostBreakdown, num_travelers: int):
    """Render budget/savings planner."""
    
    st.markdown("## 📈 Rencana Tabungan")
    
    total_needed = cost.total * num_travelers
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_savings = st.number_input(
            "💰 Tabungan Saat Ini (Rp)",
            min_value=0,
            max_value=total_needed * 2,
            value=0,
            step=1_000_000,
            format="%d"
        )
    
    with col2:
        target_date = st.date_input(
            "📅 Target Berangkat",
            min_value=date.today() + timedelta(days=30),
            value=date.today() + timedelta(days=180)
        )
    
    # Calculate
    remaining = max(total_needed - current_savings, 0)
    days_left = (target_date - date.today()).days
    months_left = days_left / 30
    
    if remaining > 0 and months_left > 0:
        monthly_saving = int(remaining / months_left)
        weekly_saving = int(remaining / (days_left / 7))
        daily_saving = int(remaining / days_left)
        
        with st.container(border=True):
            st.markdown("### 🎯 Target Tabungan")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Per Bulan", format_currency(monthly_saving))
            
            with col2:
                st.metric("Per Minggu", format_currency(weekly_saving))
            
            with col3:
                st.metric("Per Hari", format_currency(daily_saving))
            
            # Progress bar
            progress = current_savings / total_needed
            st.progress(progress)
            st.caption(f"Terkumpul: {progress * 100:.1f}% ({format_currency(current_savings)} dari {format_currency(total_needed)})")
    
    elif remaining == 0:
        st.success("🎉 Tabungan Anda sudah cukup! Siap berangkat umrah!")
    else:
        st.info("Masukkan tabungan saat ini untuk melihat rencana")


def render_save_simulation(params: Dict, cost: CostBreakdown):
    """Render save/export simulation."""
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Simpan Simulasi", use_container_width=True):
            simulation = {
                "timestamp": datetime.now().isoformat(),
                "params": {k: str(v) if isinstance(v, date) else v for k, v in params.items()},
                "total": cost.total,
            }
            st.session_state.sim_saved.append(simulation)
            st.success("✅ Simulasi disimpan!")
    
    with col2:
        if st.button("📤 Export PDF", use_container_width=True):
            st.info("Fitur export PDF akan segera hadir")
    
    with col3:
        if st.button("📱 Share WhatsApp", use_container_width=True):
            total = format_currency(cost.total)
            msg = f"Simulasi Umrah LABBAIK:\n💰 Total: {total}/orang\n🔗 Hitung di: labbaik.streamlit.app"
            st.code(msg)
            st.caption("Copy dan paste ke WhatsApp")


def render_saved_simulations():
    """Render saved simulations."""
    
    saved = st.session_state.get("sim_saved", [])
    
    if saved:
        st.markdown("## 📁 Simulasi Tersimpan")
        
        for i, sim in enumerate(saved[-5:], 1):  # Show last 5
            with st.container(border=True):
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    st.caption(f"#{i}")
                
                with col2:
                    params = sim["params"]
                    st.caption(f"{params.get('departure_city', 'N/A')} | {params.get('duration', 0)} hari")
                
                with col3:
                    st.markdown(f"**{format_currency(sim['total'])}**")


# =============================================================================
# LIVE HOTEL PRICES
# =============================================================================

def render_live_hotel_prices(params: Dict):
    """Render live hotel prices from APIs."""

    st.markdown("## 🏨 Harga Hotel Live")
    st.caption("Data real-time dari berbagai sumber (Amadeus, Xotelo, dll)")

    # Try to load live data
    try:
        from services.umrah import get_cost_integration_service

        service = get_cost_integration_service()

        # Format dates
        check_in = params.get("departure_date")
        if check_in:
            check_in_str = check_in.strftime("%Y-%m-%d")
            duration = params.get("duration", 10)
            check_out_str = (check_in + timedelta(days=duration)).strftime("%Y-%m-%d")
        else:
            check_in_str = None
            check_out_str = None

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🕋 Hotel Makkah")

            makkah_price = service.get_hotel_price(
                "Makkah",
                params.get("hotel_star_makkah", 4),
                check_in_str,
                check_out_str
            )

            with st.container(border=True):
                # Data source indicator
                if makkah_price.is_live_data:
                    st.success(f"🟢 Live Data ({makkah_price.source})")
                else:
                    st.warning("🟡 Data Estimasi")

                st.markdown(f"**{makkah_price.hotel_name}**")
                st.markdown(f"{'⭐' * makkah_price.hotel_stars}")

                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Per Malam", format_currency(makkah_price.price_per_night_idr))
                with metric_col2:
                    st.metric("Jarak", f"{makkah_price.distance_to_haram_km:.1f} km")

                st.caption(f"🚶 {makkah_price.walking_time_minutes} menit ke Masjidil Haram")

        with col2:
            st.markdown("### 🕌 Hotel Madinah")

            madinah_price = service.get_hotel_price(
                "Madinah",
                params.get("hotel_star_madinah", 4),
                check_in_str,
                check_out_str
            )

            with st.container(border=True):
                if madinah_price.is_live_data:
                    st.success(f"🟢 Live Data ({madinah_price.source})")
                else:
                    st.warning("🟡 Data Estimasi")

                st.markdown(f"**{madinah_price.hotel_name}**")
                st.markdown(f"{'⭐' * madinah_price.hotel_stars}")

                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Per Malam", format_currency(madinah_price.price_per_night_idr))
                with metric_col2:
                    st.metric("Jarak", f"{madinah_price.distance_to_haram_km:.1f} km")

                st.caption(f"🚶 {madinah_price.walking_time_minutes} menit ke Masjid Nabawi")

        # Transport section
        st.markdown("---")
        st.markdown("### 🚄 Transportasi Makkah - Madinah")

        transport = service.get_transport_price("Makkah", "Madinah", "train")

        transport_cols = st.columns(3)
        with transport_cols[0]:
            with st.container(border=True):
                st.markdown("**🚄 Haramain Train**")
                st.markdown(f"**{format_currency(transport.get('price_idr', 420000))}**")
                st.caption(f"~{transport.get('duration_hours', 2.5)} jam")

        with transport_cols[1]:
            bus = service.get_transport_price("Makkah", "Madinah", "bus")
            with st.container(border=True):
                st.markdown("**🚌 SAPTCO Bus**")
                st.markdown(f"**{format_currency(bus.get('price_idr', 210000))}**")
                st.caption(f"~{bus.get('duration_hours', 5)} jam")

        with transport_cols[2]:
            car = service.get_transport_price("Makkah", "Madinah", "private_car")
            with st.container(border=True):
                st.markdown("**🚗 Private Car**")
                st.markdown(f"**{format_currency(car.get('price_idr', 840000))}**")
                st.caption(f"~{car.get('duration_hours', 4.5)} jam")

        # Show all available hotels
        st.markdown("---")
        with st.expander("📋 Lihat Semua Hotel Tersedia"):
            city_choice = st.radio(
                "Pilih Kota",
                ["Makkah", "Madinah"],
                horizontal=True,
                key="live_hotel_city"
            )

            hotels = service.get_hotels_by_city(city_choice, check_in_str, check_out_str, max_results=10)

            if hotels:
                for hotel in hotels:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.markdown(f"**{hotel['hotel_name']}**")
                            st.caption(f"{'⭐' * hotel['stars']} | {hotel['rating']}")
                        with col2:
                            st.markdown(f"**{format_currency(hotel['price_per_night_idr'])}**/malam")
                        with col3:
                            st.caption(f"📍 {hotel['distance_to_haram_km']:.1f} km")
                            st.caption(f"🚶 {hotel['walking_time_minutes']} min")
            else:
                st.info("Tidak ada data hotel tersedia")

    except ImportError:
        st.info("🔧 Modul data live belum tersedia. Gunakan estimasi statis.")
    except Exception as e:
        st.warning(f"⚠️ Gagal memuat data live: {str(e)}")
        st.info("Menggunakan estimasi harga statis")


# =============================================================================
# MAIN PAGE RENDERER
# =============================================================================

def render_simulator_page():
    """Main cost simulator page renderer."""

    # Track page view
    try:
        from services.analytics import track_page
        track_page("simulator")
    except:
        pass
    
    # Initialize state
    init_simulator_state()
    
    # Header
    st.markdown("# 💰 Simulasi Biaya Umrah")
    st.caption("Hitung estimasi biaya umrah sesuai preferensi Anda")
    
    # Quick info
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💚 Mulai Dari", "Rp 15 Juta")
        with col2:
            st.metric("⭐ Paket Populer", "Rp 25 Juta")
        with col3:
            st.metric("👑 VIP", "Rp 55 Juta")
        with col4:
            st.metric("📊 Akurasi", "95%+")
    
    st.divider()
    
    # Two column layout
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        params = render_input_section()
    
    # Calculate
    cost = calculate_cost(
        departure_city=params["departure_city"],
        departure_date=params["departure_date"],
        duration=params["duration"],
        nights_makkah=params["nights_makkah"],
        nights_madinah=params["nights_madinah"],
        hotel_star_makkah=params["hotel_star_makkah"],
        hotel_star_madinah=params["hotel_star_madinah"],
        flight_class=params["flight_class"],
        meal_type=params["meal_type"],
        num_travelers=params["num_travelers"],
        include_mutawif=params["include_mutawif"],
        include_insurance=params["include_insurance"],
    )
    
    with col_result:
        # Main result
        with st.container(border=True):
            st.markdown("## 🎯 Estimasi Total")
            st.markdown(f"# {format_currency(cost.total)}")
            st.caption("per orang")
            
            if params["num_travelers"] > 1:
                group_total = cost.total * params["num_travelers"]
                st.info(f"👥 Total {params['num_travelers']} orang: **{format_currency(group_total)}**")
        
        # Quick breakdown
        render_cost_breakdown(cost, params["num_travelers"])
    
    st.divider()

    # Additional sections
    tabs = st.tabs(["📊 Grafik", "🔄 Perbandingan", "💡 Tips Hemat", "📈 Rencana Tabungan", "🏨 Hotel Live"])

    with tabs[0]:
        render_cost_chart(cost)

    with tabs[1]:
        render_comparison()

    with tabs[2]:
        render_savings_tips(cost)

    with tabs[3]:
        render_budget_planner(cost, params["num_travelers"])

    with tabs[4]:
        render_live_hotel_prices(params)
    
    # Save/export
    render_save_simulation(params, cost)
    
    # Saved simulations
    render_saved_simulations()
    
    # Footer
    st.divider()
    st.caption("💡 Harga bersifat estimasi dan dapat berubah. Hubungi tim kami untuk penawaran terbaik.")


# Export
__all__ = ["render_simulator_page"]
