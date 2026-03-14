"""Railtracks configuration for LLM and vector store initialization."""

from __future__ import annotations

__all__ = [
    "get_llm",
    "get_vector_store",
    "is_railtracks_enabled",
    "rt",
    "RAILTRACKS_AVAILABLE",
]

from functools import lru_cache
from pathlib import Path

from app.core.config import Settings, get_settings

try:
    import railtracks as rt
    from railtracks.vector_stores.chroma import ChromaVectorStore
    from railtracks.rag.embedding_service import EmbeddingService
    RAILTRACKS_AVAILABLE = True
except Exception:  # pragma: no cover - environment dependent
    RAILTRACKS_AVAILABLE = False
    rt = None  # type: ignore
    ChromaVectorStore = None  # type: ignore
    EmbeddingService = None  # type: ignore

_VECTOR_BACKEND_SIGNATURE: tuple[str, str | None] | None = None


def _resolve_vector_store_path(settings: Settings) -> str | None:
    """Resolve Chroma backend path according to configured runtime mode."""

    if settings.vector_store_mode == "memory":
        return None

    persist_path = Path(settings.chroma_persist_dir).expanduser()
    persist_path.mkdir(parents=True, exist_ok=True)
    return str(persist_path)


def _sync_chroma_backend_signature(mode: str, path: str | None) -> None:
    """Reset shared Chroma client if backend mode/path changed across runs."""

    global _VECTOR_BACKEND_SIGNATURE

    next_signature = (mode, path)
    if (
        _VECTOR_BACKEND_SIGNATURE is not None
        and _VECTOR_BACKEND_SIGNATURE != next_signature
        and ChromaVectorStore is not None
        and hasattr(ChromaVectorStore, "_chroma")
    ):
        delattr(ChromaVectorStore, "_chroma")
    _VECTOR_BACKEND_SIGNATURE = next_signature


@lru_cache(maxsize=1)
def get_llm():
    """Initialize and return cached OpenAI LLM instance.

    The LLM is configured using the HuggingFace endpoint compatible with
    OpenAI API format. Uses settings from environment variables.

    Returns:
        OpenAILLM: Configured LLM instance for inference.

    Raises:
        RuntimeError: If Railtracks is not installed or API key is missing.
    """
    if not RAILTRACKS_AVAILABLE:
        raise RuntimeError(
            "Railtracks is not installed. Install with: pip install 'railtracks[chroma]>=0.1.0'"
        )

    settings: Settings = get_settings()

    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is required")

    return rt.llm.OpenAILLM(
        model=settings.railtracks_model,
        api_key=settings.openai_api_key,
        base_url=settings.railtracks_base_url,
    )


@lru_cache(maxsize=1)
def get_vector_store() -> ChromaVectorStore:
    """Initialize and return cached ChromaDB vector store instance.

    Creates a persistent ChromaDB collection for RAG operations.
    The collection is stored in the configured persist directory.

    Returns:
        ChromaVectorStore: Configured vector store for semantic search.

    Raises:
        RuntimeError: If Railtracks/ChromaDB is not installed.
    """
    if not RAILTRACKS_AVAILABLE:
        raise RuntimeError(
            "Railtracks is not installed. Install with: pip install 'railtracks[chroma]>=0.1.0'"
        )

    settings: Settings = get_settings()

    path = _resolve_vector_store_path(settings)
    _sync_chroma_backend_signature(settings.vector_store_mode, path)

    embedding_service = EmbeddingService()

    return ChromaVectorStore(
        collection_name=settings.chroma_collection_name,
        embedding_function=embedding_service.embed,
        path=path,
    )


def is_railtracks_enabled() -> bool:
    """Check if Railtracks is properly configured and available.

    Returns:
        bool: True if Railtracks can be used, False otherwise.
    """
    settings: Settings = get_settings()
    return bool(
        RAILTRACKS_AVAILABLE
        and settings.railtracks_enabled
        and settings.openai_api_key
    )
