"""
LABBAIK AI v6.0 - Premium Booking Flow
======================================
Complete booking experience with real-time pricing,
package comparison, and interactive UI.
"""

import streamlit as st
from datetime import date, timedelta, datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import random
import json

# =============================================================================
# DATA CLASSES & ENUMS
# =============================================================================

class BookingStep(str, Enum):
    PACKAGE = "package"
    SCHEDULE = "schedule"
    TRAVELERS = "travelers"
    ADDONS = "addons"
    REVIEW = "review"
    PAYMENT = "payment"
    CONFIRMATION = "confirmation"


class PackageType(str, Enum):
    BACKPACKER = "backpacker"
    REGULER = "reguler"
    PLUS = "plus"
    VIP = "vip"
    MANDIRI = "mandiri"


class HotelCategory(str, Enum):
    BUDGET = "budget"       # Bintang 2-3
    STANDARD = "standard"   # Bintang 3
    SUPERIOR = "superior"   # Bintang 4
    PREMIUM = "premium"     # Bintang 5
    DELUXE = "deluxe"      # Bintang 5+


@dataclass
class Package:
    """Package definition."""
    type: PackageType
    name: str
    icon: str
    description: str
    base_price: int
    hotel_makkah: str
    hotel_madinah: str
    distance_haram: str
    meals: str
    transport: str
    mutawif: str
    features: List[str]
    popular: bool = False
    best_value: bool = False


@dataclass
class Traveler:
    """Traveler information."""
    name: str
    passport_number: str
    passport_expiry: date
    birth_date: date
    gender: str
    nationality: str
    phone: str
    email: str
    is_primary: bool = False
    special_needs: str = ""
    room_preference: str = "double"


@dataclass
class AddOn:
    """Add-on service."""
    id: str
    name: str
    icon: str
    description: str
    price: int
    category: str
    popular: bool = False


# =============================================================================
# PACKAGE DEFINITIONS
# =============================================================================

PACKAGES = [
    Package(
        type=PackageType.BACKPACKER,
        name="Backpacker",
        icon="🎒",
        description="Paket ekonomis untuk jamaah mandiri yang ingin pengalaman autentik",
        base_price=18_000_000,
        hotel_makkah="Hotel Bintang 2-3",
        hotel_madinah="Hotel Bintang 2-3",
        distance_haram="800m - 1.5km",
        meals="Tidak termasuk",
        transport="Bus sharing",
        mutawif="Sharing group (1:30)",
        features=[
            "✈️ Tiket pesawat PP",
            "🏨 Hotel 9 malam",
            "📋 Visa umrah",
            "🚌 Transport bandara",
            "📚 Panduan digital",
            "💬 Support 24/7",
        ],
    ),
    Package(
        type=PackageType.REGULER,
        name="Reguler",
        icon="⭐",
        description="Paket standar dengan keseimbangan harga dan kenyamanan",
        base_price=25_000_000,
        hotel_makkah="Hotel Bintang 3-4",
        hotel_madinah="Hotel Bintang 3-4",
        distance_haram="400m - 800m",
        meals="3x sehari (prasmanan)",
        transport="Bus AC group",
        mutawif="Sharing (1:20)",
        features=[
            "✈️ Tiket pesawat PP",
            "🏨 Hotel 9 malam",
            "📋 Visa umrah",
            "🍽️ Makan 3x sehari",
            "🚌 Transport full",
            "👨‍🏫 Mutawif berpengalaman",
            "🎁 Perlengkapan umrah",
            "📸 Dokumentasi",
        ],
        popular=True,
    ),
    Package(
        type=PackageType.PLUS,
        name="Plus",
        icon="🌟",
        description="Paket premium dengan fasilitas lebih dan kenyamanan ekstra",
        base_price=35_000_000,
        hotel_makkah="Hotel Bintang 4-5",
        hotel_madinah="Hotel Bintang 4-5",
        distance_haram="200m - 400m",
        meals="3x sehari + snack",
        transport="Bus VIP / Hiace",
        mutawif="Dedicated (1:15)",
        features=[
            "✈️ Tiket pesawat PP (bagasi 30kg)",
            "🏨 Hotel premium 9 malam",
            "📋 Visa umrah + handling VIP",
            "🍽️ Makan premium",
            "🚌 Transport VIP",
            "👨‍🏫 Mutawif senior",
            "🎁 Perlengkapan premium",
            "🕌 Ziarah tambahan",
            "📸 Album foto profesional",
        ],
        best_value=True,
    ),
    Package(
        type=PackageType.VIP,
        name="VIP Executive",
        icon="👑",
        description="Pengalaman umrah mewah dengan pelayanan terbaik",
        base_price=55_000_000,
        hotel_makkah="Hotel Bintang 5 (Fairmont/Pullman)",
        hotel_madinah="Hotel Bintang 5 (Oberoi/Crowne)",
        distance_haram="< 100m (view Ka'bah)",
        meals="Fine dining + room service",
        transport="Private car / Limousine",
        mutawif="Personal (1:5)",
        features=[
            "✈️ Business class flight",
            "🏨 Suite room 9 malam",
            "📋 Fast track visa & handling",
            "🍽️ Fine dining experience",
            "🚗 Private transport",
            "👨‍🏫 Personal mutawif",
            "🎁 Luxury amenities",
            "🕌 Private ziarah tour",
            "📸 Professional videography",
            "🎖️ Lounge access",
            "💆 Spa & wellness",
        ],
    ),
    Package(
        type=PackageType.MANDIRI,
        name="Mandiri",
        icon="🧭",
        description="Fleksibilitas penuh untuk umrah mandiri berpengalaman",
        base_price=15_000_000,
        hotel_makkah="Pilihan sendiri",
        hotel_madinah="Pilihan sendiri",
        distance_haram="Sesuai pilihan",
        meals="Tidak termasuk",
        transport="Tidak termasuk",
        mutawif="Panduan digital + hotline",
        features=[
            "📋 Visa umrah",
            "📚 Panduan digital lengkap",
            "💬 24/7 hotline support",
            "🗺️ Rekomendasi hotel",
            "📍 GPS guided tour",
            "🎓 Video tutorial ibadah",
        ],
    ),
]


# =============================================================================
# ADD-ONS DEFINITIONS
# =============================================================================

ADDONS = [
    AddOn(
        id="travel_insurance",
        name="Asuransi Perjalanan Premium",
        icon="🛡️",
        description="Perlindungan medis hingga $100,000 + evakuasi",
        price=500_000,
        category="protection",
        popular=True,
    ),
    AddOn(
        id="extra_baggage",
        name="Extra Bagasi 10kg",
        icon="🧳",
        description="Tambahan bagasi untuk oleh-oleh",
        price=350_000,
        category="comfort",
    ),
    AddOn(
        id="airport_lounge",
        name="Airport Lounge Access",
        icon="✨",
        description="Akses lounge premium di bandara",
        price=450_000,
        category="comfort",
    ),
    AddOn(
        id="ziarah_makkah",
        name="Ziarah Plus Makkah",
        icon="🕋",
        description="Jabal Rahmah, Gua Hira, Muzdalifah, Mina",
        price=350_000,
        category="experience",
        popular=True,
    ),
    AddOn(
        id="ziarah_madinah",
        name="Ziarah Plus Madinah",
        icon="🕌",
        description="Uhud, Quba, Qiblatain, Khandaq",
        price=300_000,
        category="experience",
    ),
    AddOn(
        id="simcard",
        name="SIM Card Saudi (10GB)",
        icon="📱",
        description="Internet + telepon lokal",
        price=150_000,
        category="utility",
    ),
    AddOn(
        id="zamzam_5l",
        name="Air Zamzam 5 Liter",
        icon="💧",
        description="Kemasan khusus untuk dibawa pulang",
        price=100_000,
        category="souvenir",
    ),
    AddOn(
        id="prayer_set",
        name="Set Perlengkapan Sholat Premium",
        icon="📿",
        description="Sajadah + tasbih + mukena/sarung",
        price=250_000,
        category="utility",
    ),
    AddOn(
        id="photography",
        name="Foto Profesional",
        icon="📸",
        description="50+ foto edited + album digital",
        price=500_000,
        category="experience",
    ),
    AddOn(
        id="wheelchair",
        name="Layanan Kursi Roda",
        icon="♿",
        description="Kursi roda + pendamping saat thawaf/sa'i",
        price=400_000,
        category="special",
    ),
]


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def format_currency(amount: int) -> str:
    """Format number as Indonesian Rupiah."""
    return f"Rp {amount:,.0f}".replace(",", ".")


def calculate_total_price(data: Dict) -> Dict[str, int]:
    """Calculate total booking price."""
    package = next((p for p in PACKAGES if p.type.value == data.get("package_type")), None)
    if not package:
        return {"base": 0, "addons": 0, "seasonal": 0, "total": 0}
    
    travelers = data.get("travelers", [])
    traveler_count = max(len(travelers), 1)
    
    # Base price
    base_price = package.base_price * traveler_count
    
    # Hotel upgrade
    hotel_upgrade = 0
    hotel_star = data.get("hotel_star", 3)
    if hotel_star == 4:
        hotel_upgrade = 3_000_000 * traveler_count
    elif hotel_star == 5:
        hotel_upgrade = 8_000_000 * traveler_count
    
    # Add-ons
    selected_addons = data.get("addons", [])
    addons_price = 0
    for addon_id in selected_addons:
        addon = next((a for a in ADDONS if a.id == addon_id), None)
        if addon:
            addons_price += addon.price * traveler_count
    
    # Seasonal adjustment
    dep_date = data.get("departure_date")
    seasonal = 0
    if dep_date:
        month = dep_date.month
        if month in [3, 4]:  # Ramadan
            seasonal = int(base_price * 0.25)
        elif month in [6, 7, 12]:  # Peak season
            seasonal = int(base_price * 0.15)
    
    total = base_price + hotel_upgrade + addons_price + seasonal
    
    return {
        "base": base_price,
        "hotel_upgrade": hotel_upgrade,
        "addons": addons_price,
        "seasonal": seasonal,
        "total": total,
        "per_person": total // traveler_count if traveler_count > 0 else total,
    }


def generate_booking_number() -> str:
    """Generate unique booking number."""
    import random
    import string
    return "LBK-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_booking_state():
    """Initialize booking session state."""
    
    if "booking_step" not in st.session_state:
        st.session_state.booking_step = BookingStep.PACKAGE
    
    if "booking_data" not in st.session_state:
        st.session_state.booking_data = {
            "package_type": None,
            "departure_city": "Jakarta",
            "departure_date": None,
            "return_date": None,
            "travelers": [],
            "hotel_star": 4,
            "days_makkah": 5,
            "days_madinah": 4,
            "addons": [],
            "notes": "",
            "promo_code": "",
        }


def get_current_step() -> BookingStep:
    """Get current booking step."""
    return st.session_state.get("booking_step", BookingStep.PACKAGE)


def set_step(step: BookingStep):
    """Set current booking step."""
    st.session_state.booking_step = step


def next_step():
    """Move to next step."""
    steps = list(BookingStep)
    current = get_current_step()
    idx = steps.index(current)
    if idx < len(steps) - 1:
        set_step(steps[idx + 1])


def prev_step():
    """Move to previous step."""
    steps = list(BookingStep)
    current = get_current_step()
    idx = steps.index(current)
    if idx > 0:
        set_step(steps[idx - 1])


# =============================================================================
# RENDER COMPONENTS
# =============================================================================

def render_progress_bar():
    """Render booking progress indicator."""
    
    steps = [
        (BookingStep.PACKAGE, "📦 Paket"),
        (BookingStep.SCHEDULE, "📅 Jadwal"),
        (BookingStep.TRAVELERS, "👥 Jamaah"),
        (BookingStep.ADDONS, "🎁 Add-ons"),
        (BookingStep.REVIEW, "📋 Review"),
        (BookingStep.PAYMENT, "💳 Bayar"),
        (BookingStep.CONFIRMATION, "✅ Selesai"),
    ]
    
    current = get_current_step()
    current_idx = list(BookingStep).index(current)
    
    # Progress bar
    progress = (current_idx + 1) / len(steps)
    st.progress(progress)
    
    # Step indicators
    cols = st.columns(len(steps))
    for i, (step, label) in enumerate(steps):
        with cols[i]:
            if i < current_idx:
                st.markdown(f"✅ ~~{label}~~")
            elif i == current_idx:
                st.markdown(f"🔵 **{label}**")
            else:
                st.caption(f"⚪ {label}")


def render_price_summary():
    """Render real-time price summary in sidebar."""
    
    with st.sidebar:
        st.markdown("### 💰 Ringkasan Biaya")
        
        data = st.session_state.booking_data
        prices = calculate_total_price(data)
        
        travelers_count = max(len(data.get("travelers", [])), 1)
        
        with st.container(border=True):
            st.markdown(f"**👥 {travelers_count} Jamaah**")
            
            st.markdown("---")
            
            # Base
            if data.get("package_type"):
                package = next((p for p in PACKAGES if p.type.value == data["package_type"]), None)
                if package:
                    st.markdown(f"📦 {package.name}")
                    st.caption(f"{format_currency(prices['base'])}")
            
            # Hotel upgrade
            if prices.get("hotel_upgrade", 0) > 0:
                st.markdown(f"🏨 Upgrade Hotel")
                st.caption(f"+{format_currency(prices['hotel_upgrade'])}")
            
            # Add-ons
            if prices.get("addons", 0) > 0:
                st.markdown(f"🎁 Add-ons")
                st.caption(f"+{format_currency(prices['addons'])}")
            
            # Seasonal
            if prices.get("seasonal", 0) > 0:
                st.markdown(f"📅 Seasonal")
                st.caption(f"+{format_currency(prices['seasonal'])}")
            
            st.markdown("---")
            
            # Total
            st.markdown(f"### Total")
            st.markdown(f"## {format_currency(prices['total'])}")
            st.caption(f"{format_currency(prices['per_person'])} / orang")
        
        # Promo code
        promo = st.text_input("🎟️ Kode Promo", placeholder="Masukkan kode")
        if promo:
            if promo.upper() == "LABBAIK10":
                st.success("✅ Diskon 10% applied!")
            else:
                st.error("❌ Kode tidak valid")


def render_step_package():
    """Render package selection step."""
    
    st.markdown("## 📦 Pilih Paket Umrah")
    st.caption("Pilih paket yang sesuai dengan kebutuhan dan budget Anda")
    
    # Package comparison
    selected = st.session_state.booking_data.get("package_type")
    
    # Grid view
    for i in range(0, len(PACKAGES), 2):
        cols = st.columns(2)
        
        for j, col in enumerate(cols):
            if i + j < len(PACKAGES):
                package = PACKAGES[i + j]
                
                with col:
                    is_selected = selected == package.type.value
                    
                    with st.container(border=True):
                        # Header badges
                        badges = ""
                        if package.popular:
                            badges += "🔥 POPULER "
                        if package.best_value:
                            badges += "💎 BEST VALUE"
                        
                        if badges:
                            st.markdown(f"**{badges}**")
                        
                        # Package header
                        st.markdown(f"### {package.icon} {package.name}")
                        st.caption(package.description)
                        
                        # Price
                        st.markdown(f"### {format_currency(package.base_price)}")
                        st.caption("per orang")
                        
                        # Key features
                        st.markdown("---")
                        st.markdown(f"🏨 **Hotel:** {package.hotel_makkah}")
                        st.markdown(f"📍 **Jarak:** {package.distance_haram}")
                        st.markdown(f"🍽️ **Makan:** {package.meals}")
                        st.markdown(f"👨‍🏫 **Mutawif:** {package.mutawif}")
                        
                        # Expandable features
                        with st.expander("Lihat semua fitur"):
                            for feature in package.features:
                                st.markdown(f"- {feature}")
                        
                        # Select button
                        btn_type = "primary" if is_selected else "secondary"
                        btn_label = "✓ Terpilih" if is_selected else "Pilih Paket"
                        
                        if st.button(btn_label, key=f"pkg_{package.type.value}", type=btn_type, use_container_width=True):
                            st.session_state.booking_data["package_type"] = package.type.value
                            st.rerun()
    
    # Navigation
    st.divider()
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if selected:
            if st.button("Lanjut →", type="primary", use_container_width=True):
                next_step()
                st.rerun()
        else:
            st.warning("Pilih paket terlebih dahulu")


def render_step_schedule():
    """Render schedule selection step."""
    
    st.markdown("## 📅 Pilih Jadwal Perjalanan")
    
    data = st.session_state.booking_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🛫 Keberangkatan")
        
        departure_city = st.selectbox(
            "Kota Keberangkatan",
            ["Jakarta", "Surabaya", "Bandung", "Medan", "Makassar", "Semarang", "Yogyakarta", "Palembang", "Balikpapan", "Pekanbaru"],
            index=0
        )
        data["departure_city"] = departure_city
        
        departure_date = st.date_input(
            "Tanggal Berangkat",
            min_value=date.today() + timedelta(days=30),
            value=date.today() + timedelta(days=60)
        )
        data["departure_date"] = departure_date
        
        # Calendar highlight
        month = departure_date.month
        if month == 3 or month == 4:
            st.warning("⚠️ **Periode Ramadan** - Harga lebih tinggi, sangat ramai")
        elif month in [6, 7]:
            st.info("ℹ️ **Peak Season** - Musim liburan sekolah")
        elif month == 12:
            st.info("ℹ️ **Peak Season** - Liburan akhir tahun")
        else:
            st.success("✅ **Regular Season** - Harga normal")
    
    with col2:
        st.markdown("### 🛬 Kepulangan")
        
        duration = st.selectbox(
            "Durasi Trip",
            [9, 10, 12, 14, 21],
            format_func=lambda x: f"{x} hari / {x-1} malam",
            index=1
        )
        
        return_date = departure_date + timedelta(days=duration)
        data["return_date"] = return_date
        
        st.info(f"📅 **Pulang:** {return_date.strftime('%d %B %Y')}")
        
        # Duration breakdown
        st.markdown("### ⏱️ Pembagian Waktu")
        
        max_nights = duration - 1
        
        days_makkah = st.slider(
            "Malam di Makkah",
            min_value=3,
            max_value=max_nights - 2,
            value=min(5, max_nights - 3)
        )
        data["days_makkah"] = days_makkah
        
        days_madinah = max_nights - days_makkah
        data["days_madinah"] = days_madinah
        
        st.caption(f"🕋 {days_makkah} malam di Makkah")
        st.caption(f"🕌 {days_madinah} malam di Madinah")
    
    # Hotel selection
    st.markdown("---")
    st.markdown("### 🏨 Kategori Hotel")
    
    package_type = data.get("package_type")
    
    hotel_cols = st.columns(5)
    hotel_options = [
        (3, "⭐⭐⭐", "Standar", "300-500m dari Masjid"),
        (4, "⭐⭐⭐⭐", "Superior", "100-300m dari Masjid"),
        (5, "⭐⭐⭐⭐⭐", "Premium", "< 100m, view Ka'bah"),
    ]
    
    current_hotel = data.get("hotel_star", 4)
    
    for i, (star, icons, name, desc) in enumerate(hotel_options):
        with hotel_cols[i]:
            is_selected = current_hotel == star
            
            with st.container(border=True):
                st.markdown(f"### {icons}")
                st.markdown(f"**{name}**")
                st.caption(desc)
                
                upgrade = ""
                if star == 4:
                    upgrade = "+Rp 3 Juta"
                elif star == 5:
                    upgrade = "+Rp 8 Juta"
                
                if upgrade:
                    st.caption(upgrade)
                
                if st.button(
                    "✓" if is_selected else "Pilih",
                    key=f"hotel_{star}",
                    type="primary" if is_selected else "secondary",
                    use_container_width=True
                ):
                    data["hotel_star"] = star
                    st.rerun()
    
    # Navigation
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Kembali", use_container_width=True):
            prev_step()
            st.rerun()
    
    with col3:
        if st.button("Lanjut →", type="primary", use_container_width=True):
            next_step()
            st.rerun()


def render_step_travelers():
    """Render travelers data step."""
    
    st.markdown("## 👥 Data Jamaah")
    st.caption("Masukkan data sesuai paspor untuk semua jamaah")
    
    data = st.session_state.booking_data
    travelers = data.get("travelers", [])
    
    # Summary
    if travelers:
        st.success(f"✅ {len(travelers)} jamaah terdaftar")
    
    # Add traveler form
    with st.expander("➕ Tambah Jamaah Baru", expanded=not travelers):
        with st.form("add_traveler", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Nama Lengkap (sesuai paspor) *")
                passport_number = st.text_input("Nomor Paspor *")
                passport_expiry = st.date_input(
                    "Masa Berlaku Paspor *",
                    min_value=date.today() + timedelta(days=180),
                    value=date.today() + timedelta(days=365 * 2)
                )
                nationality = st.selectbox(
                    "Kewarganegaraan",
                    ["Indonesia", "Malaysia", "Singapura", "Lainnya"]
                )
            
            with col2:
                birth_date = st.date_input(
                    "Tanggal Lahir *",
                    max_value=date.today() - timedelta(days=365),
                    value=date.today() - timedelta(days=365 * 35)
                )
                gender = st.radio("Jenis Kelamin *", ["Laki-laki", "Perempuan"], horizontal=True)
                phone = st.text_input("Nomor HP (WhatsApp)")
                email = st.text_input("Email")
            
            # Additional options
            col1, col2 = st.columns(2)
            with col1:
                room_pref = st.selectbox(
                    "Preferensi Kamar",
                    ["Double (2 orang)", "Triple (3 orang)", "Quad (4 orang)"],
                    index=0
                )
            with col2:
                special_needs = st.text_input("Kebutuhan Khusus", placeholder="Kursi roda, vegetarian, dll.")
            
            is_primary = st.checkbox("Jamaah utama (contact person)")
            
            if st.form_submit_button("➕ Tambah Jamaah", type="primary", use_container_width=True):
                if name and passport_number:
                    new_traveler = {
                        "name": name,
                        "passport_number": passport_number,
                        "passport_expiry": passport_expiry.isoformat(),
                        "birth_date": birth_date.isoformat(),
                        "gender": "male" if gender == "Laki-laki" else "female",
                        "nationality": nationality,
                        "phone": phone,
                        "email": email,
                        "room_preference": room_pref,
                        "special_needs": special_needs,
                        "is_primary": is_primary,
                    }
                    travelers.append(new_traveler)
                    data["travelers"] = travelers
                    st.success(f"✅ {name} berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error("Nama dan nomor paspor wajib diisi")
    
    # List travelers
    if travelers:
        st.markdown("### 📋 Daftar Jamaah")
        
        for i, t in enumerate(travelers):
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
                
                with col1:
                    st.markdown(f"### {i+1}")
                    if t.get("is_primary"):
                        st.caption("👑 Utama")
                
                with col2:
                    st.markdown(f"**{t['name']}**")
                    st.caption(f"🛂 {t['passport_number']}")
                
                with col3:
                    gender_icon = "👨" if t['gender'] == 'male' else "👩"
                    st.caption(f"{gender_icon} {t.get('birth_date', 'N/A')}")
                    if t.get("special_needs"):
                        st.caption(f"⚠️ {t['special_needs']}")
                
                with col4:
                    if st.button("🗑️", key=f"del_{i}", help="Hapus jamaah"):
                        travelers.pop(i)
                        data["travelers"] = travelers
                        st.rerun()
    
    # Navigation
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Kembali", use_container_width=True):
            prev_step()
            st.rerun()
    
    with col3:
        if travelers:
            if st.button("Lanjut →", type="primary", use_container_width=True):
                next_step()
                st.rerun()
        else:
            st.warning("Tambahkan minimal 1 jamaah")


def render_step_addons():
    """Render add-ons selection step."""
    
    st.markdown("## 🎁 Pilih Add-ons")
    st.caption("Tambahkan layanan ekstra untuk pengalaman umrah yang lebih lengkap")
    
    data = st.session_state.booking_data
    selected_addons = data.get("addons", [])
    
    # Group by category
    categories = {
        "protection": ("🛡️ Perlindungan", [a for a in ADDONS if a.category == "protection"]),
        "comfort": ("✨ Kenyamanan", [a for a in ADDONS if a.category == "comfort"]),
        "experience": ("🌟 Pengalaman", [a for a in ADDONS if a.category == "experience"]),
        "utility": ("🔧 Utilitas", [a for a in ADDONS if a.category == "utility"]),
        "souvenir": ("🎁 Oleh-oleh", [a for a in ADDONS if a.category == "souvenir"]),
        "special": ("♿ Kebutuhan Khusus", [a for a in ADDONS if a.category == "special"]),
    }
    
    for cat_id, (cat_name, addons) in categories.items():
        if addons:
            st.markdown(f"### {cat_name}")
            
            cols = st.columns(3)
            for i, addon in enumerate(addons):
                with cols[i % 3]:
                    is_selected = addon.id in selected_addons
                    
                    with st.container(border=True):
                        # Popular badge
                        if addon.popular:
                            st.markdown("🔥 **POPULER**")
                        
                        st.markdown(f"### {addon.icon} {addon.name}")
                        st.caption(addon.description)
                        st.markdown(f"**{format_currency(addon.price)}**")
                        st.caption("per orang")
                        
                        if st.checkbox(
                            "Tambahkan" if not is_selected else "✓ Ditambahkan",
                            value=is_selected,
                            key=f"addon_{addon.id}"
                        ):
                            if addon.id not in selected_addons:
                                selected_addons.append(addon.id)
                        else:
                            if addon.id in selected_addons:
                                selected_addons.remove(addon.id)
            
            st.markdown("")
    
    data["addons"] = selected_addons
    
    # Summary
    if selected_addons:
        st.success(f"✅ {len(selected_addons)} add-ons dipilih")
    
    # Navigation
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Kembali", use_container_width=True):
            prev_step()
            st.rerun()
    
    with col3:
        if st.button("Lanjut →", type="primary", use_container_width=True):
            next_step()
            st.rerun()


def render_step_review():
    """Render booking review step."""
    
    st.markdown("## 📋 Review Booking")
    
    data = st.session_state.booking_data
    prices = calculate_total_price(data)
    
    # Package summary
    package = next((p for p in PACKAGES if p.type.value == data.get("package_type")), None)
    
    with st.container(border=True):
        st.markdown("### 📦 Paket")
        if package:
            st.markdown(f"## {package.icon} {package.name}")
            st.caption(package.description)
    
    # Schedule
    with st.container(border=True):
        st.markdown("### 📅 Jadwal")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Berangkat", data.get("departure_date", "N/A").strftime("%d %b %Y") if data.get("departure_date") else "N/A")
        with col2:
            st.metric("Pulang", data.get("return_date", "N/A").strftime("%d %b %Y") if data.get("return_date") else "N/A")
        with col3:
            if data.get("departure_date") and data.get("return_date"):
                days = (data["return_date"] - data["departure_date"]).days
                st.metric("Durasi", f"{days} hari")
        
        st.caption(f"📍 Dari: {data.get('departure_city', 'N/A')}")
        st.caption(f"🕋 {data.get('days_makkah', 0)} malam di Makkah | 🕌 {data.get('days_madinah', 0)} malam di Madinah")
    
    # Travelers
    travelers = data.get("travelers", [])
    with st.container(border=True):
        st.markdown("### 👥 Jamaah")
        for i, t in enumerate(travelers, 1):
            primary = " 👑" if t.get("is_primary") else ""
            st.markdown(f"{i}. **{t['name']}**{primary} - {t['passport_number']}")
        st.info(f"Total: {len(travelers)} jamaah")
    
    # Add-ons
    selected_addons = data.get("addons", [])
    if selected_addons:
        with st.container(border=True):
            st.markdown("### 🎁 Add-ons")
            for addon_id in selected_addons:
                addon = next((a for a in ADDONS if a.id == addon_id), None)
                if addon:
                    st.markdown(f"- {addon.icon} {addon.name} ({format_currency(addon.price)}/orang)")
    
    # Price breakdown
    with st.container(border=True):
        st.markdown("### 💰 Rincian Biaya")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"📦 Paket ({len(travelers)} orang)")
            if prices.get("hotel_upgrade", 0) > 0:
                st.markdown("🏨 Upgrade Hotel")
            if prices.get("addons", 0) > 0:
                st.markdown("🎁 Add-ons")
            if prices.get("seasonal", 0) > 0:
                st.markdown("📅 Seasonal Adjustment")
            st.markdown("---")
            st.markdown("**TOTAL**")
        
        with col2:
            st.markdown(f"{format_currency(prices['base'])}")
            if prices.get("hotel_upgrade", 0) > 0:
                st.markdown(f"+{format_currency(prices['hotel_upgrade'])}")
            if prices.get("addons", 0) > 0:
                st.markdown(f"+{format_currency(prices['addons'])}")
            if prices.get("seasonal", 0) > 0:
                st.markdown(f"+{format_currency(prices['seasonal'])}")
            st.markdown("---")
            st.markdown(f"**{format_currency(prices['total'])}**")
    
    # Terms
    st.markdown("### 📜 Syarat & Ketentuan")
    agree = st.checkbox("Saya telah membaca dan menyetujui syarat dan ketentuan yang berlaku")
    
    # Notes
    notes = st.text_area("📝 Catatan Tambahan (opsional)", placeholder="Permintaan khusus, alergi makanan, dll.")
    data["notes"] = notes
    
    # Navigation
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Kembali", use_container_width=True):
            prev_step()
            st.rerun()
    
    with col3:
        if agree:
            if st.button("Lanjut ke Pembayaran →", type="primary", use_container_width=True):
                next_step()
                st.rerun()
        else:
            st.warning("Setujui syarat dan ketentuan")


def render_step_payment():
    """Render payment step."""
    
    st.markdown("## 💳 Pembayaran")
    
    data = st.session_state.booking_data
    prices = calculate_total_price(data)
    total = prices["total"]
    
    # Payment options
    st.markdown("### 💵 Pilih Jenis Pembayaran")
    
    payment_type = st.radio(
        "Opsi pembayaran",
        ["DP 30%", "DP 50%", "Lunas 100%"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if payment_type == "DP 30%":
        amount = int(total * 0.3)
        remaining = total - amount
        st.info(f"Bayar sekarang: **{format_currency(amount)}** | Sisa: {format_currency(remaining)}")
    elif payment_type == "DP 50%":
        amount = int(total * 0.5)
        remaining = total - amount
        st.info(f"Bayar sekarang: **{format_currency(amount)}** | Sisa: {format_currency(remaining)}")
    else:
        amount = total
        remaining = 0
        st.success(f"Bayar lunas: **{format_currency(amount)}** | Hemat Rp 500.000!")
    
    st.markdown("---")
    
    # Payment method
    st.markdown("### 🏦 Metode Pembayaran")
    
    method = st.radio(
        "Pilih metode",
        ["💳 Transfer Bank", "📱 Virtual Account", "💰 E-Wallet", "💳 Kartu Kredit"],
        label_visibility="collapsed"
    )
    
    with st.container(border=True):
        if "Transfer" in method:
            st.markdown("""
            **Bank BCA**
            - No. Rekening: `123-456-7890`
            - Atas Nama: PT LABBAIK WISATA MANDIRI
            
            **Bank Mandiri**
            - No. Rekening: `098-765-4321`
            - Atas Nama: PT LABBAIK WISATA MANDIRI
            """)
        elif "Virtual" in method:
            st.markdown("Virtual Account akan digenerate setelah konfirmasi booking")
            st.markdown(f"**Total: {format_currency(amount)}**")
        elif "E-Wallet" in method:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.button("GoPay", use_container_width=True)
            with col2:
                st.button("OVO", use_container_width=True)
            with col3:
                st.button("DANA", use_container_width=True)
            with col4:
                st.button("ShopeePay", use_container_width=True)
        else:
            st.markdown("Pembayaran kartu kredit akan diarahkan ke payment gateway")
    
    # Upload bukti
    st.markdown("### 📤 Upload Bukti Pembayaran")
    uploaded = st.file_uploader(
        "Upload screenshot/foto bukti transfer",
        type=["jpg", "jpeg", "png", "pdf"],
        help="Format: JPG, PNG, atau PDF. Max 5MB"
    )
    
    if uploaded:
        st.success("✅ File berhasil diupload")
    
    # Navigation
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Kembali", use_container_width=True):
            prev_step()
            st.rerun()
    
    with col3:
        if uploaded or method != "💳 Transfer Bank":
            if st.button("Konfirmasi Pembayaran →", type="primary", use_container_width=True):
                next_step()
                st.rerun()
        else:
            st.warning("Upload bukti pembayaran")


def render_step_confirmation():
    """Render confirmation step."""
    
    st.balloons()
    
    booking_number = generate_booking_number()
    
    st.markdown("## ✅ Booking Berhasil!")
    
    with st.container(border=True):
        st.markdown("### 🎉 Alhamdulillah!")
        
        st.markdown(f"""
        Booking Umrah Anda telah berhasil dibuat.
        
        ### Nomor Booking
        ## `{booking_number}`
        
        Simpan nomor ini untuk referensi.
        """)
        
        st.success("📧 Email konfirmasi telah dikirim ke alamat email jamaah utama")
        st.info("📱 WhatsApp konfirmasi akan dikirim dalam 1x24 jam")
    
    # Next steps
    with st.container(border=True):
        st.markdown("### 📋 Langkah Selanjutnya")
        
        steps = [
            ("1️⃣", "Simpan nomor booking Anda"),
            ("2️⃣", "Cek email untuk detail lengkap"),
            ("3️⃣", "Tunggu konfirmasi dari tim kami (1x24 jam)"),
            ("4️⃣", "Siapkan dokumen yang diperlukan"),
            ("5️⃣", "Lunasi pembayaran sesuai jadwal"),
            ("6️⃣", "Ikuti briefing pra-keberangkatan"),
        ]
        
        for num, text in steps:
            st.markdown(f"{num} {text}")
    
    # Actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 Kembali ke Beranda", use_container_width=True):
            st.session_state.booking_step = BookingStep.PACKAGE
            st.session_state.booking_data = {}
            st.rerun()
    
    with col2:
        if st.button("📥 Download Konfirmasi", use_container_width=True):
            st.info("PDF konfirmasi akan segera tersedia")
    
    with col3:
        if st.button("📤 Share", use_container_width=True):
            st.info("Bagikan ke WhatsApp/sosmed")


# =============================================================================
# MAIN PAGE RENDERER
# =============================================================================

def render_booking_page():
    """Main booking page renderer."""

    # Track page view
    try:
        from services.analytics import track_page
        track_page("booking")
    except:
        pass
    
    # Initialize state
    init_booking_state()
    
    # Header
    st.markdown("# 🕋 Booking Umrah")
    st.caption("Pesan perjalanan umrah Anda dengan mudah dan aman")
    
    # Progress bar
    render_progress_bar()
    
    st.divider()
    
    # Price summary in sidebar
    if get_current_step() not in [BookingStep.PACKAGE, BookingStep.CONFIRMATION]:
        render_price_summary()
    
    # Render current step
    current = get_current_step()
    
    step_renderers = {
        BookingStep.PACKAGE: render_step_package,
        BookingStep.SCHEDULE: render_step_schedule,
        BookingStep.TRAVELERS: render_step_travelers,
        BookingStep.ADDONS: render_step_addons,
        BookingStep.REVIEW: render_step_review,
        BookingStep.PAYMENT: render_step_payment,
        BookingStep.CONFIRMATION: render_step_confirmation,
    }
    
    renderer = step_renderers.get(current)
    if renderer:
        renderer()
    
    # Footer
    if current != BookingStep.CONFIRMATION:
        st.divider()
        st.caption("🔒 Data Anda aman dan terenkripsi | 💬 Butuh bantuan? Chat kami 24/7")


# Export
__all__ = ["render_booking_page"]
