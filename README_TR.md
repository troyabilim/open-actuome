# OpenActuome — Türkçe başlangıç

**Proje sahibi: [Troya Science](https://troyascience.com)**  
**Sürüm: 0.1.0 — deneysel taslak, 9 Kasım 2026**

OpenActuome; bir robotun hareket üreten donanımının kapasitesini, sınırlarını ve
bu bilgilerin kaynağını ortak biçimde tanımlamak için hazırlanmış açık bir öneridir.
Actuome bu fiziksel profilin, Actuomics ise ölçüm ve analiz yaklaşımının önerilen adıdır.

Pakette çalışan bir doğrulayıcı, JSON şeması, sentetik örnekler, ölçüm protokolü,
kaynaklı manifesto, kıyaslama şablonu ve araştırma notu bulunur.

Proje deposu: [https://github.com/troyabilim/open-actuome](https://github.com/troyabilim/open-actuome).

## Kullanım

Python 3.10 veya üzeri gerekir; ek paket yüklemek gerekmez.

```sh
python validate_actuome.py examples/demo_bench.synthetic.json
python tools/profile_report.py examples/demo_bench.synthetic.json
python -m unittest discover -s tests -v
```

Başarılı sonuç, dosyanın yapısının ve iç tutarlılığının geçtiğini söyler.
Fiziksel ölçümlerin doğruluğunu veya robotun güvenliğini onaylamaz. Dosyalar
sentetik örnek veya ölçülmemiş şablondur; gerçek robot ölçümü içermez.

## İlk bakılacak dosyalar

- [Doğrulama sonuçları](VALIDATION_REPORT.md)
- `docs/MANIFESTO_TR.md`: fikrin Türkçe açıklaması.
- `docs/SPECIFICATION.md`: teknik kapsam ve birimler.
- `docs/MEASUREMENT_PROTOCOL.md`: gerçek ölçüm ekleme yöntemi.
- `benchmarks/INDEX_TEMPLATE.md`: puansız, kaynak odaklı kıyaslama tablosu.

Bu sürüm modelin farklı robotlara kendiliğinden aktarılmasını sağlamaz;
mevcut simülasyon araçlarıyla denenmiş bir bağlantı da henüz içermez.
Sonraki somut hedef, iki farklı eyleyicide gerçek ölçüm ve tek bir araçla
doğrulanmış aktarım denemesidir.

Resmî hak sahibi: **TROYA BİLİM EĞİTİM ORGANİZASYON TEKNOLOJİ LİMİTED ŞİRKETİ**.
