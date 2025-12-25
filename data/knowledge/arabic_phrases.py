"""
LABBAIK AI v6.0 - Arabic Phrases Knowledge Base
===============================================
Comprehensive collection of Arabic phrases for Umrah pilgrims.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class ArabicPhrase:
    """Arabic phrase with transliteration and meaning."""
    id: str
    arabic: str
    transliteration: str
    meaning_id: str  # Indonesian meaning
    meaning_en: str  # English meaning
    category: str
    context: str = ""
    audio_url: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "arabic": self.arabic,
            "transliteration": self.transliteration,
            "meaning_id": self.meaning_id,
            "meaning_en": self.meaning_en,
            "category": self.category,
            "context": self.context,
        }


# =============================================================================
# GREETINGS & COMMON PHRASES
# =============================================================================

GREETING_PHRASES = [
    ArabicPhrase(
        id="greet_001",
        arabic="السَّلَامُ عَلَيْكُمْ",
        transliteration="Assalamu'alaikum",
        meaning_id="Semoga keselamatan atas kalian",
        meaning_en="Peace be upon you",
        category="greeting",
        context="Salam pembuka ketika bertemu seseorang"
    ),
    ArabicPhrase(
        id="greet_002",
        arabic="وَعَلَيْكُمُ السَّلَامُ",
        transliteration="Wa'alaikumussalam",
        meaning_id="Dan semoga keselamatan atas kalian juga",
        meaning_en="And peace be upon you too",
        category="greeting",
        context="Jawaban salam"
    ),
    ArabicPhrase(
        id="greet_003",
        arabic="صَبَاحُ الْخَيْرِ",
        transliteration="Shabahul khair",
        meaning_id="Selamat pagi",
        meaning_en="Good morning",
        category="greeting",
        context="Salam di pagi hari"
    ),
    ArabicPhrase(
        id="greet_004",
        arabic="مَسَاءُ الْخَيْرِ",
        transliteration="Masa'ul khair",
        meaning_id="Selamat sore/malam",
        meaning_en="Good evening",
        category="greeting",
        context="Salam di sore/malam hari"
    ),
    ArabicPhrase(
        id="greet_005",
        arabic="شُكْرًا",
        transliteration="Syukran",
        meaning_id="Terima kasih",
        meaning_en="Thank you",
        category="greeting",
        context="Mengucapkan terima kasih"
    ),
    ArabicPhrase(
        id="greet_006",
        arabic="عَفْوًا",
        transliteration="'Afwan",
        meaning_id="Sama-sama / Maaf",
        meaning_en="You're welcome / Excuse me",
        category="greeting",
        context="Menjawab terima kasih atau minta izin"
    ),
    ArabicPhrase(
        id="greet_007",
        arabic="جَزَاكَ اللهُ خَيْرًا",
        transliteration="Jazakallahu khairan",
        meaning_id="Semoga Allah membalasmu dengan kebaikan",
        meaning_en="May Allah reward you with goodness",
        category="greeting",
        context="Terima kasih Islami"
    ),
    ArabicPhrase(
        id="greet_008",
        arabic="إِنْ شَاءَ اللهُ",
        transliteration="Insya Allah",
        meaning_id="Jika Allah menghendaki",
        meaning_en="God willing",
        category="greeting",
        context="Ketika berencana melakukan sesuatu"
    ),
    ArabicPhrase(
        id="greet_009",
        arabic="مَا شَاءَ اللهُ",
        transliteration="Masyaa Allah",
        meaning_id="Atas kehendak Allah",
        meaning_en="As Allah has willed",
        category="greeting",
        context="Mengagumi sesuatu"
    ),
    ArabicPhrase(
        id="greet_010",
        arabic="الْحَمْدُ لِلَّهِ",
        transliteration="Alhamdulillah",
        meaning_id="Segala puji bagi Allah",
        meaning_en="All praise is due to Allah",
        category="greeting",
        context="Bersyukur"
    ),
]

# =============================================================================
# UMRAH RITUALS - IHRAM
# =============================================================================

IHRAM_PHRASES = [
    ArabicPhrase(
        id="ihram_001",
        arabic="لَبَّيْكَ اللَّهُمَّ عُمْرَةً",
        transliteration="Labbaika Allahumma 'Umratan",
        meaning_id="Aku penuhi panggilan-Mu ya Allah untuk Umrah",
        meaning_en="Here I am O Allah, for Umrah",
        category="ihram",
        context="Niat ihram untuk Umrah"
    ),
    ArabicPhrase(
        id="ihram_002",
        arabic="لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لَا شَرِيكَ لَكَ لَبَّيْكَ، إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لَا شَرِيكَ لَكَ",
        transliteration="Labbaika Allahumma labbaik, labbaika la syarikalaka labbaik, innal hamda wan ni'mata laka wal mulk, la syarikalak",
        meaning_id="Aku penuhi panggilan-Mu ya Allah, aku penuhi panggilan-Mu. Aku penuhi panggilan-Mu, tiada sekutu bagi-Mu, aku penuhi panggilan-Mu. Sesungguhnya segala puji, nikmat dan kerajaan adalah milik-Mu. Tiada sekutu bagi-Mu",
        meaning_en="Here I am at Your service, O Allah. Here I am at Your service. Here I am at Your service, You have no partner. Here I am at Your service. Truly all praise, grace and dominion is Yours. You have no partner",
        category="ihram",
        context="Talbiyah - dibaca berulang-ulang selama ihram"
    ),
]

# =============================================================================
# UMRAH RITUALS - TAWAF
# =============================================================================

TAWAF_PHRASES = [
    ArabicPhrase(
        id="tawaf_001",
        arabic="بِسْمِ اللَّهِ وَاللَّهُ أَكْبَرُ",
        transliteration="Bismillahi wallahu akbar",
        meaning_id="Dengan nama Allah dan Allah Maha Besar",
        meaning_en="In the name of Allah and Allah is the Greatest",
        category="tawaf",
        context="Mengawali tawaf saat menyentuh/menghadap Hajar Aswad"
    ),
    ArabicPhrase(
        id="tawaf_002",
        arabic="رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ",
        transliteration="Rabbana atina fid dunya hasanah, wa fil akhirati hasanah, wa qina 'adzaban nar",
        meaning_id="Ya Tuhan kami, berilah kami kebaikan di dunia dan kebaikan di akhirat, dan lindungilah kami dari siksa neraka",
        meaning_en="Our Lord, give us good in this world and good in the Hereafter, and protect us from the punishment of the Fire",
        category="tawaf",
        context="Doa antara Rukun Yamani dan Hajar Aswad"
    ),
    ArabicPhrase(
        id="tawaf_003",
        arabic="سُبْحَانَ اللَّهِ وَالْحَمْدُ لِلَّهِ وَلَا إِلَهَ إِلَّا اللَّهُ وَاللَّهُ أَكْبَرُ",
        transliteration="Subhanallah wal hamdulillah wa la ilaha illallah wallahu akbar",
        meaning_id="Maha Suci Allah, segala puji bagi Allah, tiada Tuhan selain Allah, dan Allah Maha Besar",
        meaning_en="Glory be to Allah, all praise to Allah, there is no god but Allah, and Allah is the Greatest",
        category="tawaf",
        context="Dzikir selama tawaf"
    ),
]

# =============================================================================
# UMRAH RITUALS - SA'I
# =============================================================================

SAI_PHRASES = [
    ArabicPhrase(
        id="sai_001",
        arabic="إِنَّ الصَّفَا وَالْمَرْوَةَ مِنْ شَعَائِرِ اللَّهِ",
        transliteration="Innash shafa wal marwata min sya'airillah",
        meaning_id="Sesungguhnya Shafa dan Marwah adalah sebagian dari syi'ar Allah",
        meaning_en="Indeed, Safa and Marwah are among the symbols of Allah",
        category="sai",
        context="Dibaca saat mendekati bukit Shafa untuk memulai sa'i"
    ),
    ArabicPhrase(
        id="sai_002",
        arabic="أَبْدَأُ بِمَا بَدَأَ اللَّهُ بِهِ",
        transliteration="Abda'u bima bada'allahu bih",
        meaning_id="Aku mulai dengan apa yang Allah mulai dengannya",
        meaning_en="I begin with what Allah began with",
        category="sai",
        context="Dibaca sebelum naik ke bukit Shafa"
    ),
    ArabicPhrase(
        id="sai_003",
        arabic="لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ",
        transliteration="La ilaha illallahu wahdahu la syarikalah, lahul mulku wa lahul hamdu wa huwa 'ala kulli syai'in qadir",
        meaning_id="Tiada Tuhan selain Allah Yang Maha Esa, tiada sekutu bagi-Nya. Bagi-Nya kerajaan dan bagi-Nya segala pujian. Dia Maha Kuasa atas segala sesuatu",
        meaning_en="There is no god but Allah alone, with no partner. To Him belongs the dominion and to Him is all praise, and He is over all things powerful",
        category="sai",
        context="Doa di atas bukit Shafa dan Marwah"
    ),
]

# =============================================================================
# UMRAH RITUALS - TAHALLUL
# =============================================================================

TAHALLUL_PHRASES = [
    ArabicPhrase(
        id="tahallul_001",
        arabic="بِسْمِ اللَّهِ",
        transliteration="Bismillah",
        meaning_id="Dengan nama Allah",
        meaning_en="In the name of Allah",
        category="tahallul",
        context="Sebelum mencukur/memotong rambut"
    ),
    ArabicPhrase(
        id="tahallul_002",
        arabic="الْحَمْدُ لِلَّهِ الَّذِي أَتَمَّ لَنَا نُسُكَنَا",
        transliteration="Alhamdulillahil ladzi atamma lana nusukana",
        meaning_id="Segala puji bagi Allah yang telah menyempurnakan manasik kami",
        meaning_en="All praise to Allah who has completed our rituals",
        category="tahallul",
        context="Setelah tahallul selesai"
    ),
]

# =============================================================================
# ENTERING MOSQUE
# =============================================================================

MOSQUE_PHRASES = [
    ArabicPhrase(
        id="mosque_001",
        arabic="بِسْمِ اللَّهِ وَالصَّلَاةُ وَالسَّلَامُ عَلَى رَسُولِ اللَّهِ، اللَّهُمَّ افْتَحْ لِي أَبْوَابَ رَحْمَتِكَ",
        transliteration="Bismillahi was shalatu was salamu 'ala rasulillah. Allahummaftah li abwaba rahmatik",
        meaning_id="Dengan nama Allah, shalawat dan salam atas Rasulullah. Ya Allah bukakanlah untukku pintu-pintu rahmat-Mu",
        meaning_en="In the name of Allah, blessings and peace upon the Messenger of Allah. O Allah, open for me the doors of Your mercy",
        category="mosque",
        context="Doa masuk masjid"
    ),
    ArabicPhrase(
        id="mosque_002",
        arabic="بِسْمِ اللَّهِ وَالصَّلَاةُ وَالسَّلَامُ عَلَى رَسُولِ اللَّهِ، اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ",
        transliteration="Bismillahi was shalatu was salamu 'ala rasulillah. Allahumma inni as'aluka min fadlik",
        meaning_id="Dengan nama Allah, shalawat dan salam atas Rasulullah. Ya Allah aku memohon kepada-Mu dari karunia-Mu",
        meaning_en="In the name of Allah, blessings and peace upon the Messenger of Allah. O Allah, I ask You from Your bounty",
        category="mosque",
        context="Doa keluar masjid"
    ),
    ArabicPhrase(
        id="mosque_003",
        arabic="اللَّهُمَّ زِدْ هَذَا الْبَيْتَ تَشْرِيفًا وَتَعْظِيمًا وَتَكْرِيمًا وَمَهَابَةً",
        transliteration="Allahumma zid hadhal baita tasyrifan wa ta'zhiman wa takriman wa mahabah",
        meaning_id="Ya Allah, tambahkanlah kemuliaan, keagungan, kehormatan, dan kewibawaan bait ini",
        meaning_en="O Allah, increase this House in honor, greatness, dignity and reverence",
        category="mosque",
        context="Doa saat melihat Ka'bah untuk pertama kali"
    ),
]

# =============================================================================
# DAILY PRACTICAL PHRASES
# =============================================================================

PRACTICAL_PHRASES = [
    ArabicPhrase(
        id="pract_001",
        arabic="أَيْنَ الْحَمَّامُ؟",
        transliteration="Ainal hammam?",
        meaning_id="Di mana kamar mandi?",
        meaning_en="Where is the bathroom?",
        category="practical",
        context="Menanyakan lokasi kamar mandi"
    ),
    ArabicPhrase(
        id="pract_002",
        arabic="كَمْ الثَّمَنُ؟",
        transliteration="Kamits tsaman?",
        meaning_id="Berapa harganya?",
        meaning_en="How much is the price?",
        category="practical",
        context="Menanyakan harga"
    ),
    ArabicPhrase(
        id="pract_003",
        arabic="أُرِيدُ مَاءً",
        transliteration="Uridu ma'an",
        meaning_id="Saya mau air",
        meaning_en="I want water",
        category="practical",
        context="Meminta air minum"
    ),
    ArabicPhrase(
        id="pract_004",
        arabic="أَيْنَ الْفُنْدُقُ؟",
        transliteration="Ainal funduq?",
        meaning_id="Di mana hotelnya?",
        meaning_en="Where is the hotel?",
        category="practical",
        context="Menanyakan lokasi hotel"
    ),
    ArabicPhrase(
        id="pract_005",
        arabic="سَاعِدْنِي مِنْ فَضْلِكَ",
        transliteration="Sa'idni min fadlik",
        meaning_id="Tolong bantu saya",
        meaning_en="Please help me",
        category="practical",
        context="Meminta bantuan"
    ),
    ArabicPhrase(
        id="pract_006",
        arabic="أَنَا مِنْ إِنْدُونِيسِيَا",
        transliteration="Ana min Indonesia",
        meaning_id="Saya dari Indonesia",
        meaning_en="I am from Indonesia",
        category="practical",
        context="Memperkenalkan asal negara"
    ),
    ArabicPhrase(
        id="pract_007",
        arabic="لَا أَفْهَمُ",
        transliteration="La afham",
        meaning_id="Saya tidak mengerti",
        meaning_en="I don't understand",
        category="practical",
        context="Menyatakan tidak mengerti"
    ),
    ArabicPhrase(
        id="pract_008",
        arabic="تَكَلَّمْ بِبُطْءٍ مِنْ فَضْلِكَ",
        transliteration="Takallam bibuth'in min fadlik",
        meaning_id="Tolong bicara pelan-pelan",
        meaning_en="Please speak slowly",
        category="practical",
        context="Meminta lawan bicara berbicara lebih pelan"
    ),
    ArabicPhrase(
        id="pract_009",
        arabic="أَيْنَ الْمَسْجِدُ الْحَرَامُ؟",
        transliteration="Ainal masjidil haram?",
        meaning_id="Di mana Masjidil Haram?",
        meaning_en="Where is Masjidil Haram?",
        category="practical",
        context="Menanyakan arah Masjidil Haram"
    ),
    ArabicPhrase(
        id="pract_010",
        arabic="أَيْنَ الْمَسْجِدُ النَّبَوِيُّ؟",
        transliteration="Ainal masjidun nabawi?",
        meaning_id="Di mana Masjid Nabawi?",
        meaning_en="Where is the Prophet's Mosque?",
        category="practical",
        context="Menanyakan arah Masjid Nabawi"
    ),
]

# =============================================================================
# NUMBERS
# =============================================================================

NUMBER_PHRASES = [
    ArabicPhrase(
        id="num_001", arabic="وَاحِدٌ", transliteration="Wahid",
        meaning_id="Satu", meaning_en="One", category="numbers"
    ),
    ArabicPhrase(
        id="num_002", arabic="اِثْنَانِ", transliteration="Itsnan",
        meaning_id="Dua", meaning_en="Two", category="numbers"
    ),
    ArabicPhrase(
        id="num_003", arabic="ثَلَاثَةٌ", transliteration="Tsalatsah",
        meaning_id="Tiga", meaning_en="Three", category="numbers"
    ),
    ArabicPhrase(
        id="num_004", arabic="أَرْبَعَةٌ", transliteration="Arba'ah",
        meaning_id="Empat", meaning_en="Four", category="numbers"
    ),
    ArabicPhrase(
        id="num_005", arabic="خَمْسَةٌ", transliteration="Khamsah",
        meaning_id="Lima", meaning_en="Five", category="numbers"
    ),
    ArabicPhrase(
        id="num_006", arabic="سِتَّةٌ", transliteration="Sittah",
        meaning_id="Enam", meaning_en="Six", category="numbers"
    ),
    ArabicPhrase(
        id="num_007", arabic="سَبْعَةٌ", transliteration="Sab'ah",
        meaning_id="Tujuh", meaning_en="Seven", category="numbers"
    ),
    ArabicPhrase(
        id="num_008", arabic="ثَمَانِيَةٌ", transliteration="Tsamaniyah",
        meaning_id="Delapan", meaning_en="Eight", category="numbers"
    ),
    ArabicPhrase(
        id="num_009", arabic="تِسْعَةٌ", transliteration="Tis'ah",
        meaning_id="Sembilan", meaning_en="Nine", category="numbers"
    ),
    ArabicPhrase(
        id="num_010", arabic="عَشَرَةٌ", transliteration="'Asyarah",
        meaning_id="Sepuluh", meaning_en="Ten", category="numbers"
    ),
]

# =============================================================================
# COLLECTION FUNCTIONS
# =============================================================================

def get_all_phrases() -> List[ArabicPhrase]:
    """Get all Arabic phrases."""
    all_phrases = []
    all_phrases.extend(GREETING_PHRASES)
    all_phrases.extend(IHRAM_PHRASES)
    all_phrases.extend(TAWAF_PHRASES)
    all_phrases.extend(SAI_PHRASES)
    all_phrases.extend(TAHALLUL_PHRASES)
    all_phrases.extend(MOSQUE_PHRASES)
    all_phrases.extend(PRACTICAL_PHRASES)
    all_phrases.extend(NUMBER_PHRASES)
    return all_phrases


def get_phrases_by_category(category: str) -> List[ArabicPhrase]:
    """Get phrases by category."""
    all_phrases = get_all_phrases()
    return [p for p in all_phrases if p.category == category]


def get_phrase_categories() -> List[str]:
    """Get all unique categories."""
    return [
        "greeting",
        "ihram",
        "tawaf",
        "sai",
        "tahallul",
        "mosque",
        "practical",
        "numbers"
    ]


def search_phrases(query: str) -> List[ArabicPhrase]:
    """Search phrases by keyword."""
    query = query.lower()
    all_phrases = get_all_phrases()
    
    results = []
    for phrase in all_phrases:
        if (query in phrase.arabic or
            query in phrase.transliteration.lower() or
            query in phrase.meaning_id.lower() or
            query in phrase.meaning_en.lower()):
            results.append(phrase)
    
    return results


def get_phrase_count() -> int:
    """Get total phrase count."""
    return len(get_all_phrases())


# Export for RAG
ARABIC_PHRASES_TEXT = "\n\n".join([
    f"**{p.transliteration}** ({p.arabic})\n"
    f"Arti: {p.meaning_id}\n"
    f"Konteks: {p.context}"
    for p in get_all_phrases()
])
