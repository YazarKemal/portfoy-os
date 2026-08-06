# Task 005 — Core Portfolio Ledger

## Goal

Implement the first real financial-recording and deterministic portfolio-calculation layer for Portföy OS.

`docs/architecture/core-portfolio-ledger.md` is the binding architecture contract. Read it completely before editing.

This task replaces demo-only backend capability with a reliable single-user ledger API. It does not connect the frontend yet.

## Branch and safety rules

- Work only on `feat/core-portfolio-ledger`.
- Pull the latest remote branch before editing.
- Do not modify `main`.
- Do not merge a pull request.
- Do not force-push.
- Do not modify UI layout or dashboard mock data.
- Do not add OpenAI, live market data, recommendations, automatic trading, authentication, scraping, or external network calls.
- Do not read or expose `.env` values.
- Do not use float for financial calculations.
- Preserve the existing health endpoint and CI workflow.

## 1. Add domain enums

Update `services/api/app/enums.py`.

Add:

```python
class TransactionStatus(enum.StrEnum):
    DRAFT = "DRAFT"
    POSTED = "POSTED"
    VOIDED = "VOIDED"


class TransactionSource(enum.StrEnum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    AI = "AI"
```

Do not rename existing `TransactionType`, `DataLatency`, or `DataSourceStatusState` members.

## 2. Refactor the database model into one ledger

Update `services/api/app/models.py` and create a new Alembic migration after `001_initial_core_models.py`.

### Account additions

Add:

```text
is_active              boolean, non-null, default true
allow_negative_balance boolean, non-null, default false
```

### Transaction changes

The existing `transactions` table becomes the canonical ledger table.

Required columns and behavior:

```text
asset_id             nullable
quantity             nullable NUMERIC(28,10)
unit_price           nullable NUMERIC(20,8)
gross_amount         non-null NUMERIC(20,4)
fee_amount           non-null NUMERIC(20,4), default 0
tax_amount           non-null NUMERIC(20,4), default 0
net_cash_effect      non-null NUMERIC(20,4)
status               TransactionStatus enum, non-null, default DRAFT
source               TransactionSource enum, non-null, default MANUAL
idempotency_key      nullable string(100), unique
confirmed_at         nullable timestamptz
voided_at            nullable timestamptz
void_reason          nullable text
updated_at           non-null timestamptz
```

The old `total_amount` field may be renamed to `gross_amount` in the migration or replaced safely. The final ORM model and database must expose only `gross_amount`.

Add basic database constraints:

- `gross_amount >= 0`
- `fee_amount >= 0`
- `tax_amount >= 0`
- `quantity IS NULL OR quantity > 0`
- `unit_price IS NULL OR unit_price > 0`

### Remove separate cash-flow storage

Drop the `cash_flows` table in the upgrade and remove the `CashFlow` ORM model and relationship.

This project is pre-production and contains no user financial data. The downgrade must recreate the original `cash_flows` table and restore the original transaction shape sufficiently for Alembic roundtrip validation.

### Migration requirements

- Use a new revision ID such as `002_core_portfolio_ledger`.
- Preserve PostgreSQL enum creation/drop ordering.
- Upgrade, current/head check, downgrade, and re-upgrade must pass in CI.
- Do not modify the original `001` migration.

## 3. Add explicit single-user dependency

Update configuration and create dependencies/services as needed.

Add settings with safe non-secret defaults:

```text
DEFAULT_USER_EMAIL=owner@portfoy.local
DEFAULT_USER_DISPLAY_NAME=Portföy Sahibi
```

Implement an async dependency that resolves the configured user and creates it when absent.

Requirements:

- User creation must be race-safe.
- Routers must not duplicate user lookup logic.
- Keep the dependency isolated so real authentication can replace it later.
- Do not expose a public user-creation endpoint in this task.

## 4. Add money normalization utilities

Create `services/api/app/domain/money.py`.

Provide typed Decimal helpers for:

- money quantization to 4 decimal places,
- price quantization to 8 decimal places,
- quantity quantization to 10 decimal places,
- rejecting NaN, Infinity, negative absolute inputs, and zero when a positive value is required.

Requirements:

- Use `Decimal` only.
- Define explicit rounding behavior using `ROUND_HALF_EVEN`.
- Do not change the global Decimal context.
- Utilities must have focused unit tests.

## 5. Implement the pure ledger engine

Create `services/api/app/domain/ledger.py`.

Use typed dataclasses or frozen domain models. Do not import FastAPI in this module.

The engine must process chronologically ordered `POSTED` events and return:

### Account state

- cash balance,
- net external contributions,
- total realized result,
- positions keyed by asset ID.

### Position state

- quantity,
- cost basis,
- weighted average cost,
- realized P/L.

### Calculation rules

#### BUY

```text
gross = quantity × unit price
cash effect = -(gross + fee + tax)
new cost basis = old cost basis + gross + fee + tax
```

#### SELL

```text
gross = quantity × unit price
cash effect = gross - fee - tax
allocated cost = current average cost × sold quantity
realized P/L = cash effect - allocated cost
```

Reject a sale above available quantity.

#### DIVIDEND / INTEREST

Increase cash by `gross - fee - tax` and increase realized result by the same amount.

#### DEPOSIT / WITHDRAWAL

Affect cash and net external contributions, not realized result.

```text
DEPOSIT:    contributions += gross
WITHDRAWAL: contributions -= gross
```

#### FEE / TAX

Reduce cash and realized result by `gross`.

#### TRANSFER_IN / TRANSFER_OUT

Affect account cash but not external contributions or investment result.

The engine must verify that each persisted event's `net_cash_effect` matches the deterministic value derived from its fields. A mismatch is a domain error, not silently accepted.

### Event ordering

Sort by:

1. `transaction_date`
2. `created_at`
3. `id`

The same input sequence must always produce the same state.

## 6. Add stable domain errors

Create `services/api/app/errors.py`.

Implement a typed `DomainError` containing:

- `code`
- `message`
- optional `context`
- HTTP status mapping

Add a FastAPI exception handler returning:

```json
{
  "detail": {
    "code": "INSUFFICIENT_CASH",
    "message": "...",
    "context": {}
  }
}
```

Required codes:

```text
ACCOUNT_NOT_FOUND
ASSET_NOT_FOUND
TRANSACTION_NOT_FOUND
INVALID_TRANSACTION_SHAPE
INVALID_TRANSACTION_STATE
INSUFFICIENT_CASH
INSUFFICIENT_QUANTITY
DUPLICATE_IDEMPOTENCY_KEY
PRICE_NOT_AVAILABLE
```

Client behavior must never depend on parsing message text.

## 7. Add Pydantic schemas

Create a `services/api/app/schemas/` package with:

```text
accounts.py
assets.py
transactions.py
portfolio.py
```

Use Pydantic v2 and strict typing.

### General rules

- `extra="forbid"` on write schemas.
- Currency codes normalized to uppercase 3-character values.
- Codes normalized to uppercase.
- Datetimes must be timezone-aware.
- Decimal response fields remain Decimal so JSON serialization preserves precision.
- Do not use `any` or untyped dictionaries where a schema is possible.

### Transaction draft input

Support:

```text
account_id
asset_id optional
transaction_type
quantity optional
unit_price optional
gross_amount optional
fee_amount default 0
tax_amount default 0
currency
transaction_date
source default MANUAL
idempotency_key optional
notes optional
```

For BUY/SELL, derive gross amount from quantity × unit price. If caller also sends gross amount, it must match after quantization or the request is rejected.

For cash/income events, gross amount is required and positive.

### Draft response

Return normalized values and a human-review summary, including:

- derived gross amount,
- fee,
- tax,
- signed cash effect,
- projected account cash after confirmation,
- projected position quantity when applicable,
- warning list,
- transaction status.

Warnings are deterministic facts only; do not include investment recommendations.

## 8. Implement services

Create `services/api/app/services/` with focused modules:

```text
users.py
accounts.py
assets.py
transactions.py
portfolio.py
```

### Accounts

- Create account for default user.
- List only the default user's accounts.
- Get account with ownership check.
- Reject empty names and unsupported currency shapes.

### Assets

- Create globally unique assets.
- List and get assets.
- Add manual price observations.
- Latest price selection order:
  1. greatest `market_time`
  2. greatest `observed_at`
  3. greatest `id`

Manual price writes must store:

```text
provider = "manual"
data_latency = MANUAL
```

### Transaction drafts

`create_draft` must:

1. Resolve and lock the account when necessary.
2. Verify account ownership and active state.
3. Verify asset existence and required/forbidden asset rules.
4. Normalize all Decimal values.
5. Derive `gross_amount` and `net_cash_effect`.
6. Calculate current posted account state.
7. Calculate projected state.
8. Reject insufficient quantity immediately.
9. Return `INSUFFICIENT_CASH` if the projected balance is negative and the account does not allow it.
10. Persist a `DRAFT` transaction.

### Idempotency

If the same non-null `idempotency_key` is reused:

- return the existing transaction when the normalized request is equivalent,
- raise `DUPLICATE_IDEMPOTENCY_KEY` when the payload conflicts.

Do not solve this only with a pre-check; handle the database uniqueness race.

### Confirmation

`confirm_transaction` must:

1. Select the draft row with `FOR UPDATE`.
2. Require `DRAFT` status.
3. Lock the account.
4. Recompute current posted state.
5. Revalidate cash and quantity constraints.
6. Set status to `POSTED` and `confirmed_at` in one transaction.
7. Return the posted transaction.

Confirmation must be safe under two concurrent requests. At most one confirmation succeeds.

### Void

Only a `DRAFT` transaction may be voided.

Require a non-empty reason and set:

```text
status = VOIDED
voided_at = now
void_reason = supplied reason
```

Posted entries have no update/delete/void behavior in this milestone.

## 9. Implement API routers

Add routers under `services/api/app/routers/` and include them in `app/main.py` with prefix `/api/v1`.

### Accounts

```text
POST /api/v1/accounts
GET  /api/v1/accounts
GET  /api/v1/accounts/{account_id}
```

### Assets

```text
POST /api/v1/assets
GET  /api/v1/assets
GET  /api/v1/assets/{asset_id}
POST /api/v1/assets/{asset_id}/prices
GET  /api/v1/assets/{asset_id}/prices/latest
```

### Transactions

```text
POST /api/v1/transactions/drafts
GET  /api/v1/transactions
GET  /api/v1/transactions/{transaction_id}
POST /api/v1/transactions/{transaction_id}/confirm
POST /api/v1/transactions/{transaction_id}/void
```

Transaction listing requirements:

- default newest first,
- `limit` default 50 and maximum 200,
- optional filters for account, asset, type, and status,
- only default-user-owned account transactions.

### Portfolio

```text
GET /api/v1/portfolio/summary
GET /api/v1/portfolio/holdings
```

## 10. Implement portfolio valuation

The portfolio service must:

1. Load all posted events for the default user's accounts.
2. Calculate account states using the pure ledger engine.
3. Fetch the latest known price for every open position.
4. Return holdings and aggregate summary.

### Holding response

Include:

```text
account_id
account_name
asset_id
asset_code
asset_name
quantity
average_cost
cost_basis
realized_pnl
latest_price nullable
price_provider nullable
price_market_time nullable
price_observed_at nullable
price_latency nullable
market_value nullable
unrealized_pnl nullable
valuation_status: VALUED | PRICE_MISSING
```

### Summary response

Include:

```text
currency
cash_balance
net_external_contributions
realized_pnl
unrealized_pnl nullable
total_market_value nullable
total_portfolio_value nullable
total_return nullable
open_position_count
missing_price_count
account_count
calculated_at
```

If at least one open position has no price:

- keep cash, contributions, realized P/L, and available holding facts,
- set aggregate valuation-dependent totals to `null`,
- report the missing count,
- do not guess values.

## 11. Tests

Add comprehensive tests without external network access.

### Pure domain tests

At minimum:

- money quantization and invalid Decimal rejection,
- one buy with fee and tax,
- two buys producing weighted-average cost,
- partial sell and realized P/L,
- full sell returning zero quantity and zero cost basis,
- oversell rejection,
- deposit then buy cash calculation,
- withdrawal contribution behavior,
- dividend and interest realized result,
- standalone fee and tax result,
- transfer behavior,
- event ordering determinism,
- persisted cash-effect mismatch rejection.

### Service/API tests

At minimum:

- default user created once,
- create/list/get account,
- create/list/get asset,
- manual price creation and latest-price tie breaking,
- deposit draft does not affect portfolio before confirmation,
- deposit confirmation affects cash and contributions,
- buy draft and confirmation after deposit,
- buy rejection with insufficient cash,
- sell rejection with insufficient quantity,
- duplicate idempotency equivalent request returns existing draft,
- duplicate idempotency conflicting request returns stable error,
- concurrent/double confirmation cannot post twice,
- draft void with reason,
- posted transaction cannot be voided,
- transaction filters and ownership boundary,
- summary with valued position,
- summary with missing price returns null valuation totals,
- no update/delete routes for posted transactions.

Use exact Decimal assertions. Do not use approximate float comparisons.

## 12. Documentation

Update `README.md` with:

- single-user mode explanation,
- new environment settings,
- migration command,
- example API sequence:
  1. create account,
  2. create deposit draft,
  3. confirm deposit,
  4. create asset,
  5. add manual price,
  6. create and confirm buy,
  7. read portfolio summary.

Do not include real API keys or real investment examples.

## 13. Validation

Run from repository root:

```bash
git diff --check
python3 -m compileall services/api/app services/api/tests services/api/alembic
pnpm install --frozen-lockfile
pnpm lint
pnpm typecheck
pnpm build
```

When backend dependencies and PostgreSQL are available, also run:

```bash
cd services/api
uv sync --all-groups
uv run ruff check .
uv run mypy app
uv run alembic upgrade head
uv run alembic current
uv run alembic downgrade -1
uv run alembic upgrade head
uv run pytest
```

Return to repository root before inspecting the final diff.

## 14. Commit and push

Stage only Task 005 implementation files.

Commit with this exact message:

```text
feat: implement core portfolio ledger
```

Push normally to:

```text
origin feat/core-portfolio-ledger
```

Do not merge.

## 15. Report

Return:

- commit SHA,
- exact changed files,
- migration revision and roundtrip result,
- Ruff, mypy, pytest, frontend lint/typecheck/build results,
- API endpoints implemented,
- ledger calculation cases covered,
- any uncompleted requirement and why,
- final `git status`,
- pull request URL only if one already exists.
