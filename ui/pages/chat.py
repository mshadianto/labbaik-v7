"""
LABBAIK AI v6.0 - AI Chat (Super WOW Edition)
=============================================
Enhanced chat interface with quick actions,
smart suggestions, rich responses, and history.
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Any, Optional
import random

# =============================================================================
# CONSTANTS & DATA
# =============================================================================

# Quick question categories
QUICK_CATEGORIES = {
    "📋 Persiapan": [
        "Apa saja syarat umrah?",
        "Dokumen apa yang harus disiapkan?",
        "Berapa lama proses visa umrah?",
        "Vaksin apa yang diperlukan?",
        "Apa yang harus dibawa ke tanah suci?",
    ],
    "🕋 Ibadah": [
        "Bagaimana tata cara umrah?",
        "Apa saja rukun umrah?",
        "Bagaimana cara thawaf yang benar?",
        "Apa doa saat sa'i?",
        "Kapan waktu terbaik untuk umrah?",
    ],
    "💰 Biaya": [
        "Berapa biaya umrah tahun ini?",
        "Apa saja yang termasuk dalam paket?",
        "Bagaimana cara cicilan umrah?",
        "Tips hemat umrah?",
        "Paket umrah paling ekonomis?",
    ],
    "🗣️ Bahasa Arab": [
        "Cara mengucapkan talbiyah?",
        "Frasa penting di Arab Saudi?",
        "Doa masuk Masjidil Haram?",
        "Cara bertanya dalam bahasa Arab?",
        "Angka dalam bahasa Arab?",
    ],
    "🏨 Akomodasi": [
        "Hotel terbaik dekat Masjidil Haram?",
        "Berapa jarak ideal hotel ke Masjid?",
        "Fasilitas hotel umrah apa saja?",
        "Tips memilih hotel di Makkah?",
        "Perbedaan hotel bintang 3, 4, 5?",
    ],
    "👩 Wanita": [
        "Aturan mahram untuk wanita?",
        "Umrah saat haid bagaimana?",
        "Tips pakaian wanita di Arab Saudi?",
        "Apa yang harus diperhatikan wanita?",
        "Perbedaan ihram pria dan wanita?",
    ],
}

# Suggested follow-ups based on context
FOLLOW_UP_SUGGESTIONS = {
    "persiapan": [
        "Lalu apa langkah selanjutnya?",
        "Berapa lama proses ini?",
        "Apa ada tips tambahan?",
    ],
    "ibadah": [
        "Bagaimana doanya?",
        "Apa kesalahan umum yang harus dihindari?",
        "Jelaskan lebih detail",
    ],
    "biaya": [
        "Bisa lebih hemat lagi?",
        "Apa saja yang tidak termasuk?",
        "Bandingkan dengan paket lain",
    ],
    "default": [
        "Jelaskan lebih detail",
        "Ada tips lain?",
        "Apa yang harus saya perhatikan?",
    ],
}

# Sample AI responses (in production, this would come from actual AI)
SAMPLE_RESPONSES = {
    "syarat": """
## ✅ Syarat Umrah

Untuk melaksanakan ibadah umrah, berikut syarat yang harus dipenuhi:

### Syarat Wajib
1. **Islam** - Muslim yang beriman
2. **Baligh** - Sudah dewasa (pubertas)
3. **Berakal** - Sehat secara mental
4. **Merdeka** - Bukan budak (sudah tidak relevan di zaman modern)
5. **Mampu** - Secara fisik dan finansial

### Dokumen yang Diperlukan
- 📘 **Paspor** - Minimal berlaku 7 bulan dari tanggal keberangkatan
- 📷 **Pas foto** - Ukuran 4x6, background putih
- 💉 **Kartu vaksin** - Meningitis dan COVID-19
- 📋 **KTP** - Untuk verifikasi identitas

### Untuk Wanita di Bawah 45 Tahun
- Harus ditemani mahram (suami, ayah, saudara laki-laki, dll)
- Atau dengan rombongan wanita minimal 4 orang dengan izin tertulis mahram

---
💡 **Tips:** Siapkan dokumen minimal 2 bulan sebelum keberangkatan!
""",
    "tata_cara": """
## 🕋 Tata Cara Umrah

Umrah memiliki 4 rukun yang harus dilakukan secara berurutan:

### 1. Ihram 📿
- Niat umrah dari miqat
- Memakai pakaian ihram (pria: 2 lembar kain putih tanpa jahitan)
- Membaca talbiyah: *"Labbaikallahumma labbaik..."*

### 2. Thawaf 🔄
- Mengelilingi Ka'bah 7 kali
- Dimulai dari Hajar Aswad
- Berakhir di Hajar Aswad
- Membaca doa dan dzikir

### 3. Sa'i 🚶
- Berjalan antara Shafa dan Marwah
- 7 kali perjalanan (dimulai dari Shafa)
- Mengingat perjuangan Siti Hajar

### 4. Tahallul ✂️
- Mencukur atau memotong rambut
- Pria: minimal 3 helai rambut
- Wanita: memotong ujung rambut seujung jari

---
🤲 Setelah selesai, Anda telah resmi menyelesaikan ibadah umrah!
""",
    "biaya": """
## 💰 Estimasi Biaya Umrah 2025

Biaya umrah bervariasi tergantung beberapa faktor:

### Range Harga per Paket
| Paket | Harga | Hotel |
|-------|-------|-------|
| 🎒 Backpacker | Rp 18-22 Juta | Bintang 2-3 |
| ⭐ Reguler | Rp 25-30 Juta | Bintang 3-4 |
| 🌟 Plus | Rp 35-45 Juta | Bintang 4-5 |
| 👑 VIP | Rp 55-80 Juta | Bintang 5+ |

### Yang Mempengaruhi Harga
1. **Musim** - Ramadan & liburan lebih mahal
2. **Hotel** - Jarak ke Masjid & bintang
3. **Durasi** - 9-21 hari
4. **Airline** - Garuda vs budget airline

### Tips Hemat 💡
- Pilih musim reguler (Mei, Sep, Oct)
- Berangkat rombongan untuk diskon grup
- Booking minimal 3 bulan sebelumnya

---
📊 Gunakan **Simulasi Biaya** untuk perhitungan lebih akurat!
""",
}


# =============================================================================
# SESSION STATE
# =============================================================================

def init_chat_state():
    """Initialize chat session state."""
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Assalamu'alaikum! 👋 Saya asisten AI LABBAIK yang siap membantu Anda merencanakan ibadah umrah. Silakan tanya apa saja tentang persiapan, tata cara, biaya, atau hal lainnya seputar umrah.",
                "timestamp": datetime.now().isoformat(),
            }
        ]
    
    if "chat_context" not in st.session_state:
        st.session_state.chat_context = "default"
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Check for quick question from home page
    if "quick_question" in st.session_state and st.session_state.quick_question:
        question = st.session_state.quick_question
        st.session_state.quick_question = None
        process_user_message(question)

    # Check for voice message from voice input
    if "voice_message" in st.session_state and st.session_state.voice_message:
        voice_text = st.session_state.voice_message
        st.session_state.voice_message = None
        process_user_message(voice_text)


def add_message(role: str, content: str):
    """Add message to chat."""
    st.session_state.chat_messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    })


def get_ai_response(user_message: str) -> str:
    """Get AI response for user message (mock implementation)."""
    
    user_lower = user_message.lower()
    
    # Detect context and generate response
    if any(word in user_lower for word in ["syarat", "persyaratan", "dokumen", "persiapan"]):
        st.session_state.chat_context = "persiapan"
        return SAMPLE_RESPONSES["syarat"]
    
    elif any(word in user_lower for word in ["tata cara", "rukun", "cara", "thawaf", "sai", "ihram"]):
        st.session_state.chat_context = "ibadah"
        return SAMPLE_RESPONSES["tata_cara"]
    
    elif any(word in user_lower for word in ["biaya", "harga", "cost", "budget", "mahal", "murah"]):
        st.session_state.chat_context = "biaya"
        return SAMPLE_RESPONSES["biaya"]
    
    else:
        st.session_state.chat_context = "default"
        return f"""
Terima kasih atas pertanyaannya! 🤲

Pertanyaan Anda tentang **"{user_message}"** sangat baik.

Untuk memberikan jawaban yang lebih spesifik, saya perlu informasi tambahan:

1. Apakah Anda sudah pernah umrah sebelumnya?
2. Kapan rencana keberangkatan Anda?
3. Ada preferensi khusus yang ingin dipertimbangkan?

Silakan pilih kategori di bawah untuk pertanyaan yang lebih spesifik, atau ketik pertanyaan baru.

---
💡 **Tip:** Anda juga bisa menggunakan fitur **Simulasi Biaya** untuk menghitung estimasi umrah!
"""


def process_user_message(message: str):
    """Process user message and get response."""
    
    # Add user message
    add_message("user", message)
    
    # Get AI response (simulated)
    response = get_ai_response(message)
    
    # Add AI response
    add_message("assistant", response)


# =============================================================================
# RENDER COMPONENTS
# =============================================================================

def render_sidebar():
    """Render chat sidebar with quick actions."""
    
    with st.sidebar:
        st.markdown("## 🎯 Aksi Cepat")
        
        # Quick actions
        actions = [
            ("💰 Simulasi Biaya", "simulator"),
            ("📦 Booking", "booking"),
            ("👥 Umrah Bareng", "umrah_bareng"),
            ("📚 Panduan", "guide"),
        ]
        
        for label, page in actions:
            if st.button(label, use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.divider()
        
        # Chat history
        st.markdown("## 📜 Riwayat")
        
        history = st.session_state.get("chat_history", [])
        if history:
            for i, item in enumerate(history[-5:]):
                with st.container(border=True):
                    st.caption(item.get("date", "N/A"))
                    if st.button(f"💬 {item.get('preview', 'Chat')[:20]}...", key=f"hist_{i}", use_container_width=True):
                        st.info("Memuat riwayat chat...")
        else:
            st.caption("Belum ada riwayat")
        
        st.divider()
        
        # Chat controls
        st.markdown("## ⚙️ Pengaturan")
        
        if st.button("🗑️ Hapus Chat", use_container_width=True):
            st.session_state.chat_messages = [st.session_state.chat_messages[0]]
            st.rerun()
        
        if st.button("📤 Export Chat", use_container_width=True):
            st.info("Fitur export akan segera hadir")


def render_quick_questions():
    """Render quick question buttons."""
    
    with st.expander("💡 Pertanyaan Populer", expanded=False):
        tabs = st.tabs(list(QUICK_CATEGORIES.keys()))
        
        for tab, (category, questions) in zip(tabs, QUICK_CATEGORIES.items()):
            with tab:
                for q in questions:
                    if st.button(q, key=f"quick_{q}", use_container_width=True):
                        process_user_message(q)
                        st.rerun()


def render_chat_messages():
    """Render chat message history."""

    messages = st.session_state.chat_messages
    tts_enabled = st.session_state.get("tts_enabled", False)

    for idx, msg in enumerate(messages):
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            with st.chat_message("user"):
                st.markdown(content)
        else:
            with st.chat_message("assistant", avatar="🕋"):
                st.markdown(content)

                # TTS button for assistant messages (only last message to keep it clean)
                if tts_enabled and idx == len(messages) - 1:
                    render_tts_player(content, idx)


def render_tts_player(text: str, message_idx: int):
    """Render TTS audio player for a message."""
    try:
        from services.ai.speech_service import text_to_speech, is_tts_available

        if not is_tts_available():
            return

        # Use session state to cache audio
        cache_key = f"tts_audio_{message_idx}"

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔊 Dengar", key=f"tts_btn_{message_idx}", use_container_width=True):
                with st.spinner("Membuat audio..."):
                    audio_bytes = text_to_speech(text)
                    if audio_bytes:
                        st.session_state[cache_key] = audio_bytes

        # Play cached audio if available
        if cache_key in st.session_state and st.session_state[cache_key]:
            st.audio(st.session_state[cache_key], format="audio/mp3")

    except Exception as e:
        pass  # Silently fail for TTS


def render_follow_up_suggestions():
    """Render follow-up question suggestions."""
    
    context = st.session_state.get("chat_context", "default")
    suggestions = FOLLOW_UP_SUGGESTIONS.get(context, FOLLOW_UP_SUGGESTIONS["default"])
    
    if len(st.session_state.chat_messages) > 1:
        st.markdown("**💬 Tanya lebih lanjut:**")
        
        cols = st.columns(len(suggestions))
        
        for col, suggestion in zip(cols, suggestions):
            with col:
                if st.button(suggestion, key=f"followup_{suggestion}", use_container_width=True):
                    process_user_message(suggestion)
                    st.rerun()


def render_chat_input():
    """Render chat input."""
    
    user_input = st.chat_input("Ketik pertanyaan Anda di sini...")
    
    if user_input:
        process_user_message(user_input)
        st.rerun()


def render_chat_features():
    """Render additional chat features."""

    with st.expander("🛠️ Fitur Tambahan", expanded=False):
        # Voice Input Section
        st.markdown("##### 🎤 Voice Input")
        st.caption("Rekam suara Anda untuk bertanya (Bahasa Indonesia)")

        audio_data = st.audio_input(
            "Tekan untuk merekam",
            key="voice_input",
            label_visibility="collapsed"
        )

        if audio_data is not None:
            # Process voice input
            try:
                from services.ai.speech_service import transcribe_audio

                with st.spinner("🎧 Mengkonversi suara ke teks..."):
                    audio_bytes = audio_data.read()
                    transcribed_text = transcribe_audio(audio_bytes, language="id")

                if transcribed_text:
                    st.success(f"📝 Terdeteksi: **{transcribed_text}**")

                    # Set as pending message to be sent
                    if st.button("📤 Kirim Pertanyaan Ini", use_container_width=True, type="primary"):
                        st.session_state.voice_message = transcribed_text
                        st.rerun()
                else:
                    st.warning("Tidak ada suara terdeteksi. Coba rekam ulang.")

            except Exception as e:
                st.error(f"Gagal memproses audio: {str(e)}")

        st.divider()

        # TTS Toggle Section
        st.markdown("##### 🔊 Voice Response")
        tts_col1, tts_col2 = st.columns([3, 2])

        with tts_col1:
            tts_enabled = st.toggle(
                "Aktifkan respon suara",
                value=st.session_state.get("tts_enabled", False),
                key="tts_toggle",
                help="AI akan membacakan jawaban dengan suara"
            )
            st.session_state.tts_enabled = tts_enabled

        with tts_col2:
            if tts_enabled:
                try:
                    from services.ai.speech_service import is_tts_available
                    if is_tts_available():
                        st.success("✓ TTS Aktif", icon="🔊")
                    else:
                        st.warning("edge-tts belum terinstall")
                except:
                    st.warning("TTS tidak tersedia")

        st.divider()

        # Other features
        col2, col3, col4 = st.columns(3)

        with col2:
            if st.button("📷 Upload Gambar", use_container_width=True):
                st.info("Upload gambar untuk analisis")

        with col3:
            if st.button("📄 Upload Dokumen", use_container_width=True):
                st.info("Upload dokumen untuk review")

        with col4:
            if st.button("🔗 Share Chat", use_container_width=True):
                st.info("Bagikan chat ini")


def render_ai_status():
    """Render AI status indicator."""
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.caption("🟢 AI Assistant Aktif")
    
    with col2:
        st.caption(f"💬 {len(st.session_state.chat_messages)} pesan")
    
    with col3:
        st.caption("⚡ Fast Mode")


# =============================================================================
# MAIN PAGE RENDERER  
# =============================================================================

def render_chat_page():
    """Main chat page renderer."""

    # Track page view
    try:
        from services.analytics import track_page
        track_page("chat")
    except:
        pass
    
    # Initialize state
    init_chat_state()
    
    # Header
    st.markdown("# 🤖 AI Assistant")
    st.caption("Asisten cerdas untuk semua pertanyaan seputar umrah")
    
    # AI Status
    render_ai_status()
    
    st.divider()
    
    # Sidebar
    render_sidebar()
    
    # Quick questions
    render_quick_questions()
    
    # Chat container
    chat_container = st.container(height=500)
    
    with chat_container:
        render_chat_messages()
    
    # Follow-up suggestions
    render_follow_up_suggestions()
    
    # Additional features
    render_chat_features()
    
    # Chat input
    render_chat_input()
    
    # Footer
    st.divider()
    st.caption("💡 Tips: Tanya dengan spesifik untuk jawaban yang lebih akurat | 🔒 Percakapan Anda aman dan privat")


# Export
__all__ = ["render_chat_page"]
