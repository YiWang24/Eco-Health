# Pages and components

## Routes

| Route | Description |
|-------|-------------|
| `/` | Welcome (Hero, Features, CTA) |
| `/onboarding` | Onboarding form (header/footer from `onboarding/layout.js`) |
| `/dashboard` | Dashboard home (nutrition, quick actions, suggestions, recipes) |
| `/dashboard/scan/fridge` | Fridge scan (boxes, list, summary, tip) |
| `/dashboard/scan/meal` | Meal scan |
| `/dashboard/scan/receipt` | Receipt scan |
| `/dashboard/chat` | Chat |
| `/dashboard/livelarder` | LiveLarder |
| `/dashboard/recipes` | Recipes list (placeholder) |
| `/dashboard/profile` | Profile (placeholder; link to onboarding) |

Optional later: `/login`.

## Components

- **layout/** — Header (variants: welcome / dashboard), Footer, BottomNav
- **ui/** — Icon, Button, EmptyState, LoadingSpinner
- **welcome/** — HeroSection, FeaturesGrid, CtaSection
- **dashboard/** — NutritionCard, QuickActions, SmartSuggestion, RecipeCard
- **onboarding/** — ProgressStepper
- **scan/** — CameraFrame, DetectionBoxOverlay, DetectedIngredientList, FreshnessLegend

## Notes

- New dashboard pages use `dashboard/layout.js` (Header + BottomNav).
- Detection data: see comments in `DetectionBoxOverlay.js` and `DetectedIngredientList.js`.
- Use `<EmptyState />` for empty lists; `<LoadingSpinner />` or button text for loading.
