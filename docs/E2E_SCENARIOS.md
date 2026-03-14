# E2E Scenario Design (Hackathon User Journey)

**Last Updated:** 2026-03-14

This document redesigns end-to-end scenario coverage around the product user journey:

**User Onboarding → Food and Chat Input → Agent Loop → Personalized Meal Plan → User Feedback → Agent Replans Automatically**

The goal of this document is to define **functional E2E scenarios** that prove the hackathon product delivers a complete user-facing experience, not just isolated API success.

This document is intentionally focused on:

- user-visible workflow coverage
- business behavior and expected outcomes
- cross-step scenario continuity
- recommendation quality expectations
- feedback-driven replanning behavior

This document intentionally excludes:

- rollout strategy
- observability/metrics design
- fallback architecture design
- infrastructure monitoring
- logging-only validation

---

## 1. Product Journey Under Test

The system should support this complete journey:

1. **User Onboarding**
   - user creates or updates their health and food-planning profile
   - user stores health goals, restrictions, preferences, budget, and time constraints

2. **Food and Chat Input**
   - user provides real-world context through fridge scan, meal scan, receipt scan, and chat

3. **Agent Loop**
   - system understands multimodal input
   - retrieves user memory and current context
   - reasons over goals, constraints, pantry state, spoilage, budget, and time
   - retrieves grounded recipes and planning candidates

4. **Personalized Meal Plan**
   - system returns actionable meal recommendations with useful options and supporting details

5. **User Feedback**
   - user refines the recommendation through natural language

6. **Automatic Replanning**
   - system updates the meal recommendation without restarting the workflow

---

## 2. E2E Design Principles

Each E2E scenario should validate one or more of the following product truths:

1. **Context persists across steps**
   - onboarding data and prior inputs remain available to future planning

2. **Planning is personalized**
   - outputs reflect health goals, restrictions, preferences, budget, and available time

3. **Planning is grounded**
   - outputs connect to pantry state, recent meal context, and retrievable recipe content

4. **Planning is actionable**
   - results include enough detail for the user to cook, shop, or make a decision immediately

5. **Planning is adaptive**
   - user feedback changes future output without requiring a full restart

6. **Planning is flexible**
   - the user can reach a valid result through multiple input combinations

---

## 3. Journey-Level Scenario Matrix

| Journey Stage | Scenario Group | What Must Be Proven |
|---|---|---|
| User Onboarding | profile + goals setup | the agent receives stable long-term constraints |
| Food and Chat Input | fridge / meal / receipt / chat | the agent can build context from multiple real-world input channels |
| Agent Loop | context merge + reasoning | the system combines memory and new inputs into one coherent planning request |
| Personalized Meal Plan | recommendation output | the result is useful, constraint-aware, and actionable |
| User Feedback | natural-language refinement | the user can reshape the plan conversationally |
| Agent Replans Automatically | automatic replan | the system creates a new recommendation without restarting onboarding or input ingestion |

---

## 4. Core User Journey Scenarios

## 4.1 Journey A — First-Time Healthy Planning Setup

### Goal
Prove that a first-time user can complete onboarding and create a recommendation-ready profile.

### Input Conditions
- new user
- no existing profile
- no goals saved yet

### User Actions
1. user signs in
2. user submits baseline health context:
   - age
   - height
   - weight
   - activity level
   - health conditions
3. user submits goals and constraints:
   - primary health goal
   - dietary preferences
   - allergies and restrictions
   - cooking/eating habits
   - time availability
   - budget preference

### Expected Agent/System Behavior
- system persists onboarding context
- system stores profile and goals as future planning constraints
- future planning requests can reuse these constraints automatically

### Expected Output/Validation
- profile is retrievable
- goals are retrievable
- fields are correctly stored and associated with the authenticated user

### Business Value
This proves the system is not stateless chat. It builds durable personalized nutrition context.

---

## 4.2 Journey B — Fridge-First Planning

### Goal
Prove that a user can scan the fridge, identify ingredients and spoilage risk, and receive a pantry-aware recommendation.

### Input Conditions
- user already completed onboarding
- pantry is initially empty or outdated
- fridge contains ingredients with one or more near-expiry items

### User Actions
1. user submits fridge scan
2. system extracts ingredients and expiry hints
3. user asks: "What should I cook tonight?"
4. user requests recommendation

### Expected Agent/System Behavior
- fridge scan updates pantry state
- expiring items become available to planner
- planner uses onboarding goals + pantry + chat instruction
- planner prioritizes ingredients close to expiry

### Expected Output/Validation
- recommendation references available ingredients
- spoilage alert is included when appropriate
- grocery gap is minimized because pantry is known
- response is actionable and personalized

### Business Value
This demonstrates the food-waste reduction story and pantry-aware planning.

---

## 4.3 Journey C — Receipt-to-Pantry-to-Plan

### Goal
Prove that a grocery receipt can refresh pantry state and immediately improve planning quality.

### Input Conditions
- user has goals and constraints
- receipt contains recently purchased ingredients
- no fridge scan required for this scenario

### User Actions
1. user submits grocery receipt scan
2. system extracts purchased items
3. system updates pantry inventory
4. user requests a meal recommendation

### Expected Agent/System Behavior
- receipt scan creates pantry updates
- recommendation uses newly purchased ingredients where relevant
- grocery gap avoids re-listing items the user just bought

### Expected Output/Validation
- pantry includes receipt-derived items
- recommendation is grounded in pantry state
- grocery list is smaller or more realistic than without receipt context

### Business Value
This validates the "virtual pantry" concept and reduces duplicate grocery suggestions.

---

## 4.4 Journey D — Meal Logging Informs the Next Plan

### Goal
Prove that recent meal intake can shape future meal recommendations.

### Input Conditions
- user has completed onboarding
- user submits a meal photo before planning the next meal

### User Actions
1. user submits meal scan
2. system logs meal nutrition
3. user requests another meal recommendation

### Expected Agent/System Behavior
- meal scan creates a recent meal record
- planner can access the latest meal log
- planner uses this context to produce a more informed next recommendation

### Expected Output/Validation
- meal log exists
- planner run includes latest meal context
- recommendation remains valid and personalized

### Business Value
This supports the story that the system reasons across a user's food timeline, not just one isolated input.

---

## 4.5 Journey E — Chat-Only Personalization

### Goal
Prove that even without a new scan, the user can steer planning through natural language.

### Input Conditions
- user already has profile/goals saved
- pantry may or may not already exist
- latest instruction is delivered through chat only

### User Actions
1. user sends chat instruction such as:
   - "Make it vegetarian."
   - "Use ingredients that will expire soon."
   - "I only have 15 minutes."
2. user requests recommendation or chat triggers replanning automatically

### Expected Agent/System Behavior
- system persists the latest chat message
- planner interprets the message as planning intent
- planner merges chat instruction with saved constraints

### Expected Output/Validation
- recommendation changes according to the message
- time constraints, dietary direction, or spoilage priority are reflected in output
- no onboarding restart is required

### Business Value
This demonstrates low-friction interaction and conversational control.

---

## 5. Personalized Meal Plan Scenarios

## 5.1 Scenario Group — Output Is Actionable

### Goal
Prove that the returned plan is not just a generic recipe name but a complete next-step decision package.

### Expected Recommendation Structure
The response should include:

- `recipe_title`
- `steps`
- `nutrition_summary`
- `substitutions`
- `spoilage_alerts`
- `grocery_gap`

### Rich Product Expectation
For the hackathon design, the ideal meal-plan experience may contain:

- **2-3 meal options**
- each option includes:
  - recommended recipe
  - step-by-step cooking instructions
  - nutrition breakdown
  - substitutions
  - spoilage relevance
  - minimal shopping list

### Current MVP Compatibility Note
If the current backend returns a single `RecommendationBundle`, E2E coverage should still validate:
- recommendation usefulness
- personalization quality
- actionability
- replan flexibility

Multi-option recommendation can be treated as:
- an extension scenario
- or a near-term contract evolution

### Expected Output/Validation
- recipe steps are non-empty
- nutrition summary is present
- grocery gap is present and coherent
- substitutions exist when constraints require them
- spoilage alerts exist when near-expiry ingredients are present

---

## 5.2 Scenario Group — Recommendation Reflects Health Goal

### Goal
Prove that planning changes based on the user's primary health goal.

### Example Goal Variants
- maintain healthy lifestyle
- lose weight
- build muscle
- heart health
- blood sugar control

### Scenario Examples
1. **Lose weight**
   - recommendation should trend toward lighter calorie direction
   - substitutions may reduce calories

2. **Build muscle**
   - recommendation should trend toward higher protein direction

3. **Heart health**
   - recommendation should avoid obviously conflicting ingredient directions
   - grocery gap and substitutions should support healthier swaps

4. **Blood sugar control**
   - recommendation should respect the nutrition intent implied by this goal

### Expected Output/Validation
- recommendations differ in meaningful ways based on primary health goal
- recommendation remains grounded in pantry and user constraints

### Business Value
This proves the system is truly personalized and not returning one-size-fits-all advice.

---

## 5.3 Scenario Group — Recommendation Reflects Lifestyle Constraints

### Goal
Prove that planning respects the user's real-world living habits, not just nutrition math.

### Input Dimensions
- cooking vs eating outside
- schedule constraints
- time for food prep
- budget preference
- cuisine preference
- allergies and restrictions

### Expected Agent/System Behavior
The planner should reason over:
- cook time
- affordability
- food preference
- restriction safety
- pantry practicality

### Example Cases
1. **15-minute availability**
   - recommendation should be quick to prepare

2. **Budget saver preference**
   - grocery gap should stay minimal and practical

3. **Asian food preference**
   - recipe direction should align where feasible

4. **No red meat / lactose intolerant / nut allergy**
   - output should remain compliant and safe

### Expected Output/Validation
- constraints are visible in recommendation quality
- recommendation remains usable and realistic

---

## 6. Agent Loop Scenarios

## 6.1 Scenario Group — Memory Retrieval and Context Merge

### Goal
Prove that the agent combines multiple sources of memory into one planning decision.

### Context Sources
- onboarding profile
- saved goals
- pantry from fridge/receipt
- latest meal log
- latest chat instruction
- prior recommendation context during replan

### Expected Agent/System Behavior
When request payload is partial:
- missing constraints are loaded from stored goals
- missing inventory is loaded from pantry
- missing meal context is loaded from latest meal log
- missing message is loaded from latest chat message

### Expected Output/Validation
- planner succeeds even with incomplete request payload
- recommendation still reflects stored user state

### Business Value
This is essential to the “agent” story: the system remembers and reasons, rather than requiring repeated manual input.

---

## 6.2 Scenario Group — Constraint Reasoning

### Goal
Prove that the agent reasons across competing constraints.

### Constraint Types
- nutrition targets
- ingredient availability
- spoilage risk
- budget
- cook time
- allergies
- restrictions
- preference signals

### Example Composite Scenario
A user:
- wants weight loss
- is vegetarian
- has peanut allergy
- only has 15 minutes
- has spinach expiring tomorrow
- prefers lower grocery spend

### Expected Agent/System Behavior
- planner balances all of the above
- recommendation avoids allergen conflicts
- recommendation respects vegetarian constraint
- recommendation notices spoilage urgency
- grocery gap stays small
- output remains actionable

### Expected Output/Validation
- no allergen in grocery gap
- substitutions exist if candidate fit is imperfect
- spoilage alert exists if expiring ingredient is not fully utilized
- recommendation remains coherent

---

## 6.3 Scenario Group — Recipe Grounding

### Goal
Prove that the agent retrieves grounded recipe candidates rather than inventing vague meal advice.

### Expected Agent/System Behavior
- recipe retrieval is invoked
- recommendation uses grounded recipe structure and metadata
- shopping list aligns with chosen recipe

### Expected Output/Validation
- recipe detail endpoint returns usable recipe metadata
- grocery gap is consistent with the chosen recipe
- recommendation can be explained through recipe content

### Business Value
This supports trust and makes the result easier to act on.

---

## 7. Feedback and Automatic Replan Scenarios

## 7.1 Journey F — Simple Reject Replan

### Goal
Prove that rejecting a plan generates a new recommendation automatically.

### User Actions
1. user receives recommendation
2. user rejects it with a short instruction:
   - "Make it lower calories."

### Expected Agent/System Behavior
- feedback event is stored
- message is interpreted as updated constraint direction
- new planner run executes automatically
- new recommendation id is created

### Expected Output/Validation
- `replanned_recommendation_id` is returned
- latest recommendation is different from original
- new recommendation remains valid

### Business Value
This proves the experience is iterative, not dead-end.

---

## 7.2 Journey G — Structured Constraint Parsing from Natural Language

### Goal
Prove that free-text feedback can be translated into structured planning constraints.

### Example User Messages
- "Swap chicken for tofu."
- "Make it lower calories."
- "I only have 15 minutes."
- "No dairy."
- "Keep it under 450 calories and vegetarian."

### Expected Agent/System Behavior
The system should infer where possible:
- calorie target or reduction direction
- cook time limit
- dietary restriction
- allergen-style exclusions
- protein direction
- budget hints
- ingredient substitution intent

### Expected Output/Validation
- planner run trace shows replan trigger
- new recommendation reflects the parsed constraint changes
- no full reset is required

### Business Value
This is central to the natural interaction story.

---

## 7.3 Journey H — Multi-Step Replan Cascade

### Goal
Prove that the system supports multiple rounds of refinement.

### User Actions
1. initial recommendation is created
2. user asks for a different cuisine
3. second recommendation is created
4. user then asks for more protein
5. third recommendation is created

### Expected Agent/System Behavior
- each replan preserves continuity
- each replan produces a new recommendation id
- prior recommendation context can influence the next step without locking the user in

### Expected Output/Validation
- recommendation ids are distinct across the chain
- each recommendation remains valid
- constraints remain enforced across the chain

### Business Value
This demonstrates continuous AI-assisted meal decision making.

---

## 8. Scenario Catalog by Functional Capability

| Scenario ID | Scenario Name | Journey Stage | Primary Capability |
|---|---|---|---|
| E2E-01 | First-time onboarding | User Onboarding | profile + goals persistence |
| E2E-02 | Update onboarding later | User Onboarding | editable long-term constraints |
| E2E-03 | Fridge-first planning | Food Input → Agent Loop | pantry + spoilage-aware planning |
| E2E-04 | Receipt-to-pantry planning | Food Input → Agent Loop | purchased-items memory |
| E2E-05 | Meal-log-informed recommendation | Food Input → Agent Loop | recent intake context |
| E2E-06 | Chat-only planning refinement | Food Input → Agent Loop | natural-language planning intent |
| E2E-07 | Persisted context autofill | Agent Loop | memory retrieval and merge |
| E2E-08 | Constraint-heavy planning | Agent Loop | multi-constraint reasoning |
| E2E-09 | Actionable recommendation bundle | Personalized Meal Plan | useful output package |
| E2E-10 | Multi-option meal plan | Personalized Meal Plan | 2-3 alternative options design target |
| E2E-11 | Health-goal-specific recommendation | Personalized Meal Plan | goal-sensitive planning |
| E2E-12 | Lifestyle-aware recommendation | Personalized Meal Plan | time/budget/habit-aware planning |
| E2E-13 | Reject and auto replan | User Feedback → Replan | automatic recommendation refresh |
| E2E-14 | Natural-language constraint parsing | User Feedback → Replan | free-text to structured override |
| E2E-15 | Multi-step replan cascade | User Feedback → Replan | continuous decision loop |

---

## 9. MVP Coverage vs Target Coverage

## 9.1 Current MVP-Aligned Coverage

The current MVP should at minimum prove these journey capabilities:

1. onboarding profile and goals persist
2. fridge/meal/receipt/chat inputs can be stored or processed
3. pantry context is reused by planner
4. planner returns an actionable recommendation bundle
5. spoilage and restriction logic affect output
6. feedback reject triggers a new recommendation
7. planner can replan multiple times

## 9.2 Expanded Hackathon Target Coverage

The richer user-journey design should additionally aim to prove:

1. health condition influences planning direction
2. primary health goal meaningfully changes recommendation style
3. cooking/eating habits affect recommendation practicality
4. budget preference affects grocery gap strategy
5. time availability affects recipe suitability
6. cuisine preference influences recipe selection where feasible
7. output can evolve from a single recommendation to **2-3 alternatives**

---

## 10. Acceptance Criteria by Journey Stage

## 10.1 User Onboarding Acceptance
- user can create and update health profile
- user can create and update goals/constraints
- onboarding data persists for future planning

## 10.2 Food Input Acceptance
- fridge scan updates pantry
- receipt scan updates pantry
- meal scan logs meal context
- chat message persists planning intent

## 10.3 Agent Loop Acceptance
- planner can combine stored and fresh context
- planner can reason over multiple constraints
- planner can produce a coherent plan from partial request input

## 10.4 Personalized Meal Plan Acceptance
- output is actionable
- output is personalized
- output is grounded in pantry and recipe context
- output includes enough detail to cook or shop immediately

## 10.5 Feedback Acceptance
- user can reject and refine naturally
- feedback persists as part of user history
- feedback meaningfully changes the next plan

## 10.6 Automatic Replan Acceptance
- system generates a new recommendation id
- system does not require onboarding restart
- system does not require re-entering all prior context
- replan remains constraint-safe and actionable

---

## 11. Recommended E2E Test Execution Order

For a full judge-facing walkthrough, use this order:

1. **E2E-01** First-time onboarding
2. **E2E-03** Fridge-first planning
3. **E2E-04** Receipt-to-pantry planning
4. **E2E-06** Chat-only planning refinement
5. **E2E-07** Persisted context autofill
6. **E2E-09** Actionable recommendation bundle
7. **E2E-11** Health-goal-specific recommendation
8. **E2E-13** Reject and auto replan
9. **E2E-14** Natural-language constraint parsing
10. **E2E-15** Multi-step replan cascade

If time is limited for demo:
- onboarding
- one food scan
- one recommendation
- one natural-language reject
- one replanned recommendation

That is the minimum complete product story.

---

## 12. Future-Friendly Scenario Extensions

These are valuable next-step E2E scenarios once the contract expands:

### Extension A — Multi-option recommendation bundle
Validate that one planner response can contain 2-3 meal alternatives ranked by:
- time fit
- taste fit
- pantry fit
- grocery fit

### Extension B — Health-condition-aware planning
Validate that:
- high blood pressure
- diabetes
- high cholesterol

meaningfully influence planning direction and substitutions.

### Extension C — Habit-aware planning
Validate differences between:
- mostly cooks at home
- usually eats outside
- irregular weekday schedule
- batch-prep preference

### Extension D — Meal-level target generation
Validate that backend can estimate:
- daily calorie intake target
- macro targets
- meal-level target direction

from onboarding and goal setup.

---

## 13. Summary

This E2E design reframes testing around the **real user journey**, not just endpoint mechanics.

The system should prove that it can:

- learn who the user is
- understand what food context the user provides
- reason over health, pantry, time, budget, and restrictions
- return a useful meal plan
- accept natural-language feedback
- automatically improve the recommendation in a continuous loop

That is the core hackathon story:

**an AI dietitian that turns real-life food context into daily meal decisions, then keeps improving through natural interaction.**