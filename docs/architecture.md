# Mimari Kararlar

## 1. Ledger-first yaklaşımı

Portföyün gerçeği, ekrandaki güncel toplam değil işlem defteridir. Pozisyonlar ve portföy anlık görüntüleri işlemlerden yeniden üretilebilir olmalıdır.

## 2. Çift zaman damgası

Fiyat verilerinde en az iki zaman tutulur:

- `market_time`: fiyatın piyasaya ait olduğu zaman
- `observed_at`: sistemin veriyi aldığı zaman

Bu ayrım gecikmeli ve gün sonu verilerinde zorunludur.

## 3. Para ve hassasiyet

- Para: `NUMERIC(20, 4)` başlangıç varsayımı
- Birim/adet: `NUMERIC(28, 10)` başlangıç varsayımı
- Oranlar: domain ihtiyacına göre `NUMERIC`

Şema uygulanırken varlık türlerinin hassasiyet gereksinimleri test edilmelidir.

## 4. Veri kaynağı adapterları

Her sağlayıcı şu sözleşmeyi uygulamalıdır:

- sağlayıcı kimliği
- desteklenen varlık türleri
- fiyat alma yöntemi
- veri gecikme sınıfı
- sağlık durumu
- hata sınıflandırması

TEFAS, TCMB EVDS, gecikmeli hisse verisi ve CSV içe aktarma birbirinden bağımsız adapterlar olacaktır.

## 5. AI izolasyonu

AI katmanı yalnızca hesaplanmış ve doğrulanmış JSON çıktısını açıklayabilir. Veritabanına finansal işlem yazamaz ve emir üretemez.

## 6. Kimlik doğrulama

İlk geliştirme ortamında tek kullanıcı kabul edilebilir; fakat bütün domain tabloları gelecekte çoklu kullanıcı izolasyonunu destekleyecek biçimde `user_id` veya sahiplik ilişkisi içermelidir.
