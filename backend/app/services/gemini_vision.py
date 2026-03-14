"""OpenAI Vision integration utilities for fridge/meal/receipt parsing."""

from __future__ import annotations

import base64
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import httpx

from app.core.config import get_settings

try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except Exception:  # pragma: no cover - environment dependent
    OpenAI = None
    OPENAI_AVAILABLE = False


_DATA_URL_RE = re.compile(r"^data:(?P<mime>[^;]+);base64,(?P<data>.+)$", re.DOTALL)


def _extract_json_object(text: str) -> dict[str, Any] | None:
    text = (text or "").strip()
    if not text:
        return None
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else None
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        parsed = json.loads(match.group(0))
        return parsed if isinstance(parsed, dict) else None
    except Exception:
        return None


def _guess_mime_type(image_ref: str, default_mime: str = "image/jpeg") -> str:
    lower = image_ref.lower()
    if lower.endswith(".png"):
        return "image/png"
    if lower.endswith(".webp"):
        return "image/webp"
    if lower.endswith(".gif"):
        return "image/gif"
    return default_mime


def _load_image_bytes(image_ref: str) -> tuple[bytes, str] | None:
    """Load image from various sources and return (bytes, mime_type)."""
    image_ref = image_ref.strip()
    data_url_match = _DATA_URL_RE.match(image_ref)
    if data_url_match:
        mime = data_url_match.group("mime")
        decoded = base64.b64decode(data_url_match.group("data"))
        return decoded, mime

    if image_ref.startswith("http://") or image_ref.startswith("https://"):
        try:
            response = httpx.get(image_ref, timeout=12.0)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            mime_type = content_type.split(";", 1)[0].strip() or _guess_mime_type(image_ref)
            if not mime_type.startswith("image/"):
                mime_type = _guess_mime_type(image_ref)
            return response.content, mime_type
        except Exception:
            return None

    local = Path(image_ref).expanduser()
    if local.exists() and local.is_file():
        mime_type = _guess_mime_type(local.name)
        return local.read_bytes(), mime_type

    return None


def _encode_image_to_base64_url(image_bytes: bytes, mime_type: str) -> str:
    """Encode image bytes to base64 data URL for OpenAI API."""
    base64_data = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{base64_data}"


@lru_cache(maxsize=1)
def _get_client():
    settings = get_settings()
    if not OPENAI_AVAILABLE or not settings.openai_api_key or OpenAI is None:
        return None
    return OpenAI(api_key=settings.openai_api_key, base_url=settings.railtracks_base_url)


def _generate_structured_json(image_ref: str, prompt: str) -> dict[str, Any] | None:
    client = _get_client()
    if not client:
        return None

    image_result = _load_image_bytes(image_ref)
    if not image_result:
        return None

    image_bytes, mime_type = image_result
    base64_image = _encode_image_to_base64_url(image_bytes, mime_type)

    settings = get_settings()
    model = settings.railtracks_model or "gpt-4o"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": base64_image},
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=700,
        )
    except Exception:
        return None

    content = response.choices[0].message.content
    payload = _extract_json_object(content or "")
    return payload


def _normalize_ingredient_rows(
    rows: list[dict[str, Any]] | None,
    *,
    default_expires: int,
    limit: int,
) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in rows or []:
        ingredient = str(item.get("ingredient") or "").strip().lower()
        if not ingredient:
            continue
        quantity = item.get("quantity")
        expires = item.get("expires_in_days")
        try:
            expires_int = int(expires) if expires is not None else default_expires
        except Exception:
            expires_int = default_expires
        expires_int = max(0, min(expires_int, 30))

        normalized.append(
            {
                "ingredient": ingredient,
                "quantity": str(quantity).strip() if quantity else None,
                "expires_in_days": expires_int,
            }
        )
        if len(normalized) >= limit:
            break
    return normalized


def parse_fridge_ingredients_with_gemini(image_ref: str) -> list[dict[str, Any]]:
    """Parse fridge image into normalized ingredient items using OpenAI Vision."""

    prompt = (
        "You are extracting ingredients from a fridge image. "
        "Return strict JSON object with key 'ingredients' only. "
        "Each ingredient item must contain: ingredient (lowercase English), quantity, expires_in_days (integer 0-30). "
        "Do not include markdown."
    )
    payload = _generate_structured_json(image_ref, prompt)
    if not payload:
        return []
    return _normalize_ingredient_rows(payload.get("ingredients"), default_expires=3, limit=16)


def parse_meal_with_gemini(image_ref: str) -> dict[str, Any] | None:
    """Parse meal image and estimate nutrition fields using OpenAI Vision."""

    prompt = (
        "Identify the meal and estimate macros. "
        "Return strict JSON object with keys: meal_name, calories, protein_g, carbs_g, fat_g. "
        "All macro values must be integers."
    )
    payload = _generate_structured_json(image_ref, prompt)
    if not payload:
        return None

    meal_name = str(payload.get("meal_name") or "").strip()

    def _safe_int(value: Any, default: int) -> int:
        try:
            parsed = int(value)
            return max(0, parsed)
        except Exception:
            return default

    return {
        "meal_name": meal_name or "recognized meal",
        "calories": _safe_int(payload.get("calories"), 520),
        "protein_g": _safe_int(payload.get("protein_g"), 28),
        "carbs_g": _safe_int(payload.get("carbs_g"), 46),
        "fat_g": _safe_int(payload.get("fat_g"), 20),
    }


def parse_receipt_with_gemini(image_ref: str) -> list[dict[str, Any]]:
    """Parse receipt image into normalized purchased items using OpenAI Vision."""

    prompt = (
        "Extract grocery items from this shopping receipt image. "
        "Return strict JSON object with key 'items' only. "
        "Each item must contain: ingredient (lowercase English), quantity, expires_in_days (integer 0-30 estimated shelf life). "
        "Do not include non-food products."
    )
    payload = _generate_structured_json(image_ref, prompt)
    if not payload:
        return []
    return _normalize_ingredient_rows(payload.get("items"), default_expires=5, limit=20)
