"""
LABBAIK AI - Partner API Service
=================================
API key management and partner API operations.
"""

import sqlite3
import os
import secrets
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from enum import Enum


# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "labbaik.db")


class APIKeyStatus(str, Enum):
    """API Key status"""
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    RATE_LIMITED = "rate_limited"


@dataclass
class APIKey:
    """API Key model"""
    id: Optional[int] = None
    partner_id: int = 0
    key_hash: str = ""
    key_prefix: str = ""  # First 8 chars for identification
    name: str = ""
    status: APIKeyStatus = APIKeyStatus.ACTIVE

    # Permissions
    permissions: List[str] = field(default_factory=list)
    rate_limit: int = 1000  # Requests per day
    requests_today: int = 0

    # Tracking
    created_at: datetime = field(default_factory=datetime.now)
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    @property
    def is_valid(self) -> bool:
        """Check if key is valid"""
        if self.status != APIKeyStatus.ACTIVE:
            return False
        if self.expires_at and self.expires_at < datetime.now():
            return False
        return True

    def has_permission(self, permission: str) -> bool:
        """Check if key has permission"""
        return "*" in self.permissions or permission in self.permissions


def generate_api_key() -> tuple[str, str]:
    """
    Generate new API key.
    Returns: (full_key, key_hash)
    """
    # Format: lbk_live_xxxxxxxxxxxxxxxxxxxx
    random_part = secrets.token_hex(24)
    full_key = f"lbk_live_{random_part}"

    # Hash for storage
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()

    return full_key, key_hash


class PartnerAPI:
    """Partner API management service"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        """Initialize API tables"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # API Keys table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    partner_id INTEGER NOT NULL,
                    key_hash TEXT UNIQUE NOT NULL,
                    key_prefix TEXT NOT NULL,
                    name TEXT,
                    status TEXT DEFAULT 'active',

                    permissions TEXT,
                    rate_limit INTEGER DEFAULT 1000,
                    requests_today INTEGER DEFAULT 0,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used_at TIMESTAMP,
                    expires_at TIMESTAMP,

                    FOREIGN KEY (partner_id) REFERENCES users(id)
                )
            """)

            # API Request Logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    api_key_id INTEGER,
                    partner_id INTEGER,
                    endpoint TEXT NOT NULL,
                    method TEXT NOT NULL,
                    status_code INTEGER,
                    response_time_ms INTEGER,
                    ip_address TEXT,
                    user_agent TEXT,
                    request_body TEXT,
                    response_body TEXT,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (api_key_id) REFERENCES api_keys(id)
                )
            """)

            # Webhooks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS webhooks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    partner_id INTEGER NOT NULL,
                    url TEXT NOT NULL,
                    events TEXT NOT NULL,
                    secret TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    last_triggered_at TIMESTAMP,
                    failure_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (partner_id) REFERENCES users(id)
                )
            """)

            # Partner packages (packages uploaded by partners)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS partner_packages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    partner_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    price INTEGER NOT NULL,
                    duration_days INTEGER,
                    departure_city TEXT,
                    departure_dates TEXT,
                    hotel_makkah TEXT,
                    hotel_madinah TEXT,
                    airline TEXT,
                    inclusions TEXT,
                    exclusions TEXT,
                    quota INTEGER DEFAULT 0,
                    booked INTEGER DEFAULT 0,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (partner_id) REFERENCES users(id)
                )
            """)

            # Partner bookings
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS partner_bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    booking_code TEXT UNIQUE NOT NULL,
                    partner_id INTEGER NOT NULL,
                    package_id INTEGER NOT NULL,
                    customer_name TEXT NOT NULL,
                    customer_email TEXT,
                    customer_phone TEXT,
                    num_pax INTEGER DEFAULT 1,
                    total_price INTEGER NOT NULL,
                    commission_amount INTEGER,
                    status TEXT DEFAULT 'pending',
                    payment_status TEXT DEFAULT 'unpaid',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (partner_id) REFERENCES users(id),
                    FOREIGN KEY (package_id) REFERENCES partner_packages(id)
                )
            """)

            # Indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_apikey_hash ON api_keys(key_hash)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_apikey_partner ON api_keys(partner_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_apilogs_key ON api_logs(api_key_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_packages_partner ON partner_packages(partner_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_bookings_partner ON partner_bookings(partner_id)")

            conn.commit()

    def create_api_key(
        self,
        partner_id: int,
        name: str = "Default API Key",
        permissions: List[str] = None,
        rate_limit: int = 1000,
        expires_days: int = None
    ) -> tuple[str, APIKey]:
        """
        Create new API key for partner.
        Returns: (full_key, api_key_object)
        """
        full_key, key_hash = generate_api_key()
        key_prefix = full_key[:12]

        if permissions is None:
            permissions = ["packages:read", "bookings:read", "bookings:write"]

        expires_at = None
        if expires_days:
            expires_at = datetime.now() + timedelta(days=expires_days)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO api_keys (
                    partner_id, key_hash, key_prefix, name, status,
                    permissions, rate_limit, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                partner_id, key_hash, key_prefix, name, APIKeyStatus.ACTIVE.value,
                ",".join(permissions), rate_limit,
                expires_at.isoformat() if expires_at else None
            ))
            conn.commit()

            api_key = APIKey(
                id=cursor.lastrowid,
                partner_id=partner_id,
                key_hash=key_hash,
                key_prefix=key_prefix,
                name=name,
                status=APIKeyStatus.ACTIVE,
                permissions=permissions,
                rate_limit=rate_limit,
                expires_at=expires_at
            )

        return full_key, api_key

    def validate_api_key(self, api_key: str) -> tuple[bool, str, Optional[APIKey]]:
        """
        Validate API key.
        Returns: (is_valid, error_message, api_key_object)
        """
        if not api_key or not api_key.startswith("lbk_live_"):
            return False, "Invalid API key format", None

        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM api_keys WHERE key_hash = ?
            """, (key_hash,))
            row = cursor.fetchone()

            if not row:
                return False, "API key not found", None

            api_key_obj = self._row_to_apikey(row)

            if api_key_obj.status == APIKeyStatus.REVOKED:
                return False, "API key has been revoked", None

            if api_key_obj.expires_at and api_key_obj.expires_at < datetime.now():
                return False, "API key has expired", None

            # Check rate limit
            if api_key_obj.requests_today >= api_key_obj.rate_limit:
                return False, "Rate limit exceeded", None

            # Update usage
            cursor.execute("""
                UPDATE api_keys
                SET requests_today = requests_today + 1,
                    last_used_at = datetime('now')
                WHERE id = ?
            """, (api_key_obj.id,))
            conn.commit()

            return True, "", api_key_obj

    def _row_to_apikey(self, row: sqlite3.Row) -> APIKey:
        """Convert row to APIKey object"""
        return APIKey(
            id=row["id"],
            partner_id=row["partner_id"],
            key_hash=row["key_hash"],
            key_prefix=row["key_prefix"],
            name=row["name"],
            status=APIKeyStatus(row["status"]) if row["status"] else APIKeyStatus.ACTIVE,
            permissions=row["permissions"].split(",") if row["permissions"] else [],
            rate_limit=row["rate_limit"] or 1000,
            requests_today=row["requests_today"] or 0,
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else datetime.now(),
            last_used_at=datetime.fromisoformat(row["last_used_at"]) if row["last_used_at"] else None,
            expires_at=datetime.fromisoformat(row["expires_at"]) if row["expires_at"] else None,
        )

    def get_partner_keys(self, partner_id: int) -> List[APIKey]:
        """Get all API keys for a partner"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM api_keys WHERE partner_id = ? ORDER BY created_at DESC
            """, (partner_id,))
            return [self._row_to_apikey(row) for row in cursor.fetchall()]

    def revoke_api_key(self, key_id: int, partner_id: int) -> bool:
        """Revoke an API key"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE api_keys SET status = ? WHERE id = ? AND partner_id = ?
            """, (APIKeyStatus.REVOKED.value, key_id, partner_id))
            conn.commit()
            return cursor.rowcount > 0

    def log_request(
        self,
        api_key_id: int,
        partner_id: int,
        endpoint: str,
        method: str,
        status_code: int,
        response_time_ms: int,
        ip_address: str = None,
        user_agent: str = None,
        request_body: str = None,
        response_body: str = None,
        error_message: str = None
    ):
        """Log API request"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO api_logs (
                    api_key_id, partner_id, endpoint, method, status_code,
                    response_time_ms, ip_address, user_agent,
                    request_body, response_body, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                api_key_id, partner_id, endpoint, method, status_code,
                response_time_ms, ip_address, user_agent,
                request_body, response_body, error_message
            ))
            conn.commit()

    def get_api_stats(self, partner_id: int) -> Dict[str, Any]:
        """Get API usage statistics for partner"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            stats = {}

            # Total requests today
            cursor.execute("""
                SELECT SUM(requests_today) FROM api_keys WHERE partner_id = ?
            """, (partner_id,))
            stats["requests_today"] = cursor.fetchone()[0] or 0

            # Total requests all time
            cursor.execute("""
                SELECT COUNT(*) FROM api_logs WHERE partner_id = ?
            """, (partner_id,))
            stats["total_requests"] = cursor.fetchone()[0]

            # Requests by endpoint
            cursor.execute("""
                SELECT endpoint, COUNT(*) as count
                FROM api_logs
                WHERE partner_id = ?
                GROUP BY endpoint
                ORDER BY count DESC
                LIMIT 10
            """, (partner_id,))
            stats["by_endpoint"] = {row["endpoint"]: row["count"] for row in cursor.fetchall()}

            # Error rate
            cursor.execute("""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as errors
                FROM api_logs
                WHERE partner_id = ?
                AND created_at >= datetime('now', '-24 hours')
            """, (partner_id,))
            row = cursor.fetchone()
            total = row["total"] or 1
            errors = row["errors"] or 0
            stats["error_rate_24h"] = round(errors / total * 100, 2)

            # Avg response time
            cursor.execute("""
                SELECT AVG(response_time_ms) FROM api_logs
                WHERE partner_id = ?
                AND created_at >= datetime('now', '-24 hours')
            """, (partner_id,))
            stats["avg_response_time_ms"] = round(cursor.fetchone()[0] or 0, 2)

            return stats

    def reset_daily_limits(self):
        """Reset daily request counts (run daily via cron)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE api_keys SET requests_today = 0")
            conn.commit()


# Singleton
_partner_api: Optional[PartnerAPI] = None


def get_partner_api() -> PartnerAPI:
    """Get singleton PartnerAPI instance"""
    global _partner_api
    if _partner_api is None:
        _partner_api = PartnerAPI()
    return _partner_api
