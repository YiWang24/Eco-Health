# Project structure

Next.js 14 App Router, JavaScript, Tailwind. Single source of truth for repo layout.

## Root

```
├── package.json, next.config.js, tailwind.config.js, postcss.config.js, jsconfig.json
├── .gitignore, README.md, FILE_STRUCTURE.md
├── public/
├── docs/ (STRUCTURE.md, PAGES_AND_COMPONENTS.md, DESIGN.md, FRONTEND_CHECKLIST.md, UI_DESIGN_PHASE_CHECKLIST.md)
└── src/
    ├── app/
    ├── components/
    └── lib/
```

## src/app

| Path | Role |
|------|------|
| `layout.js`, `globals.css` | Root layout and styles |
| `page.js` | Home / welcome |
| `onboarding/layout.js`, `onboarding/page.js` | Onboarding shell and form |
| `dashboard/layout.js`, `dashboard/page.js` | Dashboard shell and home |
| `dashboard/profile/page.js` | Profile (link to onboarding) |
| `dashboard/recipes/page.js`, `dashboard/recipes/[slug]/page.js` | Recipes list and detail |
| `dashboard/chat/page.js` | Chat |
| `dashboard/livelarder/page.js` | LiveLarder |
| `dashboard/scan/fridge/layout.js`, `dashboard/scan/fridge/page.js` | Fridge scan (multi-image, Inventory tab) |
| `dashboard/scan/meal/page.js`, `dashboard/scan/receipt/page.js` | Meal and receipt scan |

## src/components

| Dir | Role |
|-----|------|
| `layout/` | Header, Footer, BottomNav |
| `ui/` | Icon, Button, EmptyState, LoadingSpinner |
| `welcome/` | HeroSection, FeaturesGrid, CtaSection |
| `dashboard/` | NutritionCard, QuickActions, SmartSuggestion, RecipeCard |
| `onboarding/` | ProgressStepper |
| `scan/` | CameraFrame, DetectionBoxOverlay, DetectedIngredientList, FreshnessLegend |

## src/lib

- `constants.js` — APP_NAME, ROUTES

## Conventions

- Path alias: `@/` → `src/`
- Layouts: root → all; `dashboard/layout.js` → all `/dashboard/*`; `onboarding/layout.js` → onboarding
- Prefer server components; use client only when needed (e.g. fridge tab state, BottomNav pathname)
