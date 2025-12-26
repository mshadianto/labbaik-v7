"""
LABBAIK AI v7.0 - Complete Umrah Experience
============================================
Super enhanced Umrah feature combining guide + doa player + audio.
"""

import streamlit as st
from typing import List, Optional
import io

# Import from umrah_guide
from features.umrah_guide import (
    UMRAH_DEFINITION, UMRAH_VIRTUES, UMRAH_PILLARS, UMRAH_SUNNAHS,
    MIQAT_LOCATIONS, UMRAH_DOAS, HISTORICAL_SITES, UMRAH_PROCEDURES,
    Doa, DoaCategory, UmrahProcedure, Miqat, HistoricalSite
)

# TTS imports
try:
    import edge_tts
    import asyncio
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

# Voice options
VOICE_OPTIONS = {
    "pria": "ar-SA-HamedNeural",
    "wanita": "ar-SA-ZariyahNeural",
}


# =============================================================================
# AUDIO GENERATION
# =============================================================================

@st.cache_data(ttl=3600)
def generate_audio_edge(text: str, voice: str = "wanita") -> bytes:
    """Generate audio using Edge TTS."""
    if not HAS_EDGE_TTS:
        return None
    try:
        voice_id = VOICE_OPTIONS.get(voice, VOICE_OPTIONS["wanita"])
        async def _gen():
            comm = edge_tts.Communicate(text, voice_id, rate="-20%")
            buf = io.BytesIO()
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    buf.write(chunk["data"])
            buf.seek(0)
            return buf.read()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(_gen())
        loop.close()
        return result
    except:
        return None


@st.cache_data(ttl=3600)
def generate_audio_gtts(text: str) -> bytes:
    """Generate audio using gTTS."""
    if not HAS_GTTS:
        return None
    try:
        tts = gTTS(text=text, lang="ar", slow=True)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except:
        return None


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_doa_card_enhanced(doa: Doa, voice: str = "wanita", lang: str = "id"):
    """Render enhanced doa card with audio."""
    with st.container():
        # Header
        cols = st.columns([4, 1])
        with cols[0]:
            st.markdown(f"### {doa.name}")
            st.caption(f"{doa.category.value.title()} | {doa.when_to_read}")
        with cols[1]:
            if doa.is_wajib:
                st.error("WAJIB")

        # Arabic
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; border: 1px solid #d4af37;">
            <div style="direction: rtl; text-align: right; font-family: 'Amiri', serif; font-size: 1.8rem; line-height: 2.2; color: #d4af37;">
                {doa.arabic}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Audio
        if HAS_EDGE_TTS or HAS_GTTS:
            with st.expander("🔊 Putar Audio"):
                voice_col1, voice_col2 = st.columns(2)
                with voice_col1:
                    selected_voice = st.radio("Suara:", ["👩 Wanita", "👨 Pria"],
                                              horizontal=True, key=f"v_{doa.id}")
                voice = "pria" if "Pria" in selected_voice else "wanita"

                audio = generate_audio_edge(doa.arabic, voice) if HAS_EDGE_TTS else generate_audio_gtts(doa.arabic)
                if audio:
                    st.audio(audio, format="audio/mp3")

        # Latin
        st.markdown(f"**Latin:** *{doa.latin}*")

        # Translation
        trans = doa.translation_id if lang == "id" else doa.translation_en
        st.markdown(f"**Artinya:** {trans}")

        # Source
        if doa.source:
            st.caption(f"📚 {doa.source}")

        st.divider()


def render_umrah_step(proc: UmrahProcedure):
    """Render Umrah procedure step."""
    badge = ""
    if proc.is_pillar:
        badge = "🔴 RUKUN"
    elif proc.is_obligatory:
        badge = "🟡 WAJIB"

    with st.expander(f"**{proc.step}. {proc.name}** {badge}", expanded=False):
        st.markdown(f"**{proc.name_ar}**")
        st.markdown(proc.description)
        st.caption(f"📍 Lokasi: {proc.location}")

        if proc.tips:
            st.markdown("**💡 Tips:**")
            for tip in proc.tips:
                st.markdown(f"- {tip}")

        if proc.doas:
            st.markdown("**🤲 Doa terkait:**")
            for doa_id in proc.doas:
                doa = next((d for d in UMRAH_DOAS if d.id == doa_id), None)
                if doa:
                    st.info(f"**{doa.name}**: {doa.latin[:50]}...")

        if proc.sunnahs:
            st.markdown("**✨ Sunnah:**")
            for s in proc.sunnahs:
                st.markdown(f"- {s}")


def render_miqat_info(miqat: Miqat):
    """Render Miqat information."""
    st.markdown(f"""
    <div style="background: #1a1a2e; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #d4af37;">
        <h4 style="color: #d4af37; margin: 0;">{miqat.name}</h4>
        <p style="color: #888; margin: 0.3rem 0;">{miqat.name_ar}</p>
        <p style="color: white; margin: 0.5rem 0;">📍 {miqat.location}</p>
        <p style="color: #aaa; margin: 0;">Untuk: {miqat.for_travelers_from}</p>
        <p style="color: #888; font-size: 0.9rem;">Jarak ke Makkah: {miqat.distance_to_makkah}</p>
    </div>
    """, unsafe_allow_html=True)


def render_historical_site(site: HistoricalSite):
    """Render historical site."""
    city_color = "#d4af37" if site.city == "MAKKAH" else "#00d9ff"
    st.markdown(f"""
    <div style="background: #1a1a2e; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {city_color};">
        <div style="display: flex; justify-content: space-between;">
            <h4 style="color: {city_color}; margin: 0;">{site.name}</h4>
            <span style="color: #888;">{site.city}</span>
        </div>
        <p style="color: #888; margin: 0.3rem 0;">{site.name_ar}</p>
        <p style="color: white; margin: 0.5rem 0;">{site.description}</p>
        <p style="color: #aaa; font-style: italic;">✨ {site.significance}</p>
        <p style="color: #888; font-size: 0.85rem;">💡 {site.visiting_tips}</p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN PAGE
# =============================================================================

def render_umrah_complete_page():
    """Render the complete Umrah guide page."""

    st.markdown("# 🕋 Panduan Umrah Lengkap")
    st.caption("Berdasarkan Panduan Resmi Kementerian Haji dan Umrah Arab Saudi")

    # Initialize
    if "doa_bookmarks" not in st.session_state:
        st.session_state.doa_bookmarks = set()

    # Main tabs
    tabs = st.tabs([
        "📖 Panduan Umrah",
        "🤲 Koleksi Doa",
        "🗺️ Miqat",
        "🏛️ Tempat Bersejarah",
        "📚 Rukun & Sunnah"
    ])

    # === TAB 1: PANDUAN UMRAH ===
    with tabs[0]:
        st.markdown("## Apa itu Umrah?")
        st.info(UMRAH_DEFINITION["id"])

        st.markdown("### ✨ Keutamaan Umrah")
        for v in UMRAH_VIRTUES:
            st.markdown(f"- **{v['text_id']}**")
            st.caption(f"  📜 {v['hadith']}")

        st.divider()
        st.markdown("## 📋 Langkah-langkah Umrah")

        for proc in UMRAH_PROCEDURES:
            render_umrah_step(proc)

    # === TAB 2: KOLEKSI DOA ===
    with tabs[1]:
        st.markdown("## 🤲 Koleksi Doa Umrah")

        # Filter
        col1, col2 = st.columns([2, 1])
        with col1:
            categories = ["Semua"] + [c.value.title() for c in DoaCategory]
            selected_cat = st.selectbox("Kategori:", categories)
        with col2:
            wajib_only = st.checkbox("Hanya Wajib")

        # Filter doas
        doas = UMRAH_DOAS
        if selected_cat != "Semua":
            cat_map = {c.value.title(): c for c in DoaCategory}
            doas = [d for d in doas if d.category == cat_map.get(selected_cat)]
        if wajib_only:
            doas = [d for d in doas if d.is_wajib]

        st.caption(f"Menampilkan {len(doas)} doa")

        for doa in doas:
            render_doa_card_enhanced(doa)

    # === TAB 3: MIQAT ===
    with tabs[2]:
        st.markdown("## 🗺️ Lokasi Miqat")
        st.info("Miqat adalah batas tempat di mana jamaah harus memulai ihram sebelum memasuki Makkah.")

        for miqat in MIQAT_LOCATIONS:
            render_miqat_info(miqat)

    # === TAB 4: TEMPAT BERSEJARAH ===
    with tabs[3]:
        st.markdown("## 🏛️ Tempat Bersejarah")

        col1, col2 = st.columns(2)
        with col1:
            city_filter = st.radio("Kota:", ["Semua", "Makkah", "Madinah"], horizontal=True)

        sites = HISTORICAL_SITES
        if city_filter != "Semua":
            sites = [s for s in sites if s.city == city_filter.upper()]

        for site in sites:
            render_historical_site(site)

    # === TAB 5: RUKUN & SUNNAH ===
    with tabs[4]:
        st.markdown("## 📚 Rukun, Wajib & Sunnah Umrah")

        st.markdown("### 🔴 Rukun Umrah (Wajib Dilakukan)")
        st.caption("Jika ditinggalkan, umrah tidak sah")
        for p in UMRAH_PILLARS:
            st.markdown(f"""
            **{p['name_id']}** ({p['name_ar']})
            > {p['description_id']}
            """)

        st.divider()

        st.markdown("### ✨ Sunnah-sunnah Umrah")
        st.caption("Dianjurkan untuk dilakukan")
        for s in UMRAH_SUNNAHS:
            st.markdown(f"- {s['name']}")

        st.divider()

        st.markdown("### 🚫 Larangan saat Ihram")
        prohibitions = [
            "Memotong rambut atau kuku",
            "Memakai wewangian",
            "Berburu atau membunuh binatang darat",
            "Menikah atau melamar",
            "Berhubungan suami istri",
            "Pria: Memakai pakaian berjahit, menutup kepala",
            "Wanita: Memakai cadar dan sarung tangan"
        ]
        for p in prohibitions:
            st.markdown(f"- ❌ {p}")


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [
    "render_umrah_complete_page",
    "render_doa_card_enhanced",
    "generate_audio_edge",
]
