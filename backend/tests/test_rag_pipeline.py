"""Tests for RAG pipeline with ChromaDB vector store."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.agents.rag_pipeline import RAGPipeline, get_rag_pipeline
from app.agents.rt_config import get_vector_store
from app.core.config import get_settings
from app.schemas.contracts import ConstraintSet, InventoryItem, InventorySnapshot


@pytest.fixture(autouse=True)
def isolate_rag_snapshot(tmp_path, monkeypatch):
    """Isolate vector snapshot path and caches per test to avoid cross-test bleed."""

    monkeypatch.setenv("VECTOR_STORE_MODE", "memory")
    monkeypatch.setenv("VECTOR_SNAPSHOT_PATH", str(tmp_path / "rag_snapshot.json"))
    get_settings.cache_clear()
    get_vector_store.cache_clear()
    get_rag_pipeline.cache_clear()
    yield
    get_rag_pipeline.cache_clear()
    get_vector_store.cache_clear()
    get_settings.cache_clear()


class TestRAGPipelineInit:
    """Tests for RAG pipeline initialization."""

    def test_initializes_when_railtracks_enabled(self) -> None:
        """Should initialize when Railtracks is enabled."""
        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store") as mock_vs:
                mock_vs.return_value = MagicMock()

                pipeline = RAGPipeline()
                assert pipeline._enabled
                assert pipeline._vector_store is not None

    def test_disables_when_railtracks_disabled(self) -> None:
        """Should disable when Railtracks is not enabled."""
        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=False):
            pipeline = RAGPipeline()
            assert not pipeline._enabled
            assert pipeline._vector_store is None

    def test_disables_on_vector_store_error(self) -> None:
        """Should disable gracefully when vector store fails to initialize."""
        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store") as mock_vs:
                mock_vs.side_effect = RuntimeError("ChromaDB not available")

                pipeline = RAGPipeline()
                assert not pipeline._enabled
                assert pipeline._vector_store is None


class TestRAGPipelineInitialize:
    """Tests for recipe indexing."""

    def test_initialize_returns_false_when_disabled(self) -> None:
        """Should return False when pipeline is disabled."""
        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=False):
            pipeline = RAGPipeline()
            result = pipeline.initialize()
            assert not result

    def test_initialize_indexes_recipes(self) -> None:
        """Should index provided recipes into vector store."""
        mock_vector_store = MagicMock()
        mock_vector_store.add_texts = MagicMock()

        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store", return_value=mock_vector_store):
                pipeline = RAGPipeline()

                recipes = [
                    {
                        "recipe_id": "r1",
                        "recipe_title": "Tofu Stir-Fry",
                        "ingredients": ["tofu", "spinach", "soy sauce"],
                        "instructions": "Stir-fry tofu with vegetables",
                        "category": "dinner",
                        "area": "Asian",
                        "tags": ["vegetarian"],
                    },
                    {
                        "recipe_id": "r2",
                        "recipe_title": "Chicken Soup",
                        "ingredients": ["chicken", "carrots", "celery"],
                        "instructions": "Boil chicken with vegetables",
                        "category": "soup",
                        "area": "American",
                        "tags": [],
                    },
                ]

                result = pipeline.initialize(recipes=recipes)

                assert result
                assert pipeline._indexed
                mock_vector_store.add_texts.assert_called_once()
                call_args = mock_vector_store.add_texts.call_args
                assert len(call_args.kwargs["texts"]) == 2
                assert len(call_args.kwargs["ids"]) == 2

    def test_initialize_skips_when_already_indexed(self) -> None:
        """Should skip indexing if already indexed."""
        mock_vector_store = MagicMock()

        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store", return_value=mock_vector_store):
                pipeline = RAGPipeline()
                pipeline._indexed = True

                result = pipeline.initialize()

                assert result
                mock_vector_store.add_texts.assert_not_called()

    def test_initialize_fetches_recipes_when_none_provided(self) -> None:
        """Should fetch recipes from external source when none provided."""
        mock_vector_store = MagicMock()
        mock_vector_store.add_texts = MagicMock()

        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store", return_value=mock_vector_store):
                with patch("app.agents.rag_pipeline.retrieve_recipe_candidates") as mock_fetch:
                    mock_fetch.return_value = [
                        {
                            "recipe_id": "r1",
                            "recipe_title": "Test Recipe",
                            "ingredients": ["test"],
                            "instructions": "test instructions",
                            "category": "test",
                            "area": "test",
                            "tags": [],
                        }
                    ]

                    pipeline = RAGPipeline()
                    result = pipeline.initialize(recipes=None)

                    assert result
                    assert pipeline._indexed
                    mock_fetch.assert_called()

    def test_initialize_returns_false_on_empty_recipes(self) -> None:
        """Should return False when no recipes available."""
        mock_vector_store = MagicMock()

        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store", return_value=mock_vector_store):
                with patch("app.agents.rag_pipeline.retrieve_recipe_candidates", return_value=[]):
                    pipeline = RAGPipeline()
                    result = pipeline.initialize(recipes=None)

                    assert not result

    def test_initialize_returns_false_on_fetch_error(self) -> None:
        """Should return False when recipe fetch fails."""
        mock_vector_store = MagicMock()

        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store", return_value=mock_vector_store):
                with patch(
                    "app.agents.rag_pipeline.retrieve_recipe_candidates",
                    side_effect=RuntimeError("API error")
                ):
                    pipeline = RAGPipeline()
                    result = pipeline.initialize(recipes=None)

                    assert not result


class TestRAGPipelineRecipeDocument:
    """Tests for recipe document creation."""

    def test_create_recipe_document_includes_all_fields(self) -> None:
        """Should include all recipe fields in document."""
        doc = RAGPipeline._create_recipe_document(
            recipe_title="Tofu Bowl",
            ingredients=["tofu", "spinach", "rice"],
            instructions="Cook tofu and vegetables, serve over rice",
            category="dinner",
            area="Asian",
            tags=["vegetarian", "healthy"],
        )

        assert "Recipe: Tofu Bowl" in doc
        assert "Category: dinner" in doc
        assert "Cuisine: Asian" in doc
        assert "Ingredients: tofu, spinach, rice" in doc
        assert "Tags: vegetarian, healthy" in doc
        assert "Cook tofu and vegetables" in doc

    def test_create_recipe_document_handles_missing_fields(self) -> None:
        """Should handle missing optional fields gracefully."""
        doc = RAGPipeline._create_recipe_document(
            recipe_title="Simple Recipe",
            ingredients=["salt"],
            instructions="Add salt",
            category="",
            area="",
            tags=[],
        )

        assert "Recipe: Simple Recipe" in doc
        assert "Ingredients: salt" in doc
        # Empty category/area/tags should not appear
        assert "Category:" not in doc or "Category: unknown" in doc
        assert "Cuisine:" not in doc or "Cuisine: unknown" in doc
        assert "Tags:" not in doc

    def test_create_recipe_document_truncates_long_instructions(self) -> None:
        """Should truncate long instructions."""
        long_instructions = "A" * 1000
        doc = RAGPipeline._create_recipe_document(
            recipe_title="Test",
            ingredients=["test"],
            instructions=long_instructions,
            category="",
            area="",
            tags=[],
        )

        # Instructions should be truncated to ~500 chars
        assert len(doc) < 1000


class TestRAGPipelineRetrieveContext:
    """Tests for context retrieval."""

    def test_retrieve_context_returns_empty_when_disabled(self) -> None:
        """Should return empty list when pipeline is disabled."""
        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=False):
            pipeline = RAGPipeline()
            inventory = InventorySnapshot(user_id="test", items=[])
            constraints = ConstraintSet(calories_target=500)

            results = pipeline.retrieve_context(inventory, constraints)

            assert results == []

    def test_retrieve_context_uses_vector_search_when_enabled(self) -> None:
        """Should use vector search when enabled."""
        mock_doc = MagicMock()
        mock_doc.metadata = {
            "recipe_id": "r1",
            "recipe_title": "Match Recipe",
            "category": "dinner",
            "area": "Asian",
        }
        mock_doc.score = 0.95

        mock_vector_store = MagicMock()
        mock_vector_store.similarity_search = MagicMock(return_value=[mock_doc])

        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store", return_value=mock_vector_store):
                pipeline = RAGPipeline()
                pipeline._indexed = True

                inventory = InventorySnapshot(
                    user_id="test",
                    items=[InventoryItem(ingredient="spinach", quantity="1 bunch", expires_in_days=1)]
                )
                constraints = ConstraintSet(calories_target=500)

                results = pipeline.retrieve_context(inventory, constraints, limit=5)

                assert len(results) == 1
                assert results[0]["recipe_id"] == "r1"
                assert results[0]["recipe_title"] == "Match Recipe"
                assert results[0]["source"] == "vector_search"
                mock_vector_store.similarity_search.assert_called_once()

    def test_retrieve_context_falls_back_on_vector_error(self) -> None:
        """Should fall back to keyword search on vector search error."""
        mock_vector_store = MagicMock()
        mock_vector_store.similarity_search = MagicMock(side_effect=RuntimeError("Search failed"))

        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store", return_value=mock_vector_store):
                with patch("app.agents.rag_pipeline.retrieve_recipe_candidates") as mock_retrieve:
                    mock_retrieve.return_value = [
                        {
                            "recipe_id": "r1",
                            "recipe_title": "Keyword Recipe",
                            "ingredients": ["test"],
                            "instructions": "test",
                            "category": "test",
                            "area": "test",
                            "tags": [],
                        }
                    ]

                    pipeline = RAGPipeline()
                    pipeline._indexed = True

                    inventory = InventorySnapshot(
                        user_id="test",
                        items=[InventoryItem(ingredient="spinach", quantity="1 bunch", expires_in_days=1)]
                    )
                    constraints = ConstraintSet(calories_target=500)

                    results = pipeline.retrieve_context(inventory, constraints)

                    assert len(results) == 1
                    assert results[0]["source"] == "keyword_search"

    def test_retrieve_context_builds_query_from_inventory(self) -> None:
        """Should build search query including expiring ingredients."""
        mock_vector_store = MagicMock()

        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store", return_value=mock_vector_store):
                pipeline = RAGPipeline()
                pipeline._indexed = True

                inventory = InventorySnapshot(
                    user_id="test",
                    items=[
                        InventoryItem(ingredient="spinach", quantity="1 bunch", expires_in_days=1),
                        InventoryItem(ingredient="tofu", quantity="400g", expires_in_days=5),
                    ]
                )
                constraints = ConstraintSet(calories_target=500)

                pipeline.retrieve_context(inventory, constraints)

                # Check that query includes expiring ingredients
                call_args = mock_vector_store.similarity_search.call_args
                query = call_args.kwargs["query"]
                assert "spinach" in query
                assert "expir" in query.lower()

    def test_retrieve_context_includes_dietary_restrictions_in_query(self) -> None:
        """Should include dietary restrictions in search query."""
        mock_vector_store = MagicMock()

        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store", return_value=mock_vector_store):
                pipeline = RAGPipeline()
                pipeline._indexed = True

                inventory = InventorySnapshot(user_id="test", items=[])
                constraints = ConstraintSet(
                    calories_target=500,
                    dietary_restrictions=["vegetarian", "gluten-free"],
                    max_cook_time_minutes=15,
                )

                pipeline.retrieve_context(inventory, constraints)

                call_args = mock_vector_store.similarity_search.call_args
                query = call_args.kwargs["query"]
                assert "vegetarian" in query
                assert "gluten-free" in query or "gluten free" in query
                assert "quick" in query or "easy" in query

    def test_retrieve_context_respects_limit(self) -> None:
        """Should return at most limit results."""
        mock_docs = []
        for i in range(10):
            mock_doc = MagicMock()
            mock_doc.metadata = {
                "recipe_id": f"r{i}",
                "recipe_title": f"Recipe {i}",
                "category": "test",
                "area": "test",
            }
            mock_docs.append(mock_doc)

        mock_vector_store = MagicMock()
        mock_vector_store.similarity_search = MagicMock(return_value=mock_docs)

        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
            with patch("app.agents.rag_pipeline.get_vector_store", return_value=mock_vector_store):
                pipeline = RAGPipeline()
                pipeline._indexed = True

                results = pipeline.retrieve_context(None, None, limit=3)

                assert len(results) == 3


class TestRAGPipelineBuildSearchQuery:
    """Tests for search query building."""

    def test_build_search_query_with_expiring_items(self) -> None:
        """Should prioritize expiring items in query."""
        inventory = InventorySnapshot(
            user_id="test",
            items=[
                InventoryItem(ingredient="spinach", quantity="1 bunch", expires_in_days=1),
                InventoryItem(ingredient="rice", quantity="500g", expires_in_days=30),
            ]
        )

        query = RAGPipeline._build_search_query(inventory, None)
        assert "spinach" in query
        assert "expir" in query.lower()

    def test_build_search_query_with_all_available_items(self) -> None:
        """Should include available ingredients in query."""
        inventory = InventorySnapshot(
            user_id="test",
            items=[
                InventoryItem(ingredient="tofu", quantity="400g", expires_in_days=5),
                InventoryItem(ingredient="broccoli", quantity="1 head", expires_in_days=7),
            ]
        )

        query = RAGPipeline._build_search_query(inventory, None)
        assert "tofu" in query
        assert "broccoli" in query

    def test_build_search_query_with_constraints(self) -> None:
        """Should include dietary restrictions and time constraints."""
        inventory = None
        constraints = ConstraintSet(
            dietary_restrictions=["vegan"],
            max_cook_time_minutes=20,
        )

        query = RAGPipeline._build_search_query(inventory, constraints)
        assert "vegan" in query
        assert "quick" in query or "easy" in query

    def test_build_search_query_defaults_to_healthy(self) -> None:
        """Should default to healthy recipes when no context."""
        query = RAGPipeline._build_search_query(None, None)
        assert "healthy" in query or "easy" in query


class TestRAGPipelineKeywordRetrieve:
    """Tests for keyword retrieval."""

    def test_keyword_retrieve_uses_external_service(self) -> None:
        """Should use external recipe service for keyword retrieval."""
        with patch("app.agents.rag_pipeline.retrieve_recipe_candidates") as mock_retrieve:
            mock_retrieve.return_value = [
                {
                    "recipe_id": "r1",
                    "recipe_title": "Keyword Recipe",
                    "ingredients": ["test"],
                    "instructions": "test",
                    "category": "test",
                    "area": "test",
                    "tags": [],
                }
            ]

            inventory = InventorySnapshot(
                user_id="test",
                items=[InventoryItem(ingredient="tofu", quantity="400g", expires_in_days=2)]
            )
            constraints = ConstraintSet(calories_target=500)

            pipeline = RAGPipeline()
            results = pipeline._keyword_retrieve(inventory=inventory, constraints=constraints, limit=5)

            assert len(results) == 1
            assert results[0]["recipe_id"] == "r1"
            assert results[0]["source"] == "keyword_search"
            mock_retrieve.assert_called_once()

    def test_keyword_retrieve_includes_full_recipe(self) -> None:
        """Should include full recipe data in keyword retrieval results."""
        full_recipe = {
            "recipe_id": "r1",
            "recipe_title": "Complete Recipe",
            "ingredients": ["ingredient1", "ingredient2"],
            "instructions": "Step 1. Step 2.",
            "category": "dinner",
            "area": "Italian",
            "tags": ["quick"],
        }

        with patch("app.agents.rag_pipeline.retrieve_recipe_candidates") as mock_retrieve:
            mock_retrieve.return_value = [full_recipe]

            pipeline = RAGPipeline()
            results = pipeline._keyword_retrieve(inventory=None, constraints=None, limit=5)

            assert results[0]["full_recipe"] == full_recipe


class TestRAGPipelineCached:
    """Tests for cached pipeline instance."""

    def test_get_rag_pipeline_returns_cached_instance(self) -> None:
        """Should return the same cached instance."""
        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=False):
            pipeline1 = get_rag_pipeline()
            pipeline2 = get_rag_pipeline()

            assert pipeline1 is pipeline2

    def test_get_rag_pipeline_cache_clears_on_call(self) -> None:
        """Cached pipeline can be cleared."""
        with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=False):
            pipeline1 = get_rag_pipeline()
            get_rag_pipeline.cache_clear()
            pipeline2 = get_rag_pipeline()

            # Different instances after cache clear
            assert pipeline1 is not pipeline2


class TestRAGPipelineFetchRecipes:
    """Tests for recipe fetching."""

    def test_fetch_sample_recipes_uses_search_terms(self) -> None:
        """Should use diverse search terms to fetch recipes."""
        with patch("app.agents.rag_pipeline.retrieve_recipe_candidates") as mock_retrieve:
            mock_retrieve.return_value = [
                {
                    "recipe_id": "r1",
                    "recipe_title": "Test Recipe",
                    "ingredients": ["test"],
                    "instructions": "test",
                }
            ]

            pipeline = RAGPipeline()
            recipes = pipeline._fetch_sample_recipes(limit=15)

            # Should be called at least once with different terms
            assert len(recipes) >= 1

    def test_fetch_sample_recipes_handles_errors(self) -> None:
        """Should return empty list on fetch errors."""
        with patch(
            "app.agents.rag_pipeline.retrieve_recipe_candidates",
            side_effect=RuntimeError("API error")
        ):
            pipeline = RAGPipeline()
            recipes = pipeline._fetch_sample_recipes()

            assert recipes == []

    def test_fetch_sample_recipes_respects_limit(self) -> None:
        """Should not return more than limit recipes."""
        with patch("app.agents.rag_pipeline.retrieve_recipe_candidates") as mock_retrieve:
            mock_retrieve.return_value = [
                {
                    "recipe_id": f"r{i}",
                    "recipe_title": f"Recipe {i}",
                    "ingredients": ["test"],
                    "instructions": "test",
                }
                for i in range(20)
            ]

            pipeline = RAGPipeline()
            recipes = pipeline._fetch_sample_recipes(limit=10)

            assert len(recipes) <= 10
