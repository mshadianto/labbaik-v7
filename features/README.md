# LABBAIK AI v6.0 - Enhanced Features Package

## 🎯 Inspired by PilgrimPal & Leading Hajj/Umrah Apps

Package ini berisi fitur-fitur baru yang terinspirasi dari PilgrimPal dan app-app terbaik untuk jamaah Hajj/Umrah, dioptimasi untuk Streamlit.

---

## 📦 Features Included

### 1. 📊 Crowd Prediction (`crowd_prediction.py`)
Prediksi keramaian Masjidil Haram & Masjid Nabawi.

**Features:**
- Real-time crowd level indicator
- 24-hour forecast chart
- Weekly heatmap
- Best times recommendation
- Prayer time correlation

**Usage:**
```python
from features.crowd_prediction import render_crowd_widget, render_crowd_prediction_page

# Mini widget for sidebar
render_crowd_widget("makkah", compact=True)

# Full page
render_crowd_prediction_page()
```

---

### 2. 🆘 SOS Emergency (`sos_emergency.py`)
One-tap emergency system dengan WhatsApp integration.

**Features:**
- Emergency type selection (Medical, Lost, Security)
- WhatsApp pre-filled message with location
- Personal emergency contacts
- Saudi emergency numbers (911, Embassy, Hospitals)
- Medical info storage (blood type, allergies)

**Usage:**
```python
from features.sos_emergency import render_sos_button, render_sos_page

# Sidebar button
render_sos_button("small")

# Full page
render_sos_page()
```

---

### 3. 📍 Group Tracking (`group_tracking.py`)
Real-time location sharing untuk rombongan umrah.

**Features:**
- Create/join group with code
- Member status dashboard (online/away/offline)
- Check-in at key locations
- Location map view
- SOS alert to group

**Usage:**
```python
from features.group_tracking import render_group_tracking_page, render_tracking_mini_widget

# Mini widget
render_tracking_mini_widget()

# Full page
render_group_tracking_page()
```

---

### 4. 🕋 3D Manasik (`manasik_3d.py`)
Interactive 3D Ka'bah simulation dengan panduan ritual.

**Features:**
- 3D Ka'bah viewer (Three.js)
- Step-by-step ritual guide
- Doa dengan translasi
- Tips & kesalahan umum
- Progress tracker

**Usage:**
```python
from features.manasik_3d import render_3d_kaaba, render_manasik_page

# 3D viewer only
render_3d_kaaba()

# Full page with guide
render_manasik_page()
```

---

### 5. 🔍 Smart Comparison (`smart_comparison.py`)
AI-powered package comparison.

**Features:**
- Multi-factor scoring algorithm
- Personalized recommendations
- Side-by-side comparison
- Value analysis
- Filter by preferences

**Usage:**
```python
from features.smart_comparison import render_smart_comparison_page

# Full comparison page
render_smart_comparison_page()
```

---

### 6. 📈 Analytics Dashboard (`analytics/dashboard.py`)
Enhanced visitor analytics.

**Features:**
- Daily/weekly trend charts
- Hourly distribution
- Geographic distribution
- Device stats
- User flow visualization

**Usage:**
```python
from services.analytics.dashboard import render_analytics_dashboard

render_analytics_dashboard()
```

---

## 🚀 Installation

### Step 1: Copy Files
```bash
# Copy features folder to project
cp -r features /path/to/labbaik-v6/

# Copy analytics dashboard
cp services/analytics/dashboard.py /path/to/labbaik-v6/services/analytics/
```

### Step 2: Update Navigation
Add new menu items to `app.py`:

```python
# In your navigation/menu
PAGES = {
    "home": ("🏠 Beranda", render_home_page),
    "chat": ("🤖 AI Chat", render_chat_page),
    "simulator": ("💰 Simulasi", render_simulator_page),
    "umrah_mandiri": ("🧭 Umrah Mandiri", render_umrah_mandiri_page),
    "umrah_bareng": ("👥 Umrah Bareng", render_umrah_bareng_page),
    "booking": ("📦 Booking", render_booking_page),
    # NEW FEATURES
    "crowd": ("📊 Keramaian", render_crowd_prediction_page),
    "sos": ("🆘 Darurat", render_sos_page),
    "tracking": ("📍 Tracking", render_group_tracking_page),
    "manasik": ("🕋 Manasik 3D", render_manasik_page),
    "compare": ("🔍 Bandingkan", render_smart_comparison_page),
}
```

### Step 3: Add Sidebar Widgets
```python
# In sidebar rendering
with st.sidebar:
    st.markdown("## Quick Access")
    
    # SOS Button
    render_sos_button("small")
    
    # Crowd Widget
    render_crowd_widget("makkah", compact=True)
    
    # Tracking Widget
    render_tracking_mini_widget()
    
    # Manasik Progress
    render_manasik_mini_widget()
```

---

## 📋 File Structure

```
features/
├── __init__.py              # Package exports
├── crowd_prediction.py      # Crowd prediction widget
├── sos_emergency.py         # Emergency SOS system
├── group_tracking.py        # Group tracking system
├── manasik_3d.py           # 3D Manasik simulator
├── smart_comparison.py      # Smart package comparison
└── README.md               # This file

services/analytics/
├── __init__.py
├── tracker.py              # Page view tracking
└── dashboard.py            # Analytics dashboard (NEW)
```

---

## 🔧 Dependencies

All features use standard Streamlit components. No additional packages required!

Optional for enhanced 3D:
- Three.js (loaded via CDN)

---

## 📝 Changelog

### v6.0.0 (Dec 2024)
- ✨ Added Crowd Prediction Widget
- ✨ Added SOS Emergency System
- ✨ Added Group Tracking
- ✨ Added 3D Manasik Simulator
- ✨ Added Smart Package Comparison
- ✨ Enhanced Analytics Dashboard

---

## 🤝 Credits

Features inspired by:
- PilgrimPal (pilgrimpal.net)
- Nusuk (nusuk.sa)
- PilgrimApp (pilgrimapp.com)
- HajjGuide.AI (hajjguide.ai)

Developed for LABBAIK AI by Claude (Anthropic).

---

## 📞 Support

Untuk pertanyaan atau bantuan:
- GitHub Issues
- WhatsApp: [KIM Consulting]
