# Agent Sorumlulukları

## TARS / mimari denetim

- Ürün kapsamını ve finansal doğruluk kurallarını belirler.
- Domain modelleri, veri kökeni ve güvenlik kararlarını inceler.
- Finansal hesap formüllerini ve test senaryolarını doğrular.
- Claude tarafından üretilen değişiklikleri diff ve test sonuçları üzerinden denetler.

## Claude Code + DeepSeek V4 Pro

- Onaylı görev dosyasına göre geniş kod iskeletini üretir.
- Tekrarlı CRUD, migration, şema, UI iskeleti ve test altyapısını uygular.
- Test/lint komutlarını çalıştırır ve sonuçları raporlar.
- Kapsam dışına çıkmaz; finansal varsayım icat etmez.

## Kullanıcı

- API anahtarlarını yalnızca yerel `.env` içinde yönetir.
- Banka/aracı kurum erişim bilgilerini projeye eklemez.
- Claude Code oturumundaki planı ve test sonucunu kontrol eder.
