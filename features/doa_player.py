"""
LABBAIK AI v6.0 - Voice Doa Player
===================================
Audio playback for Umrah duas with:
- Arabic text with proper RTL display
- Latin transliteration
- Indonesian translation
- Audio playback (TTS or pre-recorded)
- Bookmark/favorites system

Uses Web Speech API for TTS when audio files not available.
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json

# =============================================================================
# DOA DATABASE
# =============================================================================

@dataclass
class Doa:
    """Doa/prayer data structure."""
    id: str
    name: str
    arabic: str
    latin: str
    translation: str
    category: str
    when_to_read: str
    audio_url: str = ""  # Optional audio file URL
    is_wajib: bool = False


class DoaCategory(str, Enum):
    PERJALANAN = "perjalanan"
    IHRAM = "ihram"
    TAWAF = "tawaf"
    SAI = "sai"
    MASJID = "masjid"
    HARIAN = "harian"
    ZIARAH = "ziarah"


# Complete Umrah Doa Database
UMRAH_DOAS: List[Doa] = [
    # PERJALANAN
    Doa(
        id="doa_001",
        name="Doa Keluar Rumah",
        arabic="بِسْمِ اللهِ تَوَكَّلْتُ عَلَى اللهِ وَلاَ حَوْلَ وَلاَ قُوَّةَ إِلاَّ بِاللهِ",
        latin="Bismillahi tawakkaltu 'alallah, wa laa hawla wa laa quwwata illa billah",
        translation="Dengan nama Allah, aku bertawakal kepada Allah. Tidak ada daya dan kekuatan kecuali dengan pertolongan Allah.",
        category=DoaCategory.PERJALANAN,
        when_to_read="Saat keluar rumah menuju bandara"
    ),
    Doa(
        id="doa_002",
        name="Doa Naik Kendaraan",
        arabic="سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ وَإِنَّا إِلَى رَبِّنَا لَمُنْقَلِبُونَ",
        latin="Subhanalladzi sakhkhara lana hadza wa ma kunna lahu muqrinin, wa inna ila rabbina lamunqalibun",
        translation="Maha Suci Allah yang telah menundukkan ini untuk kami, padahal kami tidak mampu menguasainya. Dan sesungguhnya kami akan kembali kepada Tuhan kami.",
        category=DoaCategory.PERJALANAN,
        when_to_read="Saat naik pesawat/kendaraan"
    ),
    Doa(
        id="doa_003",
        name="Doa Safar (Perjalanan)",
        arabic="اللَّهُمَّ إِنَّا نَسْأَلُكَ فِي سَفَرِنَا هَذَا الْبِرَّ وَالتَّقْوَى وَمِنَ الْعَمَلِ مَا تَرْضَى",
        latin="Allahumma inna nas'aluka fi safarina hadzal birra wat-taqwa, wa minal 'amali ma tardha",
        translation="Ya Allah, kami memohon kepada-Mu dalam perjalanan kami ini kebaikan dan takwa, serta amal yang Engkau ridhai.",
        category=DoaCategory.PERJALANAN,
        when_to_read="Saat memulai perjalanan"
    ),
    
    # IHRAM
    Doa(
        id="doa_010",
        name="Niat Ihram Umrah",
        arabic="لَبَّيْكَ اللَّهُمَّ عُمْرَةً",
        latin="Labbaika Allahumma 'Umratan",
        translation="Aku penuhi panggilan-Mu ya Allah untuk melaksanakan umrah.",
        category=DoaCategory.IHRAM,
        when_to_read="Saat niat ihram di miqat",
        is_wajib=True
    ),
    Doa(
        id="doa_011",
        name="Talbiyah",
        arabic="لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لَا شَرِيكَ لَكَ",
        latin="Labbaik Allahumma labbaik, labbaika laa syariika laka labbaik. Innal hamda wan ni'mata laka wal mulk, laa syariika lak",
        translation="Aku memenuhi panggilan-Mu ya Allah, aku memenuhi panggilan-Mu. Aku memenuhi panggilan-Mu, tidak ada sekutu bagi-Mu, aku memenuhi panggilan-Mu. Sesungguhnya segala puji, nikmat, dan kerajaan adalah milik-Mu. Tidak ada sekutu bagi-Mu.",
        category=DoaCategory.IHRAM,
        when_to_read="Sepanjang perjalanan menuju Makkah",
        is_wajib=True
    ),
    
    # TAWAF
    Doa(
        id="doa_020",
        name="Doa Melihat Ka'bah",
        arabic="اللَّهُمَّ زِدْ هَذَا الْبَيْتَ تَشْرِيفًا وَتَعْظِيمًا وَتَكْرِيمًا وَمَهَابَةً",
        latin="Allahumma zid hadzal baita tasyrifan wa ta'zhiman wa takriman wa mahabah",
        translation="Ya Allah, tambahkanlah kemuliaan, keagungan, kehormatan, dan kewibawaan rumah ini.",
        category=DoaCategory.TAWAF,
        when_to_read="Pertama kali melihat Ka'bah"
    ),
    Doa(
        id="doa_021",
        name="Doa di Hajar Aswad (Istilam)",
        arabic="بِسْمِ اللهِ وَاللهُ أَكْبَرُ",
        latin="Bismillahi wallahu akbar",
        translation="Dengan nama Allah, Allah Maha Besar.",
        category=DoaCategory.TAWAF,
        when_to_read="Saat menghadap/menyentuh Hajar Aswad",
        is_wajib=True
    ),
    Doa(
        id="doa_022",
        name="Doa Antara Rukun Yamani dan Hajar Aswad",
        arabic="رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ",
        latin="Rabbana atina fid-dunya hasanah, wa fil akhirati hasanah, wa qina 'adzaban-nar",
        translation="Ya Tuhan kami, berilah kami kebaikan di dunia dan kebaikan di akhirat, dan lindungilah kami dari siksa api neraka.",
        category=DoaCategory.TAWAF,
        when_to_read="Antara Rukun Yamani dan Hajar Aswad (setiap putaran)",
        is_wajib=True
    ),
    Doa(
        id="doa_023",
        name="Doa Setelah Tawaf",
        arabic="اللَّهُمَّ إِنِّي أَسْأَلُكَ عِلْمًا نَافِعًا وَرِزْقًا طَيِّبًا وَعَمَلًا مُتَقَبَّلًا",
        latin="Allahumma inni as'aluka 'ilman nafi'an, wa rizqan thayyiban, wa 'amalan mutaqabbalan",
        translation="Ya Allah, aku memohon kepada-Mu ilmu yang bermanfaat, rizki yang halal, dan amal yang diterima.",
        category=DoaCategory.TAWAF,
        when_to_read="Setelah selesai tawaf, saat minum air zamzam"
    ),
    
    # SAI
    Doa(
        id="doa_030",
        name="Doa di Bukit Shafa",
        arabic="إِنَّ الصَّفَا وَالْمَرْوَةَ مِنْ شَعَائِرِ اللهِ",
        latin="Innas-shafa wal marwata min sya'a'irillah",
        translation="Sesungguhnya Shafa dan Marwah adalah sebagian dari syiar-syiar Allah.",
        category=DoaCategory.SAI,
        when_to_read="Saat naik ke bukit Shafa (pertama kali saja)",
        is_wajib=True
    ),
    Doa(
        id="doa_031",
        name="Doa di Shafa dan Marwah",
        arabic="اللهُ أَكْبَرُ اللهُ أَكْبَرُ اللهُ أَكْبَرُ، لَا إِلَهَ إِلَّا اللهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ",
        latin="Allahu akbar, Allahu akbar, Allahu akbar. Laa ilaha illallahu wahdahu laa syarika lah, lahul mulku wa lahul hamdu wa huwa 'ala kulli syai'in qadir",
        translation="Allah Maha Besar (3x). Tidak ada Tuhan selain Allah Yang Maha Esa, tidak ada sekutu bagi-Nya. Milik-Nya kerajaan dan pujian, dan Dia Maha Kuasa atas segala sesuatu.",
        category=DoaCategory.SAI,
        when_to_read="Di atas bukit Shafa dan Marwah"
    ),
    
    # MASJID
    Doa(
        id="doa_040",
        name="Doa Masuk Masjid",
        arabic="اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ",
        latin="Allahummaf-tah li abwaba rahmatik",
        translation="Ya Allah, bukakanlah untukku pintu-pintu rahmat-Mu.",
        category=DoaCategory.MASJID,
        when_to_read="Saat masuk Masjidil Haram/Nabawi"
    ),
    Doa(
        id="doa_041",
        name="Doa Keluar Masjid",
        arabic="اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ",
        latin="Allahumma inni as'aluka min fadlik",
        translation="Ya Allah, aku memohon karunia-Mu.",
        category=DoaCategory.MASJID,
        when_to_read="Saat keluar dari masjid"
    ),
    
    # HARIAN
    Doa(
        id="doa_050",
        name="Doa Sebelum Makan",
        arabic="بِسْمِ اللهِ وَعَلَى بَرَكَةِ اللهِ",
        latin="Bismillahi wa 'ala barakatillah",
        translation="Dengan nama Allah dan dengan berkah Allah.",
        category=DoaCategory.HARIAN,
        when_to_read="Sebelum makan"
    ),
    Doa(
        id="doa_051",
        name="Doa Setelah Makan",
        arabic="الْحَمْدُ لِلهِ الَّذِي أَطْعَمَنَا وَسَقَانَا وَجَعَلَنَا مُسْلِمِينَ",
        latin="Alhamdulillahilladzi ath'amana wa saqana wa ja'alana muslimin",
        translation="Segala puji bagi Allah yang telah memberi kami makan dan minum, serta menjadikan kami orang-orang muslim.",
        category=DoaCategory.HARIAN,
        when_to_read="Setelah makan"
    ),
    Doa(
        id="doa_052",
        name="Doa Sebelum Tidur",
        arabic="بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا",
        latin="Bismika Allahumma amutu wa ahya",
        translation="Dengan nama-Mu ya Allah, aku mati dan aku hidup.",
        category=DoaCategory.HARIAN,
        when_to_read="Sebelum tidur"
    ),
    Doa(
        id="doa_053",
        name="Doa Bangun Tidur",
        arabic="الْحَمْدُ لِلهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ",
        latin="Alhamdulillahilladzi ahyana ba'da ma amatana wa ilaihin-nusyur",
        translation="Segala puji bagi Allah yang telah menghidupkan kami setelah mematikan kami, dan kepada-Nya kami dibangkitkan.",
        category=DoaCategory.HARIAN,
        when_to_read="Setelah bangun tidur"
    ),
    
    # ZIARAH
    Doa(
        id="doa_060",
        name="Salam di Makam Rasulullah",
        arabic="السَّلَامُ عَلَيْكَ يَا رَسُولَ اللهِ، السَّلَامُ عَلَيْكَ يَا نَبِيَّ اللهِ، السَّلَامُ عَلَيْكَ يَا خَيْرَ خَلْقِ اللهِ",
        latin="Assalamu 'alaika ya Rasulallah, assalamu 'alaika ya Nabiyyallah, assalamu 'alaika ya khaira khalqillah",
        translation="Salam sejahtera atasmu wahai Rasulullah, salam sejahtera atasmu wahai Nabi Allah, salam sejahtera atasmu wahai sebaik-baik makhluk Allah.",
        category=DoaCategory.ZIARAH,
        when_to_read="Di depan makam Rasulullah SAW"
    ),
    Doa(
        id="doa_061",
        name="Doa Setelah Umrah",
        arabic="الْحَمْدُ لِلَّهِ الَّذِي بِنِعْمَتِهِ تَتِمُّ الصَّالِحَاتُ",
        latin="Alhamdulillahilladzi bini'matihi tatimmus-shalihat",
        translation="Segala puji bagi Allah yang dengan nikmat-Nya sempurnalah segala amal shalih.",
        category=DoaCategory.ZIARAH,
        when_to_read="Setelah selesai umrah (tahallul)"
    ),
]


# =============================================================================
# TTS COMPONENT (Web Speech API)
# =============================================================================

TTS_HTML_TEMPLATE = """
<div id="doa-player-{doa_id}" style="background: linear-gradient(135deg, #1a1a1a, #2d2d2d); padding: 1.5rem; border-radius: 15px; border: 1px solid #d4af37; margin-bottom: 1rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <div>
            <h3 style="color: #d4af37; margin: 0;">{name}</h3>
            <span style="color: #888; font-size: 0.85rem;">{category} • {when_to_read}</span>
        </div>
        <div style="display: flex; gap: 0.5rem;">
            {wajib_badge}
            <button onclick="speakArabic_{doa_id}()" style="background: #d4af37; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-size: 1rem;">
                🔊 Play
            </button>
        </div>
    </div>
    
    <div style="background: #0a0a0a; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <div style="direction: rtl; text-align: right; font-family: 'Traditional Arabic', 'Amiri', serif; font-size: 1.8rem; line-height: 2; color: #d4af37;">
            {arabic}
        </div>
    </div>
    
    <div style="color: #888; font-style: italic; margin-bottom: 0.5rem;">
        {latin}
    </div>
    
    <div style="color: white;">
        {translation}
    </div>
</div>

<script>
function speakArabic_{doa_id}() {{
    const text = `{arabic}`;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ar-SA';
    utterance.rate = 0.8;
    window.speechSynthesis.speak(utterance);
}}
</script>
"""


# =============================================================================
# RENDER FUNCTIONS
# =============================================================================

def render_doa_card(doa: Doa, show_audio: bool = True):
    """Render a single doa card with audio player."""
    
    wajib_badge = ""
    if doa.is_wajib:
        wajib_badge = '<span style="background: #ef4444; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.75rem;">WAJIB</span>'
    
    # Use Streamlit components instead of raw HTML for better compatibility
    with st.container():
        # Header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {doa.name}")
            st.caption(f"{doa.category.value.title()} • {doa.when_to_read}")
        
        with col2:
            if doa.is_wajib:
                st.error("WAJIB", icon="⚠️")
        
        # Arabic text
        st.markdown(f"""
        <div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border: 1px solid #333;">
            <div style="direction: rtl; text-align: right; font-family: 'Traditional Arabic', 'Amiri', serif; font-size: 1.8rem; line-height: 2.2; color: #d4af37;">
                {doa.arabic}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Latin & Translation
        st.markdown(f"*{doa.latin}*")
        st.markdown(f"**Artinya:** {doa.translation}")
        
        # Audio controls
        if show_audio:
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("🔊 Play", key=f"play_{doa.id}"):
                    # Trigger TTS via JavaScript
                    st.components.v1.html(f"""
                    <script>
                        const text = `{doa.arabic}`;
                        const utterance = new SpeechSynthesisUtterance(text);
                        utterance.lang = 'ar-SA';
                        utterance.rate = 0.7;
                        window.speechSynthesis.speak(utterance);
                    </script>
                    """, height=0)
                    st.toast("🔊 Memutar doa...", icon="🕋")
            
            with col2:
                # Bookmark button
                bookmarks = st.session_state.get("doa_bookmarks", set())
                is_bookmarked = doa.id in bookmarks
                
                if st.button(
                    "❤️" if is_bookmarked else "🤍",
                    key=f"bookmark_{doa.id}"
                ):
                    if is_bookmarked:
                        bookmarks.discard(doa.id)
                        st.toast("Dihapus dari favorit")
                    else:
                        bookmarks.add(doa.id)
                        st.toast("Ditambahkan ke favorit!")
                    st.session_state.doa_bookmarks = bookmarks
        
        st.divider()


def render_doa_list(category: DoaCategory = None, wajib_only: bool = False):
    """Render list of duas filtered by category."""
    
    # Filter doas
    doas = UMRAH_DOAS
    
    if category:
        doas = [d for d in doas if d.category == category]
    
    if wajib_only:
        doas = [d for d in doas if d.is_wajib]
    
    if not doas:
        st.info("Tidak ada doa dalam kategori ini")
        return
    
    for doa in doas:
        render_doa_card(doa)


def render_doa_player_page():
    """Full doa player page."""
    
    st.markdown("# 🤲 Doa & Dzikir Umrah")
    st.caption("Kumpulan doa lengkap untuk perjalanan umrah")
    
    # Initialize bookmarks
    if "doa_bookmarks" not in st.session_state:
        st.session_state.doa_bookmarks = set()
    
    # Category filter
    col1, col2 = st.columns([2, 1])
    
    with col1:
        categories = ["Semua"] + [c.value.title() for c in DoaCategory]
        selected = st.selectbox("📂 Kategori", categories)
    
    with col2:
        wajib_only = st.checkbox("⚠️ Hanya Wajib")
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📖 Semua Doa", "❤️ Favorit", "📋 Quick Reference"])
    
    with tab1:
        if selected == "Semua":
            render_doa_list(wajib_only=wajib_only)
        else:
            # Convert back to enum
            category_map = {c.value.title(): c for c in DoaCategory}
            category = category_map.get(selected)
            render_doa_list(category=category, wajib_only=wajib_only)
    
    with tab2:
        bookmarks = st.session_state.get("doa_bookmarks", set())
        
        if bookmarks:
            bookmarked_doas = [d for d in UMRAH_DOAS if d.id in bookmarks]
            for doa in bookmarked_doas:
                render_doa_card(doa)
        else:
            st.info("Belum ada doa favorit. Tekan ❤️ untuk menambahkan.")
    
    with tab3:
        st.markdown("### 📋 Ringkasan Doa Wajib Umrah")
        
        wajib_doas = [d for d in UMRAH_DOAS if d.is_wajib]
        
        for i, doa in enumerate(wajib_doas, 1):
            st.markdown(f"""
            **{i}. {doa.name}** ({doa.category.value.title()})
            
            > *{doa.latin}*
            """)
        
        st.divider()
        
        st.markdown("### 🕋 Urutan Doa dalam Umrah")
        
        st.markdown("""
        1. **Niat Ihram** - Di Miqat
        2. **Talbiyah** - Sepanjang perjalanan ke Makkah
        3. **Doa Melihat Ka'bah** - Pertama kali melihat Ka'bah
        4. **Doa Istilam** - Di Hajar Aswad (setiap putaran)
        5. **Doa Tawaf** - Selama 7 putaran
        6. **Doa Minum Zamzam** - Setelah sholat tawaf
        7. **Doa Sa'i di Shafa** - Awal sa'i
        8. **Doa Sa'i** - 7 kali Shafa-Marwah
        9. **Doa Selesai Umrah** - Setelah tahallul
        """)


def render_doa_mini_widget():
    """Mini widget showing quick doa access."""
    
    wajib_count = sum(1 for d in UMRAH_DOAS if d.is_wajib)
    total_count = len(UMRAH_DOAS)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a1a, #2d2d2d); padding: 1rem; border-radius: 15px; border: 1px solid #d4af37;">
        <div style="color: #d4af37; font-size: 0.8rem;">🤲 Doa Umrah</div>
        <div style="color: white; font-weight: bold;">{wajib_count} Wajib / {total_count} Total</div>
        <div style="color: #888; font-size: 0.75rem;">Klik untuk buka player</div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [
    "Doa",
    "DoaCategory",
    "UMRAH_DOAS",
    "render_doa_card",
    "render_doa_list",
    "render_doa_player_page",
    "render_doa_mini_widget",
]
