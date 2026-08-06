# Core Portfolio Ledger Architecture

Status: Approved architecture contract for `feat/core-portfolio-ledger`

## 1. Purpose

The Core Portfolio Ledger is the accounting and audit foundation of Portföy OS. Every later capability—portfolio analytics, planning, candidate scoring, risk controls, market-data integration, and OpenAI explanations—must consume this ledger instead of inventing or recalculating financial facts independently.

This layer is not a brokerage connection, automatic trading system, or recommendation engine.

## 2. Core principles

1. **Posted financial events are auditable**
   - A posted event is never silently edited or deleted.
   - Draft events do not affect balances or positions.
   - Invalid drafts can be voided with a reason.

2. **One deterministic calculation engine**
   - Cash balance, quantity, cost basis, realized P/L, unrealized P/L, and portfolio value are calculated in backend domain code.
   - The frontend and OpenAI must never reproduce accounting logic.

3. **Decimal precision only**
   - Money, prices, quantities, fees, and taxes use `Decimal` and PostgreSQL `NUMERIC`.
   - No float arithmetic is allowed in ledger calculations.

4. **Explicit confirmation**
   - User input first creates a normalized draft.
   - A separate confirmation action posts the draft.
   - The confirmation endpoint revalidates cash and position constraints.

5. **Single-user mode is explicit**
   - Authentication is out of scope for this milestone.
   - API requests resolve one configured default user through a dependency.
   - This must be isolated so authentication can replace it later.

6. **Data provenance remains visible**
   - Asset prices retain provider, market time, observed time, and latency.
   - Valuation responses expose missing or stale price state.

7. **No profit guarantee**
   - The ledger records facts and produces deterministic accounting results.
   - It does not predict returns or issue buy/sell instructions.

## 3. Unified transaction model

The existing `transactions` table becomes the canonical ledger-event table. The separate `cash_flows` table is removed in the new migration because cash events and asset events must appear in one chronological audit stream.

### Transaction lifecycle

- `DRAFT`: normalized and reviewable, but has no financial effect.
- `POSTED`: confirmed and included in all calculations.
- `VOIDED`: cancelled before posting; retained for audit.

### Transaction source

- `MANUAL`
- `IMPORT`
- `AI`

`AI` means an AI-created draft. It does not mean the AI confirmed or executed the transaction.

### Canonical fields

- `id`
- `account_id`
- `asset_id` nullable for pure cash events
- `transaction_type`
- `status`
- `source`
- `quantity` nullable
- `unit_price` nullable
- `gross_amount`
- `fee_amount`
- `tax_amount`
- `net_cash_effect` signed
- `currency`
- `transaction_date`
- `idempotency_key` nullable and unique
- `notes`
- `confirmed_at`
- `voided_at`
- `void_reason`
- `created_at`
- `updated_at`

### Event requirements

| Type | Asset | Quantity / unit price | Cash effect |
|---|---|---|---|
| BUY | required | required | `-(gross + fee + tax)` |
| SELL | required | required | `gross - fee - tax` |
| DIVIDEND | required | not required | `amount - tax - fee` |
| INTEREST | optional | not required | `amount - tax - fee` |
| DEPOSIT | forbidden | not required | `+amount` |
| WITHDRAWAL | forbidden | not required | `-amount` |
| FEE | optional | not required | `-amount` |
| TAX | optional | not required | `-amount` |
| TRANSFER_IN | forbidden | not required | `+amount` |
| TRANSFER_OUT | forbidden | not required | `-amount` |

All request amounts are positive absolute inputs. The backend derives the signed cash effect.

## 4. Accounting method

Portföy OS uses perpetual weighted-average cost for each `(account, asset)` position.

### Buy

- Quantity increases by purchased quantity.
- Cost basis increases by `gross + fee + tax`.
- Average cost becomes `new cost basis / new quantity`.

### Sell

- Selling more than the available quantity is rejected.
- Allocated cost is `current average cost × sold quantity`.
- Realized P/L is `net sale proceeds - allocated cost`.
- Quantity and cost basis decrease by the sold portion.

### Income and standalone costs

- Dividend and interest increase realized result.
- Standalone fees and taxes reduce realized result.
- Deposits and withdrawals alter cash and net contributions, not investment performance.
- Transfers alter account cash, but aggregate portfolio transfers should net to zero when both sides exist.

## 5. Cash controls

Each account gains:

- `is_active`
- `allow_negative_balance`, default `false`

When confirming an event with a negative cash effect, the service obtains a row lock, recomputes posted cash balance, and rejects the event if it would create a negative balance unless the account explicitly allows it.

## 6. Valuation and summary

Only `POSTED` events affect summaries.

### Account and portfolio outputs

- cash balance
- quantity by asset
- weighted average cost
- cost basis
- latest known price
- price provider and freshness
- market value
- realized P/L
- unrealized P/L
- net external contributions
- total portfolio value
- total return = total value - net external contributions

If an asset has no price, its position remains visible with an unavailable valuation. The service must not silently substitute a guessed price.

## 7. API boundary

Base prefix: `/api/v1`

### Accounts

- `POST /accounts`
- `GET /accounts`
- `GET /accounts/{account_id}`

### Assets and manual prices

- `POST /assets`
- `GET /assets`
- `GET /assets/{asset_id}`
- `POST /assets/{asset_id}/prices`
- `GET /assets/{asset_id}/prices/latest`

### Transactions

- `POST /transactions/drafts`
- `GET /transactions`
- `GET /transactions/{transaction_id}`
- `POST /transactions/{transaction_id}/confirm`
- `POST /transactions/{transaction_id}/void`

No update or delete endpoint exists for posted events.

### Portfolio

- `GET /portfolio/summary`
- `GET /portfolio/holdings`

## 8. Domain errors

The API exposes stable error codes, including:

- `ACCOUNT_NOT_FOUND`
- `ASSET_NOT_FOUND`
- `TRANSACTION_NOT_FOUND`
- `INVALID_TRANSACTION_SHAPE`
- `INVALID_TRANSACTION_STATE`
- `INSUFFICIENT_CASH`
- `INSUFFICIENT_QUANTITY`
- `DUPLICATE_IDEMPOTENCY_KEY`
- `PRICE_NOT_AVAILABLE`

Error messages may be Turkish, but clients must branch on codes rather than message text.

## 9. Module boundaries

Recommended backend structure:

```text
app/
  dependencies.py
  errors.py
  domain/
    ledger.py
    money.py
  schemas/
    accounts.py
    assets.py
    transactions.py
    portfolio.py
  services/
    users.py
    accounts.py
    assets.py
    transactions.py
    portfolio.py
  routers/
    accounts.py
    assets.py
    transactions.py
    portfolio.py
```

Routers validate HTTP concerns. Services coordinate database operations. Pure accounting rules live in `domain/ledger.py` and must be unit-testable without FastAPI.

## 10. Milestone exclusions

- Frontend API wiring
- Authentication
- Live TEFAS, metal, FX, or exchange adapters
- Automated trading
- Recommendation or candidate scoring
- Plan-management engine
- OpenAI integration
- Tax-law advice

These capabilities will be built on top of this ledger after it passes migration, typecheck, and accounting tests.
