-- ============================================================================
-- LABBAIK AI - Schema V1.3
-- Transport POIs, Itinerary Legs, Provider Metrics, FX Rates
-- ============================================================================

-- Enable UUID extension if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- Transport POIs (Stations/Terminals)
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

-- Seed POI Data (Haramain Train Stations & SAPTCO Terminals)
INSERT INTO transport_pois (name, name_ar, city, type, lat, lon, address, source)
VALUES
    -- Makkah
    ('Makkah Haramain Station', 'محطة مكة المكرمة', 'MAKKAH', 'TRAIN_STATION',
     21.4106, 39.8739, 'Al Rusayfah, Makkah', 'haramain'),
    ('SAPTCO Makkah Terminal', 'محطة سابتكو مكة', 'MAKKAH', 'BUS_TERMINAL',
     21.4225, 39.8262, 'Al Aziziyah, Makkah', 'saptco'),

    -- Madinah
    ('Madinah Haramain Station', 'محطة المدينة المنورة', 'MADINAH', 'TRAIN_STATION',
     24.5530, 39.7045, 'Knowledge Economic City, Madinah', 'haramain'),
    ('SAPTCO Madinah Terminal', 'محطة سابتكو المدينة', 'MADINAH', 'BUS_TERMINAL',
     24.4672, 39.6024, 'Central Area, Madinah', 'saptco')
ON CONFLICT DO NOTHING;

-- ============================================================================
-- Transport Schedule (JSON-first scraped data)
-- ============================================================================
CREATE TABLE IF NOT EXISTS transport_schedule (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    operator TEXT NOT NULL,  -- 'HARAMAIN', 'SAPTCO'
    mode TEXT NOT NULL,      -- 'TRAIN', 'BUS'
    route TEXT NOT NULL,     -- 'MAKKAH_MADINAH', 'MADINAH_MAKKAH'
    depart_time_local TIMESTAMPTZ,
    arrive_time_local TIMESTAMPTZ,
    duration_min INTEGER,
    price_sar NUMERIC(10, 2),
    class TEXT,              -- 'ECONOMY', 'BUSINESS'
    availability TEXT,       -- 'AVAILABLE', 'LIMITED', 'SOLD_OUT'
    source_url TEXT,
    source_method TEXT,      -- 'JSON', 'HTML', 'SNAPSHOT'
    payload JSONB,
    fetched_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_transport_schedule_route ON transport_schedule(operator, route, fetched_at DESC);
CREATE INDEX IF NOT EXISTS idx_transport_schedule_depart ON transport_schedule(depart_time_local);

-- ============================================================================
-- Itinerary Legs (Hotel → Station/Terminal with real ETA)
-- ============================================================================
CREATE TABLE IF NOT EXISTS itinerary_legs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_hotel_id TEXT NOT NULL,
    from_poi_id UUID REFERENCES transport_pois(id),
    to_poi_id UUID REFERENCES transport_pois(id),
    mode TEXT NOT NULL,           -- 'TRAIN', 'BUS', 'WALK', 'TAXI'
    walk_distance_m INTEGER,
    walk_duration_min INTEGER,
    depart_time_local TIMESTAMPTZ,
    arrive_time_local TIMESTAMPTZ,
    duration_min INTEGER,
    confidence NUMERIC(4, 2) DEFAULT 0.8,
    payload JSONB,
    fetched_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_legs_hotel_mode ON itinerary_legs(from_hotel_id, mode, fetched_at DESC);

-- ============================================================================
-- FX Rates (ECB + manual fallback)
-- ============================================================================
CREATE TABLE IF NOT EXISTS fx_rates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    base TEXT NOT NULL,           -- 'EUR', 'USD', 'SAR'
    quote TEXT NOT NULL,          -- 'SAR', 'IDR', 'MYR'
    rate NUMERIC(18, 8) NOT NULL,
    source TEXT DEFAULT 'ECB',    -- 'ECB', 'MANUAL', 'FALLBACK'
    asof_date DATE NOT NULL,
    fetched_at TIMESTAMPTZ DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_fx_rates_pair_date ON fx_rates(base, quote, asof_date);
CREATE INDEX IF NOT EXISTS idx_fx_rates_latest ON fx_rates(base, quote, asof_date DESC);

-- Default fallback rates (approximate, update regularly)
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
-- Provider Metrics (Observability)
-- ============================================================================
CREATE TABLE IF NOT EXISTS provider_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider TEXT NOT NULL,       -- 'HARAMAIN', 'SAPTCO', 'ECB', 'system'
    metric TEXT NOT NULL,         -- 'coverage_hotels', 'offers_count', 'transport_rows', 'fx_updated'
    value NUMERIC(18, 4) NOT NULL,
    metadata JSONB,
    ts TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_metrics_provider_ts ON provider_metrics(provider, ts DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_metric_ts ON provider_metrics(metric, ts DESC);

-- ============================================================================
-- Alert Rules (Simple threshold-based)
-- ============================================================================
CREATE TABLE IF NOT EXISTS alert_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    metric TEXT NOT NULL,
    operator TEXT NOT NULL CHECK (operator IN ('<', '>', '<=', '>=', '=')),
    threshold NUMERIC(18, 4) NOT NULL,
    severity TEXT DEFAULT 'WARNING' CHECK (severity IN ('INFO', 'WARNING', 'CRITICAL')),
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Default alert rules
INSERT INTO alert_rules (name, metric, operator, threshold, severity)
VALUES
    ('low_offers_24h', 'offers_24h', '<', 50, 'WARNING'),
    ('no_transport_24h', 'transport_24h', '<', 1, 'CRITICAL'),
    ('fx_stale', 'fx_age_hours', '>', 48, 'WARNING'),
    ('scrape_fail_rate', 'scrape_fail_pct', '>', 50, 'CRITICAL')
ON CONFLICT (name) DO NOTHING;

-- ============================================================================
-- Transport Snapshots (Last known good data for fallback)
-- ============================================================================
CREATE TABLE IF NOT EXISTS transport_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    operator TEXT NOT NULL,
    route TEXT NOT NULL,
    snapshot_data JSONB NOT NULL,
    snapshot_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_transport_snapshots_op_route ON transport_snapshots(operator, route);
