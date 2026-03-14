# Railtracks Architecture (Agentic V1)

## Overview

Planner execution is Railtracks-only and stage-based:

1. API receives `PlanRequest`
2. `planner_context` builds effective request (goals/pantry/meal/chat merge)
3. `RailtracksAgenticWorkflow.recommend_async()` runs:
   - `Perceive`
   - `Prioritize`
   - `Retrieve`
   - `Query Recipe`
   - `Formulate` (Railtracks LLM)
   - `Reflect` (max 3 attempts)
   - `Finalize Execution Plan`
4. `planner_execution` persists recommendation + plan run + execution artifacts + long-term memory updates
5. API returns `RecommendationBundle`

No ADK path and no multi-engine failover chain are present.

## Components

- `app/agents/rt_workflow.py`
  - stage orchestrator
  - bounded reflection/retry loop
  - V1 agent output assembly
- `app/agents/tools.py`
  - perception + recipe + macro + grocery tools
  - local execution tools (`sync_to_calendar`, `decompose_cooking_workflow`, `schedule_proactive_prep`)
- `app/services/planner_execution.py`
  - wraps workflow execution with persistence and execution-tool writes
- `app/services/user_memory.py`
  - updates long-term memory metrics from recommendation and feedback signals

## Tool Registry

- `analyze_fridge_vision`
- `analyze_meal_vision`
- `parse_receipt_items`
- `retrieve_recipe_candidates`
- `calculate_meal_macros`
- `generate_grocery_gap_tool`
- `decompose_cooking_workflow`
- `schedule_proactive_prep`
- `sync_to_calendar`

## Runtime Modes

- `plan_runs.mode`: `railtracks-agentic`
- `plan_runs.status`: `PROCESSING | COMPLETED | FAILED`

If workflow execution fails, request fails and run status is persisted as `FAILED`.
