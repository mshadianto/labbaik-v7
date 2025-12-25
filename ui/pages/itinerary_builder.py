"""
================================================================================
🗓️ LABBAIK AI - AI ITINERARY BUILDER
================================================================================
Lokasi: ui/pages/itinerary_builder.py (atau features/itinerary_builder.py)
Fitur: Generate jadwal harian Umrah otomatis dengan AI
================================================================================
"""

import streamlit as st
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional
import json

# =============================================================================
# 🎨 STYLING
# =============================================================================

ITINERARY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');

.itinerary-hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 1.5rem;
    border: 1px solid #d4af37;
}

.itinerary-hero h1 {
    color: #d4af37;
    margin: 0;
    font-size: 2rem;
}

.itinerary-hero .subtitle {
    color: #888;
    font-size: 1rem;
}

.day-card {
    background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%);
    border-radius: 15px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-left: 4px solid #d4af37;
}

.day-header {
    color: #d4af37;
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.activity-item {
    display: flex;
    align-items: flex-start;
    padding: 0.75rem 0;
    border-bottom: 1px solid #333;
}

.activity-item:last-child {
    border-bottom: none;
}

.activity-time {
    color: #d4af37;
    font-weight: bold;
    min-width: 60px;
    font-size: 0.9rem;
}

.activity-icon {
    font-size: 1.2rem;
    margin: 0 0.75rem;
}

.activity-content {
    flex: 1;
}

.activity-title {
    color: white;
    font-weight: 500;
}

.activity-desc {
    color: #888;
    font-size: 0.85rem;
    margin-top: 0.25rem;
}

.activity-tag {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 10px;
    font-size: 0.7rem;
    margin-top: 0.25rem;
}

.tag-ibadah { background: #1a4d1a; color: #4ade80; }
.tag-transport { background: #1a3d4d; color: #60a5fa; }
.tag-rest { background: #4d3d1a; color: #fbbf24; }
.tag-food { background: #4d1a1a; color: #f87171; }
.tag-explore { background: #3d1a4d; color: #c084fc; }

.summary-box {
    background: linear-gradient(135deg, #0d2818 0%, #1a4d2e 100%);
    border: 1px solid #4ade80;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.tips-box {
    background: linear-gradient(135deg, #2d1a0d 0%, #4d3319 100%);
    border: 1px solid #d4af37;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.export-btn {
    background: linear-gradient(135deg, #d4af37 0%, #f4d03f 100%);
    color: #1a1a1a;
    padding: 0.75rem 1.5rem;
    border-radius: 10px;
    font-weight: bold;
    text-align: center;
    cursor: pointer;
}

.stat-mini {
    text-align: center;
    padding: 1rem;
    background: #2d2d2d;
    border-radius: 10px;
}

.stat-mini .number {
    font-size: 1.5rem;
    color: #d4af37;
    font-weight: bold;
}

.stat-mini .label {
    color: #888;
    font-size: 0.8rem;
}
</style>
"""

# =============================================================================
# 📊 ITINERARY DATA & TEMPLATES
# =============================================================================

# Prayer times template (approximate, will vary by season)
PRAYER_TIMES_MAKKAH = {
    "fajr": "05:00",
    "sunrise": "06:30",
    "dhuhr": "12:15",
    "asr": "15:30",
    "maghrib": "18:00",
    "isha": "19:30"
}

PRAYER_TIMES_MADINAH = {
    "fajr": "05:15",
    "sunrise": "06:45",
    "dhuhr": "12:20",
    "asr": "15:35",
    "maghrib": "18:05",
    "isha": "19:35"
}

# Activity templates
ACTIVITIES = {
    # Makkah Activities
    "arrival_jeddah": {
        "title": "Landing di Jeddah Airport",
        "icon": "✈️",
        "duration": 90,
        "tag": "transport",
        "desc": "Imigrasi, ambil bagasi, tukar uang jika perlu"
    },
    "hhr_to_makkah": {
        "title": "Haramain Train ke Makkah",
        "icon": "🚄",
        "duration": 45,
        "tag": "transport",
        "desc": "Kereta cepat dari Jeddah Airport ke Makkah (SAR 75)"
    },
    "hhr_to_madinah": {
        "title": "Haramain Train ke Madinah",
        "icon": "🚄",
        "duration": 150,
        "tag": "transport",
        "desc": "Kereta cepat Makkah ke Madinah (SAR 250, 2.5 jam)"
    },
    "hhr_madinah_jeddah": {
        "title": "Haramain Train ke Jeddah",
        "icon": "🚄",
        "duration": 110,
        "tag": "transport",
        "desc": "Kereta cepat Madinah ke Jeddah Airport (SAR 200)"
    },
    "checkin_hotel_makkah": {
        "title": "Check-in Hotel Makkah",
        "icon": "🏨",
        "duration": 30,
        "tag": "rest",
        "desc": "Simpan bagasi, istirahat sebentar, persiapan ihram"
    },
    "checkin_hotel_madinah": {
        "title": "Check-in Hotel Madinah",
        "icon": "🏨",
        "duration": 30,
        "tag": "rest",
        "desc": "Simpan bagasi, istirahat, siap-siap ke Masjid Nabawi"
    },
    "umrah_full": {
        "title": "UMRAH: Thawaf + Sa'i + Tahallul",
        "icon": "🕋",
        "duration": 180,
        "tag": "ibadah",
        "desc": "Thawaf 7 putaran → Sholat 2 rakaat → Minum Zamzam → Sa'i 7 kali → Potong rambut"
    },
    "thawaf_sunnah": {
        "title": "Thawaf Sunnah",
        "icon": "🕋",
        "duration": 60,
        "tag": "ibadah",
        "desc": "Thawaf sunnah untuk menambah pahala"
    },
    "sholat_fajr": {
        "title": "Sholat Subuh di Masjidil Haram",
        "icon": "🌙",
        "duration": 45,
        "tag": "ibadah",
        "desc": "Sholat Subuh berjamaah"
    },
    "sholat_dhuhr": {
        "title": "Sholat Dzuhur",
        "icon": "☀️",
        "duration": 30,
        "tag": "ibadah",
        "desc": "Sholat Dzuhur berjamaah"
    },
    "sholat_asr": {
        "title": "Sholat Ashar",
        "icon": "🌤️",
        "duration": 30,
        "tag": "ibadah",
        "desc": "Sholat Ashar berjamaah"
    },
    "sholat_maghrib": {
        "title": "Sholat Maghrib",
        "icon": "🌅",
        "duration": 30,
        "tag": "ibadah",
        "desc": "Sholat Maghrib berjamaah"
    },
    "sholat_isha": {
        "title": "Sholat Isya",
        "icon": "🌙",
        "duration": 30,
        "tag": "ibadah",
        "desc": "Sholat Isya berjamaah"
    },
    "rest_morning": {
        "title": "Istirahat Pagi",
        "icon": "😴",
        "duration": 120,
        "tag": "rest",
        "desc": "Tidur/istirahat setelah Subuh"
    },
    "rest_afternoon": {
        "title": "Istirahat Siang",
        "icon": "😴",
        "duration": 90,
        "tag": "rest",
        "desc": "Qailulah (tidur siang sunnah)"
    },
    "rest_night": {
        "title": "Tidur Malam",
        "icon": "😴",
        "duration": 360,
        "tag": "rest",
        "desc": "Istirahat untuk ibadah esok hari"
    },
    "breakfast": {
        "title": "Sarapan",
        "icon": "🍳",
        "duration": 30,
        "tag": "food",
        "desc": "Sarapan di hotel atau sekitar Haram"
    },
    "lunch": {
        "title": "Makan Siang",
        "icon": "🍽️",
        "duration": 45,
        "tag": "food",
        "desc": "Makan siang"
    },
    "dinner": {
        "title": "Makan Malam",
        "icon": "🍽️",
        "duration": 45,
        "tag": "food",
        "desc": "Makan malam"
    },
    "ziarah_makkah": {
        "title": "Ziarah Tempat Bersejarah Makkah",
        "icon": "🏛️",
        "duration": 180,
        "tag": "explore",
        "desc": "Jabal Nur, Gua Hira, Jabal Tsur, Arafah, Mina, Muzdalifah"
    },
    "shopping_makkah": {
        "title": "Belanja Oleh-oleh",
        "icon": "🛍️",
        "duration": 120,
        "tag": "explore",
        "desc": "Belanja di sekitar Masjidil Haram atau mall"
    },
    # Madinah Activities
    "sholat_masjid_nabawi": {
        "title": "Sholat di Masjid Nabawi",
        "icon": "🕌",
        "duration": 45,
        "tag": "ibadah",
        "desc": "Sholat berjamaah di Masjid Nabawi (1000x lipat pahala)"
    },
    "ziarah_raudhah": {
        "title": "Ziarah Raudhah",
        "icon": "💚",
        "duration": 60,
        "tag": "ibadah",
        "desc": "Sholat & berdoa di Raudhah (taman surga)"
    },
    "ziarah_makam_rasul": {
        "title": "Ziarah Makam Rasulullah ﷺ",
        "icon": "🌹",
        "duration": 30,
        "tag": "ibadah",
        "desc": "Salam kepada Rasulullah, Abu Bakar, dan Umar"
    },
    "ziarah_baqi": {
        "title": "Ziarah Pemakaman Baqi",
        "icon": "🪦",
        "duration": 45,
        "tag": "ibadah",
        "desc": "Ziarah makam sahabat & keluarga Nabi"
    },
    "ziarah_uhud": {
        "title": "Ziarah Jabal Uhud",
        "icon": "⛰️",
        "duration": 120,
        "tag": "explore",
        "desc": "Makam Hamzah, lokasi Perang Uhud"
    },
    "ziarah_quba": {
        "title": "Sholat di Masjid Quba",
        "icon": "🕌",
        "duration": 90,
        "tag": "ibadah",
        "desc": "Masjid pertama dalam Islam (pahala = umrah)"
    },
    "ziarah_qiblatain": {
        "title": "Sholat di Masjid Qiblatain",
        "icon": "🕌",
        "duration": 60,
        "tag": "ibadah",
        "desc": "Masjid dua kiblat"
    },
    "ziarah_7_masjid": {
        "title": "Ziarah 7 Masjid (Sab'ah Masajid)",
        "icon": "🕌",
        "duration": 90,
        "tag": "explore",
        "desc": "Kompleks 7 masjid bersejarah"
    },
    "departure": {
        "title": "Check-out & Berangkat ke Airport",
        "icon": "✈️",
        "duration": 60,
        "tag": "transport",
        "desc": "Persiapan pulang ke tanah air"
    },
    "free_time": {
        "title": "Waktu Bebas",
        "icon": "🚶",
        "duration": 60,
        "tag": "rest",
        "desc": "Eksplorasi bebas atau istirahat"
    }
}

# Route templates
ROUTE_TEMPLATES = {
    "makkah_first": {
        "name": "Makkah Dulu",
        "desc": "Landing Jeddah → Makkah → Madinah → Pulang via Madinah/Jeddah",
        "flow": ["jeddah", "makkah", "madinah", "departure"]
    },
    "madinah_first": {
        "name": "Madinah Dulu", 
        "desc": "Landing Jeddah/Madinah → Madinah → Makkah → Pulang via Jeddah",
        "flow": ["arrival", "madinah", "makkah", "departure"]
    }
}

# Ziarah packages
ZIARAH_MAKKAH = [
    {"name": "Jabal Nur & Gua Hira", "duration": 120, "desc": "Tempat turunnya wahyu pertama"},
    {"name": "Jabal Tsur", "duration": 90, "desc": "Tempat persembunyian Nabi saat hijrah"},
    {"name": "Arafah", "duration": 60, "desc": "Lokasi wukuf haji"},
    {"name": "Mina & Muzdalifah", "duration": 90, "desc": "Lokasi mabit & lempar jumrah"},
    {"name": "Pemakaman Ma'la", "duration": 45, "desc": "Makam Khadijah & keluarga Nabi"},
]

ZIARAH_MADINAH = [
    {"name": "Masjid Quba", "duration": 60, "desc": "Masjid pertama, pahala = umrah"},
    {"name": "Jabal Uhud", "duration": 90, "desc": "Lokasi Perang Uhud, makam Hamzah"},
    {"name": "Masjid Qiblatain", "duration": 45, "desc": "Masjid dua kiblat"},
    {"name": "Pemakaman Baqi", "duration": 30, "desc": "Makam sahabat & keluarga Nabi"},
    {"name": "7 Masjid", "duration": 60, "desc": "Kompleks masjid bersejarah"},
    {"name": "Kebun Kurma", "duration": 45, "desc": "Ajwa, kurma favorit Nabi"},
]

# =============================================================================
# 🔧 HELPER FUNCTIONS
# =============================================================================

def time_add(time_str: str, minutes: int) -> str:
    """Add minutes to time string."""
    h, m = map(int, time_str.split(":"))
    total = h * 60 + m + minutes
    return f"{(total // 60) % 24:02d}:{total % 60:02d}"

def generate_day_schedule(
    day_num: int,
    location: str,
    day_type: str,
    prayer_times: dict,
    preferences: dict
) -> List[dict]:
    """Generate schedule for a single day."""
    schedule = []
    
    if day_type == "arrival_makkah":
        # Arrival day - Makkah
        schedule = [
            {"time": "06:00", **ACTIVITIES["arrival_jeddah"]},
            {"time": "07:30", **ACTIVITIES["hhr_to_makkah"]},
            {"time": "08:30", **ACTIVITIES["checkin_hotel_makkah"]},
            {"time": "09:00", **ACTIVITIES["rest_morning"]},
            {"time": "12:15", **ACTIVITIES["sholat_dhuhr"]},
            {"time": "13:00", **ACTIVITIES["lunch"]},
            {"time": "14:00", **ACTIVITIES["rest_afternoon"]},
            {"time": "15:30", **ACTIVITIES["sholat_asr"]},
            {"time": "16:30", **ACTIVITIES["umrah_full"]},
            {"time": "18:00", **ACTIVITIES["sholat_maghrib"]},
            {"time": "19:00", **ACTIVITIES["dinner"]},
            {"time": "19:30", **ACTIVITIES["sholat_isha"]},
            {"time": "21:00", **ACTIVITIES["rest_night"]},
        ]
    
    elif day_type == "arrival_madinah":
        # Arrival day - Madinah first
        schedule = [
            {"time": "06:00", **ACTIVITIES["arrival_jeddah"]},
            {"time": "07:30", "title": "Haramain Train ke Madinah", "icon": "🚄", "duration": 110, "tag": "transport", "desc": "Kereta cepat dari Jeddah ke Madinah (SAR 200)"},
            {"time": "10:00", **ACTIVITIES["checkin_hotel_madinah"]},
            {"time": "10:30", **ACTIVITIES["rest_morning"]},
            {"time": "12:20", **ACTIVITIES["sholat_masjid_nabawi"]},
            {"time": "13:00", **ACTIVITIES["lunch"]},
            {"time": "14:00", **ACTIVITIES["rest_afternoon"]},
            {"time": "15:35", **ACTIVITIES["sholat_masjid_nabawi"]},
            {"time": "16:30", **ACTIVITIES["ziarah_makam_rasul"]},
            {"time": "18:05", **ACTIVITIES["sholat_maghrib"]},
            {"time": "19:00", **ACTIVITIES["dinner"]},
            {"time": "19:35", **ACTIVITIES["sholat_isha"]},
            {"time": "21:00", **ACTIVITIES["rest_night"]},
        ]
    
    elif day_type == "makkah_regular":
        # Regular day in Makkah
        schedule = [
            {"time": "04:30", "title": "Bangun & Persiapan", "icon": "⏰", "duration": 30, "tag": "rest", "desc": "Wudhu, persiapan ke Haram"},
            {"time": "05:00", **ACTIVITIES["sholat_fajr"]},
            {"time": "06:00", "title": "Thawaf Sunnah / Dzikir", "icon": "🕋", "duration": 60, "tag": "ibadah", "desc": "Thawaf sunnah atau dzikir pagi"},
            {"time": "07:00", **ACTIVITIES["breakfast"]},
            {"time": "08:00", **ACTIVITIES["rest_morning"]},
            {"time": "12:15", **ACTIVITIES["sholat_dhuhr"]},
            {"time": "13:00", **ACTIVITIES["lunch"]},
            {"time": "14:00", **ACTIVITIES["rest_afternoon"]},
            {"time": "15:30", **ACTIVITIES["sholat_asr"]},
            {"time": "16:30", **ACTIVITIES["thawaf_sunnah"]},
            {"time": "18:00", **ACTIVITIES["sholat_maghrib"]},
            {"time": "19:00", **ACTIVITIES["dinner"]},
            {"time": "19:30", **ACTIVITIES["sholat_isha"]},
            {"time": "20:30", "title": "Ibadah Malam / Tahajud", "icon": "🌙", "duration": 90, "tag": "ibadah", "desc": "Thawaf, dzikir, atau tahajud"},
            {"time": "22:00", **ACTIVITIES["rest_night"]},
        ]
        
        # Add ziarah option
        if preferences.get("include_ziarah") and day_num % 2 == 0:
            schedule[7] = {"time": "08:00", **ACTIVITIES["ziarah_makkah"]}
    
    elif day_type == "madinah_regular":
        # Regular day in Madinah
        schedule = [
            {"time": "04:45", "title": "Bangun & Persiapan", "icon": "⏰", "duration": 30, "tag": "rest", "desc": "Wudhu, persiapan ke Masjid Nabawi"},
            {"time": "05:15", **ACTIVITIES["sholat_masjid_nabawi"]},
            {"time": "06:00", "title": "Dzikir Pagi / Raudhah", "icon": "💚", "duration": 60, "tag": "ibadah", "desc": "Dzikir atau antri Raudhah"},
            {"time": "07:00", **ACTIVITIES["breakfast"]},
            {"time": "08:00", **ACTIVITIES["rest_morning"]},
            {"time": "12:20", **ACTIVITIES["sholat_masjid_nabawi"]},
            {"time": "13:00", **ACTIVITIES["lunch"]},
            {"time": "14:00", **ACTIVITIES["rest_afternoon"]},
            {"time": "15:35", **ACTIVITIES["sholat_masjid_nabawi"]},
            {"time": "16:30", **ACTIVITIES["ziarah_baqi"]},
            {"time": "18:05", **ACTIVITIES["sholat_maghrib"]},
            {"time": "19:00", **ACTIVITIES["dinner"]},
            {"time": "19:35", **ACTIVITIES["sholat_isha"]},
            {"time": "20:30", "title": "Sholat & Dzikir Malam", "icon": "🌙", "duration": 90, "tag": "ibadah", "desc": "Ibadah malam di Masjid Nabawi"},
            {"time": "22:00", **ACTIVITIES["rest_night"]},
        ]
        
        # Add ziarah variations
        if preferences.get("include_ziarah"):
            if day_num == 1:
                schedule[9] = {"time": "16:30", **ACTIVITIES["ziarah_quba"]}
            elif day_num == 2:
                schedule[9] = {"time": "16:30", **ACTIVITIES["ziarah_uhud"]}
    
    elif day_type == "travel_makkah_madinah":
        # Travel day Makkah to Madinah
        schedule = [
            {"time": "04:30", "title": "Bangun & Persiapan", "icon": "⏰", "duration": 30, "tag": "rest", "desc": "Wudhu, packing"},
            {"time": "05:00", **ACTIVITIES["sholat_fajr"]},
            {"time": "06:00", "title": "Check-out Hotel", "icon": "🏨", "duration": 60, "tag": "transport", "desc": "Check-out dan ke stasiun"},
            {"time": "07:00", **ACTIVITIES["hhr_to_madinah"]},
            {"time": "10:00", **ACTIVITIES["checkin_hotel_madinah"]},
            {"time": "10:30", **ACTIVITIES["rest_morning"]},
            {"time": "12:20", **ACTIVITIES["sholat_masjid_nabawi"]},
            {"time": "13:00", **ACTIVITIES["lunch"]},
            {"time": "14:00", **ACTIVITIES["ziarah_makam_rasul"]},
            {"time": "15:35", **ACTIVITIES["sholat_masjid_nabawi"]},
            {"time": "16:30", **ACTIVITIES["free_time"]},
            {"time": "18:05", **ACTIVITIES["sholat_maghrib"]},
            {"time": "19:00", **ACTIVITIES["dinner"]},
            {"time": "19:35", **ACTIVITIES["sholat_isha"]},
            {"time": "21:00", **ACTIVITIES["rest_night"]},
        ]
    
    elif day_type == "travel_madinah_makkah":
        # Travel day Madinah to Makkah (need ihram!)
        schedule = [
            {"time": "04:45", "title": "Bangun & Persiapan Ihram", "icon": "⏰", "duration": 30, "tag": "rest", "desc": "Mandi, pakai ihram, niat umrah"},
            {"time": "05:15", **ACTIVITIES["sholat_masjid_nabawi"]},
            {"time": "06:00", "title": "Check-out & ke Miqat Bir Ali", "icon": "🏨", "duration": 90, "tag": "transport", "desc": "Ke Masjid Dzulhulaifah untuk ihram"},
            {"time": "07:30", "title": "Ihram di Bir Ali", "icon": "🧕", "duration": 30, "tag": "ibadah", "desc": "Sholat 2 rakaat, niat umrah, mulai talbiyah"},
            {"time": "08:00", **ACTIVITIES["hhr_to_makkah"]},
            {"time": "10:30", **ACTIVITIES["checkin_hotel_makkah"]},
            {"time": "11:00", **ACTIVITIES["rest_morning"]},
            {"time": "12:15", **ACTIVITIES["sholat_dhuhr"]},
            {"time": "13:00", **ACTIVITIES["lunch"]},
            {"time": "14:00", **ACTIVITIES["umrah_full"]},
            {"time": "18:00", **ACTIVITIES["sholat_maghrib"]},
            {"time": "19:00", **ACTIVITIES["dinner"]},
            {"time": "19:30", **ACTIVITIES["sholat_isha"]},
            {"time": "21:00", **ACTIVITIES["rest_night"]},
        ]
    
    elif day_type == "departure":
        # Departure day
        schedule = [
            {"time": "04:30", "title": "Bangun & Persiapan", "icon": "⏰", "duration": 30, "tag": "rest", "desc": "Wudhu, packing final"},
            {"time": "05:00", "title": "Sholat Subuh Terakhir", "icon": "🌙", "duration": 45, "tag": "ibadah", "desc": "Sholat Subuh terakhir di Tanah Suci 😢"},
            {"time": "06:00", **ACTIVITIES["breakfast"]},
            {"time": "07:00", **ACTIVITIES["departure"]},
            {"time": "08:00", "title": "Ke Bandara", "icon": "🚄", "duration": 120, "tag": "transport", "desc": "Perjalanan ke Jeddah Airport"},
            {"time": "10:00", "title": "Check-in Bandara", "icon": "✈️", "duration": 180, "tag": "transport", "desc": "Check-in, imigrasi, tunggu boarding"},
            {"time": "13:00", "title": "Boarding & Terbang", "icon": "✈️", "duration": 0, "tag": "transport", "desc": "Pulang ke Indonesia. Alhamdulillah! 🤲"},
        ]
    
    else:
        # Default fallback
        schedule = [
            {"time": "05:00", **ACTIVITIES["sholat_fajr"]},
            {"time": "12:15", **ACTIVITIES["sholat_dhuhr"]},
            {"time": "15:30", **ACTIVITIES["sholat_asr"]},
            {"time": "18:00", **ACTIVITIES["sholat_maghrib"]},
            {"time": "19:30", **ACTIVITIES["sholat_isha"]},
        ]
    
    return schedule

def generate_full_itinerary(
    duration: int,
    route: str,
    makkah_days: int,
    madinah_days: int,
    preferences: dict
) -> List[dict]:
    """Generate complete itinerary."""
    itinerary = []
    current_day = 1
    
    if route == "makkah_first":
        # Day 1: Arrival in Makkah
        itinerary.append({
            "day": current_day,
            "date": None,  # Will be filled later
            "location": "Makkah",
            "title": f"Hari {current_day}: Arrival & Umrah",
            "type": "arrival_makkah",
            "schedule": generate_day_schedule(current_day, "makkah", "arrival_makkah", PRAYER_TIMES_MAKKAH, preferences)
        })
        current_day += 1
        
        # Makkah days
        for i in range(makkah_days - 1):
            itinerary.append({
                "day": current_day,
                "date": None,
                "location": "Makkah",
                "title": f"Hari {current_day}: Ibadah di Makkah",
                "type": "makkah_regular",
                "schedule": generate_day_schedule(current_day, "makkah", "makkah_regular", PRAYER_TIMES_MAKKAH, preferences)
            })
            current_day += 1
        
        # Travel to Madinah
        itinerary.append({
            "day": current_day,
            "date": None,
            "location": "Makkah → Madinah",
            "title": f"Hari {current_day}: Perjalanan ke Madinah",
            "type": "travel_makkah_madinah",
            "schedule": generate_day_schedule(current_day, "travel", "travel_makkah_madinah", PRAYER_TIMES_MADINAH, preferences)
        })
        current_day += 1
        
        # Madinah days
        for i in range(madinah_days - 1):
            itinerary.append({
                "day": current_day,
                "date": None,
                "location": "Madinah",
                "title": f"Hari {current_day}: Ibadah di Madinah",
                "type": "madinah_regular",
                "schedule": generate_day_schedule(i + 1, "madinah", "madinah_regular", PRAYER_TIMES_MADINAH, preferences)
            })
            current_day += 1
        
        # Departure
        itinerary.append({
            "day": current_day,
            "date": None,
            "location": "Madinah → Indonesia",
            "title": f"Hari {current_day}: Pulang ke Tanah Air",
            "type": "departure",
            "schedule": generate_day_schedule(current_day, "departure", "departure", PRAYER_TIMES_MADINAH, preferences)
        })
    
    else:  # madinah_first
        # Day 1: Arrival in Madinah
        itinerary.append({
            "day": current_day,
            "date": None,
            "location": "Madinah",
            "title": f"Hari {current_day}: Arrival Madinah",
            "type": "arrival_madinah",
            "schedule": generate_day_schedule(current_day, "madinah", "arrival_madinah", PRAYER_TIMES_MADINAH, preferences)
        })
        current_day += 1
        
        # Madinah days
        for i in range(madinah_days - 1):
            itinerary.append({
                "day": current_day,
                "date": None,
                "location": "Madinah",
                "title": f"Hari {current_day}: Ibadah di Madinah",
                "type": "madinah_regular",
                "schedule": generate_day_schedule(i + 1, "madinah", "madinah_regular", PRAYER_TIMES_MADINAH, preferences)
            })
            current_day += 1
        
        # Travel to Makkah (with Ihram!)
        itinerary.append({
            "day": current_day,
            "date": None,
            "location": "Madinah → Makkah",
            "title": f"Hari {current_day}: Ihram & Perjalanan ke Makkah",
            "type": "travel_madinah_makkah",
            "schedule": generate_day_schedule(current_day, "travel", "travel_madinah_makkah", PRAYER_TIMES_MAKKAH, preferences)
        })
        current_day += 1
        
        # Makkah days
        for i in range(makkah_days - 1):
            itinerary.append({
                "day": current_day,
                "date": None,
                "location": "Makkah",
                "title": f"Hari {current_day}: Ibadah di Makkah",
                "type": "makkah_regular",
                "schedule": generate_day_schedule(current_day, "makkah", "makkah_regular", PRAYER_TIMES_MAKKAH, preferences)
            })
            current_day += 1
        
        # Departure
        itinerary.append({
            "day": current_day,
            "date": None,
            "location": "Makkah → Indonesia",
            "title": f"Hari {current_day}: Pulang ke Tanah Air",
            "type": "departure",
            "schedule": generate_day_schedule(current_day, "departure", "departure", PRAYER_TIMES_MAKKAH, preferences)
        })
    
    return itinerary

def export_to_text(itinerary: List[dict], start_date: date) -> str:
    """Export itinerary to plain text format."""
    output = []
    output.append("=" * 50)
    output.append("🕋 JADWAL UMRAH - Generated by LABBAIK.AI")
    output.append("=" * 50)
    output.append("")
    
    for day in itinerary:
        day_date = start_date + timedelta(days=day["day"] - 1)
        output.append(f"📅 {day['title']}")
        output.append(f"   {day_date.strftime('%A, %d %B %Y')} | 📍 {day['location']}")
        output.append("-" * 40)
        
        for item in day["schedule"]:
            output.append(f"   {item['time']}  {item['icon']} {item['title']}")
            if item.get('desc'):
                output.append(f"          └─ {item['desc']}")
        
        output.append("")
    
    output.append("=" * 50)
    output.append("Generated by LABBAIK.AI - labbaik-umrahplanner.streamlit.app")
    output.append("⚠️ Jadwal bersifat estimasi, sesuaikan dengan kondisi aktual")
    output.append("=" * 50)
    
    return "\n".join(output)

def export_to_whatsapp(itinerary: List[dict], start_date: date) -> str:
    """Export itinerary to WhatsApp-friendly format."""
    output = []
    output.append("🕋 *JADWAL UMRAH*")
    output.append("_Generated by LABBAIK.AI_")
    output.append("")
    
    for day in itinerary:
        day_date = start_date + timedelta(days=day["day"] - 1)
        output.append(f"*{day['title']}*")
        output.append(f"📍 {day['location']} | {day_date.strftime('%d/%m/%Y')}")
        output.append("")
        
        for item in day["schedule"]:
            output.append(f"⏰ {item['time']} {item['icon']} {item['title']}")
        
        output.append("")
        output.append("─" * 20)
        output.append("")
    
    output.append("🔗 labbaik-umrahplanner.streamlit.app")
    
    return "\n".join(output)

# =============================================================================
# 🎨 UI COMPONENTS
# =============================================================================

def render_hero():
    """Render hero section."""
    st.markdown(ITINERARY_CSS, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="itinerary-hero">
        <h1>🗓️ AI Itinerary Builder</h1>
        <p class="subtitle">Generate jadwal Umrah harian otomatis dalam hitungan detik</p>
    </div>
    """, unsafe_allow_html=True)

def render_day_schedule(day: dict, day_date: date):
    """Render a single day's schedule."""
    st.markdown(f"""
    <div class="day-card">
        <div class="day-header">
            📅 {day['title']} — {day_date.strftime('%A, %d %b %Y')}
            <span style="margin-left:auto;font-size:0.9rem;color:#888;">📍 {day['location']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    for item in day["schedule"]:
        tag_class = f"tag-{item.get('tag', 'rest')}"
        tag_label = {
            "ibadah": "Ibadah",
            "transport": "Transport",
            "rest": "Istirahat",
            "food": "Makan",
            "explore": "Ziarah"
        }.get(item.get('tag'), '')
        
        st.markdown(f"""
        <div class="activity-item">
            <span class="activity-time">{item['time']}</span>
            <span class="activity-icon">{item['icon']}</span>
            <div class="activity-content">
                <div class="activity-title">{item['title']}</div>
                <div class="activity-desc">{item.get('desc', '')}</div>
                <span class="activity-tag {tag_class}">{tag_label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_itinerary_summary(itinerary: List[dict], preferences: dict):
    """Render itinerary summary."""
    total_days = len(itinerary)
    makkah_days = sum(1 for d in itinerary if "Makkah" in d["location"] and "→" not in d["location"])
    madinah_days = sum(1 for d in itinerary if "Madinah" in d["location"] and "→" not in d["location"])
    travel_days = sum(1 for d in itinerary if "→" in d["location"])
    
    st.markdown("""
    <div class="summary-box">
        <h3 style="color:#4ade80;margin-top:0;">📊 Ringkasan Itinerary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    with cols[0]:
        st.markdown(f"""
        <div class="stat-mini">
            <div class="number">{total_days}</div>
            <div class="label">Total Hari</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
        <div class="stat-mini">
            <div class="number">{makkah_days}</div>
            <div class="label">Hari di Makkah</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown(f"""
        <div class="stat-mini">
            <div class="number">{madinah_days}</div>
            <div class="label">Hari di Madinah</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown(f"""
        <div class="stat-mini">
            <div class="number">{travel_days}</div>
            <div class="label">Hari Perjalanan</div>
        </div>
        """, unsafe_allow_html=True)

def render_tips():
    """Render tips section."""
    st.markdown("""
    <div class="tips-box">
        <h3 style="color:#d4af37;margin-top:0;">💡 Tips Penting</h3>
    </div>
    """, unsafe_allow_html=True)
    
    tips = [
        "⏰ **Waktu sholat bersifat estimasi** - cek waktu aktual via aplikasi Muslim Pro atau azan masjid",
        "🚶 **Jarak hotel ke Haram** sangat mempengaruhi waktu tempuh, sesuaikan jadwal",
        "😴 **Jangan skip istirahat** - fisik yang fit = ibadah lebih khusyuk",
        "🥤 **Minum banyak air** - cuaca panas, dehidrasi berbahaya",
        "📱 **Download peta offline** - WiFi tidak selalu tersedia",
        "🕐 **Datang lebih awal** untuk sholat Jumat (minimal 2 jam sebelum)",
    ]
    
    for tip in tips:
        st.markdown(tip)

# =============================================================================
# 🚀 MAIN PAGE FUNCTION
# =============================================================================

def render_itinerary_builder_page():
    """Main entry point for Itinerary Builder page."""
    
    # Initialize session state
    if "itinerary_generated" not in st.session_state:
        st.session_state.itinerary_generated = False
    if "current_itinerary" not in st.session_state:
        st.session_state.current_itinerary = None
    
    render_hero()
    
    # === INPUT FORM ===
    with st.container(border=True):
        st.markdown("### ⚙️ Konfigurasi Perjalanan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "📅 Tanggal Keberangkatan",
                value=date.today() + timedelta(days=30),
                min_value=date.today()
            )
            
            duration = st.slider(
                "⏱️ Total Durasi (hari)",
                min_value=7,
                max_value=21,
                value=9,
                help="Durasi total perjalanan termasuk travel"
            )
            
            route = st.selectbox(
                "🛤️ Rute Perjalanan",
                options=["makkah_first", "madinah_first"],
                format_func=lambda x: "Makkah Dulu → Madinah" if x == "makkah_first" else "Madinah Dulu → Makkah",
                help="Pilih mana yang dikunjungi lebih dulu"
            )
        
        with col2:
            # Calculate default split
            default_makkah = (duration - 2) * 2 // 3 + 1
            default_madinah = duration - default_makkah - 1
            
            makkah_days = st.slider(
                "🕋 Hari di Makkah",
                min_value=3,
                max_value=duration - 4,
                value=min(default_makkah, duration - 4),
                help="Jumlah hari di Makkah (termasuk arrival/departure)"
            )
            
            madinah_days = duration - makkah_days - 1  # -1 for travel day
            st.info(f"🕌 Hari di Madinah: **{madinah_days} hari** (otomatis)")
            
            include_ziarah = st.checkbox(
                "🏛️ Include Ziarah Tempat Bersejarah",
                value=True,
                help="Tambahkan ziarah ke tempat bersejarah"
            )
        
        # Preferences
        preferences = {
            "include_ziarah": include_ziarah,
            "pace": "normal"  # Could add: relaxed, intensive
        }
        
        # Generate button
        if st.button("🚀 Generate Itinerary", use_container_width=True, type="primary"):
            with st.spinner("✨ AI sedang menyusun jadwal terbaik untuk Anda..."):
                itinerary = generate_full_itinerary(
                    duration=duration,
                    route=route,
                    makkah_days=makkah_days,
                    madinah_days=madinah_days,
                    preferences=preferences
                )
                
                st.session_state.current_itinerary = itinerary
                st.session_state.itinerary_start_date = start_date
                st.session_state.itinerary_generated = True
                st.rerun()
    
    # === DISPLAY ITINERARY ===
    if st.session_state.itinerary_generated and st.session_state.current_itinerary:
        itinerary = st.session_state.current_itinerary
        start_date = st.session_state.itinerary_start_date
        
        st.divider()
        
        # Summary
        render_itinerary_summary(itinerary, preferences)
        
        st.divider()
        
        # Export buttons
        st.markdown("### 📤 Export Jadwal")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            text_export = export_to_text(itinerary, start_date)
            st.download_button(
                "📄 Download TXT",
                data=text_export,
                file_name=f"jadwal_umrah_{start_date.strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            wa_export = export_to_whatsapp(itinerary, start_date)
            st.download_button(
                "📱 Format WhatsApp",
                data=wa_export,
                file_name=f"jadwal_umrah_wa_{start_date.strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            json_export = json.dumps(itinerary, indent=2, default=str)
            st.download_button(
                "💾 Download JSON",
                data=json_export,
                file_name=f"jadwal_umrah_{start_date.strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.divider()
        
        # Day by day schedule
        st.markdown("### 📋 Jadwal Harian")
        
        # Day selector
        day_options = [f"Hari {d['day']}: {d['location']}" for d in itinerary]
        
        view_mode = st.radio(
            "Tampilan:",
            ["📑 Semua Hari", "🔍 Per Hari"],
            horizontal=True
        )
        
        if view_mode == "📑 Semua Hari":
            for day in itinerary:
                day_date = start_date + timedelta(days=day["day"] - 1)
                render_day_schedule(day, day_date)
        else:
            selected_day = st.selectbox("Pilih Hari:", day_options)
            day_idx = day_options.index(selected_day)
            day = itinerary[day_idx]
            day_date = start_date + timedelta(days=day["day"] - 1)
            render_day_schedule(day, day_date)
        
        st.divider()
        
        # Tips
        render_tips()
        
        # Reset button
        st.divider()
        if st.button("🔄 Buat Jadwal Baru", use_container_width=True):
            st.session_state.itinerary_generated = False
            st.session_state.current_itinerary = None
            st.rerun()
    
    # DYOR Disclaimer
    st.divider()
    st.warning("""
    ⚠️ **DYOR - Do Your Own Research**
    
    Jadwal ini bersifat **estimasi** dan dibuat otomatis oleh AI. 
    Waktu sholat, durasi aktivitas, dan kondisi di lapangan dapat berbeda.
    
    Selalu sesuaikan dengan:
    - Kondisi fisik & kesehatan Anda
    - Jarak hotel ke Masjidil Haram / Masjid Nabawi
    - Musim & cuaca saat berkunjung
    - Jadwal penerbangan aktual
    
    **LABBAIK.AI tidak bertanggung jawab atas perubahan jadwal di lapangan.**
    """)


# =============================================================================
# EXPORT
# =============================================================================

__all__ = ["render_itinerary_builder_page"]
