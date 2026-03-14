# Agent Specification (Hackathon MVP, Agentic V1)

## 1. Product Goal

Build a multimodal dietary planning agent that produces an executable next-meal decision from:

- onboarding constraints
- pantry and intake context
- free-form user intent

The agent must optimize for nutrition goals, spoilage reduction, grocery efficiency, and usability.

## 2. Scope

### In Scope

1. Profile/goals onboarding and strict JWT-authenticated access.
2. Fridge/meal/receipt/chat ingestion with persisted context.
3. Stage-based Railtracks planner flow:
   - Perceive
   - Prioritize
   - Retrieve
   - Query Recipe
   - Formulate
   - Reflect (retry up to 3 attempts)
   - Finalize Execution Plan
4. Feedback-driven replanning with constraint inheritance from original run snapshot.
5. Local execution tools:
   - calendar block persistence
   - cooking DAG task decomposition
   - proactive prep window scheduling
6. Long-term memory aggregates:
   - favorite recipes
   - purchase patterns
   - cumulative money saved
   - food-waste reduction metrics
   - sustainability impact metrics

### Out of Scope

- analytics dashboard UX
- production observability/traffic strategy
- external calendar providers (Google/Apple/MCP) in this round

## 3. Core Workflow

### 3.1 Perceive

Build one effective `PlanRequest` from request payload + persisted context:

- goals fallback
- pantry fallback
- latest meal fallback
- latest chat fallback

### 3.2 Prioritize

Extract planning priorities:

- expiring ingredients
- allergies/restrictions
- time/budget boundaries

### 3.3 Retrieve + Query Recipe

Use RAG context + recipe provider candidates (TheMealDB) to produce ranked recipe options.

### 3.4 Formulate

Railtracks LLM generates a structured recommendation draft.

### 3.5 Reflect

Apply hard checks and adjustment guidance:

- allergen/diet safety
- macro and calorie guidance
- spoilage reminders

If violated, retry with alternate candidate (max 3 attempts total).

### 3.6 Finalize Execution Plan

Generate executable artifacts:

- calendar blocks
- DAG cooking tasks
- proactive prep windows

Persist artifacts locally.

## 4. Tool Contracts

### Perception/Planning Tools

- `analyze_fridge_vision`
- `analyze_meal_vision`
- `parse_receipt_items`
- `retrieve_recipe_candidates`
- `calculate_meal_macros`
- `generate_grocery_gap_tool`

### Execution Tools

- `decompose_cooking_workflow`
- `schedule_proactive_prep`
- `sync_to_calendar`

All execution tools are local-first and persist to SQLite.

## 5. Memory Model

### Short-Term

- effective request context
- run trace and reflection notes
- prior recipe hint for replan continuity

### Long-Term

Stored in `user_memory_profiles`:

- `favorite_recipes`
- `purchase_patterns`
- `cumulative_money_saved`
- `food_waste_reduction_metrics`
- `sustainability_impact_metrics`

## 6. Public Contract (V1)

Planner endpoints keep existing paths (`/api/v1/planner/*`) and return `RecommendationBundle`.

Fields:

- `recommendation_id`
- `decision` (`recipe_title`, `rationale`, `confidence`)
- `meal_plan` (`steps`, `nutrition_summary`, `substitutions`, `spoilage_alerts`)
- `grocery_plan` (`missing_ingredients`, `optimized_grocery_list`, `estimated_gap_cost`)
- `execution_plan` (`calendar_blocks`, `cooking_dag_tasks`, `proactive_prep_windows`)
- `reflection` (`status`, `attempts`, `violations`, `adjustments`)
- `memory_updates` (`short_term_updates`, `long_term_metric_deltas`)
