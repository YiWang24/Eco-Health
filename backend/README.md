# Backend (FastAPI + Google ADK)

This backend hosts the MVP APIs for **Eco-Health Agentic Dietitian**.

## Current Status

- API scaffolding is in place for hackathon MVP contracts.
- Endpoint handlers are placeholders where business logic is not yet implemented.
- Core docs are in `/docs` and should be treated as the source of truth.

## Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Environment

Copy and edit:

```bash
cp .env.example .env
```

Required contract (MVP):

- `GEMINI_API_KEY`
- `COGNITO_REGION`
- `COGNITO_USER_POOL_ID`
- `COGNITO_CLIENT_ID`
- `COGNITO_ISSUER`
- `RECIPE_API_BASE_URL`
- `RECIPE_API_KEY`
- `DATABASE_URL`
- `REDIS_URL` (optional for this phase)
