# Umrah Crawler

FastAPI backend service for crawling hotel and transport data for Umrah planning.

## Features

- **Multi-source hotel data**: Amadeus, Xotelo, MakCorps APIs
- **Transport schedules**: Haramain Railway, SAPTCO Bus
- **Job queue system**: Background crawling with APScheduler
- **PostgreSQL storage**: Hotels, offers, transport schedules
- **Rate limiting**: Respect API limits

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your credentials

# Initialize database
psql $DATABASE_URL < sql/schema.sql

# Run API server
uvicorn app.main:app --reload

# Run job scheduler (separate terminal)
python -m app.jobs
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /search_hotels` | Search hotels by city/dates |
| `GET /hotel/{id}/offers` | Get offers for a hotel |
| `GET /availability/calendar` | Get availability calendar |
| `GET /transport/makkah-madinah` | Get transport options |

## Directory Structure

```
umrah-crawler/
├── app/
│   ├── main.py          # FastAPI app
│   ├── db.py            # Database connection
│   ├── crud.py          # Database queries
│   ├── jobs.py          # Background job scheduler
│   ├── settings.py      # Configuration
│   ├── providers/       # Data source integrations
│   │   ├── amadeus.py
│   │   ├── xotelo.py
│   │   ├── makcorps.py
│   │   ├── haramain.py
│   │   └── saptco.py
│   └── utils/           # Utilities
│       ├── http.py
│       ├── rate_limiter.py
│       └── normalize.py
├── sql/
│   └── schema.sql       # Database schema
├── requirements.txt
└── .env.example
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `AMADEUS_CLIENT_ID` | Amadeus API client ID |
| `AMADEUS_CLIENT_SECRET` | Amadeus API secret |
| `XOTELO_RAPIDAPI_KEY` | RapidAPI key for Xotelo |
| `MAKCORPS_API_KEY` | MakCorps API key (optional) |

## Data Flow

1. **Job Scheduler** enqueues crawl jobs (prices, transport)
2. **Providers** fetch data from APIs
3. **Hotels Master** table stores normalized hotel info
4. **Offers** table stores price snapshots
5. **API** serves aggregated data to frontend
