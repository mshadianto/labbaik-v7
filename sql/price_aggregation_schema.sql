-- =============================================================================
-- LABBAIK AI v7.5 - Real-time Price Aggregation Schema
-- =============================================================================
-- Run this script to create price aggregation tables
-- psql $DATABASE_URL < sql/price_aggregation_schema.sql

-- =====================================================
-- AGGREGATED PRICES (normalized from all sources)
-- =====================================================
CREATE TABLE IF NOT EXISTS aggregated_prices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    offer_hash VARCHAR(64) NOT NULL,
    source_type VARCHAR(20) NOT NULL,
    source_name VARCHAR(50) NOT NULL,
    source_offer_id VARCHAR(100),

    -- Offer Details
    offer_type VARCHAR(20) NOT NULL,
    name VARCHAR(255) NOT NULL,
    name_normalized VARCHAR(255),
    city VARCHAR(50) NOT NULL,

    -- Hotel-specific
    stars INTEGER,
    distance_to_haram_m INTEGER,
    walking_time_minutes INTEGER,
    amenities JSONB,

    -- Package-specific
    duration_days INTEGER,
    departure_city VARCHAR(50),
    airline VARCHAR(50),
    hotel_makkah VARCHAR(100),
    hotel_makkah_stars INTEGER,
    hotel_madinah VARCHAR(100),
    hotel_madinah_stars INTEGER,
    inclusions JSONB,

    -- Pricing
    price_sar DECIMAL(12, 2),
    price_idr DECIMAL(15, 0),
    price_per_night_sar DECIMAL(10, 2),
    price_per_night_idr DECIMAL(12, 0),
    currency_original VARCHAR(3) DEFAULT 'IDR',

    -- Validity
    check_in_date DATE,
    check_out_date DATE,
    valid_from TIMESTAMP,
    valid_until TIMESTAMP,

    -- Availability
    is_available BOOLEAN DEFAULT true,
    availability_status VARCHAR(20) DEFAULT 'available',
    rooms_left INTEGER,
    quota INTEGER,

    -- Metadata
    source_url TEXT,
    raw_data JSONB,
    confidence_score DECIMAL(3, 2) DEFAULT 1.00,

    -- Timestamps
    scraped_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Unique constraint
    CONSTRAINT uq_offer_source_date UNIQUE (offer_hash, source_name, check_in_date)
);

-- Indexes for aggregated_prices
CREATE INDEX IF NOT EXISTS idx_agg_prices_city ON aggregated_prices(city);
CREATE INDEX IF NOT EXISTS idx_agg_prices_type ON aggregated_prices(offer_type);
CREATE INDEX IF NOT EXISTS idx_agg_prices_source ON aggregated_prices(source_type, source_name);
CREATE INDEX IF NOT EXISTS idx_agg_prices_price ON aggregated_prices(price_idr);
CREATE INDEX IF NOT EXISTS idx_agg_prices_stars ON aggregated_prices(stars);
CREATE INDEX IF NOT EXISTS idx_agg_prices_checkin ON aggregated_prices(check_in_date);
CREATE INDEX IF NOT EXISTS idx_agg_prices_available ON aggregated_prices(is_available);
CREATE INDEX IF NOT EXISTS idx_agg_prices_updated ON aggregated_prices(updated_at);
CREATE INDEX IF NOT EXISTS idx_agg_prices_name_norm ON aggregated_prices(name_normalized);

-- =====================================================
-- PRICE HISTORY (for trend analysis)
-- =====================================================
CREATE TABLE IF NOT EXISTS price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregated_price_id UUID REFERENCES aggregated_prices(id) ON DELETE CASCADE,

    -- Price snapshot
    price_sar DECIMAL(12, 2) NOT NULL,
    price_idr DECIMAL(15, 0) NOT NULL,
    availability_status VARCHAR(20),
    rooms_left INTEGER,

    -- Context
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_name VARCHAR(50) NOT NULL,

    -- Trend computation
    price_change_sar DECIMAL(12, 2),
    price_change_percent DECIMAL(5, 2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_price_history_agg ON price_history(aggregated_price_id);
CREATE INDEX IF NOT EXISTS idx_price_history_recorded ON price_history(recorded_at);
CREATE INDEX IF NOT EXISTS idx_price_history_source ON price_history(source_name);

-- =====================================================
-- PARTNER PRICE FEEDS
-- =====================================================
CREATE TABLE IF NOT EXISTS partner_price_feeds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id UUID NOT NULL,

    -- Feed Metadata
    feed_name VARCHAR(100) NOT NULL,
    feed_type VARCHAR(20) NOT NULL DEFAULT 'package',

    -- Pricing
    price_idr DECIMAL(15, 0) NOT NULL,
    price_sar DECIMAL(12, 2),
    price_per_person_idr DECIMAL(15, 0),

    -- Package Details
    package_name VARCHAR(255),
    description TEXT,
    hotel_makkah VARCHAR(100),
    hotel_makkah_stars INTEGER,
    hotel_madinah VARCHAR(100),
    hotel_madinah_stars INTEGER,
    duration_days INTEGER,
    departure_city VARCHAR(50),
    departure_dates JSONB,
    airline VARCHAR(50),
    flight_class VARCHAR(20) DEFAULT 'economy',
    room_type VARCHAR(20) DEFAULT 'quad',
    inclusions JSONB,
    exclusions JSONB,
    itinerary JSONB,

    -- Availability
    quota INTEGER DEFAULT 0,
    booked INTEGER DEFAULT 0,
    is_available BOOLEAN DEFAULT true,

    -- Validity
    valid_from DATE,
    valid_until DATE,

    -- Business
    commission_rate DECIMAL(4, 2) DEFAULT 10.00,
    markup_percent DECIMAL(4, 2),

    -- Approval
    status VARCHAR(20) DEFAULT 'pending',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP,
    approved_by UUID,
    rejection_reason TEXT,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_partner_feeds_partner ON partner_price_feeds(partner_id);
CREATE INDEX IF NOT EXISTS idx_partner_feeds_status ON partner_price_feeds(status);
CREATE INDEX IF NOT EXISTS idx_partner_feeds_valid ON partner_price_feeds(valid_from, valid_until);
CREATE INDEX IF NOT EXISTS idx_partner_feeds_type ON partner_price_feeds(feed_type);
CREATE INDEX IF NOT EXISTS idx_partner_feeds_city ON partner_price_feeds(departure_city);

-- =====================================================
-- SCRAPING JOBS (background job tracking)
-- =====================================================
CREATE TABLE IF NOT EXISTS scraping_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Job Details
    job_type VARCHAR(50) NOT NULL,
    job_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    priority INTEGER DEFAULT 0,

    -- Configuration
    config JSONB,
    target_sources JSONB,

    -- Results
    items_found INTEGER DEFAULT 0,
    items_saved INTEGER DEFAULT 0,
    items_updated INTEGER DEFAULT 0,
    items_failed INTEGER DEFAULT 0,
    errors JSONB,
    result_summary JSONB,

    -- Timing
    scheduled_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_seconds INTEGER,

    -- Metadata
    triggered_by VARCHAR(50) DEFAULT 'scheduler',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_scraping_jobs_status ON scraping_jobs(status);
CREATE INDEX IF NOT EXISTS idx_scraping_jobs_type ON scraping_jobs(job_type);
CREATE INDEX IF NOT EXISTS idx_scraping_jobs_scheduled ON scraping_jobs(scheduled_at);

-- =====================================================
-- PRICE ALERTS (user subscriptions)
-- =====================================================
CREATE TABLE IF NOT EXISTS price_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,

    -- Alert Name
    alert_name VARCHAR(100),

    -- Alert Criteria
    offer_type VARCHAR(20) NOT NULL DEFAULT 'package',
    city VARCHAR(50),
    target_price_idr DECIMAL(15, 0),
    max_price_idr DECIMAL(15, 0),
    hotel_stars_min INTEGER,
    hotel_stars_max INTEGER,
    departure_city VARCHAR(50),
    check_in_from DATE,
    check_in_to DATE,
    duration_days_min INTEGER,
    duration_days_max INTEGER,

    -- Notification Settings
    notify_email BOOLEAN DEFAULT true,
    notify_whatsapp BOOLEAN DEFAULT false,
    notify_push BOOLEAN DEFAULT false,

    -- Trigger Settings
    trigger_on_price_drop BOOLEAN DEFAULT true,
    trigger_on_new_offer BOOLEAN DEFAULT false,
    min_price_drop_percent DECIMAL(4, 2) DEFAULT 5.00,

    -- Status
    is_active BOOLEAN DEFAULT true,
    last_triggered_at TIMESTAMP,
    trigger_count INTEGER DEFAULT 0,
    last_checked_at TIMESTAMP,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_price_alerts_user ON price_alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_price_alerts_active ON price_alerts(is_active);
CREATE INDEX IF NOT EXISTS idx_price_alerts_city ON price_alerts(city);

-- =====================================================
-- DATA SOURCE STATS (tracking source health)
-- =====================================================
CREATE TABLE IF NOT EXISTS data_source_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    source_name VARCHAR(50) NOT NULL,
    source_type VARCHAR(20) NOT NULL,

    -- Stats
    total_offers INTEGER DEFAULT 0,
    active_offers INTEGER DEFAULT 0,
    avg_price_idr DECIMAL(15, 0),
    min_price_idr DECIMAL(15, 0),
    max_price_idr DECIMAL(15, 0),

    -- Health
    last_successful_fetch TIMESTAMP,
    last_failed_fetch TIMESTAMP,
    consecutive_failures INTEGER DEFAULT 0,
    success_rate DECIMAL(5, 2),
    avg_response_time_ms INTEGER,

    -- Quota (for rate-limited APIs)
    daily_quota INTEGER,
    daily_used INTEGER DEFAULT 0,
    quota_reset_at TIMESTAMP,

    -- Timestamps
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_source_stats UNIQUE (source_name, recorded_at::date)
);

CREATE INDEX IF NOT EXISTS idx_source_stats_name ON data_source_stats(source_name);
CREATE INDEX IF NOT EXISTS idx_source_stats_recorded ON data_source_stats(recorded_at);

-- =====================================================
-- FUNCTIONS & TRIGGERS
-- =====================================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tables
DROP TRIGGER IF EXISTS update_aggregated_prices_updated_at ON aggregated_prices;
CREATE TRIGGER update_aggregated_prices_updated_at
    BEFORE UPDATE ON aggregated_prices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_partner_feeds_updated_at ON partner_price_feeds;
CREATE TRIGGER update_partner_feeds_updated_at
    BEFORE UPDATE ON partner_price_feeds
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_price_alerts_updated_at ON price_alerts;
CREATE TRIGGER update_price_alerts_updated_at
    BEFORE UPDATE ON price_alerts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- VIEWS
-- =====================================================

-- Best prices per source and city
CREATE OR REPLACE VIEW v_best_prices_by_source AS
SELECT DISTINCT ON (source_name, city, offer_type)
    source_name,
    source_type,
    city,
    offer_type,
    name,
    stars,
    price_idr,
    price_sar,
    is_available,
    updated_at
FROM aggregated_prices
WHERE is_available = true
ORDER BY source_name, city, offer_type, price_idr ASC;

-- Price trends summary
CREATE OR REPLACE VIEW v_price_trends AS
SELECT
    ap.id,
    ap.name,
    ap.city,
    ap.source_name,
    ap.price_idr as current_price_idr,
    ph.price_idr as previous_price_idr,
    CASE
        WHEN ph.price_idr IS NOT NULL AND ph.price_idr > 0
        THEN ROUND(((ap.price_idr - ph.price_idr) / ph.price_idr * 100)::numeric, 2)
        ELSE 0
    END as change_percent,
    CASE
        WHEN ap.price_idr < COALESCE(ph.price_idr, ap.price_idr) THEN 'down'
        WHEN ap.price_idr > COALESCE(ph.price_idr, ap.price_idr) THEN 'up'
        ELSE 'stable'
    END as trend_direction
FROM aggregated_prices ap
LEFT JOIN LATERAL (
    SELECT price_idr
    FROM price_history
    WHERE aggregated_price_id = ap.id
    ORDER BY recorded_at DESC
    LIMIT 1 OFFSET 1
) ph ON true
WHERE ap.is_available = true;

-- =====================================================
-- SAMPLE DATA (Optional - for testing)
-- =====================================================

-- Uncomment below to insert sample data for testing
/*
INSERT INTO aggregated_prices (
    offer_hash, source_type, source_name, offer_type, name, name_normalized,
    city, stars, distance_to_haram_m, price_sar, price_idr, is_available
) VALUES
    (md5('demo-hotel-1'), 'demo', 'demo', 'hotel', 'Hilton Makkah Convention', 'hilton makkah convention', 'Makkah', 5, 450, 850, 3612500, true),
    (md5('demo-hotel-2'), 'demo', 'demo', 'hotel', 'Swissotel Al Maqam', 'swissotel al maqam', 'Makkah', 5, 200, 1200, 5100000, true),
    (md5('demo-hotel-3'), 'demo', 'demo', 'hotel', 'Pullman Zamzam Makkah', 'pullman zamzam makkah', 'Makkah', 5, 100, 1500, 6375000, true)
ON CONFLICT DO NOTHING;
*/

-- =====================================================
-- GRANTS (if needed)
-- =====================================================
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_app_user;
