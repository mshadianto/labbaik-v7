"""Test Agoda snapshot functionality."""
import asyncio
import os
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.providers.agoda import fetch_agoda_hotels, refresh_agoda_snapshot


async def test_fetch():
    """Test fetching hotels from Agoda API."""
    print("=" * 60)
    print("Testing fetch_agoda_hotels()")
    print("=" * 60)

    for city in ["MAKKAH", "MADINAH"]:
        hotels = await fetch_agoda_hotels(city)
        print(f"\n{city}: {len(hotels)} hotels fetched")

        for h in hotels[:5]:
            price = f"${h.price_usd:.2f}" if h.price_usd else "N/A"
            name = h.name[:42] if h.name else "Unknown"
            print(f"  {h.star_rating:>3}* | {price:>10} | {name} ({h.area})")


async def test_snapshot():
    """Test snapshot (requires database)."""
    print("\n" + "=" * 60)
    print("Testing refresh_agoda_snapshot() - MAKKAH only")
    print("=" * 60)

    try:
        result = await refresh_agoda_snapshot({"city": "MAKKAH", "days_ahead": 30})
        print(f"\nResult: {result}")
    except Exception as e:
        print(f"\nSnapshot failed (expected if no DB): {e}")


async def main():
    key = os.getenv("RAPIDAPI_KEY")
    if not key:
        print("ERROR: Set RAPIDAPI_KEY environment variable first")
        print("  export RAPIDAPI_KEY=your_key_here")
        sys.exit(1)

    print(f"RAPIDAPI_KEY: {key[:8]}...{key[-4:]}")
    print()

    await test_fetch()

    # Uncomment to test DB snapshot:
    # await test_snapshot()


if __name__ == "__main__":
    asyncio.run(main())
