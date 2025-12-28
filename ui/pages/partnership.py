"""
LABBAIK AI - Partnership Portal
================================
Halaman khusus untuk program kemitraan travel umrah.
Menampilkan tier pricing dari config/pricing.yaml.
"""

import streamlit as st
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# PRICING DATA LOADER
# =============================================================================

def load_pricing_data():
    """Load pricing data from config."""
    try:
        from utils.pricing_loader import (
            get_pioneer_config,
            get_all_batches,
            get_current_batch,
            get_faq,
            get_contact_info,
            get_current_day,
            get_batch_countdown,
            is_batch_available,
        )
        return {
            "config": get_pioneer_config(),
            "batches": get_all_batches(),
            "current_batch": get_current_batch(),
            "faq": get_faq(),
            "contact": get_contact_info(),
            "current_day": get_current_day(),
            "get_countdown": get_batch_countdown,
            "is_available": is_batch_available,
        }
    except Exception as e:
        logger.error(f"Failed to load pricing data: {e}")
        return None


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_hero_section(config: dict):
    """Render hero section with program info."""
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">
            {config.get('program_name', 'Labbaik Pioneer 2026')}
        </h1>
        <p style="font-size: 1.2rem; color: #666; max-width: 600px; margin: 0 auto;">
            {config.get('program_description', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_current_batch_banner(data: dict):
    """Render banner for current active batch."""
    current = data["current_batch"]
    if not current:
        return

    countdown = data["get_countdown"](current)

    if current.highlight:
        st.success(f"""
        **{current.name}** sedang berlangsung!
        {current.tagline}
        {"Tersisa " + str(countdown) + " hari lagi" if countdown else "Daftar sekarang!"}
        """, icon="🎉")
    else:
        st.info(f"""
        **{current.name}** - {current.tagline}
        {"Tersisa " + str(countdown) + " hari" if countdown else "Pendaftaran terbuka"}
        """)


def render_pricing_card(batch, is_current: bool, partner_count: int = 0):
    """Render a single pricing card."""

    # Card styling based on highlight
    if batch.highlight:
        border_color = batch.badge_color
        bg_color = "#FFF9E6"
        badge = "TERBATAS"
    elif is_current:
        border_color = "#4CAF50"
        bg_color = "#F0FFF0"
        badge = "AKTIF"
    else:
        border_color = "#E0E0E0"
        bg_color = "#FAFAFA"
        badge = None

    # Container
    with st.container():
        # Header with badge
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {batch.name}")
            st.caption(batch.tagline)
        with col2:
            if badge:
                if batch.highlight:
                    st.markdown(f"<span style='background: {batch.badge_color}; color: #000; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.8rem;'>{badge}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span style='background: #4CAF50; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;'>{badge}</span>", unsafe_allow_html=True)

        # Price
        if batch.is_free:
            st.markdown(f"<h2 style='color: #4CAF50; margin: 0.5rem 0;'>GRATIS</h2>", unsafe_allow_html=True)
            st.caption("Setup Fee")
        else:
            st.markdown(f"<h2 style='margin: 0.5rem 0;'>{batch.setup_fee_display}</h2>", unsafe_allow_html=True)
            st.caption("Setup Fee (sekali bayar)")

        st.divider()

        # Key Info
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Status", batch.status)
        with col2:
            commission_label = f"{batch.commission_display}"
            if batch.commission_locked:
                commission_label += " (Locked)"
            st.metric("Komisi", commission_label)

        # Setup Type
        st.markdown(f"**Setup:** {batch.setup_type_display}")

        # Benefits
        st.markdown("**Benefit:**")
        for benefit in batch.benefits:
            st.markdown(f"- {benefit}")

        # Slot info
        if batch.max_partners:
            remaining = batch.max_partners - partner_count
            if remaining > 0:
                st.warning(f"Sisa {remaining} slot dari {batch.max_partners}")
            else:
                st.error("Slot penuh!")

        # CTA Button
        if is_current and (batch.max_partners is None or partner_count < batch.max_partners):
            if st.button(f"Daftar {batch.name}", key=f"cta_{batch.id}", type="primary", use_container_width=True):
                st.session_state.selected_batch = batch.id
                st.session_state.show_registration = True
                st.rerun()


def render_pricing_cards(data: dict):
    """Render all pricing cards in columns."""
    batches = data["batches"]
    current = data["current_batch"]

    st.markdown("## Pilih Paket Kemitraan")
    st.markdown("---")

    # Get partner counts from database (placeholder for now)
    partner_counts = {}  # TODO: Load from database

    # Display in columns
    cols = st.columns(len(batches))

    for idx, batch in enumerate(batches):
        with cols[idx]:
            is_current = current and batch.id == current.id
            count = partner_counts.get(batch.id, 0)
            render_pricing_card(batch, is_current, count)


def render_comparison_table(data: dict):
    """Render enhanced feature comparison table."""
    batches = data["batches"]

    st.markdown("""
    <style>
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        font-size: 0.95rem;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .comparison-table th {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #d4af37;
        padding: 1rem;
        text-align: center;
        font-weight: 600;
        border: none;
    }
    .comparison-table th.highlight {
        background: linear-gradient(135deg, #d4af37 0%, #f4d03f 100%);
        color: #1a1a2e;
    }
    .comparison-table td {
        padding: 0.875rem 1rem;
        text-align: center;
        border-bottom: 1px solid #e0e0e0;
        background: #fff;
    }
    .comparison-table tr:nth-child(even) td {
        background: #f8f9fa;
    }
    .comparison-table tr:hover td {
        background: #fff3cd;
    }
    .comparison-table td:first-child {
        text-align: left;
        font-weight: 500;
        background: #f0f0f0 !important;
        color: #333;
    }
    .comparison-table .feature-icon {
        margin-right: 0.5rem;
    }
    .comparison-table .check {
        color: #28a745;
        font-weight: bold;
    }
    .comparison-table .cross {
        color: #dc3545;
    }
    .comparison-table .highlight-cell {
        background: #fff9e6 !important;
        font-weight: 600;
        color: #856404;
    }
    .comparison-table .gold-text {
        color: #d4af37;
        font-weight: 600;
    }
    .comparison-table .free-badge {
        background: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("### Perbandingan Lengkap Antar Paket")

    # Build enhanced comparison data with icons
    features = [
        ("💰", "Setup Fee", [
            f"<span class='free-badge'>GRATIS</span>" if b.setup_fee == 0 else b.setup_fee_display
            for b in batches
        ]),
        ("⭐", "Status Member", [b.status for b in batches]),
        ("⏱️", "Durasi Status", [
            "<span class='gold-text'>Selamanya</span>" if not b.status_duration_months else f"{b.status_duration_months} bulan"
            for b in batches
        ]),
        ("📊", "Komisi Bagi Hasil", [
            f"<span class='gold-text'>{b.commission_display}</span>" if b.commission_locked else b.commission_display
            for b in batches
        ]),
        ("🔒", "Komisi Terlindungi", [
            "<span class='check'>✓ Locked Selamanya</span>" if b.commission_locked else "<span class='cross'>✗</span>"
            for b in batches
        ]),
        ("🛠️", "Tipe Onboarding", [b.setup_type_display for b in batches]),
        ("👥", "Kuota Partner", [
            f"<strong>{b.max_partners}</strong> partner" if b.max_partners else "Unlimited"
            for b in batches
        ]),
        ("📞", "Support Level", [
            "Priority 24/7" if b.setup_type == "white_glove" else "Jam Kerja" if idx < 2 else "Email"
            for idx, b in enumerate(batches)
        ]),
        ("🎓", "Training", [
            "1-on-1 Konsultasi" if b.setup_type == "white_glove" else "2 Sesi Online" if idx == 1 else "Video Tutorial"
            for idx, b in enumerate(batches)
        ]),
        ("🚀", "Akses Fitur Beta", [
            "<span class='check'>✓</span>" if b.setup_type == "white_glove" else "<span class='cross'>✗</span>"
            for b in batches
        ]),
    ]

    # Build HTML table
    html = "<table class='comparison-table'>"

    # Header row
    html += "<tr><th>Fitur</th>"
    for idx, b in enumerate(batches):
        highlight = "highlight" if b.highlight else ""
        html += f"<th class='{highlight}'>{b.name}</th>"
    html += "</tr>"

    # Data rows
    for icon, feature_name, values in features:
        html += "<tr>"
        html += f"<td><span class='feature-icon'>{icon}</span>{feature_name}</td>"
        for idx, val in enumerate(values):
            cell_class = "highlight-cell" if batches[idx].highlight else ""
            html += f"<td class='{cell_class}'>{val}</td>"
        html += "</tr>"

    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)

    # Legend
    st.markdown("""
    <div style="margin-top: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 8px; font-size: 0.85rem;">
        <strong>Keterangan:</strong><br>
        <span style="color: #28a745;">✓</span> = Tersedia &nbsp;&nbsp;
        <span style="color: #dc3545;">✗</span> = Tidak Tersedia &nbsp;&nbsp;
        <span style="color: #d4af37;">●</span> = Keunggulan Batch 1
    </div>
    """, unsafe_allow_html=True)


def render_faq_section(faq_list: list):
    """Render FAQ accordion."""
    if not faq_list:
        return

    st.markdown("## Pertanyaan Umum")

    for idx, faq in enumerate(faq_list):
        with st.expander(faq.get("question", ""), expanded=False):
            st.markdown(faq.get("answer", ""))


def render_contact_section(contact: dict):
    """Render enhanced contact/CTA section."""

    st.markdown("""
    <style>
    .contact-section {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
    }
    .contact-title {
        color: #d4af37;
        font-size: 1.75rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .contact-subtitle {
        color: #aaa;
        text-align: center;
        margin-bottom: 2rem;
    }
    .contact-cards {
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    .contact-card {
        flex: 1;
        min-width: 200px;
        max-width: 280px;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        text-decoration: none;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .contact-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .contact-card-wa {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
    }
    .contact-card-email {
        background: linear-gradient(135deg, #EA4335 0%, #C5221F 100%);
    }
    .contact-card-calendly {
        background: linear-gradient(135deg, #006BFF 0%, #0052CC 100%);
    }
    .contact-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }
    .contact-label {
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.25rem;
    }
    .contact-value {
        color: rgba(255,255,255,0.9);
        font-size: 0.95rem;
    }
    .contact-cta {
        margin-top: 2rem;
        text-align: center;
    }
    .contact-cta-text {
        color: #888;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

    wa = contact.get("whatsapp", "")
    wa_display = contact.get("whatsapp_display", wa)
    email = contact.get("email", "")
    calendly = contact.get("calendly", "")

    wa_link = f"https://wa.me/{wa.replace('+', '').replace('-', '')}" if wa else "#"

    html = f"""
    <div class="contact-section">
        <div class="contact-title">Siap Bergabung?</div>
        <div class="contact-subtitle">Hubungi kami untuk konsultasi gratis dan mulai perjalanan digital Anda</div>

        <div class="contact-cards">
            <a href="{wa_link}" target="_blank" class="contact-card contact-card-wa">
                <div class="contact-icon">📱</div>
                <div class="contact-label">WhatsApp</div>
                <div class="contact-value">{wa_display}</div>
            </a>

            <a href="mailto:{email}" class="contact-card contact-card-email">
                <div class="contact-icon">📧</div>
                <div class="contact-label">Email</div>
                <div class="contact-value">{email}</div>
            </a>

            <a href="{calendly}" target="_blank" class="contact-card contact-card-calendly">
                <div class="contact-icon">📅</div>
                <div class="contact-label">Jadwalkan Meeting</div>
                <div class="contact-value">Pilih waktu yang cocok</div>
            </a>
        </div>

        <div class="contact-cta">
            <div class="contact-cta-text">
                Respon cepat dalam waktu 1x24 jam kerja
            </div>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def render_registration_form(data: dict):
    """Render partner registration form."""
    batch_id = st.session_state.get("selected_batch")
    batch = None

    for b in data["batches"]:
        if b.id == batch_id:
            batch = b
            break

    if not batch:
        st.error("Batch tidak ditemukan")
        return

    st.markdown(f"## Daftar: {batch.name}")
    st.info(f"Setup Fee: {batch.setup_fee_display} | Komisi: {batch.commission_display}")

    with st.form("registration_form"):
        st.markdown("### Data Travel")
        company_name = st.text_input("Nama Travel *", placeholder="PT. Travel Umrah Indonesia")
        company_email = st.text_input("Email Bisnis *", placeholder="info@travel.com")
        company_phone = st.text_input("Telepon *", placeholder="021-12345678")
        company_address = st.text_area("Alamat Kantor", placeholder="Jl. Contoh No. 123, Jakarta")

        st.markdown("### Data PIC")
        pic_name = st.text_input("Nama PIC *", placeholder="Ahmad Subari")
        pic_phone = st.text_input("WhatsApp PIC *", placeholder="08123456789")
        pic_position = st.text_input("Jabatan", placeholder="Direktur / Owner")

        st.markdown("### Informasi Tambahan")
        experience = st.selectbox("Pengalaman di Industri Umrah", [
            "< 1 tahun",
            "1-3 tahun",
            "3-5 tahun",
            "> 5 tahun"
        ])
        packages_per_year = st.number_input("Estimasi Paket Umrah per Tahun", min_value=1, value=10)
        motivation = st.text_area("Mengapa tertarik bergabung Labbaik?", placeholder="Ceritakan motivasi Anda...")

        agree_tos = st.checkbox("Saya setuju dengan Syarat & Ketentuan Kemitraan Labbaik")

        submitted = st.form_submit_button("Kirim Pendaftaran", type="primary", use_container_width=True)

        if submitted:
            if not all([company_name, company_email, company_phone, pic_name, pic_phone]):
                st.error("Mohon lengkapi semua field yang wajib (*)")
            elif not agree_tos:
                st.error("Anda harus menyetujui Syarat & Ketentuan")
            else:
                # TODO: Save to database
                registration_data = {
                    "batch_id": batch.id,
                    "batch_name": batch.name,
                    "commission_rate": batch.commission_rate,
                    "setup_fee": batch.setup_fee,
                    "status": batch.status,
                    "company_name": company_name,
                    "company_email": company_email,
                    "company_phone": company_phone,
                    "company_address": company_address,
                    "pic_name": pic_name,
                    "pic_phone": pic_phone,
                    "pic_position": pic_position,
                    "experience": experience,
                    "packages_per_year": packages_per_year,
                    "motivation": motivation,
                    "registered_at": datetime.now().isoformat(),
                }

                st.success("Pendaftaran berhasil dikirim! Tim kami akan menghubungi Anda dalam 1x24 jam.")
                st.json(registration_data)

                # Clear state
                st.session_state.show_registration = False
                st.session_state.selected_batch = None

    if st.button("Kembali ke Daftar Harga"):
        st.session_state.show_registration = False
        st.session_state.selected_batch = None
        st.rerun()


# =============================================================================
# MAIN PAGE RENDERER
# =============================================================================

def render_partnership_page():
    """Main partnership page renderer."""

    # Track page view
    try:
        from services.analytics import track_page
        track_page("partnership")
    except:
        pass

    # Load pricing data
    data = load_pricing_data()

    if not data:
        st.error("Gagal memuat data pricing. Silakan coba lagi.")
        return

    # Check if showing registration form
    if st.session_state.get("show_registration"):
        render_registration_form(data)
        return

    # Hero Section
    render_hero_section(data["config"])

    # Current Batch Banner
    render_current_batch_banner(data)

    st.divider()

    # Pricing Cards
    render_pricing_cards(data)

    st.divider()

    # Comparison Table
    with st.expander("Lihat Perbandingan Lengkap", expanded=False):
        render_comparison_table(data)

    st.divider()

    # FAQ
    render_faq_section(data["faq"])

    st.divider()

    # Contact
    render_contact_section(data["contact"])

    # Footer
    st.divider()
    st.caption("Labbaik Pioneer 2026 - Program kemitraan terbatas untuk travel umrah terpilih.")


# Export
__all__ = ["render_partnership_page"]
