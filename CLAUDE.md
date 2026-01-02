# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LABBAIK AI is a Streamlit-based AI platform for Umrah (Islamic pilgrimage) planning. It helps Indonesian Muslims plan their Umrah journey with features like AI chat, cost simulation, group matching, Travel CRM, and emergency SOS.

**Tech Stack:** Python 3.9+, Streamlit, PostgreSQL (Supabase), Groq/OpenAI LLM, ChromaDB for RAG

**Deployment:** Railway (https://labbaik-v7-production.up.railway.app/)

## Common Commands

```bash
# Run the application
streamlit run app.py

# Install dependencies
pip install -r requirements.txt

# Run with virtual environment (Windows)
venv\Scripts\activate
streamlit run app.py

# Initialize admin user
python scripts/init_admin.py

# Initialize CRM database schema
python scripts/init_crm_schema.py

# Database maintenance
python scripts/run_optimize_indexes.py
python scripts/run_cleanup_data.py
```

### Database Setup (Supabase)

Run migration in Supabase SQL Editor:
```bash
# Full schema migration
sql/supabase_migration.sql

# CRM tables only
sql/travel_crm_schema.sql
```

### Umrah Crawler (Separate FastAPI Backend)

```bash
cd umrah-crawler
uvicorn app.main:app --reload      # Run API server
python -m app.jobs                  # Background job scheduler
psql $DATABASE_URL < sql/schema.sql # Initialize schema
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
  intelligence/ # Name normalization, pricing, risk scores
  umrah/        # Hotel/transport data fetching from multiple APIs
  user/         # User management and access control
  crm/          # Travel CRM (leads, bookings, jamaah, invoices)
  subscription/ # Premium subscription handling
  partner_api/  # REST API for travel agent partners
features/       # Standalone feature modules (SOS, crowd prediction, etc.)
ui/pages/       # Streamlit page renderers
ui/components/  # Reusable UI components
data/           # Static data and knowledge bases
config/         # YAML configuration files
sql/            # Database schemas and migrations
scripts/        # Utility and initialization scripts
umrah-crawler/  # Separate FastAPI backend for data crawling
```

### Key Patterns

**Feature Flags:** Features are lazy-imported with try/except and `HAS_*` boolean flags (e.g., `HAS_CROWD_PREDICTION`). Check these flags before using features. See the imports section in `app.py` for the full list.

**Session State:** All state is managed via `st.session_state`. See `init_session_state()` in `app.py` for all keys including navigation, auth, chat, gamification, SOS, tracking, and more.

**Service Layer:**
- `services/ai/chat_service.py` - Groq/OpenAI chat with rate limiting
- `services/database/repository.py` - Database singleton with connection pooling
- `services/user/user_repository.py` - User CRUD with PostgreSQL/SQLite fallback
- `services/intelligence/` - Name normalization, currency conversion, risk scoring

**Configuration:**
- Primary: Streamlit secrets (`.streamlit/secrets.toml`) and environment variables
- Secondary: `config/settings.yaml` (env vars override YAML values)
- Use `get_settings()` from `core/config.py` to access configuration

### AI Services

The AI layer uses a provider abstraction via `AIServiceFactory`:
- `GroqChatService` - Primary LLM (llama-3.3-70b-versatile), with rate limiting
- `GLMChatService` - GLM-4 from Zhipu AI (glm-4, glm-4-plus, glm-4-flash)
- `OpenAIChatService` - Fallback (gpt-4o-mini)
- All extend `BaseChatService` from `services/ai/base.py`

Provider selection is available in the chat page sidebar. Users can switch between providers in real-time.

### Travel CRM System

CRM modules for travel agent partners in `services/crm/`:
- Lead Management - Pipeline, follow-up tracking, activity log
- Booking Tracker - Status, payments, installments
- Jamaah Database - Pilgrim data, documents, history
- Quote/Invoice Generator - Automated pricing and billing

UI pages: `ui/pages/crm_*.py`

### User Roles & Access Control

Role hierarchy (see `services/user/access_control.py`):
- GUEST (0) → FREE (1) → PREMIUM (2) → PARTNER (3) → ADMIN (4)

Use `check_page_access(page)` to verify permissions before rendering premium features.

### Database

PostgreSQL (Supabase) with connection pooling. Uses pooler URL (port 6543) for serverless compatibility.

- `services/user/user_repository.py` - User operations with PostgreSQL/SQLite fallback
- `services/database/repository.py` - General database singleton
- Auto-initializes from `DATABASE_URL` env var or Streamlit secrets

## Environment Variables

Required:
- `DATABASE_URL` - PostgreSQL connection string (use Supabase pooler URL)

AI Providers (at least one required):
- `GROQ_API_KEY` - Groq API key (llama-3.3-70b-versatile)
- `GLM_API_KEY` - Zhipu AI key (glm-4)
- `OPENAI_API_KEY` - OpenAI key (gpt-4o-mini)

Optional:
- `WAHA_API_URL`, `WAHA_SESSION` - WhatsApp integration (WAHA self-hosted)
- `AMADEUS_API_KEY`, `AMADEUS_API_SECRET` - Amadeus hotel API
- `RAPIDAPI_KEY` - RapidAPI key for Xotelo
- `ADMIN_EMAIL`, `ADMIN_PASSWORD` - Auto-create admin on startup

## Deployment (Railway)

Environment variables are set in Railway dashboard. Local changes to `secrets.toml` don't affect production.

```bash
# Link project (if Railway CLI installed)
railway link
railway variables set KEY=value
```

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
