"""
LABBAIK AI v7.0 - WhatsApp Bot Service
=======================================
Intelligent WhatsApp bot for Umrah assistance:
- AI Chat for Umrah questions
- Doa search and audio
- Step-by-step Umrah guide
- Group management
- SOS Emergency
- Booking notifications

Commands:
- MENU - Show all commands
- DOA [keyword] - Search doa
- UMRAH - Umrah guide
- LANGKAH [1-6] - Umrah step detail
- MIQAT - Miqat locations
- SOS - Emergency help
- JADWAL - Prayer times
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

# Import from existing modules
from features.whatsapp_service import WAHAClient, WAHAConfig, MessageTemplates
from features.umrah_guide import (
    UMRAH_DOAS, UMRAH_PROCEDURES, MIQAT_LOCATIONS, UMRAH_PILLARS,
    UMRAH_VIRTUES, HISTORICAL_SITES, Doa, DoaCategory
)


# =============================================================================
# BOT COMMANDS
# =============================================================================

class BotCommand(str, Enum):
    MENU = "menu"
    DOA = "doa"
    UMRAH = "umrah"
    LANGKAH = "langkah"
    MIQAT = "miqat"
    ZIARAH = "ziarah"
    SOS = "sos"
    JADWAL = "jadwal"
    HELP = "help"
    TANYA = "tanya"
    RUKUN = "rukun"
    SUNNAH = "sunnah"


# =============================================================================
# BOT RESPONSES
# =============================================================================

class BotResponses:
    """Pre-defined bot responses."""

    @staticmethod
    def menu() -> str:
        return """🕋 *LABBAIK AI - Menu Utama*

Ketik perintah berikut:

📖 *UMRAH* - Panduan lengkap umrah
🔢 *LANGKAH 1-6* - Detail langkah umrah
🤲 *DOA [kata kunci]* - Cari doa
   _Contoh: DOA TAWAF_
📍 *MIQAT* - Lokasi miqat
🏛️ *ZIARAH* - Tempat bersejarah
📚 *RUKUN* - Rukun umrah
✨ *SUNNAH* - Sunnah umrah
🆘 *SOS* - Bantuan darurat
❓ *TANYA [pertanyaan]* - Tanya AI
   _Contoh: TANYA apa doa masuk masjid_

Ketik *MENU* kapan saja untuk kembali.

_LABBAIK AI v7.0 - Platform Umrah Cerdas_"""

    @staticmethod
    def umrah_overview() -> str:
        return """🕋 *PANDUAN UMRAH LENGKAP*

*Definisi:*
Umrah adalah ibadah kepada Allah melalui Ihram, Tawaf, Sa'i, dan Tahallul (potong/cukur rambut).

*Keutamaan Umrah:*
✨ Penghapusan dosa-dosa
✨ Menghilangkan kemiskinan
✨ Menjadi tamu Allah

*6 Langkah Umrah:*
1️⃣ Persiapan & Niat
2️⃣ Ihram di Miqat
3️⃣ Tawaf (7 putaran)
4️⃣ Sholat di Maqam Ibrahim
5️⃣ Sa'i (Safa-Marwah)
6️⃣ Tahallul (potong rambut)

Ketik *LANGKAH 1* s/d *LANGKAH 6* untuk detail.
Ketik *RUKUN* untuk rukun umrah.
Ketik *DOA TAWAF* untuk doa tawaf.

_LABBAIK AI - Platform Umrah Cerdas_"""

    @staticmethod
    def rukun_umrah() -> str:
        text = """📚 *RUKUN UMRAH*
_(Wajib dilakukan, jika ditinggalkan umrah tidak sah)_

"""
        for i, pillar in enumerate(UMRAH_PILLARS, 1):
            text += f"""*{i}. {pillar['name_id']}* ({pillar['name_ar']})
   {pillar['description_id']}

"""
        text += """_Ketik UMRAH untuk panduan lengkap_
_LABBAIK AI - Platform Umrah Cerdas_"""
        return text

    @staticmethod
    def sunnah_umrah() -> str:
        return """✨ *SUNNAH-SUNNAH UMRAH*

Dianjurkan untuk dilakukan:

1. Mandi sebelum Ihram
2. Memakai wewangian sebelum Ihram
3. Membaca Talbiyah dengan suara keras (pria)
4. Idhtiba' (membuka bahu kanan) saat Tawaf
5. Ramal (jalan cepat) di 3 putaran pertama Tawaf
6. Mencium atau menyentuh Hajar Aswad
7. Berdoa di Multazam
8. Minum air Zamzam
9. Sholat 2 rakaat di belakang Maqam Ibrahim
10. Berlari kecil di antara tanda hijau saat Sa'i (pria)

_Ketik UMRAH untuk panduan lengkap_
_LABBAIK AI - Platform Umrah Cerdas_"""

    @staticmethod
    def miqat_info() -> str:
        text = """📍 *LOKASI MIQAT*
_(Tempat memulai Ihram)_

"""
        for miqat in MIQAT_LOCATIONS:
            text += f"""🔹 *{miqat.name}*
   {miqat.name_ar}
   📍 {miqat.location}
   🚗 Jarak: {miqat.distance_to_makkah}
   👥 Untuk: {miqat.for_travelers_from}

"""
        text += """_LABBAIK AI - Platform Umrah Cerdas_"""
        return text

    @staticmethod
    def ziarah_info() -> str:
        text = """🏛️ *TEMPAT BERSEJARAH*

*MAKKAH:*
"""
        for site in HISTORICAL_SITES:
            if site.city == "MAKKAH":
                text += f"• {site.name} - {site.significance[:50]}...\n"

        text += "\n*MADINAH:*\n"
        for site in HISTORICAL_SITES:
            if site.city == "MADINAH":
                text += f"• {site.name} - {site.significance[:50]}...\n"

        text += "\n_LABBAIK AI - Platform Umrah Cerdas_"
        return text

    @staticmethod
    def sos_help() -> str:
        return """🆘 *BANTUAN DARURAT*

*Nomor Darurat Saudi Arabia:*
🚑 Ambulans: 997
👮 Polisi: 999
🚒 Pemadam: 998
🏥 Kesehatan: 937

*Kontak Penting:*
📞 KBRI Riyadh: +966-11-488-2800
📞 KJRI Jeddah: +966-12-667-6020

*Jika Tersesat:*
1. Tenang, jangan panik
2. Cari petugas keamanan (berbaju hijau)
3. Tunjukkan kartu identitas/paspor
4. Hubungi pemandu grup

*Tips Keamanan:*
• Simpan nomor pemandu grup
• Foto hotel & kamar Anda
• Selalu bawa paspor copy
• Catat lokasi hotel di Maps

_LABBAIK AI - Platform Umrah Cerdas_"""

    @staticmethod
    def step_detail(step_num: int) -> str:
        if step_num < 1 or step_num > len(UMRAH_PROCEDURES):
            return "❌ Langkah tidak valid. Ketik LANGKAH 1 s/d LANGKAH 6"

        proc = UMRAH_PROCEDURES[step_num - 1]
        badge = "🔴 RUKUN" if proc.is_pillar else "🟡 WAJIB" if proc.is_obligatory else ""

        text = f"""📋 *LANGKAH {proc.step}: {proc.name.upper()}* {badge}

*{proc.name_ar}*

{proc.description}

📍 *Lokasi:* {proc.location}

"""
        if proc.tips:
            text += "*💡 Tips:*\n"
            for tip in proc.tips:
                text += f"• {tip}\n"

        if proc.sunnahs:
            text += "\n*✨ Sunnah:*\n"
            for s in proc.sunnahs:
                text += f"• {s}\n"

        if proc.doas:
            text += "\n*🤲 Doa terkait:*\n"
            for doa_id in proc.doas:
                doa = next((d for d in UMRAH_DOAS if d.id == doa_id), None)
                if doa:
                    text += f"• {doa.name}\n"
            text += f"\n_Ketik DOA {proc.name.split()[0].upper()} untuk detail doa_"

        text += "\n\n_LABBAIK AI - Platform Umrah Cerdas_"
        return text

    @staticmethod
    def doa_result(doa: Doa) -> str:
        wajib = "⚠️ WAJIB" if doa.is_wajib else ""
        return f"""🤲 *{doa.name}* {wajib}

*Arab:*
{doa.arabic}

*Latin:*
_{doa.latin}_

*Artinya:*
{doa.translation_id}

📍 *Kapan dibaca:*
{doa.when_to_read}

📚 {doa.source if doa.source else ''}

_Ketik DOA [kata kunci] untuk cari doa lain_
_LABBAIK AI - Platform Umrah Cerdas_"""

    @staticmethod
    def doa_list(doas: List[Doa], keyword: str) -> str:
        if not doas:
            return f"""❌ Tidak ditemukan doa dengan kata kunci "{keyword}"

*Coba kata kunci:*
• DOA TAWAF
• DOA SAI
• DOA IHRAM
• DOA MASJID
• DOA PERJALANAN

_LABBAIK AI - Platform Umrah Cerdas_"""

        if len(doas) == 1:
            return BotResponses.doa_result(doas[0])

        text = f"""🤲 *Ditemukan {len(doas)} doa untuk "{keyword}":*

"""
        for i, doa in enumerate(doas[:5], 1):
            wajib = "⚠️" if doa.is_wajib else ""
            text += f"{i}. *{doa.name}* {wajib}\n   _{doa.when_to_read}_\n\n"

        if len(doas) > 5:
            text += f"_...dan {len(doas) - 5} doa lainnya_\n\n"

        text += """Ketik *DOA [nama doa]* untuk detail lengkap.

_LABBAIK AI - Platform Umrah Cerdas_"""
        return text

    @staticmethod
    def ai_response(question: str, answer: str) -> str:
        return f"""🤖 *LABBAIK AI*

*Pertanyaan:*
_{question}_

*Jawaban:*
{answer}

_Ketik TANYA [pertanyaan] untuk bertanya lagi_
_LABBAIK AI - Platform Umrah Cerdas_"""

    @staticmethod
    def unknown_command() -> str:
        return """❓ Maaf, perintah tidak dikenali.

Ketik *MENU* untuk melihat daftar perintah.

_LABBAIK AI - Platform Umrah Cerdas_"""


# =============================================================================
# DOA SEARCH
# =============================================================================

def search_doa(keyword: str) -> List[Doa]:
    """Search doas by keyword."""
    keyword = keyword.lower().strip()
    results = []

    for doa in UMRAH_DOAS:
        if (keyword in doa.name.lower() or
            keyword in doa.translation_id.lower() or
            keyword in doa.when_to_read.lower() or
            keyword in doa.category.value.lower() or
            keyword in doa.latin.lower()):
            results.append(doa)

    return results


# =============================================================================
# AI RESPONSE (Simple keyword-based)
# =============================================================================

def get_ai_response(question: str) -> str:
    """Get AI response for question (simple keyword matching)."""
    q = question.lower()

    # Doa-related questions
    if any(k in q for k in ["doa", "bacaan", "baca"]):
        if "tawaf" in q:
            doas = search_doa("tawaf")
            if doas:
                return BotResponses.doa_result(doas[0])
        elif "sai" in q or "sa'i" in q:
            doas = search_doa("sai")
            if doas:
                return BotResponses.doa_result(doas[0])
        elif "ihram" in q:
            doas = search_doa("ihram")
            if doas:
                return BotResponses.doa_result(doas[0])
        elif "masjid" in q:
            doas = search_doa("masjid")
            if doas:
                return BotResponses.doa_result(doas[0])
        return "Ketik DOA [kata kunci] untuk mencari doa. Contoh: DOA TAWAF"

    # Umrah steps
    if any(k in q for k in ["langkah", "cara", "step", "bagaimana"]):
        return BotResponses.umrah_overview()

    # Miqat
    if "miqat" in q:
        return BotResponses.miqat_info()

    # Rukun
    if "rukun" in q or "wajib" in q:
        return BotResponses.rukun_umrah()

    # Sunnah
    if "sunnah" in q or "sunah" in q:
        return BotResponses.sunnah_umrah()

    # Ihram
    if "ihram" in q:
        return BotResponses.step_detail(2)

    # Tawaf
    if "tawaf" in q:
        return BotResponses.step_detail(3)

    # Sai
    if "sai" in q or "sa'i" in q:
        return BotResponses.step_detail(5)

    # Default
    return """Untuk pertanyaan tentang Umrah, silakan ketik:
• UMRAH - Panduan lengkap
• DOA [keyword] - Cari doa
• RUKUN - Rukun umrah
• LANGKAH 1-6 - Detail langkah

Atau hubungi pemandu Anda untuk pertanyaan spesifik."""


# =============================================================================
# WHATSAPP BOT HANDLER
# =============================================================================

@dataclass
class IncomingMessage:
    """Incoming WhatsApp message."""
    from_number: str
    message: str
    timestamp: datetime
    message_id: str = ""
    is_group: bool = False
    group_id: str = ""
    sender_name: str = ""


class WhatsAppBot:
    """WhatsApp Bot for Labbaik AI."""

    def __init__(self, waha_client: WAHAClient = None):
        self.client = waha_client or WAHAClient()
        self.responses = BotResponses()
        self.command_handlers: Dict[str, Callable] = {
            BotCommand.MENU: self._handle_menu,
            BotCommand.HELP: self._handle_menu,
            BotCommand.UMRAH: self._handle_umrah,
            BotCommand.LANGKAH: self._handle_langkah,
            BotCommand.DOA: self._handle_doa,
            BotCommand.MIQAT: self._handle_miqat,
            BotCommand.ZIARAH: self._handle_ziarah,
            BotCommand.RUKUN: self._handle_rukun,
            BotCommand.SUNNAH: self._handle_sunnah,
            BotCommand.SOS: self._handle_sos,
            BotCommand.TANYA: self._handle_tanya,
        }

    def process_message(self, message: IncomingMessage) -> str:
        """Process incoming message and return response."""
        text = message.message.strip()

        # Parse command and arguments
        parts = text.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        # Check if it's a known command
        try:
            cmd = BotCommand(command)
            handler = self.command_handlers.get(cmd)
            if handler:
                return handler(args)
        except ValueError:
            pass

        # Check for greeting
        greetings = ["halo", "hai", "hi", "hello", "assalamualaikum", "assalamu'alaikum"]
        if command in greetings:
            return self._handle_greeting(message.sender_name)

        # Default: show menu for unknown commands
        return self.responses.unknown_command()

    def send_response(self, to: str, message: str) -> Dict[str, Any]:
        """Send response message."""
        return self.client.send_text(to, message)

    # Command Handlers
    def _handle_menu(self, args: str = "") -> str:
        return self.responses.menu()

    def _handle_umrah(self, args: str = "") -> str:
        return self.responses.umrah_overview()

    def _handle_langkah(self, args: str = "") -> str:
        try:
            step_num = int(args.strip())
            return self.responses.step_detail(step_num)
        except (ValueError, TypeError):
            return """❌ Format salah. Gunakan:
• LANGKAH 1 - Persiapan & Niat
• LANGKAH 2 - Ihram di Miqat
• LANGKAH 3 - Tawaf
• LANGKAH 4 - Sholat di Maqam Ibrahim
• LANGKAH 5 - Sa'i
• LANGKAH 6 - Tahallul"""

    def _handle_doa(self, args: str = "") -> str:
        if not args:
            return """🤲 *Cari Doa*

Ketik DOA diikuti kata kunci:
• DOA TAWAF
• DOA SAI
• DOA IHRAM
• DOA MASJID
• DOA PERJALANAN
• DOA MAKAN
• DOA TIDUR

_LABBAIK AI - Platform Umrah Cerdas_"""

        doas = search_doa(args)
        return self.responses.doa_list(doas, args)

    def _handle_miqat(self, args: str = "") -> str:
        return self.responses.miqat_info()

    def _handle_ziarah(self, args: str = "") -> str:
        return self.responses.ziarah_info()

    def _handle_rukun(self, args: str = "") -> str:
        return self.responses.rukun_umrah()

    def _handle_sunnah(self, args: str = "") -> str:
        return self.responses.sunnah_umrah()

    def _handle_sos(self, args: str = "") -> str:
        return self.responses.sos_help()

    def _handle_tanya(self, args: str = "") -> str:
        if not args:
            return """❓ *Tanya LABBAIK AI*

Ketik TANYA diikuti pertanyaan Anda:
• TANYA apa doa saat tawaf
• TANYA bagaimana cara sai
• TANYA apa itu miqat

_LABBAIK AI - Platform Umrah Cerdas_"""

        answer = get_ai_response(args)
        return self.responses.ai_response(args, answer)

    def _handle_greeting(self, name: str = "") -> str:
        name_text = f" {name}" if name else ""
        return f"""🕋 *Wa'alaikumussalam{name_text}!*

Selamat datang di *LABBAIK AI* - Asisten Umrah Cerdas.

Saya siap membantu perjalanan umrah Anda:
✅ Panduan langkah umrah
✅ Koleksi doa lengkap
✅ Informasi miqat
✅ Tempat bersejarah
✅ Bantuan darurat

Ketik *MENU* untuk melihat semua perintah.

_LABBAIK AI v7.0 - Platform Umrah Cerdas_"""


# =============================================================================
# WEBHOOK HANDLER (for FastAPI/Flask integration)
# =============================================================================

def create_webhook_handler(bot: WhatsAppBot = None):
    """Create webhook handler for incoming messages."""
    bot = bot or WhatsAppBot()

    def handle_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming webhook from WAHA.

        Expected payload structure:
        {
            "event": "message",
            "session": "default",
            "payload": {
                "from": "6281234567890@c.us",
                "body": "MENU",
                "timestamp": 1234567890,
                "id": "msg_id",
                "fromMe": false,
                "isGroup": false
            }
        }
        """
        try:
            event = payload.get("event", "")

            if event != "message":
                return {"status": "ignored", "reason": "not a message event"}

            msg_payload = payload.get("payload", {})

            # Skip messages from self
            if msg_payload.get("fromMe", False):
                return {"status": "ignored", "reason": "message from self"}

            # Parse message
            from_id = msg_payload.get("from", "")
            from_number = from_id.replace("@c.us", "").replace("@g.us", "")

            message = IncomingMessage(
                from_number=from_number,
                message=msg_payload.get("body", ""),
                timestamp=datetime.fromtimestamp(msg_payload.get("timestamp", 0)),
                message_id=msg_payload.get("id", ""),
                is_group="@g.us" in from_id,
                group_id=from_id if "@g.us" in from_id else "",
                sender_name=msg_payload.get("notifyName", "")
            )

            # Process and respond
            response = bot.process_message(message)

            # Send response
            if message.is_group:
                result = bot.client.send_to_group(message.group_id.replace("@g.us", ""), response)
            else:
                result = bot.send_response(message.from_number, response)

            return {
                "status": "success",
                "response_sent": result.get("success", False),
                "to": message.from_number
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}

    return handle_webhook


# =============================================================================
# FASTAPI ROUTER (Optional - for standalone deployment)
# =============================================================================

def create_fastapi_router():
    """Create FastAPI router for WhatsApp bot webhook."""
    try:
        from fastapi import APIRouter, Request, HTTPException
        from fastapi.responses import JSONResponse
    except ImportError:
        return None

    router = APIRouter(prefix="/whatsapp", tags=["WhatsApp Bot"])
    bot = WhatsAppBot()
    webhook_handler = create_webhook_handler(bot)

    @router.post("/webhook")
    async def webhook(request: Request):
        """Handle incoming WhatsApp webhook."""
        try:
            payload = await request.json()
            result = webhook_handler(payload)
            return JSONResponse(content=result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "ok", "service": "labbaik-whatsapp-bot"}

    @router.post("/send")
    async def send_message(request: Request):
        """Send message endpoint (for testing)."""
        try:
            data = await request.json()
            phone = data.get("phone", "")
            message = data.get("message", "")

            if not phone or not message:
                raise HTTPException(status_code=400, detail="phone and message required")

            result = bot.send_response(phone, message)
            return JSONResponse(content=result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router


# =============================================================================
# STREAMLIT UI
# =============================================================================

def render_bot_simulator():
    """Render WhatsApp bot simulator in Streamlit."""
    import streamlit as st

    st.markdown("## 🤖 WhatsApp Bot Simulator")
    st.caption("Test bot responses without sending actual WhatsApp messages")

    bot = WhatsAppBot()

    # Chat history
    if "bot_history" not in st.session_state:
        st.session_state.bot_history = []

    # Display chat history
    for msg in st.session_state.bot_history:
        if msg["type"] == "user":
            st.markdown(f"**You:** {msg['text']}")
        else:
            st.markdown(f"**Bot:**\n{msg['text']}")
        st.divider()

    # Input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Ketik pesan:", key="bot_input", placeholder="MENU")
    with col2:
        send = st.button("Kirim", type="primary")

    if send and user_input:
        # Add user message
        st.session_state.bot_history.append({"type": "user", "text": user_input})

        # Get bot response
        message = IncomingMessage(
            from_number="simulator",
            message=user_input,
            timestamp=datetime.now()
        )
        response = bot.process_message(message)

        # Add bot response
        st.session_state.bot_history.append({"type": "bot", "text": response})

        st.rerun()

    # Quick commands
    st.markdown("### Quick Commands")
    cols = st.columns(4)
    commands = ["MENU", "UMRAH", "DOA TAWAF", "MIQAT", "RUKUN", "SOS", "LANGKAH 1", "TANYA apa itu ihram"]

    for i, cmd in enumerate(commands):
        with cols[i % 4]:
            if st.button(cmd, key=f"quick_{i}"):
                st.session_state.bot_history.append({"type": "user", "text": cmd})
                message = IncomingMessage(from_number="simulator", message=cmd, timestamp=datetime.now())
                response = bot.process_message(message)
                st.session_state.bot_history.append({"type": "bot", "text": response})
                st.rerun()

    # Clear history
    if st.button("🗑️ Clear History"):
        st.session_state.bot_history = []
        st.rerun()


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "WhatsAppBot",
    "IncomingMessage",
    "BotCommand",
    "BotResponses",
    "search_doa",
    "create_webhook_handler",
    "create_fastapi_router",
    "render_bot_simulator",
]
