"""
LABBAIK AI v6.0 - Umrah Knowledge Base
=====================================
Comprehensive knowledge base for Umrah guidance.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field


# =============================================================================
# UMRAH GUIDE
# =============================================================================

UMRAH_OVERVIEW = """
# Panduan Lengkap Ibadah Umrah

## Apa itu Umrah?

Umrah adalah ibadah yang dilakukan dengan mengunjungi Ka'bah di Masjidil Haram, Makkah, 
dengan melaksanakan serangkaian ritual ibadah. Umrah sering disebut "haji kecil" 
dan dapat dilakukan kapan saja sepanjang tahun, berbeda dengan haji yang hanya 
dilaksanakan pada waktu tertentu.

## Perbedaan Umrah dan Haji

| Aspek | Umrah | Haji |
|-------|-------|------|
| Waktu | Sepanjang tahun | Bulan Dzulhijjah |
| Hukum | Sunnah Muakkadah | Wajib (sekali seumur hidup) |
| Rukun | 4 rukun | 6 rukun |
| Wukuf | Tidak ada | Ada (di Arafah) |
| Durasi | 2-3 jam | 5-6 hari |

## Keutamaan Umrah

1. Menghapus dosa-dosa kecil antara umrah yang satu dengan yang lainnya
2. Pahala seperti jihad di jalan Allah bagi wanita
3. Tamu Allah SWT yang doanya dikabulkan
4. Meningkatkan keimanan dan ketakwaan
"""

UMRAH_REQUIREMENTS = """
# Syarat dan Rukun Umrah

## Syarat Wajib Umrah

1. **Islam** - Wajib beragama Islam
2. **Baligh** - Sudah dewasa/baligh
3. **Berakal** - Dalam keadaan waras
4. **Merdeka** - Bukan budak
5. **Mampu** - Mampu secara fisik dan finansial

## Syarat Sah Umrah

1. **Islam**
2. **Mumayyiz** - Dapat membedakan yang baik dan buruk
3. **Ihram dari Miqat**

## 4 Rukun Umrah

### 1. Ihram (نية الإحرام)
Niat memasuki ibadah umrah dari miqat dengan memakai pakaian ihram.

**Tata Cara:**
- Mandi sunnah (ghusl)
- Memakai pakaian ihram (pria: 2 kain putih tanpa jahitan)
- Shalat sunnah ihram 2 rakaat
- Membaca niat: "Labbaika Allahumma 'Umratan"
- Membaca talbiyah

### 2. Tawaf (الطواف)
Mengelilingi Ka'bah sebanyak 7 kali putaran dimulai dari Hajar Aswad.

**Ketentuan:**
- Dimulai dari Hajar Aswad
- Ka'bah berada di sebelah kiri
- 7 putaran sempurna
- Dalam keadaan suci
- Menutup aurat

### 3. Sa'i (السعي)
Berjalan antara bukit Safa dan Marwah sebanyak 7 kali.

**Ketentuan:**
- Dimulai dari Safa
- Berakhir di Marwah
- Safa ke Marwah = 1 kali
- Total 7 kali perjalanan

### 4. Tahallul (التحلل)
Mencukur atau memotong rambut setelah selesai sa'i.

**Ketentuan:**
- Pria: mencukur habis (lebih utama) atau memendekkan
- Wanita: memotong ujung rambut sepanjang 1 ruas jari

## Wajib Umrah

1. **Ihram dari Miqat** - Memulai ihram dari tempat yang ditentukan
2. **Tidak melanggar larangan ihram**

## Sunah Umrah

1. Mandi sebelum ihram
2. Memakai minyak wangi sebelum ihram
3. Shalat 2 rakaat setelah ihram
4. Membaca talbiyah dengan keras (pria)
5. Raml (jalan cepat) pada 3 putaran pertama tawaf (pria)
6. Idhtiba' (membuka bahu kanan) saat tawaf (pria)
7. Istilam Hajar Aswad
8. Shalat 2 rakaat di belakang Maqam Ibrahim
9. Minum air Zamzam
10. Berlari kecil di antara tanda hijau saat sa'i (pria)
"""

IHRAM_GUIDE = """
# Panduan Lengkap Ihram

## Definisi Ihram

Ihram adalah niat memasuki ibadah haji atau umrah yang ditandai dengan 
memakai pakaian ihram dan membaca niat di miqat.

## Miqat (Tempat Memulai Ihram)

### Miqat Makani (Tempat)

1. **Dzul Hulaifah (Bir Ali)** - Untuk jamaah dari Madinah (450 km dari Makkah)
2. **Al-Juhfah (Rabigh)** - Untuk jamaah dari Mesir, Syam, Maghrib (187 km)
3. **Qarnul Manazil** - Untuk jamaah dari Najd (78 km)
4. **Yalamlam** - Untuk jamaah dari Yaman (120 km)
5. **Dzatu Irq** - Untuk jamaah dari Iraq (94 km)

### Miqat Zamani (Waktu)

Umrah dapat dilakukan sepanjang tahun.

## Tata Cara Ihram

### Persiapan

1. **Mandi Sunnah (Ghusl)**
   - Niat: "Nawaitul ghusla lil ihram"
   - Mandi seperti mandi junub

2. **Memotong Kuku dan Rambut**
   - Memotong kuku tangan dan kaki
   - Mencukur bulu ketiak dan kemaluan
   - Merapikan kumis (pria)

3. **Memakai Wewangian**
   - Diperbolehkan sebelum niat ihram
   - Tidak boleh setelah niat ihram

### Pakaian Ihram

**Pria:**
- 2 lembar kain putih tidak berjahit
- Rida' (selempang/selendang) untuk bahu
- Izar (kain bawahan) untuk pinggang ke bawah
- Sandal yang tidak menutupi mata kaki

**Wanita:**
- Pakaian biasa yang menutup aurat
- Tidak harus putih
- Tidak boleh memakai cadar dan sarung tangan
- Wajah dan telapak tangan terbuka

### Shalat Sunnah Ihram

- 2 rakaat setelah memakai pakaian ihram
- Rakaat 1: Al-Fatihah + Al-Kafirun
- Rakaat 2: Al-Fatihah + Al-Ikhlas

### Niat Ihram

**Untuk Umrah:**
```
لَبَّيْكَ اللَّهُمَّ عُمْرَةً
"Labbaika Allahumma 'Umratan"
"Aku penuhi panggilan-Mu ya Allah untuk umrah"
```

### Talbiyah

```
لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ، لَبَّيْكَ لاَ شَرِيكَ لَكَ لَبَّيْكَ، 
إِنَّ الْحَمْدَ وَالنِّعْمَةَ لَكَ وَالْمُلْكَ، لاَ شَرِيكَ لَكَ

"Labbaik Allahumma labbaik, labbaik la syarika laka labbaik,
innal hamda wan ni'mata laka wal mulk, la syarika lak"

"Aku penuhi panggilan-Mu ya Allah, aku penuhi panggilan-Mu,
aku penuhi panggilan-Mu, tidak ada sekutu bagi-Mu,
sesungguhnya segala puji, nikmat dan kerajaan adalah milik-Mu,
tidak ada sekutu bagi-Mu"
```

## Larangan Ihram

### Untuk Pria dan Wanita

1. Memotong atau mencabut rambut
2. Memotong kuku
3. Memakai wewangian
4. Berburu binatang darat
5. Menikah atau menikahkan
6. Berhubungan suami istri
7. Bermesraan yang membangkitkan syahwat
8. Memotong pohon di tanah haram

### Khusus Pria

1. Memakai pakaian berjahit
2. Menutup kepala dengan sesuatu yang melekat

### Khusus Wanita

1. Memakai cadar
2. Memakai sarung tangan

## Dam (Denda) Pelanggaran

| Pelanggaran | Dam |
|-------------|-----|
| Mencukur rambut (dengan udzur) | Puasa 3 hari / sedekah 6 fakir miskin / menyembelih kambing |
| Memakai pakaian berjahit | Puasa 3 hari / sedekah 6 fakir miskin / menyembelih kambing |
| Memakai wewangian | Puasa 3 hari / sedekah 6 fakir miskin / menyembelih kambing |
| Berhubungan suami istri (sebelum tahallul awal) | Umrah batal + menyembelih unta |
"""

TAWAF_GUIDE = """
# Panduan Lengkap Tawaf

## Definisi Tawaf

Tawaf adalah mengelilingi Ka'bah sebanyak 7 kali putaran dimulai dari 
Hajar Aswad dengan Ka'bah berada di sebelah kiri.

## Jenis-Jenis Tawaf

1. **Tawaf Qudum** - Tawaf kedatangan (sunnah)
2. **Tawaf Ifadhah** - Tawaf rukun haji
3. **Tawaf Wada'** - Tawaf perpisahan (wajib haji)
4. **Tawaf Umrah** - Rukun umrah
5. **Tawaf Sunnah** - Tawaf tambahan

## Syarat Sah Tawaf

1. Islam
2. Berakal (tidak gila)
3. Niat
4. Suci dari hadats besar dan kecil
5. Suci dari najis (badan, pakaian, tempat)
6. Menutup aurat
7. Di dalam Masjidil Haram
8. Ka'bah di sebelah kiri
9. 7 putaran sempurna
10. Dimulai dari Hajar Aswad

## Tata Cara Tawaf

### Persiapan

1. Berwudhu
2. Menutup aurat
3. Niat tawaf

### Memulai Tawaf

**Posisi Awal:**
- Berdiri sejajar dengan Hajar Aswad
- Batas: garis coklat di lantai

**Istilam (Menyentuh/Mengisyaratkan ke Hajar Aswad):**

Jika bisa menyentuh:
- Sentuh dengan tangan kanan
- Cium Hajar Aswad
- Ucapkan: "Bismillahi Allahu Akbar"

Jika tidak bisa menyentuh:
- Hadapkan telapak tangan ke Hajar Aswad
- Ucapkan: "Bismillahi Allahu Akbar"
- Cium telapak tangan

### Putaran Tawaf

**Putaran 1-3 (Raml - khusus pria):**
- Jalan cepat dengan langkah pendek
- Menggerakkan bahu
- Idhtiba' (buka bahu kanan)

**Putaran 4-7:**
- Jalan biasa

### Doa Tawaf

**Antara Rukun Yamani dan Hajar Aswad:**
```
رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ

"Rabbana atina fid-dunya hasanah, wa fil-akhirati hasanah, 
wa qina 'adzab an-nar"

"Ya Tuhan kami, berilah kami kebaikan di dunia dan kebaikan 
di akhirat, dan lindungilah kami dari siksa neraka"
```

**Doa Bebas:**
- Boleh berdoa dengan bahasa apa saja
- Boleh berdzikir, membaca Al-Quran

### Setelah Tawaf

**Shalat 2 Rakaat di Belakang Maqam Ibrahim:**
- Rakaat 1: Al-Fatihah + Al-Kafirun
- Rakaat 2: Al-Fatihah + Al-Ikhlas
- Jika tidak bisa di Maqam Ibrahim, boleh di mana saja di Masjidil Haram

**Minum Air Zamzam:**
- Berdoa sebelum minum
- Minum dengan posisi berdiri
- Menghadap kiblat
- Minum sampai puas

## Hal yang Membatalkan Tawaf

1. Hadats (besar atau kecil)
2. Keluar dari Masjidil Haram saat tawaf
3. Berjalan di dalam Hijr Ismail
4. Putaran tidak sempurna

## Tips Tawaf

1. Pilih waktu yang tidak terlalu ramai
2. Gunakan kursi roda jika kesulitan berjalan
3. Wanita haid menunggu suci dahulu
4. Jaga barang-barang berharga
5. Tetap fokus pada ibadah, hindari selfie
"""

SAI_GUIDE = """
# Panduan Lengkap Sa'i

## Definisi Sa'i

Sa'i adalah berjalan dari bukit Safa ke bukit Marwah dan sebaliknya 
sebanyak 7 kali, sebagai rukun umrah dan haji.

## Sejarah Sa'i

Sa'i mengikuti jejak Siti Hajar yang berlari-lari antara Safa dan Marwah 
mencari air untuk putranya, Nabi Ismail AS, hingga Allah SWT memancarkan 
air Zamzam.

## Syarat Sah Sa'i

1. Dilakukan setelah tawaf
2. Dimulai dari Safa
3. Berakhir di Marwah
4. 7 kali perjalanan (Safa-Marwah = 1)
5. Dilakukan di Mas'a (tempat sa'i)
6. Dilakukan dengan berjalan (jika mampu)

## Tata Cara Sa'i

### Memulai dari Safa

**Di Bukit Safa:**
```
إِنَّ الصَّفَا وَالْمَرْوَةَ مِنْ شَعَائِرِ اللهِ

"Innas-Safa wal-Marwata min sya'a'irillah"
"Sesungguhnya Safa dan Marwah adalah sebagian dari syi'ar Allah"
```

**Menghadap Ka'bah:**
- Angkat kedua tangan
- Ucapkan takbir 3x: "Allahu Akbar, Allahu Akbar, Allahu Akbar"
- Tahlil: "La ilaha illallah"
- Berdoa dengan doa bebas

### Berjalan ke Marwah

**Perjalanan:**
- Safa ke Marwah = perjalanan ke-1
- Marwah ke Safa = perjalanan ke-2
- Dan seterusnya hingga ke-7

**Berlari Kecil (Khusus Pria):**
- Di antara dua tanda lampu hijau
- Sekitar 50 meter
- Wanita tetap berjalan biasa

### Di Bukit Marwah

- Menghadap Ka'bah
- Berdoa seperti di Safa
- Tidak perlu membaca ayat lagi

### Doa Selama Sa'i

Tidak ada doa khusus, boleh berdoa bebas:

```
رَبِّ اغْفِرْ وَارْحَمْ وَاهْدِنِي السَّبِيلَ الأَقْوَمَ

"Rabbighfir warham wahdinis-sabilal aqwam"
"Ya Tuhanku, ampunilah, rahmatilah, dan tunjukilah 
jalan yang paling lurus"
```

## Hitungan Sa'i

| No | Dari | Ke | 
|----|------|-----|
| 1 | Safa | Marwah |
| 2 | Marwah | Safa |
| 3 | Safa | Marwah |
| 4 | Marwah | Safa |
| 5 | Safa | Marwah |
| 6 | Marwah | Safa |
| 7 | Safa | Marwah |

**Total: 7 kali, berakhir di Marwah**

## Ketentuan Tambahan

### Boleh:

1. Tidak dalam keadaan suci (wudhu tidak wajib, tapi sunnah)
2. Wanita haid boleh sa'i
3. Menggunakan kursi roda
4. Istirahat sebentar jika lelah
5. Minum di tengah sa'i

### Tidak Boleh:

1. Memotong perjalanan dengan keluar dari Mas'a
2. Meninggalkan sa'i terlalu lama tanpa udzur
3. Memulai dari Marwah

## Setelah Sa'i

Setelah sa'i selesai, langsung tahallul (memotong/mencukur rambut) 
untuk menyelesaikan umrah.
"""

TAHALLUL_GUIDE = """
# Panduan Tahallul

## Definisi Tahallul

Tahallul adalah mencukur atau memotong rambut setelah menyelesaikan 
sa'i sebagai tanda selesainya ibadah umrah.

## Ketentuan Tahallul

### Untuk Pria

**Mencukur Habis (Halq) - Lebih Utama:**
- Mencukur seluruh rambut kepala
- Pahala lebih besar (Rasulullah SAW mendoakan 3x untuk yang mencukur)

**Memendekkan (Taqshir):**
- Memotong rambut minimal sepanjang 1 ruas jari
- Dari seluruh bagian kepala

### Untuk Wanita

**Memotong Ujung Rambut (Taqshir):**
- Memotong ujung rambut sepanjang 1 ruas jari (sekitar 2-3 cm)
- Kumpulkan rambut, potong ujungnya
- Wanita tidak boleh mencukur habis

## Tata Cara Tahallul

1. Selesai sa'i di Marwah
2. Niat tahallul
3. Baca: "Bismillah, Allahu Akbar"
4. Cukur atau potong rambut
5. Umrah selesai

## Tempat Tahallul

- Boleh di Mas'a (setelah sa'i)
- Boleh di tukang cukur sekitar Masjidil Haram
- Boleh di hotel

## Setelah Tahallul

Setelah tahallul, semua larangan ihram menjadi halal kembali:

1. Boleh memakai pakaian biasa
2. Boleh memakai wewangian
3. Boleh memotong kuku
4. Boleh mencukur rambut lainnya
5. Boleh berhubungan suami istri

## Tips Tahallul

1. Pria disunnahkan mencukur habis untuk pahala lebih besar
2. Jika tidak menemukan tukang cukur, boleh saling mencukur
3. Rambut yang dicukur tidak perlu dikubur
4. Pastikan memotong dari seluruh bagian kepala

## Doa Setelah Tahallul

```
الْحَمْدُ لِلَّهِ الَّذِي قَضَى عَنَّا نُسُكَنَا، اللَّهُمَّ اجْعَلْهُ حَجًّا مَبْرُورًا 
وَسَعْيًا مَشْكُورًا وَذَنْبًا مَغْفُورًا

"Alhamdulillahilladzi qadha 'anna nusukana, Allahumma-j'alhu 
hajjan mabruran, wa sa'yan masykuran, wa dzanban maghfuran"

"Segala puji bagi Allah yang telah menyelesaikan ibadah kami,
Ya Allah jadikanlah haji yang mabrur, sa'i yang diterima,
dan dosa yang diampuni"
```
"""

# =============================================================================
# ARABIC PHRASES
# =============================================================================

ARABIC_PHRASES = [
    {
        "id": 1,
        "category": "Salam & Sapaan",
        "arabic": "السَّلَامُ عَلَيْكُمْ",
        "transliteration": "Assalamu'alaikum",
        "meaning": "Semoga keselamatan atas kalian",
        "response": "Wa'alaikumussalam (Dan semoga keselamatan atas kalian juga)"
    },
    {
        "id": 2,
        "category": "Salam & Sapaan",
        "arabic": "صَبَاحُ الْخَيْرِ",
        "transliteration": "Shabahul khair",
        "meaning": "Selamat pagi",
        "response": "Shabahun nuur (Pagi yang terang)"
    },
    {
        "id": 3,
        "category": "Salam & Sapaan",
        "arabic": "مَسَاءُ الْخَيْرِ",
        "transliteration": "Masa'ul khair",
        "meaning": "Selamat sore/malam",
        "response": "Masa'un nuur"
    },
    {
        "id": 4,
        "category": "Talbiyah",
        "arabic": "لَبَّيْكَ اللَّهُمَّ لَبَّيْكَ",
        "transliteration": "Labbaik Allahumma labbaik",
        "meaning": "Aku penuhi panggilan-Mu ya Allah",
        "context": "Dibaca saat ihram dan selama perjalanan"
    },
    {
        "id": 5,
        "category": "Doa",
        "arabic": "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً",
        "transliteration": "Rabbana atina fid-dunya hasanah",
        "meaning": "Ya Tuhan kami, berilah kami kebaikan di dunia",
        "context": "Doa antara Rukun Yamani dan Hajar Aswad"
    },
    {
        "id": 6,
        "category": "Percakapan",
        "arabic": "كَمْ الثَّمَنُ؟",
        "transliteration": "Kam ats-tsaman?",
        "meaning": "Berapa harganya?",
        "context": "Saat berbelanja"
    },
    {
        "id": 7,
        "category": "Percakapan",
        "arabic": "أَيْنَ الْحَرَمُ؟",
        "transliteration": "Ainal haram?",
        "meaning": "Di mana Masjidil Haram?",
        "context": "Bertanya arah"
    },
    {
        "id": 8,
        "category": "Percakapan",
        "arabic": "شُكْرًا جَزِيلًا",
        "transliteration": "Syukran jazilan",
        "meaning": "Terima kasih banyak",
        "context": "Mengucapkan terima kasih"
    },
    {
        "id": 9,
        "category": "Percakapan",
        "arabic": "عَفْوًا",
        "transliteration": "'Afwan",
        "meaning": "Sama-sama / Maaf",
        "context": "Merespons terima kasih atau meminta maaf"
    },
    {
        "id": 10,
        "category": "Percakapan",
        "arabic": "مِنْ فَضْلِكَ",
        "transliteration": "Min fadhlika",
        "meaning": "Tolong / Mohon",
        "context": "Meminta dengan sopan"
    },
    {
        "id": 11,
        "category": "Angka",
        "arabic": "وَاحِدٌ، اِثْنَانِ، ثَلَاثَةٌ",
        "transliteration": "Wahid, itsnan, tsalatsah",
        "meaning": "Satu, dua, tiga",
        "context": "Berhitung"
    },
    {
        "id": 12,
        "category": "Tempat",
        "arabic": "أَيْنَ الْحَمَّامُ؟",
        "transliteration": "Ainal hammam?",
        "meaning": "Di mana toilet?",
        "context": "Bertanya lokasi toilet"
    },
    {
        "id": 13,
        "category": "Tempat",
        "arabic": "أَيْنَ الْفُنْدُقُ؟",
        "transliteration": "Ainal funduq?",
        "meaning": "Di mana hotel?",
        "context": "Bertanya lokasi hotel"
    },
    {
        "id": 14,
        "category": "Makanan",
        "arabic": "أُرِيدُ مَاءً",
        "transliteration": "Uridu ma'an",
        "meaning": "Saya mau air",
        "context": "Memesan air minum"
    },
    {
        "id": 15,
        "category": "Makanan",
        "arabic": "الْحِسَابُ مِنْ فَضْلِكَ",
        "transliteration": "Al-hisab min fadhlika",
        "meaning": "Minta bon/bill",
        "context": "Di restoran"
    },
    {
        "id": 16,
        "category": "Darurat",
        "arabic": "سَاعِدْنِي",
        "transliteration": "Sa'idni",
        "meaning": "Tolong saya",
        "context": "Meminta pertolongan"
    },
    {
        "id": 17,
        "category": "Darurat",
        "arabic": "أَحْتَاجُ طَبِيبًا",
        "transliteration": "Ahtaju thabiban",
        "meaning": "Saya butuh dokter",
        "context": "Kondisi darurat kesehatan"
    },
    {
        "id": 18,
        "category": "Dzikir",
        "arabic": "سُبْحَانَ اللهِ",
        "transliteration": "Subhanallah",
        "meaning": "Maha Suci Allah",
        "context": "Dzikir / takjub"
    },
    {
        "id": 19,
        "category": "Dzikir",
        "arabic": "الْحَمْدُ لِلَّهِ",
        "transliteration": "Alhamdulillah",
        "meaning": "Segala puji bagi Allah",
        "context": "Dzikir / syukur"
    },
    {
        "id": 20,
        "category": "Dzikir",
        "arabic": "اللهُ أَكْبَرُ",
        "transliteration": "Allahu Akbar",
        "meaning": "Allah Maha Besar",
        "context": "Dzikir / takbir"
    },
]


# =============================================================================
# FAQ
# =============================================================================

FAQ_DATA = [
    {
        "question": "Berapa lama waktu yang dibutuhkan untuk umrah?",
        "answer": "Ritual umrah itu sendiri (tawaf, sa'i, tahallul) dapat dilakukan dalam 2-3 jam. Namun, paket umrah biasanya 9-12 hari termasuk ziarah ke Madinah."
    },
    {
        "question": "Apakah wanita haid boleh umrah?",
        "answer": "Wanita haid boleh melakukan semua ibadah umrah KECUALI tawaf. Ia harus menunggu suci dahulu untuk tawaf. Sa'i boleh dilakukan saat haid."
    },
    {
        "question": "Berapa biaya umrah dari Indonesia?",
        "answer": "Biaya umrah bervariasi mulai dari Rp 25-50 juta untuk paket reguler, hingga Rp 100 juta+ untuk paket VIP. Harga tergantung musim, hotel, dan fasilitas."
    },
    {
        "question": "Kapan waktu terbaik untuk umrah?",
        "answer": "Musim reguler (di luar Ramadan dan musim haji) lebih hemat dan tidak terlalu ramai. Umrah di Ramadan lebih utama pahalanya namun lebih mahal dan ramai."
    },
    {
        "question": "Apa yang harus dipersiapkan sebelum umrah?",
        "answer": "Dokumen (paspor, visa), vaksinasi (meningitis wajib), persiapan fisik (latihan jalan), persiapan mental (niat ikhlas), dan mempelajari tata cara umrah."
    },
    {
        "question": "Apakah anak-anak boleh umrah?",
        "answer": "Boleh, namun umrah anak yang belum baligh tidak menggugurkan kewajiban umrah setelah baligh. Pastikan anak sudah cukup umur untuk mengikuti ritual."
    },
    {
        "question": "Bagaimana jika batal wudhu saat tawaf?",
        "answer": "Jika batal wudhu saat tawaf, segera berwudhu dan lanjutkan dari putaran yang tertinggal, tidak perlu mengulang dari awal."
    },
    {
        "question": "Apakah boleh umrah sendirian tanpa travel?",
        "answer": "Boleh (umrah mandiri), namun perlu persiapan lebih matang. Wanita disunnahkan bersama mahram. Umrah mandiri cocok untuk yang berpengalaman."
    },
    {
        "question": "Apa perbedaan hotel bintang 3 dan 5 di Makkah?",
        "answer": "Perbedaan utama adalah jarak ke Masjidil Haram dan fasilitas. Hotel bintang 5 biasanya sangat dekat (bisa jalan kaki), sedangkan bintang 3 mungkin perlu transportasi."
    },
    {
        "question": "Bagaimana cara mendapatkan visa umrah?",
        "answer": "Visa umrah diurus oleh travel agent terakreditasi Kemenag. Syaratnya: paspor berlaku min. 6 bulan, foto, sertifikat vaksin meningitis, dan booking dari travel agent."
    },
]


# =============================================================================
# PACKING LIST
# =============================================================================

PACKING_LIST = {
    "documents": [
        "Paspor (masa berlaku min. 6 bulan)",
        "Visa umrah",
        "Tiket pesawat (print & digital)",
        "Bukti booking hotel",
        "Kartu vaksinasi meningitis",
        "Fotokopi paspor (3 lembar)",
        "Pas foto 4x6 dan 3x4 (background putih)",
        "Kartu identitas (KTP)",
        "Kartu BPJS/asuransi kesehatan",
    ],
    "clothing_men": [
        "Pakaian ihram (2 set)",
        "Baju koko / gamis (3-4 pcs)",
        "Celana panjang (3-4 pcs)",
        "Kaos dalam (5-6 pcs)",
        "Celana dalam (5-6 pcs)",
        "Sandal jepit",
        "Sepatu/sandal gunung nyaman",
        "Peci/kopiah",
        "Sabuk ihram",
        "Jaket tipis",
    ],
    "clothing_women": [
        "Mukena (2-3 set)",
        "Gamis/abaya (3-4 pcs)",
        "Jilbab/khimar (4-5 pcs)",
        "Kaos kaki (5-6 pasang)",
        "Dalaman gamis",
        "Sandal nyaman",
        "Sepatu untuk jalan jauh",
        "Manset/handsock",
        "Ciput/inner jilbab",
    ],
    "toiletries": [
        "Sabun & shampoo",
        "Sikat gigi & pasta gigi",
        "Deodoran (non-alkohol untuk ihram)",
        "Handuk kecil",
        "Tisu basah & kering",
        "Sunblock (non-wangi)",
        "Lip balm",
        "Sisir",
        "Gunting kuku",
        "Alat cukur",
    ],
    "health": [
        "Obat pribadi",
        "Obat maag",
        "Obat diare",
        "Obat flu & demam",
        "Vitamin",
        "Koyo/balsem",
        "Plester luka",
        "Masker medis",
        "Hand sanitizer",
        "Minyak angin",
    ],
    "electronics": [
        "Handphone & charger",
        "Power bank",
        "Adapter colokan (Saudi: Type G)",
        "Earphone",
        "Kamera (opsional)",
    ],
    "others": [
        "Koper besar",
        "Tas kecil/sling bag",
        "Kacamata hitam",
        "Payung lipat",
        "Botol minum",
        "Snack ringan",
        "Buku doa/panduan umrah",
        "Tasbih",
        "Sajadah travel",
        "Uang tunai (Riyal Saudi)",
        "Kantong plastik",
    ],
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_guides() -> Dict[str, str]:
    """Get all guide content."""
    return {
        "overview": UMRAH_OVERVIEW,
        "requirements": UMRAH_REQUIREMENTS,
        "ihram": IHRAM_GUIDE,
        "tawaf": TAWAF_GUIDE,
        "sai": SAI_GUIDE,
        "tahallul": TAHALLUL_GUIDE,
    }


def get_arabic_phrases(category: str = None) -> List[Dict]:
    """Get Arabic phrases, optionally filtered by category."""
    if category:
        return [p for p in ARABIC_PHRASES if p["category"].lower() == category.lower()]
    return ARABIC_PHRASES


def get_faq() -> List[Dict]:
    """Get FAQ data."""
    return FAQ_DATA


def get_packing_list() -> Dict[str, List[str]]:
    """Get packing list."""
    return PACKING_LIST


def search_knowledge(query: str) -> List[Dict[str, Any]]:
    """
    Simple keyword search in knowledge base.
    
    Args:
        query: Search query
    
    Returns:
        List of matching content
    """
    query_lower = query.lower()
    results = []
    
    # Search in guides
    guides = get_all_guides()
    for name, content in guides.items():
        if query_lower in content.lower():
            results.append({
                "type": "guide",
                "name": name,
                "content": content[:500] + "...",
                "relevance": content.lower().count(query_lower)
            })
    
    # Search in FAQ
    for faq in FAQ_DATA:
        if query_lower in faq["question"].lower() or query_lower in faq["answer"].lower():
            results.append({
                "type": "faq",
                "question": faq["question"],
                "answer": faq["answer"],
                "relevance": 1
            })
    
    # Search in Arabic phrases
    for phrase in ARABIC_PHRASES:
        if (query_lower in phrase["meaning"].lower() or 
            query_lower in phrase["transliteration"].lower()):
            results.append({
                "type": "phrase",
                "data": phrase,
                "relevance": 1
            })
    
    # Sort by relevance
    results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
    
    return results[:10]
