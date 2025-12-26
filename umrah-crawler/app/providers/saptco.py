# app/providers/saptco.py
from sqlalchemy import text
from app.db import get_session
from app.utils.http import get

SAPTCO_URL = "https://saptco.com.sa/"  # base; jadwal biasanya via halaman trip schedule


async def fetch_saptco_schedule():
    r = await get(SAPTCO_URL, headers={"User-Agent": "umrah-crawler/1.0"})
    async with get_session() as session:
        await session.execute(text("""
          INSERT INTO transport_schedule(mode, operator, from_city, to_city, source_url)
          VALUES ('BUS','SAPTCO','MAKKAH','MADINAH',:u)
        """), {"u": SAPTCO_URL})
        await session.commit()
    return {"ok": True, "html_len": len(r.text)}
