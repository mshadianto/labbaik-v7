"""
LABBAIK AI - Initialize Admin User
===================================
Run once to create admin account.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.user.user_service import UserService, UserRole, UserStatus


def create_admin():
    """Create admin user"""
    service = UserService()

    # Admin credentials
    ADMIN_EMAIL = "mshadianto.v1@gmail.com"
    ADMIN_PASSWORD = "Labbaik2025!"  # Change after first login
    ADMIN_NAME = "MS Hadianto"

    # Check if already exists
    existing = service.get_user_by_email(ADMIN_EMAIL)
    if existing:
        if existing.role == UserRole.ADMIN:
            print(f"[OK] Admin sudah ada: {ADMIN_EMAIL}")
            return existing
        else:
            # Upgrade to admin
            existing.role = UserRole.ADMIN
            existing.status = UserStatus.ACTIVE
            service.repo.update(existing)
            print(f"[OK] User di-upgrade ke Admin: {ADMIN_EMAIL}")
            return existing

    # Create new admin
    success, message, user = service.register(
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD,
        name=ADMIN_NAME,
        source="system"
    )

    if success and user:
        # Set as admin
        user.role = UserRole.ADMIN
        user.status = UserStatus.ACTIVE
        service.repo.update(user)
        print(f"[OK] Admin berhasil dibuat!")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"   [!] Segera ganti password setelah login!")
        return user
    else:
        print(f"[ERROR] Gagal membuat admin: {message}")
        return None


if __name__ == "__main__":
    print("=" * 50)
    print("LABBAIK AI - Admin Initialization")
    print("=" * 50)
    create_admin()
    print("=" * 50)
