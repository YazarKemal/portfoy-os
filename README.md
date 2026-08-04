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

## İlk kilometre taşı

1. Monorepo iskeleti
2. Next.js web uygulaması
3. FastAPI servisi
4. PostgreSQL + Redis geliştirme ortamı
5. Hesap, varlık ve işlem veri modeli
6. Sağlık kontrolü ve veri kaynağı durum modeli
7. Deterministik finansal hesaplamalar için test altyapısı

## Hedef teknoloji yığını

- Web: Next.js, TypeScript, Tailwind CSS
- API: Python, FastAPI, SQLAlchemy 2, Alembic
- Veri: PostgreSQL
- İş kuyruğu/önbellek: Redis
- Paket yönetimi: pnpm ve uv
- Yerel ortam: Docker Compose

## Geliştirme dalı

İlk geliştirme çalışmaları `feat/bootstrap-foundation` dalında yürütülür.

## Başlangıç

Claude Code kullanılacaksa önce `CLAUDE.md`, ardından `docs/agent-tasks/001-bootstrap.md` tamamen okunmalıdır.
