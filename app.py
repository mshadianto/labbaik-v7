"""
LABBAIK AI - Platform Umrah Cerdas Indonesia
=============================================
By MS Hadianto

Main entry point - compatible with Streamlit Cloud deployment

Features:
- AI Chat Assistant for Umrah guidance
- Cost Simulator with Scenario Planning
- Live Package Price Updates
- WhatsApp Bot Integration
- Group Tracking & SOS Emergency
"""

import streamlit as st
import os
import sys
from datetime import datetime, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import version info
try:
    from core.version import get_display_version, APP_VERSION
except ImportError:
    def get_display_version():
        return "v7.1.0"
    APP_VERSION = "7.1.0"

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="LABBAIK AI - Platform Umrah Cerdas",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://labbaik.cloud/help',
        'Report a bug': 'https://labbaik.cloud/feedback',
        'About': 'LABBAIK AI - Platform Perencanaan Umrah AI #1 Indonesia'
    }
)

# =============================================================================
# LAZY IMPORTS & FEATURE FLAGS
# =============================================================================

# Core Pages Imports
try:
    from ui.pages.home import render_home_page
    from ui.pages.chat import render_chat_page
    from ui.pages.simulator import render_simulator_page
    from ui.pages.umrah_mandiri import render_umrah_mandiri_page
    from ui.pages.umrah_bareng import render_umrah_bareng_page
    from ui.pages.booking import render_booking_page
except ImportError:
    # Fallback for core pages if development environment is incomplete
    def render_home_page(): st.title("🏠 Beranda (Dev Mode)")
    def render_chat_page(): st.title("🤖 Chat (Dev Mode)")
    def render_simulator_page(): st.title("💰 Simulator (Dev Mode)")
    def render_umrah_mandiri_page(): st.title("🧭 Umrah Mandiri (Dev Mode)")
    def render_umrah_bareng_page(): st.title("👥 Umrah Bareng (Dev Mode)")
    def render_booking_page(): st.title("📦 Booking (Dev Mode)")

# =============================================================================
# 🆕 AI Itinerary Builder
# =============================================================================
try:
    from ui.pages.itinerary_builder import render_itinerary_builder_page
    HAS_ITINERARY = True
except ImportError:
    HAS_ITINERARY = False
    def render_itinerary_builder_page():
        st.markdown("# 🗓️ AI Itinerary Builder")
        st.warning("⚠️ Fitur AI Itinerary Builder belum tersedia")
        st.info("Segera hadir: Generate jadwal Umrah harian otomatis!")

# =============================================================================
# Smart Checklist
# =============================================================================
try:
    from ui.pages.smart_checklist import render_smart_checklist_page
    HAS_CHECKLIST = True
except ImportError:
    HAS_CHECKLIST = False
    def render_smart_checklist_page():
        st.markdown("# 📋 Smart Checklist")
        st.warning("⚠️ Fitur Smart Checklist belum tersedia")
        st.info("Segera hadir: Checklist packing Umrah yang dipersonalisasi!")

# Crowd Prediction
try:
    from features.crowd_prediction import (
        render_crowd_prediction_page,
        render_crowd_widget,
    )
    HAS_CROWD_PREDICTION = True
except ImportError:
    HAS_CROWD_PREDICTION = False
    def render_crowd_prediction_page(): st.warning("⚠️ Fitur Crowd Prediction belum tersedia")
    def render_crowd_widget(location="makkah", compact=True): pass

# SOS Emergency
try:
    from features.sos_emergency import (
        render_sos_page,
        render_sos_button,
    )
    HAS_SOS = True
except ImportError:
    HAS_SOS = False
    def render_sos_page(): st.warning("⚠️ Fitur SOS Emergency belum tersedia")
    def render_sos_button(size="small"): pass

# Group Tracking
try:
    from features.group_tracking import (
        render_group_tracking_page,
        render_tracking_mini_widget,
    )
    HAS_TRACKING = True
except ImportError:
    HAS_TRACKING = False
    def render_group_tracking_page(): st.warning("⚠️ Fitur Group Tracking belum tersedia")
    def render_tracking_mini_widget(): pass

# 3D Manasik
try:
    from features.manasik_3d import (
        render_manasik_page,
        render_manasik_mini_widget,
    )
    HAS_MANASIK = True
except ImportError:
    HAS_MANASIK = False
    def render_manasik_page(): st.warning("⚠️ Fitur 3D Manasik belum tersedia")
    def render_manasik_mini_widget(): pass

# Smart Comparison
try:
    from features.smart_comparison import render_smart_comparison_page
    HAS_COMPARISON = True
except ImportError:
    HAS_COMPARISON = False
    def render_smart_comparison_page(): st.warning("⚠️ Fitur Smart Comparison belum tersedia")

# Analytics Dashboard
try:
    from services.analytics.dashboard import render_analytics_dashboard
    HAS_ANALYTICS = True
except ImportError:
    HAS_ANALYTICS = False
    def render_analytics_dashboard(): st.warning("⚠️ Fitur Analytics Dashboard belum tersedia")

# User Auth & Management
try:
    from ui.pages.auth_page import (
        render_auth_page,
        render_login_widget,
        render_user_badge,
    )
    from ui.pages.user_analytics import render_user_analytics_page
    from services.user.user_service import get_current_user, is_logged_in
    from services.user.access_control import (
        check_page_access,
        render_access_denied,
        get_page_access_role,
    )
    HAS_USER_MANAGEMENT = True
except ImportError:
    HAS_USER_MANAGEMENT = False
    def render_auth_page(): st.warning("⚠️ Fitur User Management belum tersedia")
    def render_login_widget(): pass
    def render_user_badge(): pass
    def render_user_analytics_page(): st.warning("⚠️ Fitur User Analytics belum tersedia")
    def get_current_user(): return None
    def is_logged_in(): return False
    def check_page_access(page): return True, ""
    def render_access_denied(reason, name=""): st.error("Access denied")
    def get_page_access_role(page): return None

# Subscription & Referral
try:
    from ui.pages.subscription_page import render_subscription_page, render_subscription_widget
    from ui.pages.referral_page import render_referral_page, render_referral_widget
    HAS_SUBSCRIPTION = True
except ImportError:
    HAS_SUBSCRIPTION = False
    def render_subscription_page(): st.warning("⚠️ Fitur Subscription belum tersedia")
    def render_subscription_widget(): pass
    def render_referral_page(): st.warning("⚠️ Fitur Referral belum tersedia")
    def render_referral_widget(): pass

# Partner System
try:
    from ui.pages.partnership import render_partnership_page
    from ui.pages.partner_dashboard import render_partner_dashboard
    from ui.pages.package_builder import render_package_builder_page
    from ui.pages.api_docs import render_api_docs_page
    HAS_PARTNER_SYSTEM = True
except ImportError:
    HAS_PARTNER_SYSTEM = False
    def render_partnership_page(): st.warning("⚠️ Partnership Portal belum tersedia")
    def render_partner_dashboard(): st.warning("⚠️ Partner Dashboard belum tersedia")
    def render_package_builder_page(): st.warning("⚠️ Package Builder belum tersedia")
    def render_api_docs_page(): st.warning("⚠️ API Docs belum tersedia")

# =============================================================================
# CRM & Travel Operations System
# =============================================================================
try:
    from ui.pages.crm_leads import render_crm_leads_page
    from ui.pages.crm_bookings import render_crm_bookings_page
    from ui.pages.crm_jamaah import render_crm_jamaah_page
    from ui.pages.crm_quotes import render_crm_quotes_page
    from ui.pages.crm_analytics import render_crm_analytics_page
    from ui.pages.crm_broadcast import render_crm_broadcast_page
    from ui.pages.crm_competitors import render_crm_competitors_page
    HAS_CRM = True
except ImportError:
    HAS_CRM = False
    def render_crm_leads_page(): st.warning("⚠️ CRM Leads belum tersedia")
    def render_crm_bookings_page(): st.warning("⚠️ CRM Bookings belum tersedia")
    def render_crm_jamaah_page(): st.warning("⚠️ CRM Jamaah belum tersedia")
    def render_crm_quotes_page(): st.warning("⚠️ CRM Quotes belum tersedia")
    def render_crm_analytics_page(): st.warning("⚠️ CRM Analytics belum tersedia")
    def render_crm_broadcast_page(): st.warning("⚠️ CRM Broadcast belum tersedia")
    def render_crm_competitors_page(): st.warning("⚠️ CRM Competitors belum tersedia")

# =============================================================================
# v7.5 Price Aggregation System
# =============================================================================
try:
    from ui.pages.price_comparison import render_price_comparison_page, render_best_prices_widget
    HAS_PRICE_AGGREGATION = True
except ImportError:
    HAS_PRICE_AGGREGATION = False
    def render_price_comparison_page(): st.warning("⚠️ Price Comparison belum tersedia")
    def render_best_prices_widget(): pass

# WhatsApp Integration
try:
    from services.whatsapp import (
        render_whatsapp_settings,
        render_whatsapp_status,
        get_whatsapp_service,
    )
    HAS_WHATSAPP = True
except ImportError:
    HAS_WHATSAPP = False
    def render_whatsapp_settings(): st.warning("⚠️ WhatsApp Integration belum tersedia")
    def render_whatsapp_status(): pass
    def get_whatsapp_service(): return None

# Doa Player
try:
    from features.doa_player import (
        render_doa_player_page,
        render_doa_mini_widget,
    )
    HAS_DOA_PLAYER = True
except ImportError:
    HAS_DOA_PLAYER = False
    def render_doa_player_page():
        st.markdown("# 🤲 Doa & Dzikir")
        st.info("🚧 Fitur ini sedang dalam pengembangan...")
    def render_doa_mini_widget(): pass

# PWA Support
try:
    from features.pwa_support import (
        init_pwa,
        render_pwa_settings_page,
        render_install_button,
    )
    HAS_PWA = True
except ImportError:
    HAS_PWA = False
    def init_pwa(): pass
    def render_pwa_settings_page(): st.warning("⚠️ PWA Support belum tersedia")
    def render_install_button(): pass

# Page Tracking Service
try:
    from services.analytics import track_page
    HAS_TRACKING_SERVICE = True
except ImportError:
    HAS_TRACKING_SERVICE = False
    def track_page(page_name): pass


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        # Navigation
        "current_page": "home",
        
        # Authentication
        "user": None,
        "user_role": None,
        "is_authenticated": False,
        "auth_mode": "login",
        
        # Chat
        "chat_messages": [],
        
        # Visitor tracking
        "visitor_counted": False,
        
        # Gamification
        "xp": 0,
        "level": 1,
        "achievements": [],
        "daily_challenges_completed": [],
        
        # Theme
        "theme": "dark",
        
        # SOS Emergency
        "sos_contacts": [],
        "sos_user_info": {},
        "sos_triggered": False,
        
        # Group Tracking
        "tracking_groups": {},
        "current_group_id": None,
        "my_member_id": None,
        
        # Manasik Progress
        "manasik_progress": {},
        
        # Analytics
        "tracked_pages": set(),
        
        # Crowd Prediction
        "crowd_location": "makkah",
        
        # Itinerary Builder
        "itinerary_generated": False,
        "current_itinerary": None,
        
        # 🆕 Smart Checklist
        "checklist_items": {},
        "checklist_profile": {
            "gender": "male",
            "duration": 9,
            "season": "normal",
            "health_conditions": []
        },
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =============================================================================
# VISITOR TRACKING
# =============================================================================

def track_visitor():
    """Track unique visitors."""
    if not st.session_state.get("visitor_counted"):
        st.session_state.visitor_counted = True
        
        # Track with analytics service
        if HAS_TRACKING_SERVICE:
            try:
                track_page("home")
            except:
                pass


# =============================================================================
# GAMIFICATION SYSTEM
# =============================================================================

def get_level_title(level: int) -> str:
    """Get title based on level."""
    titles = {
        1: "Pemula", 2: "Pelajar", 3: "Praktisi", 4: "Ahli", 5: "Master",
        6: "Guru", 7: "Ulama", 8: "Syaikh", 9: "Mufti", 10: "Grand Master"
    }
    return titles.get(level, "Legend")


def add_xp(amount: int, reason: str = ""):
    """Add XP and check for level up."""
    st.session_state.xp = st.session_state.get("xp", 0) + amount
    
    # Check level up
    current_level = st.session_state.get("level", 1)
    xp_needed = current_level * 100
    
    if st.session_state.xp >= xp_needed and current_level < 10:
        st.session_state.level = current_level + 1
        st.session_state.xp = st.session_state.xp - xp_needed
        st.toast(f"🎉 Level Up! Sekarang Level {st.session_state.level}!", icon="⬆️")
    
    if reason:
        st.toast(f"🎯 +{amount} poin! {reason}", icon="✨")


# =============================================================================
# VISITOR ANALYTICS STATUS
# =============================================================================

def render_visitor_analytics_status():
    """Render live visitor analytics status."""
    try:
        # Try to get LIVE visitor stats from database
        from services.database.repository import get_db
        
        db = get_db()
        if db:
            try:
                # Get latest visitor data
                result = db.fetch_one("""
                    SELECT 
                        COALESCE(SUM(unique_visitors), 0) as visitors,
                        COALESCE(SUM(page_views), 0) as views,
                        MAX(updated_at) as last_update
                    FROM visitor_stats
                    WHERE date = CURRENT_DATE
                """)
                
                if result and result.get('last_update'):
                    # Format timestamp for WIB (UTC+7)
                    last_update = result.get('last_update')
                    if isinstance(last_update, datetime):
                        wib_time = last_update + timedelta(hours=7)
                        time_str = wib_time.strftime('%d %b %H:%M')
                        
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1a5f3c 0%, #2d8659 100%); 
                                    padding: 0.5rem; border-radius: 10px; text-align: center; 
                                    border: 1px solid #4ade80;">
                            <div style="color: #4ade80; font-weight: bold; font-size: 0.9rem;">
                                🟢 Live Data
                            </div>
                            <div style="color: #d4af37; font-size: 0.7rem; margin-top: 0.2rem;">
                                Update: {time_str} WIB
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        return
            except Exception as e:
                # Log but don't show error to user
                pass
        
        # Fallback: Show database status
        db_status = "🟢 Database Connected" if os.getenv("DATABASE_URL") else "🟡 Local Mode"
        st.caption(f"Status: {db_status}")
        
    except ImportError:
        # Module not available
        st.caption("Status: 🟡 Offline Mode")
    except Exception:
        # Any other error
        st.caption("📊 System Active")


# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================

def render_sidebar():
    """Render sidebar with navigation, widgets, and branding."""
    with st.sidebar:
        # Logo & Brand
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem;">🕋</div>
            <h2 style="color: #d4af37; margin: 0;">LABBAIK AI</h2>
            <p style="color: #888; font-size: 0.85rem;">Platform Umrah Cerdas</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")

        # User Login Widget
        if HAS_USER_MANAGEMENT:
            render_login_widget()
            st.markdown("")

        # SOS Emergency Button (Always Visible)
        if HAS_SOS:
            if st.button("🆘 DARURAT / SOS", key="sos_sidebar_main", use_container_width=True, type="primary"):
                st.session_state.current_page = "sos"
                st.rerun()
            st.markdown("")
        
        # Live Visitor Analytics Status
        render_visitor_analytics_status()
        
        st.markdown("---")
        
        # Main Navigation Menu
        st.markdown("### 🧭 Menu Utama")
        
        main_menu = [
            ("🏠", "Beranda", "home"),
            ("🤖", "AI Assistant", "chat"),
            ("💰", "Simulasi Biaya", "simulator"),
            ("👥", "Umrah Bareng", "umrah_bareng"),
            ("🧭", "Umrah Mandiri", "umrah_mandiri"),
            ("📦", "Booking", "booking"),
        ]
        
        for icon, label, page_key in main_menu:
            is_active = st.session_state.get("current_page") == page_key
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon} {label}", key=f"nav_{page_key}", use_container_width=True, type=btn_type):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        # ✨ New Features Menu
        st.markdown("### ✨ Fitur Baru")

        # Check user access for premium features
        user = get_current_user() if HAS_USER_MANAGEMENT else None
        user_role = user.role.value if user else "guest"

        # Feature list with premium indicator
        # Format: (icon, label, page_key, is_available, is_premium)
        new_features = [
            ("📊", "Prediksi Keramaian", "crowd", HAS_CROWD_PREDICTION, False),
            ("💰", "Perbandingan Harga", "price_comparison", HAS_PRICE_AGGREGATION, False),  # v7.5
            ("📍", "Group Tracking", "tracking", HAS_TRACKING, True),  # Premium
            ("🗓️", "AI Itinerary", "itinerary", HAS_ITINERARY, True),  # Premium
            ("📋", "Smart Checklist", "checklist", HAS_CHECKLIST, False),
            ("🕋", "Manasik 3D", "manasik", HAS_MANASIK, False),
            ("🤲", "Doa & Dzikir", "doa", HAS_DOA_PLAYER, False),
            ("🔍", "Bandingkan Paket", "compare", HAS_COMPARISON, False),
            ("👤", "Akun Saya", "auth", HAS_USER_MANAGEMENT, False),
            ("⭐", "Upgrade Premium", "subscription", HAS_SUBSCRIPTION, False),
            ("🎁", "Referral", "referral", HAS_SUBSCRIPTION, False),
            ("🤝", "Kemitraan", "partner", HAS_PARTNER_SYSTEM, False),
            ("📲", "Install App", "install", HAS_PWA, False),
        ]

        # Admin/Partner Features
        if HAS_USER_MANAGEMENT and is_logged_in():
            if user and user.role.value in ["admin", "partner"]:
                st.markdown("---")
                st.markdown("### 🔐 Admin/Mitra")

                if user.role.value in ["partner", "admin"]:
                    if st.button("📊 Partner Dashboard", key="nav_partner_dash", use_container_width=True):
                        st.session_state.current_page = "partner_dashboard"
                        st.rerun()
                    if st.button("📦 Package Builder", key="nav_package_builder", use_container_width=True):
                        st.session_state.current_page = "package_builder"
                        st.rerun()
                    if st.button("📖 API Docs", key="nav_api_docs", use_container_width=True):
                        st.session_state.current_page = "api_docs"
                        st.rerun()

                if user.role.value == "admin":
                    if st.button("👥 User Analytics", key="nav_user_analytics", use_container_width=True):
                        st.session_state.current_page = "user_analytics"
                        st.rerun()
                    if st.button("📈 Analytics", key="nav_analytics_admin", use_container_width=True):
                        st.session_state.current_page = "analytics"
                        st.rerun()

                if st.button("📱 WhatsApp", key="nav_whatsapp_admin", use_container_width=True):
                    st.session_state.current_page = "whatsapp"
                    st.rerun()

                # CRM Menu for Partners/Admins
                if HAS_CRM:
                    st.markdown("---")
                    st.markdown("### 💼 CRM Travel")

                    if st.button("📊 Dashboard CRM", key="nav_crm_analytics", use_container_width=True):
                        st.session_state.current_page = "crm_analytics"
                        st.rerun()
                    if st.button("👥 Manajemen Lead", key="nav_crm_leads", use_container_width=True):
                        st.session_state.current_page = "crm_leads"
                        st.rerun()
                    if st.button("📅 Booking & Bayar", key="nav_crm_bookings", use_container_width=True):
                        st.session_state.current_page = "crm_bookings"
                        st.rerun()
                    if st.button("👤 Database Jamaah", key="nav_crm_jamaah", use_container_width=True):
                        st.session_state.current_page = "crm_jamaah"
                        st.rerun()
                    if st.button("📋 Quote & Invoice", key="nav_crm_quotes", use_container_width=True):
                        st.session_state.current_page = "crm_quotes"
                        st.rerun()
                    if st.button("📢 WA Broadcast", key="nav_crm_broadcast", use_container_width=True):
                        st.session_state.current_page = "crm_broadcast"
                        st.rerun()
                    if st.button("📈 Monitor Kompetitor", key="nav_crm_competitors", use_container_width=True):
                        st.session_state.current_page = "crm_competitors"
                        st.rerun()

        # Partner CTA for non-partners
        if not user or (user and user.role.value not in ["partner", "admin"]):
            st.markdown("---")
            st.markdown("""
                <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                            padding: 0.75rem; border-radius: 12px; text-align: center;">
                    <div style="color: #000; font-weight: bold; font-size: 0.9rem;">Jadi Mitra Travel</div>
                    <div style="color: #333; font-size: 0.75rem;">Komisi hingga 15%</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Gabung Mitra", key="nav_partner_cta", use_container_width=True):
                st.session_state.current_page = "partner"
                st.rerun()

        for icon, label, page_key, is_available, is_premium in new_features:
            if is_available:
                is_active = st.session_state.get("current_page") == page_key

                # Add lock icon for premium features if user doesn't have access
                premium_locked = is_premium and user_role not in ["premium", "partner", "admin"]
                lock_icon = " 🔒" if premium_locked else ""

                label_display = f"**{label}**" if is_active else label
                if st.button(f"{icon} {label_display}{lock_icon}", key=f"nav_{page_key}", use_container_width=True):
                    st.session_state.current_page = page_key
                    st.rerun()
        
        st.markdown("---")
        
        # Quick Widgets
        st.markdown("### 📊 Quick Info")
        
        # Conditional rendering of mini widgets
        if HAS_WHATSAPP:
            try: render_whatsapp_status()
            except: pass
        
        if HAS_CROWD_PREDICTION:
            try: render_crowd_widget("makkah", compact=True)
            except: pass
            
        if HAS_TRACKING:
            try: render_tracking_mini_widget()
            except: pass
            
        if HAS_MANASIK:
            try: render_manasik_mini_widget()
            except: pass
            
        if HAS_DOA_PLAYER:
            try: render_doa_mini_widget()
            except: pass
        
        st.markdown("---")
        
        # Gamification Stats
        st.markdown("### 🏆 Progress Anda")
        
        level = st.session_state.get("level", 1)
        xp = st.session_state.get("xp", 0)
        xp_for_next = level * 100
        
        st.markdown(f"**Level {level}** - {get_level_title(level)}")
        st.progress(min(xp / xp_for_next, 1.0))
        st.caption(f"{xp}/{xp_for_next} XP")
        
        achievements = st.session_state.get("achievements", [])
        if achievements:
            badges = " ".join(achievements[:5])
            st.caption(f"🎖️ {badges}")
        
        st.markdown("---")
        
        # Footer
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0;">
            <p style="color: #666; font-size: 0.75rem;">
                {get_display_version()}<br>
                © 2025 MS Hadianto
            </p>
            <p style="color: #444; font-size: 0.65rem;">
                Platform Umrah Cerdas Indonesia<br>
                Powered by AI
            </p>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# PAGE ROUTER
# =============================================================================

def render_page():
    """Render the current page based on session state."""
    page = st.session_state.get("current_page", "home")
    
    # Track page view
    if HAS_TRACKING_SERVICE:
        try:
            track_page(page)
        except:
            pass
    
    # Page routing map
    page_map = {
        # Core pages
        "home": render_home_page,
        "chat": render_chat_page,
        "simulator": render_simulator_page,
        "umrah_mandiri": render_umrah_mandiri_page,
        "umrah_bareng": render_umrah_bareng_page,
        "booking": render_booking_page,

        # New feature pages
        "itinerary": render_itinerary_builder_page,
        "checklist": render_smart_checklist_page,
        "crowd": render_crowd_prediction_page,
        "sos": render_sos_page,
        "tracking": render_group_tracking_page,
        "manasik": render_manasik_page,
        "compare": render_smart_comparison_page,
        "analytics": render_analytics_dashboard,
        "whatsapp": render_whatsapp_settings,
        "doa": render_doa_player_page,
        "install": render_pwa_settings_page,

        # User management pages
        "auth": render_auth_page,
        "user_analytics": render_user_analytics_page,

        # Subscription & Growth
        "subscription": render_subscription_page,
        "referral": render_referral_page,

        # Partner System
        "partner": render_partnership_page,
        "partner_dashboard": render_partner_dashboard,
        "package_builder": render_package_builder_page,
        "api_docs": render_api_docs_page,

        # CRM System
        "crm_analytics": render_crm_analytics_page,
        "crm_leads": render_crm_leads_page,
        "crm_bookings": render_crm_bookings_page,
        "crm_jamaah": render_crm_jamaah_page,
        "crm_quotes": render_crm_quotes_page,
        "crm_broadcast": render_crm_broadcast_page,
        "crm_competitors": render_crm_competitors_page,

        # v7.5 Price Aggregation
        "price_comparison": render_price_comparison_page,
    }
    
    renderer = page_map.get(page, render_home_page)

    # Check page access control
    if HAS_USER_MANAGEMENT and page not in ["home", "auth"]:
        has_access, reason = check_page_access(page)
        if not has_access:
            page_names = {
                "chat": "AI Chat",
                "tracking": "Group Tracking",
                "itinerary": "AI Itinerary",
                "user_analytics": "User Analytics",
                "analytics": "Analytics Dashboard",
                "whatsapp": "WhatsApp Settings",
                "partner_dashboard": "Partner Dashboard",
            }
            render_access_denied(reason, page_names.get(page, page))
            return

    try:
        renderer()
    except Exception as e:
        # Improved Error Handling UI
        st.error(f"❌ Terjadi kesalahan saat memuat halaman: {str(e)}")
        st.info("Sistem telah mencatat error ini. Silakan kembali ke Beranda.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Kembali ke Beranda", key="err_home", use_container_width=True):
                st.session_state.current_page = "home"
                st.rerun()
        with col2:
            if st.button("🆘 Emergency", key="err_sos", type="primary", use_container_width=True):
                st.session_state.current_page = "sos"
                st.rerun()


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()
    
    # Initialize PWA support
    if HAS_PWA:
        init_pwa()
    
    # Track visitor
    track_visitor()
    
    # Award XP for visiting (once per session per page)
    page = st.session_state.get("current_page", "home")
    visit_key = f"visited_{page}"
    if not st.session_state.get(visit_key):
        st.session_state[visit_key] = True
        add_xp(5, f"Mengunjungi {page}")
    
    # Check for SOS trigger from any page
    if st.session_state.get("sos_triggered") and st.session_state.get("current_page") != "sos":
        st.session_state.current_page = "sos"
        st.rerun()
    
    # Render sidebar
    render_sidebar()
    
    # Render main content
    render_page()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
