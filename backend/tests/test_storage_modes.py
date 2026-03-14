"""Tests for local-first storage modes and snapshot behavior."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.agents.rag_pipeline import RAGPipeline
from app.agents.rt_config import get_vector_store
from app.core.config import get_settings


def test_sqlite_snapshot_written_after_commit(client: TestClient, auth_headers) -> None:
    snapshot_path = Path(os.environ["SQLITE_SNAPSHOT_PATH"])
    if snapshot_path.exists():
        snapshot_path.unlink()

    user_id = "sqlite-snapshot-user"
    response = client.put(
        f"/api/v1/profiles/{user_id}",
        json={"age": 31, "dietary_preferences": ["vegetarian"]},
        headers=auth_headers(user_id),
    )
    assert response.status_code == 200
    assert snapshot_path.exists()
    assert snapshot_path.stat().st_size > 0


def test_vector_snapshot_persist_and_restore(tmp_path, monkeypatch) -> None:
    snapshot_path = tmp_path / "vector_snapshot.json"
    monkeypatch.setenv("VECTOR_STORE_MODE", "memory")
    monkeypatch.setenv("VECTOR_SNAPSHOT_PATH", str(snapshot_path))
    get_settings.cache_clear()
    get_vector_store.cache_clear()

    recipes = [
        {
            "recipe_id": "snapshot_r1",
            "recipe_title": "Tofu Bowl",
            "ingredients": ["tofu", "spinach"],
            "instructions": "Cook and serve.",
            "category": "dinner",
            "area": "Asian",
            "tags": ["vegetarian"],
        }
    ]

    mock_store = MagicMock()
    mock_store.add_texts = MagicMock()
    with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
        with patch("app.agents.rag_pipeline.get_vector_store", return_value=mock_store):
            pipeline = RAGPipeline()
            assert pipeline.initialize(recipes=recipes) is True
            assert snapshot_path.exists()

    restored_store = MagicMock()
    restored_store.add_texts = MagicMock()
    with patch("app.agents.rag_pipeline.is_railtracks_enabled", return_value=True):
        with patch("app.agents.rag_pipeline.get_vector_store", return_value=restored_store):
            restored_pipeline = RAGPipeline()
            assert restored_pipeline._indexed is True
            restored_store.add_texts.assert_called_once()

