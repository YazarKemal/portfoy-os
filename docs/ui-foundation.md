# Portföy OS — UI Foundation Specification

Status: Approved design contract for `feat/ui-foundation`
Owner: ChatGPT UI/UX
Implementation agent role: translate this contract into Next.js components without changing product hierarchy, visual language, or interaction rules.

## 1. Product Experience Direction

Portföy OS is a Türkiye-focused portfolio tracking and decision-support product. It is not a trading terminal, brokerage interface, or automatic buy/sell system.

The interface must feel:

- trustworthy before impressive,
- premium without decorative excess,
- data-dense without becoming visually noisy,
- understandable to a non-professional investor,
- precise enough for financial records,
- calm during both gains and losses.

The product should sit visually between a modern private-banking dashboard and a focused analytics tool. Avoid crypto-dashboard aesthetics, neon gradients, glassmorphism, excessive shadows, market-ticker clutter, and gamified profit imagery.

### Experience principles

1. **Position before performance**
   The user must first understand what they own, how much it is worth, and how current the data is.

2. **Context before recommendation**
   Future analysis modules may present candidates, but every candidate must expose risk, data freshness, portfolio role, and reasoning.

3. **Numbers are primary content**
   Typography, spacing, alignment, and tabular numerals must make financial values easy to compare.

4. **No silent financial mutations**
   Creating, editing, importing, or interpreting a transaction must always end with an explicit review/confirmation step.

5. **Data provenance is visible**
   Market time, observed time, source/provider, and latency state must be available wherever price-derived values appear.

6. **Colour never carries meaning alone**
   Positive/negative/warning states also use signs, labels, or icons.

## 2. Information Architecture

### Primary navigation

1. **Genel Bakış** — `/`
   - total portfolio value,
   - daily and total change,
   - performance,
   - allocation,
   - recent activity,
   - data freshness,
   - high-level portfolio observations.

2. **Portföyüm** — `/portfolio`
   - holdings,
   - accounts,
   - asset details,
   - position cost and value,
   - realized/unrealized results.

3. **İşlemler** — `/transactions`
   - transaction history,
   - buy/sell/deposit/withdrawal/interest/dividend/fee/tax records,
   - add transaction,
   - future CSV import.

4. **Analiz** — `/analysis`
   - future fund, metal, FX, and instrument analysis,
   - candidate scoring,
   - comparisons,
   - portfolio concentration and risk observations.
   - In UI Foundation this item may appear as a disabled `Yakında` destination; do not invent live analysis.

5. **İzleme Listesi** — `/watchlist`
   - user-selected instruments,
   - observation status,
   - future candidate follow-up.
   - In UI Foundation this may be a disabled `Yakında` destination.

6. **Veri Durumu** — `/data-status`
   - source/provider health,
   - last successful update,
   - latency classification,
   - partial outage or stale data details.

### Secondary navigation

- **Ayarlar** — `/settings`
- **Yardım ve yöntem** — future documentation surface
- Account/profile control

### Navigation naming rules

- Use Turkish labels in the UI.
- Prefer `Analiz` over `Öneriler` because the product supports decisions rather than issuing commands.
- Prefer `İşlem ekle` over `Al/Sat` because the system records more than market trades.
- Never label an automated action as if the system executed a brokerage order.

## 3. Application Shell

### Desktop — 1280 px and above

- Fixed left sidebar: `248px` wide.
- Top bar inside content region: `72px` high.
- Main content max width: `1600px`.
- Main page horizontal padding: `32px` at standard desktop, `40px` above 1440 px.
- Content grid: 12 columns, `24px` gutters.
- Sidebar remains visually quiet; the dashboard content carries hierarchy.

Sidebar anatomy:

1. Portföy OS wordmark and compact symbol.
2. Primary navigation.
3. Optional `Yakında` badge for unavailable modules.
4. Bottom section: data-health shortcut, settings, profile.

### Tablet — 768–1279 px

- Collapsed rail sidebar: `80px`.
- Icon labels exposed with tooltip and accessible name.
- Main content padding: `24px`.
- Dashboard grid becomes 8 columns.
- Tables may switch to cards when essential columns no longer fit.

### Mobile — below 768 px

- No permanent sidebar.
- Top app bar: product mark, current portfolio/account selector, overflow menu.
- Bottom navigation with a maximum of five entries:
  - Genel Bakış,
  - Portföy,
  - İşlemler,
  - Analiz,
  - Daha Fazla.
- Primary action `İşlem ekle` uses a visible button in the page header or a bottom-sheet trigger; do not use an unlabeled floating plus button.
- Main content padding: `16px`.
- Cards stack in one column.
- Charts preserve labels and do not become decorative miniatures.

## 4. Dashboard Hierarchy

Dashboard order is fixed unless usability testing proves a better sequence.

### 4.1 Page header

Left:

- eyebrow: selected portfolio or consolidated view,
- title: `Genel Bakış`,
- supporting line: current date and data status summary.

Right:

- portfolio/account selector,
- data freshness badge,
- primary `İşlem ekle` button.

### 4.2 Portfolio hero

The hero is the dominant card but must not resemble an advertising banner.

Required content:

- label: `Toplam portföy değeri`,
- primary value,
- daily change in currency and percentage,
- total return in currency and percentage,
- comparison period selector: `1A`, `3A`, `6A`, `YBB`, `1Y`, `Tümü`,
- last calculation timestamp,
- visibility toggle for private values.

The hero uses a neutral dark surface, restrained brand accent, or a light elevated surface. No gradient that compromises number contrast.

### 4.3 Key metrics

Four standard metrics:

1. `Yatırılan ana para`
2. `Gerçekleşmemiş kâr/zarar`
3. `Gerçekleşmiş kâr/zarar`
4. `Nakit ve kısa vadeli rezerv`

Metric cards include:

- label,
- formatted value,
- optional comparison,
- one-line context or definition,
- optional info tooltip.

### 4.4 Performance and allocation

Desktop layout:

- Performance chart: 8 columns.
- Allocation card: 4 columns.

Performance chart requirements:

- line or area chart with restrained fill,
- selectable period,
- portfolio value tooltip,
- optional invested-principal comparison line,
- no misleading truncated axes without disclosure,
- empty state when history is insufficient.

Allocation requirements:

- donut only when category count is manageable,
- always pair chart with a labelled list,
- show category name, value, and percentage,
- group tiny categories into `Diğer` only with drill-down support later,
- support asset classes such as fon, hisse, değerli maden, döviz, mevduat/nakit.

### 4.5 Holdings overview

Desktop uses a data table.

Core columns:

- Varlık,
- Tür,
- Miktar,
- Ortalama maliyet,
- Güncel fiyat,
- Piyasa değeri,
- Günlük değişim,
- Toplam kâr/zarar,
- Veri zamanı.

Rules:

- Asset name is primary; code/provider metadata is secondary.
- Numeric columns align right and use tabular figures.
- The row is clickable but still exposes an accessible `Detay` action.
- Sorting must state active direction.
- Positive and negative results show `+`/`−` signs and labels, not colour alone.
- On mobile, transform each holding into a compact position card showing value, quantity, cost, total result, and freshness.

### 4.6 Recent transactions

Show the latest five records with:

- transaction type icon and label,
- asset/account,
- date,
- quantity or amount,
- total value,
- status when a record needs review.

Actions:

- `Tüm işlemleri gör`,
- `İşlem ekle`.

### 4.7 Portfolio observation card

This is not an AI recommendation card in UI Foundation.

It may show deterministic placeholder observations such as:

- `Portföyünüzün %42'si tek bir varlık sınıfında.`,
- `2 fiyat kaynağı 24 saatten eski.`,
- `Nakit rezerviniz toplam değerin %8'i.`

Use label `Portföy gözlemleri`, not `AI tavsiyesi`.

Future OpenAI output must be visually distinguishable from calculated facts and must expose its source inputs and generation time.

## 5. Design Tokens

All visual values must be represented by semantic CSS custom properties. Components must not hard-code hex values.

### 5.1 Core palette — light theme

```css
:root {
  --color-bg-canvas: #f4f6f8;
  --color-bg-surface: #ffffff;
  --color-bg-subtle: #eef2f5;
  --color-bg-inverse: #111c2e;

  --color-text-primary: #172033;
  --color-text-secondary: #5d6879;
  --color-text-tertiary: #7d8796;
  --color-text-inverse: #f8fafc;

  --color-border-subtle: #e2e7ed;
  --color-border-strong: #cbd3dc;

  --color-brand-primary: #1859c9;
  --color-brand-hover: #1249aa;
  --color-brand-soft: #eaf1ff;

  --color-positive: #087f5b;
  --color-positive-soft: #e8f7f1;
  --color-negative: #c92a2a;
  --color-negative-soft: #fff0f0;
  --color-warning: #a96000;
  --color-warning-soft: #fff4df;
  --color-info: #2463a6;
  --color-info-soft: #eaf3fc;

  --color-focus: #2f6fe4;
}
```

### 5.2 Data visualization palette

Use in this order and verify adjacent contrast:

```css
--chart-1: #1859c9;
--chart-2: #0f8b8d;
--chart-3: #7c5cba;
--chart-4: #d17a22;
--chart-5: #65748b;
--chart-6: #b84f77;
```

Green and red are reserved primarily for gain/loss semantics and should not dominate category charts.

### 5.3 Typography

Default font stack:

```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

Do not add a network-fetched web font during UI Foundation. The stack must render safely in CI and offline development.

Type scale:

- Display financial value: `40/48`, weight 650 desktop; `32/40` mobile.
- Page title: `28/36`, weight 650.
- Section title: `20/28`, weight 650.
- Card title: `16/24`, weight 600.
- Body: `14/22`, weight 400.
- Small/meta: `12/18`, weight 500.

Rules:

- Apply `font-variant-numeric: tabular-nums lining-nums` to monetary, percentage, date, and quantity values.
- Avoid all-caps headings except tiny status labels.
- Do not use font weights below 400 for financial metadata.

### 5.4 Spacing

Base unit: `4px`.

Approved scale:

`4, 8, 12, 16, 20, 24, 32, 40, 48, 64`

Default card padding:

- Desktop: `24px`.
- Mobile: `20px` or `16px` for dense list cards.

### 5.5 Radius and elevation

- Small controls: `8px`.
- Inputs/buttons: `10px`.
- Cards: `14px`.
- Large modal/drawer: `18px`.
- Pills/badges: full radius.

Elevation:

- Standard cards primarily use border, not shadow.
- Floating surfaces use one restrained shadow token.
- Do not stack border, strong shadow, and tinted background on the same ordinary card.

### 5.6 Motion

- Standard transition: `160ms ease-out`.
- Drawer/dialog: `220ms`.
- Respect `prefers-reduced-motion`.
- Never animate financial values in a way that delays comprehension.

## 6. Core Component Contract

### Layout

- `AppShell`
- `SidebarNavigation`
- `MobileNavigation`
- `TopBar`
- `PageContainer`
- `PageHeader`
- `SectionHeader`
- `ResponsiveGrid`

### Primitives

- `Button`: primary, secondary, tertiary, destructive, icon-only.
- `IconButton`: requires accessible label.
- `Card`: default, subtle, inverse, interactive.
- `Badge`: neutral, positive, negative, warning, info.
- `Input`, `Select`, `Textarea`.
- `Dialog`, `Drawer`, `DropdownMenu`, `Tooltip`.
- `Tabs`, `SegmentedControl`.
- `Skeleton`, `Spinner`.
- `EmptyState`, `ErrorState`, `InlineAlert`.

### Financial components

- `MoneyValue`
  - receives Decimal-safe formatted string or minor-unit-safe value,
  - never calculates with JavaScript floats,
  - supports privacy masking.

- `ChangeValue`
  - amount plus percentage,
  - positive/negative/neutral semantics,
  - explicit sign.

- `MetricCard`
- `DataFreshnessBadge`
- `SourceMetadata`
- `PortfolioValueHero`
- `PerformanceChart`
- `AllocationBreakdown`
- `HoldingsTable`
- `HoldingCard`
- `RecentTransactions`
- `PortfolioObservation`

### Component rules

- Presentational components receive prepared values; they do not own portfolio calculations.
- Formatting helpers are centralized.
- Avoid giant dashboard files. Each major card is its own component.
- Use Server Components by default; add `use client` only for genuine interaction.
- Icons must come from one consistent icon set. Do not mix emoji, text symbols, and multiple icon libraries.
- Do not install a full UI framework in UI Foundation.

## 7. Financial Display Conventions

### Locale

- Locale: `tr-TR`.
- Default reporting currency: `TRY`.
- Example: `₺125.430,75`.
- Currency code may accompany ambiguous or non-TRY values: `1.250,00 USD`.
- Percent example: `%4,28` in Turkish prose; change component may show `+%4,28` consistently.

### Dates and time

- Date: `5 Ağu 2026`.
- Date with time: `5 Ağu 2026, 22:45`.
- Use 24-hour time.
- Display timezone context where market time could be misunderstood.

### Precision

- Portfolio totals: 2 decimal places.
- Unit price: configurable by instrument, up to 4 visible decimals by default.
- Quantity: up to 10 decimals when needed; trim insignificant trailing zeros.
- Never display false precision merely because the database supports it.

### Privacy mode

- Masks monetary values consistently, not selectively.
- Preserve structural labels and percentage direction only if product policy permits.
- The toggle state should persist locally, not be sent to analytics.

## 8. States and Feedback

Every major dashboard region must define:

1. Loading
2. Empty
3. Partial data
4. Stale data
5. Error
6. Success/ready

### Empty dashboard

Do not show a fake profitable portfolio. Use an onboarding state:

- title: `Portföyünüzü oluşturmaya başlayın`,
- explanation,
- primary action: `İlk hesabı ekle`,
- secondary action: `İşlem ekleme yöntemini incele`.

### Stale data

- Keep last known value visible.
- Mark it as stale.
- Show observed time and source.
- Explain whether totals include stale positions.

### Error

- State what failed.
- State what remains available.
- Offer retry only when retry is meaningful.
- Never replace a failed value with zero.

### Transaction confirmation

Future add-transaction flow:

1. Entry
2. Parsed/normalized preview
3. Validation feedback
4. Explicit confirmation
5. Success receipt with edit/undo path

Natural-language/OpenAI entry must always pass through steps 2–4.

## 9. Accessibility Requirements

- Target WCAG 2.2 AA.
- Visible focus ring for all keyboard controls.
- Minimum interactive target: `44x44px` on touch surfaces.
- Sidebar and bottom navigation expose active page programmatically.
- Tables use semantic headers and captions.
- Charts provide text summaries and accessible data alternatives.
- Tooltips never contain information unavailable elsewhere.
- Error messages associate with form fields.
- Do not hide focus outlines without a replacement.
- Gain/loss states include text/sign/icon beyond colour.

## 10. Responsive Acceptance Matrix

Implementation must be visually checked at minimum:

- 360 × 800
- 390 × 844
- 768 × 1024
- 1024 × 768
- 1280 × 800
- 1440 × 900
- 1920 × 1080

No horizontal page scroll is permitted. A holdings table may use an explicitly labelled inner scroll container only when the card alternative is not active.

## 11. UI Foundation Implementation Scope

Included:

- semantic token layer,
- reset/global styles,
- responsive application shell,
- desktop/sidebar and mobile navigation,
- dashboard page using typed mock data,
- reusable core and financial display components,
- loading, empty, stale, and error examples,
- Turkish formatting helpers,
- accessibility baseline,
- responsive verification,
- unit tests only where supported by existing toolchain; do not add a large test framework solely for this milestone.

Excluded:

- real backend data integration,
- authentication,
- brokerage connectivity,
- automatic trading,
- OpenAI API integration,
- live market feeds,
- real recommendations,
- chart library dependency unless clearly justified,
- dark-mode toggle,
- elaborate animation.

## 12. Mock Dashboard Content Contract

Use realistic but explicitly mock data in a dedicated typed module. Do not embed values throughout JSX.

Suggested scenario:

- Total portfolio value: `₺428.650,40`
- Daily change: `+₺2.184,30`, `+%0,51`
- Total return: `+₺38.420,70`, `+%9,85`
- Principal: `₺390.229,70`
- Unrealized result: `+₺31.780,20`
- Realized result: `+₺6.640,50`
- Cash/reserve: `₺54.200,00`

Holdings should cover several classes without implying investment advice:

- a generic money-market fund,
- a generic gold fund or physical-gold position,
- a generic equity fund,
- USD cash,
- TRY cash/reserve.

Do not use a real instrument as a promoted recommendation. Mark the fixture source as `Demo veri`.

## 13. Definition of Done

UI Foundation is complete only when:

- the shell works at all target widths,
- navigation has correct active and focus states,
- dashboard hierarchy matches this specification,
- all money and percentages use centralized Turkish formatters,
- numbers use tabular figures,
- data freshness is visible,
- no component performs financial calculations,
- mock data is typed and isolated,
- loading/empty/error/stale states are represented,
- no automated-trading language appears,
- lint passes,
- TypeScript typecheck passes,
- production build passes,
- the implementation agent reports exact changed files and validation results.

## 14. Governance

Claude Code or another implementation agent may make implementation-level choices only when they do not alter:

- navigation hierarchy,
- dashboard order,
- semantic token meanings,
- financial terminology,
- confirmation requirements,
- accessibility requirements,
- product boundary against automatic trading.

Any proposed change to those areas must be reviewed as a UI/UX decision before implementation.