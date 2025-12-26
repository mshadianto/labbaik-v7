import os
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

# Handle missing DATABASE_URL gracefully
engine = None
SessionLocal = None

if DATABASE_URL:
    # Convert postgres:// to postgresql+asyncpg:// if needed
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

    engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    """Initialize database connection."""
    if not engine:
        print("WARNING: DATABASE_URL not set, running in demo mode")
        return False

    async with engine.begin() as conn:
        await conn.exec_driver_sql("SELECT 1")
    return True


@asynccontextmanager
async def get_session():
    """Get database session."""
    if not SessionLocal:
        raise RuntimeError("Database not configured. Set DATABASE_URL environment variable.")

    async with SessionLocal() as session:
        yield session


def is_db_configured() -> bool:
    """Check if database is configured."""
    return engine is not None
