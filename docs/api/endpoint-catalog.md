# Endpoint Catalog (MVP)

Base prefix: `/api/v1`

## 1. Auth / Profile / Goals

### `GET /auth/cognito/callback`
- Purpose: map Cognito callback into app bootstrap flow.
- Auth: public callback route.
- Response: callback metadata.

### `GET /auth/me`
- Purpose: resolve current authenticated user context.
- Auth: required.
- Response: `AuthContext`.

### `GET /profiles/{user_id}`
- Purpose: read user profile.
- Auth: required.

### `PUT /profiles/{user_id}`
- Purpose: create/update user profile.
- Auth: required.

### `GET /goals/{user_id}`
- Purpose: read user nutrition goals.
- Auth: required.

### `PUT /goals/{user_id}`
- Purpose: create/update user goals.
- Auth: required.

## 2. Input Ingestion

### `POST /inputs/fridge-scan`
- Purpose: submit fridge image for ingredient parsing and pantry update.
- Auth: required.
- Response: async `JobEnvelope`.

### `POST /inputs/meal-scan`
- Purpose: submit meal image for automatic nutrition logging.
- Auth: required.
- Response: async `JobEnvelope`.

### `POST /inputs/receipt-scan`
- Purpose: submit receipt image for purchased-item extraction.
- Auth: required.
- Response: async `JobEnvelope`.

### `POST /inputs/chat-message`
- Purpose: persist user natural-language planning instruction.
- Auth: required.
- Response: `ChatMessageResponse`.

### `GET /inputs/jobs/{job_id}`
- Purpose: query async ingestion status/result.
- Auth: required.
- Response: `JobEnvelope`.

## 3. Planning

### `POST /planner/recommendations`
- Purpose: execute Railtracks planner flow and create recommendation.
- Auth: required.
- Request: `PlanRequest`.
- Response: `RecommendationBundle`.

### `POST /planner/recommendations/{recommendation_id}/replan`
- Purpose: manual replan with optional overrides.
- Auth: required.
- Request: optional `ReplanRequest`.
- Response: `RecommendationBundle`.

### `GET /planner/recommendations/latest/{user_id}`
- Purpose: fetch latest recommendation for user.
- Auth: required.
- Response: `RecommendationBundle`.

### `GET /planner/runs/latest/{user_id}`
- Purpose: fetch latest planner run trace and execution mode (`railtracks` or `fallback`).
- Auth: required.
- Response: run metadata (`run_id`, `status`, `mode`, `trace_notes`, `recommendation_id`, timestamps).

## 4. Output Views

### `GET /planner/recommendations/{recommendation_id}/recipe`
- Purpose: fetch selected recipe detail and metadata.
- Auth: required.

### `GET /planner/recommendations/{recommendation_id}/nutrition`
- Purpose: fetch nutrition summary.
- Auth: required.

### `GET /planner/recommendations/{recommendation_id}/grocery-gap`
- Purpose: fetch minimal missing-ingredient list.
- Auth: required.

## 5. Feedback Loop

### `PATCH /feedback/recommendations/{recommendation_id}`
- Purpose: accept/reject recommendation with optional text instruction.
- Auth: required.
- Behavior: `reject` triggers automatic Railtracks replanning.
- Response: `FeedbackResponse` (includes `replanned_recommendation_id` on reject).
