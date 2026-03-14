# OpenAPI Contract (MVP, Business Scope)

This contract locks API behavior for the hackathon MVP.

- Base URL (local): `http://localhost:8000`
- API prefix: `/api/v1`
- Planner engine: `Railtracks`
- Auth: `Authorization: Bearer <cognito_access_token>`
- Content type: `application/json`

## 1. Common Models

### 1.1 `ProblemResponse`

```json
{
  "code": "RECIPE_API_TIMEOUT",
  "message": "Recipe provider timed out",
  "trace_id": "5f53980b-9fd3-4fd7-bf55-6a2379ebdf56",
  "retryable": true
}
```

### 1.2 `JobEnvelope`

```json
{
  "job_id": "e9e3a2a3-6f96-4f2b-81d0-0b01993f264f",
  "status": "PENDING",
  "result": null
}
```

Status enum:
- `PENDING`
- `PROCESSING`
- `COMPLETED`
- `FAILED`

### 1.3 Core Contracts

#### `ConstraintSet`

```json
{
  "calories_target": 2100,
  "protein_g_target": 130,
  "carbs_g_target": 220,
  "fat_g_target": 70,
  "dietary_restrictions": ["vegetarian"],
  "allergies": ["peanut"],
  "budget_limit": 30,
  "max_cook_time_minutes": 20
}
```

#### `InventorySnapshot`

```json
{
  "user_id": "u_123",
  "items": [
    {
      "ingredient": "spinach",
      "quantity": "200g",
      "expires_in_days": 1
    }
  ]
}
```

#### `MealLog`

```json
{
  "user_id": "u_123",
  "meal_name": "chicken salad",
  "calories": 540,
  "protein_g": 38,
  "carbs_g": 35,
  "fat_g": 24
}
```

#### `PlanRequest`

```json
{
  "user_id": "u_123",
  "constraints": {
    "calories_target": 2100,
    "protein_g_target": 130,
    "dietary_restrictions": ["vegetarian"],
    "allergies": ["peanut"],
    "max_cook_time_minutes": 20
  },
  "inventory": {
    "user_id": "u_123",
    "items": [
      {"ingredient": "tofu", "quantity": "400g", "expires_in_days": 2}
    ]
  },
  "latest_meal_log": {
    "user_id": "u_123",
    "meal_name": "oatmeal",
    "calories": 320,
    "protein_g": 15,
    "carbs_g": 52,
    "fat_g": 8
  },
  "user_message": "Use expiring ingredients first"
}
```

#### `RecommendationBundle`

```json
{
  "recommendation_id": "rec_abc123",
  "recipe_title": "Tofu Spinach Stir-Fry",
  "steps": [
    "Press tofu and cube it",
    "Stir-fry garlic and tofu",
    "Add spinach and finish with sauce"
  ],
  "nutrition_summary": {
    "calories": 560,
    "protein_g": 36,
    "carbs_g": 42,
    "fat_g": 25
  },
  "substitutions": ["Use tempeh if tofu unavailable"],
  "spoilage_alerts": ["Spinach should be used within 24h"],
  "grocery_gap": [
    {"ingredient": "low-sodium soy sauce", "reason": "required for seasoning"}
  ]
}
```

#### `FeedbackPatch`

```json
{
  "action": "reject",
  "message": "Make it under 450 calories and dairy-free"
}
```

#### `ReplanRequest`

```json
{
  "constraints": {
    "calories_target": 450,
    "max_cook_time_minutes": 15
  },
  "user_message": "Make it vegetarian and lighter"
}
```

#### `AgentTrace`

```json
{
  "run_id": "run_789",
  "stage": "REFLECT",
  "notes": [
    "Calorie target exceeded in candidate #1",
    "Selected candidate #2 after retry"
  ]
}
```

#### Input Payloads

`FridgeScanRequest`

```json
{
  "image_url": "https://example.com/fridge.jpg",
  "detected_items": [
    {"ingredient": "spinach", "quantity": "1 bunch", "expires_in_days": 1}
  ]
}
```

`MealScanRequest`

```json
{
  "image_url": "https://example.com/meal.jpg",
  "meal_name": "tofu stir fry",
  "calories": 520,
  "protein_g": 28,
  "carbs_g": 46,
  "fat_g": 20
}
```

`ReceiptScanRequest`

```json
{
  "image_url": "https://example.com/receipt.jpg",
  "items": [
    {"ingredient": "tomato", "quantity": "4", "expires_in_days": 4}
  ]
}
```

`ChatMessageRequest`

```json
{
  "message": "Make it vegetarian and under 500 calories"
}
```

`ChatMessageResponse`

```json
{
  "event_id": 21,
  "user_id": "user-1",
  "message": "Make it vegetarian and under 500 calories"
}
```

`FeedbackResponse`

```json
{
  "event_id": 88,
  "recommendation_id": "c3b3d1f8-0ca2-45e2-bdf3-3fe2e2777f64",
  "action": "reject",
  "message": "lower calories please",
  "replanned_recommendation_id": "8fdfd79d-cf22-45c0-afde-87a1d1c53a99"
}
```

## 2. Endpoint Families

See `docs/api/endpoint-catalog.md`.

- auth/profile/goals
- inputs (fridge/meal/receipt/chat)
- planning and replanning
- planner run tracing
- recommendation output surfaces
- feedback loop

## 3. Response Status Rules

- `200`: successful read/write request.
- `202`: accepted async ingestion request (`JobEnvelope`).
- `400`: malformed request payload.
- `401/403`: authentication/authorization failure.
- `404`: entity not found.
- `422`: invalid semantic constraints.
- `500`: internal planner/runtime failure.
- `502/504`: upstream provider bridge timeout/error.

## 4. Hackathon Compatibility Rules

- Additive contract changes only.
- Keep `PlanRequest`, `RecommendationBundle`, `FeedbackPatch`, `JobEnvelope` stable.
- Unknown fields in incoming payloads should be ignored in MVP.

## 5. Replanning Rules

- `POST /planner/recommendations/{recommendation_id}/replan` accepts optional `ReplanRequest`.
- `PATCH /feedback/recommendations/{recommendation_id}` with `action=reject` triggers automatic Railtracks replanning.
