# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LABBAIK AI is a Streamlit-based AI platform for Umrah (Islamic pilgrimage) planning. It helps Indonesian Muslims plan their Umrah journey with features like AI chat, cost simulation, group matching, and emergency SOS.

**Tech Stack:** Python 3.9+, Streamlit, PostgreSQL (Neon), Groq/OpenAI LLM, ChromaDB for RAG

## Common Commands

```bash
# Run the application
streamlit run app.py

# Install dependencies
pip install -r requirements.txt

# Run with virtual environment (Windows)
venv\Scripts\activate
streamlit run app.py
```

## Architecture

### Entry Point
- `app.py` - Main Streamlit application with lazy imports and feature flags. Handles routing, session state, and sidebar navigation.

### Directory Structure

```
core/           # Configuration, constants, exceptions, logging
services/       # Backend services (AI, database, analytics, WhatsApp)
features/       # Standalone feature modules (SOS, crowd prediction, etc.)
ui/pages/       # Streamlit page renderers
ui/components/  # Reusable UI components
data/           # Static data and knowledge bases
config/         # YAML configuration files
```

### Key Patterns

**Feature Flags:** Features are lazy-imported with try/except and `HAS_*` boolean flags (e.g., `HAS_CROWD_PREDICTION`). Check these flags before using features.

**Session State:** All state is managed via `st.session_state`. See `init_session_state()` in `app.py` for all keys.

**Service Layer:**
- `services/ai/chat_service.py` - Groq/OpenAI chat with fallback via `UnifiedChatService`
- `services/database/repository.py` - Database singleton with connection pooling and base repository pattern
- `services/analytics/` - Page tracking and visitor analytics

**Configuration:**
- Primary: Environment variables and Streamlit secrets (`.streamlit/secrets.toml`)
- Secondary: `config/settings.yaml` (YAML values are overridden by env vars)
- Use `get_settings()` from `core/config.py` to access configuration

### AI Services

The AI layer uses a provider abstraction:
- `GroqChatService` - Primary LLM (llama-3.3-70b-versatile)
- `OpenAIChatService` - Fallback (gpt-4o-mini)
- Services are registered via `AIServiceFactory`

### Umrah Data Services (`services/umrah/`)

Hybrid data fetching for hotels, transport, and live pricing:

**Data Sources (Priority Order):**
1. Amadeus Hotel API (free tier)
2. Xotelo API (RapidAPI)
3. MakCorps Free API
4. Demo data (fallback)

**Key Classes:**
- `HybridUmrahDataManager` - Main orchestrator, combines all data sources
- `CostIntegrationService` - Bridges data fetcher with cost simulator
- `LocationService` - Geocoding via Nominatim, routing via OSRM
- `TransportService` - Haramain Railway & SAPTCO bus schedules

**Usage:**
```python
from services.umrah import get_umrah_data_manager, get_cost_integration_service

# Search hotels
manager = get_umrah_data_manager()
hotels = manager.search_hotels("Makkah", check_in="2025-03-01")

# Get live prices for cost simulation
service = get_cost_integration_service()
price = service.get_hotel_price("Makkah", star_rating=4)
```

### Umrah Crawler (`umrah-crawler/`)

Separate FastAPI backend for data crawling with job queue:

```bash
# Run API server
cd umrah-crawler && uvicorn app.main:app --reload

# Run job scheduler
python -m app.jobs
```

**API Endpoints:**
- `GET /search_hotels` - Search hotels by city/dates
- `GET /hotel/{id}/offers` - Get offers for a hotel
- `GET /transport/makkah-madinah` - Transport options

**Database Tables:** `hotels_master`, `offers`, `provider_hotel_map`, `transport_schedule`, `crawl_jobs`

### Database

PostgreSQL with connection pooling via `DatabaseConnection` singleton. The `BaseRepository` class provides CRUD operations. Key repositories:
- `UserRepository`
- `ChatRepository`
- `BookingRepository`

## Environment Variables

Required:
- `DATABASE_URL` - PostgreSQL connection string
- `GROQ_API_KEY` - Groq API key for LLM

Optional:
- `OPENAI_API_KEY` - OpenAI key for embeddings/fallback
- `WAHA_API_URL`, `WAHA_SESSION` - WhatsApp integration
- `AMADEUS_API_KEY`, `AMADEUS_API_SECRET` - Amadeus hotel API
- `RAPIDAPI_KEY` - RapidAPI key for Xotelo and other services

## Conventions

- All UI text is in Indonesian (Bahasa Indonesia)
- Pages follow the pattern: `render_*_page()` functions
- Feature modules export `render_*_page()` and `render_*_widget()` for sidebar widgets
- Use `track_page(page_name)` for analytics
- Gamification: Use `add_xp(amount, reason)` to award points

## Commit Message Format

Follow conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
