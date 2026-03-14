# UI design phase checklist

Goal: demo-ready UI without real APIs. Then move to API integration.

## 1. Consistency

- Colors, font, radius, spacing: one system (tailwind theme; Icon only).
- Dark mode: `dark:` and root `class="dark"` work.
- Buttons/cards: a few clear types (primary, secondary, etc.).

## 2. Pages and flow

- Welcome: CTA to onboarding/login; footer links (can be `#` for now).
- Onboarding: clear steps (Step 1/4); required fields marked; visible next/submit.
- Dashboard: nutrition, quick actions, suggestions, recipes; bottom nav covers main entry points.
- Scans: fridge (boxes, list, summary, tip); meal (confirm action); receipt (list + main action).
- Chat: sample message + input; space for 2–3 meal cards.
- LiveLarder: image + status labels + update.

Walk the journey (welcome → onboarding → dashboard → scan/chat); fix dead links or blank screens.

## 3. States

- Default: each block has a clear “with data” look.
- Loading: skeleton or spinner; button shows “Loading…” or spinner.
- Empty: short copy + CTA (e.g. “Scan fridge”).
- Error: inline or toast + optional “Retry”.
- Disabled: submit disabled or visually muted when form incomplete.

## 4. Responsive

- Mobile: fixed bottom nav, scrollable lists, modals/drawers fit.
- Tablet: two-column (e.g. scan) works at mid width.
- Desktop: content not too wide (max-w); chat readable.

Test with dev tools or real devices; adjust breakpoints.

## 5. Accessibility

- Tab order and visible focus.
- Every input has label or aria-label; icon buttons have aria-label.
- Contrast sufficient.

## 6. Deliverables

- Page list (routes + names; done / todo).
- Component list (shared components and where used).
- Design doc (colors, type, spacing, button usage) — e.g. DESIGN.md.
- Optional: screenshots or short video for stakeholders.

## 7. Skip for now

- Real login/API, token, upload to backend, streamed chat, heavy perf work.

## 8. Self-check order

1. Walk all pages; fix missing or broken links.
2. Unify button/card/input styles.
3. Add loading, empty, error UI where needed.
4. Check responsive; fix layout.
5. Tab + aria-label + form labels.
6. Update page list + design doc (and optional screenshots).

## 9. Last check (summary)

| Area | Status |
|------|--------|
| Consistency | OK — theme, Icon, focus-visible |
| Pages and flow | OK — CTAs, no dead links |
| States | OK — EmptyState, LoadingSpinner |
| Responsive | OK — nav, max-w, lg grid; verify on device |
| A11y | OK — focus, labels, aria-label |
| Deliverables | OK — PAGES_AND_COMPONENTS.md, DESIGN.md |

Next: device pass; finish onboarding id/htmlFor; add loading on submit/upload when wiring API.
