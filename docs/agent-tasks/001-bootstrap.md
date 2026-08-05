# Görev 001 — Monorepo ve çekirdek veri modeli

Bu görev Claude Code + DeepSeek V4 Pro tarafından uygulanacaktır.

## Başlamadan önce

Aşağıdaki dosyaları eksiksiz oku:

1. `CLAUDE.md`
2. `AGENTS.md`
3. `docs/architecture.md`
4. `docs/financial-rules.md`
5. `docs/product-spec.md`

## İstenen uygulama

1. pnpm workspace kur.
2. `apps/web` altında strict TypeScript kullanan Next.js uygulaması oluştur.
3. `services/api` altında FastAPI uygulaması oluştur.
4. Python bağımlılık yönetimini `uv` ve `pyproject.toml` ile kur.
5. SQLAlchemy 2 async model yapısı ve Alembic ekle.
6. Şu çekirdek modelleri oluştur:
   - User
   - Account
   - Asset
   - AssetPrice
   - Transaction
   - CashFlow
   - PortfolioSnapshot
   - DataSourceStatus
7. İşlem enumları:
   - BUY
   - SELL
   - DEPOSIT
   - WITHDRAWAL
   - DIVIDEND
   - INTEREST
   - FEE
   - TAX
   - TRANSFER_IN
   - TRANSFER_OUT
8. `/health` ve `/api/v1/health/data-sources` endpointlerini ekle.
9. pytest, Ruff ve mypy yapılandır.
10. Frontend için ESLint ve typecheck scriptleri ekle.
11. GitHub Actions içinde backend test/lint ve frontend lint/typecheck çalıştır.
12. README'yi tam yerel kurulum komutlarıyla güncelle.

## Teknik kısıtlar

- Para alanlarında float yasak.
- API anahtarları veya gerçek secret değerleri eklenmeyecek.
- Finansal öneri veya alım-satım özelliği eklenmeyecek.
- Router katmanına iş kuralı yazılmayacak.
- Testlerde gerçek PostgreSQL zorunlu tutulabilir; bunun için açık ve kararlı bir test komutu sağlanmalı.
- Oluşturulan migration geri alınabilir olmalı.

## Çalıştırılacak doğrulamalar

```bash
pnpm install
pnpm lint
pnpm typecheck
uv sync --directory services/api --all-extras
uv run --directory services/api ruff check .
uv run --directory services/api mypy app
uv run --directory services/api pytest
```

Docker gerekiyorsa:

```bash
cp .env.example .env
docker compose up -d postgres redis
```

## Beklenen cevap formatı

1. Uygulama planı
2. Oluşturulan/değiştirilen dosyalar
3. Mimari kararlar
4. Çalıştırılan komutlar ve sonuçları
5. Bilinen eksikler

## Claude Code için tek komutluk görev metni

```text
Read CLAUDE.md and every document referenced by docs/agent-tasks/001-bootstrap.md. Implement Task 001 exactly as written. Do not add recommendations, scraping, broker integrations, or AI UI. Before editing, present a concise plan. After editing, run every available validation command, fix failures, and report exact results. Do not commit or push.
```
