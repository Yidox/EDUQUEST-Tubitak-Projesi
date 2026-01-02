# 🔬 EDUQUEST: Bilimsel Keşif ve Simülasyon Merkezi
### TÜBİTAK 2209-A Araştırma Projeleri Destekleme Programı Kapsamında Geliştirilmiştir.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/Lisans-MIT-green)
![Status](https://img.shields.io/badge/Durum-Tamamland%C4%B1-success)

## 🎯 1. Projenin Amacı
**EDUQUEST**, ortaöğretim ve lise düzeyindeki öğrencilerin soyut bilimsel kavramları (Fizik, Kimya, Biyoloji ve Matematik) somutlaştırarak öğrenmelerini sağlamak amacıyla geliştirilmiş kapsamlı bir eğitim simülasyon yazılımıdır.

Bu proje, **TÜBİTAK 2209-A** hedefleri doğrultusunda; ezberci eğitim yerine, **"Yaparak-Yaşayarak Öğrenme"** modelini dijital ortama taşımayı hedefler. Öğrenciler, sanal laboratuvar ortamlarında tehlikesizce deney yapabilir, oyunlaştırma (Gamification) teknikleriyle motivasyonlarını artırabilirler.

---

## 🛠️ 2. Kurulum Talimatları (Installation)

Projeyi yerel makinenizde sorunsuz çalıştırmak için aşağıdaki adımları takip edin:

### Gereksinimler
* Python 3.x yüklü bir bilgisayar.
* `matplotlib`, `numpy`, `pillow` kütüphaneleri.

### Adım Adım Kurulum
1. **Projeyi İndirin:**
   Bu sayfadaki "Code" butonuna tıklayıp "Download ZIP" diyerek dosyaları indirin ve masaüstüne çıkarın.

2. **Kütüphaneleri Yükleyin:**
   Terminali (veya Komut İstemi'ni) proje klasöründe açın ve şu komutu girin:
   ```bash
   pip install -r requirements.txt

```

*(Alternatif Manuel Kurulum: `pip install matplotlib numpy pillow`)*

3. **Uygulamayı Başlatın:**
```bash
python main.py

```



⚠️ **ÖNEMLİ NOT:** `avatar.jpg` dosyası, `main.py` ile aynı klasörde bulunmalıdır. Aksi takdirde uygulama açılışta hata verebilir.

---

## 💻 3. Kullanım Detayları ve Modüller

Uygulama, kullanıcı girişinden sonra soldaki menü üzerinden erişilebilen 10 farklı eğitim modülü içerir:

### 🧪 A. Kimya Laboratuvarı

* **İçerik:** Periyodik tablodan elementler (H, O, C, Na vb.) seçilerek çalışma alanına sürüklenir.
* **Etkileşim:** Elementler birbirine yaklaştığında otomatik bağ kurar (Örn: 2H + O -> H₂O).
* **Kazanım:** Atom yapısı ve bileşik oluşturma mantığı kavranır.

### ⚡ B. Elektrik Laboratuvarı

* **İçerik:** Pil, ampul, anahtar ve kablolarla sanal devre kurulumu.
* **Etkileşim:** Devre tamamlandığında ampuller yanar, multimetre ile anlık Voltaj (V) ve Akım (A) değerleri ölçülür.
* **Kazanım:** Ohm yasası ve basit elektrik devreleri öğrenilir.

### 🔭 C. Optik Laboratuvarı

* **İçerik:** Lazer ışığı, düzlem aynalar, engeller ve hedefler.
* **Etkileşim:** Aynaların açıları değiştirilerek ışığın yansıması sağlanır ve hedefler vurulmaya çalışılır.
* **Kazanım:** Işığın yansıma kuralları ve geometrik optik.

### 🧩 D. Cebir & Zeka Oyunu

* **İçerik:** Seviyeli matematik bulmacaları ve geometri soruları.
* **Etkileşim:** Kapı şifresini çözmek için verilen denklem veya üçgen sorularının doğru cevaplanması gerekir.
* **Kazanım:** Problem çözme yeteneği ve matematiksel düşünme.

### 🧬 E. Biyoloji Simülasyonu

* **İçerik:** Av-Avcı (Tavşan-Kurt) popülasyon grafiği.
* **Parametreler:** Üreme hızı, salgın hastalık, kamuflaj mutasyonu gibi değişkenlerle ekosistem dengesi simüle edilir.
* **Kazanım:** Doğal seçilim ve ekosistem dinamikleri.

### 👷 F. Matematik Laboratuvarı (Balistik)

* **İçerik:** Eğik atış simülasyonu (Top atışı).
* **Etkileşim:** Hedefi vurmak için doğru "Hız (v)" ve "Açı (θ)" değerleri hesaplanarak ateşlenir.
* **Kazanım:** Fiziksel atış hareketleri ve parabol denklemleri.

### 🏆 G. Bilim Quizi

* **İçerik:** LGS müfredatına uygun Fizik, Kimya, Biyoloji ve Matematik soruları.
* **Özellik:** Doğru cevaplarla "Seri (Streak)" yapılır ve XP kazanılır.

### 📊 H. Performans Analizi

* **İçerik:** Öğrencinin çözdüğü sorulara ve yaptığı deneylere göre oluşan "Yetenek Haritası".
* **Görsel:** Radar grafiği (Spider Chart) ile hangi derste ne kadar iyi olduğu gösterilir.

### 🌱 I. İrade Yönetimi (Habit Tracker)

* **İçerik:** "Zinciri Kırma" metodu ile günlük alışkanlık takibi.
* **Özellik:** Öğrencilerin düzenli ders çalışma alışkanlığı kazanmasını teşvik eden motive edici sözler içerir.

### 🤖 J. AI Asistan (Prof. Pixel)

* **İçerik:** Akıllı sohbet botu.
* **Özellik:** Bilimsel terimleri (DNA, Basınç, Asit vb.) veritabanından tarayarak açıklamalar yapar.

---

## 📊 Proje Mimarisi (Teknik Detaylar)

Proje, **Nesne Yönelimli Programlama (OOP)** prensiplerine sadık kalınarak geliştirilmiştir.

* `App` Sınıfı: Ana uygulama döngüsünü yönetir.
* `DB` Sınıfı: Kullanıcı verilerini ve skorları SQLite veritabanında yönetir.
* `EducationalTicker` Sınıfı: Kayan yazı animasyonlarını oluşturur.
* **Grafik Motoru:** Matplotlib ve Tkinter Canvas entegrasyonu ile dinamik çizimler yapılır.

---

**Geliştirici:** YİĞİT HAKTAN DİNLER
**Ders:** BOZ213 - NESNE TABANLI PROGRAMLAMA
**Tarih:** Ocak 2026

```

```
