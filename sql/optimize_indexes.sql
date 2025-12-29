-- =====================================================
-- LABBAIK AI - Database Optimization Indexes
-- =====================================================
-- Run this script to add missing indexes for better
-- query performance and reduced compute usage.
-- =====================================================

-- Prices Packages Table
CREATE INDEX IF NOT EXISTS idx_packages_city
    ON prices_packages(departure_city);

CREATE INDEX IF NOT EXISTS idx_packages_price
    ON prices_packages(price_idr);

CREATE INDEX IF NOT EXISTS idx_packages_scraped
    ON prices_packages(scraped_at DESC);

CREATE INDEX IF NOT EXISTS idx_packages_source
    ON prices_packages(source_id);

CREATE INDEX IF NOT EXISTS idx_packages_available
    ON prices_packages(is_available)
    WHERE is_available = true;

-- Prices Hotels Table
CREATE INDEX IF NOT EXISTS idx_hotels_city
    ON prices_hotels(city);

CREATE INDEX IF NOT EXISTS idx_hotels_stars
    ON prices_hotels(star_rating);

CREATE INDEX IF NOT EXISTS idx_hotels_price
    ON prices_hotels(price_per_night_idr);

CREATE INDEX IF NOT EXISTS idx_hotels_scraped
    ON prices_hotels(scraped_at DESC);

CREATE INDEX IF NOT EXISTS idx_hotels_distance
    ON prices_hotels(distance_meters);

-- Composite index for common search pattern
CREATE INDEX IF NOT EXISTS idx_hotels_city_stars
    ON prices_hotels(city, star_rating DESC);

-- Prices Flights Table
CREATE INDEX IF NOT EXISTS idx_flights_origin
    ON prices_flights(origin_city);

CREATE INDEX IF NOT EXISTS idx_flights_destination
    ON prices_flights(destination_city);

CREATE INDEX IF NOT EXISTS idx_flights_date
    ON prices_flights(departure_date);

CREATE INDEX IF NOT EXISTS idx_flights_price
    ON prices_flights(price_idr);

CREATE INDEX IF NOT EXISTS idx_flights_airline
    ON prices_flights(airline);

-- Composite index for route search
CREATE INDEX IF NOT EXISTS idx_flights_route
    ON prices_flights(origin_city, destination_city);

-- Users Table (if exists)
CREATE INDEX IF NOT EXISTS idx_users_email
    ON users(email);

CREATE INDEX IF NOT EXISTS idx_users_role
    ON users(role);

CREATE INDEX IF NOT EXISTS idx_users_active
    ON users(is_active)
    WHERE is_active = true;

-- Conversations Table (if exists)
CREATE INDEX IF NOT EXISTS idx_conversations_user
    ON conversations(user_id);

CREATE INDEX IF NOT EXISTS idx_conversations_updated
    ON conversations(updated_at DESC);

-- Bookings Table (if exists)
CREATE INDEX IF NOT EXISTS idx_bookings_user
    ON bookings(user_id);

CREATE INDEX IF NOT EXISTS idx_bookings_status
    ON bookings(status);

CREATE INDEX IF NOT EXISTS idx_bookings_created
    ON bookings(created_at DESC);

-- =====================================================
-- Analyze tables after index creation
-- =====================================================
ANALYZE prices_packages;
ANALYZE prices_hotels;
ANALYZE prices_flights;

-- Check index usage (run after some time)
-- SELECT
--     schemaname,
--     tablename,
--     indexname,
--     idx_scan,
--     idx_tup_read,
--     idx_tup_fetch
-- FROM pg_stat_user_indexes
-- ORDER BY idx_scan DESC;
