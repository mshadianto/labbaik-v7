<![CDATA[<div align="center">

# 🕋 LABBAIK AI v6.0

### Platform AI Perencanaan Umrah #1 Indonesia

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://labbaik-umrahplanner.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![PWA](https://img.shields.io/badge/PWA-Ready-5A0FC8?style=for-the-badge&logo=pwa&logoColor=white)](#-progressive-web-app-pwa)

**Super Boom Edition** 🚀

[Demo](https://labbaik-umrahplanner.streamlit.app) • [Dokumentasi](#-dokumentasi) • [Fitur](#-fitur-lengkap) • [Instalasi](#-instalasi) • [Kontribusi](#-kontribusi)

---

<img src="https://em-content.zobj.net/source/apple/354/kaaba_1f54b.png" width="120" alt="Ka'bah">

*Memudahkan Perjalanan Suci Anda dengan Teknologi AI*

</div>

---

## 📋 Daftar Isi

- [Tentang Project](#-tentang-project)
- [Fitur Lengkap](#-fitur-lengkap)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Instalasi](#-instalasi)
- [Konfigurasi](#-konfigurasi)
- [Struktur Project](#-struktur-project)
- [API Reference](#-api-reference)
- [Progressive Web App (PWA)](#-progressive-web-app-pwa)
- [WhatsApp Integration (WAHA)](#-whatsapp-integration-waha)
- [Database Schema](#-database-schema)
- [Deployment](#-deployment)
- [Roadmap](#-roadmap)
- [Kontribusi](#-kontribusi)
- [Tim Pengembang](#-tim-pengembang)
- [Lisensi](#-lisensi)

---

## 🎯 Tentang Project

**LABBAIK AI** adalah platform berbasis AI yang dirancang khusus untuk membantu umat Muslim Indonesia dalam merencanakan perjalanan Umrah. Dengan pendekatan *"Do Your Own Research"* (DYOR), platform ini memberikan informasi komprehensif, simulasi biaya, dan panduan lengkap untuk ibadah Umrah.

### 🌟 Visi
Menjadi platform perencanaan Umrah digital #1 di Indonesia yang memudahkan umat Muslim dalam mempersiapkan perjalanan suci mereka.

### 🎯 Misi
- Menyediakan informasi akurat tentang Umrah
- Membantu jamaah merencanakan budget dengan simulasi biaya
- Memberikan panduan manasik interaktif
- Memfasilitasi keamanan jamaah dengan fitur darurat
- Menghubungkan jamaah dengan rombongan yang sesuai

### ✨ Keunggulan
| Keunggulan | Deskripsi |
|------------|-----------|
| 🤖 **AI-Powered** | Chatbot cerdas untuk menjawab pertanyaan seputar Umrah |
| 📱 **PWA Ready** | Dapat diinstall seperti aplikasi native |
| 📴 **Offline Mode** | Akses doa & panduan tanpa internet |
| 🆘 **Emergency SOS** | Tombol darurat dengan integrasi WhatsApp |
| 🕋 **3D Interactive** | Simulasi Ka'bah 3D untuk pembelajaran manasik |
| 🔒 **Privacy First** | Data pengguna aman dan terenkripsi |

---

## ✨ Fitur Lengkap

### 🏠 Core Features

<table>
<tr>
<td width="50%">

#### 🤖 AI Assistant
- Chatbot berbasis LLM (Groq/OpenAI)
- Hybrid RAG System
- Sumber islami terverifikasi
- Multi-turn conversation
- Context-aware responses

</td>
<td width="50%">

#### 💰 Simulasi Biaya
- Kalkulasi real-time
- Breakdown detail per komponen
- Multi-currency support
- Perbandingan paket
- Export PDF/Excel

</td>
</tr>
<tr>
<td>

#### 👥 Umrah Bareng
- Cari rombongan sesuai tanggal
- Filter berdasarkan preferensi
- Sistem matching otomatis
- Chat group terintegrasi
- Review & rating

</td>
<td>

#### 🧭 Umrah Mandiri
- Panduan step-by-step
- Checklist persiapan
- Tips & trik lengkap
- Video tutorial
- FAQ comprehensive

</td>
</tr>
<tr>
<td>

#### 📦 Booking System
- Multi travel agent
- Real-time availability
- Secure payment gateway
- E-ticket generation
- Booking management

</td>
<td>

#### 📈 Analytics Dashboard
- Visitor statistics
- Page tracking
- User behavior analysis
- Performance metrics
- Export reports

</td>
</tr>
</table>

### 🆕 New Features (v6.0)

<table>
<tr>
<td width="50%">

#### 📊 Prediksi Keramaian
```
Prediksi level keramaian Masjidil Haram
dan Masjid Nabawi berdasarkan:
- Waktu sholat
- Hari dalam seminggu
- Musim (Ramadhan, Haji, reguler)
- Data historis
```
**Output:** Rekomendasi waktu terbaik untuk ibadah

</td>
<td width="50%">

#### 🆘 SOS Emergency
```
Sistem darurat satu ketukan:
- Kirim lokasi GPS real-time
- Notifikasi WhatsApp otomatis
- Kontak kedutaan & RS
- Group alert untuk rombongan
```
**Integrasi:** WAHA WhatsApp API

</td>
</tr>
<tr>
<td>

#### 📍 Group Tracking
```
Lacak anggota rombongan:
- Real-time location sharing
- Status online/offline
- Check-in di lokasi penting
- SOS alert ke ketua rombongan
- Battery level indicator
```
**Fitur:** Shareable group code

</td>
<td>

#### 🕋 Manasik 3D
```
Simulasi interaktif Ka'bah:
- 3D model dengan Three.js
- Titik penting (Hajar Aswad, dll)
- Panduan ritual step-by-step
- Progress tracker
- Doa setiap rukun
```
**Interactive:** Drag to rotate, scroll to zoom

</td>
</tr>
<tr>
<td>

#### 🔍 Smart Comparison
```
Bandingkan paket dengan AI:
- Multi-factor scoring
- Location score
- Comfort score
- Value score
- Personalized matching
```
**Algorithm:** Weighted scoring system

</td>
<td>

#### 🤲 Doa & Dzikir
```
Kumpulan doa lengkap:
- 6 kategori (30+ doa)
- Arabic + transliterasi + terjemahan
- Tasbih digital counter
- Offline available
- Bookmark favorites
```
**Categories:** Safar, Ihram, Thawaf, Sa'i, Umum, Dzikir

</td>
</tr>
<tr>
<td>

#### 📲 PWA Support
```
Progressive Web App:
- Installable di semua device
- Offline mode untuk doa
- Push notifications
- Home screen icon
- Fullscreen experience
```
**Supported:** Android, iOS, Desktop

</td>
<td>

#### 📱 WhatsApp Integration
```
WAHA API Integration:
- Auto-send SOS alerts
- Booking confirmation
- Group notifications
- Departure reminders
- Two-way messaging
```
**Platform:** Self-hosted WAHA

</td>
</tr>
</table>

### 📿 Tasbih Digital

<div align="center">

| Feature | Description |
|---------|-------------|
| 🔢 Counter | Hitung dzikir dengan tap |
| 🎯 Target | Pilih 33, 99, 100, atau 1000 |
| 🔄 Reset | Reset kapan saja |
| 🎉 Celebration | Balloons saat target tercapai |
| 📊 Progress | Visual progress bar |

</div>

---

## 🛠 Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) | Web Framework |
| ![Three.js](https://img.shields.io/badge/Three.js-000000?style=flat&logo=three.js&logoColor=white) | 3D Visualization |
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) | PWA & Components |
| ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) | Styling |

### Backend
| Technology | Purpose |
|------------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Core Language |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white) | Database (Neon) |
| ![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F61?style=flat) | Vector Search |

### AI/ML
| Technology | Purpose |
|------------|---------|
| ![Groq](https://img.shields.io/badge/Groq-00D4AA?style=flat) | LLM Provider |
| ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white) | Embeddings |
| ![LangChain](https://img.shields.io/badge/LangChain-121212?style=flat) | RAG Framework |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| ![Streamlit Cloud](https://img.shields.io/badge/Streamlit_Cloud-FF4B4B?style=flat&logo=streamlit&logoColor=white) | Hosting |
| ![WAHA](https://img.shields.io/badge/WAHA-25D366?style=flat&logo=whatsapp&logoColor=white) | WhatsApp API |
| ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white) | Version Control |

---

## 🚀 Instalasi

### Prerequisites

```bash
# Python 3.9 atau lebih tinggi
python --version  # Python 3.9+

# pip package manager
pip --version

# Git
git --version
```

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/labbaik-ai.git
cd labbaik-ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
# Edit secrets.toml dengan credentials Anda

# 5. Run application
streamlit run app.py
```

### Docker Installation

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

```bash
# Build dan run
docker build -t labbaik-ai .
docker run -p 8501:8501 labbaik-ai
```

---

## ⚙️ Konfigurasi

### Streamlit Secrets

Buat file `.streamlit/secrets.toml`:

```toml
# =============================================================================
# DATABASE
# =============================================================================
DATABASE_URL = "postgresql://user:password@host.neon.tech/dbname?sslmode=require"

# =============================================================================
# AI PROVIDERS
# =============================================================================
GROQ_API_KEY = "gsk_your_groq_api_key_here"
OPENAI_API_KEY = "sk-your_openai_api_key_here"  # Optional, untuk embeddings

# =============================================================================
# WHATSAPP (WAHA)
# =============================================================================
WAHA_API_URL = "https://your-waha-instance.com"
WAHA_API_KEY = ""  # Optional
WAHA_SESSION = "Labbaik"

# =============================================================================
# OPTIONAL SERVICES
# =============================================================================
# GOOGLE_MAPS_API_KEY = ""
# SENDGRID_API_KEY = ""
# SENTRY_DSN = ""
```

### Environment Variables

| Variable | Required | Description |
|----------|:--------:|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `GROQ_API_KEY` | ✅ | Groq API key untuk LLM |
| `OPENAI_API_KEY` | ❌ | OpenAI key untuk embeddings |
| `WAHA_API_URL` | ❌ | WAHA instance URL |
| `WAHA_SESSION` | ❌ | WAHA session name |

---

## 📁 Struktur Project

```
labbaik-ai/
│
├── 📄 app.py                      # Main entry point
├── 📄 requirements.txt            # Python dependencies
├── 📄 README.md                   # This file
├── 📄 LICENSE                     # MIT License
│
├── 📁 .streamlit/
│   ├── config.toml               # Streamlit config
│   └── secrets.toml              # Secrets (gitignored)
│
├── 📁 features/                   # Feature modules
│   ├── __init__.py
│   ├── crowd_prediction.py       # 📊 Crowd prediction
│   ├── sos_emergency.py          # 🆘 SOS system
│   ├── group_tracking.py         # 📍 Group tracking
│   ├── manasik_3d.py             # 🕋 3D Ka'bah
│   ├── smart_comparison.py       # 🔍 Package comparison
│   ├── doa_player.py             # 🤲 Doa & dzikir
│   ├── pwa_support.py            # 📲 PWA support
│   └── whatsapp_service.py       # 📱 WhatsApp integration
│
├── 📁 services/
│   ├── 📁 analytics/
│   │   ├── __init__.py
│   │   ├── tracker.py            # Page tracking
│   │   └── dashboard.py          # Analytics dashboard
│   │
│   ├── 📁 whatsapp/
│   │   ├── __init__.py
│   │   └── waha_client.py        # WAHA API client
│   │
│   ├── 📁 ai/
│   │   ├── __init__.py
│   │   ├── chat_engine.py        # LLM chat
│   │   └── rag_system.py         # RAG implementation
│   │
│   └── 📁 database/
│       ├── __init__.py
│       ├── connection.py         # DB connection
│       └── models.py             # Data models
│
├── 📁 ui/
│   ├── 📁 pages/
│   │   ├── home.py
│   │   ├── chat.py
│   │   ├── simulator.py
│   │   ├── umrah_mandiri.py
│   │   ├── umrah_bareng.py
│   │   └── booking.py
│   │
│   └── 📁 components/
│       ├── header.py
│       ├── sidebar.py
│       └── cards.py
│
├── 📁 data/
│   ├── doa_database.json         # Doa collection
│   ├── emergency_contacts.json   # Emergency contacts
│   └── sample_packages.json      # Sample packages
│
├── 📁 static/
│   ├── icons/                    # PWA icons
│   ├── images/                   # Static images
│   └── audio/                    # Audio files (future)
│
├── 📁 tests/
│   ├── test_features.py
│   ├── test_services.py
│   └── test_ui.py
│
└── 📁 docs/
    ├── screenshots/
    ├── api/
    └── guides/
```

---

## 📚 API Reference

### Features API

#### Crowd Prediction

```python
from features.crowd_prediction import CrowdPredictor, render_crowd_widget

# Initialize predictor
predictor = CrowdPredictor()

# Get prediction
level = predictor.predict(
    location="makkah",  # or "madinah"
    datetime=datetime.now()
)
# Returns: 0-100 (crowd level)

# Render widget
render_crowd_widget(location="makkah", compact=True)
```

#### SOS Emergency

```python
from features.sos_emergency import SOSService, EmergencyType

# Initialize service
sos = SOSService()

# Add emergency contact
sos.add_emergency_contact(
    name="Keluarga",
    phone="081234567890",
    relationship="Istri"
)

# Generate SOS message
message = sos.generate_sos_message(
    emergency_type=EmergencyType.MEDICAL,
    details="Butuh pertolongan medis"
)

# Get WhatsApp link
wa_link = sos.get_whatsapp_link(phone, message)
```

#### Group Tracking

```python
from features.group_tracking import GroupTrackingService

# Initialize service
tracking = GroupTrackingService()

# Create group
group = tracking.create_group(
    name="Rombongan Umrah 2025",
    leader_name="Ahmad"
)
# Returns: group with shareable code

# Join group
tracking.join_group(code="ABC123", name="Budi")

# Update location
tracking.update_my_location(
    latitude=-6.2088,
    longitude=106.8456
)
```

#### Doa Player

```python
from features.doa_player import UMRAH_DOAS, DoaCategory, render_doa_card

# Get doas by category
thawaf_doas = [d for d in UMRAH_DOAS if d.category == DoaCategory.TAWAF]

# Render single doa
render_doa_card(doa)

# Render full page
render_doa_player_page()
```

### Services API

#### WhatsApp (WAHA)

```python
from services.whatsapp import WhatsAppService

# Initialize
wa = WhatsAppService()

# Check availability
if wa.is_available:
    # Send text
    result = wa.client.send_text(
        phone="6281234567890",
        message="Test message"
    )
    
    # Send SOS alert
    wa.send_sos_alert(
        recipients=["6281234567890"],
        name="Ahmad",
        emergency_type="Darurat Medis",
        location="Masjidil Haram",
        latitude=21.4225,
        longitude=39.8262
    )
```

#### Analytics

```python
from services.analytics import track_page, get_visitor_stats

# Track page view
track_page("home")

# Get statistics
stats = get_visitor_stats()
# Returns: {total_visitors, today_visitors, page_views, etc.}
```

---

## 📲 Progressive Web App (PWA)

### Features

| Feature | Status | Description |
|---------|:------:|-------------|
| Installable | ✅ | Add to home screen |
| Offline Mode | ✅ | Cached content available |
| Push Notifications | 🔜 | Coming soon |
| Background Sync | 🔜 | Coming soon |

### Offline Available Content

- ✅ Semua doa & dzikir
- ✅ Panduan manasik
- ✅ 3D Ka'bah viewer
- ✅ Kontak darurat
- ✅ Checklist persiapan
- ❌ AI Chat (requires internet)
- ❌ Real-time tracking (requires internet)

### Installation Guide

<table>
<tr>
<td width="33%">

**Android (Chrome)**
1. Buka LABBAIK AI di Chrome
2. Tap menu ⋮ (3 titik)
3. Pilih "Add to Home Screen"
4. Tap "Install"
5. Done! 🎉

</td>
<td width="33%">

**iOS (Safari)**
1. Buka LABBAIK AI di Safari
2. Tap icon Share 📤
3. Scroll dan pilih "Add to Home Screen"
4. Tap "Add"
5. Done! 🎉

</td>
<td width="33%">

**Desktop (Chrome/Edge)**
1. Buka LABBAIK AI
2. Klik icon ⊕ di address bar
3. Klik "Install"
4. Done! 🎉

</td>
</tr>
</table>

---

## 📱 WhatsApp Integration (WAHA)

### Setup WAHA

1. **Deploy WAHA Instance**
   ```bash
   docker run -d \
     --name waha \
     -p 3000:3000 \
     devlikeapro/waha
   ```

2. **Create Session**
   - Buka WAHA Dashboard: `http://localhost:3000/dashboard`
   - Klik "Create Session"
   - Name: `Labbaik`
   - Klik "Start"
   - Scan QR Code dengan WhatsApp

3. **Configure in Streamlit**
   ```toml
   WAHA_API_URL = "http://your-waha-url:3000"
   WAHA_SESSION = "Labbaik"
   ```

### Message Templates

| Template | Trigger | Content |
|----------|---------|---------|
| SOS Alert | Emergency button | Location + emergency type + user info |
| Booking Confirmation | After booking | Package details + booking ID |
| Group Notification | Admin action | Group updates |
| Departure Reminder | Scheduled | Countdown + checklist |

---

## 🗄️ Database Schema

### Tables

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Visitor statistics
CREATE TABLE visitor_stats (
    id SERIAL PRIMARY KEY,
    page_name VARCHAR(100) NOT NULL UNIQUE,
    visit_count INTEGER DEFAULT 0,
    unique_visitors INTEGER DEFAULT 0,
    last_visited TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Travel groups
CREATE TABLE travel_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(6) UNIQUE NOT NULL,
    leader_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Group members
CREATE TABLE group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES travel_groups(id),
    user_id INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'active',
    last_location JSONB,
    last_seen TIMESTAMP
);
```

---

## 🚢 Deployment

### Streamlit Cloud (Recommended)

1. **Fork/Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`

3. **Configure Secrets**
   - Go to App Settings → Secrets
   - Paste your secrets.toml content

4. **Deploy!**
   - Click "Deploy"
   - Your app will be live at `https://your-app.streamlit.app`

### Docker Compose

```yaml
version: '3.8'
services:
  labbaik:
    build: .
    ports:
      - "8501:8501"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - GROQ_API_KEY=${GROQ_API_KEY}
    restart: unless-stopped
    
  waha:
    image: devlikeapro/waha
    ports:
      - "3000:3000"
    volumes:
      - waha_data:/app/.waha
    restart: unless-stopped

volumes:
  waha_data:
```

---

## 🗺️ Roadmap

### ✅ v6.0 (Current) - Super Boom Edition
- [x] Crowd Prediction
- [x] SOS Emergency + WhatsApp
- [x] Group Tracking
- [x] 3D Manasik
- [x] Smart Comparison
- [x] Doa & Dzikir Player
- [x] PWA Support
- [x] Analytics Dashboard

### 🔜 v6.1 (Q1 2025)
- [ ] Voice-guided doa (TTS)
- [ ] Push notifications
- [ ] Multi-language (EN, AR)
- [ ] Prayer time integration
- [ ] Weather forecast

### 🔮 v7.0 (Q2 2025)
- [ ] Native mobile app (Flutter)
- [ ] Real GPS tracking
- [ ] Augmented Reality guides
- [ ] Video call with mutawif
- [ ] Social features

---

## 🤝 Kontribusi

Kami sangat menghargai kontribusi dari komunitas!

### Cara Berkontribusi

1. **Fork** repository ini
2. **Create branch** untuk fitur Anda
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** perubahan Anda
   ```bash
   git commit -m 'feat: add amazing feature'
   ```
4. **Push** ke branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open Pull Request**

### Commit Convention

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting |
| `refactor` | Code refactoring |
| `test` | Adding tests |
| `chore` | Maintenance |

---

## 👨‍💻 Tim Pengembang

<div align="center">

| Role | Name | Contact |
|:----:|:----:|:-------:|
| **Founder & Lead Developer** | MS Hadianto | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourprofile) |
| **Company** | KIM Consulting | [![Website](https://img.shields.io/badge/Website-000000?style=flat&logo=About.me&logoColor=white)](https://kimconsulting.id) |

</div>

### Acknowledgments

Terinspirasi oleh:
- [PilgrimPal](https://pilgrimpal.net)
- [Nusuk](https://nusuk.sa)
- [Ibraheem AI](https://ibraheem.ai)
- [HajjGuide.ai](https://hajjguide.ai)

---

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

```
MIT License

Copyright (c) 2025 MS Hadianto / KIM Consulting

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">

### 🤲 Doa Penutup

*"Ya Allah, mudahkanlah perjalanan umrah bagi siapa saja yang menggunakan platform ini. Jadikanlah ibadah mereka mabrur dan diterima di sisi-Mu. Aamiin."*

---

**⭐ Star this repo if you find it helpful!**

---

Made with ❤️ and ☕ in Indonesia 🇮🇩

**LABBAIK AI** - *Memudahkan Perjalanan Suci Anda*

🕋

</div>
]]>