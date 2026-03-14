# Backend System Design (Hackathon Business Scope)

## 1. Architecture Style

Modular monolith focused on fast business delivery and minimal setup complexity:

- API: FastAPI
- Agent runtime: Railtracks
- Data: SQLite memory-first database + file snapshots
- Auth: AWS Cognito
- Recipe provider: TheMealDB
- Async jobs: FastAPI `BackgroundTasks`

### Why memory-first SQLite + snapshots

For the hackathon MVP, the backend should avoid introducing extra infrastructure components unless they are essential to the user-facing experience.

Using memory-first SQLite with file snapshots gives us:

- no separate database service to provision
- lower local setup complexity
- easier demo startup
- fewer moving parts during judging
- enough relational capability for current MVP entities and flows
- file persistence across restarts (startup restore + write-time snapshot flush)

This means the backend can run as a single lightweight application process while still supporting the full onboarding → input → planning → feedback → replan loop.

## 2. Runtime Flow

1. User completes onboarding (profile + goals).
2. User submits receipt/fridge/meal/chat context.
3. Ingestion jobs update pantry + meal logs in the memory SQLite runtime (auto-snapshotted to file).
4. Planner request is created.
5. Railtracks workflow runs `Perceive -> Prioritize -> Retrieve -> Query Recipe -> Formulate -> Reflect -> Finalize Execution Plan`.
6. Recommendation V1 bundle is returned and persisted in the local SQLite database.
7. Feedback reject triggers replan with merged constraints.

## 3. Domain Modules

- `auth`
- `profiles`
- `goals`
- `inventory`
- `intake`
- `planner`
- `recipes`
- `feedback`

## 4. Data Model

Although the database engine is simplified, the business entities remain the same.

| Entity | Purpose | Core Fields |
|---|---|---|
| `users` | app identity | `id`, `email`, timestamps |
| `profiles` | health baseline | age/height/weight/activity/preferences/allergies |
| `goals` | nutrition constraints | calories/macros/restrictions/budget/time |
| `pantry_items` | current stock | ingredient/quantity/expires/source |
| `receipt_events` | parsed receipts | image_url/parsed_items |
| `meal_logs` | consumed meals | meal_name/macros |
| `chat_messages` | natural-language intent | message |
| `plan_runs` | planner execution | status/mode/request/response/notes |
| `recommendations` | final output | recipe/steps/nutrition/substitutions/grocery_gap |
| `feedback_events` | accept/reject actions | action/message/recommendation_id |
| `calendar_blocks` | local schedule sync | start/end/title/recommendation_id |
| `cooking_tasks` | DAG + prep tasks | task type/dependencies/timing |
| `prep_windows` | proactive prep windows | time window/assigned tasks |
| `user_memory_profiles` | long-term metrics | favorites/patterns/money+waste+sustainability |

## 5. Persistence Model Simplification

### 5.1 Storage choice

The MVP uses memory-first SQLite with local snapshot files instead of PostgreSQL.

### 5.2 What this changes

- no external DB container or hosted DB is required
- no database bootstrap beyond app startup is required
- startup can restore from snapshot file into memory runtime
- every write commit flushes memory state to snapshot file
- schema can be created automatically when the app starts
- local development and demo environments can use the same lightweight storage model
- user and recommendation data can survive service restarts

### 5.3 What this does not change

It does **not** change the business design of the backend:

- onboarding data is still modeled relationally
- pantry and meal context are still persisted for planner reuse
- feedback and replan history are still tracked
- planner runs and recommendations are still stored as structured entities

### 5.4 Tradeoff

The main tradeoff is that SQLite is still a lightweight single-process-oriented database and is not intended to replace a larger production database architecture.

For hackathon scope, this is acceptable because the priority is:

- simpler architecture
- faster setup
- fewer operational dependencies
- reliable demo behavior across application restarts

## 6. Agent Loop

1. **Perceive**: collect profile/goals/pantry/intake/chat.
2. **Prioritize**: apply spoilage and hard-constraint priority.
3. **Retrieve**: fetch context from RAG and user memory.
4. **Query Recipe/Formulate**: generate candidate-backed recommendation draft.
5. **Reflect**: enforce allergies/diet/macro direction with retry.
6. **Finalize Execution**: persist calendar block + DAG tasks + prep windows.

## 7. Error Handling (Business)

- Input parse failure marks ingestion job as `FAILED`.
- Planner execution failure marks `plan_runs.status=FAILED`.
- No recipe candidates returns planner error; client can retry after context update.

## 8. MVP Scope Boundary

In scope:

1. profile/goals onboarding
2. fridge/meal/receipt/chat ingestion
3. Railtracks planner
4. recipe retrieval + normalization
5. grocery gap generation
6. feedback-driven replan
7. Memory-first SQLite + file snapshot persistence to reduce infrastructure complexity
8. local execution scheduling artifacts
9. long-term memory metric updates

Out of scope:

- dashboard analytics
- external calendar provider integrations
- external database infrastructure
- multi-service persistence architecture
