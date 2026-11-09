# Actuome Manifestosu
## Fiziksel yapay zekânın donanım varsayımlarını görünür kılmak

**OpenActuome · Deneysel öneri 0.1.0 · 9 Kasım 2026**  
Proje sahibi: **[Troya Science](https://troyascience.com)**

### Zekânın fiziksel bir karşılığı var

Bir robot modeli hareket komutları üretir. Bu komutların nasıl bir harekete
dönüştüğü ise motorlara, aktarma mekanizmalarına, kontrol sistemine, haberleşmeye,
enerjiye, sıcaklığa ve çevreyle temasa bağlıdır. Bir koşulda işe yarayan komut,
başka bir koşulda aynı sonucu vermeyebilir.

Robotik bu sorunu yeni keşfetmedi. Dinamik modelleme, sistem tanılama ve kontrol
uzun süredir çalışılıyor. MuJoCo eyleyici ve aktarım modelleri içeriyor [1].
Isaac Lab tork-hız sınırlarını ve komut gecikmesini modelleyebiliyor [2]. Farklı
robotlardan öğrenilen deneyimin başka robotlarda işe yaradığını gösteren
araştırmalar da var [3]. Yeni bir önerinin bu birikimi yok saymaması gerekir.

Bizim geliştirmek istediğimiz nokta, donanıma ilişkin varsayımların ekipler ve
araçlar arasında nasıl paylaşıldığı. Tek bir tork değeri, bunun sürekli mi yoksa
kısa süreli mi uygulanabildiğini söylemez. Gecikmenin başlangıç ve bitiş anları
tanımlanmamışsa iki sayıyı karşılaştırmak yanıltıcı olabilir. Sıcaklık sınırının
anlamı sensörün yerine ve çalışma koşullarına bağlıdır. Ölçülmemiş bir özelliğin
yerine sıfır yazmak, belirsizliği bilgiye dönüştürmez.

### Önerdiğimiz kavram

**Actuome** adını, bir fiziksel sistemin hareket üretme kapasitesini ve sınırlarını;
bunların kaynakları ve geçerli oldukları koşullarla birlikte tanımlayan profil
için öneriyoruz. **Actuomics**, bu profillerin ölçülmesi, incelenmesi ve
karşılaştırılması yaklaşımına verdiğimiz ad.

Bunlar proje kapsamında önerilen tanımlardır. Yeni bir bilim dalının oluştuğunu
veya bütün sektörün bu terimleri benimsediğini iddia etmiyoruz. Biyolojik benzetme
ismi açıklamaya yardımcı olur; bir robotu genomla eşitlemez. Eksiksiz olduğunu
iddia eden bir tablo yerine, sınırları açık ve kullanılabilir bir başlangıç tercih
ediyoruz.

### Önce veri ve kaynak

OpenActuome 0.1; tek serbestlik dereceli hareket eksenlerini, doğru birimleri,
sürekli ve kısa süreli kuvvet/tork sınırlarını, hızı, tanımlı gecikme ölçümlerini
ve geri sürülebilirliği ele alır. Sıcaklık bilgileri ve kuvvet/tork-hız eğrileri
isteğe bağlıdır. Her eksendeki bilgi; ölçülmüş, üretici beyanı, simülasyon,
sentetik veya bilinmiyor olarak işaretlenir.

Profil, donanım sürümünü ve ölçüm koşullarını belirtir. Bir robotun yalnızca
belirli eksenleri anlatılıyorsa bunun kısmi bir profil olduğunu açıkça söyler.
Doğrulayıcı dosya yapısını ve alanlar arasındaki tutarlılığı kontrol eder.
Raporlama aracı, evrensel bir başarı puanı uydurmadan bu bilgileri görünür kılar.

Bu paketle verilen örnekler sentetiktir veya ölçülmemiş şablondur. Tesla, Figure,
Unitree, Boston Dynamics ya da başka bir üreticiye ait teknik ölçüm değildir.
Gerçek robotlar arasında bir performans sıralaması sunulmuyor.

### Uyumluluğu deneyerek göstermek

Ortak bir tanım biçimi, aynı verinin tekrar tekrar toplanmasını azaltabilir ve
varsayımları incelemeyi kolaylaştırabilir. Fakat kendi başına bir robot modelini
başka donanıma uyarlamaz, kalibrasyonun yerini tutmaz ve güvenli çalışma onayı
vermez. Mevcut araçlarla uyumluluğu, açık alan eşlemeleri ve geri dönüş testleriyle
göstermek istiyoruz.

İlk deneysel hedefimiz iki farklı eyleyiciyi aynı protokolle ölçmek, kaynaklarıyla
birlikte yayımlamak ve desteklenen alanları tek bir mevcut araca aktarmak.
Aktarımda korunan ve kaybolan bilgileri de raporlayacağız. İleride performans
iyileşmesi ileri sürülürse karşılaştırma yöntemi, tekrar sayısı ve belirsizlik
sonuçla birlikte açıklanmalı.

### Açık katkı çağrısı

Donanım mühendislerini, kontrol araştırmacılarını, simülasyon geliştiricilerini
ve robotik ekiplerini bu taslağı eleştirmeye davet ediyoruz. Hangi alanlar belirsiz?
Hangi ölçümler uygulanabilir? Hangi mevcut tanımları tekrar kullanmalıyız?
Öneri gerçek bir iş akışında hangi yükü azaltabilir?

Hedefimiz, hareket üretme kapasitesini daha anlaşılır ve denetlenebilir biçimde
paylaşmak. OpenActuome'un değeri, kendisini standart ilan etmesinden değil;
işe yarayan katkılardan ve bağımsız kullanımdan doğacak.

**Troya Science — [troyascience.com](https://troyascience.com)** tarafından başlatılmıştır.

### Kaynaklar

1. [MuJoCo dinamik ve eyleyici modeli](https://mujoco.readthedocs.io/en/stable/computation/index.html).
2. [Isaac Lab eyleyici modelleri](https://isaac-sim.github.io/IsaacLab/main/source/concepts/actuators.html).
3. [Open X-Embodiment ve RT-X araştırması](https://robotics-transformer-x.github.io/).

Resmî hak sahibi: **TROYA BİLİM EĞİTİM ORGANİZASYON TEKNOLOJİ LİMİTED ŞİRKETİ**.
