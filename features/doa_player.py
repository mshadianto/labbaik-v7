"""
LABBAIK AI v6.0 - Voice Doa Player
===================================
Audio playback for Umrah duas with:
- Arabic text with proper RTL display
- Latin transliteration
- Indonesian translation
- Audio playback (TTS or pre-recorded)
- Bookmark/favorites system
- Voice chat for doa questions

Uses Web Speech API for TTS when audio files not available.
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
import base64

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
# ENHANCED AUDIO PLAYER COMPONENT
# =============================================================================

AUDIO_PLAYER_HTML = """
<div id="enhanced-player-{doa_id}" style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 1.5rem; border-radius: 20px; border: 1px solid #d4af37; margin-bottom: 1.5rem; box-shadow: 0 10px 40px rgba(212, 175, 55, 0.1);">

    <!-- Header -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <div>
            <h3 style="color: #d4af37; margin: 0; font-size: 1.2rem;">{name}</h3>
            <span style="color: #888; font-size: 0.8rem;">{category} • {when_to_read}</span>
        </div>
        {wajib_badge}
    </div>

    <!-- Arabic Text -->
    <div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;">
        <div style="direction: rtl; text-align: right; font-family: 'Amiri', 'Traditional Arabic', serif; font-size: 2rem; line-height: 2.2; color: #d4af37;">
            {arabic}
        </div>
    </div>

    <!-- Audio Controls -->
    <div style="background: rgba(212, 175, 55, 0.1); padding: 1rem; border-radius: 15px; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
            <!-- Play/Pause/Stop -->
            <div style="display: flex; gap: 0.5rem;">
                <button id="play-{doa_id}" onclick="playDoa_{doa_id}()" style="background: #d4af37; border: none; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; font-size: 1.5rem; display: flex; align-items: center; justify-content: center;">
                    ▶️
                </button>
                <button onclick="pauseDoa_{doa_id}()" style="background: #333; border: 1px solid #d4af37; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 1rem;">
                    ⏸️
                </button>
                <button onclick="stopDoa_{doa_id}()" style="background: #333; border: 1px solid #d4af37; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 1rem;">
                    ⏹️
                </button>
            </div>

            <!-- Speed Control -->
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="color: #888; font-size: 0.8rem;">Kecepatan:</span>
                <select id="speed-{doa_id}" onchange="updateSpeed_{doa_id}()" style="background: #333; color: white; border: 1px solid #d4af37; padding: 5px 10px; border-radius: 8px;">
                    <option value="0.5">0.5x (Lambat)</option>
                    <option value="0.7" selected>0.7x (Normal)</option>
                    <option value="0.9">0.9x (Cepat)</option>
                    <option value="1.0">1.0x (Asli)</option>
                </select>
            </div>

            <!-- Repeat Toggle -->
            <button id="repeat-{doa_id}" onclick="toggleRepeat_{doa_id}()" style="background: #333; border: 1px solid #555; padding: 8px 15px; border-radius: 20px; cursor: pointer; color: #888;">
                🔁 Ulangi
            </button>
        </div>

        <!-- Status -->
        <div id="status-{doa_id}" style="color: #888; font-size: 0.8rem; margin-top: 0.5rem;">
            Siap diputar
        </div>
    </div>

    <!-- Latin & Translation -->
    <div style="color: #aaa; font-style: italic; margin-bottom: 0.5rem; font-size: 0.95rem;">
        {latin}
    </div>
    <div style="color: #eee; font-size: 1rem;">
        <strong>Artinya:</strong> {translation}
    </div>
</div>

<script>
(function() {{
    let currentUtterance_{doa_id} = null;
    let repeatEnabled_{doa_id} = false;
    let playbackSpeed_{doa_id} = 0.7;

    window.playDoa_{doa_id} = function() {{
        window.speechSynthesis.cancel();

        const text = `{arabic}`;
        currentUtterance_{doa_id} = new SpeechSynthesisUtterance(text);
        currentUtterance_{doa_id}.lang = 'ar-SA';
        currentUtterance_{doa_id}.rate = playbackSpeed_{doa_id};
        currentUtterance_{doa_id}.pitch = 1.0;

        // Find Arabic voice if available
        const voices = window.speechSynthesis.getVoices();
        const arabicVoice = voices.find(v => v.lang.includes('ar'));
        if (arabicVoice) currentUtterance_{doa_id}.voice = arabicVoice;

        currentUtterance_{doa_id}.onstart = () => {{
            document.getElementById('status-{doa_id}').innerText = '🔊 Sedang memutar...';
            document.getElementById('play-{doa_id}').innerText = '🔊';
        }};

        currentUtterance_{doa_id}.onend = () => {{
            document.getElementById('status-{doa_id}').innerText = repeatEnabled_{doa_id} ? '🔁 Mengulang...' : '✅ Selesai';
            document.getElementById('play-{doa_id}').innerText = '▶️';
            if (repeatEnabled_{doa_id}) {{
                setTimeout(() => playDoa_{doa_id}(), 1500);
            }}
        }};

        currentUtterance_{doa_id}.onerror = () => {{
            document.getElementById('status-{doa_id}').innerText = '❌ Error - coba lagi';
        }};

        window.speechSynthesis.speak(currentUtterance_{doa_id});
    }};

    window.pauseDoa_{doa_id} = function() {{
        if (window.speechSynthesis.speaking) {{
            window.speechSynthesis.pause();
            document.getElementById('status-{doa_id}').innerText = '⏸️ Dijeda';
        }} else if (window.speechSynthesis.paused) {{
            window.speechSynthesis.resume();
            document.getElementById('status-{doa_id}').innerText = '🔊 Melanjutkan...';
        }}
    }};

    window.stopDoa_{doa_id} = function() {{
        window.speechSynthesis.cancel();
        repeatEnabled_{doa_id} = false;
        document.getElementById('repeat-{doa_id}').style.borderColor = '#555';
        document.getElementById('repeat-{doa_id}').style.color = '#888';
        document.getElementById('status-{doa_id}').innerText = 'Siap diputar';
        document.getElementById('play-{doa_id}').innerText = '▶️';
    }};

    window.updateSpeed_{doa_id} = function() {{
        playbackSpeed_{doa_id} = parseFloat(document.getElementById('speed-{doa_id}').value);
    }};

    window.toggleRepeat_{doa_id} = function() {{
        repeatEnabled_{doa_id} = !repeatEnabled_{doa_id};
        const btn = document.getElementById('repeat-{doa_id}');
        btn.style.borderColor = repeatEnabled_{doa_id} ? '#d4af37' : '#555';
        btn.style.color = repeatEnabled_{doa_id} ? '#d4af37' : '#888';
        btn.style.background = repeatEnabled_{doa_id} ? 'rgba(212,175,55,0.2)' : '#333';
    }};

    // Load voices
    if (window.speechSynthesis.onvoiceschanged !== undefined) {{
        window.speechSynthesis.onvoiceschanged = () => {{}};
    }}
}})();
</script>
"""

# =============================================================================
# VOICE CHAT COMPONENT
# =============================================================================

VOICE_CHAT_HTML = """
<div id="voice-chat-container" style="background: linear-gradient(135deg, #0f3460, #16213e); padding: 1.5rem; border-radius: 20px; border: 1px solid #00d9ff; margin-bottom: 1.5rem;">
    <h3 style="color: #00d9ff; margin-bottom: 1rem;">🎙️ Tanya Doa dengan Suara</h3>

    <div style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
        <!-- Record Button -->
        <button id="voice-record-btn" onclick="toggleRecording()" style="background: linear-gradient(135deg, #e94560, #ff6b6b); border: none; width: 70px; height: 70px; border-radius: 50%; cursor: pointer; font-size: 2rem; box-shadow: 0 5px 20px rgba(233, 69, 96, 0.4); transition: all 0.3s;">
            🎤
        </button>

        <div style="flex: 1; min-width: 200px;">
            <div id="voice-status" style="color: #aaa; margin-bottom: 0.5rem;">
                Tekan tombol mikrofon untuk bertanya
            </div>
            <div id="voice-transcript" style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 10px; min-height: 50px; color: white; font-size: 1rem;">
                <span style="color: #666;">Pertanyaan Anda akan muncul di sini...</span>
            </div>
        </div>
    </div>

    <!-- Example Questions -->
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(0,217,255,0.2);">
        <span style="color: #888; font-size: 0.8rem;">💡 Contoh pertanyaan:</span>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
            <span onclick="setQuestion('Apa doa masuk masjid?')" style="background: rgba(0,217,255,0.1); color: #00d9ff; padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; cursor: pointer; border: 1px solid rgba(0,217,255,0.3);">Doa masuk masjid?</span>
            <span onclick="setQuestion('Bacaan talbiyah lengkap')" style="background: rgba(0,217,255,0.1); color: #00d9ff; padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; cursor: pointer; border: 1px solid rgba(0,217,255,0.3);">Talbiyah lengkap</span>
            <span onclick="setQuestion('Doa saat tawaf')" style="background: rgba(0,217,255,0.1); color: #00d9ff; padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; cursor: pointer; border: 1px solid rgba(0,217,255,0.3);">Doa saat tawaf</span>
            <span onclick="setQuestion('Doa wajib saat sai')" style="background: rgba(0,217,255,0.1); color: #00d9ff; padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; cursor: pointer; border: 1px solid rgba(0,217,255,0.3);">Doa wajib sai</span>
        </div>
    </div>
</div>

<script>
(function() {
    let recognition = null;
    let isRecording = false;

    // Initialize Speech Recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'id-ID';

        recognition.onresult = function(event) {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            document.getElementById('voice-transcript').innerHTML = transcript || '<span style="color: #666;">Mendengarkan...</span>';

            if (event.results[event.results.length - 1].isFinal) {
                // Send to Streamlit
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: transcript
                }, '*');
            }
        };

        recognition.onstart = function() {
            document.getElementById('voice-status').innerText = '🔴 Mendengarkan... Silakan bicara';
            document.getElementById('voice-record-btn').style.background = 'linear-gradient(135deg, #ff0000, #ff4444)';
            document.getElementById('voice-record-btn').style.animation = 'pulse 1s infinite';
        };

        recognition.onend = function() {
            isRecording = false;
            document.getElementById('voice-status').innerText = 'Tekan tombol mikrofon untuk bertanya lagi';
            document.getElementById('voice-record-btn').style.background = 'linear-gradient(135deg, #e94560, #ff6b6b)';
            document.getElementById('voice-record-btn').style.animation = 'none';
        };

        recognition.onerror = function(event) {
            document.getElementById('voice-status').innerText = '❌ Error: ' + event.error;
            isRecording = false;
        };
    }

    window.toggleRecording = function() {
        if (!recognition) {
            document.getElementById('voice-status').innerText = '❌ Browser tidak mendukung voice input';
            return;
        }

        if (isRecording) {
            recognition.stop();
            isRecording = false;
        } else {
            recognition.start();
            isRecording = true;
        }
    };

    window.setQuestion = function(question) {
        document.getElementById('voice-transcript').innerText = question;
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: question
        }, '*');
    };
})();
</script>

<style>
@keyframes pulse {
    0% { transform: scale(1); box-shadow: 0 5px 20px rgba(255, 0, 0, 0.4); }
    50% { transform: scale(1.1); box-shadow: 0 5px 30px rgba(255, 0, 0, 0.6); }
    100% { transform: scale(1); box-shadow: 0 5px 20px rgba(255, 0, 0, 0.4); }
}
</style>
"""

# Legacy template (kept for compatibility)
TTS_HTML_TEMPLATE = AUDIO_PLAYER_HTML


# =============================================================================
# RENDER FUNCTIONS
# =============================================================================

def render_doa_card(doa: Doa, show_audio: bool = True, enhanced: bool = True):
    """Render a single doa card with audio player."""

    wajib_badge = ""
    if doa.is_wajib:
        wajib_badge = '<span style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; padding: 5px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: bold;">⚠️ WAJIB</span>'

    if enhanced and show_audio:
        # Use enhanced HTML audio player
        html = AUDIO_PLAYER_HTML.format(
            doa_id=doa.id.replace("-", "_"),
            name=doa.name,
            category=doa.category.value.title(),
            when_to_read=doa.when_to_read,
            arabic=doa.arabic,
            latin=doa.latin,
            translation=doa.translation,
            wajib_badge=wajib_badge
        )
        st.components.v1.html(html, height=420)

        # Bookmark button (Streamlit native)
        bookmarks = st.session_state.get("doa_bookmarks", set())
        is_bookmarked = doa.id in bookmarks

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(
                "❤️ Favorit" if is_bookmarked else "🤍 Simpan",
                key=f"bookmark_{doa.id}"
            ):
                if is_bookmarked:
                    bookmarks.discard(doa.id)
                    st.toast("Dihapus dari favorit")
                else:
                    bookmarks.add(doa.id)
                    st.toast("Ditambahkan ke favorit!")
                st.session_state.doa_bookmarks = bookmarks
                st.rerun()
    else:
        # Fallback to simple Streamlit components
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### {doa.name}")
                st.caption(f"{doa.category.value.title()} • {doa.when_to_read}")

            with col2:
                if doa.is_wajib:
                    st.error("WAJIB", icon="⚠️")

            st.markdown(f"""
            <div style="background: #0a0a0a; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border: 1px solid #333;">
                <div style="direction: rtl; text-align: right; font-family: 'Traditional Arabic', 'Amiri', serif; font-size: 1.8rem; line-height: 2.2; color: #d4af37;">
                    {doa.arabic}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"*{doa.latin}*")
            st.markdown(f"**Artinya:** {doa.translation}")

            if show_audio:
                col1, col2, col3 = st.columns([1, 1, 2])

                with col1:
                    if st.button("🔊 Play", key=f"play_{doa.id}"):
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


def render_voice_chat():
    """Render voice chat component for asking doa questions."""
    st.components.v1.html(VOICE_CHAT_HTML, height=280)


def search_doa(query: str) -> List[Doa]:
    """Search doas by keyword."""
    query_lower = query.lower()
    results = []

    for doa in UMRAH_DOAS:
        if (query_lower in doa.name.lower() or
            query_lower in doa.translation.lower() or
            query_lower in doa.when_to_read.lower() or
            query_lower in doa.category.value.lower()):
            results.append(doa)

    return results


def render_doa_answer(query: str):
    """Render AI-style answer for doa question."""
    results = search_doa(query)

    if results:
        st.success(f"Ditemukan {len(results)} doa terkait:")
        for doa in results[:3]:  # Show top 3
            render_doa_card(doa, enhanced=True)
    else:
        st.info("Tidak ditemukan doa yang cocok. Coba kata kunci lain seperti: tawaf, sai, ihram, masjid")


def render_doa_player_page():
    """Full doa player page."""

    st.markdown("# 🤲 Doa & Dzikir Umrah")
    st.caption("Kumpulan doa lengkap untuk perjalanan umrah dengan audio player")

    # Initialize session state
    if "doa_bookmarks" not in st.session_state:
        st.session_state.doa_bookmarks = set()
    if "doa_voice_query" not in st.session_state:
        st.session_state.doa_voice_query = ""

    # Tabs - add voice chat tab
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Semua Doa", "🎙️ Tanya Suara", "❤️ Favorit", "📋 Quick Reference"])

    with tab2:
        st.markdown("### 🎙️ Tanya Doa dengan Suara")
        st.caption("Gunakan suara Anda untuk mencari doa yang tepat")

        # Voice chat component
        render_voice_chat()

        # Text input fallback
        query = st.text_input(
            "Atau ketik pertanyaan:",
            placeholder="Contoh: doa masuk masjid, talbiyah, doa tawaf...",
            key="doa_search_input"
        )

        if query:
            render_doa_answer(query)

    # Category filter (for tab1)
    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            categories = ["Semua"] + [c.value.title() for c in DoaCategory]
            selected = st.selectbox("📂 Kategori", categories)

        with col2:
            wajib_only = st.checkbox("⚠️ Hanya Wajib")

        st.divider()

        if selected == "Semua":
            render_doa_list(wajib_only=wajib_only)
        else:
            category_map = {c.value.title(): c for c in DoaCategory}
            category = category_map.get(selected)
            render_doa_list(category=category, wajib_only=wajib_only)

    with tab3:
        bookmarks = st.session_state.get("doa_bookmarks", set())

        if bookmarks:
            st.success(f"Anda memiliki {len(bookmarks)} doa favorit")
            bookmarked_doas = [d for d in UMRAH_DOAS if d.id in bookmarks]
            for doa in bookmarked_doas:
                render_doa_card(doa, enhanced=True)
        else:
            st.info("Belum ada doa favorit. Tekan 🤍 Simpan pada doa untuk menambahkan ke favorit.")

    with tab4:
        st.markdown("### 📋 Ringkasan Doa Wajib Umrah")

        wajib_doas = [d for d in UMRAH_DOAS if d.is_wajib]

        for i, doa in enumerate(wajib_doas, 1):
            with st.expander(f"{i}. {doa.name} ({doa.category.value.title()})"):
                st.markdown(f"""
                **Arab:** {doa.arabic}

                **Latin:** *{doa.latin}*

                **Artinya:** {doa.translation}

                **Kapan dibaca:** {doa.when_to_read}
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
    "render_voice_chat",
    "search_doa",
]
