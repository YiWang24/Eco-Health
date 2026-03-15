"""Shared pytest fixtures for backend tests."""

from __future__ import annotations

import json
import os
import sys
import time
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient
from jose import jwt
from jose.utils import base64url_encode

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def _base64_int(value: int) -> str:
    raw = value.to_bytes((value.bit_length() + 7) // 8, "big")
    return base64url_encode(raw).decode("utf-8")


TEST_KID = "test-kid"
TEST_ISSUER = "https://local-cognito.example.com"
TEST_CLIENT_ID = "local-client-id"

_TEST_PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
TEST_PRIVATE_KEY_PEM = _TEST_PRIVATE_KEY.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
).decode("utf-8")

public_numbers = _TEST_PRIVATE_KEY.public_key().public_numbers()
TEST_JWKS = {
    "keys": [
        {
            "kty": "RSA",
            "kid": TEST_KID,
            "use": "sig",
            "alg": "RS256",
            "n": _base64_int(public_numbers.n),
            "e": _base64_int(public_numbers.e),
        }
    ]
}

os.environ["DATABASE_URL"] = ""
os.environ["SQLITE_MODE"] = "memory"
os.environ["SQLITE_SNAPSHOT_PATH"] = str(BACKEND_ROOT / "tests" / ".tmp" / "snapshot.sqlite3")
os.environ["SQLITE_AUTO_SNAPSHOT"] = "true"
os.environ["ENV"] = "development"
os.environ["RAILTRACKS_ENABLED"] = "false"
os.environ["GEMINI_API_KEY"] = ""
os.environ["RECIPE_API_BASE_URL"] = ""
os.environ["RAILTRACKS_BASE_URL"] = "https://generativelanguage.googleapis.com/v1beta"
os.environ["RAILTRACKS_MODEL"] = "gemini-2.5-flash"
os.environ["VECTOR_STORE_MODE"] = "memory"
os.environ["CHROMA_PERSIST_DIR"] = "./test_chroma_db"
os.environ["CHROMA_COLLECTION_NAME"] = "test_eco_health"
os.environ["VECTOR_SNAPSHOT_PATH"] = str(BACKEND_ROOT / "tests" / ".tmp" / "vector_snapshot.json")
os.environ["COGNITO_ISSUER"] = TEST_ISSUER
os.environ["COGNITO_CLIENT_ID"] = TEST_CLIENT_ID
os.environ["COGNITO_JWKS_JSON"] = json.dumps(TEST_JWKS)

from app.agents.io_contracts import AgentPlanInputV1, AgentPlanOutputV1
from app.core.database import Base, engine
from app.main import app
from app.schemas.contracts import (
    DecisionBlock,
    ExecutionPlanBlock,
    GroceryPlanBlock,
    ConstraintSet,
    GroceryItem,
    InventoryItem,
    InventorySnapshot,
    MealPlanBlock,
    MemoryUpdatesBlock,
    NutritionSummary,
    PlanRequest,
    RecommendationBundle,
    ReflectionBlock,
)


def issue_test_token(user_id: str, email: str | None = None) -> str:
    """Issue a short-lived RS256 token signed by local test private key."""

    now = int(time.time())
    claims = {
        "sub": user_id,
        "email": email or f"{user_id}@example.com",
        "iss": TEST_ISSUER,
        "aud": TEST_CLIENT_ID,
        "iat": now,
        "exp": now + 3600,
    }
    return jwt.encode(
        claims=claims,
        key=TEST_PRIVATE_KEY_PEM,
        algorithm="RS256",
        headers={"kid": TEST_KID},
    )


@pytest.fixture(scope="session", autouse=True)
def database_lifecycle() -> Generator[None, None, None]:
    snapshot = Path(os.environ["SQLITE_SNAPSHOT_PATH"])
    if snapshot.exists():
        snapshot.unlink()
    snapshot.parent.mkdir(parents=True, exist_ok=True)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers():
    """Return Authorization header builder using strict Cognito-compatible JWT."""

    def _build(user_id: str, email: str | None = None) -> dict[str, str]:
        return {"Authorization": f"Bearer {issue_test_token(user_id, email)}"}

    return _build


@pytest.fixture(autouse=True)
def stub_planner_workflow(monkeypatch):
    """Use deterministic planner stub for offline functional tests."""

    class _StubWorkflow:
        async def recommend_async(self, request: AgentPlanInputV1) -> AgentPlanOutputV1:
            plan_request = request.to_plan_request()
            constraints = plan_request.constraints
            grocery = [
                GroceryItem(ingredient="peanut", reason="sauce"),
                GroceryItem(ingredient="chicken breast", reason="protein"),
                GroceryItem(ingredient="onion", reason="aroma"),
            ]
            violations: list[dict] = []

            if constraints.allergies:
                allergy_set = {item.lower() for item in constraints.allergies}
                next_grocery = []
                for item in grocery:
                    if item.ingredient.lower() in allergy_set:
                        violations.append({"type": "allergen_block", "ingredient": item.ingredient.lower()})
                        continue
                    next_grocery.append(item)
                grocery = next_grocery

            restrictions = {item.lower() for item in constraints.dietary_restrictions}
            if "vegetarian" in restrictions or "vegan" in restrictions:
                grocery = [item for item in grocery if "chicken" not in item.ingredient.lower()]
                violations.append({"type": "diet_restriction_conflict"})

            substitutions = []
            if constraints.calories_target is not None and constraints.calories_target < 650:
                substitutions.append("Use a lighter sauce to reduce calories")
            if constraints.protein_g_target is not None and constraints.protein_g_target > 22:
                substitutions.append("Add tofu, beans, or Greek yogurt to increase protein")
            if "vegetarian" in restrictions or "vegan" in restrictions:
                substitutions.append("Swap animal protein for tofu, lentils, or tempeh")
            if not substitutions:
                substitutions.append("Keep current recipe and portion size")

            bundle = RecommendationBundle(
                recommendation_id="stub-rec-id",
                decision=DecisionBlock(
                    recipe_title="Chicken Test Bowl",
                    rationale="Stubbed planner output for deterministic tests",
                    confidence=0.81,
                ),
                meal_plan=MealPlanBlock(
                    steps=["Prepare ingredients", "Cook quickly", "Serve"],
                    nutrition_summary=NutritionSummary(
                        calories=650,
                        protein_g=22,
                        carbs_g=72,
                        fat_g=28,
                    ),
                    substitutions=substitutions,
                    spoilage_alerts=["Prioritize spinach within 48h"] if plan_request.inventory else [],
                ),
                grocery_plan=GroceryPlanBlock(
                    missing_ingredients=grocery,
                    optimized_grocery_list=grocery,
                    estimated_gap_cost=float(len(grocery) * 2.0),
                ),
                execution_plan=ExecutionPlanBlock(),
                reflection=ReflectionBlock(
                    status="adjusted_with_violations" if violations else "ok",
                    attempts=1,
                    violations=violations,
                    adjustments=["Stub adjustment applied"] if violations else ["No adjustment needed"],
                ),
                memory_updates=MemoryUpdatesBlock(
                    short_term_updates=["stub_context_loaded"],
                    long_term_metric_deltas={},
                ),
            )
            trace = ["workflow:railtracks-agentic", "stage:PERCEIVE", "stage:FINALIZE"]
            if constraints.calories_target is not None and constraints.calories_target < 650:
                trace.append("reflection:calorie_overflow")
            if constraints.protein_g_target is not None and constraints.protein_g_target > 22:
                trace.append("reflection:protein_under_target")
            if constraints.allergies:
                trace.append("violation:allergen_block")
            if "vegetarian" in restrictions or "vegan" in restrictions:
                trace.append("violation:diet_restriction_conflict")
            return AgentPlanOutputV1.from_recommendation_bundle(
                bundle,
                trace_notes=trace,
                mode="railtracks-agentic",
            )

    monkeypatch.setattr(
        "app.services.planner_execution.get_railtracks_workflow",
        lambda: _StubWorkflow(),
    )


@pytest.fixture
def sample_inventory_snapshot() -> InventorySnapshot:
    """Sample inventory snapshot for testing."""
    return InventorySnapshot(
        user_id="test-user",
        items=[
            InventoryItem(ingredient="spinach", quantity="1 bunch", expires_in_days=1),
            InventoryItem(ingredient="tofu", quantity="400g", expires_in_days=2),
            InventoryItem(ingredient="rice", quantity="500g", expires_in_days=30),
        ],
    )


@pytest.fixture
def sample_constraint_set() -> ConstraintSet:
    """Sample constraint set for testing."""
    return ConstraintSet(
        calories_target=500,
        protein_g_target=25,
        carbs_g_target=50,
        fat_g_target=20,
        dietary_restrictions=["vegetarian"],
        allergies=["peanut"],
        max_cook_time_minutes=20,
    )


@pytest.fixture
def sample_plan_request(
    sample_inventory_snapshot,
    sample_constraint_set,
) -> PlanRequest:
    """Sample plan request for testing."""
    return PlanRequest(
        user_id="test-user",
        constraints=sample_constraint_set,
        inventory=sample_inventory_snapshot,
        user_message="Use expiring ingredients first",
    )


@pytest.fixture
def mock_railtracks_settings():
    """Mock settings for Railtracks-enabled tests."""
    settings = MagicMock()
    settings.railtracks_enabled = True
    settings.gemini_api_key = "test-key-12345"
    settings.gemini_model = "gemini-2.5-flash"
    settings.railtracks_model = "gemini-2.5-flash"
    settings.railtracks_base_url = "https://generativelanguage.googleapis.com/v1beta"
    settings.vector_store_mode = "memory"
    settings.chroma_persist_dir = "./test_chroma_db"
    settings.chroma_collection_name = "test_eco_health"
    return settings


@pytest.fixture
def mock_railtracks_llm():
    """Mock Railtracks LLM for testing."""
    llm = MagicMock()
    llm.model = "gemini-2.5-flash"
    llm.api_key = "test-key"
    return llm


@pytest.fixture
def mock_vector_store():
    """Mock ChromaDB vector store for testing."""
    store = MagicMock()
    store.add_texts = MagicMock()
    store.similarity_search = MagicMock(return_value=[])
    store.delete = MagicMock()
    return store


@pytest.fixture
def mock_recipe_candidates():
    """Mock recipe candidates for testing."""
    return [
        {
            "recipe_id": "meal_1",
            "recipe_title": "Tofu Spinach Stir-Fry",
            "ingredients": ["tofu", "spinach", "soy sauce", "ginger"],
            "instructions": "Press tofu and stir-fry with vegetables.",
            "steps": ["Press tofu", "Chop vegetables", "Stir-fry together"],
            "category": "dinner",
            "area": "Asian",
            "tags": ["vegetarian", "healthy"],
        },
        {
            "recipe_id": "meal_2",
            "recipe_title": "Vegetable Rice Bowl",
            "ingredients": ["rice", "broccoli", "carrots", "soy sauce"],
            "instructions": "Cook rice and vegetables, combine in bowl.",
            "steps": ["Cook rice", "Steam vegetables", "Combine and serve"],
            "category": "dinner",
            "area": "Asian",
            "tags": ["vegetarian"],
        },
    ]


@pytest.fixture
def enable_railtracks(monkeypatch):
    """Enable Railtracks for a test."""
    monkeypatch.setenv("RAILTRACKS_ENABLED", "true")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-for-testing")
    from app.agents.rt_config import get_vector_store
    from app.core.config import get_settings

    get_settings.cache_clear()
    get_vector_store.cache_clear()
    yield
    get_vector_store.cache_clear()
    get_settings.cache_clear()
