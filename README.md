# LABBAIK AI v7.4

### Platform AI Perencanaan Umrah #1 di Indonesia

**Enterprise Edition** - *Memudahkan Perjalanan Suci Anda dengan Teknologi AI*

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Demo Video

Lihat LABBAIK AI beraksi:

| Video | Link |
|-------|------|
| **Demo Live Session** | [![YouTube](https://img.shields.io/badge/YouTube-Live-red?logo=youtube)](https://www.youtube.com/live/sS7T6YqIJHI) |
| **Feature Walkthrough** | [![YouTube](https://img.shields.io/badge/YouTube-Watch-red?logo=youtube)](https://youtu.be/e1XsLF6aUaA) |

---

## Daftar Isi

1. [Tentang Project](#tentang-project)
2. [Fitur Unggulan v7.4](#fitur-unggulan-v74)
3. [Travel CRM System](#travel-crm-system)
4. [Tech Stack](#tech-stack)
5. [Struktur Project](#struktur-project)
6. [Instalasi](#instalasi)
7. [Konfigurasi](#konfigurasi)
8. [User Roles & Access Control](#user-roles--access-control)
9. [API Documentation](#api-documentation)
10. [Knowledge Base](#knowledge-base)
11. [Roadmap](#roadmap)

---

## Tentang Project

**LABBAIK AI** adalah platform inovatif berbasis Kecerdasan Buatan (AI) yang dirancang untuk mendampingi umat Muslim Indonesia dalam merencanakan perjalanan Umrah. Dengan semangat **DYOR (Do Your Own Research)**, kami menyediakan ekosistem digital yang transparan, informatif, dan aman.

### Visi & Misi

* **Visi:** Menjadi kompas digital utama bagi jamaah Umrah di seluruh Indonesia
* **Misi:** Digitalisasi manasik, transparansi biaya, dan peningkatan keamanan jamaah melalui teknologi AI

### Keunggulan Utama

* **AI Assistant** - Konsultasi ibadah & logistik 24/7
* **Smart Pricing** - Perbandingan harga real-time multi-platform
* **Knowledge Base** - Panduan lengkap umrah, tips hemat, hidden gems
* **Partner API** - REST API untuk integrasi travel agent
* **Multi-tier Access** - Role-based access control

---

## Fitur Unggulan v7.4

### Core Features

| Fitur | Deskripsi |
|-------|-----------|
| **AI Chat Assistant** | Tanya jawab seputar umrah dengan AI berbasis RAG |
| **Cost Simulator** | Kalkulasi budget dengan breakdown lengkap |
| **Package Comparison** | Bandingkan paket umrah dengan weighted scoring |
| **Crowd Prediction** | Prediksi kepadatan Masjidil Haram & Nabawi |
| **3D Manasik** | Visualisasi tawaf dan sa'i interaktif |

### Premium Features

| Fitur | Deskripsi |
|-------|-----------|
| **Real-time Tracking** | Pantau posisi jamaah rombongan |
| **SOS Emergency** | Tombol darurat dengan lokasi GPS |
| **Analytics Dashboard** | Statistik penggunaan dan insights |
| **Unlimited Chat** | Tanpa batas konsultasi AI |

### Partner Features

| Fitur | Deskripsi |
|-------|-----------|
| **Partner Dashboard** | Kelola paket dan booking |
| **Package Builder** | Rancang paket umrah dengan kalkulasi margin |
| **Travel CRM** | Kelola lead, booking, pembayaran, jamaah |
| **REST API** | Integrasi sistem booking |
| **Webhook Events** | Notifikasi real-time |
| **Commission Tracking** | Monitoring komisi |

### Intelligence Services (v1.1)

| Service | Deskripsi |
|---------|-----------|
| **Name Normalization** | Arabic/Latin transliteration untuk matching |
| **Currency Conversion** | Multi-currency (SAR, IDR, USD, dll) |
| **Risk Score** | Prediksi sold-out hotel (0-100) |

---

## Travel CRM System

Sistem CRM lengkap untuk travel agent mitra, mengelola seluruh operasional dari lead hingga keberangkatan.

### Modul CRM

| Modul | Fitur |
|-------|-------|
| **Dashboard Analytics** | KPI cards, lead funnel, revenue chart, payment status |
| **Lead Management** | Pipeline view, follow-up tracking, activity log |
| **Booking Tracker** | Manajemen booking, status pembayaran, cicilan |
| **Jamaah Database** | Data jamaah, document checklist, riwayat |
| **Quote Generator** | Generate penawaran dari Package Builder |
| **Invoice Generator** | Buat invoice DP, cicilan, pelunasan |
| **WA Broadcast** | Blast pesan ke leads/jamaah dengan template |
| **Competitor Monitor** | Pantau dan bandingkan harga kompetitor |

### Package Builder

Fitur untuk merancang paket umrah dengan kalkulasi otomatis:

- **Durasi:** 9, 12, 14 hari
- **Hotel:** Bintang 3-5 Makkah & Madinah
- **Penerbangan:** 7 maskapai, 8 kota keberangkatan
- **Transport:** Haramain train, bus VIP, private
- **Kamar:** Quad, triple, double, single
- **Makan:** Full board, half board, breakfast only
- **Margin:** Preset 10-25% atau custom
- **Season:** Low, regular, high, Ramadan multiplier

### Database Schema

```
leads              → Data prospek/calon jamaah
lead_activities    → Riwayat follow-up
jamaah             → Database jamaah
bookings           → Data booking
payments           → Riwayat pembayaran
documents          → Dokumen jamaah (paspor, KTP, dll)
quotes             → Penawaran/quote
invoices           → Invoice
broadcasts         → Campaign WA blast
competitor_prices  → Harga kompetitor
crm_analytics      → Event analytics
```

### Setup CRM Database

```bash
# Jalankan schema PostgreSQL
python scripts/init_crm_schema.py
```

---

## Tech Stack

### Core Technology

| Component | Technology |
|-----------|------------|
| Language | Python 3.9+ |
| Framework | Streamlit |
| Database | SQLite / PostgreSQL |
| Vector DB | ChromaDB |

### AI & Services

| Component | Technology |
|-----------|------------|
| LLM Engine | Groq (Llama 3) / OpenAI |
| Orchestration | LangChain |
| WhatsApp API | WAHA (Self-hosted) |

---

## Struktur Project

```
labbaik-v7/
├── app.py                      # Entry point
├── requirements.txt            # Dependencies
│
├── ui/                         # User Interface
│   ├── pages/                  # Page components
│   │   ├── home.py
│   │   ├── chat.py
│   │   ├── simulator.py
│   │   ├── package_builder.py  # Package Builder
│   │   ├── crm_analytics.py    # CRM Dashboard
│   │   ├── crm_leads.py        # Lead Management
│   │   ├── crm_bookings.py     # Booking Tracker
│   │   ├── crm_jamaah.py       # Jamaah Database
│   │   ├── crm_quotes.py       # Quote & Invoice
│   │   ├── crm_broadcast.py    # WA Broadcast
│   │   ├── crm_competitors.py  # Competitor Monitor
│   │   └── ...
│   └── components/             # Reusable components
│
├── services/                   # Business Logic
│   ├── ai/                     # AI & RAG services
│   ├── user/                   # User management
│   ├── crm/                    # CRM Services (NEW)
│   │   ├── __init__.py
│   │   ├── models.py           # Dataclass models
│   │   ├── config.py           # Config loader
│   │   └── repository.py       # Database operations
│   ├── subscription/           # Premium subscriptions
│   ├── partner_api/            # Partner API
│   └── intelligence/           # Intelligence services
│
├── features/                   # Feature modules
│   ├── crowd_prediction.py
│   ├── manasik_3d.py
│   └── sos_emergency.py
│
├── config/                     # Configuration files
│   ├── package_builder.yaml    # Package Builder config
│   └── travel_crm.yaml         # CRM config
│
├── sql/                        # Database schemas
│   └── travel_crm_schema.sql   # CRM tables
│
├── utils/                      # Utilities
│   └── package_calculator.py   # Package cost calculator
│
├── data/                       # Data & Knowledge
│   └── knowledge/
│
└── scripts/                    # Utility scripts
    ├── init_admin.py           # Admin initialization
    └── init_crm_schema.py      # CRM schema setup
```

---

## Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/mshadianto/labbaik-v7.git
cd labbaik-v7
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Admin

```bash
python scripts/init_admin.py
```

### 5. Initialize CRM Database (Optional)

```bash
python scripts/init_crm_schema.py
```

### 6. Run Application

```bash
streamlit run app.py
```

---

## Konfigurasi

### Environment Variables

Buat file `.streamlit/secrets.toml`:

```toml
# Database
DATABASE_URL = "sqlite:///data/labbaik.db"

# AI Services
GROQ_API_KEY = "gsk_your_key"
OPENAI_API_KEY = "sk_your_key"  # Optional

# WhatsApp (WAHA)
WAHA_API_URL = "http://localhost:3000"
WAHA_SESSION = "Labbaik"
```

### Admin Setup

Jalankan script untuk setup admin:

```bash
python scripts/init_admin.py
```

Atau set via environment variables:

```toml
# .streamlit/secrets.toml
ADMIN_EMAIL = "your_email@example.com"
ADMIN_PASSWORD = "your_secure_password"
```

> **Security Note:** Jangan commit credentials ke repository!

---

## User Roles & Access Control

### Role Hierarchy

| Role | Level | Description |
|------|-------|-------------|
| GUEST | 0 | Visitor tanpa login |
| FREE | 1 | User terdaftar gratis |
| PREMIUM | 2 | Subscriber berbayar |
| PARTNER | 3 | Travel agent partner |
| ADMIN | 4 | Full access |

### Feature Access Matrix

| Feature | Guest | Free | Premium | Partner | Admin |
|---------|-------|------|---------|---------|-------|
| Home & Landing | Y | Y | Y | Y | Y |
| AI Chat | - | 10/day | Unlimited | Unlimited | Unlimited |
| Cost Simulator | Y | Y | Y | Y | Y |
| Package Comparison | Y | Y | Y | Y | Y |
| Tracking | - | - | Y | Y | Y |
| Partner Dashboard | - | - | - | Y | Y |
| Admin Dashboard | - | - | - | - | Y |
| API Access | - | - | - | Y | Y |

### Subscription Plans

| Plan | Price | Duration |
|------|-------|----------|
| Monthly | Rp 99,000 | 30 days |
| Quarterly | Rp 249,000 | 90 days |
| Yearly | Rp 799,000 | 365 days |
| Lifetime | Rp 1,990,000 | Forever |

---

## API Documentation

### Base URL

```
https://api.labbaik.cloud/api/v1
```

### Authentication

```http
Authorization: Bearer lbk_live_xxxxxxxxxxxx
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/packages` | List all packages |
| GET | `/packages/{id}` | Get package detail |
| POST | `/bookings` | Create booking |
| GET | `/bookings/{code}` | Get booking status |
| GET | `/analytics/overview` | Partner analytics |

### Rate Limits

| Plan | Requests/Day |
|------|--------------|
| Silver | 1,000 |
| Gold | 10,000 |
| Enterprise | Unlimited |

---

## Knowledge Base

### Panduan Lengkap

| Topic | Content |
|-------|---------|
| **Manasik Umrah** | Ihram, Tawaf, Sa'i, Tahallul |
| **Tips Hemat** | Tiket, hotel, transport, akomodasi |
| **Hidden Gems** | Tempat wisata religi Makkah & Madinah |
| **Cafe & Healing** | Tempat nongkrong untuk recharge |
| **Oleh-oleh Murah** | Pasar & tips belanja hemat |
| **Makanan Indonesia** | Restoran Indonesia di Saudi |
| **Packing Tips** | Vacuum bag, melipat baju, checklist |

### Budget Comparison

| Item | Standard | Hemat | Savings |
|------|----------|-------|---------|
| Tiket | Rp 12 jt | Rp 7 jt | 42% |
| Hotel 9 malam | Rp 15 jt | Rp 7 jt | 53% |
| Transport | Rp 3 jt | Rp 1.5 jt | 50% |
| Makan | Rp 4 jt | Rp 2 jt | 50% |
| **TOTAL** | **Rp 34 jt** | **Rp 17.5 jt** | **49%** |

---

## Intelligence Services

### Name Normalization

```python
from services.intelligence import normalize_name, match_hotel_name

# Arabic to Latin
normalize_name("فندق هيلتون مكة")  # → "hilton mecca"

# Fuzzy matching
match_hotel_name("Hilton Mekah", candidates)
```

### Currency Conversion

```python
from services.intelligence import to_sar, to_idr, format_price_dual

to_sar(500, "USD")      # → 1875.0
to_idr(100, "SAR")      # → 425000
format_price_dual(500)  # → "500 SAR (Rp 2.125.000)"
```

### Risk Score

```python
from services.intelligence import compute_risk_score

risk = compute_risk_score("hotel-id", "MAKKAH", checkin_date)
# score: 75, level: HIGH, recommendation: "Book soon!"
```

---

## Roadmap

### Completed

- [x] v7.0 - Core platform & AI Chat
- [x] v7.1 - User management & access control
- [x] v7.2 - Subscription & referral system
- [x] v7.3 - Partner API & intelligence services
- [x] v7.4 - Travel CRM System & Package Builder

### Upcoming

- [ ] v7.5 - Real-time price aggregation
- [ ] v7.6 - Mobile app (React Native)
- [ ] v8.0 - AR navigation di Masjidil Haram

---

## Contributing

Kami mengundang developer untuk berkontribusi:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Commit Convention

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring

---

## Team

**Lead Developer:** MS Hadianto

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

### Doa Penutup

*"Ya Allah, mudahkanlah perjalanan umrah bagi siapa saja yang menggunakan platform ini. Jadikanlah ibadah mereka mabrur dan diterima di sisi-Mu. Aamiin."*

**Star repo ini jika bermanfaat!**

Made with love in Indonesia

</div>
