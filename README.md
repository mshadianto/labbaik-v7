# 🕋 LABBAIK AI v6.0

### Platform AI Perencanaan Umrah #1 di Indonesia

**Super Boom Edition** 🚀 — *Memudahkan Perjalanan Suci Anda dengan Teknologi AI*

**[Jelajahi Demo](https://labbaik-umrahplanner.streamlit.app)** • [Dokumentasi](https://www.google.com/search?q=%23-dokumentasi) • [Fitur](https://www.google.com/search?q=%23-fitur-lengkap) • [Instalasi](https://www.google.com/search?q=%23-instalasi) • [Kontribusi](https://www.google.com/search?q=%23-kontribusi)

---

## 📋 Daftar Isi

1. [Tentang Project](https://www.google.com/search?q=%23-tentang-project)
2. [Fitur Unggulan v6.0](https://www.google.com/search?q=%23-fitur-unggulan-v60)
3. [Tech Stack](https://www.google.com/search?q=%23-tech-stack)
4. [Struktur Folder](https://www.google.com/search?q=%23-struktur-project)
5. [Instalasi & Konfigurasi](https://www.google.com/search?q=%23-instalasi)
6. [Integrasi WhatsApp (WAHA)](https://www.google.com/search?q=%23-whatsapp-integration-waha)
7. [Roadmap Masa Depan](https://www.google.com/search?q=%23-roadmap)

---

## 🎯 Tentang Project

**LABBAIK AI** adalah platform inovatif berbasis Kecerdasan Buatan (AI) yang dirancang untuk mendampingi umat Muslim Indonesia dalam merencanakan perjalanan Umrah secara mandiri maupun berkelompok. Dengan semangat **DYOR (Do Your Own Research)**, kami menyediakan ekosistem digital yang transparan, informatif, dan aman.

### 🌟 Visi & Misi

* **Visi:** Menjadi kompas digital utama bagi jamaah Umrah di seluruh Indonesia.
* **Misi:** Digitalisasi manasik, transparansi biaya, dan peningkatan keamanan jamaah melalui teknologi *real-time tracking* dan AI.

### ✨ Keunggulan Utama

* 🤖 **AI Assistant:** Konsultasi ibadah & logistik 24/7.
* 📱 **PWA Ready:** Performa ringan, bisa di-install di HP tanpa melalui App Store.
* 🆘 **Safety First:** Integrasi tombol darurat SOS langsung ke WhatsApp Group.
* 🕋 **3D Experience:** Simulasi tawaf dan sa'i secara visual untuk persiapan mental.

---

## 🚀 Fitur Unggulan (v6.0)

### 📊 Dashboard Cerdas

| Fitur | Deskripsi |
| --- | --- |
| **Prediksi Keramaian** | Estimasi kepadatan Masjidil Haram & Nabawi menggunakan data historis & waktu shalat. |
| **Simulasi Biaya** | Kalkulasi budget real-time dengan breakdown komponen (Visa, Tiket, Hotel). |
| **Smart Comparison** | Algoritma *weighted scoring* untuk membandingkan paket travel secara objektif. |

### 🛡️ Keamanan & Pendampingan

* **SOS Emergency:** Satu ketukan untuk mengirim lokasi GPS & info medis ke tim pendukung via **WAHA API**.
* **Group Tracking:** Pantau posisi anggota rombongan secara *real-time* untuk meminimalisir jamaah terpisah.
* **Tasbih Digital:** Counter dzikir interaktif dengan visual progress dan perayaan saat target tercapai.

---

## 🛠 Tech Stack

### **Core Technology**

* **Language:** Python 3.9+
* **Web Framework:** Streamlit (Frontend & Backend)
* **Database:** PostgreSQL (Hosted on Neon)
* **Vector DB:** ChromaDB (Untuk RAG System)

### **AI & API Services**

* **LLM Engine:** Groq (Llama 3) / OpenAI
* **Orchestration:** LangChain
* **WhatsApp API:** WAHA (Self-hosted Docker)
* **3D Rendering:** Three.js Integration

---

## 📁 Struktur Project

```bash
labbaik-ai/
├── 📄 app.py                 # Entry point aplikasi
├── 📁 features/              # Modul fitur utama
│   ├── crowd_prediction.py   # Prediksi kepadatan
│   ├── manasik_3d.py        # Visualisasi Ka'bah
│   └── sos_emergency.py      # Logika SOS & WAHA
├── 📁 services/              # Integrasi sistem luar
│   ├── 📁 ai/                # RAG & Chat Engine
│   └── 📁 whatsapp/          # WAHA Client & Templates
├── 📁 ui/                    # Komponen antarmuka
│   ├── 📁 pages/             # Halaman-halaman aplikasi
│   └── 📁 components/        # Sidebar, Header, Cards
└── 📁 data/                  # Database lokal & JSON

```

---

## ⚙️ Instalasi & Setup

### **1. Clone & Environment**

```bash
git clone https://github.com/yourusername/labbaik-ai.git
cd labbaik-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

```

### **2. Konfigurasi Secrets**

Buat file `.streamlit/secrets.toml`:

```toml
DATABASE_URL = "postgresql://user:pass@host/dbname"
GROQ_API_KEY = "gsk_your_key"
WAHA_API_URL = "http://your-waha-instance:3000"
WAHA_SESSION = "Labbaik"

```

### **3. Running via Docker**

```bash
docker build -t labbaik-ai .
docker run -p 8501:8501 labbaik-ai

```

---

## 📱 WhatsApp Integration (WAHA)

Aplikasi ini menggunakan **WAHA (WhatsApp HTTP API)** untuk otomasi pesan.

* **SOS Alert:** Mengirim pesan otomatis: *"Darurat! [Nama] butuh bantuan di [Lokasi GPS]"*.
* **Konfirmasi Booking:** Mengirim detail PDF itinerary langsung ke nomor user.

> **Note:** Pastikan instance WAHA Anda sudah aktif dan terhubung dengan sesi WhatsApp aktif sebelum menjalankan fitur ini.

---

## 🗺️ Roadmap

* [x] **v6.0:** PWA Support & SOS Emergency.
* [ ] **v6.1 (Q1 2025):** Voice-guided doa (Text-to-Speech) & Multi-language support.
* [ ] **v7.0 (Q2 2025):** Augmented Reality (AR) untuk navigasi di area Masjidil Haram.

---

## 🤝 Kontribusi & Tim

Kami mengundang para developer untuk berkontribusi. Silakan ajukan *Pull Request* dengan mengikuti standar commit kami (`feat:`, `fix:`, `docs:`).

**Pengembang Utama:**

* **MS Hadianto** - Founder & Lead Developer ([LinkedIn](https://linkedin.com/in/yourprofile))

---

<div align="center">

### 🤲 Doa Penutup

*"Ya Allah, mudahkanlah perjalanan umrah bagi siapa saja yang menggunakan platform ini. Jadikanlah ibadah mereka mabrur dan diterima di sisi-Mu. Aamiin."*

**⭐ Star repo ini jika menurut Anda bermanfaat!**

Made with ❤️ in Indonesia 🇮🇩

</div>

