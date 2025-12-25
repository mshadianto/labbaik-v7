"""
================================================================================
📋 LABBAIK AI - SMART CHECKLIST
================================================================================
Lokasi: ui/pages/smart_checklist.py (atau features/smart_checklist.py)
Fitur: Checklist packing & persiapan Umrah yang dipersonalisasi
================================================================================
"""

import streamlit as st
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional
import json

# =============================================================================
# 🎨 STYLING
# =============================================================================

CHECKLIST_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');

.checklist-hero {
    background: linear-gradient(135deg, #1a2a1a 0%, #2d4a2d 50%, #1a3a1a 100%);
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 1.5rem;
    border: 1px solid #4ade80;
}

.checklist-hero h1 {
    color: #4ade80;
    margin: 0;
    font-size: 2rem;
}

.checklist-hero .subtitle {
    color: #888;
    font-size: 1rem;
}

.category-card {
    background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%);
    border-radius: 15px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-left: 4px solid #4ade80;
}

.category-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.category-title {
    color: #4ade80;
    font-size: 1.2rem;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.category-progress {
    color: #888;
    font-size: 0.9rem;
}

.item-row {
    display: flex;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #333;
}

.item-row:last-child {
    border-bottom: none;
}

.item-priority {
    font-size: 0.7rem;
    padding: 0.15rem 0.5rem;
    border-radius: 10px;
    margin-left: auto;
}

.priority-wajib { background: #4a1a1a; color: #f87171; }
.priority-penting { background: #4a3a1a; color: #fbbf24; }
.priority-opsional { background: #1a3a4a; color: #60a5fa; }

.progress-ring {
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%);
    border-radius: 15px;
    border: 1px solid #4ade80;
}

.progress-number {
    font-size: 3rem;
    font-weight: bold;
    color: #4ade80;
}

.progress-label {
    color: #888;
    font-size: 0.9rem;
}

.tip-card {
    background: linear-gradient(135deg, #2d1a0d 0%, #4d3319 100%);
    border: 1px solid #d4af37;
    border-radius: 15px;
    padding: 1rem;
    margin: 0.5rem 0;
}

.warning-card {
    background: linear-gradient(135deg, #4a1a1a 0%, #3d1515 100%);
    border: 1px solid #f87171;
    border-radius: 15px;
    padding: 1rem;
    margin: 0.5rem 0;
}

.share-box {
    background: linear-gradient(135deg, #1a3a1a 0%, #2d4a2d 100%);
    border: 1px solid #4ade80;
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
}
</style>
"""

# =============================================================================
# 📊 CHECKLIST DATA
# =============================================================================

# Priority levels
PRIORITY = {
    "wajib": {"label": "WAJIB", "color": "#f87171", "class": "priority-wajib"},
    "penting": {"label": "Penting", "color": "#fbbf24", "class": "priority-penting"},
    "opsional": {"label": "Opsional", "color": "#60a5fa", "class": "priority-opsional"},
}

# Master checklist data
CHECKLIST_DATA = {
    "dokumen": {
        "title": "📄 Dokumen Penting",
        "icon": "📄",
        "color": "#f87171",
        "items": [
            {"id": "paspor", "name": "Paspor (masa aktif >6 bulan)", "priority": "wajib", "gender": "all"},
            {"id": "visa", "name": "Visa Umrah / E-Tourist", "priority": "wajib", "gender": "all"},
            {"id": "tiket", "name": "Tiket Pesawat (print & digital)", "priority": "wajib", "gender": "all"},
            {"id": "hotel", "name": "Bukti Booking Hotel", "priority": "wajib", "gender": "all"},
            {"id": "foto", "name": "Pas Foto 4x6 (5 lembar)", "priority": "wajib", "gender": "all"},
            {"id": "ktp", "name": "Fotokopi KTP", "priority": "penting", "gender": "all"},
            {"id": "kk", "name": "Fotokopi Kartu Keluarga", "priority": "penting", "gender": "all"},
            {"id": "vaksin", "name": "Sertifikat Vaksin Meningitis", "priority": "wajib", "gender": "all"},
            {"id": "asuransi", "name": "Kartu Asuransi Perjalanan", "priority": "penting", "gender": "all"},
            {"id": "surat_mahram", "name": "Surat Izin Mahram (wanita <45 thn)", "priority": "wajib", "gender": "female"},
            {"id": "buku_nikah", "name": "Fotokopi Buku Nikah", "priority": "penting", "gender": "female"},
            {"id": "itinerary", "name": "Jadwal Perjalanan (Itinerary)", "priority": "penting", "gender": "all"},
        ]
    },
    "pakaian_pria": {
        "title": "👔 Pakaian (Pria)",
        "icon": "👔",
        "color": "#60a5fa",
        "gender": "male",
        "items": [
            {"id": "ihram_set", "name": "Kain Ihram (2 set)", "priority": "wajib", "gender": "male"},
            {"id": "sabuk_ihram", "name": "Sabuk/Ikat Pinggang Ihram", "priority": "penting", "gender": "male"},
            {"id": "sandal", "name": "Sandal Jepit (2 pasang)", "priority": "wajib", "gender": "male"},
            {"id": "baju_harian", "name": "Baju Harian (sesuai durasi)", "priority": "wajib", "gender": "male"},
            {"id": "celana", "name": "Celana Panjang (3-5)", "priority": "wajib", "gender": "male"},
            {"id": "kaos_dalam", "name": "Kaos Dalam (5-7)", "priority": "wajib", "gender": "male"},
            {"id": "sarung", "name": "Sarung (2-3)", "priority": "penting", "gender": "male"},
            {"id": "peci", "name": "Peci/Kopiah (2-3)", "priority": "penting", "gender": "male"},
            {"id": "jaket", "name": "Jaket/Sweater (AC masjid dingin)", "priority": "penting", "gender": "male"},
            {"id": "handuk", "name": "Handuk (2)", "priority": "wajib", "gender": "male"},
        ]
    },
    "pakaian_wanita": {
        "title": "👗 Pakaian (Wanita)",
        "icon": "👗",
        "color": "#f472b6",
        "gender": "female",
        "items": [
            {"id": "mukena", "name": "Mukena (2-3 set)", "priority": "wajib", "gender": "female"},
            {"id": "hijab", "name": "Hijab/Kerudung (5-7)", "priority": "wajib", "gender": "female"},
            {"id": "gamis", "name": "Gamis/Abaya (3-5)", "priority": "wajib", "gender": "female"},
            {"id": "kaos_kaki", "name": "Kaos Kaki (5-7 pasang)", "priority": "wajib", "gender": "female"},
            {"id": "sandal_w", "name": "Sandal Nyaman (2 pasang)", "priority": "wajib", "gender": "female"},
            {"id": "dalaman", "name": "Dalaman/Manset (5-7)", "priority": "wajib", "gender": "female"},
            {"id": "ciput", "name": "Ciput/Inner Hijab (5)", "priority": "penting", "gender": "female"},
            {"id": "jaket_w", "name": "Cardigan/Jaket (AC dingin)", "priority": "penting", "gender": "female"},
            {"id": "handuk_w", "name": "Handuk (2)", "priority": "wajib", "gender": "female"},
            {"id": "peniti", "name": "Peniti/Bros Hijab", "priority": "penting", "gender": "female"},
        ]
    },
    "ibadah": {
        "title": "📿 Perlengkapan Ibadah",
        "icon": "📿",
        "color": "#4ade80",
        "items": [
            {"id": "quran", "name": "Al-Quran Kecil", "priority": "wajib", "gender": "all"},
            {"id": "buku_doa", "name": "Buku Doa & Dzikir Umrah", "priority": "wajib", "gender": "all"},
            {"id": "tasbih", "name": "Tasbih", "priority": "penting", "gender": "all"},
            {"id": "sajadah", "name": "Sajadah Travel (lipat)", "priority": "opsional", "gender": "all"},
            {"id": "buku_manasik", "name": "Buku Panduan Manasik", "priority": "penting", "gender": "all"},
            {"id": "counter", "name": "Alat Hitung Thawaf (digital/manual)", "priority": "penting", "gender": "all"},
        ]
    },
    "kesehatan": {
        "title": "💊 Obat & Kesehatan",
        "icon": "💊",
        "color": "#f87171",
        "items": [
            {"id": "obat_rutin", "name": "Obat Rutin Pribadi", "priority": "wajib", "gender": "all"},
            {"id": "paracetamol", "name": "Paracetamol/Panadol", "priority": "wajib", "gender": "all"},
            {"id": "obat_maag", "name": "Obat Maag (Promag/Mylanta)", "priority": "penting", "gender": "all"},
            {"id": "obat_diare", "name": "Obat Diare (Diapet/Entrostop)", "priority": "wajib", "gender": "all"},
            {"id": "obat_flu", "name": "Obat Flu & Batuk", "priority": "penting", "gender": "all"},
            {"id": "vitamin", "name": "Vitamin C & Multivitamin", "priority": "penting", "gender": "all"},
            {"id": "minyak_angin", "name": "Minyak Angin/Kayu Putih", "priority": "penting", "gender": "all"},
            {"id": "plester", "name": "Plester & Betadine", "priority": "penting", "gender": "all"},
            {"id": "masker", "name": "Masker (N95 recommended)", "priority": "wajib", "gender": "all"},
            {"id": "hand_sanitizer", "name": "Hand Sanitizer", "priority": "wajib", "gender": "all"},
            {"id": "sunblock", "name": "Sunblock/Sunscreen SPF50", "priority": "penting", "gender": "all"},
            {"id": "koyo", "name": "Koyo untuk Pegal", "priority": "opsional", "gender": "all"},
            {"id": "obat_haid", "name": "Obat Penunda Haid (konsul dokter)", "priority": "penting", "gender": "female"},
            {"id": "pembalut", "name": "Pembalut/Pantyliner", "priority": "wajib", "gender": "female"},
        ]
    },
    "toiletries": {
        "title": "🧴 Toiletries",
        "icon": "🧴",
        "color": "#60a5fa",
        "items": [
            {"id": "sabun", "name": "Sabun Mandi (travel size)", "priority": "wajib", "gender": "all"},
            {"id": "shampoo", "name": "Shampoo (travel size)", "priority": "wajib", "gender": "all"},
            {"id": "pasta_gigi", "name": "Pasta Gigi & Sikat Gigi", "priority": "wajib", "gender": "all"},
            {"id": "deodoran", "name": "Deodoran (NON-PARFUM saat ihram)", "priority": "penting", "gender": "all"},
            {"id": "lotion", "name": "Lotion/Pelembab (non-parfum)", "priority": "opsional", "gender": "all"},
            {"id": "sisir", "name": "Sisir", "priority": "penting", "gender": "all"},
            {"id": "gunting_kuku", "name": "Gunting Kuku", "priority": "penting", "gender": "all"},
            {"id": "tisu_basah", "name": "Tisu Basah & Kering", "priority": "wajib", "gender": "all"},
            {"id": "parfum", "name": "Parfum (HANYA setelah tahallul)", "priority": "opsional", "gender": "all"},
            {"id": "sabun_ihram", "name": "Sabun Khusus Ihram (non-parfum)", "priority": "penting", "gender": "all"},
        ]
    },
    "elektronik": {
        "title": "📱 Elektronik",
        "icon": "📱",
        "color": "#a78bfa",
        "items": [
            {"id": "hp", "name": "Handphone + Charger", "priority": "wajib", "gender": "all"},
            {"id": "powerbank", "name": "Powerbank (min 10000mAh)", "priority": "wajib", "gender": "all"},
            {"id": "adaptor", "name": "Adaptor Universal (Saudi: Type G)", "priority": "wajib", "gender": "all"},
            {"id": "kabel", "name": "Kabel Charger Cadangan", "priority": "penting", "gender": "all"},
            {"id": "earphone", "name": "Earphone/Headset", "priority": "penting", "gender": "all"},
            {"id": "kamera", "name": "Kamera/GoPro (opsional)", "priority": "opsional", "gender": "all"},
            {"id": "memory", "name": "Memory Card Cadangan", "priority": "opsional", "gender": "all"},
        ]
    },
    "uang": {
        "title": "💰 Uang & Finansial",
        "icon": "💰",
        "color": "#fbbf24",
        "items": [
            {"id": "riyal", "name": "Uang Saudi Riyal (SAR)", "priority": "wajib", "gender": "all"},
            {"id": "usd", "name": "Uang Dollar (cadangan)", "priority": "penting", "gender": "all"},
            {"id": "rupiah", "name": "Uang Rupiah (untuk di bandara)", "priority": "penting", "gender": "all"},
            {"id": "kartu_debit", "name": "Kartu Debit (pastikan aktif luar negeri)", "priority": "wajib", "gender": "all"},
            {"id": "kartu_kredit", "name": "Kartu Kredit (backup)", "priority": "penting", "gender": "all"},
            {"id": "dompet", "name": "Dompet/Money Belt", "priority": "wajib", "gender": "all"},
            {"id": "fotokopi_kartu", "name": "Fotokopi Kartu ATM/Kredit", "priority": "penting", "gender": "all"},
        ]
    },
    "tas": {
        "title": "🎒 Tas & Koper",
        "icon": "🎒",
        "color": "#f97316",
        "items": [
            {"id": "koper", "name": "Koper Besar (max 23kg)", "priority": "wajib", "gender": "all"},
            {"id": "tas_kabin", "name": "Tas Kabin/Backpack", "priority": "wajib", "gender": "all"},
            {"id": "tas_kecil", "name": "Tas Kecil untuk ke Masjid", "priority": "wajib", "gender": "all"},
            {"id": "tas_sandal", "name": "Tas Sandal (untuk di masjid)", "priority": "penting", "gender": "all"},
            {"id": "kunci_koper", "name": "Gembok Koper TSA", "priority": "penting", "gender": "all"},
            {"id": "luggage_tag", "name": "Luggage Tag/Label Koper", "priority": "penting", "gender": "all"},
            {"id": "plastik", "name": "Plastik Ziplock (berbagai ukuran)", "priority": "penting", "gender": "all"},
            {"id": "laundry_bag", "name": "Tas Laundry/Baju Kotor", "priority": "penting", "gender": "all"},
        ]
    },
    "lainnya": {
        "title": "🔧 Lain-lain",
        "icon": "🔧",
        "color": "#888",
        "items": [
            {"id": "payung", "name": "Payung Lipat", "priority": "penting", "gender": "all"},
            {"id": "botol_minum", "name": "Botol Minum (untuk Zamzam)", "priority": "wajib", "gender": "all"},
            {"id": "snack", "name": "Snack/Makanan Ringan", "priority": "opsional", "gender": "all"},
            {"id": "bantal_leher", "name": "Bantal Leher (untuk pesawat)", "priority": "opsional", "gender": "all"},
            {"id": "penutup_mata", "name": "Penutup Mata (sleep mask)", "priority": "opsional", "gender": "all"},
            {"id": "jam", "name": "Jam Tangan", "priority": "opsional", "gender": "all"},
            {"id": "kacamata", "name": "Kacamata/Sunglasses", "priority": "penting", "gender": "all"},
            {"id": "senter", "name": "Senter Kecil/Flashlight", "priority": "opsional", "gender": "all"},
            {"id": "oleh2", "name": "List Oleh-oleh (dari keluarga)", "priority": "opsional", "gender": "all"},
        ]
    },
    "apps": {
        "title": "📲 Aplikasi Wajib Download",
        "icon": "📲",
        "color": "#4ade80",
        "items": [
            {"id": "app_nusuk", "name": "NUSUK (Visa & Permit)", "priority": "wajib", "gender": "all"},
            {"id": "app_maps", "name": "Google Maps (download offline!)", "priority": "wajib", "gender": "all"},
            {"id": "app_careem", "name": "Careem (Taxi)", "priority": "wajib", "gender": "all"},
            {"id": "app_uber", "name": "Uber (alternatif)", "priority": "penting", "gender": "all"},
            {"id": "app_whatsapp", "name": "WhatsApp", "priority": "wajib", "gender": "all"},
            {"id": "app_translate", "name": "Google Translate (offline Arabic)", "priority": "penting", "gender": "all"},
            {"id": "app_muslim_pro", "name": "Muslim Pro (waktu sholat)", "priority": "penting", "gender": "all"},
            {"id": "app_grab", "name": "Grab (untuk di Indonesia)", "priority": "opsional", "gender": "all"},
        ]
    }
}

# Items that should be warned about (prohibited during Ihram)
IHRAM_PROHIBITED = [
    "parfum", "deodoran"  # if they contain fragrance
]

# Weather-specific additions
WEATHER_ITEMS = {
    "summer": [
        {"id": "topi", "name": "Topi/Payung (panas ekstrem)", "priority": "wajib", "gender": "all"},
        {"id": "cooling_towel", "name": "Cooling Towel", "priority": "penting", "gender": "all"},
    ],
    "winter": [
        {"id": "jaket_tebal", "name": "Jaket Tebal", "priority": "penting", "gender": "all"},
        {"id": "syal", "name": "Syal/Scarf", "priority": "penting", "gender": "all"},
    ],
    "ramadan": [
        {"id": "kurma", "name": "Kurma untuk Berbuka", "priority": "penting", "gender": "all"},
        {"id": "sahur_snack", "name": "Snack untuk Sahur", "priority": "penting", "gender": "all"},
    ]
}

# =============================================================================
# 🔧 SESSION STATE & HELPERS
# =============================================================================

def init_checklist_state():
    """Initialize checklist session state."""
    if "checklist_items" not in st.session_state:
        st.session_state.checklist_items = {}
    if "checklist_profile" not in st.session_state:
        st.session_state.checklist_profile = {
            "gender": "male",
            "duration": 9,
            "season": "normal",
            "health_conditions": []
        }

def get_filtered_checklist(gender: str, season: str) -> Dict:
    """Get checklist filtered by gender and season."""
    filtered = {}
    
    for cat_id, category in CHECKLIST_DATA.items():
        # Skip gender-specific categories
        if category.get("gender") and category["gender"] != gender:
            continue
        
        # Filter items by gender
        items = []
        for item in category["items"]:
            if item["gender"] == "all" or item["gender"] == gender:
                items.append(item)
        
        if items:
            filtered[cat_id] = {
                **category,
                "items": items
            }
    
    # Add weather-specific items
    if season in WEATHER_ITEMS:
        if "lainnya" in filtered:
            filtered["lainnya"]["items"].extend(WEATHER_ITEMS[season])
    
    return filtered

def calculate_progress(checklist: Dict, checked_items: Dict) -> tuple:
    """Calculate overall progress."""
    total = 0
    done = 0
    wajib_total = 0
    wajib_done = 0
    
    for cat_id, category in checklist.items():
        for item in category["items"]:
            total += 1
            if checked_items.get(item["id"]):
                done += 1
            
            if item["priority"] == "wajib":
                wajib_total += 1
                if checked_items.get(item["id"]):
                    wajib_done += 1
    
    return done, total, wajib_done, wajib_total

def export_to_text(checklist: Dict, checked_items: Dict, profile: Dict) -> str:
    """Export checklist to text format."""
    lines = []
    lines.append("=" * 50)
    lines.append("📋 CHECKLIST UMRAH - LABBAIK.AI")
    lines.append("=" * 50)
    lines.append(f"Durasi: {profile['duration']} hari")
    lines.append(f"Gender: {'Pria' if profile['gender'] == 'male' else 'Wanita'}")
    lines.append("")
    
    done, total, wajib_done, wajib_total = calculate_progress(checklist, checked_items)
    lines.append(f"Progress: {done}/{total} ({int(done/total*100) if total > 0 else 0}%)")
    lines.append(f"Item Wajib: {wajib_done}/{wajib_total}")
    lines.append("")
    lines.append("-" * 50)
    
    for cat_id, category in checklist.items():
        lines.append("")
        lines.append(f"{category['icon']} {category['title']}")
        lines.append("-" * 30)
        
        for item in category["items"]:
            check = "✅" if checked_items.get(item["id"]) else "⬜"
            priority = f"[{PRIORITY[item['priority']]['label']}]" if item["priority"] == "wajib" else ""
            lines.append(f"  {check} {item['name']} {priority}")
    
    lines.append("")
    lines.append("=" * 50)
    lines.append("Generated by LABBAIK.AI")
    lines.append("labbaik-umrahplanner.streamlit.app")
    lines.append("=" * 50)
    
    return "\n".join(lines)

def export_to_whatsapp(checklist: Dict, checked_items: Dict, profile: Dict) -> str:
    """Export checklist to WhatsApp format."""
    lines = []
    lines.append("📋 *CHECKLIST UMRAH*")
    lines.append(f"_Durasi: {profile['duration']} hari_")
    lines.append("")
    
    done, total, wajib_done, wajib_total = calculate_progress(checklist, checked_items)
    lines.append(f"✅ Progress: *{done}/{total}* ({int(done/total*100) if total > 0 else 0}%)")
    lines.append("")
    
    for cat_id, category in checklist.items():
        # Only show unchecked items
        unchecked = [item for item in category["items"] if not checked_items.get(item["id"])]
        if unchecked:
            lines.append(f"*{category['title']}*")
            for item in unchecked[:5]:  # Limit to 5 per category
                priority = "🔴" if item["priority"] == "wajib" else "🟡" if item["priority"] == "penting" else "🔵"
                lines.append(f"{priority} {item['name']}")
            if len(unchecked) > 5:
                lines.append(f"   _...dan {len(unchecked)-5} item lainnya_")
            lines.append("")
    
    lines.append("─" * 20)
    lines.append("🔗 labbaik-umrahplanner.streamlit.app")
    
    return "\n".join(lines)

# =============================================================================
# 🎨 UI COMPONENTS
# =============================================================================

def render_hero():
    """Render hero section."""
    st.markdown(CHECKLIST_CSS, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="checklist-hero">
        <h1>📋 Smart Checklist</h1>
        <p class="subtitle">Checklist Packing Umrah yang Dipersonalisasi</p>
    </div>
    """, unsafe_allow_html=True)

def render_profile_form():
    """Render profile configuration form."""
    with st.container(border=True):
        st.markdown("### ⚙️ Personalisasi Checklist")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            gender = st.selectbox(
                "👤 Jenis Kelamin",
                options=["male", "female"],
                format_func=lambda x: "Pria" if x == "male" else "Wanita",
                index=0 if st.session_state.checklist_profile["gender"] == "male" else 1
            )
            st.session_state.checklist_profile["gender"] = gender
        
        with col2:
            duration = st.slider(
                "📅 Durasi (hari)",
                min_value=7,
                max_value=21,
                value=st.session_state.checklist_profile["duration"]
            )
            st.session_state.checklist_profile["duration"] = duration
        
        with col3:
            season = st.selectbox(
                "🌡️ Musim/Kondisi",
                options=["normal", "summer", "winter", "ramadan"],
                format_func=lambda x: {
                    "normal": "Normal",
                    "summer": "Musim Panas (Jun-Sep)",
                    "winter": "Musim Dingin (Des-Feb)",
                    "ramadan": "Bulan Ramadan"
                }[x]
            )
            st.session_state.checklist_profile["season"] = season
        
        # Health conditions
        st.markdown("**🏥 Kondisi Kesehatan (opsional):**")
        health_cols = st.columns(4)
        health_options = ["Diabetes", "Hipertensi", "Asma", "Alergi"]
        
        conditions = []
        for i, condition in enumerate(health_options):
            with health_cols[i]:
                if st.checkbox(condition, key=f"health_{condition}"):
                    conditions.append(condition)
        st.session_state.checklist_profile["health_conditions"] = conditions

def render_progress_summary(checklist: Dict, checked_items: Dict):
    """Render progress summary."""
    done, total, wajib_done, wajib_total = calculate_progress(checklist, checked_items)
    
    pct = int(done / total * 100) if total > 0 else 0
    wajib_pct = int(wajib_done / wajib_total * 100) if wajib_total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="progress-ring">
            <div class="progress-number">{pct}%</div>
            <div class="progress-label">Total Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="progress-ring">
            <div class="progress-number">{done}/{total}</div>
            <div class="progress-label">Item Tercek</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = "#4ade80" if wajib_pct == 100 else "#f87171"
        st.markdown(f"""
        <div class="progress-ring" style="border-color:{color};">
            <div class="progress-number" style="color:{color};">{wajib_pct}%</div>
            <div class="progress-label">Item WAJIB</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        remaining = total - done
        st.markdown(f"""
        <div class="progress-ring">
            <div class="progress-number">{remaining}</div>
            <div class="progress-label">Sisa Item</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Warning if wajib items not complete
    if wajib_pct < 100:
        st.warning(f"⚠️ **{wajib_total - wajib_done} item WAJIB belum dicentang!** Pastikan semua item wajib sudah siap.")

def render_category_checklist(cat_id: str, category: Dict, checked_items: Dict):
    """Render a single category checklist."""
    items = category["items"]
    done_count = sum(1 for item in items if checked_items.get(item["id"]))
    
    with st.expander(f"{category['icon']} {category['title']} ({done_count}/{len(items)})", expanded=done_count < len(items)):
        # Progress bar
        pct = done_count / len(items) if items else 0
        st.progress(pct)
        
        # Items
        for item in items:
            col1, col2 = st.columns([4, 1])
            
            with col1:
                checked = st.checkbox(
                    item["name"],
                    value=checked_items.get(item["id"], False),
                    key=f"check_{item['id']}"
                )
                st.session_state.checklist_items[item["id"]] = checked
            
            with col2:
                priority = PRIORITY[item["priority"]]
                st.markdown(f"""
                <span class="item-priority {priority['class']}">{priority['label']}</span>
                """, unsafe_allow_html=True)
            
            # Special warnings
            if item["id"] in IHRAM_PROHIBITED and checked:
                st.caption("⚠️ Ingat: TIDAK boleh dipakai saat ihram!")

def render_tips():
    """Render packing tips."""
    st.markdown("### 💡 Tips Packing")
    
    tips = [
        ("🎒", "**Berat Koper:** Max 23kg untuk bagasi, 7kg untuk kabin"),
        ("📦", "**Pisahkan:** Taruh perlengkapan ihram di tas kabin"),
        ("🔒", "**Keamanan:** Gunakan gembok TSA untuk koper"),
        ("📱", "**Backup:** Foto semua dokumen, simpan di cloud"),
        ("💊", "**Obat:** Bawa resep dokter untuk obat-obatan"),
        ("🧴", "**Cairan:** Toiletries max 100ml untuk kabin"),
    ]
    
    cols = st.columns(2)
    for i, (icon, tip) in enumerate(tips):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="tip-card">
                {icon} {tip}
            </div>
            """, unsafe_allow_html=True)

def render_prohibited_items():
    """Render prohibited items warning."""
    st.markdown("### 🚫 Barang Terlarang")
    
    st.markdown("""
    <div class="warning-card">
        <strong>❌ JANGAN BAWA:</strong><br>
        • Narkoba & obat terlarang<br>
        • Alkohol<br>
        • Senjata tajam<br>
        • Buku/materi yang bertentangan dengan Islam<br>
        • Makanan dari babi<br>
        • E-cigarette/Vape (ilegal di Saudi)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-card">
        <strong>⚠️ SAAT IHRAM DILARANG:</strong><br>
        • Parfum/wewangian<br>
        • Menutup kepala (pria)<br>
        • Pakaian berjahit (pria)<br>
        • Memotong kuku & rambut<br>
        • Berburu & membunuh binatang
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# 🚀 MAIN PAGE FUNCTION
# =============================================================================

def render_smart_checklist_page():
    """Main entry point for Smart Checklist page."""
    
    # Initialize state
    init_checklist_state()
    
    # Render hero
    render_hero()
    
    # Profile form
    render_profile_form()
    
    st.divider()
    
    # Get filtered checklist
    profile = st.session_state.checklist_profile
    checklist = get_filtered_checklist(profile["gender"], profile["season"])
    checked_items = st.session_state.checklist_items
    
    # Progress summary
    render_progress_summary(checklist, checked_items)
    
    st.divider()
    
    # Export buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        text_export = export_to_text(checklist, checked_items, profile)
        st.download_button(
            "📄 Download TXT",
            data=text_export,
            file_name="checklist_umrah.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        wa_export = export_to_whatsapp(checklist, checked_items, profile)
        st.download_button(
            "📱 Format WhatsApp",
            data=wa_export,
            file_name="checklist_umrah_wa.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        json_export = json.dumps({
            "profile": profile,
            "checked_items": checked_items,
            "timestamp": datetime.now().isoformat()
        }, indent=2)
        st.download_button(
            "💾 Backup JSON",
            data=json_export,
            file_name="checklist_backup.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col4:
        if st.button("🔄 Reset Semua", use_container_width=True):
            st.session_state.checklist_items = {}
            st.rerun()
    
    st.divider()
    
    # Main checklist
    st.markdown("### ✅ Checklist Item")
    
    # Quick filter
    filter_option = st.radio(
        "Filter:",
        ["📋 Semua", "🔴 Wajib Saja", "⬜ Belum Dicentang"],
        horizontal=True
    )
    
    # Render categories
    for cat_id, category in checklist.items():
        # Apply filter
        if filter_option == "🔴 Wajib Saja":
            category = {
                **category,
                "items": [i for i in category["items"] if i["priority"] == "wajib"]
            }
        elif filter_option == "⬜ Belum Dicentang":
            category = {
                **category,
                "items": [i for i in category["items"] if not checked_items.get(i["id"])]
            }
        
        if category["items"]:
            render_category_checklist(cat_id, category, checked_items)
    
    st.divider()
    
    # Tips & Warnings
    col1, col2 = st.columns(2)
    
    with col1:
        render_tips()
    
    with col2:
        render_prohibited_items()
    
    # Share box
    st.divider()
    done, total, _, _ = calculate_progress(checklist, checked_items)
    pct = int(done / total * 100) if total > 0 else 0
    
    st.markdown(f"""
    <div class="share-box">
        <h3 style="color:#4ade80;margin-top:0;">📤 Bagikan Progress Anda!</h3>
        <p style="color:#888;">Progress packing: <strong>{pct}%</strong> ({done}/{total} item)</p>
        <p style="color:#666;font-size:0.85rem;">
            Screenshot dan share ke grup WhatsApp keluarga! 📱
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # DYOR
    st.divider()
    st.warning("""
    ⚠️ **DYOR - Do Your Own Research**
    
    Checklist ini bersifat panduan umum. Sesuaikan dengan:
    - Kebutuhan pribadi Anda
    - Kondisi kesehatan
    - Aturan maskapai penerbangan
    - Regulasi terbaru Saudi Arabia
    
    **LABBAIK.AI tidak bertanggung jawab atas barang yang tertinggal.**
    """)


# =============================================================================
# EXPORT
# =============================================================================

__all__ = ["render_smart_checklist_page"]
