"""
LABBAIK AI - Partner Landing Page
==================================
Landing page for travel agent partner recruitment.
"""

import streamlit as st
from datetime import datetime
from services.user import get_current_user, is_logged_in, UserRole


def render_partner_landing_page():
    """Main partner landing page"""

    # Hero Section
    render_hero_section()

    # Benefits
    render_benefits_section()

    # How it works
    render_how_it_works()

    # Commission structure
    render_commission_section()

    # Features for partners
    render_features_section()

    # Testimonials
    render_testimonials()

    # FAQ
    render_faq_section()

    # CTA & Registration
    render_registration_section()


def render_hero_section():
    """Hero banner"""
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1a5f3c 0%, #0d3320 100%);
                    padding: 3rem 2rem; border-radius: 20px; text-align: center;
                    margin-bottom: 2rem;">
            <div style="font-size: 1rem; color: #FFD700; margin-bottom: 0.5rem;">
                PROGRAM MITRA LABBAIK AI
            </div>
            <h1 style="font-size: 2.5rem; color: #fff; margin: 0;">
                Jadilah Mitra Travel Umrah #1 Indonesia
            </h1>
            <p style="font-size: 1.2rem; color: #ccc; margin: 1rem 0 2rem;">
                Tingkatkan penjualan paket Umrah Anda dengan teknologi AI.
                Komisi menarik untuk setiap booking!
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <div style="background: rgba(255,255,255,0.1); padding: 1rem 2rem; border-radius: 12px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #FFD700;">500+</div>
                    <div style="color: #aaa;">Mitra Aktif</div>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 1rem 2rem; border-radius: 12px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #FFD700;">10.000+</div>
                    <div style="color: #aaa;">Jamaah Terlayani</div>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 1rem 2rem; border-radius: 12px;">
                    <div style="font-size: 2rem; font-weight: bold; color: #FFD700;">15%</div>
                    <div style="color: #aaa;">Komisi per Booking</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_benefits_section():
    """Partner benefits"""
    st.markdown("## Keuntungan Menjadi Mitra")

    col1, col2, col3 = st.columns(3)

    benefits = [
        (col1, "💰", "Komisi Tinggi", "Dapatkan hingga 15% komisi untuk setiap booking yang berhasil melalui platform Anda."),
        (col2, "🤖", "AI Assistant", "Gunakan AI chatbot untuk menjawab pertanyaan calon jamaah 24/7 tanpa perlu staff tambahan."),
        (col3, "📊", "Dashboard Analytics", "Pantau performa penjualan, conversion rate, dan insight jamaah secara real-time."),
    ]

    for col, icon, title, desc in benefits:
        with col:
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 1.5rem;
                            border-radius: 16px; text-align: center; height: 200px;">
                    <div style="font-size: 3rem;">{icon}</div>
                    <h3 style="margin: 0.5rem 0;">{title}</h3>
                    <p style="color: #888; font-size: 0.9rem;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    col1, col2, col3 = st.columns(3)

    benefits2 = [
        (col1, "📱", "White-Label Solution", "Integrasikan LABBAIK AI ke website travel Anda dengan branding sendiri."),
        (col2, "🎓", "Training & Support", "Pelatihan penggunaan platform dan support prioritas dari tim kami."),
        (col3, "🔗", "API Integration", "Hubungkan sistem booking Anda langsung ke platform LABBAIK."),
    ]

    for col, icon, title, desc in benefits2:
        with col:
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 1.5rem;
                            border-radius: 16px; text-align: center; height: 200px;">
                    <div style="font-size: 3rem;">{icon}</div>
                    <h3 style="margin: 0.5rem 0;">{title}</h3>
                    <p style="color: #888; font-size: 0.9rem;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)


def render_how_it_works():
    """How partnership works"""
    st.markdown("---")
    st.markdown("## Cara Kerja")

    st.markdown("""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 2rem 0;">
            <div style="text-align: center;">
                <div style="background: #FFD700; color: #000; width: 50px; height: 50px;
                            border-radius: 50%; display: flex; align-items: center;
                            justify-content: center; margin: 0 auto 1rem; font-weight: bold; font-size: 1.5rem;">1</div>
                <h4>Daftar</h4>
                <p style="color: #888; font-size: 0.85rem;">Isi form pendaftaran mitra dan lengkapi dokumen</p>
            </div>
            <div style="text-align: center;">
                <div style="background: #FFD700; color: #000; width: 50px; height: 50px;
                            border-radius: 50%; display: flex; align-items: center;
                            justify-content: center; margin: 0 auto 1rem; font-weight: bold; font-size: 1.5rem;">2</div>
                <h4>Verifikasi</h4>
                <p style="color: #888; font-size: 0.85rem;">Tim kami verifikasi dalam 1-2 hari kerja</p>
            </div>
            <div style="text-align: center;">
                <div style="background: #FFD700; color: #000; width: 50px; height: 50px;
                            border-radius: 50%; display: flex; align-items: center;
                            justify-content: center; margin: 0 auto 1rem; font-weight: bold; font-size: 1.5rem;">3</div>
                <h4>Onboarding</h4>
                <p style="color: #888; font-size: 0.85rem;">Training dan setup akun partner</p>
            </div>
            <div style="text-align: center;">
                <div style="background: #FFD700; color: #000; width: 50px; height: 50px;
                            border-radius: 50%; display: flex; align-items: center;
                            justify-content: center; margin: 0 auto 1rem; font-weight: bold; font-size: 1.5rem;">4</div>
                <h4>Mulai Jualan</h4>
                <p style="color: #888; font-size: 0.85rem;">Upload paket dan mulai terima booking!</p>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_commission_section():
    """Commission structure"""
    st.markdown("---")
    st.markdown("## Struktur Komisi")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                        padding: 2rem; border-radius: 16px; color: #000;">
                <h3 style="margin: 0;">Mitra Silver</h3>
                <div style="font-size: 3rem; font-weight: bold; margin: 1rem 0;">10%</div>
                <div>Komisi per booking</div>
                <hr style="border-color: rgba(0,0,0,0.2);">
                <ul style="padding-left: 1.2rem; margin: 0;">
                    <li>0-10 booking/bulan</li>
                    <li>Dashboard basic</li>
                    <li>Email support</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
                        padding: 2rem; border-radius: 16px; color: #000;
                        border: 3px solid #FFD700;">
                <div style="background: #FFD700; color: #000; padding: 2px 8px;
                            border-radius: 4px; font-size: 0.7rem; display: inline-block;
                            margin-bottom: 0.5rem;">RECOMMENDED</div>
                <h3 style="margin: 0;">Mitra Gold</h3>
                <div style="font-size: 3rem; font-weight: bold; margin: 1rem 0;">15%</div>
                <div>Komisi per booking</div>
                <hr style="border-color: rgba(0,0,0,0.2);">
                <ul style="padding-left: 1.2rem; margin: 0;">
                    <li>10+ booking/bulan</li>
                    <li>Dashboard advanced + API</li>
                    <li>WhatsApp priority support</li>
                    <li>White-label branding</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem;
                    background: rgba(255,215,0,0.1); border-radius: 12px;">
            <strong>Bonus:</strong> Dapatkan bonus 5% tambahan untuk 3 bulan pertama!
        </div>
    """, unsafe_allow_html=True)


def render_features_section():
    """Features for partners"""
    st.markdown("---")
    st.markdown("## Fitur Untuk Mitra")

    features = [
        ("🎯", "Lead Management", "Terima dan kelola leads dari platform secara otomatis"),
        ("📦", "Package Management", "Upload dan kelola paket Umrah dengan mudah"),
        ("💳", "Payment Integration", "Terima pembayaran langsung ke rekening Anda"),
        ("📈", "Analytics Dashboard", "Pantau performa dan insight jamaah"),
        ("🔌", "API Access", "Integrasikan dengan sistem existing Anda"),
        ("📱", "Mobile App", "Kelola booking dari smartphone"),
        ("🎨", "White Label", "Custom branding untuk website Anda"),
        ("💬", "AI Chatbot", "Layani calon jamaah 24/7 dengan AI"),
    ]

    cols = st.columns(4)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 4]:
            st.markdown(f"""
                <div style="padding: 1rem; margin-bottom: 1rem;">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div style="font-weight: bold; margin: 0.5rem 0;">{title}</div>
                    <div style="font-size: 0.8rem; color: #888;">{desc}</div>
                </div>
            """, unsafe_allow_html=True)


def render_testimonials():
    """Partner testimonials"""
    st.markdown("---")
    st.markdown("## Testimoni Mitra")

    testimonials = [
        {
            "name": "H. Ahmad Fauzi",
            "company": "Al-Hidayah Tour",
            "location": "Jakarta",
            "text": "Sejak bergabung dengan LABBAIK, booking kami naik 40%. AI chatbot sangat membantu menjawab pertanyaan calon jamaah.",
            "image": "👤"
        },
        {
            "name": "Ustadzah Fatimah",
            "company": "Barokah Travel",
            "location": "Surabaya",
            "text": "Platform yang sangat user-friendly. Tim support responsif dan komisi tepat waktu setiap bulan.",
            "image": "👤"
        },
        {
            "name": "Bp. Ridwan",
            "company": "Mabrur Tour",
            "location": "Bandung",
            "text": "API integration memudahkan kami connect dengan sistem booking yang sudah ada. Sangat profesional!",
            "image": "👤"
        },
    ]

    cols = st.columns(3)
    for i, t in enumerate(testimonials):
        with cols[i]:
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 1.5rem;
                            border-radius: 16px; height: 280px;">
                    <div style="font-size: 3rem; text-align: center;">{t['image']}</div>
                    <p style="font-style: italic; color: #ccc; margin: 1rem 0;">"{t['text']}"</p>
                    <div style="margin-top: auto;">
                        <div style="font-weight: bold;">{t['name']}</div>
                        <div style="color: #FFD700; font-size: 0.85rem;">{t['company']}</div>
                        <div style="color: #888; font-size: 0.8rem;">{t['location']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)


def render_faq_section():
    """FAQ section"""
    st.markdown("---")
    st.markdown("## FAQ")

    faqs = [
        ("Apa syarat menjadi mitra?", "Travel agent harus memiliki izin PPIU atau bekerjasama dengan PPIU terdaftar. Lengkapi dokumen legalitas saat pendaftaran."),
        ("Berapa lama proses verifikasi?", "Proses verifikasi memakan waktu 1-2 hari kerja setelah dokumen lengkap diterima."),
        ("Kapan komisi dibayarkan?", "Komisi dibayarkan setiap tanggal 1 dan 15 untuk booking yang sudah selesai (jamaah berangkat)."),
        ("Apakah ada biaya pendaftaran?", "Tidak ada biaya pendaftaran. Anda hanya membayar fee per transaksi yang berhasil."),
        ("Bagaimana dengan refund?", "Kebijakan refund mengikuti terms paket masing-masing. Komisi akan disesuaikan jika ada refund."),
    ]

    for q, a in faqs:
        with st.expander(q):
            st.markdown(a)


def render_registration_section():
    """Registration CTA and form"""
    st.markdown("---")
    st.markdown("## Daftar Sekarang")

    user = get_current_user()

    # If already partner
    if user and user.role == UserRole.PARTNER:
        st.success("Anda sudah terdaftar sebagai Mitra LABBAIK!")
        if st.button("Buka Partner Dashboard", type="primary", use_container_width=True):
            st.session_state.current_page = "partner_dashboard"
            st.rerun()
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        with st.form("partner_registration"):
            st.markdown("### Form Pendaftaran Mitra")

            # Company info
            company_name = st.text_input("Nama Travel/Perusahaan *", placeholder="PT. Contoh Tour & Travel")
            col_a, col_b = st.columns(2)
            with col_a:
                ppiu_number = st.text_input("Nomor PPIU", placeholder="Jika memiliki")
            with col_b:
                established_year = st.number_input("Tahun Berdiri", min_value=1990, max_value=2025, value=2020)

            # Contact info
            st.markdown("#### Kontak")
            col_a, col_b = st.columns(2)
            with col_a:
                contact_name = st.text_input("Nama PIC *", placeholder="Nama lengkap")
                contact_email = st.text_input("Email *", placeholder="email@company.com")
            with col_b:
                contact_phone = st.text_input("WhatsApp *", placeholder="08123456789")
                contact_position = st.text_input("Jabatan", placeholder="Owner / Manager")

            # Address
            st.markdown("#### Alamat")
            address = st.text_area("Alamat Kantor *", placeholder="Alamat lengkap kantor")
            col_a, col_b = st.columns(2)
            with col_a:
                city = st.text_input("Kota *")
            with col_b:
                province = st.selectbox("Provinsi *", [
                    "", "DKI Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur",
                    "Banten", "DI Yogyakarta", "Sumatera Utara", "Sumatera Barat",
                    "Sumatera Selatan", "Riau", "Lampung", "Sulawesi Selatan",
                    "Kalimantan Timur", "Bali", "Lainnya"
                ])

            # Business info
            st.markdown("#### Informasi Bisnis")
            col_a, col_b = st.columns(2)
            with col_a:
                monthly_pax = st.selectbox("Estimasi Jamaah/Bulan", [
                    "1-10 jamaah", "11-50 jamaah", "51-100 jamaah", "100+ jamaah"
                ])
            with col_b:
                has_website = st.selectbox("Sudah punya website?", ["Belum", "Ya"])

            website_url = ""
            if has_website == "Ya":
                website_url = st.text_input("URL Website", placeholder="https://")

            # Additional
            notes = st.text_area("Catatan Tambahan (opsional)", placeholder="Informasi tambahan...")

            # Agreement
            agree = st.checkbox("Saya setuju dengan Syarat & Ketentuan Program Mitra LABBAIK AI")

            submitted = st.form_submit_button("Daftar Sebagai Mitra", type="primary", use_container_width=True)

            if submitted:
                if not all([company_name, contact_name, contact_email, contact_phone, address, city, province]):
                    st.error("Mohon lengkapi semua field yang wajib (*)")
                elif not agree:
                    st.error("Anda harus menyetujui Syarat & Ketentuan")
                else:
                    # Save registration (in real app, save to database)
                    st.success("Pendaftaran berhasil dikirim! Tim kami akan menghubungi Anda dalam 1-2 hari kerja.")
                    st.balloons()

    with col2:
        st.markdown("""
            <div style="background: rgba(255,215,0,0.1); padding: 1.5rem;
                        border-radius: 16px; position: sticky; top: 1rem;">
                <h4 style="color: #FFD700;">Dokumen yang Diperlukan</h4>
                <ul style="padding-left: 1.2rem; color: #ccc;">
                    <li>KTP Pemilik/PIC</li>
                    <li>NPWP Perusahaan</li>
                    <li>Akta Pendirian</li>
                    <li>NIB/SIUP</li>
                    <li>Izin PPIU (jika ada)</li>
                </ul>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <h4 style="color: #FFD700;">Butuh Bantuan?</h4>
                <p style="color: #ccc; font-size: 0.9rem;">
                    Hubungi tim partnership kami:
                </p>
                <p style="color: #fff;">
                    📱 0812-xxxx-xxxx<br>
                    📧 partner@labbaik.cloud
                </p>
            </div>
        """, unsafe_allow_html=True)


def render_partner_landing_widget():
    """Mini CTA widget"""
    st.markdown("""
        <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                    padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="color: #000; font-weight: bold;">Jadi Mitra Travel</div>
            <div style="color: #333; font-size: 0.8rem;">Komisi hingga 15%</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Daftar Mitra", key="partner_cta_widget", use_container_width=True):
        st.session_state.current_page = "partner"
        st.rerun()
