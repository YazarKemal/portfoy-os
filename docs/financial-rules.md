# Finansal Domain Kuralları

## Muhasebe ilkeleri

- İşlemler silinmek yerine mümkün olduğunda ters kayıtla düzeltilir.
- Ücret ve vergi ayrı işlem/nakit akışı olarak tutulur.
- Gerçekleşmiş ve gerçekleşmemiş kâr birbirine karıştırılmaz.
- Para yatırma ve çekme, yatırım performansı değildir.
- Temettü ve faiz gelirleri ayrı kaynak türleriyle izlenir.
- Döviz çevriminde kullanılan kur, kaynak ve zaman kaydedilir.

## İlk maliyet yöntemi

MVP için ortalama maliyet yöntemi hazırlanacaktır. FIFO gibi alternatif yöntemler ileriki karar kaydına bırakılır. Uygulama kodu maliyet yöntemini değiştirilebilir bir strateji olarak tasarlamalıdır.

## Gerekli test örnekleri

1. Tek alım sonrası miktar ve maliyet
2. Farklı fiyatlardan iki alım sonrası ağırlıklı ortalama maliyet
3. Kısmi satış sonrası kalan miktar
4. Ücretli alımın maliyete etkisi
5. Temettünün maliyet yerine nakit gelirine yazılması
6. Para yatırmanın portföy getirisi sayılmaması
7. Decimal yuvarlama davranışı
8. Aynı zaman damgalı işlemlerde deterministik sıralama

## Terminoloji

- Gerçekleşmiş kâr/zarar: satışla kesinleşmiş sonuç
- Gerçekleşmemiş kâr/zarar: açık pozisyonun güncel değer farkı
- TWR: dış nakit akışlarının etkisini ayıran zaman ağırlıklı getiri
- XIRR: nakit akışlarının tarihini dikkate alan para ağırlıklı getiri
- Drawdown: önceki zirveden yaşanan düşüş
- Veri kökeni: fiyatın hangi sağlayıcıdan ve ne zaman geldiği
