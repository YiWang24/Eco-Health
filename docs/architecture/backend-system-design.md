# Backend System Design (Hackathon Business Scope)

## 1. Architecture Style

This MVP uses a **modular monolith** backend focused on business delivery speed:

- **API framework**: FastAPI
- **Agent orchestration**: Railtracks workflow engine
- **Data**: PostgreSQL + pgvector
- **Authentication**: AWS Cognito
- **Recipe source**: TheMealDB (external API)
- **Async model**: `BackgroundTasks` for scan ingestion; synchronous planning/replanning endpoints

## 2. Business Runtime Flow

1. User authenticates and sets profile/goals.
2. User submits multimodal context (receipt/fridge/meal/chat).
3. Ingestion pipelines normalize input into pantry/intake/memory state.
4. User triggers planner endpoint.
5. Railtracks workflow runs: `Perceive -> Reason -> Retrieve -> Act -> Reflect`.
6. Backend returns actionable recommendation bundle.
7. User feedback (`accept`/`reject + instruction`) triggers replanning.

## 3. Domain Modules

- `auth`: Cognito identity mapping and user scope control.
- `profiles`: onboarding health baseline.
- `goals`: calorie/macro/restriction/budget/time targets.
- `inventory`: pantry state from receipt/fridge events.
- `intake`: meal logs and nutrition history.
- `planner`: Railtracks run orchestration and recommendation creation.
- `recipes`: candidate retrieval + normalization from TheMealDB.
- `feedback`: accept/reject loop and constraint overrides.

## 4. Data Model (Business Entities)

| Entity | Purpose | Core Fields |
|---|---|---|
| `users` | app user identity | `id`, `email`, timestamps |
| `profiles` | personal baseline context | `age`, `height_cm`, `weight_kg`, `activity_level`, preferences/allergies |
| `goals` | optimization targets | calories/macros, restrictions, budget, max cook time |
| `pantry_items` | current ingredients | `ingredient`, `quantity`, `expires_in_days`, `source` |
| `receipt_events` | purchased-food extraction history | `image_url`, `parsed_items` |
| `meal_logs` | consumed meal history | meal name + macro estimates |
| `chat_messages` | user intent deltas | natural language instruction |
| `plan_runs` | planner execution record | `status`, `mode`, `request_payload`, `trace_notes` |
| `recommendations` | actionable output | recipe title, steps, nutrition, substitutions, grocery gap |
| `feedback_events` | user decisions over plans | `action`, `message`, `recommendation_id` |

## 5. Railtracks Agent Loop Design

### 5.1 Workflow Stages

1. **Perceive**
   - read latest profile/goals/pantry/intake/chat context
   - parse latest multimodal payloads if pending
2. **Reason**
   - prioritize expiring ingredients
   - apply goal and restriction constraints
3. **Retrieve**
   - call recipe adapter for candidate set
   - enrich with normalized recipe metadata
4. **Act**
   - select best candidate and build `RecommendationBundle`
   - compute grocery gap and nutrition estimate
5. **Reflect**
   - enforce allergy/restriction checks
   - enforce macro/time/spoilage priorities
   - add substitution guidance if needed

### 5.2 Replanning Entry Points

- `POST /planner/recommendations/{id}/replan` for explicit manual replan.
- `PATCH /feedback/recommendations/{id}` with `action=reject` for conversational replan.

Both paths rebuild context and rerun the same Railtracks workflow.

## 6. Business Fallback Rules (MVP)

- Vision parse fails -> keep request accepted, use safe default extraction.
- Recipe API fails -> return fallback local recipe pattern.
- Constraint conflict -> reflection injects substitutions/alerts and returns best feasible option.
- Feedback with vague text -> parse what can be extracted and keep existing goals for remaining fields.

## 7. Hackathon Scope Boundary

In-scope business features:

1. onboarding profile + goals
2. receipt/fridge/meal/chat ingestion
3. Railtracks planner recommendation
4. recipe retrieval + metadata
5. grocery gap output
6. feedback-driven automatic replan

Out of scope in this phase:

- dashboard analytics UI
- calendar scheduling automation
- long-term optimization beyond current meal cycle
