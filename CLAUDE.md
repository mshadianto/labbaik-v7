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

# Initialize admin user (reads from secrets or prompts)
python scripts/init_admin.py
```

### Umrah Crawler (Separate FastAPI Backend)

```bash
cd umrah-crawler

# Run API server
uvicorn app.main:app --reload

# Run background job scheduler
python -m app.jobs

# Initialize database schema
psql $DATABASE_URL < sql/schema.sql
```

## Architecture

### Entry Point
- `app.py` - Main Streamlit application with lazy imports and feature flags. Handles routing, session state, and sidebar navigation.

### Directory Structure

```
core/           # Configuration, constants, exceptions, logging
services/       # Backend services (AI, database, analytics, WhatsApp)
  ai/           # LLM services (Groq, OpenAI) with provider abstraction
  database/     # PostgreSQL connection pool and repository pattern
  intelligence/ # V1.2 services: name normalization, pricing, risk scores
  umrah/        # Hotel/transport data fetching from multiple APIs
  user/         # User management and access control
  subscription/ # Premium subscription handling
  partner_api/  # REST API for travel agent partners
features/       # Standalone feature modules (SOS, crowd prediction, etc.)
ui/pages/       # Streamlit page renderers
ui/components/  # Reusable UI components
data/           # Static data and knowledge bases
config/         # YAML configuration files
umrah-crawler/  # Separate FastAPI backend for data crawling
```

### Key Patterns

**Feature Flags:** Features are lazy-imported with try/except and `HAS_*` boolean flags (e.g., `HAS_CROWD_PREDICTION`). Check these flags before using features. See the imports section in `app.py` for the full list.

**Session State:** All state is managed via `st.session_state`. See `init_session_state()` in `app.py` for all keys including navigation, auth, chat, gamification, SOS, tracking, and more.

**Service Layer:**
- `services/ai/chat_service.py` - Groq/OpenAI chat with rate limiting
- `services/database/repository.py` - Database singleton with connection pooling
- `services/intelligence/` - Name normalization, currency conversion, risk scoring, peak season detection

**Configuration:**
- Primary: Environment variables and Streamlit secrets (`.streamlit/secrets.toml`)
- Secondary: `config/settings.yaml` (env vars override YAML values)
- Use `get_settings()` from `core/config.py` to access configuration
- Dataclass-based config: `DatabaseConfig`, `AIConfig`, `UmrahDataConfig`, `AuthConfig`

### AI Services

The AI layer uses a provider abstraction via `AIServiceFactory`:
- `GroqChatService` - Primary LLM (llama-3.3-70b-versatile), with rate limiting
- `OpenAIChatService` - Fallback (gpt-4o-mini)
- Both extend `BaseChatService` from `services/ai/base.py`

### Intelligence Services (`services/intelligence/`)

V1.2 intelligence layer for data processing:

```python
from services.intelligence import (
    # Name normalization (Arabic/Latin transliteration)
    normalize_name, match_hotel_name,

    # Currency conversion (ECB rates)
    to_sar, to_idr, format_price_dual,

    # Risk scoring for hotel availability
    compute_risk_score, RiskLevel,

    # Peak season detection
    is_peak_season, season_weight,

    # Amenity extraction from descriptions
    extract_signals, get_highlight_amenities,

    # Geo clustering for deduplication
    find_clusters, deduplicate_hotels,

    # Itinerary building
    build_itinerary, compare_transport,
)
```

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

```python
from services.umrah import get_umrah_data_manager, get_cost_integration_service

manager = get_umrah_data_manager()
hotels = manager.search_hotels("Makkah", check_in="2025-03-01")
```

### User Roles & Access Control

Role hierarchy (see `services/user/access_control.py`):
- GUEST (0) → FREE (1) → PREMIUM (2) → PARTNER (3) → ADMIN (4)

Use `check_page_access(page)` to verify permissions before rendering premium features.

### Database

PostgreSQL (Neon) with connection pooling via `DatabaseConnection` singleton. The `BaseRepository` class provides CRUD operations. Auto-initializes from `DATABASE_URL` env var or Streamlit secrets.

## Environment Variables

Required:
- `DATABASE_URL` - PostgreSQL connection string
- `GROQ_API_KEY` - Groq API key for LLM

Optional:
- `OPENAI_API_KEY` - OpenAI key for embeddings/fallback
- `WAHA_API_URL`, `WAHA_SESSION` - WhatsApp integration (WAHA self-hosted)
- `AMADEUS_API_KEY`, `AMADEUS_API_SECRET` - Amadeus hotel API
- `RAPIDAPI_KEY` - RapidAPI key for Xotelo
- `ADMIN_EMAIL`, `ADMIN_PASSWORD` - Auto-create admin on startup

## Conventions

- All UI text is in Indonesian (Bahasa Indonesia)
- Pages follow the pattern: `render_*_page()` functions in `ui/pages/`
- Feature modules export `render_*_page()` and `render_*_widget()` for sidebar
- Use `track_page(page_name)` for analytics
- Gamification: Use `add_xp(amount, reason)` to award points
- New features: Add `HAS_*` flag in `app.py`, lazy-import with try/except

## Commit Message Format

Follow conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
