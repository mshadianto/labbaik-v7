"""
LABBAIK AI v6.0 - Partner Dashboard Page
========================================
Dashboard for travel agent and hotel partners.
"""

import streamlit as st
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import random


# =============================================================================
# SAMPLE DATA
# =============================================================================

def generate_sample_bookings() -> List[Dict]:
    """Generate sample bookings for demo."""
    statuses = ["pending", "confirmed", "completed", "cancelled"]
    cities = ["Jakarta", "Surabaya", "Bandung", "Medan"]
    packages = ["Backpacker", "Reguler", "Plus", "VIP"]
    
    bookings = []
    for i in range(15):
        dep_date = date.today() + timedelta(days=random.randint(10, 90))
        bookings.append({
            "id": f"LBK-{random.randint(100000, 999999)}",
            "customer_name": f"Customer {i+1}",
            "customer_phone": f"+628{random.randint(1000000000, 9999999999)}",
            "departure_city": random.choice(cities),
            "departure_date": dep_date.strftime("%d %b %Y"),
            "return_date": (dep_date + timedelta(days=random.randint(9, 15))).strftime("%d %b %Y"),
            "package_type": random.choice(packages),
            "travelers": random.randint(1, 5),
            "total_price": random.randint(25, 75) * 1_000_000,
            "commission": random.randint(25, 75) * 100_000,
            "status": random.choice(statuses),
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%d %b %Y"),
        })
    return bookings


def generate_sample_stats() -> Dict:
    """Generate sample statistics."""
    return {
        "total_bookings": 156,
        "confirmed_bookings": 98,
        "pending_bookings": 23,
        "total_revenue": 4_250_000_000,
        "total_commission": 425_000_000,
        "pending_commission": 45_000_000,
        "total_travelers": 412,
        "avg_booking_value": 27_250_000,
        "conversion_rate": 0.68,
        "monthly_growth": 0.12,
    }


def generate_monthly_data() -> List[Dict]:
    """Generate monthly performance data."""
    months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return [
        {"month": m, "bookings": random.randint(15, 35), "revenue": random.randint(400, 800) * 1_000_000}
        for m in months
    ]


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_metric_card(title: str, value: str, delta: str = None, delta_color: str = "normal"):
    """Render a metric card."""
    st.metric(label=title, value=value, delta=delta, delta_color=delta_color)


def render_booking_table(bookings: List[Dict], show_actions: bool = True):
    """Render bookings table."""
    status_badges = {
        "pending": "🟡",
        "confirmed": "🟢",
        "completed": "✅",
        "cancelled": "🔴",
    }
    
    for booking in bookings:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{booking['id']}**")
                st.caption(f"{booking['customer_name']}")
            
            with col2:
                st.markdown(f"📍 {booking['departure_city']}")
                st.caption(f"{booking['departure_date']} - {booking['return_date']}")
            
            with col3:
                st.markdown(f"👥 {booking['travelers']}")
                st.caption(booking['package_type'])
            
            with col4:
                st.markdown(f"Rp {booking['total_price']/1_000_000:.0f}jt")
                st.caption(f"Komisi: Rp {booking['commission']/1_000_000:.1f}jt")
            
            with col5:
                st.markdown(f"{status_badges.get(booking['status'], '⚪')} {booking['status'].title()}")
                if show_actions and booking['status'] == 'pending':
                    if st.button("✅", key=f"confirm_{booking['id']}", help="Konfirmasi"):
                        st.success(f"Booking {booking['id']} dikonfirmasi!")
            
            st.divider()


def render_commission_summary(stats: Dict):
    """Render commission summary."""
    st.markdown("### 💰 Ringkasan Komisi")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Komisi",
            f"Rp {stats['total_commission']/1_000_000:.0f}jt",
            f"+{stats['monthly_growth']*100:.0f}% bulan ini"
        )
    
    with col2:
        st.metric(
            "Komisi Pending",
            f"Rp {stats['pending_commission']/1_000_000:.0f}jt"
        )
    
    with col3:
        st.metric(
            "Rata-rata per Booking",
            f"Rp {stats['total_commission']/stats['total_bookings']/1_000:.0f}rb"
        )


def render_performance_chart(monthly_data: List[Dict]):
    """Render performance chart."""
    import pandas as pd
    
    df = pd.DataFrame(monthly_data)
    
    st.markdown("### 📊 Performa Bulanan")
    
    tab1, tab2 = st.tabs(["Bookings", "Revenue"])
    
    with tab1:
        st.bar_chart(df.set_index("month")["bookings"])
    
    with tab2:
        st.line_chart(df.set_index("month")["revenue"])


def render_quick_actions():
    """Render quick action buttons."""
    st.markdown("### ⚡ Aksi Cepat")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 Input Booking Baru", use_container_width=True):
            st.session_state.partner_action = "new_booking"
    
    with col2:
        if st.button("📤 Export Laporan", use_container_width=True):
            st.info("Generating report...")
    
    with col3:
        if st.button("💳 Tarik Komisi", use_container_width=True):
            st.session_state.partner_action = "withdraw"
    
    with col4:
        if st.button("📞 Hubungi Support", use_container_width=True):
            st.info("WhatsApp: +62 812 3456 7890")


def render_new_booking_form():
    """Render form for new booking input."""
    st.markdown("### 📝 Input Booking Baru")
    
    with st.form("new_booking_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Nama Customer *")
            customer_phone = st.text_input("No. WhatsApp *", placeholder="+628...")
            customer_email = st.text_input("Email")
            departure_city = st.selectbox(
                "Kota Keberangkatan",
                ["Jakarta", "Surabaya", "Bandung", "Medan", "Makassar"]
            )
        
        with col2:
            departure_date = st.date_input("Tanggal Berangkat", min_value=date.today())
            return_date = st.date_input("Tanggal Pulang", min_value=date.today())
            travelers = st.number_input("Jumlah Jamaah", min_value=1, max_value=50, value=1)
            package_type = st.selectbox("Tipe Paket", ["Backpacker", "Reguler", "Plus", "VIP"])
        
        total_price = st.number_input(
            "Total Harga (Rp)",
            min_value=15_000_000,
            max_value=500_000_000,
            value=30_000_000,
            step=1_000_000
        )
        
        notes = st.text_area("Catatan")
        
        submitted = st.form_submit_button("💾 Simpan Booking", type="primary", use_container_width=True)
        
        if submitted:
            if customer_name and customer_phone:
                st.success(f"✅ Booking berhasil disimpan!")
                st.session_state.partner_action = None
                st.rerun()
            else:
                st.error("Nama dan nomor WhatsApp wajib diisi!")
    
    if st.button("⬅️ Kembali"):
        st.session_state.partner_action = None
        st.rerun()


def render_withdraw_form(stats: Dict):
    """Render commission withdrawal form."""
    st.markdown("### 💳 Tarik Komisi")
    
    st.info(f"Saldo komisi tersedia: **Rp {stats['pending_commission']:,.0f}**")
    
    with st.form("withdraw_form"):
        amount = st.number_input(
            "Jumlah Penarikan (Rp)",
            min_value=100_000,
            max_value=stats['pending_commission'],
            value=stats['pending_commission'],
            step=100_000
        )
        
        bank = st.selectbox(
            "Bank Tujuan",
            ["BCA", "Mandiri", "BNI", "BRI", "BSI", "CIMB Niaga"]
        )
        
        account_number = st.text_input("Nomor Rekening")
        account_name = st.text_input("Nama Pemilik Rekening")
        
        submitted = st.form_submit_button("💸 Ajukan Penarikan", type="primary", use_container_width=True)
        
        if submitted:
            if account_number and account_name:
                st.success(f"""
                ✅ Permintaan penarikan berhasil diajukan!
                
                Jumlah: Rp {amount:,.0f}
                Bank: {bank}
                Rekening: {account_number}
                
                Dana akan ditransfer dalam 1-3 hari kerja.
                """)
            else:
                st.error("Lengkapi data rekening!")
    
    if st.button("⬅️ Kembali"):
        st.session_state.partner_action = None
        st.rerun()


def render_partner_profile():
    """Render partner profile section."""
    st.markdown("### 👤 Profil Partner")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### PT Travel Sejahtera")
        st.caption("Travel Agent Partner")
        st.markdown("⭐⭐⭐⭐⭐ (4.8)")
        st.markdown("📍 Jakarta Selatan")
    
    with col2:
        with st.expander("📋 Detail Partner"):
            st.markdown("""
            - **ID Partner:** PTR-001234
            - **Sejak:** 15 Januari 2024
            - **Lisensi:** PPIU/2024/001234
            - **Komisi Rate:** 10%
            - **Status:** ✅ Aktif
            """)
        
        with st.expander("📞 Kontak"):
            st.markdown("""
            - **Email:** partner@travel.com
            - **WhatsApp:** +62 812 3456 7890
            - **Alamat:** Jl. Sudirman No. 123
            """)


# =============================================================================
# MAIN PAGE
# =============================================================================

def render_partner_dashboard():
    """Render the main partner dashboard."""

    # Track page view
    try:
        from services.analytics import track_page
        track_page("partner_dashboard")
    except:
        pass
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1>🤝 Partner Dashboard</h1>
        <p style="color: #666;">Kelola booking dan pantau performa bisnis Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check authentication
    if not st.session_state.get("partner_authenticated", False):
        render_partner_login()
        return
    
    # Initialize
    if "partner_action" not in st.session_state:
        st.session_state.partner_action = None
    
    # Handle actions
    if st.session_state.partner_action == "new_booking":
        render_new_booking_form()
        return
    
    if st.session_state.partner_action == "withdraw":
        render_withdraw_form(generate_sample_stats())
        return
    
    # Generate data
    stats = generate_sample_stats()
    bookings = generate_sample_bookings()
    monthly_data = generate_monthly_data()
    
    # Sidebar profile
    with st.sidebar:
        render_partner_profile()
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.partner_authenticated = False
            st.rerun()
    
    # Quick Actions
    render_quick_actions()
    
    st.divider()
    
    # Overview Metrics
    st.markdown("### 📈 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Booking",
            stats['total_bookings'],
            f"+{int(stats['total_bookings'] * stats['monthly_growth'])} bulan ini"
        )
    
    with col2:
        st.metric(
            "Booking Confirmed",
            stats['confirmed_bookings'],
            f"{stats['confirmed_bookings']/stats['total_bookings']*100:.0f}%"
        )
    
    with col3:
        st.metric(
            "Total Revenue",
            f"Rp {stats['total_revenue']/1_000_000_000:.1f}M",
            f"+{stats['monthly_growth']*100:.0f}%"
        )
    
    with col4:
        st.metric(
            "Total Jamaah",
            stats['total_travelers'],
            f"avg {stats['total_travelers']/stats['total_bookings']:.1f}/booking"
        )
    
    st.divider()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Bookings",
        "💰 Komisi",
        "📊 Statistik",
        "⚙️ Pengaturan"
    ])
    
    with tab1:
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox(
                "Status",
                ["Semua", "Pending", "Confirmed", "Completed", "Cancelled"]
            )
        with col2:
            date_filter = st.date_input(
                "Periode",
                value=(date.today() - timedelta(days=30), date.today())
            )
        with col3:
            search = st.text_input("Cari", placeholder="ID atau nama...")
        
        # Filter bookings
        filtered_bookings = bookings
        if status_filter != "Semua":
            filtered_bookings = [b for b in bookings if b['status'] == status_filter.lower()]
        
        st.markdown(f"**{len(filtered_bookings)} bookings**")
        render_booking_table(filtered_bookings)
    
    with tab2:
        render_commission_summary(stats)
        
        st.divider()
        
        st.markdown("### 📜 Riwayat Penarikan")
        
        withdrawals = [
            {"date": "01 Dec 2024", "amount": 15_000_000, "status": "completed", "bank": "BCA"},
            {"date": "15 Nov 2024", "amount": 12_500_000, "status": "completed", "bank": "BCA"},
            {"date": "01 Nov 2024", "amount": 18_000_000, "status": "completed", "bank": "BCA"},
        ]
        
        for w in withdrawals:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{w['date']}**")
            with col2:
                st.markdown(f"Rp {w['amount']/1_000_000:.1f}jt")
            with col3:
                st.markdown(f"✅ {w['status'].title()}")
    
    with tab3:
        render_performance_chart(monthly_data)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏆 Top Packages")
            packages_data = {
                "Reguler": 45,
                "Plus": 32,
                "VIP": 18,
                "Backpacker": 5
            }
            for pkg, count in packages_data.items():
                st.progress(count/50, f"{pkg}: {count} bookings")
        
        with col2:
            st.markdown("### 🌍 Top Kota")
            cities_data = {
                "Jakarta": 52,
                "Surabaya": 35,
                "Bandung": 28,
                "Medan": 15,
                "Makassar": 12
            }
            for city, count in cities_data.items():
                st.progress(count/60, f"{city}: {count} bookings")
    
    with tab4:
        st.markdown("### ⚙️ Pengaturan")
        
        with st.expander("🔔 Notifikasi"):
            st.checkbox("Email untuk booking baru", value=True)
            st.checkbox("WhatsApp untuk booking baru", value=True)
            st.checkbox("Laporan mingguan", value=True)
            st.checkbox("Laporan bulanan", value=True)
        
        with st.expander("💳 Informasi Bank"):
            bank = st.selectbox("Bank", ["BCA", "Mandiri", "BNI", "BRI", "BSI"])
            account = st.text_input("Nomor Rekening", value="1234567890")
            name = st.text_input("Nama Rekening", value="PT Travel Sejahtera")
            if st.button("💾 Simpan"):
                st.success("Informasi bank berhasil disimpan!")
        
        with st.expander("🔒 Keamanan"):
            if st.button("🔑 Ganti Password"):
                st.info("Link reset password akan dikirim ke email Anda.")
            if st.button("📱 Setup 2FA"):
                st.info("Scan QR code dengan aplikasi authenticator.")


def render_partner_login():
    """Render partner login form."""
    st.markdown("### 🔐 Login Partner")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("partner_login"):
            email = st.text_input("Email Partner")
            password = st.text_input("Password", type="password")
            
            submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submitted:
                if email and password:
                    st.session_state.partner_authenticated = True
                    st.rerun()
                else:
                    st.error("Email dan password wajib diisi!")
        
        st.divider()
        st.markdown("Belum punya akun partner?")
        if st.button("📝 Daftar Sekarang", use_container_width=True):
            st.info("Hubungi tim LABBAIK AI untuk pendaftaran partner.")


# Run page
if __name__ == "__main__":
    render_partner_dashboard()
