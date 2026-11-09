# Doğrulama kaydı

**OpenActuome 0.1.0 · 9 Kasım 2026 · Yerel ve GitHub kontrolleri**

Proje sahibi: **[Troya Science](https://troyascience.com)**.

## Sonuçlar

- 34 birim ve komut satırı testi geçti; başarısız test yok.
- Yerel ortam: Windows, Python 3.12.14.
- Üç örnek/şablon yapısal ve anlamsal kontrolleri geçti.
- Sentetik dosya, ölçüm etiketi gerektiren modda beklendiği gibi reddedildi.
- Ölçüm etiketi ve bütün gerekli üst veriler sağlansa da araç fiziksel ölçümü doğrulanmış saymıyor.
- Hatalı JSON, yanlış birim, eksen sayısı, referans, gecikme sırası ve sınır değerleri için reddetme testleri var.
- Rapor üretimi çalışıyor; örnek raporda veriler sentetik olarak işaretli.

## GitHub üzerinde doğrulama

9 Kasım 2026 tarihinde `18ca40bcfa947249288b97d307f711698d72ebe8` sürümündeki 34 test,
GitHub Actions üzerinde Python 3.10, 3.12 ve 3.13 ile başarıyla tamamlandı.
Üç ortamda örnek profil doğrulama ve rapor üretimi adımları da geçti.

[Doğrulanmış test çalışması](https://github.com/troyabilim/open-actuome/actions/runs/42677249000)

## Kontrolün sınırları

Fiziksel donanım deneyi, gerçek üretici kıyaslaması veya bağımsız teknik inceleme
yapılmadı. Yerel doğrulayıcı, beraberindeki şemanın kullandığı JSON Schema alt
kümesini uygular; genel amaçlı bağımsız bir JSON Schema motoruyla karşılaştırma
yapılmadı. Bu yazılım testleri gerçek donanım ölçümü veya bağımsız teknik
inceleme yerine geçmez.

## Tekrarlama

```sh
python -m unittest discover -s tests -v
python validate_actuome.py examples/demo_bench.synthetic.json --json
python tools/profile_report.py examples/demo_bench.synthetic.json
```

Bu kayıt yazılım kontrollerini bildirir. Açık kaynak taslak, onaylanmış sektör
standardı veya ölçüme dayalı ürün performansı olarak sunulmamalıdır.
