# Task 004 — Final UI Visual Polish

## Goal

Apply the final verified visual-polish corrections to the current `feat/ui-foundation` dashboard after desktop screenshot review.

This task improves visual hierarchy and financial semantics. It does not add product features, backend integration, live data, OpenAI, recommendations, authentication, or new dependencies.

Read completely before editing:

```text
docs/ui-foundation.md
docs/agent-tasks/002-ui-foundation.md
docs/agent-tasks/003-ui-qa-corrections.md
```

## Branch and safety rules

- Work only on `feat/ui-foundation`.
- Pull the latest remote branch before editing.
- Do not modify `main`.
- Do not merge.
- Do not force-push.
- Do not modify backend files, migrations, Docker, or CI.
- Do not add packages.
- Preserve all Task 003 accessibility, privacy, loading, error, responsive, and reconciliation behavior.

## 1. Remove the empty desktop/tablet top bar

The current `TopBar` contains meaningful content only on mobile. At `md` and larger it renders an empty 72 px white strip above every page.

Update the layout so:

- `TopBar` remains visible below `md` for the hamburger and mobile wordmark.
- `TopBar` is not rendered visually at `md` and larger.
- The main page content starts at the top of the application area on tablet and desktop.
- The page header should align naturally with the sidebar wordmark region.
- Do not remove the mobile menu behavior.
- Do not add a fake desktop profile, notification, or search bar merely to fill space.

Preferred implementation: make the TopBar root mobile-only with `md:hidden`, while preserving its current mobile height and behavior.

Manually verify that loading and error routes do not gain unexpected blank space.

## 2. Correct financial colour and sign semantics

The screenshot currently renders all positive metric values in green with a leading `+`. This incorrectly presents invested principal and cash reserve as gains.

Update `MetricCard` to support explicit semantic display modes, for example:

```ts
tone?: "neutral" | "signed"
```

Rules:

- Default must be `neutral`.
- Neutral metrics:
  - use primary text colour,
  - show formatted money without `+` or `−` sign logic,
  - must not turn green merely because the number is above zero.
- Signed metrics:
  - positive values use `+` and positive colour,
  - negative values use `−` and negative colour,
  - zero values use neutral colour.
- Privacy masking behavior must remain unchanged.

Apply on the dashboard:

```text
Yatırılan ana para                 neutral
Gerçekleşmemiş kâr/zarar          signed
Gerçekleşmiş kâr/zarar            signed
Nakit ve kısa vadeli rezerv       neutral
```

Do not infer financial meaning from the numeric sign inside a generic UI component.

## 3. Remove duplicate period-control groups

The same `1A / 3A / 6A / YBB / 1Y / Tümü` interactive controls currently appear in both the hero and the performance-card header.

Design decision:

- Keep the interactive period controls in `PortfolioValueHero` as the single global dashboard-period control.
- Remove the duplicate interactive button group from `PerformanceChart`.
- The performance-card header must show the currently selected period as a small, non-interactive neutral label or badge, for example:

```text
Seçili dönem: Tümü
```

- The chart must still update immediately when the hero period changes.
- Preserve controlled state in `DashboardContent`.
- Do not create a second local period state.
- Ensure the hero controls wrap or scroll safely on narrow mobile screens without causing page overflow.

## 4. Repair chart-axis formatting and layout

The current Y-axis text is produced with string replacement and slicing, which creates labels such as:

```text
428.650.
```

This is visually incorrect and fragile.

Create a centralized compact-money formatter in:

```text
apps/web/src/lib/formatters.ts
```

Requirements:

- Use `Intl.NumberFormat` with `tr-TR`.
- Use TRY currency.
- Use compact notation or another deterministic compact Turkish representation.
- Maximum one fractional digit.
- Do not manually replace punctuation or slice formatted strings.
- Example acceptable presentation:

```text
₺390,2 B
₺409,4 B
₺428,7 B
```

Update `PerformanceChart`:

- Use the centralized formatter for Y-axis labels.
- Reserve a dedicated right gutter for labels so they do not overlap the plot or clip.
- Use separate plot-left and plot-right values instead of one shared generic padding when useful.
- Keep grid lines inside the plot area.
- Keep tooltips using the existing full-money formatter.
- Preserve privacy masking and accessible summaries.
- Do not add a chart dependency.

## 5. Improve allocation-card composition

The donut center is currently visually empty.

Add a restrained center label inside the donut:

```text
5
kategori
```

Rules:

- Derive the count from `items.length`.
- Use primary text for the number and tertiary text for `kategori`.
- Keep it visible in privacy mode because it is not monetary information.
- Do not repeat total portfolio money in the center.
- Preserve the accessible distribution list and screen-reader summary.

## 6. Make the table action column visible

The holdings table has a visually blank final header even though it contains `Detay` links.

Update the final `<th>`:

- Visible label: `Detay`
- Right aligned.
- Keep `scope="col"`.
- Preserve the descriptive link `aria-label` for each holding.
- Keep rows non-clickable.

Do not rename the data column or remove table semantics.

## 7. Balance the bottom dashboard cards

On desktop, `Son İşlemler` is substantially taller than `Portföy gözlemleri`, leaving the right column visually unfinished.

Update the region so:

- Both grid children stretch to the same row height.
- `RecentTransactions` root Card uses `h-full`.
- `PortfolioObservations` root Card uses `h-full flex flex-col`.
- The deterministic-observation disclaimer sits at the bottom using `mt-auto` with appropriate top padding.
- Do not invent extra observations to fill space.
- Do not increase card shadows.

Typography polish:

- Increase the observation disclaimer from 10 px to the standard 12 px supporting-text size.
- Increase the final `Demo veri` page disclaimer from 10 px to 12 px.
- Preserve tertiary contrast and the investment-advice disclaimer wording.

## 8. Preserve known-good visual behavior

Do not regress:

- 248 px desktop sidebar,
- 80 px tablet rail,
- mobile bottom navigation,
- dashboard-wide privacy masking,
- stale-data status,
- explicit transaction navigation,
- loading and error states,
- 44 px touch targets,
- visible keyboard focus,
- semantic colour tokens,
- internal demo-data reconciliation.

The black circular `N` shown at the bottom-left during local development is the Next.js development indicator. Do not alter the application layout to accommodate it; it is not production UI.

## Validation

Run from repository root:

```bash
git diff --check
pnpm install --frozen-lockfile
pnpm lint
pnpm typecheck
pnpm build
```

Manual checks:

- 390 px mobile viewport
- 768 px tablet viewport
- 1024 px compact desktop viewport
- 1440 px desktop viewport
- no empty desktop/tablet top strip
- page header aligns correctly beside the sidebar
- principal and cash metrics are neutral, not green and not prefixed with `+`
- P/L metrics retain signed semantic colours
- only one interactive period-control group exists
- chart axis has valid compact TRY labels with no trailing punctuation
- donut center shows category count
- holdings action header is visible
- bottom cards share equal height
- privacy mode, period filtering, and navigation still work
- no horizontal overflow

## Commit and push

Stage only files required by this task.

Commit with this exact message:

```text
style: polish dashboard visual hierarchy
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
- confirmation of each visual correction,
- any requirement not completed and why,
- final `git status`.
