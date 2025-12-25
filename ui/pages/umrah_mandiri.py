"""
================================================================================
🕋 LABBAIK AI - UMRAH MANDIRI v7.1 COMPLETE
================================================================================
Lokasi: ui/pages/umrah_mandiri.py
Fitur: Official Resources, Live Crowd Map, HHR Train, Raudhah, Visa, Miqat, dll
================================================================================
"""

import streamlit as st
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional

# =============================================================================
# 🎨 STYLING
# =============================================================================

UMRAH_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');

.hero-mandiri {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
    padding: 1.5rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 1.5rem;
    border: 1px solid #d4af37;
}

.hero-mandiri h1 { color: #d4af37; margin-bottom: 0.25rem; }
.hero-mandiri .arabic { font-size: 2rem; font-family: 'Amiri', serif; color: #d4af37; }

.xp-bar-container {
    background: #2d2d2d;
    border-radius: 20px;
    height: 25px;
    overflow: hidden;
    position: relative;
    border: 1px solid #d4af37;
}

.xp-bar-fill {
    background: linear-gradient(90deg, #d4af37, #f4d03f, #d4af37);
    height: 100%;
    border-radius: 20px;
    transition: width 0.5s ease;
}

.xp-bar-text {
    position: absolute;
    width: 100%;
    text-align: center;
    line-height: 25px;
    color: white;
    font-weight: bold;
    font-size: 0.8rem;
}

.stat-card {
    background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%);
    border-radius: 15px;
    padding: 1rem;
    text-align: center;
    border: 1px solid #444;
    color: white;
}

.stat-card.active { border-color: #d4af37; }
.stat-card h3 { color: #d4af37; margin: 0; font-size: 1.1rem; }

.doa-arabic {
    font-size: 1.6rem;
    text-align: right;
    font-family: 'Amiri', serif;
    background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-right: 4px solid #d4af37;
    color: #d4af37;
    direction: rtl;
}

.countdown-box {
    background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
    color: #d4af37;
    font-size: 2rem;
    font-weight: bold;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    display: inline-block;
    border: 1px solid #d4af37;
    min-width: 60px;
    text-align: center;
}

.achievement-badge {
    background: linear-gradient(145deg, #2d2d2d 0%, #1a1a1a 100%);
    border-radius: 12px;
    padding: 0.75rem;
    text-align: center;
    border: 1px solid #d4af37;
    color: white;
}

.achievement-badge.locked { opacity: 0.5; border-color: #444; }
</style>
"""

# =============================================================================
# 📱 OFFICIAL RESOURCES DATA
# =============================================================================

OFFICIAL_RESOURCES = {
    "nusuk": {
        "name": "NUSUK - Platform Resmi",
        "url": "https://www.nusuk.sa",
        "icon": "🏛️",
        "desc": "Platform resmi Kementerian Haji & Umrah Saudi Arabia",
        "features": ["E-Visa Umrah", "Paket Umrah", "Permit Raudhah", "Info & Panduan"],
        "required": True,
        "android": "https://play.google.com/store/apps/details?id=sa.gov.moh.nusuk",
        "ios": "https://apps.apple.com/app/nusuk/id1521968498"
    },
    "prayers_map": {
        "name": "Peta Keramaian Masjid Nabawi",
        "url": "https://eserv.wmn.gov.sa/e-services/prayers_map/?lang=en",
        "icon": "🗺️",
        "desc": "Real-time crowd density dari General Presidency of Harameen",
        "features": ["Live crowd level", "Jadwal sholat Madinah", "Area mapping"],
        "required": False,
    },
    "hhr": {
        "name": "Haramain High-Speed Railway",
        "url": "https://sar.hhr.sa/",
        "icon": "🚄",
        "desc": "Kereta cepat 300km/jam Makkah-Jeddah-Madinah",
        "features": ["Booking tiket online", "Jadwal keberangkatan", "2.5 jam Makkah-Madinah"],
        "required": True,
    },
    "careem": {
        "name": "Careem - Taxi App",
        "url": "https://www.careem.com/",
        "icon": "🚗",
        "desc": "Aplikasi taxi terpopuler di Saudi Arabia",
        "features": ["Ride hailing dalam kota", "Harga transparan", "Cash/Card"],
        "required": True,
        "android": "https://play.google.com/store/apps/details?id=com.careem.acma",
        "ios": "https://apps.apple.com/app/careem/id592978487"
    },
    "simpu": {
        "name": "SISKOPATUH KEMENAG",
        "url": "https://simpu.kemenag.go.id/",
        "icon": "🇮🇩",
        "desc": "Verifikasi travel agent resmi terdaftar Kemenag RI",
        "features": ["Cek legalitas PPIU", "Database resmi", "Hotline 1500-363"],
        "required": True,
    }
}

HHR_ROUTES = [
    {"from": "Makkah", "to": "Madinah", "duration": "2j 30m", "economy": 250, "business": 375},
    {"from": "Makkah", "to": "Jeddah", "duration": "45m", "economy": 75, "business": 115},
    {"from": "Jeddah Airport", "to": "Makkah", "duration": "35m", "economy": 75, "business": 115},
    {"from": "Jeddah", "to": "Madinah", "duration": "1j 50m", "economy": 200, "business": 300},
]

ESSENTIAL_APPS = [
    {"name": "NUSUK", "icon": "🕋", "purpose": "Visa, permits, booking", "required": True},
    {"name": "Google Maps", "icon": "🗺️", "purpose": "Navigasi (download offline!)", "required": True},
    {"name": "Careem", "icon": "🚗", "purpose": "Taxi dalam kota", "required": True},
    {"name": "Uber", "icon": "🚙", "purpose": "Alternatif taxi", "required": False},
    {"name": "WhatsApp", "icon": "💬", "purpose": "Komunikasi", "required": True},
    {"name": "Tawakkalna", "icon": "📲", "purpose": "Digital ID Saudi (optional)", "required": False},
]

RAUDHAH_INFO = {
    "hadith": "Apa yang ada di antara rumahku dan mimbarku adalah taman dari taman-taman surga.",
    "source": "HR. Bukhari & Muslim",
    "location": "Area berkarpet hijau di Masjid Nabawi, Madinah",
    "size": "22m x 15m (~330 m²)",
    "booking": "Via aplikasi NUSUK",
    "tips": [
        "📱 Download dan daftar di aplikasi NUSUK",
        "📍 Aktifkan GPS saat di dekat Masjid Nabawi",
        "⏰ Slot baru muncul setiap Jumat untuk 1 minggu ke depan",
        "🕐 Cek app setiap jam atau setengah jam",
        "⚡ Slot sangat cepat habis!",
        "1️⃣ Hanya 1 permit per orang per bulan",
        "🚪 Masuk via Gate 37 (wanita)",
        "⏱️ Datang 30-45 menit sebelum slot"
    ]
}

EMERGENCY_CONTACTS = {
    "saudi": [
        {"name": "Police", "phone": "999", "icon": "👮"},
        {"name": "Ambulance", "phone": "997", "icon": "🚑"},
        {"name": "Fire", "phone": "998", "icon": "🚒"},
    ],
    "indonesia": [
        {"name": "KBRI Riyadh", "phone": "+966-11-488-2800", "icon": "🇮🇩"},
        {"name": "KJRI Jeddah", "phone": "+966-12-667-0826", "icon": "🇮🇩"},
        {"name": "Hotline KEMENAG", "phone": "1500-363", "icon": "📞"},
    ]
}

# =============================================================================
# 🎮 GAMIFICATION DATA
# =============================================================================

LEVELS = [
    {"level": 1, "name": "Niat Suci", "min_xp": 0, "icon": "🌱"},
    {"level": 2, "name": "Pencari Ilmu", "min_xp": 100, "icon": "📚"},
    {"level": 3, "name": "Perencana Cermat", "min_xp": 300, "icon": "📝"},
    {"level": 4, "name": "Penabung Setia", "min_xp": 600, "icon": "💰"},
    {"level": 5, "name": "Siap Berangkat", "min_xp": 1000, "icon": "✈️"},
    {"level": 6, "name": "Muhrim Sejati", "min_xp": 1500, "icon": "🧕"},
    {"level": 7, "name": "Thawaf Champion", "min_xp": 2100, "icon": "🕋"},
    {"level": 8, "name": "Sa'i Warrior", "min_xp": 2800, "icon": "🏃"},
    {"level": 9, "name": "Jamaah Teladan", "min_xp": 3600, "icon": "⭐"},
    {"level": 10, "name": "Haji Mabrur", "min_xp": 5000, "icon": "👑"},
]

ACHIEVEMENTS = [
    {"id": "first_step", "name": "Langkah Pertama", "icon": "👣", "desc": "Mulai journey Umrah Mandiri", "xp": 50},
    {"id": "resources_explorer", "name": "Resources Explorer", "icon": "🔗", "desc": "Jelajahi Official Resources", "xp": 50},
    {"id": "visa_checked", "name": "Visa Expert", "icon": "🛂", "desc": "Cek kelayakan visa", "xp": 75},
    {"id": "docs_ready", "name": "Dokumen Lengkap", "icon": "📄", "desc": "100% dokumen siap", "xp": 100},
    {"id": "miqat_master", "name": "Miqat Master", "icon": "📍", "desc": "Pahami miqat & ihram", "xp": 50},
    {"id": "safe_travel", "name": "Safe Traveler", "icon": "🛡️", "desc": "Verifikasi PPIU", "xp": 75},
    {"id": "budget_set", "name": "Budget Planner", "icon": "💰", "desc": "Hitung estimasi biaya", "xp": 50},
    {"id": "manasik_complete", "name": "Manasik Pro", "icon": "🕌", "desc": "Selesaikan 8 langkah manasik", "xp": 150},
    {"id": "pillar_admin", "name": "Admin Master", "icon": "📋", "desc": "Selesaikan pilar Administrasi", "xp": 100},
    {"id": "pillar_logistik", "name": "Logistik Pro", "icon": "🏨", "desc": "Selesaikan pilar Logistik", "xp": 100},
    {"id": "pillar_eksekusi", "name": "Eksekusi Ready", "icon": "🚀", "desc": "Selesaikan pilar Eksekusi", "xp": 100},
]

# =============================================================================
# 📿 MANASIK & PILLAR DATA
# =============================================================================

MANASIK_STEPS = [
    {"step": 1, "title": "Niat & Persiapan", "icon": "🎯", 
     "dua": "اَللّٰهُمَّ إِنِّيْ أُرِيْدُ الْعُمْرَةَ فَيَسِّرْهَا لِيْ",
     "latin": "Allahumma innii uridul 'umrata fayassirhaa lii",
     "arti": "Ya Allah, aku ingin umrah, maka mudahkanlah bagiku"},
    {"step": 2, "title": "Miqat & Ihram", "icon": "🧕", 
     "dua": "لَبَّيْكَ اللّٰهُمَّ عُمْرَةً",
     "latin": "Labbaik Allahumma 'umratan",
     "arti": "Aku memenuhi panggilan-Mu ya Allah untuk umrah"},
    {"step": 3, "title": "Talbiyah", "icon": "🎵", 
     "dua": "لَبَّيْكَ اللّٰهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيْكَ لَكَ لَبَّيْكَ",
     "latin": "Labbaik Allahumma labbaik, labbaik laa syariika laka labbaik",
     "arti": "Aku memenuhi panggilan-Mu ya Allah, tiada sekutu bagi-Mu"},
    {"step": 4, "title": "Thawaf (7 Putaran)", "icon": "🕋", 
     "dua": "بِسْمِ اللهِ وَاللهُ أَكْبَرُ",
     "latin": "Bismillahi wallahu akbar",
     "arti": "Dengan nama Allah, Allah Maha Besar"},
    {"step": 5, "title": "Sholat di Maqam Ibrahim", "icon": "🙏", 
     "dua": "وَاتَّخِذُوا مِنْ مَقَامِ إِبْرَاهِيمَ مُصَلًّى",
     "latin": "Wattakhidzu min maqami ibrahim mushalla",
     "arti": "Dan jadikanlah maqam Ibrahim sebagai tempat sholat"},
    {"step": 6, "title": "Minum Air Zamzam", "icon": "💧", 
     "dua": "اَللّٰهُمَّ إِنِّيْ أَسْأَلُكَ عِلْمًا نَافِعًا وَرِزْقًا وَاسِعًا وَشِفَاءً مِنْ كُلِّ دَاءٍ",
     "latin": "Allahumma inni as'aluka 'ilman naafi'an wa rizqan waasi'an wa syifaa'an min kulli daa'",
     "arti": "Ya Allah, aku memohon ilmu yang bermanfaat, rezeki yang luas, dan kesembuhan dari segala penyakit"},
    {"step": 7, "title": "Sa'i (Safa-Marwa)", "icon": "🏃", 
     "dua": "إِنَّ الصَّفَا وَالْمَرْوَةَ مِنْ شَعَائِرِ اللهِ",
     "latin": "Innash shafa wal marwata min sya'a'irillah",
     "arti": "Sesungguhnya Safa dan Marwa adalah syiar Allah"},
    {"step": 8, "title": "Tahallul (Cukur/Potong)", "icon": "✂️", 
     "dua": "اَلْحَمْدُ لِلّٰهِ الَّذِيْ قَضٰى عَنَّا نُسُكَنَا",
     "latin": "Alhamdulillahilladzi qadha 'anna nusukana",
     "arti": "Segala puji bagi Allah yang telah menyempurnakan ibadah kami"},
]

PILLAR_DATA = {
    "administrasi": {
        "title": "Administrasi", "icon": "📋", "color": "#3498db",
        "tasks": [
            {"id": "passport", "name": "Paspor aktif >6 bulan", "xp": 50},
            {"id": "foto", "name": "Pas foto 4x6 (latar putih)", "xp": 20},
            {"id": "kk", "name": "Kartu Keluarga", "xp": 20},
            {"id": "ktp", "name": "KTP", "xp": 20},
            {"id": "vaccine", "name": "Vaksin Meningitis", "xp": 40},
            {"id": "ticket", "name": "Tiket Pesawat PP", "xp": 50},
        ]
    },
    "logistik": {
        "title": "Logistik", "icon": "🏨", "color": "#2ecc71",
        "tasks": [
            {"id": "visa", "name": "Visa Umrah/Tourist", "xp": 60},
            {"id": "hotel_makkah", "name": "Hotel Makkah", "xp": 50},
            {"id": "hotel_madinah", "name": "Hotel Madinah", "xp": 50},
            {"id": "nusuk", "name": "Daftar akun NUSUK", "xp": 30},
            {"id": "simcard", "name": "SIM Card Saudi", "xp": 20},
        ]
    },
    "eksekusi": {
        "title": "Eksekusi", "icon": "🚀", "color": "#e74c3c",
        "tasks": [
            {"id": "apps", "name": "Download apps (Careem, Maps)", "xp": 30},
            {"id": "offline_maps", "name": "Google Maps offline Makkah/Madinah", "xp": 30},
            {"id": "riyal", "name": "Tukar uang ke SAR", "xp": 30},
            {"id": "packing", "name": "Packing list lengkap", "xp": 30},
            {"id": "emergency", "name": "Simpan nomor darurat", "xp": 20},
        ]
    }
}

MIQAT_DATA = {
    "jeddah_direct": {
        "name": "Yalamlam (As-Sa'diyyah)", 
        "timing": "Di pesawat, ~1 jam sebelum landing Jeddah", 
        "tips": [
            "✈️ Pakai ihram sebelum boarding LEBIH AMAN",
            "📢 Pilot biasanya announce saat melewati miqat",
            "🧕 Wanita: pakaian biasa, niat saja"
        ]
    },
    "madinah_first": {
        "name": "Dzulhulaifah (Bir Ali)", 
        "timing": "Di Madinah, sebelum berangkat ke Makkah", 
        "tips": [
            "🕌 Ada masjid miqat dengan fasilitas lengkap",
            "🚿 Kamar mandi & tempat ganti tersedia",
            "⏰ Miqat terjauh dari Makkah, paling mudah untuk pemula"
        ]
    },
}

E_TOURIST_ELIGIBLE = [
    "United States", "United Kingdom", "Canada", "Australia", 
    "Germany", "France", "Japan", "South Korea", "Singapore", 
    "Malaysia", "Brunei", "New Zealand", "Switzerland", "Netherlands"
]

# =============================================================================
# 🔧 SESSION STATE FUNCTIONS
# =============================================================================

def init_umrah_mandiri_state():
    """Initialize session state for Umrah Mandiri."""
    defaults = {
        "um_xp": 0,
        "um_level": 1,
        "um_achievements": ["first_step"],
        "um_tasks": {"administrasi": [], "logistik": [], "eksekusi": []},
        "um_departure_date": None,
        "um_duration": 9,
        "um_manasik_step": 0,
        "um_manasik_completed": [],
        "um_savings": {"target": 25000000, "current": 0},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def add_xp(amount: int, reason: str = ""):
    """Add XP and check for level up."""
    st.session_state.um_xp = st.session_state.get("um_xp", 0) + amount
    
    # Check level up
    for lv in reversed(LEVELS):
        if st.session_state.um_xp >= lv["min_xp"]:
            if st.session_state.um_level < lv["level"]:
                st.session_state.um_level = lv["level"]
                st.balloons()
                st.toast(f"🎉 Level Up! {lv['icon']} {lv['name']}")
            break
    
    if reason:
        st.toast(f"+{amount} XP: {reason}")

def unlock_achievement(aid: str):
    """Unlock an achievement."""
    if aid not in st.session_state.um_achievements:
        ach = next((a for a in ACHIEVEMENTS if a["id"] == aid), None)
        if ach:
            st.session_state.um_achievements.append(aid)
            add_xp(ach["xp"], f"🏆 {ach['name']}")

def get_current_level() -> dict:
    """Get current level info."""
    for lv in reversed(LEVELS):
        if st.session_state.um_xp >= lv["min_xp"]:
            return lv
    return LEVELS[0]

# =============================================================================
# 🎨 RENDER COMPONENTS
# =============================================================================

def render_hero():
    """Render hero section."""
    st.markdown(UMRAH_CSS, unsafe_allow_html=True)
    
    level = get_current_level()
    st.markdown(f"""
    <div class="hero-mandiri">
        <div class="arabic">لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ</div>
        <h1>🧭 Umrah Mandiri</h1>
        <p style="color:#888;">Panduan Lengkap DIY Umrah + Official Resources</p>
        <p style="color:#d4af37;margin-top:0.5rem;">{level['icon']} Level {level['level']}: {level['name']}</p>
    </div>
    """, unsafe_allow_html=True)

def render_stats_cards():
    """Render quick stats cards."""
    cols = st.columns(4)
    
    # Persiapan progress
    total_tasks = sum(len(p["tasks"]) for p in PILLAR_DATA.values())
    done_tasks = sum(len(st.session_state.um_tasks.get(k, [])) for k in PILLAR_DATA.keys())
    
    with cols[0]:
        pct = int(done_tasks / total_tasks * 100) if total_tasks > 0 else 0
        st.markdown(f"""
        <div class="stat-card {'active' if pct > 0 else ''}">
            <div style="font-size:1.5rem;">📋</div>
            <h3>Persiapan</h3>
            <div style="background:#333;border-radius:10px;height:8px;margin:0.5rem 0;">
                <div style="background:#d4af37;width:{pct}%;height:100%;border-radius:10px;"></div>
            </div>
            <small>{done_tasks}/{total_tasks} ({pct}%)</small>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        manasik_done = len(st.session_state.um_manasik_completed)
        st.markdown(f"""
        <div class="stat-card {'active' if manasik_done > 0 else ''}">
            <div style="font-size:1.5rem;">🕌</div>
            <h3>Manasik</h3>
            <div style="background:#333;border-radius:10px;height:8px;margin:0.5rem 0;">
                <div style="background:#d4af37;width:{manasik_done/8*100}%;height:100%;border-radius:10px;"></div>
            </div>
            <small>{manasik_done}/8 langkah</small>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        savings = st.session_state.um_savings
        pct_save = int(savings["current"] / savings["target"] * 100) if savings["target"] > 0 else 0
        st.markdown(f"""
        <div class="stat-card {'active' if savings['current'] > 0 else ''}">
            <div style="font-size:1.5rem;">💰</div>
            <h3>Tabungan</h3>
            <div style="background:#333;border-radius:10px;height:8px;margin:0.5rem 0;">
                <div style="background:#d4af37;width:{min(pct_save,100)}%;height:100%;border-radius:10px;"></div>
            </div>
            <small>Rp {savings['current']:,}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        if st.session_state.um_departure_date:
            days = (st.session_state.um_departure_date - date.today()).days
            days_text = f"{days} hari" if days > 0 else "Sudah lewat!"
        else:
            days_text = "Set tanggal"
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size:1.5rem;">⏰</div>
            <h3>Countdown</h3>
            <small style="color:#d4af37;font-size:1rem;">{days_text}</small>
        </div>
        """, unsafe_allow_html=True)

def render_xp_bar():
    """Render XP progress bar."""
    curr = get_current_level()
    nxt = next((lv for lv in LEVELS if lv["level"] > curr["level"]), None)
    
    if nxt:
        prog = (st.session_state.um_xp - curr["min_xp"]) / (nxt["min_xp"] - curr["min_xp"])
        xp_text = f"{st.session_state.um_xp} / {nxt['min_xp']} XP"
    else:
        prog = 1.0
        xp_text = f"{st.session_state.um_xp} XP (MAX)"
    
    st.markdown(f"""
    <div class="xp-bar-container">
        <div class="xp-bar-fill" style="width:{min(prog,1)*100}%;"></div>
        <div class="xp-bar-text">{curr['icon']} {curr['name']} — {xp_text}</div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# 📱 TAB: OFFICIAL RESOURCES (NEW!)
# =============================================================================

def render_tab_resources():
    """Render Official Resources tab - NEW FEATURE!"""
    st.markdown("## 📱 Official Resources & Live Services")
    st.info("🔗 Kumpulan link resmi Saudi & Indonesia untuk Umrah Mandiri")
    
    subtabs = st.tabs(["🏛️ Platform", "📱 Apps", "🚄 Kereta", "💚 Raudhah", "🗺️ Live Map", "🆘 Darurat"])
    
    # --- Platform Resmi ---
    with subtabs[0]:
        st.markdown("### 🏛️ Platform Resmi")
        for key, res in OFFICIAL_RESOURCES.items():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    badge = "🔴 **WAJIB**" if res.get("required") else ""
                    st.markdown(f"### {res['icon']} {res['name']} {badge}")
                    st.caption(res["desc"])
                    for f in res.get("features", []):
                        st.write(f"• {f}")
                with col2:
                    st.link_button("🔗 Buka", res["url"], use_container_width=True)
                    if res.get("android"):
                        st.link_button("Android", res["android"], use_container_width=True)
        
        # Unlock achievement
        if "resources_explorer" not in st.session_state.um_achievements:
            unlock_achievement("resources_explorer")
    
    # --- Essential Apps ---
    with subtabs[1]:
        st.markdown("### 📱 Aplikasi Wajib Download")
        st.warning("⚠️ **Download SEMUA sebelum berangkat!** WiFi di Saudi tidak selalu stabil.")
        
        cols = st.columns(3)
        for i, app in enumerate(ESSENTIAL_APPS):
            with cols[i % 3]:
                with st.container(border=True):
                    badge = "🔴" if app["required"] else "🟡"
                    st.markdown(f"<div style='text-align:center;font-size:2rem;'>{app['icon']}</div>", unsafe_allow_html=True)
                    st.markdown(f"**{app['name']}** {badge}")
                    st.caption(app["purpose"])
        
        st.divider()
        st.markdown("### ✅ Checklist Download")
        for app in ESSENTIAL_APPS:
            st.checkbox(f"{app['icon']} {app['name']} - {app['purpose']}", key=f"app_check_{app['name']}")
    
    # --- Haramain Train ---
    with subtabs[2]:
        st.markdown("### 🚄 Haramain High-Speed Railway")
        st.success("**Kereta tercepat Timur Tengah!** 300 km/jam, Makkah-Madinah hanya 2.5 jam")
        
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("🎫 Booking Tiket Resmi", "https://sar.hhr.sa/", use_container_width=True, type="primary")
        with col2:
            st.link_button("📅 Lihat Jadwal", "https://sar.hhr.sa/timetable", use_container_width=True)
        
        st.divider()
        st.markdown("#### 🛤️ Rute & Harga")
        
        for route in HHR_ROUTES:
            col1, col2, col3, col4 = st.columns([2.5, 1, 1, 1])
            with col1:
                st.markdown(f"**{route['from']} → {route['to']}**")
            with col2:
                st.caption(f"⏱️ {route['duration']}")
            with col3:
                st.write(f"💺 SAR {route['economy']}")
            with col4:
                st.write(f"🎩 SAR {route['business']}")
        
        st.divider()
        st.markdown("#### 💡 Tips Naik HHR")
        tips = [
            "📅 Book 1-2 minggu sebelumnya, terutama saat Ramadan",
            "🧳 Bagasi max 25kg + 1 hand carry",
            "⏰ Datang 30 menit sebelum keberangkatan",
            "🕌 Ada musholla & kafetaria di kereta",
            "📱 WiFi tersedia di kereta & stasiun",
            "🎫 E-ticket valid, tidak perlu print"
        ]
        for tip in tips:
            st.write(tip)
    
    # --- Raudhah Booking ---
    with subtabs[3]:
        st.markdown("### 💚 Panduan Booking Raudhah")
        
        st.success(f"""
        **Hadits:**  
        *"{RAUDHAH_INFO['hadith']}"*  
        — {RAUDHAH_INFO['source']}
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"📍 **Lokasi:** {RAUDHAH_INFO['location']}")
            st.write(f"📐 **Ukuran:** {RAUDHAH_INFO['size']}")
        with col2:
            st.write(f"📱 **Booking:** {RAUDHAH_INFO['booking']}")
        
        st.divider()
        st.markdown("#### 📱 Langkah Booking:")
        for i, tip in enumerate(RAUDHAH_INFO["tips"], 1):
            st.write(f"{i}. {tip}")
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📱 NUSUK (Android)", "https://play.google.com/store/apps/details?id=sa.gov.moh.nusuk", use_container_width=True, type="primary")
        with col2:
            st.link_button("📱 NUSUK (iOS)", "https://apps.apple.com/app/nusuk/id1521968498", use_container_width=True, type="primary")
    
    # --- Live Crowd Map ---
    with subtabs[4]:
        st.markdown("### 🗺️ Peta Keramaian Real-time Masjid Nabawi")
        
        st.info("""
        **General Presidency of Harameen** menyediakan peta keramaian real-time 
        untuk membantu jamaah merencanakan waktu kunjungan!
        """)
        
        st.link_button(
            "🗺️ BUKA PETA JAMAAH MASJID NABAWI (LIVE)", 
            "https://eserv.wmn.gov.sa/e-services/prayers_map/?lang=en",
            use_container_width=True,
            type="primary"
        )
        
        st.divider()
        st.markdown("#### 🚦 Arti Warna:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("🟢 **Available**\nArea kosong, waktu terbaik!")
        with col2:
            st.warning("🟡 **Almost Busy**\nMulai ramai")
        with col3:
            st.error("🔴 **Busy**\nSangat padat, hindari")
        
        st.divider()
        st.markdown("#### ⏰ Prediksi Waktu Terbaik:")
        predictions = [
            ("00:00 - 03:00", "🟢 Sepi", True),
            ("03:00 - 06:00", "🟡 Sedang", False),
            ("06:00 - 09:00", "🟠 Ramai", False),
            ("12:00 - 15:00", "🔴 Sangat Ramai", False),
            ("18:00 - 21:00", "🔴 Sangat Ramai", False),
            ("21:00 - 00:00", "🟡 Sedang", False),
        ]
        cols = st.columns(3)
        for i, (time, level, best) in enumerate(predictions):
            with cols[i % 3]:
                if best:
                    st.success(f"**{time}**\n{level} ✅")
                else:
                    st.info(f"**{time}**\n{level}")
    
    # --- Emergency Contacts ---
    with subtabs[5]:
        st.markdown("### 🆘 Kontak Darurat")
        st.error("⚠️ **Simpan nomor-nomor ini di HP Anda SEBELUM berangkat!**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🇸🇦 Saudi Arabia")
            for c in EMERGENCY_CONTACTS["saudi"]:
                st.markdown(f"{c['icon']} **{c['name']}:** `{c['phone']}`")
        
        with col2:
            st.markdown("#### 🇮🇩 Indonesia")
            for c in EMERGENCY_CONTACTS["indonesia"]:
                st.markdown(f"{c['icon']} **{c['name']}:** `{c['phone']}`")
        
        st.divider()
        st.markdown("#### 💾 Quick Copy")
        st.code("""
EMERGENCY SAUDI:
- Police: 999
- Ambulance: 997
- Fire: 998

INDONESIA:
- KBRI Riyadh: +966-11-488-2800
- KJRI Jeddah: +966-12-667-0826
- KEMENAG: 1500-363
        """, language="text")

# =============================================================================
# 📅 TAB: COUNTDOWN
# =============================================================================

def render_tab_countdown():
    """Render Countdown tab."""
    st.markdown("## ⏰ Countdown to Baitullah")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        dep_date = st.date_input(
            "Tanggal Keberangkatan",
            value=st.session_state.um_departure_date or (date.today() + timedelta(days=90)),
            min_value=date.today()
        )
        st.session_state.um_departure_date = dep_date
        
        duration = st.slider("Durasi (hari)", 7, 21, st.session_state.um_duration)
        st.session_state.um_duration = duration
        
        return_date = dep_date + timedelta(days=duration)
        st.info(f"📅 Pulang: **{return_date.strftime('%d %B %Y')}**")
    
    with col2:
        days_left = (dep_date - date.today()).days
        
        if days_left > 0:
            months = days_left // 30
            weeks = (days_left % 30) // 7
            days = days_left % 7
            
            st.markdown(f"""
            <div style="text-align:center;">
                <div class="countdown-box">{months}</div>
                <div class="countdown-box">{weeks}</div>
                <div class="countdown-box">{days}</div>
                <div style="display:flex;justify-content:center;gap:2rem;margin-top:0.5rem;color:#888;">
                    <span>BULAN</span>
                    <span>MINGGU</span>
                    <span>HARI</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("🕋 Selamat menunaikan ibadah Umrah!")

# =============================================================================
# 🏛️ TAB: 3 PILAR
# =============================================================================

def render_tab_pillars():
    """Render 3 Pillars tab."""
    st.markdown("## 🏛️ 3 Pilar Persiapan Umrah")
    
    for pillar_id, pillar in PILLAR_DATA.items():
        with st.expander(f"{pillar['icon']} {pillar['title']}", expanded=True):
            done_count = len(st.session_state.um_tasks.get(pillar_id, []))
            total = len(pillar["tasks"])
            pct = int(done_count / total * 100) if total > 0 else 0
            
            st.progress(pct / 100, text=f"{done_count}/{total} selesai ({pct}%)")
            
            for task in pillar["tasks"]:
                done = task["id"] in st.session_state.um_tasks.get(pillar_id, [])
                if st.checkbox(f"{task['name']} (+{task['xp']} XP)", value=done, key=f"task_{pillar_id}_{task['id']}"):
                    if task["id"] not in st.session_state.um_tasks[pillar_id]:
                        st.session_state.um_tasks[pillar_id].append(task["id"])
                        add_xp(task["xp"], task["name"])
                        
                        # Check pillar completion
                        if len(st.session_state.um_tasks[pillar_id]) == len(pillar["tasks"]):
                            unlock_achievement(f"pillar_{pillar_id}")
                else:
                    if task["id"] in st.session_state.um_tasks.get(pillar_id, []):
                        st.session_state.um_tasks[pillar_id].remove(task["id"])

# =============================================================================
# 📿 TAB: MANASIK
# =============================================================================

def render_tab_manasik():
    """Render Virtual Manasik tab."""
    st.markdown("## 📿 Virtual Manasik Umrah")
    
    # Progress indicator
    completed = len(st.session_state.um_manasik_completed)
    st.progress(completed / 8, text=f"Progress: {completed}/8 langkah")
    
    # Step selector
    cols = st.columns(8)
    for i, step in enumerate(MANASIK_STEPS):
        with cols[i]:
            is_done = i in st.session_state.um_manasik_completed
            is_current = i == st.session_state.um_manasik_step
            
            btn_type = "primary" if is_current else "secondary"
            icon = "✅" if is_done else step["icon"]
            
            if st.button(icon, key=f"step_btn_{i}", type=btn_type, use_container_width=True):
                st.session_state.um_manasik_step = i
                st.rerun()
    
    st.divider()
    
    # Current step content
    step = MANASIK_STEPS[st.session_state.um_manasik_step]
    
    st.markdown(f"### {step['icon']} Langkah {step['step']}: {step['title']}")
    
    # Arabic dua
    st.markdown(f"<div class='doa-arabic'>{step['dua']}</div>", unsafe_allow_html=True)
    
    # Latin & meaning
    st.markdown(f"**Latin:** *{step['latin']}*")
    st.markdown(f"**Arti:** {step['arti']}")
    
    st.divider()
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.um_manasik_step > 0:
            if st.button("⬅️ Sebelumnya", use_container_width=True):
                st.session_state.um_manasik_step -= 1
                st.rerun()
    
    with col2:
        is_completed = st.session_state.um_manasik_step in st.session_state.um_manasik_completed
        if not is_completed:
            if st.button("✅ Tandai Selesai", use_container_width=True, type="primary"):
                st.session_state.um_manasik_completed.append(st.session_state.um_manasik_step)
                add_xp(25, f"Manasik: {step['title']}")
                
                # Check completion
                if len(st.session_state.um_manasik_completed) == 8:
                    unlock_achievement("manasik_complete")
                st.rerun()
        else:
            st.success("✅ Sudah selesai!")
    
    with col3:
        if st.session_state.um_manasik_step < 7:
            if st.button("Selanjutnya ➡️", use_container_width=True):
                st.session_state.um_manasik_step += 1
                st.rerun()

# =============================================================================
# 💰 TAB: BUDGET
# =============================================================================

def render_tab_budget():
    """Render Budget Optimizer tab."""
    st.markdown("## 💰 Budget Optimizer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        budget = st.number_input("Total Budget (Rp)", 
            min_value=10_000_000, 
            max_value=100_000_000, 
            value=25_000_000, 
            step=1_000_000,
            format="%d"
        )
        
        duration = st.slider("Durasi Perjalanan (hari)", 7, 21, 9)
        
        travel_class = st.selectbox("Kelas Perjalanan", ["Budget", "Standard", "Premium"])
    
    with col2:
        # Calculate estimates
        multiplier = {"Budget": 0.8, "Standard": 1.0, "Premium": 1.5}[travel_class]
        
        estimates = {
            "✈️ Tiket Pesawat": int(8_000_000 * multiplier),
            "🏨 Hotel Makkah": int(400_000 * duration * multiplier),
            "🏨 Hotel Madinah": int(350_000 * (duration // 3) * multiplier),
            "🚄 Transport": int(500_000 * multiplier),
            "🍽️ Makan": int(150_000 * duration),
            "📱 SIM & Data": 100_000,
            "🎁 Oleh-oleh": 1_500_000,
            "🔄 Lain-lain": 1_000_000,
        }
        
        total = sum(estimates.values())
        
        st.markdown("#### 📊 Estimasi Biaya:")
        for item, cost in estimates.items():
            st.write(f"{item}: **Rp {cost:,}**".replace(",", "."))
        
        st.divider()
        
        if total <= budget:
            st.success(f"### ✅ Total: Rp {total:,}".replace(",", "."))
            st.write(f"💰 Sisa: Rp {budget - total:,}".replace(",", "."))
        else:
            st.error(f"### ⚠️ Total: Rp {total:,}".replace(",", "."))
            st.write(f"❌ Kurang: Rp {total - budget:,}".replace(",", "."))
    
    if st.button("💾 Simpan Perhitungan", use_container_width=True):
        if "budget_set" not in st.session_state.um_achievements:
            unlock_achievement("budget_set")
        st.success("✅ Budget tersimpan!")

# =============================================================================
# 🛂 TAB: VISA CHECKER
# =============================================================================

def render_tab_visa():
    """Render Visa Checker tab."""
    st.markdown("## 🛂 Cek Kelayakan Visa")
    
    st.info("""
    **2 Jenis Visa untuk Umrah:**
    - **E-Tourist Visa**: Instant, apply sendiri online (~Rp 3.2jt)
    - **Umrah Visa**: Via PPIU/Travel Agent (~Rp 2.5jt)
    """)
    
    with st.form("visa_check_form"):
        nationality = st.selectbox("Kewarganegaraan", 
            ["Indonesia", "Malaysia", "Brunei"] + E_TOURIST_ELIGIBLE[:5] + ["Lainnya"])
        
        st.markdown("**Apakah Anda punya visa aktif:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            has_us = st.checkbox("🇺🇸 Visa USA")
        with col2:
            has_uk = st.checkbox("🇬🇧 Visa UK")
        with col3:
            has_schengen = st.checkbox("🇪🇺 Schengen")
        
        submitted = st.form_submit_button("🔍 Cek Kelayakan", use_container_width=True, type="primary")
        
        if submitted:
            eligible_etourist = nationality in E_TOURIST_ELIGIBLE or has_us or has_uk or has_schengen
            
            st.divider()
            
            if eligible_etourist:
                st.success("### ✅ Eligible: E-Tourist Visa!")
                st.markdown("""
                **Keuntungan E-Tourist:**
                - ⏱️ Proses instant (menit)
                - 💰 Biaya ~Rp 3.2jt
                - 📅 Valid 1 tahun, multiple entry
                - ✈️ Tidak perlu travel agent
                """)
                st.link_button("🔗 Apply di NUSUK", "https://umrah.nusuk.sa", use_container_width=True, type="primary")
            else:
                st.info("### ℹ️ Gunakan: Umrah Visa via PPIU")
                st.markdown("""
                **Proses Umrah Visa:**
                - ⏱️ Proses 1-3 hari kerja
                - 💰 Biaya ~Rp 2.5jt
                - 📅 Single entry
                - 🏢 Harus via travel agent resmi
                """)
                st.link_button("🔗 Cek PPIU Resmi", "https://simpu.kemenag.go.id/", use_container_width=True)
            
            unlock_achievement("visa_checked")

# =============================================================================
# 📍 TAB: MIQAT
# =============================================================================

def render_tab_miqat():
    """Render Miqat Locator tab."""
    st.markdown("## 📍 Panduan Miqat & Ihram")
    
    st.error("⚠️ **PENTING:** Melewati miqat tanpa ihram = umrah tidak sah!")
    
    route = st.selectbox("Pilih Rute Perjalanan Anda:", [
        "Jakarta → Jeddah (Direct Flight)",
        "Jakarta → Madinah → Makkah"
    ])
    
    if st.button("🔍 Lihat Panduan Miqat", use_container_width=True, type="primary"):
        st.divider()
        
        if "Madinah" in route:
            miqat = MIQAT_DATA["madinah_first"]
            st.success(f"### 📍 Miqat Anda: {miqat['name']}")
            st.write(f"⏰ **Waktu Ihram:** {miqat['timing']}")
        else:
            miqat = MIQAT_DATA["jeddah_direct"]
            st.warning(f"### 📍 Miqat Anda: {miqat['name']}")
            st.write(f"⏰ **Waktu Ihram:** {miqat['timing']}")
        
        st.markdown("#### 💡 Tips:")
        for tip in miqat["tips"]:
            st.write(tip)
        
        st.divider()
        st.markdown("### 🤲 Niat Umrah:")
        st.markdown("<div class='doa-arabic'>لَبَّيْكَ اللّٰهُمَّ عُمْرَةً</div>", unsafe_allow_html=True)
        st.markdown("**Latin:** *Labbaik Allahumma 'umratan*")
        st.markdown("**Arti:** Aku memenuhi panggilan-Mu ya Allah untuk umrah")
        
        unlock_achievement("miqat_master")

# =============================================================================
# 🔍 TAB: PPIU VERIFICATION
# =============================================================================

def render_tab_ppiu():
    """Render PPIU Verification tab."""
    st.markdown("## 🔍 Verifikasi Travel Agent (PPIU)")
    
    st.error("""
    ⚠️ **WASPADA PENIPUAN!**  
    Banyak travel agent ilegal yang menipu jamaah. 
    SELALU verifikasi sebelum bayar!
    """)
    
    st.link_button(
        "🔗 Buka SISKOPATUH KEMENAG", 
        "https://simpu.kemenag.go.id/",
        use_container_width=True,
        type="primary"
    )
    
    st.caption("📞 Hotline KEMENAG: **1500-363**")
    
    st.divider()
    
    st.markdown("### ✅ Checklist Verifikasi:")
    checks = [
        "Nama perusahaan terdaftar di SISKOPATUH",
        "Nomor SK Kemenag valid",
        "Alamat kantor jelas & bisa dikunjungi",
        "Ada kontrak tertulis yang jelas",
        "Pembayaran via rekening perusahaan (bukan pribadi)",
        "Review positif dari jamaah sebelumnya"
    ]
    
    all_checked = True
    for check in checks:
        if not st.checkbox(check, key=f"ppiu_{check[:10]}"):
            all_checked = False
    
    st.divider()
    
    if st.button("✅ Saya Sudah Verifikasi PPIU", use_container_width=True, type="primary"):
        if all_checked:
            unlock_achievement("safe_travel")
            st.success("🛡️ Excellent! Badge Safe Traveler unlocked!")
        else:
            st.warning("⚠️ Pastikan semua checklist tercentang untuk keamanan Anda!")

# =============================================================================
# 🏆 TAB: BADGES
# =============================================================================

def render_tab_badges():
    """Render Achievements/Badges tab."""
    st.markdown("## 🏆 Koleksi Badge")
    
    unlocked = len(st.session_state.um_achievements)
    total = len(ACHIEVEMENTS)
    
    st.progress(unlocked / total, text=f"{unlocked}/{total} badges unlocked")
    
    cols = st.columns(4)
    for i, ach in enumerate(ACHIEVEMENTS):
        with cols[i % 4]:
            is_unlocked = ach["id"] in st.session_state.um_achievements
            
            if is_unlocked:
                st.markdown(f"""
                <div class="achievement-badge">
                    <div style="font-size:2rem;">{ach['icon']}</div>
                    <div><b>{ach['name']}</b></div>
                    <small style="color:#888;">{ach['desc']}</small>
                    <div style="color:#d4af37;">+{ach['xp']} XP</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="achievement-badge locked">
                    <div style="font-size:2rem;">🔒</div>
                    <div><b>???</b></div>
                    <small style="color:#666;">{ach['desc']}</small>
                </div>
                """, unsafe_allow_html=True)

# =============================================================================
# 💰 TAB: TABUNGAN
# =============================================================================

def render_tab_savings():
    """Render Savings Tracker tab."""
    st.markdown("## 💰 Tracker Tabungan Umrah")
    
    col1, col2 = st.columns(2)
    
    with col1:
        target = st.number_input("Target Tabungan (Rp)", 
            min_value=5_000_000, 
            max_value=100_000_000, 
            value=st.session_state.um_savings["target"],
            step=1_000_000,
            format="%d"
        )
        st.session_state.um_savings["target"] = target
        
        current = st.number_input("Tabungan Saat Ini (Rp)",
            min_value=0,
            max_value=target,
            value=st.session_state.um_savings["current"],
            step=100_000,
            format="%d"
        )
        st.session_state.um_savings["current"] = current
    
    with col2:
        pct = int(current / target * 100) if target > 0 else 0
        
        st.markdown(f"""
        <div style="text-align:center;padding:1rem;">
            <div style="font-size:4rem;color:#d4af37;">{pct}%</div>
            <div style="color:#888;">Tercapai</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(min(pct / 100, 1.0))
        
        remaining = target - current
        st.write(f"💰 Sisa: **Rp {remaining:,}**".replace(",", "."))
        
        if st.session_state.um_departure_date:
            days = (st.session_state.um_departure_date - date.today()).days
            if days > 0:
                daily = remaining / days
                st.info(f"📅 Tabung **Rp {int(daily):,}**/hari".replace(",", "."))

# =============================================================================
# 🆘 TAB: SOS
# =============================================================================

def render_tab_sos():
    """Render SOS Emergency tab."""
    st.markdown("## 🆘 Emergency SOS")
    
    st.error("**Untuk keadaan darurat, hubungi nomor di bawah:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🇸🇦 Saudi Arabia")
        for c in EMERGENCY_CONTACTS["saudi"]:
            st.markdown(f"""
            <div style="background:#2d0d0d;padding:1rem;border-radius:10px;margin:0.5rem 0;text-align:center;border:1px solid #dc3545;">
                <div style="font-size:1.5rem;">{c['icon']}</div>
                <div><b>{c['name']}</b></div>
                <div style="font-size:1.5rem;color:#dc3545;font-weight:bold;">{c['phone']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🇮🇩 Indonesia")
        for c in EMERGENCY_CONTACTS["indonesia"]:
            st.markdown(f"""
            <div style="background:#1a2d1a;padding:1rem;border-radius:10px;margin:0.5rem 0;text-align:center;border:1px solid #28a745;">
                <div style="font-size:1.5rem;">{c['icon']}</div>
                <div><b>{c['name']}</b></div>
                <div style="font-size:1rem;color:#28a745;font-weight:bold;">{c['phone']}</div>
            </div>
            """, unsafe_allow_html=True)

# =============================================================================
# ⚠️ DYOR DISCLAIMER
# =============================================================================

def render_dyor():
    """Render DYOR disclaimer."""
    st.warning("""
    ⚠️ **DYOR - Do Your Own Research**
    
    LABBAIK.AI adalah platform edukasi. Informasi dapat berubah sewaktu-waktu.
    Selalu verifikasi di sumber resmi:
    - 🇸🇦 [nusuk.sa](https://www.nusuk.sa) - Platform Resmi Saudi
    - 🇮🇩 [simpu.kemenag.go.id](https://simpu.kemenag.go.id) - Verifikasi PPIU
    - 📞 Hotline KEMENAG: 1500-363
    
    **Anda bertanggung jawab penuh atas keputusan perjalanan ibadah Anda.**
    """)

# =============================================================================
# 🚀 MAIN RENDER FUNCTION
# =============================================================================

def render_umrah_mandiri_page():
    """Main entry point for Umrah Mandiri page."""
    
    # Initialize state
    init_umrah_mandiri_state()
    
    # Render hero & stats
    render_hero()
    render_stats_cards()
    st.markdown("")
    render_xp_bar()
    
    st.divider()
    
    # Main tabs - RESOURCES FIRST (NEW!)
    tabs = st.tabs([
        "📱 Resources",      # NEW - Tab pertama!
        "⏰ Countdown",
        "🏛️ 3 Pilar",
        "📿 Manasik",
        "💰 Budget",
        "🛂 Visa",
        "📍 Miqat",
        "🔍 PPIU",
        "🏆 Badges",
        "💳 Tabungan",
        "🆘 SOS"
    ])
    
    with tabs[0]:
        render_tab_resources()
    
    with tabs[1]:
        render_tab_countdown()
    
    with tabs[2]:
        render_tab_pillars()
    
    with tabs[3]:
        render_tab_manasik()
    
    with tabs[4]:
        render_tab_budget()
    
    with tabs[5]:
        render_tab_visa()
    
    with tabs[6]:
        render_tab_miqat()
    
    with tabs[7]:
        render_tab_ppiu()
    
    with tabs[8]:
        render_tab_badges()
    
    with tabs[9]:
        render_tab_savings()
    
    with tabs[10]:
        render_tab_sos()
    
    st.divider()
    render_dyor()


# =============================================================================
# EXPORT
# =============================================================================

__all__ = ["render_umrah_mandiri_page"]
