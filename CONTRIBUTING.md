# Contributing

## Local Setup

```bash
cd backend
uv sync
uv run pytest tests/ -q
```

The test suite uses a shared in-memory SQLite database, while local development should use a file-backed SQLite database. No external database service is required for the default setup, which keeps local development lightweight and reduces infrastructure complexity.

## Environment Variables

The test `conftest.py` sets safe defaults for all required variables. For local development, copy or create a `.env` file with:

```
DATABASE_URL=sqlite:///./eco_health.db
RAILTRACKS_ENABLED=false
GEMINI_API_KEY=            # required when Railtracks planner or vision parsing is enabled
RAILTRACKS_MODEL=gemini-2.5-flash
GEMINI_VISION_MODEL=gemini-2.5-flash
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
RAILTRACKS_BASE_URL=https://generativelanguage.googleapis.com/v1beta
CHROMA_PERSIST_DIR=./chroma_db
CHROMA_COLLECTION_NAME=eco_health
```

See `app/core/config.py` for the full `Settings` model with defaults.

## Real-API Test Flags

Most tests run offline with mocked services. To run tests that hit real APIs:

| Flag | Workflow | Required Key |
|------|----------|-------------|
| `RUN_RAILTRACKS_E2E=1` | Railtracks + Gemini end-to-end | `GEMINI_API_KEY` |

Example:

```bash
RUN_RAILTRACKS_E2E=1 GEMINI_API_KEY=... uv run pytest tests/ -q -s
```

## Test Fixture Architecture

`tests/conftest.py` provides shared fixtures used across all test files:

| Fixture | Description |
|---------|-------------|
| `client` | FastAPI `TestClient` instance |
| `sample_inventory_snapshot` | `InventorySnapshot` with spinach (1d), tofu (2d), rice (30d) |
| `sample_constraint_set` | `ConstraintSet` with vegetarian restriction, peanut allergy, 500 cal target |
| `sample_plan_request` | `PlanRequest` combining the above fixtures |
| `mock_railtracks_settings` | `MagicMock` settings with Railtracks enabled |
| `enable_railtracks` | `monkeypatch` fixture that sets `RAILTRACKS_ENABLED=true` + test API key |

The database lifecycle fixture (`database_lifecycle`) creates tables at session start and drops them at session end. Tests use a shared in-memory SQLite database so request handlers, background jobs, and test sessions can operate on the same database state, while local development uses a file-backed SQLite database for persistence across app restarts.

## Adding a New API Endpoint

1. **Schema** — Define request/response models in `app/schemas/contracts.py`
2. **Model** — Add SQLAlchemy model in `app/models/` if persistence is needed
3. **Endpoint** — Create the route function in `app/api/v1/endpoints/`
4. **Router** — Register the new endpoint module in `app/api/v1/router.py`
5. **Tests** — Write unit and integration tests covering happy path, validation errors, and edge cases

## Adding a New Agent Tool

1. **Define** — Write the function in `app/agents/tools.py` with the `@_function_node` decorator
2. **Register** — Add the function to the `tools` list in `RailtracksPlannerWorkflow._build_agent()` (`app/agents/rt_workflow.py`)
3. **Test** — Write a unit test verifying the tool's input/output contract and edge-case handling
