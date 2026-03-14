# Agent Specification (MVP, Railtracks)

> Implementation status: planner orchestration is migrated to Railtracks workflow execution.

## 1. Goal

Deliver a business-first agent that turns user food context into practical meal decisions:

- hit nutrition targets
- prioritize expiring ingredients
- reduce grocery waste and unnecessary purchases

## 2. Railtracks Workflow Graph

```mermaid
flowchart LR
  U["User Inputs"] --> P["Perceive Node"]
  P --> R["Reason Node"]
  R --> T["Retrieve Node"]
  T --> A["Act Node"]
  A --> F["Reflect Node"]
  F --> O["RecommendationBundle"]
```

### Node Responsibilities

- **Perceive**: collect profile/goals/pantry/intake/chat + latest scan signals.
- **Reason**: resolve constraints and prioritize spoilage-sensitive ingredients.
- **Retrieve**: fetch recipe candidates and metadata from TheMealDB adapter.
- **Act**: construct recommendation, nutrition estimate, and grocery gap.
- **Reflect**: enforce hard business constraints and patch unsafe outputs.

## 3. Tool Contracts (MVP)

### 3.1 `analyze_fridge_vision(image_payload)`

Input:
- fridge image reference
- optional pre-detected items

Output:
- normalized ingredient list (`ingredient`, `quantity`, `expires_in_days`)

### 3.2 `analyze_meal_vision(image_payload)`

Input:
- meal image reference

Output:
- meal label + estimated macros (`calories`, `protein_g`, `carbs_g`, `fat_g`)

### 3.3 `parse_receipt_items(image_payload)`

Input:
- grocery receipt image reference

Output:
- normalized purchased items list for pantry merge

### 3.4 `retrieve_recipe_candidates(query_constraints)`

Input:
- ingredient priority
- dietary/allergy rules
- calorie/macro/cook-time/budget targets

Output:
- ranked candidates with parsed recipe metadata

### 3.5 `calculate_meal_macros(recipe_ingredients)`

Output:
- nutrition estimate used for scoring and response rendering

### 3.6 `generate_grocery_gap(recipe_ingredients, current_inventory)`

Output:
- minimal missing ingredients list with reason strings

## 4. Memory Policy

### 4.1 Short-Term Runtime State

- current workflow inputs
- candidate ranking context
- interim substitution decisions

### 4.2 Long-Term Persisted Memory

- profile/goals
- pantry and receipt history
- meal history
- recommendation and feedback history

## 5. Reflection Policy (Business Hard Checks)

1. remove allergen conflicts from output
2. remove non-compliant ingredients for vegetarian/vegan constraints
3. enforce calorie/macro direction via substitution guidance
4. enforce spoilage-priority reminders
5. enforce grocery-gap consistency with selected recipe

If a perfect candidate is unavailable, return best feasible plan plus explicit adjustment hints.

## 6. Feedback-Driven Replanning Policy

- `reject` feedback text is parsed into structured overrides (calorie/time/restriction/allergy hints).
- Parsed overrides merge with stored goals.
- Same Railtracks workflow reruns with updated constraints.
- New recommendation is persisted and linked through `plan_runs` + `feedback_events`.

## 7. Output Contract

Primary output is `RecommendationBundle`:

- `recipe_title`
- `steps`
- `nutrition_summary`
- `substitutions`
- `spoilage_alerts`
- `grocery_gap`

Secondary output for trace/debug:

- `plan_runs.status`
- `plan_runs.mode` (`railtracks` or `fallback`)
- `plan_runs.trace_notes`
