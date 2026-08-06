# Task 003 — UI QA Corrections

## Goal

Correct the verified accessibility, interaction, privacy, responsive, state-management, and demo-data defects in the current `feat/ui-foundation` implementation.

This is a focused correction task. It is not permission to redesign the dashboard, add backend integration, add live market data, add OpenAI, add recommendations, or change the product hierarchy.

Read these files completely before editing:

```text
docs/ui-foundation.md
docs/agent-tasks/002-ui-foundation.md
```

## Branch and safety rules

- Work only on `feat/ui-foundation`.
- Pull the latest remote branch before editing.
- Do not modify `main`.
- Do not merge a pull request.
- Do not force-push.
- Do not modify backend models, migrations, API routes, Docker files, or CI logic.
- Do not read or expose `.env` values.
- Do not install a UI framework, chart library, icon library, or state-management package.
- Reuse the existing semantic CSS tokens and component structure.

## 1. Repair accessibility and semantic defects

### 1.1 SectionHeader IDs

Fix `apps/web/src/components/ui/section-header.tsx`.

- Destructure the existing `id` prop.
- Forward it to the rendered `<h2 id={id}>`.
- Do not remove the surrounding `aria-labelledby` attributes from dashboard sections.

### 1.2 Card semantics

Fix `apps/web/src/components/ui/card.tsx`.

- When `onClick` exists and the component renders a `<button>`, set `type="button"`.
- The `interactive` visual treatment must only imply interaction when an actual interaction exists.
- A non-clickable card must not use `cursor-pointer` or hover styling that promises navigation.

Fix `HoldingCard` accordingly:

- Remove `variant="interactive"` while the card itself is not clickable.
- Keep an explicit, accessible detail link.
- Replace the raw arrow in `Detay →` with a consistent SVG icon from the local icon set.

### 1.3 Consistent transaction icons

Update the local SVG icon set under `apps/web/src/components/ui/icons.tsx`.

Add any missing icons needed for:

- buy,
- sell,
- deposit,
- withdrawal,
- dividend/interest,
- fee/tax,
- right-arrow/detail.

Then replace raw Unicode glyphs in `RecentTransactions` and `HoldingCard`.

Do not use emoji, Unicode arrows, decorative stars, or text symbols as UI icons.

### 1.4 Functional action links

The two visible `İşlem ekle` controls must perform a real navigation action.

- Add a reusable `ButtonLink` primitive, or extend the existing button system without duplicating visual classes.
- Both dashboard `İşlem ekle` actions must navigate to:

```text
/transactions?intent=create
```

- Do not add a fake modal.
- Preserve the existing primary button visual treatment and accessible focus state.

## 2. Make privacy mode dashboard-wide

The current privacy state inside `PortfolioValueHero` is insufficient.

Create a client-side dashboard orchestration component, for example:

```text
apps/web/src/components/dashboard/dashboard-content.tsx
```

The exact filename may differ, but the architecture must follow these rules:

- `app/page.tsx` remains a thin composition entry.
- One client component owns:
  - selected period,
  - privacy masked/unmasked state.
- `PortfolioValueHero` becomes controlled through props. It must not own isolated privacy or period state.
- Pass the masking state to every dashboard component that exposes monetary information.

When privacy mode is active:

- mask total portfolio value,
- daily and total change values,
- all metric-card money values,
- holdings market value, cost, current price, and P/L values,
- allocation monetary values,
- recent transaction monetary values,
- performance-chart monetary labels and accessible monetary summaries.

Percentages and non-monetary labels may remain visible.

Use one centralized masking helper or rendering primitive. Do not scatter inconsistent strings through components.

Preferred visible mask:

```text
₺••••••
```

For chart privacy mode, do not expose monetary axis labels or screen-reader monetary summaries. The chart may retain its shape, but it must show a clear `Gizlilik modu açık` label.

## 3. Make period selection real

The current period controls must not be cosmetic.

Create typed period-return mock data in `apps/web/src/data/dashboard.ts`.

Use these explicit demo values:

```text
1A   amount: 3_850.10    percentage: 0.91
3A   amount: 15_449.60   percentage: 3.74
6A   amount: 33_220.20   percentage: 8.40
YBB  amount: 38_420.70   percentage: 9.85
1Y   amount: 38_420.70   percentage: 9.85
ALL  amount: 38_420.70   percentage: 9.85
```

Requirements:

- Store these values as typed mock data, not inline JSX constants.
- The hero total-return display must use the selected period's stored amount and percentage.
- The performance chart must receive a filtered point set based on the selected period.
- Use the latest demo point (`2026-08-04`) as the reference date.
- Period cutoffs:
  - `1A`: `2026-07-04`
  - `3A`: `2026-05-04`
  - `6A`: `2026-02-04`
  - `YBB`: `2026-01-01`
  - `1Y`: `2025-08-04`
  - `ALL`: no cutoff
- Filtering belongs in a typed helper, not inside SVG rendering code.
- Keep at least two points available to the chart; use a deterministic fallback if a future dataset is too short.

## 4. Add production-quality loading and error states

Create reusable primitives:

```text
apps/web/src/components/ui/skeleton.tsx
apps/web/src/components/ui/spinner.tsx
apps/web/src/components/ui/error-state.tsx
```

### Skeleton

- Use semantic tokens.
- Use restrained motion.
- Respect `prefers-reduced-motion`.
- Support className composition without `any`.

### Spinner

- Include an accessible label strategy.
- Do not rely on colour alone.

### ErrorState

Must support:

- title,
- description,
- optional retry action,
- optional secondary navigation action.

Add:

```text
apps/web/src/app/loading.tsx
apps/web/src/app/error.tsx
```

Requirements:

- `loading.tsx` must resemble the dashboard layout rather than showing a centered generic spinner only.
- Include skeletons for header, hero, metric cards, chart/allocation, and at least one lower content region.
- `error.tsx` must be a client component and use the provided `reset()` function.
- Wrap the error presentation in the existing AppShell so navigation remains available.

## 5. Add the portfolio selector

Create an accessible static portfolio selector in the dashboard header.

Requirements:

- Native `<select>` is acceptable and preferred for this milestone.
- Visible current option:

```text
Konsolide portföy
```

- Include an accessible label.
- Position it before the `İşlem ekle` action on tablet and desktop.
- On narrow mobile widths, allow the header actions to wrap without horizontal overflow.
- Do not invent multiple accounts or backend state.

## 6. Improve responsive navigation semantics

Update sidebar navigation:

- Tablet-rail touch targets must be at least 44×44 px.
- Disabled `Analiz` and `İzleme Listesi` entries must expose `Yakında` context even when collapsed.
- Use:
  - an accessible `aria-label` containing `Yakında`,
  - a small visual status dot or lock indicator,
  - a native `title` only as supplemental desktop hover help.
- Do not make disabled entries focusable or navigable.
- Add pressed states to Button, ButtonLink, and IconButton using restrained `active:` feedback.
- Do not use large scale or bounce effects.

## 7. Reconcile demo portfolio data

Replace inconsistent holding values with one internally coherent dataset.

The allocation totals and holding market values must reconcile exactly to:

```text
Total portfolio value: 428_650.40
Unrealized P/L:        31_780.20
Daily change:           2_184.30
```

Use these exact holding market values:

```text
BGP Para Piyasası Fonu   130_625.68
Altın Fonu                51_805.12
Fiziki Altın (Gram)       98_520.60
USD Döviz                 65_200.30
Nakit Rezerv (TRY)        54_200.00
Hisse Senedi              28_298.70
```

Use these exact total P/L values:

```text
BGP Para Piyasası Fonu   10_000.00
Altın Fonu                6_000.00
Fiziki Altın (Gram)       8_500.00
USD Döviz                 3_280.20
Nakit Rezerv (TRY)            0.00
Hisse Senedi              4_000.00
```

Use these exact daily-change values:

```text
BGP Para Piyasası Fonu      125.42
Altın Fonu                   320.50
Fiziki Altın (Gram)          850.04
USD Döviz                    288.34
Nakit Rezerv (TRY)             0.00
Hisse Senedi                 600.00
```

Use these quantities and corresponding precomputed prices/costs:

```text
BGP
quantity: 10_000
averageCost: 12.062568
currentPrice: 13.062568

Altın Fonu
quantity: 800
averageCost: 57.2564
currentPrice: 64.7564

Fiziki Altın
quantity: 30
averageCost: 3000.68666667
currentPrice: 3284.02

USD
quantity: 1_800
averageCost: 34.40005556
currentPrice: 36.22238889

Nakit
quantity: 54_200
averageCost: 1
currentPrice: 1

Hisse
quantity: 1_000
averageCost: 24.2987
currentPrice: 28.2987
```

Requirements:

- Rename the final instrument from `Hisse Senedi Fonu` to `Hisse Senedi`.
- Its category must be `Hisse`, not `Fon`.
- Allocation remains:
  - Fon: 182_430.80
  - Değerli Maden: 98_520.60
  - Döviz: 65_200.30
  - Mevduat / Nakit: 54_200.00
  - Hisse: 28_298.70
- Mark `Fiziki Altın (Gram)` as `dataFreshness: "stale"` with an appropriately old demo timestamp.
- Preserve the explicit `Demo veri` disclaimer.
- Do not calculate accounting values in React components.

## 8. Reuse shared empty states

Refactor empty branches in:

- HoldingsTable,
- HoldingCard collection region if applicable,
- RecentTransactions,
- AllocationBreakdown,
- PortfolioObservations.

Use the existing `EmptyState` primitive instead of separate one-off centered paragraphs.

Keep empty-state copy concise and specific to the region.

## 9. DataFreshnessBadge composition

Refactor `DataFreshnessBadge` so it composes the existing Badge primitive rather than recreating an independent badge system.

Preferred location:

```text
apps/web/src/components/ui/data-freshness-badge.tsx
```

- Update imports everywhere.
- Preserve all four variants: live, delayed, eod, stale.
- Preserve icon + text semantics.
- Do not duplicate semantic colour mappings unnecessarily.

## 10. Holdings-row design decision

Do **not** turn semantic `<tr>` elements into pseudo-links with `role="link"`, `tabIndex`, and keyboard handlers. That pattern weakens table semantics and creates nested-interaction ambiguity.

For this milestone:

- Keep rows non-clickable.
- Keep one clear accessible `Detay` link per holding.
- Ensure the detail link has a descriptive accessible name such as:

```text
BGP Para Piyasası Fonu detayını aç
```

Update `docs/ui-foundation.md` to clarify that holding rows expose an explicit detail action rather than requiring the entire table row to be clickable.

## Validation

Run from repository root:

```bash
git diff --check
pnpm install --frozen-lockfile
pnpm lint
pnpm typecheck
pnpm build
```

Then inspect:

```bash
git diff --stat
git diff
```

Manual checks at minimum:

- 390 px mobile viewport
- 768 px tablet viewport
- 1024 px tablet/compact desktop viewport
- 1440 px desktop viewport
- privacy toggle masks all dashboard money values
- each period changes both hero return and chart dataset
- no fixed mobile-navigation overlap
- no horizontal page overflow
- keyboard focus is visible
- `İşlem ekle` controls navigate correctly
- loading and error states render inside AppShell

## Commit and push

Stage only files required by this task.

Commit with this exact message:

```text
fix: correct UI foundation QA findings
```

Push normally to:

```text
origin feat/ui-foundation
```

Do not merge.

## Report

Return:

- commit SHA,
- exact changed files,
- validation results,
- manual viewport results,
- any requirement not completed and why,
- final `git status`,
- GitHub Actions run URL if a pull request exists.
