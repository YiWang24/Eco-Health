# Agent Layer Placeholder

This directory is reserved for deployment-facing ADK artifacts:

- orchestrator configuration
- tool adapter wrappers
- reflection validator policies
- prompt templates

Implemented runtime workflow code now lives in `backend/app/agents/`:

- `workflow.py` (ADK orchestrator + fallback)
- `tools.py` (tool contracts)
- `reflection.py` (constraint validator)
- `schemas.py` (typed ADK output contract)

See `/docs/agents/agent-spec.md` for architecture details.
