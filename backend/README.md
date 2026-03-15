# Backend (FastAPI + Railtracks)

Backend MVP for **Eco-Health Agentic Dietitian**.

## Status

- Gemini-first **agentic stage workflow** (via Railtracks orchestration):
  `Perceive -> Prioritize -> Retrieve -> Query Recipe -> Formulate -> Reflect -> Finalize Execution Plan`.
- Core planner + ingestion + feedback replan loop implemented with strict JWT auth.
- Cognito auth APIs available: email sign-up, email confirmation, login, token refresh.
- Development demo bypass is opt-in only (`AUTH_BYPASS_ENABLED=true` + `X-Demo-User`).
- Default persistence uses memory-first SQLite with file snapshot backup (restore on startup, flush on every write commit).
- Vector store defaults to memory mode with local snapshot file for bootstrap.
- Execution tools are local and persisted:
  - calendar blocks
  - cooking DAG tasks
  - proactive prep windows
- Long-term memory metrics are persisted per user:
  - favorite recipes
  - purchase patterns
  - cumulative money saved
  - food-waste reduction metrics
  - sustainability impact metrics
- API contracts and design docs are under `/docs`.

## Run

```bash
cd backend
uv sync
cp .env.example .env
uv run uvicorn app.main:app --reload --port 8000
```

By default, the backend starts with memory-first local storage and snapshot files, so no PostgreSQL, pgvector, Redis, or separate database service is required for local development.

## Test

```bash
uv run pytest -q
```

Current baseline: `85 passed`.

## Planner Response (V1)

`POST /api/v1/planner/recommendations`, `GET /api/v1/planner/recommendations/{recommendation_id}`,
`GET /api/v1/planner/recommendations/history/{user_id}` and `/replan` now return `RecommendationBundle`:

- `recommendation_id`
- `decision` (`recipe_title`, `rationale`, `confidence`)
- `meal_plan` (`steps`, `nutrition_summary`, `substitutions`, `spoilage_alerts`)
- `grocery_plan` (`missing_ingredients`, `optimized_grocery_list`, `estimated_gap_cost`)
- `execution_plan` (`calendar_blocks`, `cooking_dag_tasks`, `proactive_prep_windows`)
- `reflection` (`status`, `attempts`, `violations`, `adjustments`)
- `memory_updates` (`short_term_updates`, `long_term_metric_deltas`)

## Environment

Required:

- `GEMINI_API_KEY`
- `CORS_ALLOWED_ORIGINS` (comma separated, e.g. `https://your-frontend.vercel.app,http://localhost:3000`)
- `RAILTRACKS_ENABLED`
- `GEMINI_MODEL` (or `RAILTRACKS_MODEL`)
- `GEMINI_VISION_MODEL`
- `GEMINI_EMBEDDING_MODEL`
- `VECTOR_STORE_MODE`
- `CHROMA_PERSIST_DIR`
- `CHROMA_COLLECTION_NAME`
- `VECTOR_SNAPSHOT_PATH`
- `COGNITO_REGION`
- `COGNITO_USER_POOL_ID`
- `COGNITO_CLIENT_ID`
- `COGNITO_ISSUER`
- `RECIPE_API_BASE_URL`
- `RECIPE_API_KEY`

Optional:

- `DATABASE_URL`  
  Leave empty to use `SQLITE_MODE` defaults. Set explicitly only when you need a fixed custom SQLAlchemy URL.
- `SQLITE_MODE` (`memory` or `file`)
- `SQLITE_SNAPSHOT_PATH`
- `SQLITE_AUTO_SNAPSHOT`
- `COGNITO_JWKS_JSON` / `COGNITO_JWKS_PATH`  
  Useful for strict offline JWT verification in local/dev tests.
- `AUTH_BYPASS_ENABLED`  
  If `true` in development, bypasses Cognito and reads `X-Demo-User` from request headers.
- `REDIS_URL`

## Recipe Provider

TheMealDB free endpoints used:

1. `filter.php?i=<ingredient>`
2. `lookup.php?i=<idMeal>`
3. `search.php?s=<query>`
4. `random.php`
