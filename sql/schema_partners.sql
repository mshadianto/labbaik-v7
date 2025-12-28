-- ============================================================================
-- LABBAIK AI - Partner Management Schema
-- Tables for partnership program (Pioneer 2026)
-- ============================================================================
-- AUDIT TRAIL: Komisi dan tier disimpan PERMANEN saat pendaftaran.
-- Jika struktur komisi berubah di masa depan, data mitra lama TETAP terlindungi.
-- ============================================================================

-- Enable UUID extension if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- Partner Tiers (Reference table - loaded from config)
-- ============================================================================
-- Ini adalah snapshot tier saat mitra mendaftar.
-- Walaupun config/pricing.yaml berubah, data di sini tidak berubah.
-- ============================================================================
CREATE TABLE IF NOT EXISTS partner_tiers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch_id TEXT NOT NULL UNIQUE,          -- 'batch_1', 'batch_2', etc.
    name TEXT NOT NULL,                     -- 'The Founding 10'
    program TEXT NOT NULL DEFAULT 'pioneer_2026',
    setup_fee INTEGER NOT NULL DEFAULT 0,
    commission_rate DECIMAL(5,4) NOT NULL,  -- 0.1500 = 15%
    commission_locked BOOLEAN DEFAULT FALSE,
    status TEXT NOT NULL,                   -- 'Lifetime Gold', 'Gold', 'Silver'
    status_duration_months INTEGER,         -- NULL = lifetime
    setup_type TEXT NOT NULL,               -- 'white_glove', 'self_service'
    max_partners INTEGER,                   -- NULL = unlimited
    day_start INTEGER NOT NULL DEFAULT 0,
    day_end INTEGER,                        -- NULL = ongoing
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Seed initial tiers from Pioneer 2026
INSERT INTO partner_tiers (batch_id, name, setup_fee, commission_rate, commission_locked, status, status_duration_months, setup_type, max_partners, day_start, day_end)
VALUES
    ('batch_1', 'The Founding 10', 0, 0.15, TRUE, 'Lifetime Gold', NULL, 'white_glove', 10, 0, 30),
    ('batch_2', 'Early Adopters', 7500000, 0.15, FALSE, 'Gold', 12, 'self_service', 50, 31, 90),
    ('batch_3', 'Standard Partners', 15000000, 0.10, FALSE, 'Silver', 12, 'self_service', NULL, 91, NULL)
ON CONFLICT (batch_id) DO NOTHING;

-- ============================================================================
-- Partners (Travel agencies registered in the program)
-- ============================================================================
-- CRITICAL: commission_rate_locked disimpan DI SINI, bukan di-lookup dari tier.
-- Ini menjamin mitra Batch 1 tetap dapat 15% meski tier Batch 3 jadi 10%.
-- ============================================================================
CREATE TABLE IF NOT EXISTS partners (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Tier Info (LOCKED at registration time)
    tier_id UUID REFERENCES partner_tiers(id),
    tier_batch_id TEXT NOT NULL,            -- Denormalized for quick lookup
    tier_name TEXT NOT NULL,                -- Denormalized: 'The Founding 10'
    commission_rate_locked DECIMAL(5,4) NOT NULL,  -- LOCKED commission rate
    setup_fee_paid INTEGER NOT NULL DEFAULT 0,
    status_granted TEXT NOT NULL,           -- 'Lifetime Gold', etc.
    status_expires_at TIMESTAMPTZ,          -- NULL = lifetime

    -- Company Info
    company_name TEXT NOT NULL,
    company_email TEXT NOT NULL,
    company_phone TEXT,
    company_address TEXT,
    company_logo_url TEXT,
    company_website TEXT,

    -- Legal
    npwp TEXT,
    siup_number TEXT,
    akta_number TEXT,

    -- PIC (Person in Charge)
    pic_name TEXT NOT NULL,
    pic_phone TEXT NOT NULL,
    pic_email TEXT,
    pic_position TEXT,

    -- Business Info
    experience_years TEXT,
    packages_per_year INTEGER,
    motivation TEXT,

    -- Status
    registration_status TEXT DEFAULT 'pending' CHECK (registration_status IN ('pending', 'approved', 'rejected', 'suspended')),
    approved_at TIMESTAMPTZ,
    approved_by UUID,  -- admin user id
    rejection_reason TEXT,

    -- Onboarding
    onboarding_completed BOOLEAN DEFAULT FALSE,
    onboarding_completed_at TIMESTAMPTZ,
    api_key_issued BOOLEAN DEFAULT FALSE,

    -- Metrics (updated periodically)
    total_bookings INTEGER DEFAULT 0,
    total_revenue DECIMAL(15,2) DEFAULT 0,
    total_commission_earned DECIMAL(15,2) DEFAULT 0,
    last_booking_at TIMESTAMPTZ,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_partners_tier ON partners(tier_id);
CREATE INDEX IF NOT EXISTS idx_partners_status ON partners(registration_status);
CREATE INDEX IF NOT EXISTS idx_partners_company ON partners(company_name);
CREATE UNIQUE INDEX IF NOT EXISTS idx_partners_email ON partners(company_email);

-- ============================================================================
-- Partner Transactions (For commission calculation)
-- ============================================================================
CREATE TABLE IF NOT EXISTS partner_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    partner_id UUID NOT NULL REFERENCES partners(id),

    -- Transaction Info
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('booking', 'commission_payout', 'adjustment')),
    reference_id TEXT,                      -- Booking ID, Payout ID, etc.
    description TEXT,

    -- Amounts
    gross_amount DECIMAL(15,2),             -- Total booking value
    commission_rate DECIMAL(5,4),           -- Rate at time of transaction
    commission_amount DECIMAL(15,2),        -- Calculated commission
    currency TEXT DEFAULT 'IDR',

    -- Status
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'paid', 'cancelled')),
    confirmed_at TIMESTAMPTZ,
    paid_at TIMESTAMPTZ,

    -- Metadata
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_partner_tx_partner ON partner_transactions(partner_id);
CREATE INDEX IF NOT EXISTS idx_partner_tx_type ON partner_transactions(transaction_type);
CREATE INDEX IF NOT EXISTS idx_partner_tx_status ON partner_transactions(status);
CREATE INDEX IF NOT EXISTS idx_partner_tx_created ON partner_transactions(created_at);

-- ============================================================================
-- Partner Audit Log (For GRC compliance)
-- ============================================================================
CREATE TABLE IF NOT EXISTS partner_audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    partner_id UUID REFERENCES partners(id),
    action TEXT NOT NULL,                   -- 'registered', 'approved', 'commission_changed', etc.
    actor_id UUID,                          -- Who performed the action
    actor_type TEXT,                        -- 'system', 'admin', 'partner'
    old_value JSONB,
    new_value JSONB,
    ip_address TEXT,
    user_agent TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_partner_audit_partner ON partner_audit_log(partner_id);
CREATE INDEX IF NOT EXISTS idx_partner_audit_action ON partner_audit_log(action);
CREATE INDEX IF NOT EXISTS idx_partner_audit_created ON partner_audit_log(created_at);

-- ============================================================================
-- Views for reporting
-- ============================================================================

-- Partner Summary View
CREATE OR REPLACE VIEW v_partner_summary AS
SELECT
    p.id,
    p.company_name,
    p.tier_name,
    p.tier_batch_id,
    p.commission_rate_locked * 100 as commission_percent,
    p.status_granted,
    p.registration_status,
    p.total_bookings,
    p.total_revenue,
    p.total_commission_earned,
    p.created_at as registered_at,
    p.approved_at,
    CASE
        WHEN p.status_expires_at IS NULL THEN 'Lifetime'
        WHEN p.status_expires_at > now() THEN 'Active'
        ELSE 'Expired'
    END as status_validity
FROM partners p;

-- Tier Statistics View
CREATE OR REPLACE VIEW v_tier_stats AS
SELECT
    t.batch_id,
    t.name as tier_name,
    t.max_partners,
    COUNT(p.id) as current_partners,
    COALESCE(t.max_partners - COUNT(p.id), 999) as remaining_slots,
    SUM(p.total_bookings) as total_bookings,
    SUM(p.total_revenue) as total_revenue
FROM partner_tiers t
LEFT JOIN partners p ON p.tier_id = t.id AND p.registration_status = 'approved'
GROUP BY t.id, t.batch_id, t.name, t.max_partners;
