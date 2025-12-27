"""
LABBAIK AI - User Repository
=============================
Database operations for user management.
Uses SQLite for simplicity, can be upgraded to PostgreSQL.
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
import streamlit as st

# Import user models
from services.user.user_service import User, UserRole, UserStatus


# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "labbaik.db")


def ensure_db_dir():
    """Ensure database directory exists"""
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)


class UserRepository:
    """Repository for user database operations"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        ensure_db_dir()
        self._init_db()

    @contextmanager
    def _get_connection(self):
        """Get database connection with context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        """Initialize database schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    login_count INTEGER DEFAULT 0,

                    -- Analytics/UTM
                    source TEXT,
                    referral_code TEXT,
                    utm_source TEXT,
                    utm_medium TEXT,
                    utm_campaign TEXT
                )
            """)

            # User activities table for tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    activity_type TEXT NOT NULL,
                    activity_data TEXT,
                    page TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

            # User sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_status ON users(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_created ON users(created_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_activities_user ON user_activities(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id)")

            conn.commit()

            # Auto-create admin from secrets
            self._ensure_admin_exists()

    def _ensure_admin_exists(self):
        """Auto-create admin user from Streamlit secrets if not exists"""
        import hashlib
        import secrets as sec

        try:
            # Try to get admin credentials from Streamlit secrets
            admin_email = None
            admin_password = None
            admin_name = "Admin"

            if hasattr(st, 'secrets'):
                admin_email = st.secrets.get("ADMIN_EMAIL")
                admin_password = st.secrets.get("ADMIN_PASSWORD")
                admin_name = st.secrets.get("ADMIN_NAME", "Admin")

            # Also check environment variables
            if not admin_email:
                admin_email = os.environ.get("ADMIN_EMAIL")
            if not admin_password:
                admin_password = os.environ.get("ADMIN_PASSWORD")

            if not admin_email or not admin_password:
                return  # No admin credentials configured

            admin_email = admin_email.lower().strip()

            # Check if admin already exists
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE email = ?", (admin_email,))
                if cursor.fetchone():
                    return  # Admin already exists

                # Hash password
                salt = sec.token_hex(16)
                hash_obj = hashlib.pbkdf2_hmac(
                    'sha256',
                    admin_password.encode('utf-8'),
                    salt.encode('utf-8'),
                    100000
                )
                password_hash = f"{salt}${hash_obj.hex()}"

                # Create admin user
                now = datetime.now().isoformat()
                cursor.execute("""
                    INSERT INTO users (email, name, password_hash, role, status, created_at, updated_at, login_count, source)
                    VALUES (?, ?, ?, 'admin', 'active', ?, ?, 0, 'system')
                """, (admin_email, admin_name, password_hash, now, now))
                conn.commit()
                print(f"[AUTO] Admin user created: {admin_email}")

        except Exception as e:
            # Silently fail - don't break app startup
            print(f"[WARN] Auto-admin creation failed: {e}")

    def _row_to_user(self, row: sqlite3.Row) -> User:
        """Convert database row to User object"""
        return User(
            id=row["id"],
            email=row["email"],
            name=row["name"],
            phone=row["phone"],
            password_hash=row["password_hash"],
            role=UserRole(row["role"]) if row["role"] else UserRole.FREE,
            status=UserStatus(row["status"]) if row["status"] else UserStatus.PENDING,
            city=row["city"],
            province=row["province"],
            preferred_departure_city=row["preferred_departure_city"],
            budget_range=row["budget_range"],
            travel_style=row["travel_style"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else datetime.now(),
            updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else datetime.now(),
            last_login=datetime.fromisoformat(row["last_login"]) if row["last_login"] else None,
            login_count=row["login_count"] or 0,
            source=row["source"],
            referral_code=row["referral_code"],
            utm_source=row["utm_source"],
            utm_medium=row["utm_medium"],
            utm_campaign=row["utm_campaign"],
        )

    def create(self, user: User) -> Optional[User]:
        """Create new user"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (
                        email, name, phone, password_hash, role, status,
                        city, province, preferred_departure_city, budget_range, travel_style,
                        created_at, updated_at, login_count,
                        source, referral_code, utm_source, utm_medium, utm_campaign
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user.email, user.name, user.phone, user.password_hash,
                    user.role.value, user.status.value,
                    user.city, user.province, user.preferred_departure_city,
                    user.budget_range, user.travel_style,
                    user.created_at.isoformat(), user.updated_at.isoformat(),
                    user.login_count,
                    user.source, user.referral_code,
                    user.utm_source, user.utm_medium, user.utm_campaign
                ))
                conn.commit()
                user.id = cursor.lastrowid
                return user
            except sqlite3.IntegrityError:
                return None

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return self._row_to_user(row) if row else None

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email.lower(),))
            row = cursor.fetchone()
            return self._row_to_user(row) if row else None

    def update(self, user: User) -> bool:
        """Update user"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET
                    name = ?, phone = ?, role = ?, status = ?,
                    city = ?, province = ?, preferred_departure_city = ?,
                    budget_range = ?, travel_style = ?,
                    updated_at = ?, last_login = ?, login_count = ?
                WHERE id = ?
            """, (
                user.name, user.phone, user.role.value, user.status.value,
                user.city, user.province, user.preferred_departure_city,
                user.budget_range, user.travel_style,
                user.updated_at.isoformat(),
                user.last_login.isoformat() if user.last_login else None,
                user.login_count,
                user.id
            ))
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, user_id: int) -> bool:
        """Delete user"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """Get all users with pagination"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
            return [self._row_to_user(row) for row in cursor.fetchall()]

    def search(self, query: str) -> List[User]:
        """Search users by name or email"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            search_term = f"%{query}%"
            cursor.execute("""
                SELECT * FROM users
                WHERE name LIKE ? OR email LIKE ?
                ORDER BY created_at DESC
                LIMIT 50
            """, (search_term, search_term))
            return [self._row_to_user(row) for row in cursor.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        """Get user statistics"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            stats = {}

            # Total users
            cursor.execute("SELECT COUNT(*) FROM users")
            stats["total_users"] = cursor.fetchone()[0]

            # Users by role
            cursor.execute("""
                SELECT role, COUNT(*) as count
                FROM users
                GROUP BY role
            """)
            stats["by_role"] = {row["role"]: row["count"] for row in cursor.fetchall()}

            # Users by status
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM users
                GROUP BY status
            """)
            stats["by_status"] = {row["status"]: row["count"] for row in cursor.fetchall()}

            # Users by source
            cursor.execute("""
                SELECT source, COUNT(*) as count
                FROM users
                WHERE source IS NOT NULL
                GROUP BY source
            """)
            stats["by_source"] = {row["source"]: row["count"] for row in cursor.fetchall()}

            # Users by province
            cursor.execute("""
                SELECT province, COUNT(*) as count
                FROM users
                WHERE province IS NOT NULL
                GROUP BY province
                ORDER BY count DESC
                LIMIT 10
            """)
            stats["by_province"] = {row["province"]: row["count"] for row in cursor.fetchall()}

            # Registrations per day (last 30 days)
            cursor.execute("""
                SELECT DATE(created_at) as date, COUNT(*) as count
                FROM users
                WHERE created_at >= datetime('now', '-30 days')
                GROUP BY DATE(created_at)
                ORDER BY date
            """)
            stats["daily_registrations"] = [
                {"date": row["date"], "count": row["count"]}
                for row in cursor.fetchall()
            ]

            # Active users (logged in last 7 days)
            cursor.execute("""
                SELECT COUNT(*) FROM users
                WHERE last_login >= datetime('now', '-7 days')
            """)
            stats["active_7d"] = cursor.fetchone()[0]

            # New users today
            cursor.execute("""
                SELECT COUNT(*) FROM users
                WHERE DATE(created_at) = DATE('now')
            """)
            stats["new_today"] = cursor.fetchone()[0]

            # Budget range distribution
            cursor.execute("""
                SELECT budget_range, COUNT(*) as count
                FROM users
                WHERE budget_range IS NOT NULL
                GROUP BY budget_range
            """)
            stats["by_budget"] = {row["budget_range"]: row["count"] for row in cursor.fetchall()}

            return stats

    def log_activity(self, user_id: Optional[int], activity_type: str,
                     activity_data: str = None, page: str = None):
        """Log user activity"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_activities (user_id, activity_type, activity_data, page)
                VALUES (?, ?, ?, ?)
            """, (user_id, activity_type, activity_data, page))
            conn.commit()

    def get_user_activities(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user activities"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM user_activities
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, limit))
            return [dict(row) for row in cursor.fetchall()]


# Singleton instance
_user_repository: Optional[UserRepository] = None


def get_user_repository() -> UserRepository:
    """Get singleton UserRepository instance"""
    global _user_repository
    if _user_repository is None:
        _user_repository = UserRepository()
    return _user_repository
