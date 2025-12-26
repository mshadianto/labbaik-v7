"""
Umrah Crawler Settings
"""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Database
    database_url: str = os.getenv("DATABASE_URL", "")

    # Amadeus API
    amadeus_client_id: str = os.getenv("AMADEUS_CLIENT_ID", "")
    amadeus_client_secret: str = os.getenv("AMADEUS_CLIENT_SECRET", "")

    # RapidAPI (Xotelo)
    xotelo_rapidapi_key: str = os.getenv("XOTELO_RAPIDAPI_KEY", "")

    # MakCorps
    makcorps_api_key: str = os.getenv("MAKCORPS_API_KEY", "")

    # Rate limiting
    default_rps: float = 1.0  # requests per second

    # Job settings
    job_batch_size: int = 10
    job_interval_minutes: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
