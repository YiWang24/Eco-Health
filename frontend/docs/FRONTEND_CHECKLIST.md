# Frontend checklist

## Done

- Pages and routes (welcome, onboarding, dashboard, scans, chat, livelarder, recipes, profile)
- Layout and nav (Header, Footer, BottomNav)
- Fridge scan (boxes, list, summary, tip)
- Design system (primary, dark, Tailwind, Material Icons)
- Component split (ui + feature components)

## To do (priority)

### 1. API contract (first)

Align with backend: URL, method, request/response shape. Document in e.g. `docs/API.md`.

| Feature | Frontend calls | Frontend does |
|---------|----------------|---------------|
| Auth | Login, user info | Store token, send in header |
| Onboarding | Save/update profile | Submit form, redirect on success |
| Fridge scan | Upload image → detections + list | Pass to DetectionBoxOverlay, DetectedIngredientList |
| Meal / receipt scan | Upload → result | Show result list |
| Chat | Send message → reply | Show 2–3 meal options (recipe, steps, nutrition, list) |
| Recipe detail | Get by ID | Show steps, nutrition, substitutions, list |

Use mock data until APIs exist; then swap in `api.js` (or `api/auth.js`, `api/scan.js`, `api/chat.js`).

### 2. Replace mock with API

- Add `src/lib/api.js` (or split by domain). All requests from here; base URL from env.
- Fridge: on image select → call API → pass response to overlay and list. Same idea for meal/receipt and chat.
- Agree on shapes (e.g. box as `{ left, top, width, height }` %; item: `name`, `status`, `statusText`).

### 3. Auth (if required)

- Send token in header; redirect to login/onboarding when unauth.
- Login page: call login API, store token, redirect.

### 4. Forms

- Onboarding: submit to profile API; validate required fields; show loading on submit and disable button.

### 5. Image upload

- All three scans: file input or camera; preview with `URL.createObjectURL`; upload via FormData; loading then success/error message.

### 6. Loading and errors

- Loading on every async action (button or area).
- On error: toast or inline message (e.g. “Failed, retry”).
- Empty state: message + CTA (e.g. “Scan fridge”) instead of blank.

### 7. Chat / recommendations

- Render 2–3 meal cards from API (recipe, steps, nutrition, substitutions, alerts, list). Adapt to streamed vs structured response.

### 8. Responsive and a11y

- Test mobile/tablet/desktop; fix breakpoints.
- Labels and aria-labels; keyboard focus order; contrast.

### 9. Env and CORS

- `.env.local`: e.g. `NEXT_PUBLIC_API_BASE_URL`. Use in api layer.
- CORS: backend allows frontend origin; don’t disable browser security.

## Not frontend

- Agent logic, RAG, recipe DB, nutrition calc, spoilage prediction
- Auth implementation (e.g. Cognito) — frontend only calls login and sends token

## Tips

- Define API shape before building UI.
- Use mocks first, then swap to real API.
- Handle loading and error for every request.
