# MVP Task List (Hackathon Deliverables)

This checklist is scoped to the current hackathon deliverables and focuses on user-facing business functionality only.

## Deliverable 1 - User Setup and Personalization

### Task 1.1: Auth bootstrap
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: none
- Done criteria: protected APIs can resolve the current authenticated user.

### Task 1.2: Profile onboarding
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Task 1.1
- Done criteria: user can create, update, and read profile fields including body metrics, activity level, dietary preferences, allergies, and cook-time preference.

### Task 1.3: Goal setup
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Task 1.1
- Done criteria: calorie target, macro targets, dietary restrictions, allergies, budget limit, and max cook time can be created, updated, and fetched.

## Deliverable 2 - Multimodal Context Ingestion

### Task 2.1: Fridge scan ingestion
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Deliverable 1
- Done criteria: fridge image submission creates an async job and updates pantry items with ingredient, quantity, expiry, and source.

### Task 2.2: Receipt scan ingestion
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Deliverable 1
- Done criteria: receipt image submission creates an async job, stores parsed receipt data, and merges purchased items into pantry state.

### Task 2.3: Meal scan ingestion
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Deliverable 1
- Done criteria: meal image submission creates an async job and writes a meal log with estimated nutrition.

### Task 2.4: Pantry view and cleanup
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Tasks 2.1, 2.2
- Done criteria: user can list pantry items and delete an item that is no longer available.

### Task 2.5: Spoilage alert surface
- Owner: `Backend`
- Estimate: `0.25 day`
- Dependencies: Tasks 2.1, 2.2
- Done criteria: user can fetch pantry items that are close to expiry with urgency labels.

### Task 2.6: Chat context capture
- Owner: `Backend`
- Estimate: `0.25 day`
- Dependencies: Deliverable 1
- Done criteria: user can submit a planning message that is persisted as latest planning intent.

### Task 2.7: Chat-triggered auto replan
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Task 2.6, Deliverable 3
- Done criteria: chat message endpoint can optionally trigger immediate recommendation generation using persisted context.

## Deliverable 3 - Core Planner Experience

### Task 3.1: Effective planning context builder
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Deliverable 2
- Done criteria: planner request can auto-fill missing constraints, pantry, latest meal, and latest chat message from persisted user context.

### Task 3.2: Recipe candidate retrieval
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Task 3.1
- Done criteria: recipe candidates are fetched and normalized into the internal planning format.

### Task 3.3: Candidate scoring and selection
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Task 3.2
- Done criteria: ranking considers dietary restrictions, allergies, calorie direction, cook time, spoilage priority, and grocery gap size.

### Task 3.4: Recommendation bundle assembly
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Task 3.3
- Done criteria: planner returns `RecommendationBundle` with recipe title, steps, nutrition summary, substitutions, spoilage alerts, and grocery gap.

### Task 3.5: Recommendation detail surfaces
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Task 3.4
- Done criteria: user can separately fetch recipe detail, nutrition summary, grocery gap, and latest recommendation.

### Task 3.6: Planner run visibility
- Owner: `Backend`
- Estimate: `0.25 day`
- Dependencies: Task 3.4
- Done criteria: latest planning run can be fetched with run status, execution mode, recommendation id, and trace notes.

## Deliverable 4 - Constraint Safety and Reflection

### Task 4.1: Allergy conflict handling
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Deliverable 3
- Done criteria: allergen ingredients are excluded from grocery gap and unsafe suggestions are removed from final output.

### Task 4.2: Dietary restriction enforcement
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Deliverable 3
- Done criteria: vegetarian and similar restriction conflicts trigger substitutions or compliant alternatives.

### Task 4.3: Calorie and macro adjustment guidance
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Deliverable 3
- Done criteria: overly heavy recommendations include lighter substitutions or adjustment guidance.

### Task 4.4: Spoilage-priority reminders
- Owner: `Backend`
- Estimate: `0.25 day`
- Dependencies: Deliverable 2, Deliverable 3
- Done criteria: expiring ingredients generate spoilage alerts in the recommendation response.

## Deliverable 5 - Feedback and Replanning Loop

### Task 5.1: Feedback persistence
- Owner: `Backend`
- Estimate: `0.25 day`
- Dependencies: Deliverable 3
- Done criteria: accept/reject feedback is stored with the associated recommendation.

### Task 5.2: Reject triggers automatic replan
- Owner: `Backend`
- Estimate: `0.75 day`
- Dependencies: Task 5.1
- Done criteria: rejecting a recommendation creates a new recommendation with a new id.

### Task 5.3: Manual replan endpoint
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Deliverable 3
- Done criteria: user can request a replan from an existing recommendation with optional override payload.

### Task 5.4: Feedback text parsing into structured constraints
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Task 5.2
- Done criteria: free-text instructions such as "under 450 calories", "vegetarian", "15 minutes", and budget hints are converted into planner constraints.

### Task 5.5: Prior recommendation continuity
- Owner: `Backend`
- Estimate: `0.25 day`
- Dependencies: Task 5.3
- Done criteria: replanning carries forward prior recommendation context so the next result is meaningfully different but still relevant.

## Deliverable 6 - Demo-Ready End-to-End Experience

### Task 6.1: Happy-path API walkthrough
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Deliverables 1-5
- Done criteria: end-to-end flow works in this order: auth bootstrap -> profile/goals -> scans/chat -> planner -> feedback -> replan.

### Task 6.2: Input-combination scenarios
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Deliverables 2-5
- Done criteria: system behaves correctly for fridge-only, meal-only, receipt-only, and combined scan scenarios.

### Task 6.3: Constraint scenario coverage
- Owner: `Backend`
- Estimate: `0.5 day`
- Dependencies: Deliverables 3-5
- Done criteria: demo coverage includes allergen blocking, calorie overflow guidance, vegetarian conflict handling, and spoilage-priority behavior.

### Task 6.4: Replan cascade demo
- Owner: `Backend`
- Estimate: `0.25 day`
- Dependencies: Deliverable 5
- Done criteria: one recommendation can be replanned multiple times, producing distinct recommendation ids across the chain.

## Business Acceptance Checklist

1. User can sign in and complete profile + goal setup.
2. User can submit fridge, receipt, meal, and chat inputs.
3. Pantry state updates from ingestion and can be reviewed.
4. Planner can generate a recommendation even when parts of context are omitted from the request.
5. Recommendation output is actionable and includes recipe steps, nutrition, substitutions, spoilage alerts, and grocery gap.
6. User can inspect latest recommendation and related output surfaces.
7. User can accept or reject a recommendation.
8. Reject feedback or manual replan generates a new recommendation.
9. Free-text feedback can refine future recommendations through parsed constraints.
10. The full hackathon demo flow can be shown end to end with stable business behavior.