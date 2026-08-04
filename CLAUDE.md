# Portföy OS — Claude Code Talimatları

## Proje hedefi

Türkiye'deki bireysel kullanıcı için özel portföy takip ve açıklanabilir karar destek sistemi geliştir.

## Değişmez ilkeler

1. LLM finansal hesaplama motoru değildir. Getiri, maliyet, risk ve vergi hesapları deterministik Python kodunda yapılır.
2. Otomatik alım-satım ve emir iletimi uygulanmaz.
3. Aracı kurum, banka veya e-Devlet parolaları istenmez ve saklanmaz.
4. Para değerlerinde binary float kullanılmaz; muhasebe alanlarında `Decimal`/`NUMERIC` kullanılır.
5. Zaman damgaları veritabanında UTC tutulur; kullanıcı arayüzünde Europe/Istanbul gösterilir.
6. Her dış veri kaynağı bir adapter arayüzü arkasında tutulur.
7. Her fiyat kaydında sağlayıcı, piyasa zamanı, alınma zamanı ve veri gecikme türü bulunur.
8. Tavsiye dili kullanılmaz. Çıktılar aday, gözlem, risk ve senaryo olarak sunulur.
9. Her finansal hesap için birim testi yazılır.
10. Backtestlerde look-ahead bias ve survivorship bias önlenir.

## Mimari sınırlar

- `apps/web`: Next.js kullanıcı arayüzü
- `services/api`: FastAPI REST API
- `services/worker`: zamanlanmış veri toplama işleri
- `packages/analytics`: saf ve deterministik finans fonksiyonları
- `packages/data-adapters`: dış veri kaynakları
- `docs`: karar kayıtları ve ürün sözleşmeleri

## MVP kapsamı

- Kullanıcı, hesap, varlık, fiyat, işlem, nakit akışı ve portföy anlık görüntüsü
- İşlem türleri: BUY, SELL, DEPOSIT, WITHDRAWAL, DIVIDEND, INTEREST, FEE, TAX, TRANSFER_IN, TRANSFER_OUT
- Manuel veri girişi ve güvenli CSV içe aktarma için mimari hazırlık
- Sağlık kontrolü ve veri kaynağı sağlık durumu
- Ortalama maliyet, pozisyon miktarı ve basit kâr/zarar için ileride genişletilebilir domain servisleri

## MVP dışında

- Otomatik fon/hisse seçimi
- Broker entegrasyonu
- KAP scraping
- Gerçek zamanlı BIST lisanslı veri dağıtımı
- Portföy optimizasyonu
- LLM raporları

## Kod kalitesi

- Python: Ruff, mypy, pytest
- TypeScript: ESLint, strict mode
- API sözleşmeleri tipli olmalı
- İş kuralları controller/router katmanına yazılmamalı
- Testler ağ bağlantısı gerektirmemeli
- Secret değerleri loglanmamalı

## Çalışma yöntemi

Her görevde:

1. Önce ilgili belgeleri oku.
2. Uygulama planını yaz.
3. Küçük ve doğrulanabilir değişiklikler yap.
4. Test ve lint çalıştır.
5. Başarısızlıkları düzelt.
6. Değişen dosyaları ve kalan riskleri özetle.

Kullanıcı açıkça istemedikçe commit veya push yapma.
