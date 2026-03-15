# Agentic Dietitian

Next.js (React) frontend for Eco-Health Agentic Dietitian. JavaScript + Tailwind CSS.

## Quick start

```bash
npm install
npm run dev
```

Open http://localhost:3000 (or the port shown).

## Environment

Create `frontend/.env.local` (optional but recommended):

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
# Optional: static bearer token for local debugging
# NEXT_PUBLIC_API_BEARER_TOKEN=
# Optional demo mode (only when backend AUTH_BYPASS_ENABLED=true)
# NEXT_PUBLIC_ALLOW_DEMO_AUTH=true
# NEXT_PUBLIC_DEMO_USER_ID=demo-user
```

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Dev server |
| `npm run build` | Production build |
| `npm run start` | Run production build |
| `npm run lint` | ESLint |

## Layout

- `src/app/` — Routes and layouts
- `src/components/` — Reusable UI
- `src/lib/` — Constants
- `docs/` — Structure, design, checklists

See **`docs/STRUCTURE.md`** and **`FILE_STRUCTURE.md`**.
