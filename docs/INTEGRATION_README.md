# 🕌 LABBAIK AI - Price Intelligence Integration

## Integrasi n8n Price Intelligence ke Streamlit App

### 📁 File yang Perlu Ditambahkan

```
labbaik-umrahplanner/
├── services/
│   └── price/                      # ← BUAT FOLDER INI
│       ├── __init__.py             # ← COPY
│       └── repository.py           # ← COPY
└── ui/
    └── components/
        └── price_widgets.py        # ← COPY
```

---

## 🚀 Langkah Integrasi

### Step 1: Copy File

Copy 3 file dari folder ini ke project kamu:

1. `services/price/__init__.py`
2. `services/price/repository.py`  
3. `ui/components/price_widgets.py`

### Step 2: Update Streamlit Cloud Secrets

Di Streamlit Cloud → Settings → Secrets, pastikan sudah ada:

```toml
DATABASE_URL = "postgresql://neondb_owner:YOUR_PASSWORD@ep-young-bush-a1hximj4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
```

### Step 3: Integrasi ke Halaman

---

## 📍 Contoh Integrasi

### A. Di Home Page (`ui/pages/home.py`)

```python
# Tambahkan di bagian atas
from ui.components.price_widgets import render_price_comparison_section, render_price_stats_widget

def render_home_page():
    st.title("🕋 LABBAIK AI")
    
    # ... existing code ...
    
    # Tambahkan section harga
    st.markdown("---")
    render_price_comparison_section()
```

### B. Di Simulator Page (`ui/pages/simulator.py`)

```python
# Tambahkan import
from ui.components.price_widgets import get_real_price_defaults, render_live_price_indicator

def render_simulator_page():
    st.title("💰 Simulasi Biaya Umrah")
    
    # Tampilkan status harga live
    render_live_price_indicator()
    
    # Ambil harga real dari database
    prices = get_real_price_defaults()
    
    # Gunakan untuk slider
    package_price = st.slider(
        "Estimasi Harga Paket",
        min_value=int(prices['package_min']),
        max_value=int(prices['package_max']),
        value=int(prices['package_avg']),
        step=1000000,
        format="Rp %d"
    )
    
    hotel_price = st.slider(
        "Harga Hotel/Malam (Makkah)",
        min_value=int(prices['hotel_makkah_min']),
        max_value=int(prices['hotel_makkah_max']),
        value=int(prices['hotel_makkah_avg']),
        step=100000,
        format="Rp %d"
    )
    
    # ... rest of simulator logic ...
```

### C. Di Sidebar (`app.py`)

```python
# Tambahkan import di app.py
from ui.components.price_widgets import render_price_sidebar_widget

def render_sidebar():
    with st.sidebar:
        # ... existing code ...
        
        # Tambahkan widget harga
        render_price_sidebar_widget()
        
        # ... rest of sidebar ...
```

### D. Standalone Price Page (Optional)

Buat file baru `ui/pages/prices.py`:

```python
import streamlit as st
from ui.components.price_widgets import (
    render_price_comparison_section,
    render_price_stats_widget
)

def render_prices_page():
    st.title("💰 Perbandingan Harga Umrah")
    st.caption("Data diupdate otomatis setiap 6 jam dari berbagai sumber")
    
    # Stats
    render_price_stats_widget()
    
    st.markdown("---")
    
    # Full comparison
    render_price_comparison_section()
```

Lalu tambahkan ke menu di `app.py`:

```python
menu_items = [
    # ... existing items ...
    ("💰", "Harga Live", "prices"),  # ← Tambahkan ini
]
```

---

## 📊 API Reference

### PriceRepository Methods

```python
from services.price import PriceRepository, get_price_repo

repo = get_price_repo()

# Packages
repo.get_all_packages(limit=50, min_price=20000000, max_price=50000000)
repo.get_cheapest_packages(limit=5)
repo.get_package_by_id(package_id)

# Hotels
repo.get_all_hotels(city='Makkah', min_stars=4, max_distance=500)
repo.get_hotels_near_haram(city='Makkah', max_distance=200)
repo.get_cheapest_hotels(city='Makkah', limit=5)

# Flights
repo.get_all_flights(origin='CGK', destination='JED', direct_only=True)
repo.get_direct_flights(origin='CGK', destination='JED')
repo.get_cheapest_flights(origin='CGK', destination='JED', limit=5)

# Statistics
repo.get_price_summary()
repo.get_price_ranges()  # For simulator defaults
repo.get_last_update()
```

### Cached Functions (Recommended)

```python
from services.price import (
    get_cached_packages,    # Cache 5 menit
    get_cached_hotels,      
    get_cached_flights,     
    get_cached_price_summary,  # Cache 10 menit
    get_cached_price_ranges,
)

# Dengan filter
packages = get_cached_packages(limit=20, min_price=25000000)
hotels = get_cached_hotels(city='Makkah', min_stars=4)
flights = get_cached_flights(origin='CGK', direct_only=True)
```

### UI Components

```python
from ui.components.price_widgets import (
    render_package_card,
    render_hotel_card,
    render_flight_card,
    render_price_sidebar_widget,
    render_price_stats_widget,
    render_price_comparison_section,
    render_live_price_indicator,
    get_real_price_defaults,
)
```

---

## 🔄 Cara Kerja Auto-Update

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  n8n Workflow   │─────▶│  Neon PostgreSQL │─────▶│  Streamlit App  │
│  (setiap 6 jam) │      │    (Database)    │      │   (baca data)   │
└─────────────────┘      └──────────────────┘      └─────────────────┘
        │                        │                        │
   Generate &               Store Data              Cache 5 min
   Insert Data              - packages              Query DB
   - 8 packages             - hotels                Display UI
   - 20 hotels              - flights
   - 36 flights
```

1. **n8n Workflow** berjalan otomatis setiap 6 jam
2. Data disimpan ke **Neon PostgreSQL** (database yang sama)
3. **Streamlit App** membaca data dengan cache 5 menit
4. User selalu melihat **data terbaru**

---

## ✅ Testing

Setelah integrasi, test dengan:

1. Buka app di browser
2. Cek sidebar ada widget harga
3. Cek halaman simulator pakai harga real
4. Cek halaman prices (jika dibuat)

---

## 🛠️ Troubleshooting

### Data tidak muncul
- Cek n8n workflow sudah active
- Cek database ada datanya:
  ```sql
  SELECT COUNT(*) FROM prices_packages;
  SELECT COUNT(*) FROM prices_hotels;
  SELECT COUNT(*) FROM prices_flights;
  ```

### Error "Database pool not initialized"
- Cek `DATABASE_URL` di secrets
- Pastikan format URL benar

### Cache tidak update
```python
# Clear cache manual
st.cache_data.clear()
```

---

*Made for LABBAIK.AI v6.0 - Platform AI Perencanaan Umrah #1 Indonesia* 🕌
