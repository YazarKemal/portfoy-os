# Ürün Sözleşmesi — M1

## Kullanıcı problemi

Kullanıcı farklı hesap ve yatırım araçlarındaki ana para, faiz, temettü ve piyasa değerini tek ekranda doğru biçimde görmek ister.

## M1 kullanıcı hikâyeleri

- Bir hesap oluşturabilirim.
- Bir varlık tanımlayabilirim.
- Alım, satım, para yatırma, çekme, faiz, temettü, ücret ve vergi işlemi kaydedebilirim.
- API'nin ve veri altyapısının sağlık durumunu görebilirim.
- Hatalı para hassasiyeti veya geçersiz işlem türü sisteme alınmaz.

## Kabul kriterleri

- API health endpoint HTTP 200 döndürür.
- PostgreSQL ve Redis Docker Compose ile ayağa kalkar.
- Alembic ilk migration bütün çekirdek tabloları oluşturur.
- Para alanları Decimal/NUMERIC kullanır.
- İşlem türleri enum ile sınırlandırılır.
- Testler dış ağa ihtiyaç duymadan çalışır.
- README yerel kurulum komutlarını içerir.

## M1 kapsam dışı

- Kullanıcıya fon önerme
- Canlı piyasa ekranı
- Portföy optimizasyonu
- Otomatik veri scraping
- AI sohbet ekranı
- Mobil uygulama
