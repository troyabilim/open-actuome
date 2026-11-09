# Doğrulama kaydı

**OpenActuome 0.1.0 · 9 Kasım 2026 · Yerel kontrol**

Proje sahibi: **[Troya Science](https://troyascience.com)**.

## Sonuçlar

- 34 birim ve komut satırı testi geçti; başarısız test yok.
- Ortam: Windows, Python 3.12.14. Testler yalnızca bu ortamda çalıştırıldı.
- Üç örnek/şablon yapısal ve anlamsal kontrolleri geçti.
- Sentetik dosya, ölçüm etiketi gerektiren modda beklendiği gibi reddedildi.
- Ölçüm etiketi ve bütün gerekli üst veriler sağlansa da araç fiziksel ölçümü doğrulanmış saymıyor.
- Hatalı JSON, yanlış birim, eksen sayısı, referans, gecikme sırası ve sınır değerleri için reddetme testleri var.
- Rapor üretimi çalışıyor; örnek raporda veriler sentetik olarak işaretli.
- İngilizce ve Türkçe X dizileri yedişer metin içeriyor. Bağlantı için ayrılan yer dahil üst sınır: 241 / 250 karakter.

## Kontrolün sınırları

Fiziksel donanım deneyi, gerçek üretici kıyaslaması veya bağımsız teknik inceleme
yapılmadı. Yerel doğrulayıcı, beraberindeki şemanın kullandığı JSON Schema alt
kümesini uygular; genel amaçlı bağımsız bir JSON Schema motoruyla karşılaştırma
yapılmadı. GitHub üzerindeki otomatik test akışı hazırlandı, çevrimiçi çalıştırılmadı.
Yazılımın farklı Python sürümlerinde çalışması için akış eklendi; bu sürümlerin
burada test edildiği ileri sürülmüyor.

## Tekrarlama

```sh
python -m unittest discover -s tests -v
python validate_actuome.py examples/demo_bench.synthetic.json --json
python tools/profile_report.py examples/demo_bench.synthetic.json
```

Bu kayıt yazılım kontrollerini bildirir. Açık kaynak taslak, onaylanmış sektör
standardı veya ölçüme dayalı ürün performansı olarak sunulmamalıdır.
