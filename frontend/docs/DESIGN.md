# Design (UI)

One-page reference: colors, type, spacing, buttons, forms.

## Colors

| Use | Tailwind |
|-----|----------|
| Primary | `primary`, `bg-primary`, `text-primary` (#4cae4f) |
| Background | `background-light`, `background-dark` |
| Warning / expiring | `orange-400`, `orange-500` |
| Critical / expired | `red-500`, `red-600` |

Dark mode: `dark:` prefix; toggle via root `class="dark"`.

## Type

- Font: Inter (`font-display` in tailwind.config).
- Headings: `text-2xl font-black`, `text-lg font-bold`, `text-xl font-bold`.
- Body: `text-sm`, `text-base`; secondary: `text-xs`, `text-slate-500`.

## Spacing and radius

- Radius: `rounded-lg` (inputs, buttons), `rounded-xl` (cards), `rounded-2xl` (sections), `rounded-full` (pills, avatars).
- Padding: `p-4`–`p-8`; gap: `gap-2`–`gap-6`; page: `px-6 lg:px-20`.

## Buttons

- Primary: `bg-primary text-white font-bold`; hover: opacity or scale.
- Secondary: `border-2 border-slate-200`; hover: `bg-slate-50`.
- Icon-only: add `aria-label`.
- Disabled: `disabled` + `opacity-60` or `cursor-not-allowed`.
- Loading: `<LoadingSpinner />` or “Loading…” and `disabled`.

## Forms

- Every input/select has a `<label>` or `aria-label`; prefer `htmlFor` + `id`.
- Inputs: `rounded-lg border border-slate-200 p-3 focus:ring-primary focus:border-primary`.

## Cards and lists

- Card: `rounded-2xl border border-slate-100 dark:border-slate-700 bg-white dark:bg-slate-800`, padding `p-4`–`p-8`.
- List items: consistent radius and hover.

## Accessibility

- Focus: `:focus-visible` 2px primary outline (globals.css).
- Icon buttons: require `aria-label`.
- Forms: associate labels and inputs; link errors to inputs.

## Responsive

- Mobile-first; breakpoints `sm`, `md`, `lg`.
- Bottom nav: fixed, `max-w-[640px]` centered.
- Two-column (e.g. scan): `lg:grid-cols-12`; single column on small screens.
