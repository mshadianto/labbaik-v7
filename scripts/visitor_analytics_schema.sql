-- =============================================================================
-- LABBAIK AI v6.0 - Visitor Analytics Schema
-- =============================================================================
-- Run this in Neon SQL Editor if tables don't exist
-- =============================================================================

-- Visitor Stats (summary statistics)
CREATE TABLE IF NOT EXISTS visitor_stats (
    id SERIAL PRIMARY KEY,
    stat_key VARCHAR(100) UNIQUE NOT NULL,
    stat_value INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT NOW()
);

-- Insert default stats if not exist
INSERT INTO visitor_stats (stat_key, stat_value) 
VALUES 
    ('total_visitors', 0),
    ('total_views', 0)
ON CONFLICT (stat_key) DO NOTHING;

-- Visitor Logs (detailed logs)
CREATE TABLE IF NOT EXISTS visitor_logs (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(50) NOT NULL,
    page VARCHAR(100) DEFAULT 'home',
    user_agent TEXT,
    ip_hash VARCHAR(64),
    visited_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_visitor_logs_session ON visitor_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_visitor_logs_date ON visitor_logs(visited_at);

-- Page Views (per-page analytics)
CREATE TABLE IF NOT EXISTS page_views (
    id SERIAL PRIMARY KEY,
    page_name VARCHAR(100) NOT NULL,
    session_id VARCHAR(50),
    viewed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_page_views_page ON page_views(page_name);
CREATE INDEX IF NOT EXISTS idx_page_views_date ON page_views(viewed_at);

-- =============================================================================
-- ADDITIONAL USEFUL QUERIES
-- =============================================================================

-- Get total visitors
-- SELECT stat_value FROM visitor_stats WHERE stat_key = 'total_visitors';

-- Get visitors today
-- SELECT COUNT(DISTINCT session_id) FROM visitor_logs WHERE visited_at >= CURRENT_DATE;

-- Get popular pages
-- SELECT page_name, COUNT(*) as views FROM page_views 
-- GROUP BY page_name ORDER BY views DESC LIMIT 5;

-- Get views trend (last 7 days)
-- SELECT DATE(viewed_at) as date, COUNT(*) as views FROM page_views 
-- WHERE viewed_at >= CURRENT_DATE - INTERVAL '7 days'
-- GROUP BY DATE(viewed_at) ORDER BY date;

-- Update visitor count manually
-- UPDATE visitor_stats SET stat_value = stat_value + 1, last_updated = NOW() 
-- WHERE stat_key = 'total_visitors';
