# Strategi Optimasi Neon DB - Labbaik AI

## Status Saat Ini
- **Compute Usage**: 87.8% dari monthly allowance
- **Tier**: Free (kemungkinan 0.25 CU, 191.9 hours/month)

---

## 1. Quick Wins (Immediate Actions)

### 1.1 Aktifkan Auto-Suspend di Neon Console
```
Neon Console → Project → Settings → Compute
- Auto-suspend delay: 300 seconds (5 menit)
- Scale to zero: Enabled
```
**Impact**: Compute hanya berjalan saat ada query aktif.

### 1.2 Kurangi Connection Pool Size
Edit `core/config.py` atau environment:
```python
# Dari 5 ke 2 connections
DATABASE_POOL_SIZE=2
```

### 1.3 Gunakan Neon Pooler URL
Ganti `DATABASE_URL` dengan pooler endpoint:
```
# Dari:
postgresql://user:pass@ep-xxx.neon.tech/labbaik

# Ke (pooled):
postgresql://user:pass@ep-xxx-pooler.neon.tech/labbaik?sslmode=require
```

---

## 2. Caching Strategy (Reduce DB Hits)

### 2.1 Current Cache TTLs
```python
# services/price_aggregation/cache_manager.py
SOURCE_TTLS = {
    "amadeus": 7200,     # 2 hours
    "xotelo": 3600,      # 1 hour
    "demo": 86400,       # 24 hours
}
```

### 2.2 Recommended: Increase Cache TTLs
```python
OPTIMIZED_TTLS = {
    "amadeus": 14400,    # 4 hours (dari 2)
    "xotelo": 7200,      # 2 hours (dari 1)
    "n8n": 21600,        # 6 hours (n8n sudah scheduled)
    "demo": 86400,       # 24 hours (keep)
    "partner": 7200,     # 2 hours (dari 1)
}
```

### 2.3 Add Application-Level Caching
```python
from functools import lru_cache
from datetime import datetime, timedelta

# Cache static data
@lru_cache(maxsize=100)
def get_travel_agents():
    """Cache travel agents for 1 hour."""
    return db.fetch_all("SELECT * FROM travel_agents")

# Use Streamlit session cache
@st.cache_data(ttl=3600)
def get_packages_cached(city: str):
    return db.fetch_all("SELECT * FROM packages WHERE city = %s", (city,))
```

---

## 3. Query Optimization

### 3.1 Hindari SELECT *
```python
# Bad - fetch semua kolom
cursor.execute("SELECT * FROM prices_packages")

# Good - fetch kolom yang dibutuhkan saja
cursor.execute("""
    SELECT id, package_name, price_idr, duration_days
    FROM prices_packages
""")
```

### 3.2 Batch Queries
```python
# Bad - N+1 queries
for package_id in package_ids:
    hotel = db.fetch_one("SELECT * FROM hotels WHERE package_id = %s", (package_id,))

# Good - single query
hotels = db.fetch_all("""
    SELECT * FROM hotels
    WHERE package_id = ANY(%s)
""", (package_ids,))
```

### 3.3 Use LIMIT dan Pagination
```python
# Always use LIMIT
cursor.execute("""
    SELECT * FROM prices_packages
    ORDER BY scraped_at DESC
    LIMIT 50
""")
```

### 3.4 Add Missing Indexes
```sql
-- Check existing indexes
SELECT tablename, indexname FROM pg_indexes WHERE schemaname = 'public';

-- Add if missing
CREATE INDEX IF NOT EXISTS idx_packages_city ON prices_packages(departure_city);
CREATE INDEX IF NOT EXISTS idx_packages_price ON prices_packages(price_idr);
CREATE INDEX IF NOT EXISTS idx_hotels_city ON prices_hotels(city);
CREATE INDEX IF NOT EXISTS idx_hotels_stars ON prices_hotels(star_rating);
CREATE INDEX IF NOT EXISTS idx_scraped_at ON prices_packages(scraped_at DESC);
```

---

## 4. Connection Management

### 4.1 Use Connection Pooling Properly
```python
# services/database/repository.py - sudah implemented
# Pastikan pool dikonfigurasi dengan benar:
self._pool = pool.ThreadedConnectionPool(
    minconn=1,      # Start dengan 1
    maxconn=2,      # Max 2 untuk free tier
    dsn=self._connection_string
)
```

### 4.2 Close Idle Connections
```python
# Di app.py, tambahkan cleanup on exit
import atexit

@atexit.register
def cleanup():
    from services.database import get_db
    get_db().close()
```

---

## 5. Reduce Background Jobs Frequency

### 5.1 Current Schedule (Too Frequent)
```python
# services/price_aggregation/scheduler.py
schedule = {
    "api_refresh": "every 2 hours",    # Terlalu sering
    "scraper_refresh": "every 6 hours",
    "partner_sync": "every 1 hour",    # Terlalu sering
}
```

### 5.2 Optimized Schedule
```python
OPTIMIZED_SCHEDULE = {
    "api_refresh": "every 6 hours",    # Kurangi dari 2 jam
    "scraper_refresh": "every 12 hours", # Kurangi dari 6 jam
    "partner_sync": "every 4 hours",   # Kurangi dari 1 jam
    "cleanup": "daily at 3am",         # Cleanup old data
}
```

---

## 6. Data Retention & Cleanup

### 6.1 Archive Old Price Data
```sql
-- Delete prices older than 30 days
DELETE FROM prices_packages
WHERE scraped_at < NOW() - INTERVAL '30 days';

DELETE FROM prices_hotels
WHERE scraped_at < NOW() - INTERVAL '30 days';

DELETE FROM prices_flights
WHERE scraped_at < NOW() - INTERVAL '30 days';
```

### 6.2 Vacuum Tables (Monthly)
```sql
-- Run via Neon SQL Editor
VACUUM ANALYZE prices_packages;
VACUUM ANALYZE prices_hotels;
VACUUM ANALYZE prices_flights;
```

---

## 7. Monitoring Compute Usage

### 7.1 Neon Console Metrics
```
Neon Console → Project → Monitoring
- Active time (hours)
- Compute time (CU hours)
- Data transfer
```

### 7.2 Add Query Logging (Development Only)
```python
# Untuk debug, log slow queries
import time
import logging

def fetch_with_timing(query, params=None):
    start = time.time()
    result = db.fetch_all(query, params)
    elapsed = time.time() - start

    if elapsed > 1.0:  # Log queries > 1 second
        logging.warning(f"Slow query ({elapsed:.2f}s): {query[:100]}")

    return result
```

---

## 8. Alternative: Use Demo Mode More

### 8.1 Fallback ke Demo Data
```python
# services/umrah/data_fetcher.py
def fetch_hotels(city, use_db=True):
    # Check compute budget
    if is_compute_low():
        return load_demo_hotels(city)

    # Use cache first
    cached = cache.get(f"hotels:{city}")
    if cached:
        return cached

    # Only then hit database
    return db.fetch_hotels(city)
```

### 8.2 Environment Flag
```bash
# .env atau secrets.toml
USE_DEMO_MODE=true  # Bypass DB untuk development
```

---

## 9. Upgrade Path (If Needed)

### Neon Plans Comparison
| Plan | Compute | Storage | Price |
|------|---------|---------|-------|
| Free | 0.25 CU, 191.9h | 0.5 GB | $0 |
| Launch | 1 CU, 300h | 10 GB | $19/mo |
| Scale | Autoscale | 50 GB | $69/mo |

### Kapan Upgrade?
- Free tier cukup untuk development & demo
- Launch tier untuk production dengan traffic rendah-sedang
- Scale tier untuk production dengan autoscaling

---

## 10. Implementation Checklist

### Immediate (Today)
- [ ] Enable auto-suspend di Neon Console
- [ ] Switch ke pooler URL
- [ ] Reduce pool size ke 2

### This Week
- [ ] Increase cache TTLs
- [ ] Add missing indexes
- [ ] Implement data cleanup job

### This Month
- [ ] Optimize heavy queries
- [ ] Add query timing logs
- [ ] Review and archive old data

---

## Quick Reference Commands

```bash
# Check current compute usage
# Go to: https://console.neon.tech → Project → Usage

# Test pooler connection
psql "postgresql://user:pass@ep-xxx-pooler.neon.tech/labbaik?sslmode=require"

# Check table sizes
psql -c "SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
         FROM pg_catalog.pg_statio_user_tables
         ORDER BY pg_total_relation_size(relid) DESC;"
```
