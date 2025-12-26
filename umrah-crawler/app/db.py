import os
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    # Schema dibuat via sql/schema.sql (psql), jadi di sini cukup ping koneksi
    async with engine.begin() as conn:
        await conn.exec_driver_sql("SELECT 1")


@asynccontextmanager
async def get_session():
    async with SessionLocal() as session:
        yield session
