"""SAPTCO bus schedule provider."""
from sqlalchemy import text
from app.db import get_session
from app.utils.http import get

SAPTCO_URL = "https://saptco.com.sa/"


async def fetch_saptco_schedule():
    """
    Fetch SAPTCO bus schedule.

    Note: Schedule may require scraping multiple pages.
    For now, using static known schedule.
    """
    try:
        r = await get(SAPTCO_URL, headers={"User-Agent": "umrah-crawler/1.0"})
        html_len = len(r.text)

        # Static schedule based on known SAPTCO times
        schedules = [
            {"depart": "05:00", "arrive": "10:00", "duration": 300},
            {"depart": "09:00", "arrive": "14:00", "duration": 300},
            {"depart": "13:00", "arrive": "18:00", "duration": 300},
            {"depart": "17:00", "arrive": "22:00", "duration": 300},
            {"depart": "21:00", "arrive": "02:00", "duration": 300},
        ]

        async with get_session() as session:
            for sched in schedules:
                await session.execute(text("""
                  INSERT INTO transport_schedule(mode, operator, from_city, to_city, duration_min, source_url)
                  VALUES ('BUS', 'SAPTCO', 'MAKKAH', 'MADINAH', :dur, :u)
                """), {"dur": sched["duration"], "u": SAPTCO_URL})

                # Reverse direction
                await session.execute(text("""
                  INSERT INTO transport_schedule(mode, operator, from_city, to_city, duration_min, source_url)
                  VALUES ('BUS', 'SAPTCO', 'MADINAH', 'MAKKAH', :dur, :u)
                """), {"dur": sched["duration"], "u": SAPTCO_URL})

            await session.commit()

        return {"status": "done", "source": SAPTCO_URL, "html_len": html_len}

    except Exception as e:
        return {"status": "error", "error": str(e)}
