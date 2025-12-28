"""
LABBAIK AI - Booking & Payment Tracker
========================================
UI for managing bookings and payment tracking.
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
    """Format datetime."""
    if dt is None:
        return "-"
    if isinstance(dt, str):
        return dt[:10]
    return dt.strftime("%d %b %Y")


def get_status_color(status: str) -> str:
    """Get status badge color."""
    colors = {
        "draft": "gray",
        "confirmed": "blue",
        "processing": "orange",
        "completed": "green",
        "cancelled": "red",
    }
    return colors.get(status, "gray")


def get_payment_status_color(status: str) -> str:
    """Get payment status color."""
    colors = {
        "pending": "red",
        "dp_paid": "orange",
        "partial": "blue",
        "paid": "green",
        "refunded": "gray",
    }
    return colors.get(status, "gray")


def init_session_state():
    """Initialize session state."""
    if "booking_view" not in st.session_state:
        st.session_state.booking_view = "list"
    if "selected_booking" not in st.session_state:
        st.session_state.selected_booking = None


def render_booking_stats():
    """Render booking statistics."""
    try:
        from services.crm import CRMRepository
        repo = CRMRepository()
        stats = repo.get_crm_stats()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Booking", stats.total_bookings)
        with col2:
            st.metric("Total Revenue", format_rupiah(stats.total_revenue))
        with col3:
            st.metric("Sudah Dibayar", format_rupiah(stats.total_paid))
        with col4:
            st.metric("Belum Dibayar", format_rupiah(stats.total_pending))

    except Exception as e:
        logger.error(f"Failed to load stats: {e}")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Booking", 0)
        with col2:
            st.metric("Total Revenue", "Rp 0")
        with col3:
            st.metric("Sudah Dibayar", "Rp 0")
        with col4:
            st.metric("Belum Dibayar", "Rp 0")


def render_booking_list():
    """Render booking list."""
    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        status_filter = st.selectbox(
            "Status Booking",
            options=["Semua", "draft", "confirmed", "processing", "completed", "cancelled"],
            format_func=lambda x: {
                "Semua": "Semua",
                "draft": "Draft",
                "confirmed": "Dikonfirmasi",
                "processing": "Diproses",
                "completed": "Selesai",
                "cancelled": "Dibatalkan"
            }.get(x, x)
        )

    with col2:
        payment_filter = st.selectbox(
            "Status Pembayaran",
            options=["Semua", "pending", "dp_paid", "partial", "paid"],
            format_func=lambda x: {
                "Semua": "Semua",
                "pending": "Belum Bayar",
                "dp_paid": "DP Lunas",
                "partial": "Cicilan",
                "paid": "Lunas"
            }.get(x, x)
        )

    with col3:
        departure_month = st.date_input("Keberangkatan", value=None)

    try:
        from services.crm import CRMRepository
        repo = CRMRepository()

        bookings = repo.get_bookings(
            status=status_filter if status_filter != "Semua" else None,
            payment_status=payment_filter if payment_filter != "Semua" else None,
            limit=50
        )

        if bookings:
            for booking in bookings:
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])

                    with col1:
                        st.markdown(f"**{booking.booking_code}**")
                        st.caption(booking.package_name)

                    with col2:
                        st.markdown(f":{get_status_color(booking.status)}[{booking.status.upper()}]")
                        st.caption(f"Berangkat: {format_date(booking.departure_date)}")

                    with col3:
                        st.markdown(f":{get_payment_status_color(booking.payment_status)}[{booking.payment_status.upper()}]")
                        progress = (booking.amount_paid / booking.total_price * 100) if booking.total_price > 0 else 0
                        st.progress(progress / 100, text=f"{progress:.0f}%")

                    with col4:
                        st.caption("Dibayar:")
                        st.markdown(f"**{format_rupiah(booking.amount_paid)}** / {format_rupiah(booking.total_price)}")

                    with col5:
                        if st.button("📝", key=f"booking_{booking.id}", help="Detail"):
                            st.session_state.selected_booking = booking.id
                            st.session_state.booking_view = "detail"
                            st.rerun()

                    st.divider()
        else:
            st.info("Belum ada booking. Klik 'Tambah Booking' untuk membuat booking baru.")

    except Exception as e:
        logger.error(f"Failed to load bookings: {e}")
        st.info("Belum ada data booking atau database belum terhubung.")


def render_add_booking_form():
    """Render add booking form."""
    st.markdown("### Tambah Booking Baru")

    with st.form("add_booking_form"):
        # Package info
        st.markdown("**Informasi Paket**")
        col1, col2 = st.columns(2)

        with col1:
            package_name = st.text_input("Nama Paket *", placeholder="Contoh: Paket 9 Hari Bintang 4")
            package_type = st.selectbox(
                "Tipe Paket",
                options=["regular", "plus", "vip"],
                format_func=lambda x: {"regular": "Regular", "plus": "Plus", "vip": "VIP"}.get(x, x)
            )
            duration_days = st.number_input("Durasi (hari)", min_value=5, max_value=30, value=9)

        with col2:
            departure_date = st.date_input("Tanggal Berangkat", value=date.today() + timedelta(days=30))
            return_date = st.date_input("Tanggal Pulang", value=date.today() + timedelta(days=39))
            room_type = st.selectbox(
                "Tipe Kamar",
                options=["quad", "triple", "double", "single"],
                format_func=lambda x: {
                    "quad": "Quad (4 orang)",
                    "triple": "Triple (3 orang)",
                    "double": "Double (2 orang)",
                    "single": "Single"
                }.get(x, x)
            )

        st.markdown("---")
        st.markdown("**Jamaah**")
        col1, col2 = st.columns(2)

        with col1:
            jamaah_name = st.text_input("Nama Jamaah *", placeholder="Nama lengkap")
            jamaah_phone = st.text_input("No. Telepon *", placeholder="08xxxxxxxxxx")

        with col2:
            group_code = st.text_input("Kode Grup", placeholder="Opsional")
            roommate_preference = st.text_input("Preferensi Teman Sekamar", placeholder="Opsional")

        st.markdown("---")
        st.markdown("**Harga**")
        col1, col2, col3 = st.columns(3)

        with col1:
            package_price = st.number_input("Harga Paket", min_value=0, value=25000000, step=500000)

        with col2:
            discount_amount = st.number_input("Diskon", min_value=0, value=0, step=100000)

        with col3:
            total_price = package_price - discount_amount
            st.metric("Total Harga", format_rupiah(total_price))

        discount_reason = st.text_input("Alasan Diskon", placeholder="Opsional")

        st.markdown("---")
        st.markdown("**Catatan**")
        notes = st.text_area("Catatan", placeholder="Catatan untuk jamaah...")
        internal_notes = st.text_area("Catatan Internal", placeholder="Catatan internal (tidak terlihat jamaah)...")

        submitted = st.form_submit_button("Simpan Booking", type="primary", use_container_width=True)

        if submitted:
            if not package_name or not jamaah_name or not jamaah_phone:
                st.error("Nama paket, nama jamaah, dan nomor telepon wajib diisi!")
            else:
                try:
                    from services.crm import CRMRepository, Booking, Jamaah
                    repo = CRMRepository()

                    # Check or create jamaah
                    jamaah = repo.find_jamaah_by_phone(jamaah_phone)
                    if not jamaah:
                        jamaah = Jamaah(full_name=jamaah_name, phone=jamaah_phone)
                        jamaah_id = repo.create_jamaah(jamaah)
                    else:
                        jamaah_id = jamaah.id

                    # Create booking
                    booking = Booking(
                        jamaah_id=jamaah_id,
                        package_name=package_name,
                        package_type=package_type,
                        departure_date=departure_date,
                        return_date=return_date,
                        duration_days=duration_days,
                        package_price=package_price,
                        discount_amount=discount_amount,
                        discount_reason=discount_reason if discount_reason else None,
                        total_price=total_price,
                        room_type=room_type,
                        group_code=group_code if group_code else None,
                        roommate_preference=roommate_preference if roommate_preference else None,
                        notes=notes if notes else None,
                        internal_notes=internal_notes if internal_notes else None,
                        status="draft",
                        payment_status="pending"
                    )

                    booking_id = repo.create_booking(booking)
                    if booking_id:
                        st.success("Booking berhasil dibuat!")
                        st.session_state.booking_view = "list"
                        st.rerun()
                    else:
                        st.error("Gagal membuat booking. Silakan coba lagi.")

                except Exception as e:
                    logger.error(f"Failed to create booking: {e}")
                    st.error(f"Gagal membuat booking: {str(e)}")


def render_booking_detail(booking_id: str):
    """Render booking detail."""
    try:
        from services.crm import CRMRepository
        repo = CRMRepository()
        booking = repo.get_booking(booking_id)

        if not booking:
            st.error("Booking tidak ditemukan")
            return

        # Header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"## 📋 {booking.booking_code}")
            st.caption(f"{booking.package_name} | {booking.package_type.upper() if booking.package_type else 'REGULAR'}")

        with col2:
            if st.button("← Kembali"):
                st.session_state.booking_view = "list"
                st.session_state.selected_booking = None
                st.rerun()

        st.markdown("---")

        # Status cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"**Status:** :{get_status_color(booking.status)}[{booking.status.upper()}]")

        with col2:
            st.markdown(f"**Pembayaran:** :{get_payment_status_color(booking.payment_status)}[{booking.payment_status.upper()}]")

        with col3:
            progress = (booking.amount_paid / booking.total_price * 100) if booking.total_price > 0 else 0
            st.progress(progress / 100, text=f"Terbayar: {progress:.0f}%")

        # Details
        st.markdown("### Detail Booking")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Berangkat:** {format_date(booking.departure_date)}")
            st.markdown(f"**Pulang:** {format_date(booking.return_date)}")
            st.markdown(f"**Durasi:** {booking.duration_days} hari")
            st.markdown(f"**Tipe Kamar:** {booking.room_type}")

        with col2:
            st.markdown(f"**Harga Paket:** {format_rupiah(booking.package_price)}")
            st.markdown(f"**Diskon:** {format_rupiah(booking.discount_amount)}")
            st.markdown(f"**Total:** {format_rupiah(booking.total_price)}")
            st.markdown(f"**Sisa Bayar:** {format_rupiah(booking.amount_remaining or 0)}")

        # Update status
        st.markdown("---")
        st.markdown("### Update Status")
        col1, col2 = st.columns(2)

        with col1:
            new_status = st.selectbox(
                "Status Booking",
                options=["draft", "confirmed", "processing", "completed", "cancelled"],
                index=["draft", "confirmed", "processing", "completed", "cancelled"].index(booking.status),
                format_func=lambda x: {
                    "draft": "Draft",
                    "confirmed": "Dikonfirmasi",
                    "processing": "Diproses",
                    "completed": "Selesai",
                    "cancelled": "Dibatalkan"
                }.get(x, x)
            )
            if new_status != booking.status:
                if st.button("Update Status"):
                    repo.update_booking(booking_id, {"status": new_status})
                    st.success("Status diupdate!")
                    st.rerun()

        # Payments section
        st.markdown("---")
        st.markdown("### Riwayat Pembayaran")

        payments = repo.get_payments_for_booking(booking_id)

        if payments:
            for payment in payments:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

                    with col1:
                        type_label = {
                            "dp": "DP",
                            "installment": f"Cicilan #{payment.get('installment_number', '')}",
                            "final": "Pelunasan",
                            "additional": "Tambahan"
                        }.get(payment.get("payment_type", ""), payment.get("payment_type", ""))
                        st.markdown(f"**{type_label}**")
                        st.caption(format_date(payment.get("created_at")))

                    with col2:
                        st.markdown(f"**{format_rupiah(payment.get('amount', 0))}**")
                        st.caption(payment.get("payment_method", "-"))

                    with col3:
                        status = payment.get("status", "pending")
                        color = {"pending": "orange", "confirmed": "green", "failed": "red"}.get(status, "gray")
                        st.markdown(f":{color}[{status.upper()}]")
                        if payment.get("due_date"):
                            st.caption(f"Jatuh tempo: {format_date(payment.get('due_date'))}")

                    with col4:
                        if payment.get("status") == "pending":
                            if st.button("✓", key=f"confirm_{payment.get('id')}", help="Konfirmasi"):
                                repo.confirm_payment(payment.get("id"))
                                st.success("Pembayaran dikonfirmasi!")
                                st.rerun()

                    st.divider()
        else:
            st.info("Belum ada pembayaran")

        # Add payment form
        with st.expander("Tambah Pembayaran"):
            with st.form("add_payment"):
                col1, col2 = st.columns(2)

                with col1:
                    payment_type = st.selectbox(
                        "Tipe Pembayaran",
                        options=["dp", "installment", "final"],
                        format_func=lambda x: {"dp": "DP", "installment": "Cicilan", "final": "Pelunasan"}.get(x, x)
                    )
                    amount = st.number_input("Jumlah", min_value=0, value=int(booking.total_price * 0.3), step=100000)

                with col2:
                    payment_method = st.selectbox(
                        "Metode",
                        options=["transfer", "cash", "qris"],
                        format_func=lambda x: {"transfer": "Transfer Bank", "cash": "Tunai", "qris": "QRIS"}.get(x, x)
                    )
                    due_date = st.date_input("Jatuh Tempo", value=date.today() + timedelta(days=7))

                if st.form_submit_button("Tambah Pembayaran", type="primary"):
                    from services.crm import Payment
                    payment = Payment(
                        booking_id=booking_id,
                        payment_type=payment_type,
                        amount=amount,
                        payment_method=payment_method,
                        due_date=due_date,
                        status="pending"
                    )
                    repo.create_payment(payment)
                    st.success("Pembayaran ditambahkan!")
                    st.rerun()

        # Installment calculator
        st.markdown("---")
        st.markdown("### Kalkulator Cicilan")

        remaining = booking.amount_remaining or booking.total_price
        if remaining > 0:
            col1, col2 = st.columns(2)

            with col1:
                num_installments = st.selectbox("Jumlah Cicilan", options=[3, 6, 9, 12])

            with col2:
                installment_amount = remaining / num_installments
                st.metric("Cicilan per Bulan", format_rupiah(int(installment_amount)))

            # Show schedule
            st.markdown("**Jadwal Cicilan:**")
            schedule_data = []
            for i in range(num_installments):
                due = date.today() + timedelta(days=30 * (i + 1))
                schedule_data.append({
                    "Cicilan": f"#{i + 1}",
                    "Jumlah": format_rupiah(int(installment_amount)),
                    "Jatuh Tempo": format_date(due)
                })

            import pandas as pd
            st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)

        else:
            st.success("Pembayaran sudah lunas!")

        # Notes
        if booking.notes:
            st.markdown("---")
            st.markdown("### Catatan")
            st.write(booking.notes)

    except Exception as e:
        logger.error(f"Failed to load booking detail: {e}")
        st.error("Gagal memuat detail booking")


def render_payment_reminders():
    """Render payment reminders section."""
    st.markdown("### Pengingat Pembayaran")

    try:
        from services.crm import CRMRepository
        repo = CRMRepository()

        overdue = repo.get_overdue_payments()
        pending = repo.get_pending_payments()

        if overdue:
            st.error(f"**{len(overdue)} pembayaran sudah jatuh tempo!**")
            for p in overdue[:5]:
                st.markdown(f"- {p.get('booking_code')} - {p.get('jamaah_name', 'N/A')}: {format_rupiah(p.get('amount', 0))}")

        elif pending:
            st.warning(f"**{len(pending)} pembayaran menunggu konfirmasi**")

        else:
            st.success("Tidak ada pembayaran yang jatuh tempo")

    except Exception as e:
        logger.error(f"Failed to load reminders: {e}")


def render_crm_bookings_page():
    """Main bookings page."""
    try:
        from services.analytics import track_page
        track_page("crm_bookings")
    except:
        pass

    init_session_state()

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# 📅 Booking & Pembayaran")
    with col2:
        if st.button("➕ Tambah Booking", type="primary", use_container_width=True):
            st.session_state.booking_view = "add"
            st.rerun()

    st.markdown("---")

    # Stats
    render_booking_stats()

    st.markdown("---")

    # View
    if st.session_state.booking_view == "add":
        render_add_booking_form()
    elif st.session_state.booking_view == "detail" and st.session_state.selected_booking:
        render_booking_detail(st.session_state.selected_booking)
    else:
        tab1, tab2 = st.tabs(["📋 Daftar Booking", "⏰ Pengingat"])

        with tab1:
            render_booking_list()

        with tab2:
            render_payment_reminders()


__all__ = ["render_crm_bookings_page"]
