# MVP Task List

This checklist is execution-ready for the backend-first hackathon build.

## Phase 0 - Scaffolding + Env + CI Baseline

### Task 0.1: Repository skeleton and module boundaries
- Owner: `TBD`
- Estimate: `0.5 day`
- Dependencies: none
- Done criteria: backend/frontend/docs folders exist with baseline structure.

### Task 0.2: Environment contract and local boot
- Owner: `TBD`
- Estimate: `0.5 day`
- Dependencies: Task 0.1
- Done criteria: `.env.example` covers all MVP vars; local server boots with placeholder routes.

### Task 0.3: CI baseline (lint + tests)
- Owner: `TBD`
- Estimate: `0.5 day`
- Dependencies: Task 0.2
- Done criteria: CI pipeline runs formatting, static checks, and test command for PRs.

## Phase 1 - Auth / Profile / Goals

### Task 1.1: Cognito token verification middleware
- Owner: `TBD`
- Estimate: `1 day`
- Dependencies: Phase 0
- Done criteria: protected routes validate Cognito JWT and map identity to app user.

### Task 1.2: Profile CRUD endpoints
- Owner: `TBD`
- Estimate: `0.75 day`
- Dependencies: Task 1.1
- Done criteria: profile create/read/update works with persistence.

### Task 1.3: Goal CRUD endpoints
- Owner: `TBD`
- Estimate: `0.75 day`
- Dependencies: Task 1.1
- Done criteria: nutrition and planning constraints are persisted and retrievable.

## Phase 2 - Multimodal Input Ingestion

### Task 2.1: Fridge scan ingestion and async parse pipeline
- Owner: `TBD`
- Estimate: `1 day`
- Dependencies: Phase 1
- Done criteria: fridge input accepted, async parse runs, pantry state updates.

### Task 2.2: Meal scan ingestion and nutrition log update
- Owner: `TBD`
- Estimate: `1 day`
- Dependencies: Phase 1
- Done criteria: meal scan updates `meal_logs` with macro estimates.

### Task 2.3: Receipt scan ingestion and pantry merge
- Owner: `TBD`
- Estimate: `1 day`
- Dependencies: Phase 1
- Done criteria: receipt parser adds purchased items and de-duplicates pantry records.

### Task 2.4: Chat context ingestion endpoint
- Owner: `TBD`
- Estimate: `0.5 day`
- Dependencies: Phase 1
- Done criteria: user natural-language instructions are stored for planner context.

## Phase 3 - Planner + Recipe Retrieval + Grocery Gap

### Task 3.1: Plan request assembly service
- Owner: `TBD`
- Estimate: `1 day`
- Dependencies: Phase 2
- Done criteria: planner combines goals, intake, pantry, and chat context into `PlanRequest`.

### Task 3.2: Recipe retrieval adapter (external API)
- Owner: `TBD`
- Estimate: `1 day`
- Dependencies: Task 3.1
- Done criteria: recipe candidates returned with timeout handling and source metadata.

### Task 3.3: Macro calculator and constraint scorer
- Owner: `TBD`
- Estimate: `0.75 day`
- Dependencies: Task 3.2
- Done criteria: candidates scored against macro/time/restriction constraints.

### Task 3.4: Grocery gap generation
- Owner: `TBD`
- Estimate: `0.5 day`
- Dependencies: Task 3.3
- Done criteria: minimal missing ingredients output with reasons.

### Task 3.5: Recommendation bundle endpoint
- Owner: `TBD`
- Estimate: `0.75 day`
- Dependencies: Tasks 3.1-3.4
- Done criteria: endpoint returns stable `RecommendationBundle` contract.

## Phase 4 - Feedback Replan Loop

### Task 4.1: Feedback patch endpoint and persistence
- Owner: `TBD`
- Estimate: `0.5 day`
- Dependencies: Phase 3
- Done criteria: accept/reject feedback stored with message.

### Task 4.2: Replan trigger from feedback
- Owner: `TBD`
- Estimate: `0.75 day`
- Dependencies: Task 4.1
- Done criteria: feedback triggers updated recommendation while retaining traceability.

### Task 4.3: Agent trace capture
- Owner: `TBD`
- Estimate: `0.5 day`
- Dependencies: Task 4.2
- Done criteria: each run stores stage-level trace notes for debugging/demo.

## Phase 5 - Polish, Observability, Demo Script

### Task 5.1: Structured logging and trace IDs
- Owner: `TBD`
- Estimate: `0.5 day`
- Dependencies: Phases 1-4
- Done criteria: all key endpoints emit consistent traceable logs.

### Task 5.2: Resilience pass (timeouts, retries, fallback)
- Owner: `TBD`
- Estimate: `0.75 day`
- Dependencies: Phases 2-4
- Done criteria: degraded provider modes return safe fallback behavior.

### Task 5.3: End-to-end demo script and sample dataset
- Owner: `TBD`
- Estimate: `0.5 day`
- Dependencies: all previous phases
- Done criteria: repeatable live demo flow works from onboarding to feedback replan.

## Cross-Cutting Test Scenarios

1. Contract tests for all public schemas and status transitions.
2. Agent-loop scenarios: fridge-only, meal-only, receipt-only, combined-input.
3. Constraint tests: allergy conflict, calorie overflow, substitution, spoilage priority.
4. Integrations: Cognito verification, PostgreSQL persistence, recipe API timeout fallback.
5. Demo acceptance run: full user journey from signup context to replanned recommendation.
