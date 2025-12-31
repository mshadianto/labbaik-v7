-- ============================================================================
-- LABBAIK AI - Supabase Migration Script
-- ============================================================================
-- Run this script in Supabase SQL Editor to initialize all tables
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- USERS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'free',
    status TEXT DEFAULT 'pending',

    -- Profile
    city TEXT,
    province TEXT,

    -- Umrah preferences
    preferred_departure_city TEXT,
    budget_range TEXT,
    travel_style TEXT,

    -- Tracking
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    last_login TIMESTAMPTZ,
    login_count INTEGER DEFAULT 0,

    -- Analytics/UTM
    source TEXT,
    referral_code TEXT,
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
CREATE INDEX IF NOT EXISTS idx_users_created ON users(created_at);

-- ============================================================================
-- USER ACTIVITIES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_activities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    activity_type TEXT NOT NULL,
    activity_data TEXT,
    page TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_activities_user ON user_activities(user_id);

-- ============================================================================
-- USER SESSIONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    session_token TEXT UNIQUE NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id);

-- ============================================================================
-- REFERRALS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS referrals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    referrer_id INTEGER NOT NULL REFERENCES users(id),
    referred_id INTEGER NOT NULL REFERENCES users(id),
    code TEXT NOT NULL,
    signup_rewarded BOOLEAN DEFAULT FALSE,
    premium_rewarded BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_id);
CREATE INDEX IF NOT EXISTS idx_referrals_code ON referrals(code);

-- ============================================================================
-- SUBSCRIPTIONS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INTEGER NOT NULL REFERENCES users(id),
    plan TEXT NOT NULL DEFAULT 'free',
    status TEXT NOT NULL DEFAULT 'active',
    starts_at TIMESTAMPTZ DEFAULT now(),
    ends_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_subscriptions_user ON subscriptions(user_id);

-- ============================================================================
-- TRANSPORT POIs (Stations/Terminals)
-- ============================================================================
CREATE TABLE IF NOT EXISTS transport_pois (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    name_ar TEXT,
    city TEXT NOT NULL CHECK (city IN ('MAKKAH', 'MADINAH')),
    type TEXT NOT NULL CHECK (type IN ('TRAIN_STATION', 'BUS_TERMINAL', 'AIRPORT')),
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    address TEXT,
    source TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_transport_pois_city_type ON transport_pois(city, type);

-- Seed POI Data
INSERT INTO transport_pois (name, name_ar, city, type, lat, lon, address, source)
VALUES
    ('Makkah Haramain Station', 'محطة مكة المكرمة', 'MAKKAH', 'TRAIN_STATION',
     21.4106, 39.8739, 'Al Rusayfah, Makkah', 'haramain'),
    ('SAPTCO Makkah Terminal', 'محطة سابتكو مكة', 'MAKKAH', 'BUS_TERMINAL',
     21.4225, 39.8262, 'Al Aziziyah, Makkah', 'saptco'),
    ('Madinah Haramain Station', 'محطة المدينة المنورة', 'MADINAH', 'TRAIN_STATION',
     24.5530, 39.7045, 'Knowledge Economic City, Madinah', 'haramain'),
    ('SAPTCO Madinah Terminal', 'محطة سابتكو المدينة', 'MADINAH', 'BUS_TERMINAL',
     24.4672, 39.6024, 'Central Area, Madinah', 'saptco')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- TRANSPORT SCHEDULE
-- ============================================================================
CREATE TABLE IF NOT EXISTS transport_schedule (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    operator TEXT NOT NULL,
    mode TEXT NOT NULL,
    route TEXT NOT NULL,
    depart_time_local TIMESTAMPTZ,
    arrive_time_local TIMESTAMPTZ,
    duration_min INTEGER,
    price_sar NUMERIC(10, 2),
    class TEXT,
    availability TEXT,
    source_url TEXT,
    source_method TEXT,
    payload JSONB,
    fetched_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_transport_schedule_route ON transport_schedule(operator, route, fetched_at DESC);
CREATE INDEX IF NOT EXISTS idx_transport_schedule_depart ON transport_schedule(depart_time_local);

-- ============================================================================
-- FX RATES
-- ============================================================================
CREATE TABLE IF NOT EXISTS fx_rates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    base TEXT NOT NULL,
    quote TEXT NOT NULL,
    rate NUMERIC(18, 8) NOT NULL,
    source TEXT DEFAULT 'ECB',
    asof_date DATE NOT NULL,
    fetched_at TIMESTAMPTZ DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_fx_rates_pair_date ON fx_rates(base, quote, asof_date);
CREATE INDEX IF NOT EXISTS idx_fx_rates_latest ON fx_rates(base, quote, asof_date DESC);

-- Default fallback rates
INSERT INTO fx_rates (base, quote, rate, source, asof_date)
VALUES
    ('EUR', 'SAR', 4.05, 'FALLBACK', CURRENT_DATE),
    ('EUR', 'USD', 1.08, 'FALLBACK', CURRENT_DATE),
    ('EUR', 'IDR', 17200, 'FALLBACK', CURRENT_DATE),
    ('EUR', 'MYR', 4.75, 'FALLBACK', CURRENT_DATE),
    ('USD', 'SAR', 3.75, 'FALLBACK', CURRENT_DATE),
    ('USD', 'IDR', 15900, 'FALLBACK', CURRENT_DATE),
    ('SAR', 'IDR', 4240, 'FALLBACK', CURRENT_DATE)
ON CONFLICT (base, quote, asof_date) DO UPDATE SET rate = EXCLUDED.rate;

-- ============================================================================
-- PROVIDER METRICS
-- ============================================================================
CREATE TABLE IF NOT EXISTS provider_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider TEXT NOT NULL,
    metric TEXT NOT NULL,
    value NUMERIC(18, 4) NOT NULL,
    metadata JSONB,
    ts TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_metrics_provider_ts ON provider_metrics(provider, ts DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_metric_ts ON provider_metrics(metric, ts DESC);

-- ============================================================================
-- PARTNER TIERS
-- ============================================================================
CREATE TABLE IF NOT EXISTS partner_tiers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    program TEXT NOT NULL DEFAULT 'pioneer_2026',
    setup_fee INTEGER NOT NULL DEFAULT 0,
    commission_rate DECIMAL(5,4) NOT NULL,
    commission_locked BOOLEAN DEFAULT FALSE,
    status TEXT NOT NULL,
    status_duration_months INTEGER,
    setup_type TEXT NOT NULL,
    max_partners INTEGER,
    day_start INTEGER NOT NULL DEFAULT 0,
    day_end INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Seed initial tiers
INSERT INTO partner_tiers (batch_id, name, setup_fee, commission_rate, commission_locked, status, status_duration_months, setup_type, max_partners, day_start, day_end)
VALUES
    ('batch_1', 'The Founding 10', 0, 0.15, TRUE, 'Lifetime Gold', NULL, 'white_glove', 10, 0, 30),
    ('batch_2', 'Early Adopters', 7500000, 0.15, FALSE, 'Gold', 12, 'self_service', 50, 31, 90),
    ('batch_3', 'Standard Partners', 15000000, 0.10, FALSE, 'Silver', 12, 'self_service', NULL, 91, NULL)
ON CONFLICT (batch_id) DO NOTHING;

-- ============================================================================
-- PARTNERS
-- ============================================================================
CREATE TABLE IF NOT EXISTS partners (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tier_id UUID REFERENCES partner_tiers(id),
    tier_batch_id TEXT NOT NULL,
    tier_name TEXT NOT NULL,
    commission_rate_locked DECIMAL(5,4) NOT NULL,
    setup_fee_paid INTEGER NOT NULL DEFAULT 0,
    status_granted TEXT NOT NULL,
    status_expires_at TIMESTAMPTZ,
    company_name TEXT NOT NULL,
    company_email TEXT NOT NULL,
    company_phone TEXT,
    company_address TEXT,
    company_logo_url TEXT,
    company_website TEXT,
    npwp TEXT,
    siup_number TEXT,
    akta_number TEXT,
    pic_name TEXT NOT NULL,
    pic_phone TEXT NOT NULL,
    pic_email TEXT,
    pic_position TEXT,
    experience_years TEXT,
    packages_per_year INTEGER,
    motivation TEXT,
    registration_status TEXT DEFAULT 'pending' CHECK (registration_status IN ('pending', 'approved', 'rejected', 'suspended')),
    approved_at TIMESTAMPTZ,
    approved_by UUID,
    rejection_reason TEXT,
    onboarding_completed BOOLEAN DEFAULT FALSE,
    onboarding_completed_at TIMESTAMPTZ,
    api_key_issued BOOLEAN DEFAULT FALSE,
    total_bookings INTEGER DEFAULT 0,
    total_revenue DECIMAL(15,2) DEFAULT 0,
    total_commission_earned DECIMAL(15,2) DEFAULT 0,
    last_booking_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_partners_tier ON partners(tier_id);
CREATE INDEX IF NOT EXISTS idx_partners_status ON partners(registration_status);
CREATE UNIQUE INDEX IF NOT EXISTS idx_partners_email ON partners(company_email);

-- ============================================================================
-- VISITOR ANALYTICS
-- ============================================================================
CREATE TABLE IF NOT EXISTS visitor_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id),
    ip_address TEXT,
    user_agent TEXT,
    referrer TEXT,
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT,
    device_type TEXT,
    browser TEXT,
    os TEXT,
    country TEXT,
    city TEXT,
    started_at TIMESTAMPTZ DEFAULT now(),
    ended_at TIMESTAMPTZ,
    page_views INTEGER DEFAULT 0,
    is_bounce BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_visitor_sessions_session ON visitor_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_visitor_sessions_started ON visitor_sessions(started_at);

CREATE TABLE IF NOT EXISTS page_views (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id),
    page_name TEXT NOT NULL,
    page_path TEXT,
    time_on_page INTEGER,
    scroll_depth INTEGER,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_page_views_session ON page_views(session_id);
CREATE INDEX IF NOT EXISTS idx_page_views_page ON page_views(page_name);
CREATE INDEX IF NOT EXISTS idx_page_views_created ON page_views(created_at);

-- ============================================================================
-- Done!
-- ============================================================================
