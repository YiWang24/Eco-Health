# Endpoint Catalog (Hackathon MVP, Agentic V1)

Base prefix: `/api/v1`

## 1. Auth

- `GET /auth/cognito/callback`
- `GET /auth/me`

All protected routes require strict JWT verification.

## 2. Onboarding

- `GET /profiles/{user_id}`
- `PUT /profiles/{user_id}`
- `GET /goals/{user_id}`
- `PUT /goals/{user_id}`

Only self-scope (`{user_id} == token.sub`) is allowed.

## 3. Inputs

- `POST /inputs/fridge-scan`
- `POST /inputs/meal-scan`
- `POST /inputs/receipt-scan`
- `GET /inputs/jobs/{job_id}`
- `GET /inputs/pantry`
- `DELETE /inputs/pantry/{item_id}`
- `GET /inputs/spoilage-alerts`
- `POST /inputs/chat-message?auto_replan=<bool>`
- `GET /inputs/chat-messages/latest?limit=<n>`

`auto_replan=true` returns `ChatMessageResponse.recommendation` using `RecommendationBundle`.

## 4. Planner

- `POST /planner/recommendations`
- `GET /planner/recommendations/{recommendation_id}`
- `GET /planner/recommendations/history/{user_id}?limit=<n>`
- `POST /planner/recommendations/{recommendation_id}/replan`
- `GET /planner/recommendations/latest/{user_id}`
- `GET /planner/runs/latest/{user_id}`
- `GET /planner/recommendations/{recommendation_id}/recipe`
- `GET /planner/recommendations/{recommendation_id}/nutrition`
- `GET /planner/recommendations/{recommendation_id}/grocery-gap`

### Replan Behavior

- Inherits constraints from the original recommendation run snapshot.
- Merges replan overrides and parsed natural-language constraints.
- Preserves allergy/restriction continuity across multi-step replans.

## 5. Feedback

- `PATCH /feedback/recommendations/{recommendation_id}`

`reject` triggers automatic replan and returns `replanned_recommendation_id`.

## 6. Core Contracts

### `PlanRequest`

- `user_id`
- `constraints`
- `inventory` (optional)
- `latest_meal_log` (optional)
- `user_message` (optional)
- `prior_recipe_hint` (optional)

### `RecommendationBundle`

- `recommendation_id`
- `decision`
  - `recipe_title`
  - `rationale`
  - `confidence`
- `meal_plan`
  - `steps`
  - `nutrition_summary`
  - `substitutions`
  - `spoilage_alerts`
- `grocery_plan`
  - `missing_ingredients`
  - `optimized_grocery_list`
  - `estimated_gap_cost`
- `execution_plan`
  - `calendar_blocks`
  - `cooking_dag_tasks`
  - `proactive_prep_windows`
- `reflection`
  - `status`
  - `attempts`
  - `violations`
  - `adjustments`
- `memory_updates`
  - `short_term_updates`
  - `long_term_metric_deltas`
