# OpenAPI Contract (MVP, Business Scope)

- Base URL: `http://localhost:8000`
- Prefix: `/api/v1`
- Planner engine: Railtracks orchestration with Gemini models
- Auth: strict Cognito JWT verification via `Authorization: Bearer <cognito_access_token>`
- Content-Type: `application/json`

Local demo mode (development only):
- If Cognito issuer/client-id are not configured, backend accepts `X-Demo-User` header for auth bypass.
- This mode is intended for hackathon/local integration demos only.

## 1. Common Models

### 1.1 `JobEnvelope`

```json
{
  "job_id": "e9e3a2a3-6f96-4f2b-81d0-0b01993f264f",
  "status": "PENDING",
  "result": null
}
```

`status` enum:
- `PENDING`
- `PROCESSING`
- `COMPLETED`
- `FAILED`

### 1.2 Core Contracts

`ConstraintSet`, `InventorySnapshot`, `MealLog`, `PlanRequest`, `RecommendationBundle`, `FeedbackPatch`, `AgentTrace`, `ReplanRequest` are the locked business contracts for MVP implementation.

## 2. Endpoint Families

See [endpoint-catalog.md](/Users/wy/Documents/genai/Genai/docs/api/endpoint-catalog.md).

- auth/profile/goals
- input ingestion
- chat context reads
- planning + replanning
- output views
- feedback loop

## 3. Response Status Rules

- `200`: success
- `202`: accepted async ingestion (`JobEnvelope`)
- `400`: malformed request
- `401/403`: auth failure
- `404`: resource not found
- `422`: semantic constraint validation failure
- `500`: planner/runtime failure
- `502/504`: upstream provider failure

## 4. Compatibility Rules

- Additive contract changes only.
- Keep `PlanRequest`, `RecommendationBundle`, `FeedbackPatch`, `JobEnvelope` stable.
- Ignore unknown incoming fields in MVP.

## 5. Replanning Rules

- `POST /planner/recommendations/{recommendation_id}/replan` accepts optional `ReplanRequest`.
- `PATCH /feedback/recommendations/{recommendation_id}` with `action=reject` triggers automatic replanning.
