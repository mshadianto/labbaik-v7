"""
LABBAIK AI - Quote & Invoice Generator
========================================
Generate professional quotes and invoices.
"""

import streamlit as st
from datetime import datetime, date, timedelta
import logging

logger = logging.getLogger(__name__)


def format_rupiah(amount: int) -> str:
    """Format as Rupiah."""
    if amount is None:
        return "-"
    return f"Rp {amount:,.0f}".replace(",", ".")


def format_date(dt) -> str:
    """Format date."""
    if dt is None:
        return "-"
    if isinstance(dt, str):
        return dt[:10]
    return dt.strftime("%d %b %Y")


def init_session_state():
    """Initialize session state."""
    if "quote_view" not in st.session_state:
        st.session_state.quote_view = "list"


def render_quote_generator():
    """Generate quote from package builder."""
    st.markdown("### Generate Quote Baru")

    # Load package config
    try:
        from utils.package_calculator import (
            get_config, get_hotels, get_airlines, get_origins,
            get_durations, get_room_types, get_meal_options,
            PackageScenario, calculate_package, format_currency
        )

        config = get_config()
    except Exception as e:
        logger.error(f"Failed to load package config: {e}")
        st.error("Gagal memuat konfigurasi paket")
        return

    with st.form("quote_form"):
        st.markdown("**Informasi Penerima**")
        col1, col2 = st.columns(2)

        with col1:
            recipient_name = st.text_input("Nama Penerima *", placeholder="Nama calon jamaah")
            recipient_phone = st.text_input("No. Telepon *", placeholder="08xxxxxxxxxx")

        with col2:
            recipient_email = st.text_input("Email", placeholder="email@example.com")
            valid_days = st.number_input("Berlaku (hari)", min_value=1, max_value=30, value=7)

        st.markdown("---")
        st.markdown("**Konfigurasi Paket**")

        # Duration
        col1, col2, col3 = st.columns(3)

        with col1:
            durations = get_durations()
            duration_options = {d["label"]: d for d in durations}
            selected_duration = st.selectbox("Durasi", options=list(duration_options.keys()))
            duration_data = duration_options[selected_duration]

        with col2:
            nights_makkah = st.number_input("Malam Makkah", min_value=1, max_value=14, value=duration_data.get("nights_makkah", 4))

        with col3:
            nights_madinah = st.number_input("Malam Madinah", min_value=1, max_value=14, value=duration_data.get("nights_madinah", 4))

        # Hotels
        col1, col2 = st.columns(2)

        with col1:
            hotels_makkah = get_hotels("makkah")
            hotel_makkah_options = {h["label"]: h for h in hotels_makkah}
            selected_hotel_makkah = st.selectbox("Hotel Makkah", options=list(hotel_makkah_options.keys()))
            hotel_makkah = hotel_makkah_options[selected_hotel_makkah]
            makkah_price = st.number_input("Harga/Malam Makkah", value=hotel_makkah["default_price"], step=100000)

        with col2:
            hotels_madinah = get_hotels("madinah")
            hotel_madinah_options = {h["label"]: h for h in hotels_madinah}
            selected_hotel_madinah = st.selectbox("Hotel Madinah", options=list(hotel_madinah_options.keys()))
            hotel_madinah = hotel_madinah_options[selected_hotel_madinah]
            madinah_price = st.number_input("Harga/Malam Madinah", value=hotel_madinah["default_price"], step=100000)

        # Flight
        col1, col2 = st.columns(2)

        with col1:
            airlines = get_airlines()
            airline_options = {f"{a['name']} ({a['code']})": a for a in airlines}
            selected_airline = st.selectbox("Maskapai", options=list(airline_options.keys()))
            airline = airline_options[selected_airline]

        with col2:
            origins = get_origins()
            origin_options = {o["name"]: o for o in origins}
            selected_origin = st.selectbox("Kota Keberangkatan", options=list(origin_options.keys()))
            origin = origin_options[selected_origin]

        # Room & Meal
        col1, col2 = st.columns(2)

        with col1:
            room_types = get_room_types()
            room_options = {r["label"]: r for r in room_types}
            selected_room = st.selectbox("Tipe Kamar", options=list(room_options.keys()))
            room = room_options[selected_room]

        with col2:
            meals = get_meal_options()
            meal_options = {m["label"]: m for m in meals}
            selected_meal = st.selectbox("Paket Makan", options=list(meal_options.keys()))
            meal = meal_options[selected_meal]

        # Margin
        margin_percentage = st.slider("Margin (%)", min_value=5, max_value=30, value=15)

        # Discount
        st.markdown("---")
        st.markdown("**Diskon**")
        col1, col2 = st.columns(2)

        with col1:
            discount_type = st.selectbox("Tipe Diskon", options=["Tidak ada", "Nominal", "Persentase"])

        with col2:
            if discount_type == "Nominal":
                discount_value = st.number_input("Jumlah Diskon", min_value=0, value=0, step=100000)
            elif discount_type == "Persentase":
                discount_value = st.number_input("Persentase Diskon", min_value=0, max_value=50, value=0)
            else:
                discount_value = 0

        # Notes
        notes = st.text_area("Catatan untuk Quote", placeholder="Catatan tambahan...")

        submitted = st.form_submit_button("Generate Quote", type="primary", use_container_width=True)

        if submitted:
            if not recipient_name or not recipient_phone:
                st.error("Nama dan nomor telepon penerima wajib diisi!")
            else:
                # Calculate package
                scenario = PackageScenario(
                    name=f"Quote untuk {recipient_name}",
                    duration_days=duration_data.get("days", 9),
                    nights_makkah=nights_makkah,
                    nights_madinah=nights_madinah,
                    hotel_makkah_category=hotel_makkah["category"],
                    hotel_makkah_price=makkah_price,
                    hotel_madinah_category=hotel_madinah["category"],
                    hotel_madinah_price=madinah_price,
                    airline_code=airline["code"],
                    flight_price=airline["price_economy"],
                    origin_code=origin["code"],
                    origin_surcharge=origin["surcharge"],
                    room_type=room["type"],
                    room_occupancy=room["occupancy"],
                    room_multiplier=room["price_multiplier"],
                    meal_type=meal["type"],
                    meal_price_per_day=meal["price_per_day"],
                    margin_percentage=margin_percentage
                )

                breakdown = calculate_package(scenario)

                # Apply discount
                discount_amount = 0
                if discount_type == "Nominal":
                    discount_amount = discount_value
                elif discount_type == "Persentase":
                    discount_amount = int(breakdown.selling_price_per_person * discount_value / 100)

                final_price = breakdown.selling_price_per_person - discount_amount

                # Store in session for preview
                st.session_state.quote_preview = {
                    "recipient_name": recipient_name,
                    "recipient_phone": recipient_phone,
                    "recipient_email": recipient_email,
                    "package_name": f"Paket Umrah {duration_data['label']}",
                    "duration": duration_data['label'],
                    "hotel_makkah": selected_hotel_makkah,
                    "hotel_madinah": selected_hotel_madinah,
                    "airline": selected_airline,
                    "origin": selected_origin,
                    "room": selected_room,
                    "meal": selected_meal,
                    "base_price": breakdown.selling_price_per_person,
                    "discount": discount_amount,
                    "final_price": final_price,
                    "valid_until": (date.today() + timedelta(days=valid_days)).isoformat(),
                    "notes": notes,
                    "breakdown": breakdown
                }

                st.session_state.quote_view = "preview"
                st.rerun()


def render_quote_preview():
    """Render quote preview."""
    if "quote_preview" not in st.session_state:
        st.session_state.quote_view = "create"
        st.rerun()
        return

    quote = st.session_state.quote_preview

    st.markdown("### Preview Quote")

    # Quote card
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a5f2a 0%, #2d8a3e 100%); color: white; padding: 30px; border-radius: 15px; margin-bottom: 20px;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="margin: 0; color: white;">LABBAIK</h1>
            <p style="margin: 0; opacity: 0.9;">Penawaran Paket Umrah</p>
        </div>
        <hr style="border-color: rgba(255,255,255,0.3);">
        <p><strong>Kepada:</strong> {quote['recipient_name']}</p>
        <p><strong>Telepon:</strong> {quote['recipient_phone']}</p>
        <p><strong>Berlaku sampai:</strong> {quote['valid_until']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### {quote['package_name']}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Detail Paket:**")
        st.markdown(f"- Durasi: {quote['duration']}")
        st.markdown(f"- Hotel Makkah: {quote['hotel_makkah']}")
        st.markdown(f"- Hotel Madinah: {quote['hotel_madinah']}")
        st.markdown(f"- Maskapai: {quote['airline']}")

    with col2:
        st.markdown(f"- Keberangkatan: {quote['origin']}")
        st.markdown(f"- Tipe Kamar: {quote['room']}")
        st.markdown(f"- Makan: {quote['meal']}")

    st.markdown("---")
    st.markdown("### Harga")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Harga Normal", format_rupiah(quote['base_price']))

    with col2:
        if quote['discount'] > 0:
            st.metric("Diskon", f"-{format_rupiah(quote['discount'])}")
        else:
            st.metric("Diskon", "-")

    with col3:
        st.metric("Harga Final", format_rupiah(quote['final_price']))

    if quote.get('notes'):
        st.markdown("---")
        st.markdown("**Catatan:**")
        st.write(quote['notes'])

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✏️ Edit", use_container_width=True):
            st.session_state.quote_view = "create"
            st.rerun()

    with col2:
        if st.button("💾 Simpan", type="primary", use_container_width=True):
            # Save quote to database
            try:
                from services.crm import CRMRepository, Quote
                import json

                repo = CRMRepository()

                quote_obj = Quote(
                    package_config=quote,
                    base_price=quote['base_price'],
                    discount_amount=quote['discount'],
                    final_price=quote['final_price'],
                    valid_until=date.fromisoformat(quote['valid_until']),
                    status="draft"
                )

                quote_id = repo.create_quote(quote_obj)
                if quote_id:
                    st.success("Quote berhasil disimpan!")
                    st.session_state.quote_view = "list"
                    del st.session_state.quote_preview
                    st.rerun()
                else:
                    st.error("Gagal menyimpan quote")

            except Exception as e:
                logger.error(f"Failed to save quote: {e}")
                st.error(f"Gagal menyimpan: {str(e)}")

    with col3:
        wa_number = quote['recipient_phone'].replace("+", "").replace(" ", "")
        if wa_number.startswith("0"):
            wa_number = "62" + wa_number[1:]

        message = f"""Assalamualaikum {quote['recipient_name']},

Berikut penawaran paket umrah dari Labbaik:

*{quote['package_name']}*
- Hotel Makkah: {quote['hotel_makkah']}
- Hotel Madinah: {quote['hotel_madinah']}
- Maskapai: {quote['airline']}

*Harga: {format_rupiah(quote['final_price'])}*

Berlaku sampai: {quote['valid_until']}

Hubungi kami untuk informasi lebih lanjut!"""

        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        st.link_button("📱 Kirim WA", f"https://wa.me/{wa_number}?text={encoded_message}", use_container_width=True)


def render_quote_list():
    """Render saved quotes list."""
    st.markdown("### Daftar Quote")

    try:
        from services.crm import CRMRepository
        repo = CRMRepository()

        # For now, show placeholder
        st.info("Belum ada quote tersimpan. Buat quote baru untuk memulai.")

    except Exception as e:
        logger.error(f"Failed to load quotes: {e}")
        st.info("Tidak dapat memuat daftar quote")


def render_invoice_generator():
    """Generate invoice from booking."""
    st.markdown("### Generate Invoice")

    st.info("Pilih booking untuk generate invoice")

    try:
        from services.crm import CRMRepository
        repo = CRMRepository()

        bookings = repo.get_bookings(limit=20)

        if bookings:
            booking_options = {f"{b.booking_code} - {b.package_name}": b for b in bookings}
            selected = st.selectbox("Pilih Booking", options=list(booking_options.keys()))
            booking = booking_options[selected]

            st.markdown("---")
            st.markdown(f"### Invoice untuk {booking.booking_code}")

            col1, col2 = st.columns(2)

            with col1:
                invoice_type = st.selectbox(
                    "Tipe Invoice",
                    options=["dp", "installment", "final", "full"],
                    format_func=lambda x: {
                        "dp": "DP (Uang Muka)",
                        "installment": "Cicilan",
                        "final": "Pelunasan",
                        "full": "Full Payment"
                    }.get(x, x)
                )

            with col2:
                if invoice_type == "dp":
                    amount = int(booking.total_price * 0.3)
                elif invoice_type == "full":
                    amount = booking.total_price
                else:
                    amount = booking.amount_remaining or 0

                amount = st.number_input("Jumlah", value=amount, step=100000)

            due_date = st.date_input("Jatuh Tempo", value=date.today() + timedelta(days=7))

            if st.button("Generate Invoice", type="primary"):
                from services.crm import Invoice

                invoice = Invoice(
                    booking_id=booking.id,
                    invoice_type=invoice_type,
                    subtotal=amount,
                    total=amount,
                    due_date=due_date,
                    status="unpaid"
                )

                invoice_id = repo.create_invoice(invoice)
                if invoice_id:
                    st.success("Invoice berhasil dibuat!")

                    # Show invoice preview
                    st.markdown("---")
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;">
                        <div style="text-align: center; margin-bottom: 15px;">
                            <h2 style="margin: 0;">INVOICE</h2>
                            <p style="margin: 0; color: #666;">LABBAIK TRAVEL</p>
                        </div>
                        <hr>
                        <p><strong>No. Invoice:</strong> {repo.generate_invoice_number()}</p>
                        <p><strong>Booking:</strong> {booking.booking_code}</p>
                        <p><strong>Paket:</strong> {booking.package_name}</p>
                        <hr>
                        <p><strong>Total:</strong> {format_rupiah(amount)}</p>
                        <p><strong>Jatuh Tempo:</strong> {format_date(due_date)}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Gagal membuat invoice")
        else:
            st.info("Belum ada booking. Buat booking terlebih dahulu.")

    except Exception as e:
        logger.error(f"Failed to generate invoice: {e}")
        st.error("Gagal memuat data booking")


def render_crm_quotes_page():
    """Main quotes page."""
    try:
        from services.analytics import track_page
        track_page("crm_quotes")
    except:
        pass

    init_session_state()

    st.markdown("# 📋 Quote & Invoice")

    tab1, tab2, tab3 = st.tabs(["📝 Buat Quote", "📋 Daftar Quote", "🧾 Invoice"])

    with tab1:
        if st.session_state.quote_view == "preview":
            render_quote_preview()
        else:
            render_quote_generator()

    with tab2:
        render_quote_list()

    with tab3:
        render_invoice_generator()


__all__ = ["render_crm_quotes_page"]
