-- =====================================================
-- LABBAIK AI - Data Cleanup Script
-- =====================================================
-- Run periodically to remove old data and reduce
-- storage usage. Schedule via cron or run manually.
-- =====================================================

-- Configuration
-- Adjust retention periods as needed
DO $$
DECLARE
    price_retention_days INTEGER := 30;
    log_retention_days INTEGER := 7;
    deleted_count INTEGER;
BEGIN
    -- =====================================================
    -- 1. Clean old price data (older than 30 days)
    -- =====================================================

    -- Old packages
    DELETE FROM prices_packages
    WHERE scraped_at < NOW() - (price_retention_days || ' days')::INTERVAL;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RAISE NOTICE 'Deleted % old packages', deleted_count;

    -- Old hotels
    DELETE FROM prices_hotels
    WHERE scraped_at < NOW() - (price_retention_days || ' days')::INTERVAL;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RAISE NOTICE 'Deleted % old hotels', deleted_count;

    -- Old flights
    DELETE FROM prices_flights
    WHERE scraped_at < NOW() - (price_retention_days || ' days')::INTERVAL;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RAISE NOTICE 'Deleted % old flights', deleted_count;

    -- =====================================================
    -- 2. Clean old scraping logs (older than 7 days)
    -- =====================================================

    DELETE FROM scraping_logs
    WHERE created_at < NOW() - (log_retention_days || ' days')::INTERVAL;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RAISE NOTICE 'Deleted % old scraping logs', deleted_count;

    -- =====================================================
    -- 3. Archive old conversations (optional)
    -- =====================================================

    -- Mark old conversations as archived (not delete)
    UPDATE conversations
    SET is_archived = true
    WHERE updated_at < NOW() - INTERVAL '90 days'
    AND is_archived = false;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RAISE NOTICE 'Archived % old conversations', deleted_count;

END $$;

-- =====================================================
-- 4. Reclaim space with VACUUM
-- =====================================================
-- Note: VACUUM cannot run inside transaction block
-- Run these separately if needed:

-- VACUUM ANALYZE prices_packages;
-- VACUUM ANALYZE prices_hotels;
-- VACUUM ANALYZE prices_flights;
-- VACUUM ANALYZE scraping_logs;

-- =====================================================
-- 5. Check table sizes after cleanup
-- =====================================================
SELECT
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
    pg_size_pretty(pg_relation_size(relid)) AS data_size,
    pg_size_pretty(pg_indexes_size(relid)) AS index_size,
    n_live_tup AS row_count
FROM pg_catalog.pg_statio_user_tables
JOIN pg_stat_user_tables USING (relid)
ORDER BY pg_total_relation_size(relid) DESC;
