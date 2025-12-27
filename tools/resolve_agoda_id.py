"""
Agoda City ID Resolver
======================
Resolves city IDs from Agoda web URLs to RapidAPI search-overnight format.

Usage:
    set RAPIDAPI_KEY=your_key_here
    python tools/resolve_agoda_id.py
"""

import os
import httpx

KEY = os.getenv("RAPIDAPI_KEY")
HOST = "agoda-com.p.rapidapi.com"
URL = "https://agoda-com.p.rapidapi.com/hotels/search-overnight"


def try_id(candidate_id: str):
    """Try a candidate ID format against the API."""
    headers = {
        "x-rapidapi-host": HOST,
        "x-rapidapi-key": KEY,
        "accept": "application/json",
        "user-agent": "umrah-crawler/1.0",
    }
    params = {"id": candidate_id}
    with httpx.Client(timeout=25) as c:
        r = c.get(URL, headers=headers, params=params)
        ct = (r.headers.get("content-type") or "").lower()
        ok_json = (r.status_code == 200) and ("json" in ct)
        # Show snippet to detect empty vs populated payload
        snippet = r.text[:140].replace("\n", " ")
        return r.status_code, ct, ok_json, snippet


def resolve(city_id: str):
    """Try multiple ID formats and find the one that works."""
    candidates = [
        city_id,
        f"1_{city_id}",
        f"city_{city_id}",
        f"loc_{city_id}",
    ]
    print(f"\n=== Resolve for city={city_id} ===")
    best = None
    for cand in candidates:
        code, ct, ok, snip = try_id(cand)
        print(f"id={cand:>14} -> {code} | ok_json={ok} | {ct[:30]} | {snip}")
        if ok and best is None:
            best = cand
    print(f"BEST: {best}")
    return best


if __name__ == "__main__":
    if not KEY:
        raise SystemExit("Set RAPIDAPI_KEY env first")

    # From Agoda web URLs:
    # Makkah: https://www.agoda.com/city/mecca-sa.html?city=78591
    # Madinah: https://www.agoda.com/city/medina-sa.html?city=23028
    MECCA_CITY = "78591"
    MEDINA_CITY = "23028"

    print("Agoda City ID Resolver")
    print("=" * 50)

    mecca_id = resolve(MECCA_CITY)
    medina_id = resolve(MEDINA_CITY)

    print("\n" + "=" * 50)
    print("=== Suggested config (paste to config/agoda_ids.py) ===")
    print(f'    "MAKKAH": "{mecca_id or "NEEDS_MANUAL_CHECK"}",')
    print(f'    "MADINAH": "{medina_id or "NEEDS_MANUAL_CHECK"}",')
