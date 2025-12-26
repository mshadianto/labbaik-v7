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

# =============================================================================
# HOTEL BOOKING TIPS
# =============================================================================

HOTEL_BOOKING_TIPS = """
# Tips Booking Hotel untuk Umrah

## Penting: Konfirmasi Langsung ke Hotel Setelah Booking OTA

Setelah booking melalui OTA (Agoda, Booking.com, Traveloka, dll),
**SANGAT DISARANKAN** untuk menghubungi hotel secara langsung dan konfirmasi reservasi Anda.

### Mengapa Harus Konfirmasi Langsung?

1. **Menghindari Overbooking** - OTA kadang oversell, hotel penuh saat check-in
2. **Memastikan Tipe Kamar** - Request khusus (connecting room, high floor, dll)
3. **Konfirmasi Harga** - Pastikan tidak ada hidden charge
4. **Jarak ke Masjid** - Tanyakan pintu terdekat ke Haram
5. **Layanan Shuttle** - Apakah tersedia, gratis atau berbayar

### Informasi yang Harus Disiapkan

Saat menghubungi hotel, siapkan informasi berikut:

| Data | Contoh |
|------|--------|
| **Booking Number** | AG-123456789 (dari OTA) |
| **Booking Reservation Number (BRN)** | HRN-2025-001234 (dari hotel) |
| **Tanggal Check-in** | 15 Januari 2025 |
| **Tanggal Check-out** | 20 Januari 2025 |
| **Nama Tamu** | Muhammad Ahmad (sesuai paspor) |
| **Jumlah Kamar** | 2 kamar |
| **Tipe Kamar** | Deluxe Double, Haram View |
| **Jumlah Tamu** | 4 orang dewasa |
| **Request Khusus** | Connecting room, non-smoking |

### Template Email Konfirmasi ke Hotel

```
Subject: Booking Confirmation Request - [Booking Number] - [Nama Anda]

Dear [Nama Hotel] Reservation Team,

I would like to confirm my upcoming reservation:

Booking Reference (OTA): [Nomor Booking dari OTA]
Guest Name: [Nama sesuai Paspor]
Check-in Date: [Tanggal]
Check-out Date: [Tanggal]
Room Type: [Tipe Kamar]
Number of Rooms: [Jumlah]
Number of Guests: [Jumlah]

Could you please:
1. Confirm my reservation is active
2. Provide the Hotel Confirmation Number / BRN
3. Confirm the room rate includes [breakfast/taxes/etc]
4. Advise which gate is nearest to your hotel

Special Request: [Connecting room / High floor / Early check-in / dll]

Thank you for your assistance.

Best regards,
[Nama Anda]
[Nomor WhatsApp]
```

### Kontak Hotel Populer di Makkah

| Hotel | Telepon | Email |
|-------|---------|-------|
| Hilton Suites Makkah | +966 12 531 7777 | makkah.suites@hilton.com |
| Raffles Makkah Palace | +966 12 571 9800 | makkah@raffles.com |
| Swissotel Makkah | +966 12 571 8888 | makkah@swissotel.com |
| Pullman Zamzam | +966 12 571 4000 | h8779@accor.com |
| Conrad Makkah | +966 12 577 4444 | makkah.info@conradhotels.com |
| Makkah Clock Tower | +966 12 571 2500 | - |
| Al Marwa Rayhaan | +966 12 571 1111 | - |
| Marriott Jabal Omar | +966 12 539 5555 | - |

### Kontak Hotel Populer di Madinah

| Hotel | Telepon | Email |
|-------|---------|-------|
| Oberoi Madinah | +966 14 818 3888 | reservations.madinah@oberoigroup.com |
| Anwar Al Madinah Movenpick | +966 14 818 1818 | hotel.madinah@movenpick.com |
| Dar Al Taqwa | +966 14 826 0000 | - |
| Shaza Al Madina | +966 14 828 1111 | - |
| Crowne Plaza Madinah | +966 14 827 5555 | madinah@ihg.com |
| Millennium Al Aqeeq | +966 14 366 3333 | - |

### Tips Memilih Hotel

1. **Jarak ke Masjid** - Prioritas utama! Hotel dekat bisa jalan kaki
2. **Pintu Terdekat** - Tanyakan pintu Haram mana yang terdekat
3. **Fasilitas** - Laundry, restoran halal, shuttle, wifi
4. **Review** - Baca review terbaru, terutama dari jamaah Indonesia
5. **Harga** - Bandingkan OTA vs booking langsung ke hotel

### Waktu Terbaik Booking

- **3-6 bulan sebelumnya** untuk harga terbaik
- **Hindari Ramadan & musim haji** jika ingin hemat
- **Weekday check-in** biasanya lebih murah

### Red Flags - Tanda Hotel Bermasalah

1. Tidak merespons email/telepon dalam 48 jam
2. Tidak bisa memberikan BRN/confirmation number
3. Meminta pembayaran di luar OTA
4. Review banyak yang komplain tentang reservasi hilang
5. Harga terlalu murah dibanding kompetitor
"""

# =============================================================================
# HIDDEN GEMS MAKKAH & MADINAH
# =============================================================================

HIDDEN_GEMS_MAKKAH = """
# Hidden Gems di Makkah Al-Mukarramah

Selain ibadah umrah, Makkah menyimpan banyak tempat bersejarah yang
jarang dikunjungi turis. Berikut hidden gems yang wajib dikunjungi:

## 1. Jabal Nur (Gua Hira)
**Lokasi:** 4 km dari Masjidil Haram

Tempat Nabi Muhammad SAW menerima wahyu pertama. Mendaki ke puncak
membutuhkan 1-2 jam. Pemandangan Makkah dari atas sangat indah.

**Tips:**
- Berangkat subuh untuk menghindari panas
- Bawa air yang cukup
- Pakai sepatu gunung
- Tidak disarankan untuk lansia

---

## 2. Jabal Tsur (Gua Tsur)
**Lokasi:** Selatan Makkah, 5 km dari Haram

Tempat persembunyian Nabi SAW dan Abu Bakar saat hijrah ke Madinah.
Lebih sulit didaki daripada Jabal Nur (2-3 jam).

**Kisah:**
Di sinilah laba-laba membuat sarang dan burung merpati bertelur
untuk melindungi Rasulullah dari kafir Quraisy.

---

## 3. Maqbarah Al-Ma'la (Pemakaman Jannat Al-Mu'alla)
**Lokasi:** Dekat Masjidil Haram, arah Mina

Pemakaman tertua di Makkah. Di sini dimakamkan:
- Khadijah binti Khuwailid (istri pertama Nabi)
- Abdul Muthalib (kakek Nabi)
- Abu Talib (paman Nabi)
- Abdullah bin Abdul Muthalib (ayah Nabi) - menurut sebagian riwayat

**Tips:** Ziarah setelah Subuh, lebih sepi

---

## 4. Masjid Jin
**Lokasi:** Dekat Maqbarah Al-Ma'la

Tempat di mana jin-jin mendengarkan bacaan Al-Quran dari Nabi SAW.
Masjid kecil namun penuh sejarah.

---

## 5. Masjid Tan'im (Miqat Aisyah)
**Lokasi:** 7 km dari Masjidil Haram

Miqat terdekat dari Makkah untuk umrah kedua.
Dinamakan Miqat Aisyah karena Aisyah RA memulai ihram dari sini.

**Tips:** Banyak tersedia travel murah dari sekitar Haram

---

## 6. Arafah (Di Luar Musim Haji)
**Lokasi:** 20 km dari Makkah

Berkunjung ke Jabal Rahmah dan Masjid Namira di luar musim haji.
Suasana lebih tenang untuk berdoa.

---

## 7. Muzdalifah & Mina
**Lokasi:** Antara Makkah dan Arafah

Di luar musim haji, Anda bisa melihat Jamarat dan mempelajari
jalur haji. Area ini biasanya sepi.

---

## 8. Hudaibiyah (Masjid Hudaibiyah)
**Lokasi:** Di perbatasan wilayah haram

Tempat bersejarah Perjanjian Hudaibiyah. Sayangnya masjid lama
sudah direnovasi, tapi tetap layak dikunjungi.

---

## 9. Maktabah Makkah Al-Mukarramah
**Lokasi:** Dekat Masjidil Haram

Perpustakaan Islam dengan koleksi manuskrip kuno dan buku langka.
Cocok untuk pencinta sejarah Islam.

---

## 10. Bir Tuwa (Sumur Tuwa)
**Lokasi:** Daerah Zahir, Makkah

Tempat Nabi SAW bermalam sebelum memasuki Makkah saat Fathu Makkah.

---

## Kuliner Hidden Gems Makkah

### 1. Al Baik
Ayam goreng legendaris Saudi. Cabang terdekat Haram di Kudai Road.

### 2. Shawarma Street (Jarwal)
Area dengan banyak kedai shawarma autentik, lebih murah dari sekitar Haram.

### 3. Souq Al Khalil
Pasar tradisional untuk oleh-oleh dengan harga lokal.

### 4. Restoran Yaman di Aziziyah
Nasi Mandi dan Madfun autentik dengan harga terjangkau.

### 5. Buah Segar di Pasar Al-Sitteen
Kurma, tin, dan buah-buahan segar dengan harga grosir.

---

## Cafe & Tempat Healing di Makkah

Setelah ibadah yang melelahkan, istirahat sejenak di cafe untuk recharge:

### 1. Starbucks Abraj Al-Bait (Clock Tower)
**Lokasi:** Mall Abraj Al-Bait, lantai 4
- View langsung ke Ka'bah dari jendela
- Buka 24 jam
- Wifi gratis, cocok untuk kerja remote
- **Tips:** Datang setelah Isya untuk suasana tenang

### 2. Caffe Nero - Jabal Omar
**Lokasi:** Jabal Omar Development
- Suasana modern dan cozy
- Outdoor seating dengan view kota
- Kopi dan pastry berkualitas

### 3. The Coffee Bean & Tea Leaf
**Lokasi:** Hilton Convention Center
- AC sejuk, tempat luas
- Cocok untuk istirahat lama
- Banyak colokan listrik

### 4. Costa Coffee - Makkah Mall
**Lokasi:** Makkah Mall, lantai dasar
- Suasana rileks jauh dari keramaian Haram
- Food court lengkap di sekitarnya
- Free parking mall

### 5. Angelina Paris - Raffles Makkah
**Lokasi:** Raffles Makkah Palace
- Cafe mewah dengan French pastry
- Hot chocolate signature legendary
- Perfect untuk treat yourself
- **Harga:** Premium tapi worth it

### 6. Paul Bakery - Swissotel
**Lokasi:** Swissotel Makkah
- French bakery & cafe
- Croissant dan pain au chocolat fresh
- Breakfast set lengkap

### 7. Tim Hortons - Multiple Locations
**Lokasi:** Kudai Road, Aziziyah
- Kopi Canada dengan harga terjangkau
- Donut dan Timbits favorit
- Drive-thru available

### 8. Rooftop Cafe - Makkah Towers
**Lokasi:** Makkah Towers Hotel
- View malam Makkah yang spektakuler
- Shisha tersedia (outdoor)
- Suasana santai malam hari

### 9. Brew92 - Jabal Omar
**Lokasi:** Jabal Omar Hyatt
- Local specialty coffee
- Single origin beans
- Barista skilled, latte art bagus
- Vibe anak muda Saudi

### 10. Food Court Clock Tower
**Lokasi:** Abraj Al-Bait Mall, lantai 2-3
- Berbagai pilihan makanan & minuman
- AC kuat, istirahat dari panas
- View Ka'bah dari beberapa spot
"""

HIDDEN_GEMS_MADINAH = """
# Hidden Gems di Madinah Al-Munawwarah

Kota Nabi yang penuh berkah. Selain Masjid Nabawi, banyak tempat
bersejarah yang menunggu untuk dijelajahi.

## 1. Masjid Quba
**Lokasi:** 5 km dari Masjid Nabawi

Masjid pertama dalam Islam yang dibangun Nabi SAW.
Shalat 2 rakaat di sini = pahala satu umrah!

**Tips:**
- Datang hari Sabtu (sunnah Nabi)
- Shalat 2 rakaat tahiyyatul masjid
- Gratis shuttle dari beberapa hotel

---

## 2. Masjid Qiblatain
**Lokasi:** 4 km dari Masjid Nabawi

Masjid tempat turunnya perintah mengubah kiblat dari Baitul Maqdis
ke Ka'bah. Arsitektur unik dengan dua mihrab.

---

## 3. Uhud dan Makam Syuhada
**Lokasi:** 5 km utara Masjid Nabawi

Lokasi Perang Uhud. Ziarahi makam Hamzah bin Abdul Muthalib (paman Nabi)
dan para syuhada lainnya.

**Yang Harus Dilihat:**
- Jabal Uhud (gunung merah)
- Jabal Rumat (tempat pemanah)
- Makam Syuhada Uhud

**Tips:**
- Jangan memanjat gunung (menghormati)
- Berdoa untuk para syuhada
- Bawa payung (sangat panas)

---

## 4. Masjid Sab'ah (Tujuh Masjid)
**Lokasi:** Dekat Khandaq

Kompleks 7 masjid kecil di lokasi Perang Khandaq.
Masing-masing punya sejarah tersendiri.

---

## 5. Makam Baqi (Jannatul Baqi)
**Lokasi:** Tepat di samping Masjid Nabawi

Pemakaman para sahabat Nabi dan keluarga Nabi SAW:
- Utsman bin Affan
- Hasan bin Ali
- Fatimah binti Muhammad (sebagian riwayat)
- Para istri Nabi (Ummahatul Mukminin)
- Banyak sahabat dan tabi'in

**Waktu Ziarah:**
- Pria: Setelah shalat Subuh dan Ashar
- Wanita: Tidak diperbolehkan masuk

---

## 6. Bir (Sumur) Romah
**Lokasi:** Quba area

Sumur yang dibeli Utsman bin Affan dan diwakafkan untuk umat Islam.
Airnya konon menyembuhkan.

---

## 7. Masjid Ghamama
**Lokasi:** Dekat Masjid Nabawi

Tempat Nabi SAW shalat Ied. Dinamakan Ghamama (awan) karena
awan pernah menaungi Nabi saat shalat.

---

## 8. Kebun Kurma Madinah
**Lokasi:** Sekitar Quba dan Uhud

Kunjungi perkebunan kurma dan cicipi kurma Ajwa segar langsung
dari pohonnya (musim panen: Juni-Agustus).

**Jenis Kurma Madinah:**
- **Ajwa** - Kurma Nabi, mencegah racun dan sihir
- **Sukkari** - Manis seperti gula
- **Safawi** - Lembut dan manis
- **Mabroom** - Panjang dan chewy
- **Khudri** - Ekonomis tapi enak

---

## 9. Museum Dar Al-Madinah
**Lokasi:** Pusat kota Madinah

Museum sejarah Islam dengan koleksi:
- Replika Masjid Nabawi zaman dulu
- Artefak era Nabi
- Sejarah perkembangan Madinah

---

## 10. Wadi Al-Aqiq
**Lokasi:** Barat Madinah

Lembah indah yang sering disebut dalam hadits.
Tempat yang tenang untuk refleksi.

---

## Kuliner Hidden Gems Madinah

### 1. Restoran Al Romansiah (Sultan Road)
Nasi Kabsah dan Mandi terenak di Madinah.

### 2. Kurma Segar di Pasar Kurma
Beli langsung dari petani, jauh lebih murah.

### 3. Kedai Kopi Arab di Quba
Kopi Arab dengan kurma, suasana lokal autentik.

### 4. Roti Tamis di Sekitar Baqi
Roti Arab panas dengan madu, sarapan favorit jamaah.

### 5. Jus Delima Segar
Banyak penjual jus di sekitar Masjid Nabawi, sehat dan segar!

---

## Cafe & Tempat Healing di Madinah

Madinah punya banyak spot cozy untuk istirahat dan healing:

### 1. Starbucks Reserve - Al Noor Mall
**Lokasi:** Al Noor Mall
- Premium reserve coffee
- Interior mewah dan luas
- Quiet zone tersedia
- **Tips:** Weekday lebih sepi

### 2. Dunkin' Donuts - Central Area
**Lokasi:** King Fahd Road
- Buka 24 jam
- Kopi dan donat fresh
- Harga terjangkau
- Cocok sarapan cepat

### 3. Cafe Bateel - Oberoi Hotel
**Lokasi:** The Oberoi Madinah
- Kurma premium + kopi Arabia
- Suasana super mewah
- Gift box kurma bagus untuk oleh-oleh
- **Specialty:** Date latte

### 4. Caribou Coffee - Taibah Road
**Lokasi:** Dekat Masjid Nabawi Gate 21
- Walking distance dari Haram
- Tempat luas, AC kuat
- Cocok ngobrol santai

### 5. McCafe - Multiple Locations
**Lokasi:** King Fahd Road, Central Area
- 24 jam
- Budget friendly
- Wifi gratis

### 6. Gloria Jean's Coffees
**Lokasi:** Al Rashid Mega Mall
- Australian coffee chain
- Blended drinks enak
- Mall lengkap untuk healing shopping

### 7. The Roastery - Prince Sultan Road
**Lokasi:** Area komersial Prince Sultan
- Local specialty roaster
- Pour over & espresso based
- Beans bisa dibeli pulang
- Vibe hipster Madinah

### 8. Krispy Kreme - Quba Road
**Lokasi:** Quba Commercial Area
- Donat fresh daily
- Hot glazed original harus coba
- Coffee decent untuk accompany

### 9. Garden Cafe - Anwar Al Madinah
**Lokasi:** Anwar Al Madinah Movenpick
- Outdoor garden setting
- View taman hijau
- Suasana tenang untuk refleksi
- **Tips:** Sore hari paling enak

### 10. Second Cup - Taibah
**Lokasi:** Area universitas Taibah
- Coffee Canada
- Suasana anak muda
- Harga mahasiswa friendly

### 11. Rooftop Lounge - Dar Al Taqwa
**Lokasi:** Dar Al Taqwa Hotel lantai atas
- View panorama Madinah malam
- Fresh juice & mocktails
- Shisha area tersedia

### 12. Public Parks untuk Healing
**Lokasi:** Tersebar di Madinah
- **King Fahd Garden:** Taman luas, jogging track, free
- **Al Salam Park:** Dekat Quba, cocok sore
- **Prince Mohammad Park:** Playground untuk anak
"""

# =============================================================================
# TEMPAT OLEH-OLEH MURAH (MUMER)
# =============================================================================

OLEH_OLEH_MAKKAH = """
# Tempat Beli Oleh-Oleh Murah di Makkah

Jangan beli oleh-oleh di sekitar Haram! Harga bisa 2-3x lipat.
Pergi sedikit lebih jauh untuk harga yang jauh lebih murah.

## Pasar & Mall Murah

### 1. Souq Al-Khalil (Pasar Khalil)
**Lokasi:** Jalan Al Khalil, 10 menit dari Haram
**Jam Buka:** 09:00-23:00
- Pasar tradisional terbesar Makkah
- Harga grosir untuk tasbih, sajadah, parfum
- WAJIB TAWAR! Mulai dari 50% harga yang ditawarkan
- **Tips:** Datang pagi untuk pilihan lengkap

**Harga Patokan:**
| Barang | Harga Sekitar Haram | Harga Souq Khalil |
|--------|---------------------|-------------------|
| Tasbih kayu | 30-50 SAR | 10-15 SAR |
| Sajadah biasa | 40-60 SAR | 15-25 SAR |
| Parfum non-alkohol 50ml | 80-120 SAR | 30-50 SAR |
| Kurma Ajwa 1kg | 150-200 SAR | 80-120 SAR |

### 2. Bin Dawood Supermarket
**Lokasi:** Banyak cabang (Aziziyah, Kudai)
**Jam Buka:** 24 jam
- Supermarket modern, harga fixed (tidak perlu tawar)
- Kurma kemasan, coklat, kacang Arab
- ZamZam kemasan resmi
- **Tips:** Ada promo bundle untuk oleh-oleh

### 3. Al-Sitteen Street Market
**Lokasi:** Jalan Al-Sitteen (Jalan 60)
- Buah segar, kurma curah murah
- Baju koko & gamis harga grosir
- Perlengkapan haji/umrah lengkap
- **Harga:** 30-40% lebih murah dari area Haram

### 4. Makkah Mall
**Lokasi:** 15 menit dari Haram
- Mall modern dengan banyak pilihan
- Carrefour di basement (harga supermarket)
- Brand lokal seperti Al Baik, Kudu
- **Tips:** Ke Carrefour untuk coklat & snack

### 5. Souq Al-Arab (Pasar Arab)
**Lokasi:** Daerah Aziziyah
- Khusus parfum & attar (minyak wangi)
- Harga grosir, bisa beli satuan
- Botol parfum cantik untuk kado
- **Warning:** Pastikan non-alkohol jika untuk shalat

### 6. Abraj Mall (Clock Tower) - HINDARI untuk Oleh-oleh
**Catatan:** Mall ini sangat mahal! Hanya untuk healing/cafe.
Oleh-oleh di sini harga 2-3x lipat dari pasar.

## Tips Belanja Hemat

1. **Jangan beli hari pertama** - Survey dulu, bandingkan harga
2. **Beli di luar area Haram** - Minimal 1-2 km dari Masjidil Haram
3. **Tawar dengan sopan** - Mulai 50%, deal di 60-70%
4. **Beli grosir** - Ajak teman, beli banyak dapat diskon
5. **Bayar cash** - Kadang dapat diskon 5-10%
6. **Malam lebih murah** - Pedagang ingin cepat tutup
7. **Bawa kalkulator** - Hitung konversi SAR ke IDR

## Oleh-Oleh Wajib Beli

| Oleh-Oleh | Harga Wajar | Tempat Terbaik |
|-----------|-------------|----------------|
| Kurma Ajwa 1kg | 80-120 SAR | Souq Khalil |
| Air ZamZam 5L | 10-15 SAR | Bin Dawood |
| Tasbih 99 butir | 10-20 SAR | Souq Khalil |
| Sajadah Turkey | 20-40 SAR | Al-Sitteen |
| Parfum Oud 50ml | 40-80 SAR | Souq Al-Arab |
| Kacang Arab 1kg | 25-35 SAR | Bin Dawood |
| Siwak | 2-5 SAR | Semua pasar |
| Baju koko | 30-50 SAR | Al-Sitteen |
| Mukena | 50-100 SAR | Al-Sitteen |
"""

OLEH_OLEH_MADINAH = """
# Tempat Beli Oleh-Oleh Murah di Madinah

Madinah terkenal dengan kurma berkualitas. Beli kurma di sini,
bukan di Makkah! Harga dan kualitas lebih baik.

## Pasar & Mall Murah

### 1. Pasar Kurma Madinah (Date Market)
**Lokasi:** Dekat Masjid Nabawi (Bab Salam area)
**Jam Buka:** 08:00-23:00
- SURGA KURMA! Puluhan jenis kurma
- Bisa cicip sebelum beli
- Harga per kg, tawar dengan sopan
- **Tips:** Beli Ajwa dan Sukkari di sini

**Jenis Kurma & Harga:**
| Jenis | Per Kg | Keterangan |
|-------|--------|------------|
| Ajwa (Premium) | 100-150 SAR | Kurma Nabi, kualitas terbaik |
| Ajwa (Medium) | 60-80 SAR | Ukuran lebih kecil |
| Sukkari Rutab | 40-60 SAR | Lembut, manis sekali |
| Sukkari Kering | 30-40 SAR | Tahan lama |
| Safawi | 25-35 SAR | Mirip Ajwa, lebih murah |
| Mabroom | 20-30 SAR | Panjang, chewy |
| Khudri | 15-25 SAR | Ekonomis, enak |

### 2. Al Rashid Mega Mall
**Lokasi:** King Fahd Road
- Lulu Hypermarket di basement
- Kurma kemasan, oleh-oleh modern
- Parfum branded harga kompetitif
- **Tips:** Beli coklat & snack di sini

### 3. Souq Al-Madinah (Pasar Madinah)
**Lokasi:** Sekitar area Central
- Pasar tradisional authentic
- Tasbih, sajadah, jubah
- Harga lebih murah dari Makkah
- **Tips:** Pagi hari lebih lengkap

### 4. Al Noor Mall
**Lokasi:** Prince Abdul Majeed Road
- Danube supermarket
- Oleh-oleh kemasan praktis
- Souvenir official Madinah
- **Harga:** Fixed price, tidak perlu tawar

### 5. Taibah Commercial Center
**Lokasi:** Dekat Universitas Taibah
- Area grosir baju muslim
- Gamis, jubah, abaya murah
- Perlengkapan haji/umrah
- **Harga:** 40-50% lebih murah dari mall

### 6. Quba Market
**Lokasi:** Area Masjid Quba
- Pasar lokal, harga lokal
- Kurma langsung dari petani
- Suasana authentic Saudi
- **Tips:** Kombinasi dengan ziarah Quba

## Tips Khusus Beli Kurma

1. **Cicip dulu!** - Pedagang biasanya mempersilakan
2. **Periksa kesegaran** - Jangan terlalu kering atau basah
3. **Pilih kemasan vakum** - Lebih tahan lama untuk dibawa pulang
4. **Beli di Madinah** - Kualitas lebih baik dari Makkah
5. **Ajwa untuk ibadah** - Makan 7 butir pagi hari (sunnah)
6. **Sukkari untuk oleh-oleh** - Favorit orang Indonesia

## Oleh-Oleh Khas Madinah

| Oleh-Oleh | Harga Wajar | Tempat Terbaik |
|-----------|-------------|----------------|
| Kurma Ajwa 1kg | 80-120 SAR | Pasar Kurma |
| Kurma Sukkari 1kg | 35-50 SAR | Pasar Kurma |
| Kurma Mix 3kg box | 100-150 SAR | Lulu/Danube |
| Kismis Madinah | 30-40 SAR/kg | Pasar Kurma |
| Madu Arab | 50-100 SAR | Souq Madinah |
| Habatussauda | 20-30 SAR | Souq Madinah |
| Zaitun Arab | 25-40 SAR | Supermarket |
| Sorban/Shemagh | 15-30 SAR | Taibah Center |
"""

# =============================================================================
# TEMPAT MAKAN SELERA INDONESIA
# =============================================================================

MAKANAN_INDONESIA_MAKKAH = """
# Tempat Makan Selera Indonesia di Makkah

Kangen masakan Indonesia? Berikut tempat makan yang cocok di lidah!

## Restoran Indonesia

### 1. Restoran Sederhana
**Lokasi:** Aziziyah, dekat Bin Dawood
**Jam Buka:** 11:00-23:00
- Menu: Nasi Padang lengkap!
- Rendang, gulai, sambal ijo
- Harga: 25-40 SAR per porsi
- **Favorit:** Rendang + nasi + teh manis
- Owner orang Padang asli

### 2. Warung Jawa "Mbak Yuni"
**Lokasi:** Aziziyah area
**Jam Buka:** 10:00-22:00
- Menu: Soto ayam, rawon, nasi pecel
- Harga: 20-30 SAR
- Rasanya authentic Jawa Timur
- **Tips:** Pesan soto + tempe goreng

### 3. Dapur Sunda
**Lokasi:** Kudai Road
**Jam Buka:** 11:00-22:00
- Menu: Nasi timbel, sayur asem, ikan bakar
- Sambal terasi available!
- Harga: 25-35 SAR
- **Favorit:** Nasi timbel komplit

### 4. Restoran Minang "Pagi Sore"
**Lokasi:** Rusaifah
**Jam Buka:** 07:00-23:00
- Menu: Nasi kapau, gulai otak, dendeng
- Cabai ijo mantap
- Harga: 25-40 SAR
- Buka dari pagi (sarapan)

### 5. Mie Aceh "Bang Jali"
**Lokasi:** Aziziyah
**Jam Buka:** 12:00-midnight
- Menu: Mie Aceh basah/goreng, roti cane
- Harga: 20-30 SAR
- **Tips:** Minta level pedas sesuai selera
- Porsi besar!

### 6. Ayam Penyet "Surabaya"
**Lokasi:** Kudai area
**Jam Buka:** 11:00-22:00
- Menu: Ayam penyet, lele penyet, tempe
- Sambal authentic pedas
- Harga: 20-30 SAR
- **Favorit:** Ayam penyet + es teh

## Kedai Kopi & Jajanan Indonesia

### 7. Warung Kopi Indonesia
**Lokasi:** Aziziyah
- Kopi tubruk, kopi susu
- Gorengan: tahu, tempe, pisang
- Indomie available!
- Harga: 5-15 SAR

### 8. Toko Oleh-Oleh Indonesia
**Lokasi:** Beberapa lokasi di Aziziyah
- Jual makanan instant Indonesia
- Indomie, sambal ABC, kecap
- Snack Indonesia
- **Tips:** Beli kalau kangen banget

## Tips Makan Indonesia di Makkah

1. **Area Aziziyah** - Pusat kuliner Indonesia
2. **Tanya supir/guide** - Mereka tau tempat terbaru
3. **Review Google Maps** - Cek rating sebelum pergi
4. **Jam makan** - Hindari 12:00-14:00 (ramai)
5. **Bawa sambal sendiri** - Kalau mau lebih pedas
"""

MAKANAN_INDONESIA_MADINAH = """
# Tempat Makan Selera Indonesia di Madinah

Madinah juga punya banyak pilihan makanan Indonesia!

## Restoran Indonesia

### 1. Restoran Padang "Al Minang"
**Lokasi:** King Fahd Road, dekat Masjid Nabawi
**Jam Buka:** 10:00-23:00
- Menu: Nasi Padang komplit
- Rendang, ayam pop, gulai tunjang
- Harga: 25-40 SAR
- **Favorit:** Gulai kepala ikan
- Walking distance dari hotel

### 2. Warung Nusantara
**Lokasi:** Quba Road
**Jam Buka:** 11:00-22:00
- Menu: Multi-regional Indonesia
- Soto Betawi, rawon, sate
- Harga: 20-35 SAR
- **Tips:** Coba sate ayamnya

### 3. RM Simpang Raya
**Lokasi:** Central Madinah
**Jam Buka:** 10:00-22:00
- Menu: Masakan Padang
- Dendeng balado, gulai otak
- Sambal hijau fresh
- Harga: 25-40 SAR

### 4. Kedai Aceh Madinah
**Lokasi:** Prince Sultan Road
**Jam Buka:** 12:00-midnight
- Menu: Mie Aceh, nasi goreng Aceh
- Martabak, roti cane
- Harga: 20-30 SAR
- Buka sampai malam

### 5. Sate Madura "Pak Haji"
**Lokasi:** Sekitar Baqi
**Jam Buka:** 17:00-23:00
- Menu: Sate ayam, sate kambing
- Bumbu kacang homemade
- Harga: 20-30 SAR
- **Favorit:** Sate campur + lontong

### 6. Warung Jawa Timur
**Lokasi:** Area Uhud
**Jam Buka:** 10:00-21:00
- Menu: Rawon, soto, rujak cingur
- Authentic rasa Surabaya
- Harga: 20-30 SAR
- **Tips:** Pesan rawon + tempe bacem

## Makanan Halal Lainnya (Selera Indonesia)

### 7. Al Baik - Ayam Goreng
**Lokasi:** Banyak cabang
- Mirip KFC tapi lebih enak
- Favorit orang Indonesia
- Harga: 15-25 SAR
- Wajib coba sekali!

### 8. Shawarma ala Indonesia
**Lokasi:** Jarwal area
- Shawarma besar porsi Indonesia
- Bisa request kurangi bawang
- Harga: 8-15 SAR

### 9. Nasi Bukhari/Kabsa
**Lokasi:** Restoran lokal mana saja
- Nasi Arab mirip nasi kebuli
- Rasanya cocok lidah Indonesia
- Harga: 20-35 SAR
- **Tips:** Minta sambal tambahan

## Tips Makan Indonesia di Madinah

1. **Lebih banyak pilihan** dari Makkah
2. **Area Quba & King Fahd Road** - Pusat kuliner
3. **Delivery available** - Banyak pakai Jahez/Hungerstation
4. **Grup WhatsApp jamaah** - Sering share info tempat makan
5. **Makan bersama** - Lebih hemat pesan porsi besar

## Menu Favorit Jamaah Indonesia

| Menu | Restoran | Harga |
|------|----------|-------|
| Rendang | Padang Al Minang | 35 SAR |
| Mie Aceh | Kedai Aceh | 25 SAR |
| Soto Ayam | Warung Nusantara | 20 SAR |
| Sate Campur | Pak Haji | 25 SAR |
| Al Baik | Al Baik | 18 SAR |
| Ayam Penyet | Surabaya | 25 SAR |
"""

# Combine oleh-oleh dan makanan
OLEH_OLEH = {
    "makkah": OLEH_OLEH_MAKKAH,
    "madinah": OLEH_OLEH_MADINAH,
}

MAKANAN_INDONESIA = {
    "makkah": MAKANAN_INDONESIA_MAKKAH,
    "madinah": MAKANAN_INDONESIA_MADINAH,
}


# =============================================================================
# TIPS ZIARAH
# =============================================================================

TIPS_ZIARAH = """
## Tips Ziarah Hidden Gems

1. **Sewa Mobil/Taksi** - Lebih efisien untuk keliling
2. **Guide Lokal** - Banyak yang fasih bahasa Indonesia
3. **Waktu Terbaik** - Pagi (setelah Subuh) atau sore (setelah Ashar)
4. **Niat Ibadah** - Setiap ziarah adalah ibadah
5. **Dokumentasi** - Boleh foto di luar masjid, hormati aturan
"""

# Combine all hidden gems
HIDDEN_GEMS = {
    "makkah": HIDDEN_GEMS_MAKKAH,
    "madinah": HIDDEN_GEMS_MADINAH,
}


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
# TIPS & TRIK PACKING KOPER
# =============================================================================

TIPS_PACKING_KOPER = """
# Tips & Trik Packing Koper untuk Umrah

Koper muat lebih banyak, barang rapi, dan tidak overweight!

## 1. Teknik Melipat Pakaian

### Rolling Method (Gulung)
Teknik paling hemat tempat untuk pakaian kasual.

**Cara:**
1. Letakkan baju rata di permukaan datar
2. Lipat lengan ke dalam
3. Gulung dari bawah ke atas dengan ketat
4. Susun gulungan berdiri di koper

**Cocok untuk:**
- Kaos, kaos dalam
- Celana panjang casual
- Jilbab/kerudung
- Piyama

**Hemat ruang:** 30-40% lebih kecil dari lipatan biasa!

---

### Bundle Wrapping (Bungkus Tumpuk)
Untuk pakaian formal yang tidak boleh kusut.

**Cara:**
1. Letakkan baju terbesar di dasar (gamis/jubah)
2. Tumpuk baju lebih kecil di atasnya
3. Lipat semua bersamaan dari pinggir ke tengah
4. Hasilnya satu bundle kompak

**Cocok untuk:**
- Gamis, jubah, abaya
- Kemeja/baju koko formal
- Mukena set

---

### KonMari Folding (Lipat Berdiri)
Baju dilipat kecil persegi dan disusun berdiri.

**Cara:**
1. Lipat baju jadi persegi kecil
2. Susun berdiri di koper seperti file folder
3. Semua terlihat dari atas, mudah ambil

**Keuntungan:**
- Mudah cari baju tanpa acak-acak
- Koper tetap rapi selama perjalanan

---

## 2. Vacuum Bag - GAME CHANGER!

### Apa itu Vacuum Bag?
Plastik khusus yang bisa dikecilkan dengan membuang udara di dalamnya.

### Yang Perlu Dibawa:
| Barang | Harga | Beli di |
|--------|-------|---------|
| Vacuum bag set (5-10 pcs) | Rp 50-100k | Shopee/Tokopedia |
| Pompa tangan manual | Rp 20-50k | Sudah include set |
| Pompa elektrik mini (opsional) | Rp 80-150k | Lebih cepat |

### Cara Pakai:
1. Masukkan pakaian ke vacuum bag
2. Tutup resleting rapat-rapat
3. Buka katup udara
4. Pompa sampai kempes (2-3 menit)
5. Tutup katup

### Tips Vacuum Bag:
- **Jangan terlalu penuh** - Sisakan 20% ruang
- **Pisahkan per kategori** - 1 bag = 1 jenis (kaos, celana, dll)
- **Bawa pompa manual** - Untuk re-pack saat pulang
- **Hindari untuk baju formal** - Bisa kusut permanen
- **Cocok untuk:** Handuk, selimut, pakaian dalam, kaos

### Hasil:
- Hemat ruang **50-70%**
- 1 koper bisa muat barang 2 koper!
- Baju terlindung dari air & debu

---

## 3. Bawa Makanan Indonesia

### Wajib Bawa (Kangen Killer):

| Makanan | Kemasan | Tips |
|---------|---------|------|
| **Sambal sachet** | ABC/Indofood sachet | 10-20 sachet cukup |
| **Kecap manis** | Botol kecil 135ml | Bungkus plastik anti bocor |
| **Indomie** | 5-10 bungkus | Pilih yg cup lebih praktis |
| **Abon** | Kemasan kecil | Tahan lama, enak + nasi |
| **Kerupuk** | Kemasan kecil | Untuk teman makan |
| **Bon Cabe** | Sachet | Taburan pedas instan |
| **Teri kacang** | Toples kecil | Lauk tahan lama |
| **Rendang kemasan** | Retort/kaleng | Ready to eat |

### Tips Bawa Makanan:
1. **Plastik ziplock** - Bungkus semua makanan 2 lapis
2. **Taruh di tengah koper** - Lindungi dari benturan
3. **Jangan bawa cairan >100ml di kabin** - Kecap masuk bagasi!
4. **Deklarasi jika ditanya** - "Food for personal consumption"
5. **Hindari makanan berbau tajam** - Hormati sesama jamaah

### Makanan yang TIDAK BOLEH Dibawa:
- Buah segar
- Daging/ikan mentah
- Makanan tanpa label
- Cairan dalam jumlah besar

---

## 4. Organisasi Koper

### Pembagian Zona Koper:

```
┌─────────────────────────────────────┐
│  ATAS: Barang sering dipakai        │
│  - Perlengkapan mandi               │
│  - Baju ganti 1-2 hari pertama      │
│  - Dokumen penting                  │
├─────────────────────────────────────┤
│  TENGAH: Pakaian utama              │
│  - Vacuum bag pakaian               │
│  - Mukena/gamis                     │
│  - Baju koko/jubah                  │
├─────────────────────────────────────┤
│  BAWAH: Barang berat                │
│  - Sepatu (dalam plastik)           │
│  - Oleh-oleh (kurma, zamzam)        │
│  - Makanan Indonesia                │
└─────────────────────────────────────┘
```

### Packing Cube (Tas Organizer)
Beli set packing cube untuk organisasi lebih rapi:
- **Cube besar** - Pakaian utama
- **Cube sedang** - Pakaian dalam
- **Cube kecil** - Aksesoris, charger
- **Laundry bag** - Baju kotor terpisah

**Harga:** Rp 50-150k per set di marketplace

---

## 5. Tips Berat Koper

### Batas Bagasi Umum:
| Airline | Ekonomi | Bisnis |
|---------|---------|--------|
| Garuda | 30 kg | 40 kg |
| Saudi Airlines | 23 kg x2 | 32 kg x2 |
| Emirates | 30 kg | 40 kg |
| Lion Air | 20 kg | 30 kg |

### Tips Agar Tidak Overweight:

1. **Timbang sebelum berangkat**
   - Beli timbangan koper digital (Rp 50-100k)
   - Atau timbang di timbangan badan

2. **Pakai baju terberat saat di pesawat**
   - Jaket tebal
   - Sepatu berat
   - Gamis/jubah tebal

3. **Manfaatkan tas kabin**
   - Biasanya 7 kg
   - Taruh barang berat: laptop, buku, charger

4. **Siapkan tas lipat cadangan**
   - Untuk oleh-oleh pulang
   - Tas kain/nylon yang bisa dilipat kecil

5. **Beli oleh-oleh di hari terakhir**
   - Kurma dan zamzam berat!
   - Kalkulasi sisa space sebelum beli

---

## 6. Packing untuk Ihram

### Khusus Laki-laki:

**Tas Kecil Ihram (bawa ke pesawat):**
- Kain ihram 2 lembar
- Sabuk ihram
- Sandal jepit
- Deodoran non-parfum
- Buku doa kecil

**Tips:**
- Pakai ihram dari bandara Jeddah (sebelum miqat)
- Baju biasa taruh di tas, ambil setelah tahallul
- Bawa peniti/klip untuk kain ihram

### Khusus Perempuan:

**Tas Kecil Ibadah:**
- Mukena travel (1 set)
- Jilbab cadangan
- Kaos kaki
- Sajadah travel tipis
- Tasbih
- Hand sanitizer

---

## 7. Hack Packing Pro

### Space Saver Hacks:

1. **Gulung kaos kaki dalam sepatu**
   - Hemat space + jaga bentuk sepatu

2. **Isi botol kosmetik dari rumah**
   - Beli botol travel 100ml
   - Isi shampoo, sabun cair secukupnya

3. **Pakai baju multifungsi**
   - Gamis hitam bisa formal & casual
   - Jilbab warna netral match semua

4. **Bawa hanger lipat 2-3 pcs**
   - Untuk jemur handuk di hotel

5. **Sandal di luar koper**
   - Gantung di handle atau taruh di kantong luar

6. **Compress towel tablet**
   - Handuk kecil bentuk tablet
   - Tambah air = handuk normal
   - Hemat space luar biasa!

### Anti Kusut Hacks:

1. **Tissue paper di lipatan**
   - Taruh tissue di lipatan baju formal

2. **Gantung di kamar mandi**
   - Uap panas shower hilangkan kusut

3. **Setrika travel mini**
   - Beli setrika lipat (Rp 100-200k)
   - Atau steamer travel

---

## 8. Checklist Packing

### 3 Hari Sebelum:
- [ ] Cuci semua baju yang akan dibawa
- [ ] Kumpulkan dokumen (paspor, visa, tiket)
- [ ] Beli vacuum bag & packing cube
- [ ] Charge semua elektronik
- [ ] Beli sambal, kecap, snack

### 1 Hari Sebelum:
- [ ] Lipat & pack semua pakaian
- [ ] Vakum pakaian dengan vacuum bag
- [ ] Susun koper sesuai zona
- [ ] Timbang koper
- [ ] Siapkan tas kabin
- [ ] Siapkan outfit pesawat

### Hari H:
- [ ] Double check dokumen
- [ ] Cek charger & power bank
- [ ] Bawa snack untuk pesawat
- [ ] Kunci koper dengan TSA lock
- [ ] Foto isi koper (untuk klaim jika hilang)

---

## 9. Packing Pulang (Oleh-oleh)

### Antisipasi Space Oleh-oleh:

1. **Bawa koper kosong lipat**
   - Koper cabin tambahan
   - Atau tas duffel besar

2. **Pakai baju selama di sana**
   - Kurangi baju bersih yang dibawa pulang
   - Lebih banyak space untuk oleh-oleh

3. **Vacuum bag untuk baju kotor**
   - Compress baju kotor
   - Beri space untuk kurma & zamzam

4. **Kardus dari toko**
   - Banyak toko kasih kardus gratis
   - Untuk extra bagasi

### Berat Oleh-oleh Umum:
| Oleh-oleh | Berat |
|-----------|-------|
| Kurma 5 kg | 5.5 kg (with box) |
| Air Zamzam 10L | 10 kg |
| Sajadah 5 pcs | 2 kg |
| Tasbih 10 pcs | 0.5 kg |
| Parfum 5 botol | 1 kg |

### Tips:
- **Beli zamzam di Jeddah Airport** - Bisa check-in terpisah
- **Split kurma ke beberapa tas** - Jangan 1 koper penuh kurma
- **Tinggal baju lama** - Sumbang ke hotel/masjid
"""

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
