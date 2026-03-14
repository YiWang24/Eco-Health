# MVP Task List (Business Features Only)

This checklist is scoped for hackathon business delivery. Non-functional items are intentionally excluded.

## Phase 1 - Onboarding and Goal Setup

### Task 1.1: User sign-in bootstrap
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: none
- Done criteria: authenticated user identity is available in protected API routes.

### Task 1.2: Profile create/update/read
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Task 1.1
- Done criteria: profile API supports full onboarding data roundtrip.

### Task 1.3: Goal create/update/read
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Task 1.1
- Done criteria: nutrition + restriction + budget/time goals persist and load correctly.

## Phase 2 - Multimodal Food Context Ingestion

### Task 2.1: Receipt ingestion pipeline
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Phase 1
- Done criteria: receipt scan updates pantry inventory via async job.

### Task 2.2: Fridge ingestion pipeline
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Phase 1
- Done criteria: fridge scan extracts ingredients and spoilage hints into pantry state.

### Task 2.3: Meal ingestion pipeline
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Phase 1
- Done criteria: meal scan writes meal log with macro estimates.

### Task 2.4: Chat message context endpoint
- Owner: `Backend`
- Estimate: `0.25 day`
- Dependencies: Phase 1
- Done criteria: user messages are persisted and retrievable for planning context.

## Phase 3 - Railtracks Planner Core

### Task 3.1: Effective context builder
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Phase 2
- Done criteria: planner request auto-merges goals/pantry/meal/chat context when omitted.

### Task 3.2: Recipe candidate retrieval
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Task 3.1
- Done criteria: TheMealDB candidates are fetched and normalized into internal recipe format.

### Task 3.3: Candidate scoring + selection
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Task 3.2
- Done criteria: ranking considers goals, restrictions, allergies, spoilage, and grocery gap size.

### Task 3.4: Recommendation output assembly
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Task 3.3
- Done criteria: `RecommendationBundle` returns recipe steps, nutrition, substitutions, alerts, and grocery gap.

## Phase 4 - Feedback Replan Loop

### Task 4.1: Feedback persistence
- Owner: `Backend`
- Estimate: `0.25 day`
- Dependencies: Phase 3
- Done criteria: accept/reject feedback stored with recommendation link.

### Task 4.2: Reject -> replan workflow
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Task 4.1
- Done criteria: reject feedback triggers a new planner run and returns a new recommendation id.

### Task 4.3: Feedback text constraint parsing
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Task 4.2
- Done criteria: text instructions (e.g. low calorie, vegetarian, 15 mins) are converted to structured overrides.

## Phase 5 - Demo-Ready End-to-End Flow

### Task 5.1: One-shot scripted API flow
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Phases 1-4
- Done criteria: scripted run demonstrates onboarding -> scans -> planner -> feedback replan.

### Task 5.2: Real E2E test with generated images
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Task 5.1
- Done criteria: optional real E2E test executes full flow using generated receipt/fridge/meal images.

## Business Acceptance Scenarios

1. User can complete onboarding and set goals.
2. User can submit receipt/fridge/meal scans and get planner-ready context.
3. Planner returns actionable recommendation bundle.
4. User can send chat constraints and get updated recommendations.
5. Reject feedback triggers automatic replanning with new recommendation output.
