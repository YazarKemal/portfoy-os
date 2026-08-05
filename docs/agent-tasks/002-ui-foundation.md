# Task 002 — UI Foundation and Portfolio Dashboard

## Goal

Implement the first production-quality UI layer for Portföy OS on `feat/ui-foundation`.

The implementation must follow `docs/ui-foundation.md` as the binding UI/UX contract. This task does not grant permission to redesign the information architecture, terminology, colour semantics, dashboard order, or product boundaries.

## Branch and safety rules

- Work only on `feat/ui-foundation`.
- Do not modify `main` directly.
- Do not merge a pull request.
- Do not force-push.
- Do not edit backend models, migrations, API routes, Docker configuration, or CI logic unless a frontend validation command is genuinely broken by this task.
- Do not add OpenAI integration, live market data, authentication, automatic trading, recommendations, or brokerage connectivity.
- Do not expose or read `.env` values in frontend code.

## Current frontend state

The frontend currently contains only:

- `apps/web/src/app/layout.tsx`
- `apps/web/src/app/page.tsx`
- `apps/web/src/app/globals.css`

Tailwind CSS 4 is available. No component library, icon library, or chart library is installed.

## Required implementation

### 1. Semantic global styles

Update `apps/web/src/app/globals.css`.

Requirements:

- Keep `@import "tailwindcss";`.
- Add all semantic CSS custom properties defined in `docs/ui-foundation.md`.
- Add canvas, surface, text, border, state, chart, radius, shadow, focus, spacing, and motion tokens.
- Apply a safe system font stack. Do not fetch a web font over the network.
- Apply `tabular-nums` behaviour to financial value utility classes/components.
- Add a visible `:focus-visible` treatment.
- Add base body/background/text styles.
- Add reduced-motion handling.
- Do not hard-code visual hex colours inside JSX once semantic tokens exist.

### 2. Typed mock data and formatting

Create:

```text
apps/web/src/types/dashboard.ts
apps/web/src/data/dashboard.ts
apps/web/src/lib/formatters.ts
```

Requirements:

- Define explicit types for dashboard metrics, performance points, allocation items, holdings, transactions, data freshness, and observations.
- Store all mock values in `data/dashboard.ts`; do not scatter financial values through components.
- Mark the dataset as `Demo veri`.
- Use the scenario values from `docs/ui-foundation.md`.
- Use generic instrument names, not promoted real investment recommendations.
- Create centralized `tr-TR` formatters for money, percentages, quantities, dates, and timestamps.
- Formatting utilities may format prepared numbers but must not calculate portfolio returns, cost basis, or accounting results.
- Do not use `any`.

### 3. Shared UI primitives

Create reusable components under:

```text
apps/web/src/components/ui/
```

Minimum components:

```text
button.tsx
card.tsx
badge.tsx
section-header.tsx
empty-state.tsx
inline-alert.tsx
```

Requirements:

- Support the variants needed by the dashboard.
- Use semantic tokens.
- Buttons and interactive controls need focus, hover, disabled, and active states.
- Icon-only buttons require an accessible label.
- Do not install a full UI framework.

### 4. Icon system

Create one local icon component/module, for example:

```text
apps/web/src/components/ui/icons.tsx
```

Requirements:

- Use a small consistent set of inline SVG icons.
- Include only icons required by the shell/dashboard.
- Icons use `currentColor`.
- Decorative icons use `aria-hidden`.
- Do not use emoji as UI icons.
- Do not install an icon dependency in this task.

### 5. Responsive application shell

Create components under:

```text
apps/web/src/components/layout/
```

Minimum structure:

```text
app-shell.tsx
sidebar-navigation.tsx
mobile-navigation.tsx
top-bar.tsx
page-header.tsx
```

Requirements:

- Desktop sidebar width: 248px.
- Tablet collapsed rail: 80px.
- Mobile uses top app bar and bottom navigation.
- Primary destinations:
  - Genel Bakış
  - Portföyüm
  - İşlemler
  - Analiz (`Yakında`, disabled)
  - İzleme Listesi (`Yakında`, disabled)
  - Veri Durumu
- Secondary destination: Ayarlar.
- Active navigation must be programmatically exposed.
- Disabled destinations must not navigate.
- Desktop/sidebar and mobile navigation must not render simultaneously at the same viewport size.
- No horizontal page scrolling.
- Use `use client` only in components that require pathname or local interaction state.

### 6. Dashboard components

Create components under:

```text
apps/web/src/components/dashboard/
```

Minimum components:

```text
portfolio-value-hero.tsx
metric-card.tsx
performance-chart.tsx
allocation-breakdown.tsx
holdings-table.tsx
holding-card.tsx
recent-transactions.tsx
portfolio-observations.tsx
data-freshness-badge.tsx
```

Requirements:

#### Portfolio hero

- Total portfolio value.
- Daily change amount and percentage.
- Total return amount and percentage.
- Period controls: `1A`, `3A`, `6A`, `YBB`, `1Y`, `Tümü`.
- Last calculation time.
- Privacy toggle that masks monetary values across the dashboard.
- Privacy state may be local component state; do not send it anywhere.

#### Metrics

Show:

- Yatırılan ana para
- Gerçekleşmemiş kâr/zarar
- Gerçekleşmiş kâr/zarar
- Nakit ve kısa vadeli rezerv

#### Performance chart

- Use accessible inline SVG or CSS; do not add a chart dependency.
- Render the mock performance series.
- Include an accessible text summary.
- Provide a basic hover/focus-independent legend/description.
- The chart is presentational and performs no financial calculation.

#### Allocation

- Use a restrained donut or segmented visualization without a dependency.
- Pair the visualization with a labelled list.
- Show value and percentage.

#### Holdings

Desktop/tablet:

- Semantic table with caption and headers.
- Columns from the UI contract.
- Right-align numeric fields.
- Show explicit signs and data freshness.

Mobile:

- Use `HoldingCard` rather than squeezing the full table.

#### Recent transactions

- Show five items.
- Use Turkish transaction labels.
- Include `Tüm işlemleri gör` and `İşlem ekle` controls.

#### Observations

- Label: `Portföy gözlemleri`.
- Use deterministic demo observations only.
- Do not label this as AI, advice, or recommendation.

### 7. Dashboard page

Replace `apps/web/src/app/page.tsx` placeholder with the complete dashboard.

Required order:

1. Page header
2. Portfolio value hero
3. Four metric cards
4. Performance + allocation
5. Holdings
6. Recent transactions + portfolio observations

Use the responsive rules from `docs/ui-foundation.md`.

### 8. Root layout metadata

Update `apps/web/src/app/layout.tsx` only as necessary.

Requirements:

- Keep `lang="tr"`.
- Preserve or improve the existing title/description.
- Add body classes needed for the semantic canvas and typography.
- Do not add an external font fetch.

### 9. Route placeholders

Create lightweight shell-compatible pages for:

```text
apps/web/src/app/portfolio/page.tsx
apps/web/src/app/transactions/page.tsx
apps/web/src/app/data-status/page.tsx
apps/web/src/app/settings/page.tsx
```

Requirements:

- Reuse the application shell.
- Use a clear page title and an intentional empty/coming-next state.
- Do not implement backend integration.
- Do not create active pages for disabled `Analiz` or `İzleme Listesi` yet.

### 10. State examples

The UI Foundation must visibly support or contain reusable components for:

- loading/skeleton,
- empty,
- stale data,
- partial data,
- error,
- ready.

The main demo dashboard should be in ready state while showing at least one stale-data badge. Empty/error examples can live in route placeholders or reusable components.

## Visual constraints

- Professional Türkiye-focused fintech aesthetic.
- Light theme only for this milestone, but semantic tokens must permit future theming.
- No glassmorphism.
- No neon or crypto-terminal style.
- No large decorative gradients.
- No stock photography.
- No decorative 3D illustrations.
- Standard cards rely on borders more than shadows.
- Use brand blue for interaction, not for every surface.
- Reserve green/red primarily for financial direction and status.

## Accessibility acceptance criteria

- Keyboard focus is visible.
- Touch targets are at least 44×44px where applicable.
- Active navigation uses `aria-current="page"`.
- Disabled destinations expose disabled semantics.
- Data tables use semantic markup.
- Charts have accessible text summaries.
- Colour is never the only gain/loss indicator.
- Buttons have explicit labels.
- No heading-level skips in the dashboard hierarchy.

## Responsive acceptance criteria

Visually inspect at minimum:

```text
360x800
390x844
768x1024
1024x768
1280x800
1440x900
1920x1080
```

There must be no horizontal page scroll.

## Dependency policy

- Prefer existing Next.js, React, TypeScript, Tailwind, CSS, and inline SVG.
- Do not install a UI framework.
- Do not install chart or icon packages in this task.
- If a dependency is absolutely necessary, stop and report the justification before changing `package.json` or the lockfile.

## Validation

Run from repository root:

```bash
pnpm install --frozen-lockfile
pnpm lint
pnpm typecheck
pnpm build
git diff --check
```

Also inspect:

```bash
git diff --stat
git diff
git status --short
```

## Commit and push

Stage only files required by Task 002.

Run:

```bash
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
```

Commit with:

```text
feat: build UI foundation and portfolio dashboard
```

Push normally to:

```text
origin feat/ui-foundation
```

Do not merge.

## Completion report

Report:

- commit SHA,
- exact changed files,
- components created,
- responsive behaviour implemented,
- accessibility measures,
- validation results,
- final git status,
- new GitHub Actions run URL if a PR/workflow run exists,
- any deliberate deviation from `docs/ui-foundation.md`.

A deviation without explanation is a failure.