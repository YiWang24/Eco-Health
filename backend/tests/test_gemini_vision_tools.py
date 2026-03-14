"""Tests for Gemini vision tool integration and fallback behavior."""

from app.agents import tools


def test_analyze_fridge_vision_uses_input_items_without_calling_gemini(monkeypatch) -> None:
    def _boom(_: str):  # pragma: no cover - should not be called
        raise AssertionError("Gemini parser should not be called when detected_items is provided")

    monkeypatch.setattr(tools, "parse_fridge_ingredients_with_gemini", _boom)
    payload = [{"ingredient": "apple", "quantity": "2", "expires_in_days": 5}]

    result = tools.analyze_fridge_vision("https://example.com/fridge.jpg", detected_items=payload)
    assert result["ingredients"] == payload


def test_analyze_fridge_vision_uses_gemini_when_no_detected_items(monkeypatch) -> None:
    monkeypatch.setattr(
        tools,
        "parse_fridge_ingredients_with_gemini",
        lambda _: [{"ingredient": "spinach", "quantity": "1 bunch", "expires_in_days": 1}],
    )

    result = tools.analyze_fridge_vision("https://example.com/fridge.jpg")
    assert result["ingredients"][0]["ingredient"] == "spinach"


def test_parse_receipt_items_falls_back_when_gemini_fails(monkeypatch) -> None:
    def _raise(_: str):
        raise RuntimeError("vision provider error")

    monkeypatch.setattr(tools, "parse_receipt_with_gemini", _raise)
    result = tools.parse_receipt_items("https://example.com/receipt.jpg")

    assert result["items"]
    assert result["items"][0]["ingredient"] in {"tomato", "onion"}


def test_analyze_meal_vision_uses_gemini_when_no_manual_macros(monkeypatch) -> None:
    monkeypatch.setattr(
        tools,
        "parse_meal_with_gemini",
        lambda _: {
            "meal_name": "tofu bowl",
            "calories": 430,
            "protein_g": 24,
            "carbs_g": 48,
            "fat_g": 14,
        },
    )
    result = tools.analyze_meal_vision("https://example.com/meal.jpg")

    assert result["meal_name"] == "tofu bowl"
    assert result["calories"] == 430
