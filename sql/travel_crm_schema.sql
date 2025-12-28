-- =============================================================================
-- LABBAIK AI - Travel CRM & Operations Schema
-- =============================================================================
-- Database schema for CRM, Booking, Payments, Jamaah, and Operations
-- =============================================================================

-- Enable UUID extension if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- 1. LEADS (CRM)
-- =============================================================================
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Contact Info
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    whatsapp VARCHAR(20),

    -- Lead Details
    source VARCHAR(50) DEFAULT 'direct', -- direct, referral, social, ads, website
    status VARCHAR(20) DEFAULT 'new', -- new, contacted, interested, negotiating, won, lost
    priority VARCHAR(10) DEFAULT 'medium', -- low, medium, high, urgent

    -- Interest
    interested_package VARCHAR(100),
    budget_min BIGINT,
    budget_max BIGINT,
    preferred_month VARCHAR(20),
    group_size INT DEFAULT 1,

    -- Notes
    notes TEXT,
    last_contact_date TIMESTAMP,
    next_followup_date TIMESTAMP,

    -- Assignment
    assigned_to UUID,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_source ON leads(source);
CREATE INDEX idx_leads_phone ON leads(phone);
CREATE INDEX idx_leads_next_followup ON leads(next_followup_date);

-- =============================================================================
-- 2. LEAD ACTIVITIES (Follow-up History)
-- =============================================================================
CREATE TABLE IF NOT EXISTS lead_activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,

    activity_type VARCHAR(50) NOT NULL, -- call, whatsapp, email, meeting, note
    description TEXT,
    outcome VARCHAR(50), -- answered, no_answer, callback, interested, not_interested

    created_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_lead_activities_lead ON lead_activities(lead_id);

-- =============================================================================
-- 3. JAMAAH (Customer Database)
-- =============================================================================
CREATE TABLE IF NOT EXISTS jamaah (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Personal Info
    full_name VARCHAR(255) NOT NULL,
    nik VARCHAR(20),
    passport_number VARCHAR(50),
    passport_expiry DATE,

    -- Contact
    phone VARCHAR(20) NOT NULL,
    whatsapp VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    city VARCHAR(100),
    province VARCHAR(100),

    -- Demographics
    birth_date DATE,
    birth_place VARCHAR(100),
    gender VARCHAR(10),
    blood_type VARCHAR(5),

    -- Emergency Contact
    emergency_name VARCHAR(255),
    emergency_phone VARCHAR(20),
    emergency_relation VARCHAR(50),

    -- Health
    health_notes TEXT,
    special_needs TEXT,

    -- Travel History
    umrah_count INT DEFAULT 0,
    last_umrah_date DATE,

    -- Referral
    referred_by UUID,

    -- Status
    is_active BOOLEAN DEFAULT true,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_jamaah_phone ON jamaah(phone);
CREATE INDEX idx_jamaah_passport ON jamaah(passport_number);
CREATE INDEX idx_jamaah_name ON jamaah(full_name);

-- =============================================================================
-- 4. BOOKINGS
-- =============================================================================
CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_code VARCHAR(20) UNIQUE NOT NULL,

    -- Lead/Jamaah Reference
    lead_id UUID REFERENCES leads(id),
    jamaah_id UUID REFERENCES jamaah(id),

    -- Package Details
    package_name VARCHAR(255) NOT NULL,
    package_type VARCHAR(50), -- regular, plus, vip
    departure_date DATE,
    return_date DATE,
    duration_days INT,

    -- Pricing
    package_price BIGINT NOT NULL,
    discount_amount BIGINT DEFAULT 0,
    discount_reason VARCHAR(255),
    total_price BIGINT NOT NULL,

    -- Payment Status
    payment_status VARCHAR(20) DEFAULT 'pending', -- pending, dp_paid, partial, paid, refunded
    amount_paid BIGINT DEFAULT 0,
    amount_remaining BIGINT,

    -- Booking Status
    status VARCHAR(20) DEFAULT 'draft', -- draft, confirmed, processing, completed, cancelled

    -- Group
    group_code VARCHAR(20),
    room_type VARCHAR(20),
    roommate_preference VARCHAR(255),

    -- Notes
    notes TEXT,
    internal_notes TEXT,

    -- Staff
    created_by UUID,
    confirmed_by UUID,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TIMESTAMP,
    cancelled_at TIMESTAMP
);

CREATE INDEX idx_bookings_code ON bookings(booking_code);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_payment ON bookings(payment_status);
CREATE INDEX idx_bookings_departure ON bookings(departure_date);
CREATE INDEX idx_bookings_jamaah ON bookings(jamaah_id);

-- =============================================================================
-- 5. PAYMENTS
-- =============================================================================
CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_id UUID REFERENCES bookings(id) ON DELETE CASCADE,

    -- Payment Details
    payment_type VARCHAR(20) NOT NULL, -- dp, installment, final, additional
    installment_number INT,

    amount BIGINT NOT NULL,
    payment_method VARCHAR(50), -- transfer, cash, card, qris
    bank_name VARCHAR(100),
    account_number VARCHAR(50),

    -- Status
    status VARCHAR(20) DEFAULT 'pending', -- pending, confirmed, failed, refunded

    -- Proof
    proof_url TEXT,

    -- Dates
    due_date DATE,
    paid_at TIMESTAMP,
    confirmed_at TIMESTAMP,
    confirmed_by UUID,

    -- Notes
    notes TEXT,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payments_booking ON payments(booking_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_due ON payments(due_date);

-- =============================================================================
-- 6. DOCUMENTS
-- =============================================================================
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    jamaah_id UUID REFERENCES jamaah(id) ON DELETE CASCADE,
    booking_id UUID REFERENCES bookings(id),

    -- Document Info
    doc_type VARCHAR(50) NOT NULL, -- passport, ktp, photo, kk, visa, ticket, voucher
    doc_name VARCHAR(255),
    file_url TEXT,

    -- Status
    status VARCHAR(20) DEFAULT 'pending', -- pending, uploaded, verified, rejected
    rejection_reason TEXT,

    -- Verification
    verified_by UUID,
    verified_at TIMESTAMP,

    -- Expiry (for passport, visa)
    expiry_date DATE,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_jamaah ON documents(jamaah_id);
CREATE INDEX idx_documents_booking ON documents(booking_id);
CREATE INDEX idx_documents_status ON documents(status);

-- =============================================================================
-- 7. QUOTES (Penawaran)
-- =============================================================================
CREATE TABLE IF NOT EXISTS quotes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    quote_number VARCHAR(20) UNIQUE NOT NULL,

    -- Lead Reference
    lead_id UUID REFERENCES leads(id),

    -- Package Details (JSON)
    package_config JSONB NOT NULL,

    -- Pricing
    base_price BIGINT,
    discount_amount BIGINT DEFAULT 0,
    final_price BIGINT,

    -- Validity
    valid_until DATE,

    -- Status
    status VARCHAR(20) DEFAULT 'draft', -- draft, sent, viewed, accepted, rejected, expired

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    viewed_at TIMESTAMP,
    responded_at TIMESTAMP
);

CREATE INDEX idx_quotes_lead ON quotes(lead_id);
CREATE INDEX idx_quotes_status ON quotes(status);

-- =============================================================================
-- 8. INVOICES
-- =============================================================================
CREATE TABLE IF NOT EXISTS invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_number VARCHAR(20) UNIQUE NOT NULL,

    -- References
    booking_id UUID REFERENCES bookings(id),
    jamaah_id UUID REFERENCES jamaah(id),

    -- Invoice Details
    invoice_type VARCHAR(20) NOT NULL, -- dp, installment, final, full

    -- Amounts
    subtotal BIGINT,
    discount BIGINT DEFAULT 0,
    tax BIGINT DEFAULT 0,
    total BIGINT NOT NULL,

    -- Status
    status VARCHAR(20) DEFAULT 'unpaid', -- unpaid, paid, cancelled

    -- Dates
    due_date DATE,
    paid_at TIMESTAMP,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_invoices_booking ON invoices(booking_id);
CREATE INDEX idx_invoices_status ON invoices(status);

-- =============================================================================
-- 9. BROADCASTS (WhatsApp)
-- =============================================================================
CREATE TABLE IF NOT EXISTS broadcasts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Campaign Info
    name VARCHAR(255) NOT NULL,
    message_template TEXT NOT NULL,

    -- Target
    target_type VARCHAR(20), -- all, leads, jamaah, segment
    target_filter JSONB, -- filter criteria

    -- Stats
    total_recipients INT DEFAULT 0,
    sent_count INT DEFAULT 0,
    delivered_count INT DEFAULT 0,
    read_count INT DEFAULT 0,
    failed_count INT DEFAULT 0,

    -- Status
    status VARCHAR(20) DEFAULT 'draft', -- draft, scheduled, sending, completed, failed

    -- Schedule
    scheduled_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    -- Created
    created_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_broadcasts_status ON broadcasts(status);

-- =============================================================================
-- 10. BROADCAST RECIPIENTS
-- =============================================================================
CREATE TABLE IF NOT EXISTS broadcast_recipients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    broadcast_id UUID REFERENCES broadcasts(id) ON DELETE CASCADE,

    phone VARCHAR(20) NOT NULL,
    name VARCHAR(255),

    -- Status
    status VARCHAR(20) DEFAULT 'pending', -- pending, sent, delivered, read, failed
    error_message TEXT,

    -- Timestamps
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    read_at TIMESTAMP
);

CREATE INDEX idx_broadcast_recipients_broadcast ON broadcast_recipients(broadcast_id);

-- =============================================================================
-- 11. COMPETITOR PRICES
-- =============================================================================
CREATE TABLE IF NOT EXISTS competitor_prices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Competitor Info
    competitor_name VARCHAR(255) NOT NULL,
    competitor_url TEXT,

    -- Package Info
    package_name VARCHAR(255),
    package_type VARCHAR(50),
    duration_days INT,
    hotel_makkah VARCHAR(255),
    hotel_madinah VARCHAR(255),
    airline VARCHAR(100),

    -- Pricing
    price BIGINT NOT NULL,
    currency VARCHAR(10) DEFAULT 'IDR',

    -- Source
    source VARCHAR(50), -- website, social, manual
    scraped_at TIMESTAMP,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_competitor_prices_name ON competitor_prices(competitor_name);
CREATE INDEX idx_competitor_prices_date ON competitor_prices(scraped_at);

-- =============================================================================
-- 12. ANALYTICS EVENTS
-- =============================================================================
CREATE TABLE IF NOT EXISTS crm_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    event_type VARCHAR(50) NOT NULL, -- lead_created, booking_created, payment_received, etc
    event_data JSONB,

    -- References
    lead_id UUID,
    booking_id UUID,
    jamaah_id UUID,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_crm_analytics_type ON crm_analytics(event_type);
CREATE INDEX idx_crm_analytics_date ON crm_analytics(created_at);

-- =============================================================================
-- HELPER FUNCTIONS
-- =============================================================================

-- Generate booking code
CREATE OR REPLACE FUNCTION generate_booking_code()
RETURNS VARCHAR(20) AS $$
BEGIN
    RETURN 'LBK' || TO_CHAR(NOW(), 'YYYYMMDD') || LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0');
END;
$$ LANGUAGE plpgsql;

-- Generate quote number
CREATE OR REPLACE FUNCTION generate_quote_number()
RETURNS VARCHAR(20) AS $$
BEGIN
    RETURN 'QT' || TO_CHAR(NOW(), 'YYYYMMDD') || LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0');
END;
$$ LANGUAGE plpgsql;

-- Generate invoice number
CREATE OR REPLACE FUNCTION generate_invoice_number()
RETURNS VARCHAR(20) AS $$
BEGIN
    RETURN 'INV' || TO_CHAR(NOW(), 'YYYYMMDD') || LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0');
END;
$$ LANGUAGE plpgsql;

-- Update timestamps trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update trigger to tables
CREATE TRIGGER update_leads_timestamp BEFORE UPDATE ON leads FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_jamaah_timestamp BEFORE UPDATE ON jamaah FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_bookings_timestamp BEFORE UPDATE ON bookings FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_documents_timestamp BEFORE UPDATE ON documents FOR EACH ROW EXECUTE FUNCTION update_updated_at();
