# Portföy OS

Türkiye odaklı kişisel portföy takibi, risk analizi ve açıklanabilir karar desteği uygulaması.

## Amaç

Portföy OS; nakit, vadeli mevduat, yatırım fonu, hisse, altın ve döviz işlemlerini tek bir muhasebe defterinde toplar. Gerçekleşmiş/gerçekleşmemiş kârı, nakit akışlarını, risk metriklerini ve veri güncelliğini izler.

Bu ürün:

- yatırım tavsiyesi vermez,
- garantili getiri iddiasında bulunmaz,
- aracı kurum şifresi saklamaz,
- otomatik emir göndermez,
- yapay zekâyı finansal hesaplama motoru olarak kullanmaz.

## Hedef teknoloji yığını

- **Web:** Next.js, TypeScript, Tailwind CSS
- **API:** Python, FastAPI, SQLAlchemy 2, Alembic
- **Veri:** PostgreSQL
- **İş kuyruğu/önbellek:** Redis
- **Paket yönetimi:** pnpm ve uv
- **Yerel ortam:** Docker Compose

## Yerel kurulum

### Ön gereksinimler

- Node.js >= 22
- pnpm >= 10
- Python >= 3.12
- uv (Python paket yöneticisi)
- Docker ve Docker Compose (PostgreSQL ve Redis için)

### 1. Depoyu klonla

```bash
git clone <repo-url>
cd portfoy-os
```

### 2. Ortam değişkenlerini ayarla

```bash
cp .env.example .env
```

### 3. Servisleri başlat

```bash
docker compose up -d postgres redis
```

### 4. Frontend bağımlılıklarını kur

```bash
pnpm install
```

### 5. Backend bağımlılıklarını kur

```bash
uv sync --directory services/api --all-extras
```

### 6. Veritabanı migration'larını çalıştır

```bash
uv run --directory services/api alembic upgrade head
```

### 7. API'yi başlat

```bash
uv run --directory services/api uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8. Frontend'i başlat

```bash
pnpm dev
```

API `http://localhost:8000` adresinde, web uygulaması `http://localhost:3000` adresinde çalışır.

## Doğrulama komutları

```bash
# Frontend
pnpm install
pnpm lint
pnpm typecheck

# Backend
uv sync --directory services/api --all-extras
uv run --directory services/api ruff check .
uv run --directory services/api mypy app
uv run --directory services/api pytest
```

## Proje yapısı

```
portfoy-os/
├── apps/
│   └── web/             # Next.js kullanıcı arayüzü
├── services/
│   └── api/             # FastAPI REST API
│       ├── app/
│       │   ├── models.py
│       │   ├── enums.py
│       │   ├── config.py
│       │   ├── database.py
│       │   ├── main.py
│       │   └── routers/
│       ├── alembic/     # Veritabanı migration'ları
│       └── tests/
├── packages/            # Paylaşımlı kütüphaneler
├── docs/                # Karar kayıtları ve ürün sözleşmeleri
├── docker-compose.yml
└── .github/workflows/   # CI
```

## Geliştirme

İlk geliştirme çalışmaları `feat/bootstrap-foundation` dalında yürütülür. Görev detayları için `docs/agent-tasks/` dizinine bakın.
