"""
EDUQUEST: SCIENTIFIC DISCOVERY
TÜBİTAK 2209-A PROJESİ
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import random
import math
import time
import os
import datetime 
import difflib 
import string 

# --- KÜTÜPHANELER ---
try:
    import numpy as np
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    from matplotlib import style
    style.use("dark_background")
    import matplotlib.patches as patches
    from PIL import Image, ImageTk 
except ImportError:
    messagebox.showerror("Hata", "Gerekli kütüphaneler eksik.\nLütfen terminale şunu yazın:\npython -m pip install matplotlib numpy pillow")
    exit()

# =============================================================================
# [SİSTEM] AYARLAR
# =============================================================================
CFG = {
    "APP": "EDUQUEST PRO: LABORATORY v45.14",
    "DB": "eduquest_v45_final.db",
    "COLORS": {
        "BG": "#1e272e", "PANEL": "#2f3640", "SIDEBAR": "#191919",
        "ACCENT": "#00d2d3", "HIGHLIGHT": "#ff9f43", "SUCCESS": "#1dd1a1", 
        "ERR": "#ff6b6b", "TXT": "#f1f2f6", "INFO_BAR": "#2c3e50", "INFO_TXT": "#f1c40f",
        "ATOM_H": "#ffffff", "ATOM_O": "#ff6b6b", "ATOM_C": "#576574",
        "ATOM_N": "#54a0ff", "ATOM_CL": "#1dd1a1", "ATOM_NA": "#a29bfe", "ATOM_S": "#feca57",
        "ATOM_K": "#8e44ad", "ATOM_CA": "#bdc3c7", "ATOM_FE": "#d35400",
        "ATOM_HE": "#81ecec", "ATOM_MG": "#00b894"
    },
    "FONT": {
        "H1": ("Segoe UI", 24, "bold"), "H2": ("Segoe UI", 14, "bold"), "UI": ("Verdana", 11, "bold")
    },
    "FACTS": {
        "CHEM": (
            "💡 Su (H2O), polar kovalent bağa sahiptir. | "
            "💡 Asitlerin pH değeri 0-7 arasındadır, bazlarınki 7-14. | "
            "💡 Avogadro sayısı 6.02 x 10^23'tür. | "
            "💡 Soygazlar (8A grubu) kararlı oldukları için tepkimeye girmezler. | "
            "💡 Lavoisier, Kütlenin Korunumu Kanunu'nu bulmuştur. | "
            "💡 Atomun çekirdeğinde proton ve nötron bulunur. | "
            "💡 Elektronlar çekirdek etrafındaki orbitallerde hareket eder. | "
            "💡 Endotermik tepkimeler ısı alır, egzotermik tepkimeler ısı verir. | "
            "💡 Metaller elektron vererek katyon (+), ametaller elektron alarak anyon (-) oluşturur. | "
            "💡 Oksijen (O2) yanma tepkimelerinin olmazsa olmazıdır. | "
            "💡 En hafif element Hidrojen (H), en yoğun doğal element Osmiyum (Os)'dur. | "
            "💡 İyonik bağ, metal ve ametal arasında elektron alışverişi ile oluşur. | "
            "💡 Kovalent bağ, ametaller arasında elektron ortaklaşması ile oluşur. | "
            "💡 Sabun, hidrofil (suyu seven) ve hidrofob (suyu sevmeyen) uçlara sahiptir. | "
            "💡 DNA'nın yapısında Hidrojen bağları bulunur. | "
            "💡 Cıva (Hg), oda sıcaklığında sıvı olan tek metaldir. | "
            "💡 Karbonun allotropları: Elmas, Grafit ve Fulleren'dir. | "
            "💡 Mol kavramı, atomları saymak için kullanılan bir birimdir. | "
            "💡 Simyacılar, değersiz madenleri altına çevirmeye çalışmıştır (Felsefe Taşı). | "
            "💡 Periyodik tabloyu Dimitri Mendeleyev düzenlemiştir."
        ),
        "OPTIC": (
            "💡 Işık boşlukta saniyede 300.000 km hızla yayılır. | "
            "💡 Gelme açısı her zaman yansıma açısına eşittir. | "
            "💡 Çukur ayna ışığı toplar, tümsek ayna ışığı dağıtır. | "
            "💡 Hipermetrop yakını göremez, ince kenarlı mercekle düzeltilir. | "
            "💡 Miyop uzağı göremez, kalın kenarlı mercekle düzeltilir. | "
            "💡 Işık prizmadan geçerken renklere ayrılır (Gökkuşağı etkisi). | "
            "💡 Kırmızı, Yeşil ve Mavi (RGB) ışığın ana renkleridir. | "
            "💡 Siyah bir cisim üzerine düşen tüm ışığı soğurur. | "
            "💡 Beyaz bir cisim üzerine düşen tüm ışığı yansıtır. | "
            "💡 Kırılma indisi büyük olan ortamda ışık daha yavaş ilerler. | "
            "💡 Fiber optik kablolar 'Tam Yansıma' prensibiyle çalışır. | "
            "💡 İnsan gözü, 380nm ile 740nm arasındaki dalga boylarını görebilir. | "
            "💡 Düzlem aynada görüntü sanaldır ve cisimle aynı boydadır. | "
            "💡 Işık hem dalga hem de parçacık (foton) özelliği gösterir. | "
            "💡 Snell Yasası, ışığın kırılma açılarını hesaplar. | "
            "💡 Odak noktası (F), merceğin veya aynanın ışığı topladığı yerdir. | "
            "💡 Serap olayı, ışığın sıcak hava katmanlarında kırılmasıyla oluşur. | "
            "💡 Astronomik teleskoplar genellikle çukur ayna kullanır. | "
            "💡 Işık şiddetinin birimi Candela (cd)'dır. | "
            "💡 Lazer ışığı tek renkli (monokromatik) ve odaklanmış ışıktır."
        ),
        "GAME": (
            "💡 Bir sayının 0. kuvveti her zaman 1'dir. | "
            "💡 Fibonacci dizisi: 1, 1, 2, 3, 5, 8, 13, 21... | "
            "💡 Asal sayılar sadece 1'e ve kendisine bölünebilir. | "
            "💡 En küçük asal sayı 2'dir ve tek çift asal sayıdır. | "
            "💡 Pi sayısı (3.14...) sonsuza kadar devretmeden gider. | "
            "💡 Altın Oran (Phi) yaklaşık 1.618'dir. | "
            "💡 Bir üçgenin iç açıları toplamı 180 derecedir. | "
            "💡 Pisagor Teoremi: a² + b² = c² (Dik üçgenler için). | "
            "💡 0 faktöriyel (0!) 1'e eşittir. | "
            "💡 İkinci dereceden denklemlerin grafiği bir paraboldür. | "
            "💡 Olasılık değeri her zaman 0 ile 1 arasındadır. | "
            "💡 Koordinat sisteminde yatay eksen X, dikey eksen Y'dir. | "
            "💡 Logaritma, üs alma işleminin tersidir. | "
            "💡 Türev, bir fonksiyonun anlık değişim oranıdır. | "
            "💡 İntegral, bir eğrinin altında kalan alanı hesaplar. | "
            "💡 Karmaşık sayılar 'i' (sanal birim) içerir ve i² = -1'dir. | "
            "💡 Tam sayılar kümesi 'Z' harfi ile gösterilir. | "
            "💡 Doğal sayılar 0'dan başlar ve sonsuza gider. | "
            "💡 Fonksiyonlar girdi (x) alır ve çıktı (y) üretir. | "
            "💡 Matematik, evrenin dili olarak kabul edilir."
        ),
        "BIO": (
            "💡 Mitokondri, hücrenin enerji santralidir (ATP üretir). | "
            "💡 DNA, çift sarmal yapıdadır ve genetik bilgiyi taşır. | "
            "💡 İnsan vücudunda 206 adet kemik bulunur. | "
            "💡 Fotosentez denklemi: CO2 + Su + Işık -> Besin + Oksijen. | "
            "💡 En büyük organımız deridir. | "
            "💡 Kalp kası (Miyokard) yorulmadan çalışan tek kastır. | "
            "💡 Ribozomlar protein sentezinden sorumludur. | "
            "💡 Hücre zarı seçici geçirgendir. | "
            "💡 Doğal seçilim, çevreye uyum sağlayanların hayatta kalmasıdır. | "
            "💡 İnsan beyni yaklaşık 100 milyar nöron içerir. | "
            "💡 Alyuvarlar oksijen taşır, akyuvarlar mikroplarla savaşır. | "
            "💡 Enzimler biyolojik katalizörlerdir, tepkimeleri hızlandırır. | "
            "💡 Virüsler canlı değildir, çoğalmak için konağa ihtiyaç duyarlar. | "
            "💡 Homeostazi, vücudun iç dengesini koruma durumudur. | "
            "💡 Bakteriler prokaryot (çekirdeksiz) hücrelerdir. | "
            "💡 Mantarlar fotosentez yapmaz, heterotrofturlar. | "
            "💡 Ekosistemde enerji akışı tek yönlüdür (Güneş -> Üretici -> Tüketici). | "
            "💡 Kan grubu 0 olanlar genel vericidir. | "
            "💡 Kan grubu AB olanlar genel alıcıdır. | "
            "💡 İnsan genomu %99.9 oranında tüm insanlarda aynıdır."
        ),
        "MATH": (
            "💡 Yerçekimi ivmesi (g) yaklaşık 9.81 m/s²'dir. | "
            "💡 45 derece atış açısı, sürtünmesiz ortamda en uzun menzili verir. | "
            "💡 Hava direnci, hıza ve yüzey alanına bağlıdır. | "
            "💡 Eğik atışta cisim yatayda sabit hızla gider. | "
            "💡 Eğik atışta cisim düşeyde ivmeli hareket yapar. | "
            "💡 Newton'un 2. Yasası: F = m * a (Kuvvet = Kütle x İvme). | "
            "💡 Potansiyel enerji (mgh) yüksekliğe bağlıdır. | "
            "💡 Kinetik enerji (1/2mv²) hıza bağlıdır. | "
            "💡 Enerji yoktan var edilemez, vardan yok edilemez; dönüşür. | "
            "💡 Bir cismin ağırlığı gezegene göre değişir, kütlesi değişmez. | "
            "💡 Balistik, mermilerin hareketini inceleyen bilim dalıdır. | "
            "💡 Tepe noktasında cismin düşey hızı sıfırdır. | "
            "💡 Kurtulma hızı, bir gezegenin çekiminden kaçmak için gereken hızdır. | "
            "💡 Serbest düşme yapan cismin hızı her saniye yaklaşık 10 m/s artar. | "
            "💡 Moment, kuvvetin döndürme etkisidir. | "
            "💡 Sürtünme kuvveti harekete zıt yöndedir. | "
            "💡 Terminal hız, hava direncinin ağırlığa eşit olduğu andaki sabit hızdır. | "
            "💡 Vektörler hem büyüklük hem de yön belirtir. | "
            "💡 Skaler büyüklükler sadece sayısal değer belirtir. | "
            "💡 Mühendislikte hata payı (tolerans) hayati önem taşır."
        ),
        "HABIT": (
             "Zinciri kırma! Her gün yeni bir zaferdir. | "
             "Alışkanlıklar halat gibidir, her gün bir lif ekleriz ve koparamayacak hale geliriz. | "
             "Başlamak için mükemmel olmak zorunda değilsin, ama mükemmel olmak için başlamak zorundasın. | "
             "En zor adım, ilk adımdır. Devamı gelecektir. | "
             "Bugün gelecekteki kendin için bir iyilik yap. | "
             "İrade kas gibidir, kullandıkça güçlenir. | "
             "Vazgeçmek üzere olduğunda, neden başladığını hatırla. | "
             "Küçük değişimler zamanla büyük sonuçlar doğurur. | "
             "Başarı, her gün tekrarlanan küçük çabaların toplamıdır. | "
             "Kendine inan, bu alışkanlığı yenebilecek güç senin içinde. | "
             "Acı geçicidir, ama pes etmenin pişmanlığı sonsuzdur. | "
             "Disiplin, istediğin şey ile şu anki isteklerin arasındaki köprüdür. | "
             "Mazeret üretme, sonuç üret. | "
             "Yorgun olduğunda dinlen, vazgeçme. | "
             "En iyi intikam, muazzam bir başarıdır. | "
             "Dün bitti. Yarın gelmedi. Sadece bugün var. | "
             "Zorluklar seni durdurmak için değil, güçlendirmek içindir. | "
             "Bir saatlik çalışma, bir saatlik hayalden değerlidir. | "
             "Konfor alanında hiçbir şey büyümez. | "
             "Senin rakibin başkaları değil, dünkü kendinsin."
        ),
        "QUIZ": (
            "💡 Bilgi, paylaşıldıkça çoğalan tek hazinedir. | "
            "💡 Hata yapmak, öğrenmenin en önemli adımıdır. | "
            "💡 Bilim, gerçeğe giden en güvenilir yoldur. | "
            "💡 Sorgulamayan zihin, paslanmış demire benzer. | "
            "💡 EduQuest: Keşfet, Öğren ve Uygula. | "
            "💡 Başarı, her gün tekrarlanan küçük çabaların toplamıdır. | "
            "💡 Merak, bilimin kıvılcımıdır. | "
            "💡 Karma sorularla bilgilerini test et ve XP kazan! | "
            "💡 Biyoloji, Kimya, Fizik ve Matematik tek çatı altında. | "
            "💡 Doğru cevaplar seni zirveye taşır."
        ),
        "ELEC": (
            "💡 Ohm Yasası: V = I x R (Gerilim = Akım x Direnç). | "
            "💡 Aynı yüklü cisimler birbirini iter, zıt yüklü cisimler çeker. | "
            "💡 Seri bağlı ampullerin sayısı artarsa parlaklık azalır (Direnç artar). | "
            "💡 Paralel bağlı ampullerde parlaklık değişmez. | "
            "💡 Voltmetre devreye paralel, Ampermetre seri bağlanır. | "
            "💡 Elektrik akımı elektronların titreşim hareketiyle iletilir. | "
            "💡 Pil, kimyasal enerjiyi elektrik enerjisine dönüştürür. | "
            "💡 Bir iletkenin direnci; uzunluğuna, kesit alanına ve cinsine bağlıdır. | "
            "💡 Sigorta, devreyi yüksek akımdan koruyan güvenlik elemanıdır. | "
            "💡 Topraklama, fazla yükü toprağa aktararak güvenliği sağlar."
        ),
        "AI": (
            "💡 Prof. Pixel: Sorularına cevap vermek için buradayım! | "
            "💡 'DNA nedir?', 'Asit yağmuru nasıl oluşur?' gibi sorular sor. | "
            "💡 Bilimsel merak, keşfin ilk adımıdır. | "
            "💡 LGS konularına hakimim, beni test et! | "
            "💡 Bazen kelimeleri yanlış yazsan da seni anlamaya çalışırım."
        ),
        "ANALYTICS": (
            "💡 Ölçülemeyen şey geliştirilemez. | "
            "💡 Zayıf yönlerini bilmek, güçlenmenin ilk adımıdır. | "
            "💡 Veriler yalan söylemez, grafiğini analiz et! | "
            "💡 Dengeli bir bilim insanı her alanda yetkin olmalıdır. | "
            "💡 Radar grafiği alanını genişletmek senin elinde."
        )
    }
}

# --- GÜNCELLENMİŞ VE GENİŞLETİLMİŞ BİLİM SÖZLÜĞÜ (LGS KAPSAMLI) ---
SCIENCE_DB = {
    # --- 1. ÜNİTE: MEVSİMLER VE İKLİM ---
    "mevsim": "Dünya'nın eksen eğikliği (23°27') ve Güneş etrafındaki dolanma hareketi sonucu oluşur.",
    "eksen eğikliği": "Dünya'nın dönme ekseninin 23 derece 27 dakika eğik olmasıdır. Mevsimlerin temel sebebidir.",
    "iklim": "Geniş bir bölgede, uzun yıllar (en az 30-35 yıl) boyunca gözlemlenen ortalama hava olaylarıdır. Kesindir, değişkenlik azdır.",
    "hava durumu": "Dar bir alanda, kısa sürede değişebilen atmosfer olaylarıdır (Güneşli, Yağmurlu). Tahminidir.",
    "klimatolog": "İklim bilimci. İklimi inceleyen uzmandır.",
    "meteorolog": "Hava olaylarını inceleyen uzmandır.",
    "alçak basınç": "Havanın ısınarak yükseldiği, yağış ihtimalinin fazla olduğu alandır. Yükselici hava hareketi görülür.",
    "yüksek basınç": "Havanın soğuyarak alçaldığı, havanın açık olduğu alandır. Alçalıcı hava hareketi görülür.",
    "rüzgar": "Yüksek basınç alanından alçak basınç alanına doğru yatay yönlü hava hareketidir.",
    "küresel ısınma": "Sera gazlarının artmasıyla Dünya'nın ortalama sıcaklığının artmasıdır.",
    "21 haziran": "Kuzey Yarım Küre için yaz başlangıcıdır (Yaz gündönümü). En uzun gündüz yaşanır.",
    "21 aralık": "Kuzey Yarım Küre için kış başlangıcıdır (Kış gündönümü). En uzun gece yaşanır.",
    "ekinoks": "21 Mart ve 23 Eylül tarihleridir. Gece ve gündüz süreleri tüm dünyada eşittir.",

    # --- 2. ÜNİTE: DNA VE GENETİK KOD ---
    "dna": "Deoksiribo Nükleik Asit. Hücrenin yönetici molekülüdür. Çift sarmal yapıdadır.",
    "nükleotid": "DNA'nın en küçük yapı birimidir. Fosfat, Şeker (Deoksiriboz) ve Organik Bazdan oluşur.",
    "gen": "DNA üzerindeki görev birimidir. Kalıtsal özellikleri (göz rengi vb.) taşır.",
    "kromozom": "DNA'nın protein kılıfla paketlenmiş halidir. İnsanda 2n=46 tanedir.",
    "adenin": "DNA'da Timin ile eşleşen organik bazdır.",
    "guanin": "DNA'da Sitozin ile eşleşen organik bazdır.",
    "eşlenme": "DNA'nın kendini kopyalamasıdır. Hücre bölünmesinden hemen önce gerçekleşir.",
    "kalıtım": "Özelliklerin nesilden nesile aktarılmasıdır. Mendel 'Kalıtımın Babası'dır.",
    "fenotip": "Genetik ve çevrenin etkisiyle ortaya çıkan dış görünüştür.",
    "genotip": "Canlının sahip olduğu genlerin tamamıdır (AA, Aa, aa).",
    "baskın gen": "Her durumda etkisini gösteren gendir (Dominant). Büyük harfle gösterilir (A).",
    "çekinik gen": "Sadece saf dölde etkisini gösteren gendir (Resesif). Küçük harfle gösterilir (a).",
    "mutasyon": "DNA'nın yapısında radyasyon, kimyasal vb. ile oluşan ani değişimdir (Van kedisi, Altı parmaklılık).",
    "modifikasyon": "Çevre etkisiyle genlerin işleyişinin değişmesidir. Kalıtsal değildir (Kas yapma, Bronzlaşma).",
    "adaptasyon": "Canlının yaşama ve üreme şansını artıran kalıtsal uyumdur (Bukalemun renk değişimi, Kaktüs dikenleri).",
    "biyoteknoloji": "Canlıların yapısını değiştirerek yararlı ürün elde etmektir (GDO, Klonlama, İnsülin üretimi).",

    # --- 3. ÜNİTE: BASINÇ ---
    "basınç": "Birim yüzeye etki eden dik kuvvettir. P=F/S. Birimi Pascal (Pa).",
    "katı basıncı": "Ağırlık ile doğru, yüzey alanı ile ters orantılıdır. (Bıçak keskinleşirse basınç artar).",
    "sıvı basıncı": "Derinlik (h) ve yoğunluk (d) ile doğru orantılıdır. Kabın şekline bağlı DEĞİLDİR.",
    "pascal prensibi": "Kapalı kaptaki sıvıların, basıncı her yöne aynen iletmesidir (Hidrolik fren, Berber koltuğu).",
    "açık hava basıncı": "Atmosferin ağırlığıyla yaptığı basınçtır. Barometre ile ölçülür. Toriçelli bulmuştur.",
    "toriçelli": "Deniz seviyesinde, 0°C'de açık hava basıncını 76 cm-Hg olarak ölçen bilim insanıdır.",

    # --- 4. ÜNİTE: MADDE VE ENDÜSTRİ ---
    "periyodik tablo": "Elementlerin artan atom numaralarına göre dizildiği tablodur.",
    "grup": "Periyodik tablodaki dikey sütunlardır. 18 grup vardır. Aynı gruptakilerin kimyasal özellikleri benzerdir.",
    "periyot": "Periyodik tablodaki yatay satırlardır. 7 periyot vardır.",
    "metal": "Parlak, işlenebilir, elektriği iletir. Tablonun solundadır. Cıva hariç katıdır.",
    "ametal": "Mat, kırılgandır. Elektriği iletmez. Tablonun sağındadır.",
    "yarı metal": "Fiziksel olarak metale, kimyasal olarak ametale benzer (Bor, Silisyum).",
    "soygaz": "8A grubu. Kararlıdır, tepkimeye girmez (Helyum, Neon, Argon).",
    "fiziksel değişim": "Maddenin sadece dış görünüşü değişir (Erime, Yırtılma, Çözünme).",
    "kimyasal değişim": "Maddenin iç yapısı değişir, yeni madde oluşur (Yanma, Paslanma, Ekşime, Pişme).",
    "asit": "Suda H+ verir. Tadı ekşidir. pH < 7. Mavi turnusolu kırmızı yapar (Limon, Tuz ruhu).",
    "baz": "Suda OH- verir. Tadı acıdır. pH > 7. Kırmızı turnusolu mavi yapar. Ele kayganlık verir (Sabun, Deterjan).",
    "ph": "Asitlik-Bazlık derecesidir. 0-7 Asit, 7 Nötr, 7-14 Bazdır.",
    "asit yağmuru": "Fosil yakıtlardan çıkan SO2 ve NO2 gazlarının su buharıyla birleşip asit olarak yağmasıdır.",
    "özısı": "Maddenin 1 gramının sıcaklığını 1°C artırmak için gereken ısıdır. Ayırt edicidir. Özısısı büyük olan geç ısınıp geç soğur.",
    "ısı": "Enerjidir, birimi Joule'dür. Kalorimetre ile ölçülür.",
    "sıcaklık": "Enerji değildir, moleküllerin ortalama hareketidir. Termometre ile ölçülür.",

    # --- 5. ÜNİTE: BASİT MAKİNELER ---
    "basit makine": "İş yapma kolaylığı sağlar. İşten veya enerjiden kazanç ASLA olmaz.",
    "kaldıraç": "Destek noktası etrafında dönen çubuktur.",
    "sabit makara": "Kuvvetin yönünü değiştirir. Kuvvetten kazanç yoktur.",
    "hareketli makara": "Yükle beraber hareket eder. Kuvvetten 2 kat kazanç sağlar.",
    "palanga": "Sabit ve hareketli makara sistemidir.",
    "eğik düzlem": "Rampadır. Her zaman kuvvetten kazanç, yoldan kayıp vardır.",
    "çıkrık": "Eş merkezli silindirlerdir (Kuyu kolu, Direksiyon, Tornavida).",
    "dişli çark": "Hareketi aktarır, yönü ve hızı değiştirebilir.",

    # --- 6. ÜNİTE: ENERJİ DÖNÜŞÜMLERİ ---
    "fotosentez": "Kloroplastta; Işık, CO2 ve Su kullanılarak Besin ve Oksijen üretilmesidir.",
    "solunum": "Besinin parçalanarak ATP (enerji) üretilmesidir. Mitokondride olur.",
    "fermantasyon": "Oksijensiz solunumdur. Laktik asit (yoğurt/yorgunluk) veya Etil alkol (hamur) fermantasyonu vardır.",
    "besin zinciri": "Üretici -> Otçul -> Etçil. Enerji aktarımı tek yönlüdür.",
    "üretici": "Kendi besinini üreten canlılardır (Bitkiler, Algler, Siyanobakteriler).",

    # --- 7. ÜNİTE: ELEKTRİK YÜKLERİ ---
    "elektriklenme": "Sürtünme, dokunma veya etki ile yük dengesinin bozulmasıdır.",
    "pozitif yük": "Proton sayısı > Elektron sayısı.",
    "negatif yük": "Elektron sayısı > Proton sayısı.",
    "nötr": "Proton = Elektron.",
    "topraklama": "Yüklü cismi nötrlemek için toprağa bağlamaktır.",
    "elektroskop": "Yük cinsini ve varlığını anlamaya yarayan alettir. Yaprakları vardır.",

    # --- MATEMATİK & DİĞER ---
    "pisagor": "Dik üçgende a² + b² = c² bağıntısıdır.",
    "olasılık": "İstenen durum / Tüm durumlar.",
    "karekök": "Alanı verilen karenin bir kenarını bulma işlemidir.",
    "çarpan": "Bir sayıyı tam bölen sayılardır.",
    "ebob": "En Büyük Ortak Bölen.",
    "ekok": "En Küçük Ortak Kat.",
    "özdeşlik": "Bilinmeyenin her değeri için doğru olan eşitliktir (Tam kare, İki kare farkı).",

    # --- SOHBET ---
    "merhaba": "Merhaba genç bilim insanı! Bugün hangi konuyu tekrar etmek istersin?",
    "nasılsın": "Ben bir yapay zekayım ama devrelerim harika çalışıyor! Soru sormaya hazır mısın?",
    "yardım": "Bana 8. sınıf konularından terimler sorabilirsin. Örneğin: 'Mutasyon nedir?', 'Basınç neye bağlıdır?' veya 'DNA eşlenmesi nasıl olur?'",
    "kimsin": "Ben Prof. Pixel. LGS yolculuğunda sana yardımcı olmak için kodlandım."
}

# =============================================================================
# [MODÜL] KAYAN YAZI & DATABASE
# =============================================================================
class EducationalTicker(tk.Frame):
    def __init__(self, parent, text_content):
        super().__init__(parent, bg=CFG["COLORS"]["INFO_BAR"], height=35)
        self.pack_propagate(False)
        self.canvas = tk.Canvas(self, bg=CFG["COLORS"]["INFO_BAR"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.text_id = self.canvas.create_text(0, 18, text=text_content, fill=CFG["COLORS"]["INFO_TXT"], font=("Arial", 12, "bold"), anchor="w")
        self.text_width = self.canvas.bbox(self.text_id)[2]
        self.offset = 1400
        self.animate()

    def animate(self):
        try:
            if not self.winfo_exists(): return
            self.offset -= 2.5
            if self.offset < -self.text_width: self.offset = 1400
            self.canvas.coords(self.text_id, self.offset, 18)
            self.after(20, self.animate)
        except: pass

    def update_text(self, new_text):
        self.canvas.itemconfig(self.text_id, text=new_text)
        self.text_width = self.canvas.bbox(self.text_id)[2]

class DB:
    def __init__(self):
        self.conn = sqlite3.connect(CFG["DB"])
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, xp INTEGER DEFAULT 0)""")
        # Alışkanlıklar tablosu
        self.cur.execute("""CREATE TABLE IF NOT EXISTS habits (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, streak INTEGER DEFAULT 0, last_checkin TEXT)""")
        # Performans İstatistikleri Tablosu (YENİ EKLENTİ)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS performance (user_id INTEGER, category TEXT, correct INTEGER, total INTEGER, UNIQUE(user_id, category))""")
        self.conn.commit()

    def auth(self, u, p, m="login"):
        if m=="login": return self.cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p)).fetchone()
        try: 
            self.cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u,p))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def add_xp(self, uid, amt): 
        self.cur.execute("UPDATE users SET xp = xp + ? WHERE id=?", (amt, uid))
        self.conn.commit()

    # --- YENİ EKLENTİ: İSTATİSTİK GÜNCELLEME ---
    def update_stat(self, uid, cat, is_correct):
        # Önce var mı diye bak
        row = self.cur.execute("SELECT correct, total FROM performance WHERE user_id=? AND category=?", (uid, cat)).fetchone()
        if row:
            nc = row[0] + (1 if is_correct else 0)
            nt = row[1] + 1
            self.cur.execute("UPDATE performance SET correct=?, total=? WHERE user_id=? AND category=?", (nc, nt, uid, cat))
        else:
            nc = 1 if is_correct else 0
            self.cur.execute("INSERT INTO performance (user_id, category, correct, total) VALUES (?, ?, ?, 1)", (uid, cat, nc))
        self.conn.commit()

    def reset_db(self):
        self.cur.execute("DROP TABLE IF EXISTS users")
        self.cur.execute("DROP TABLE IF EXISTS habits")
        self.cur.execute("DROP TABLE IF EXISTS performance")
        self.create_table()

# =============================================================================
# [UYGULAMA] ANA ARAYÜZ
# =============================================================================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title(CFG["APP"])
        self.root.geometry("1400x900")
        self.root.configure(bg=CFG["COLORS"]["BG"])
        self.root.state('zoomed')
        self.db = DB(); self.user = None; self.ticker = None
        self.init_login()

    def clear(self):
        for w in self.root.winfo_children(): 
            if isinstance(w, tk.Frame) and getattr(w, "is_notification", False):
                continue
            w.destroy()

    # --- MODERN BİLDİRİM SİSTEMİ ---
    def show_notification(self, title, message, type_="info"):
        if type_ == "success":
            bg_col = CFG["COLORS"]["SUCCESS"]
            fg_col = "#1e272e"
            icon = "✓"
        elif type_ == "error":
            bg_col = CFG["COLORS"]["ERR"]
            fg_col = "white"
            icon = "✕"
        else:
            bg_col = CFG["COLORS"]["HIGHLIGHT"]
            fg_col = "#1e272e"
            icon = "!"

        notif_frame = tk.Frame(self.root, bg=bg_col, padx=20, pady=15, relief="flat")
        notif_frame.is_notification = True
        notif_frame.place(relx=0.5, rely=0.05, anchor="n")

        tk.Label(notif_frame, text=icon, font=("Arial", 24, "bold"), bg=bg_col, fg=fg_col).pack(side="left", padx=(0, 15))
        msg_frame = tk.Frame(notif_frame, bg=bg_col)
        msg_frame.pack(side="left")

        tk.Label(msg_frame, text=title, font=("Segoe UI", 12, "bold"), bg=bg_col, fg=fg_col).pack(anchor="w")
        tk.Label(msg_frame, text=message, font=("Segoe UI", 10), bg=bg_col, fg=fg_col).pack(anchor="w")

        close_btn = tk.Label(notif_frame, text="✖", font=("Arial", 10), bg=bg_col, fg=fg_col, cursor="hand2")
        close_btn.pack(side="right", padx=(15, 0), anchor="n")
        close_btn.bind("<Button-1>", lambda e: notif_frame.destroy())

        self.root.after(4000, lambda: notif_frame.destroy() if notif_frame.winfo_exists() else None)

    def reset_data(self):
        if messagebox.askyesno("DİKKAT", "Tüm kullanıcı verileri silinecek! Onaylıyor musun?"):
            self.db.reset_db()
            self.show_notification("Başarılı", "Veritabanı sıfırlandı.", "success")

    def init_login(self):
        self.clear()
        
        # --- GÖRSEL EFEKT: HAREKETLİ MOLEKÜLER AĞ ---
        bg_canvas = tk.Canvas(self.root, bg="#10151a", highlightthickness=0)
        bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        particles = []
        for _ in range(40): 
            particles.append({
                "x": random.randint(0, 1400), "y": random.randint(0, 900),
                "vx": random.choice([-1.5, -0.5, 0.5, 1.5]), "vy": random.choice([-1.5, -0.5, 0.5, 1.5]),
                "size": random.randint(2, 5)
            })

        def animate_bg():
            if not bg_canvas.winfo_exists(): return
            bg_canvas.delete("all")
            w, h = self.root.winfo_width(), self.root.winfo_height()
            
            for p in particles:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                if p["x"] <= 0 or p["x"] >= w: p["vx"] *= -1
                if p["y"] <= 0 or p["y"] >= h: p["vy"] *= -1
                bg_canvas.create_oval(p["x"], p["y"], p["x"]+p["size"], p["y"]+p["size"], fill="#444", outline="")
            for i in range(len(particles)):
                for j in range(i+1, len(particles)):
                    p1 = particles[i]; p2 = particles[j]
                    dist = math.hypot(p1["x"]-p2["x"], p1["y"]-p2["y"])
                    if dist < 150: 
                        opacity = int((150 - dist) / 150 * 100)
                        color = f"#{opacity:02x}{opacity:02x}{opacity:02x}"
                        if len(color) == 7:
                            bg_canvas.create_line(p1["x"], p1["y"], p2["x"], p2["y"], fill="#2f3640", width=1)
            self.root.after(40, animate_bg)  
        animate_bg()
        # ---------------------------------------------
        f = tk.Frame(self.root, bg=CFG["COLORS"]["PANEL"], padx=60, pady=60, relief="flat")
        f.place(relx=0.5, rely=0.5, anchor="center")
        tk.Frame(self.root, bg=CFG["COLORS"]["ACCENT"], width=5).place(relx=0.5, rely=0.5, anchor="center", height=500, width=500)
        f.lift() 
        tk.Label(f, text="EDUQUEST", font=("Impact", 48), fg=CFG["COLORS"]["ACCENT"], bg=CFG["COLORS"]["PANEL"]).pack()
        tk.Label(f, text="BİLİMSEL SİMÜLASYON MERKEZİ", font=("Arial", 12), fg="white", bg=CFG["COLORS"]["PANEL"]).pack(pady=10)
        tk.Label(f, text="Kullanıcı Adı (Min 8 Karakter):", bg=CFG["COLORS"]["PANEL"], fg="gray").pack(anchor="w")
        u = tk.Entry(f, font=("Arial", 14), bg="#dfe6e9", fg="#2d3436"); u.pack(pady=5, fill="x")
        
        tk.Label(f, text="Şifre (Min 8 Karakter + Rakam):", bg=CFG["COLORS"]["PANEL"], fg="gray").pack(anchor="w")
        p = tk.Entry(f, font=("Arial", 14), show="*", bg="#dfe6e9", fg="#2d3436"); p.pack(pady=5, fill="x")
        
        def go(m):
            user_val = u.get()
            pass_val = p.get()

            if not user_val or not pass_val:
                self.show_notification("Eksik Bilgi", "Lütfen kullanıcı adı ve şifre girin.", "warning")
                return

            if m == "reg":
                if len(user_val) < 8:
                    self.show_notification("Güvenlik Hatası", "Kullanıcı adı en az 8 karakter olmalıdır!", "error")
                    return
                has_digit = any(char.isdigit() for char in pass_val)
                if len(pass_val) < 8 or not has_digit:
                    self.show_notification("Zayıf Şifre", "Şifre en az 8 karakter ve 1 rakam içermelidir!", "error")
                    return

            if m == "reg":
                if self.db.auth(user_val, pass_val, "reg"):
                    self.show_notification("Kayıt Başarılı", "Hesabınız oluşturuldu. Şimdi giriş yapabilirsiniz.", "success")
                else:
                    self.show_notification("Kayıt Hatası", "Bu kullanıcı adı zaten alınmış.", "error")
            else:
                r = self.db.auth(user_val, pass_val)
                if r:
                    self.user = {"id": r[0], "name": r[1], "xp": r[3]}
                    self.show_notification("Giriş Başarılı", f"Hoş geldin, {self.user['name']}!", "success")
                    self.root.after(1000, self.init_dash)
                else:
                    self.show_notification("Giriş Başarısız", "Kullanıcı adı veya şifre hatalı.", "error")

        tk.Button(f, text="GİRİŞ YAP", bg=CFG["COLORS"]["SUCCESS"], fg="#1e272e", font=("Arial", 11, "bold"), width=20, command=lambda: go("log")).pack(pady=15)
        tk.Button(f, text="KAYIT OL", bg="#576574", fg="white", font=("Arial", 11, "bold"), width=20, command=lambda: go("reg")).pack()

        tk.Label(f, text="Sorun mu yaşıyorsun?", bg=CFG["COLORS"]["PANEL"], fg="gray", font=("Arial", 8)).pack(pady=(20, 5))
        tk.Button(f, text="VERİTABANINI SIFIRLA", bg=CFG["COLORS"]["ERR"], fg="white", font=("Arial", 8), command=self.reset_data).pack()

    def init_dash(self):
        self.clear()
        main = tk.Frame(self.root, bg=CFG["COLORS"]["BG"]); main.pack(fill="both", expand=True)
        bar = tk.Frame(main, bg=CFG["COLORS"]["SIDEBAR"], width=260); bar.pack(side="left", fill="y"); bar.pack_propagate(False)

        # --- YENİLENEN HOŞGELDİN EKRANI ---
        welcome_frame = tk.Frame(bar, bg=CFG["COLORS"]["SIDEBAR"])
        welcome_frame.pack(pady=40, fill="x", padx=10)

        tk.Label(welcome_frame, text="HOŞ GELDİN,", font=("Verdana", 10), bg=CFG["COLORS"]["SIDEBAR"], fg="#b2bec3").pack(anchor="w", padx=10)
        tk.Label(welcome_frame, text=self.user['name'].upper(), font=("Impact", 20), bg=CFG["COLORS"]["SIDEBAR"], fg=CFG["COLORS"]["ACCENT"]).pack(anchor="w", padx=10)

        self.xp_lbl = tk.Label(bar, text=f"✨ XP: {self.user['xp']}", fg="#feca57", bg=CFG["COLORS"]["SIDEBAR"], font=("Verdana", 14, "bold")); self.xp_lbl.pack(pady=(5, 20))

        tk.Frame(bar, height=2, bg="#444").pack(fill="x", pady=10, padx=20)

        # --- RENKLİ MENÜ SİSTEMİ ---
        # Format: (Görünen İsim, Fonksiyon, Veri Anahtarı, Buton Rengi)
        mods = [
            ("🧪 KİMYA LAB", self.mod_chem, "CHEM", "#6c5ce7"),       # Mor
            ("⚡ ELEKTRİK LAB", self.mod_electric_lab, "ELEC", "#fffa65"), # Sarı
            ("🔦 OPTİK LAB", self.mod_optics, "OPTIC", "#e17055"),       # Turuncu
            ("🧩 CEBİR & ZEKA", self.mod_algebra_game, "GAME", "#00cec9"), # Turkuaz
            ("🧬 BİYOLOJİ LAB", self.mod_bio_graph, "BIO", "#00b894"),    # Yeşil
            ("👷 MATEMATİK LAB", self.mod_math_eng, "MATH", "#0984e3"),  # Mavi
            ("🏆 BİLİM QUİZİ", self.mod_quiz, "QUIZ", "#f1c40f"),        # Altın Sarısı
            ("📊 PERFORMANS", self.mod_analytics, "ANALYTICS", "#e056fd"), # YENİ EKLENTİ
            ("🌱 İRADE YÖNETİMİ", self.mod_habit_tracker, "HABIT", "#2ecc71"), # Yeşil (İrade)
            ("🤖 AI SOHBET", self.mod_ai_chat, "AI", "#a55eea"), # YENİ EKLENTİ
            ("🚪 ÇIKIŞ YAP", self.init_login, "", "#d63031")              # Kırmızı
        ]

        for t, c, k, col in mods:
            btn_fg = "white" if col not in ["#f1c40f", "#fffa65"] else "#2d3436" # Sarı butonda siyah yazı
            tk.Button(bar, text=t, font=("Verdana", 10, "bold"), bg=col, fg=btn_fg, activebackground="white", activeforeground=col,
                      anchor="w", padx=20, pady=12, borderwidth=0, cursor="hand2",
                      command=lambda cmd=c, key=k: self.load_mod(cmd, key)).pack(fill="x", pady=4, padx=10)

        # =======================================================
        # [AKILLI RESİM YÜKLEYİCİ]
        # =======================================================
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            possible_names = ["avatar.jpg", "ChatGPT Image 18 Ara 2025 19_48_57.jpg", "avatar.jpg.jpg"]
            found_img = None
            for name in possible_names:
                full_path = os.path.join(script_dir, name)
                if os.path.exists(full_path):
                    found_img = full_path
                    break
            if found_img:
                pil_image = Image.open(found_img)
                base_width = 220
                w_percent = (base_width / float(pil_image.size[0]))
                h_size = int((float(pil_image.size[1]) * float(w_percent)))
                pil_image = pil_image.resize((base_width, h_size), Image.Resampling.LANCZOS)
                self.menu_photo = ImageTk.PhotoImage(pil_image)
                tk.Label(bar, image=self.menu_photo, bg=CFG["COLORS"]["SIDEBAR"], borderwidth=0).pack(side="bottom", pady=20)
            else:
                err_msg = f"Resim dosyası bulunamadı!\n\nLütfen 'avatar.jpg' dosyasını tam olarak şu klasörün içine koy:\n{script_dir}"
                print(err_msg)
        except Exception as e:
            print(f"Resim hatası: {e}")
        # =======================================================

        right = tk.Frame(main, bg=CFG["COLORS"]["BG"]); right.pack(side="right", fill="both", expand=True)
        self.work = tk.Frame(right, bg="#111"); self.work.pack(fill="both", expand=True, padx=20, pady=20)
        self.ticker = EducationalTicker(right, "Simülasyon Seçiniz..."); self.ticker.pack(fill="x", side="bottom")
        self.load_mod(self.mod_chem, "CHEM")

    def load_mod(self, func, key):
        for w in self.work.winfo_children(): w.destroy()
        if key: self.ticker.update_text(CFG["FACTS"][key])
        func()

    def set_header(self, title):
        h = tk.Frame(self.work, bg=CFG["COLORS"]["PANEL"], height=60); h.pack(fill="x")
        tk.Label(h, text=title, font=CFG["FONT"]["H1"], fg=CFG["COLORS"]["ACCENT"], bg=CFG["COLORS"]["PANEL"]).pack(side="left", padx=30)

    # [MODÜL 1] KİMYA
    def mod_chem(self):
        self.set_header("MOLEKÜL LABORATUVARI (LİSE MÜFREDATI)")
        left = tk.Frame(self.work, bg=CFG["COLORS"]["PANEL"], width=300); left.pack(side="left", fill="y", padx=10)
        tk.Label(left, text="ELEMENTLER", fg="white", bg=CFG["COLORS"]["PANEL"], font=CFG["FONT"]["H2"]).pack(pady=10)
        self.beaker_atoms = []
        self.cv_chem = tk.Canvas(self.work, bg="#2d3436", highlightthickness=0); self.cv_chem.pack(fill="both", expand=True)

        def reset_canvas():
            self.cv_chem.delete("all")
            self.cv_chem.create_rectangle(200, 150, 1000, 650, outline="white", width=3, dash=(10,10))
            self.cv_chem.create_text(600, 120, text="REAKSİYON BÖLGESİ", fill="white", font=("Segoe UI", 16, "bold"))

        reset_canvas()

        def add_atom(sym, col):
            rx, ry = random.randint(300, 900), random.randint(200, 600)
            r = 40
            pid = self.cv_chem.create_oval(rx-r, ry-r, rx+r, ry+r, fill=col, outline="white", width=3, tags="atom")
            tid = self.cv_chem.create_text(rx, ry, text=sym, font=("Arial", 24, "bold"), tags="atom")
            self.beaker_atoms.append({"type": sym, "id": pid, "tid": tid, "x": rx, "y": ry})

        self.drag_data = {"item": None, "x": 0, "y": 0}
        def on_press(e):
            item = self.cv_chem.find_closest(e.x, e.y)[0]
            if "atom" in self.cv_chem.gettags(item): self.drag_data["item"] = item; self.drag_data["x"] = e.x; self.drag_data["y"] = e.y
        def on_drag(e):
            if self.drag_data["item"]:
                dx, dy = e.x - self.drag_data["x"], e.y - self.drag_data["y"]
                target = next((a for a in self.beaker_atoms if a["id"] == self.drag_data["item"] or a["tid"] == self.drag_data["item"]), None)
                if target:
                    self.cv_chem.move(target["id"], dx, dy); self.cv_chem.move(target["tid"], dx, dy); target["x"] += dx; target["y"] += dy; check_bonds()
                self.drag_data["x"] = e.x; self.drag_data["y"] = e.y
        def check_bonds():
            self.cv_chem.delete("bond")
            for i, a1 in enumerate(self.beaker_atoms):
                for j, a2 in enumerate(self.beaker_atoms):
                    if i >= j: continue
                    if math.dist((a1["x"],a1["y"]), (a2["x"],a2["y"])) < 130:
                        self.cv_chem.create_line(a1["x"], a1["y"], a2["x"], a2["y"], fill="white", width=6, tags="bond"); self.cv_chem.tag_lower("bond")

        self.cv_chem.bind("<Button-1>", on_press); self.cv_chem.bind("<B1-Motion>", on_drag)
        self.cv_chem.bind("<ButtonRelease-1>", lambda e: setattr(self, 'drag_data', {"item": None, "x":0, "y":0}))

        elements = [
            ("Hidrojen", "H", CFG["COLORS"]["ATOM_H"]), ("Oksijen", "O", CFG["COLORS"]["ATOM_O"]),
            ("Karbon", "C", CFG["COLORS"]["ATOM_C"]), ("Azot", "N", CFG["COLORS"]["ATOM_N"]),
            ("Klor", "Cl", CFG["COLORS"]["ATOM_CL"]), ("Sodyum", "Na", CFG["COLORS"]["ATOM_NA"]),
            ("Kükürt", "S", CFG["COLORS"]["ATOM_S"]), ("Potasyum", "K", CFG["COLORS"]["ATOM_K"]),
            ("Kalsiyum", "Ca", CFG["COLORS"]["ATOM_CA"]), ("Demir", "Fe", CFG["COLORS"]["ATOM_FE"]),
            ("Helyum", "He", CFG["COLORS"]["ATOM_HE"]), ("Magnezyum", "Mg", CFG["COLORS"]["ATOM_MG"])
        ]

        for n, s, c in elements:
            tk.Button(left, text=n, bg=c, fg="black" if c=="#ffffff" else "white", font=("Arial", 10, "bold"), pady=2, command=lambda sy=s, co=c: add_atom(sy, co)).pack(fill="x", pady=2)

        def react():
            c = {k:0 for k in ["H","O","C","N","Cl","Na","S","K","Ca","Fe","He","Mg"]}
            for a in self.beaker_atoms: c[a["type"]] += 1
            res, desc, col = "TEPKİME YOK", "Kararsız yapı veya eksik atom.", CFG["COLORS"]["ERR"]
            total_atoms = sum(c.values())
            
            # --- YAYGIN BİLEŞİKLER (TYT/AYT) ---
            # 1. SU ve OKSİTLER
            if c["H"]==2 and c["O"]==1 and total_atoms==3: 
                res, desc, col = "H₂O (Su)", "Yaşam kaynağı. Polar bileşik.", CFG["COLORS"]["SUCCESS"]
            elif c["C"]==1 and c["O"]==2 and total_atoms==3: 
                res, desc, col = "CO₂", "Karbondioksit. Sera gazı.", "#a29bfe"
            elif c["S"]==1 and c["O"]==2 and total_atoms==3:
                res, desc, col = "SO₂", "Kükürt Dioksit (Asit yağmuru öncülü).", "#ffcc00"
            elif c["S"]==1 and c["O"]==3 and total_atoms==4:
                res, desc, col = "SO₃", "Kükürt Trioksit.", "#ffcc00"
            elif c["Mg"]==1 and c["O"]==1 and total_atoms==2:
                res, desc, col = "MgO", "Magnezyum Oksit (Bazik oksit).", "white"
            elif c["Ca"]==1 and c["O"]==1 and total_atoms==2:
                res, desc, col = "CaO", "Sönmemiş Kireç.", "white"
            elif c["Fe"]==2 and c["O"]==3 and total_atoms==5: 
                res, desc, col = "Fe₂O₃", "Pas (Demir III Oksit).", "#d35400"
            
            # 2. ASİTLER (Kuvvetli ve Zayıf)
            elif c["H"]==1 and c["Cl"]==1 and total_atoms==2: 
                res, desc, col = "HCl", "Tuz Ruhu (Hidroklorik Asit).", "#ff7675"
            elif c["H"]==2 and c["S"]==1 and c["O"]==4 and total_atoms==7:
                res, desc, col = "H₂SO₄", "Zaç Yağı (Sülfürik Asit). Akü asidi.", "#e17055"
            elif c["H"]==1 and c["N"]==1 and c["O"]==3 and total_atoms==5:
                res, desc, col = "HNO₃", "Kezzap (Nitrik Asit).", "#ff7675"
            elif c["C"]==2 and c["H"]==4 and c["O"]==2 and total_atoms==8:
                res, desc, col = "CH₃COOH", "Sirke Asidi (Asetik Asit).", "#fab1a0"

            # 3. BAZLAR
            elif c["N"]==1 and c["H"]==3 and total_atoms==4:
                res, desc, col = "NH₃", "Amonyak (Zayıf Baz). Susuz baz.", "#74b9ff"
            elif c["Na"]==1 and c["O"]==1 and c["H"]==1 and total_atoms==3:
                res, desc, col = "NaOH", "Sud Kostik (Sodyum Hidroksit). Sabun yapımı.", "#dfe6e9"
            elif c["K"]==1 and c["O"]==1 and c["H"]==1 and total_atoms==3:
                res, desc, col = "KOH", "Potas Kostik (Potasyum Hidroksit). Arap sabunu.", "#dfe6e9"
            elif c["Ca"]==1 and c["O"]==2 and c["H"]==2 and total_atoms==5:
                res, desc, col = "Ca(OH)₂", "Sönmüş Kireç.", "white"

            # 4. TUZLAR
            elif c["Na"]==1 and c["Cl"]==1 and total_atoms==2: 
                res, desc, col = "NaCl", "Sofra Tuzu.", "white"
            elif c["K"]==1 and c["Cl"]==1 and total_atoms==2:
                res, desc, col = "KCl", "Potasyum Klorür.", "white"
            elif c["Ca"]==1 and c["C"]==1 and c["O"]==3 and total_atoms==5:
                res, desc, col = "CaCO₃", "Kireç Taşı (Mermer/Tebeşir).", "white"

            # 5. ORGANİK
            elif c["C"]==1 and c["H"]==4 and total_atoms==5:
                res, desc, col = "CH₄", "Metan Gazı (Doğalgazın ana bileşeni).", "#55efc4"
            elif c["C"]==6 and c["H"]==12 and c["O"]==6 and total_atoms==24:
                res, desc, col = "C₆H₁₂O₆", "Glikoz (Basit Şeker).", "#ffeaa7"

            # 6. SOYGAZLAR
            elif c["He"]>0 and total_atoms==c["He"]: 
                res, desc, col = "He", "Soygaz (Tepkime vermez).", "#81ecec"
            
            self.cv_chem.delete("res"); self.cv_chem.create_text(600, 80, text=f"{res}\n{desc}", fill=col, font=("Arial", 20, "bold"), tags="res")
            if res != "TEPKİME YOK": 
                self.db.add_xp(self.user["id"], 25); self.xp_lbl.config(text=f"XP: {self.user['xp'] + 25}")
                self.show_notification("Keşif!", f"{res} molekülü oluşturuldu!", "success")
                self.db.update_stat(self.user["id"], "Kimya", True) # Eklenti

        tk.Button(left, text="KONTROL ET", bg=CFG["COLORS"]["HIGHLIGHT"], fg="black", font=("Arial", 12, "bold"), command=react).pack(pady=10, fill="x")
        tk.Button(left, text="TEMİZLE", bg="gray", fg="white", font=("Arial", 12, "bold"), command=lambda: [reset_canvas(), self.beaker_atoms.clear()]).pack(fill="x")

    # [MODÜL 2] OPTİK
    def mod_optics(self):
        self.set_header("OPTİK LABORATUVARI: IŞIN İZLEME")
        cv = tk.Canvas(self.work, bg="#000000", highlightthickness=0); cv.pack(fill="both", expand=True)
        self.opt_level_data = {"target": (900, 150), "obstacles": [(400, 300, 420, 600), (600, 100, 620, 400)]}
        source = (100, 450)
        mirrors = []

        def draw_base():
            cv.delete("all")
            # Grid
            for i in range(0, 1400, 50): cv.create_line(i,0,i,900, fill="#111")
            for i in range(0, 900, 50): cv.create_line(0,i,1400,i, fill="#111")
            
            # Lazer (Silah)
            sx, sy = source
            cv.create_rectangle(sx-30, sy-20, sx+10, sy+20, fill="#2d3436", outline="#636e72", width=2)
            cv.create_rectangle(sx+10, sy-5, sx+25, sy+5, fill="#e17055", outline="")
            cv.create_text(sx-10, sy, text="LASER", fill="white", font=("Arial", 8, "bold"))
            
            # Hedef (Bullseye)
            tx, ty = self.opt_level_data["target"]
            cv.create_oval(tx-30, ty-30, tx+30, ty+30, fill="white", outline="#d63031", width=2)
            cv.create_oval(tx-20, ty-20, tx+20, ty+20, fill="#d63031", outline="white")
            cv.create_oval(tx-10, ty-10, tx+10, ty+10, fill="white", outline="")
            cv.create_oval(tx-4, ty-4, tx+4, ty+4, fill="#d63031", outline="")

            # Engeller
            for o in self.opt_level_data["obstacles"]: cv.create_rectangle(o, fill="#2d3436", outline="#636e72", width=2)
            # Aynalar
            for m in mirrors:
                x, y, type_ = m
                if type_ == "/":
                    cv.create_line(x-20, y+20, x+20, y-20, fill="#74b9ff", width=6, capstyle=tk.ROUND)
                else:
                    cv.create_line(x-20, y-20, x+20, y+20, fill="#74b9ff", width=6, capstyle=tk.ROUND)

        draw_base()

        def generate_level():
            tx = random.randint(400, 1000) // 50 * 50
            ty = random.randint(100, 600) // 50 * 50
            new_obs = []
            for _ in range(random.randint(2, 5)):
                ox = random.randint(300, 1100) // 50 * 50
                oy = random.randint(50, 600) // 50 * 50
                if math.dist((ox, oy), (100, 450)) > 150 and math.dist((ox, oy), (tx, ty)) > 100:
                    new_obs.append((ox, oy, ox+20, oy+random.randint(100, 300)))
            self.opt_level_data = {"target": (tx, ty), "obstacles": new_obs}
            mirrors.clear()
            draw_base()
            self.show_notification("Yeni Seviye", "Hedef ve Engeller Değişti!", "info")

        def add_mirror(e): 
            mirrors.append((round(e.x/50)*50, round(e.y/50)*50, "/"))
            draw_base()
        def remove_mirror(e): 
            x, y = round(e.x/50)*50, round(e.y/50)*50
            [mirrors.remove(m) for m in mirrors if m[0]==x and m[1]==y]
            draw_base()
        def rotate_mirror(e): 
            x, y = round(e.x/50)*50, round(e.y/50)*50
            for i, m in enumerate(mirrors):
                if m[0]==x and m[1]==y: mirrors[i] = (m[0], m[1], "\\" if m[2]=="/" else "/")
            draw_base()
            
        cv.bind("<Button-1>", add_mirror); cv.bind("<Button-2>", remove_mirror); cv.bind("<Button-3>", rotate_mirror)

        def fire():
            draw_base()
            lx, ly = source[0] + 25, source[1] 
            vx, vy = 1, 0 
            path = [(lx, ly)]
            for _ in range(50):
                hit = False
                for step in range(1, 2000, 5):
                    nx = lx + vx * step; ny = ly + vy * step
                    if math.dist((nx, ny), self.opt_level_data["target"]) < 30:
                        path.append((nx, ny))
                        cv.create_line(path, fill=CFG["COLORS"]["SUCCESS"], width=4)
                        self.db.add_xp(self.user["id"], 50)
                        self.show_notification("Harika!", "Hedef Vuruldu! +50 XP", "success")
                        self.db.update_stat(self.user["id"], "Fizik", True) # Eklenti
                        return
                    for o in self.opt_level_data["obstacles"]:
                        if o[0] < nx < o[2] and o[1] < ny < o[3]:
                            path.append((nx, ny)); hit = True; break
                    if hit: break
                    for m in mirrors:
                        if math.dist((nx, ny), (m[0], m[1])) < 20:
                            path.append((m[0], m[1]))
                            if m[2] == "/": vx, vy = -vy, -vx
                            else: vx, vy = vy, vx
                            lx = m[0] + vx * 25; ly = m[1] + vy * 25; hit = True; break
                    if hit: break
                if not hit: path.append((nx, ny)); break
            cv.create_line(path, fill="#ff7675", width=3, arrow=tk.LAST)

        ctrl = tk.Frame(self.work, bg=CFG["COLORS"]["PANEL"], height=60); ctrl.pack(side="bottom", fill="x")
        tk.Button(ctrl, text="🔴 ATEŞLE", bg="#e74c3c", fg="white", font=("Arial", 11, "bold"), command=fire).pack(side="left", padx=20, pady=10)
        tk.Button(ctrl, text="🎲 YENİ SEVİYE", bg=CFG["COLORS"]["ACCENT"], fg="black", font=("Arial", 11, "bold"), command=generate_level).pack(side="left", pady=10)
        tk.Label(ctrl, text="Sol Tık: Ayna Ekle | Sağ Tık: Çevir", bg=CFG["COLORS"]["PANEL"], fg="white").pack(side="right", padx=20)

    # [MODÜL 3] OYUN: CEBİR KAPISI (ADAPTIVE DIFFICULTY)
    def mod_algebra_game(self):
        self.set_header("CEBİR & GEOMETRİ TAPINAĞI")
        
        if not hasattr(self, 'alg_level'): 
            self.alg_level = 1
            self.alg_score = 0
            self.alg_streak = 0
            
        self.puzzle_data = {}
        
        # --- ÜST BİLGİ PANELİ ---
        top_frame = tk.Frame(self.work, bg="#222", relief="ridge", bd=2)
        top_frame.pack(fill="x", pady=10, padx=50)
        lbl_info = tk.Label(top_frame, text=f"SEVİYE: {self.alg_level} | PUAN: {self.alg_score}", 
                           font=("Consolas", 18, "bold"), bg="#222", fg=CFG["COLORS"]["HIGHLIGHT"])
        lbl_info.pack(pady=5)
        
        # --- ANA ÇİZİM ALANI ---
        cv = tk.Canvas(self.work, bg="#2d3436", height=480, highlightthickness=0)
        cv.pack(fill="x", padx=50, pady=10)
        
        math_symbols = ["π", "∑", "∫", "√", "∞", "≠", "≈", "θ", "λ", "α", "β", "∆", "fx"]
        def draw_background_atmosphere():
            w = cv.winfo_width() if cv.winfo_width() > 1 else 1300
            h = 480
            for _ in range(15):
                sx, sy = random.randint(50, w-50), random.randint(50, h-50)
                sym = random.choice(math_symbols)
                size = random.randint(20, 60)
                color = "#353b48"
                cv.create_text(sx, sy, text=sym, font=("Times New Roman", size, "bold"), fill=color, tags="bg_decor")

        def generate_puzzle():
            lvl = self.alg_level
            mode = "algebra" 
            if lvl >= 2 and random.random() > 0.4:
                mode = "geometry"
            q_text = ""; ans = 0; geo_data = None 

            if mode == "geometry":
                geo_type = random.choice(["triangle", "rectangle"])
                if geo_type == "triangle":
                    angle_a = random.randint(30, 80)
                    angle_b = random.randint(30, 80)
                    angle_c = 180 - (angle_a + angle_b)
                    missing = random.choice(["A", "B", "C"])
                    if missing == "C":
                        ans = angle_c
                        geo_data = {"type": "triangle", "vals": (angle_a, angle_b, "?"), "ans_pos": "top"}
                        q_text = "Verilen üçgende '?' kaç derecedir?"
                    elif missing == "A":
                        ans = angle_a
                        geo_data = {"type": "triangle", "vals": ("?", angle_b, angle_c), "ans_pos": "left"}
                        q_text = "Verilen üçgende '?' kaç derecedir?"
                    else:
                        ans = angle_b
                        geo_data = {"type": "triangle", "vals": (angle_a, "?", angle_c), "ans_pos": "right"}
                        q_text = "Verilen üçgende '?' kaç derecedir?"
                elif geo_type == "rectangle":
                    side_a = random.randint(4, 12)
                    side_b = random.randint(5, 15)
                    area = side_a * side_b
                    if random.choice([True, False]): # Alanı sor
                        ans = area
                        geo_data = {"type": "rect_area", "sides": (side_a, side_b)}
                        q_text = "Şeklin ALANI kaç birim karedir?"
                    else: # Kenarı sor
                        ans = side_b
                        geo_data = {"type": "rect_side", "sides": (side_a, "?"), "area": area}
                        q_text = f"Alan = {area} br² ise '?' kaçtır?"
            else: 
                # --- KLASİK CEBİR (ALGEBRA) ---
                if lvl <= 3:
                    a = random.randint(2, 6); x = random.randint(2, 12); b = random.randint(5, 30)
                    rhs = a * x + b
                    q_text = f"{a}x + {b} = {rhs}\n\nx = ?"
                    ans = x
                elif lvl <= 6:
                    if random.random() > 0.5:
                        base = random.randint(2, 5); exp = random.randint(2, 4)
                        res = base ** exp
                        q_text = f"{base} üssü x = {res}\n({base}ˣ = {res})\n\nx = ?"
                        ans = exp
                    else:
                        n = random.randint(4, 6)
                        q_text = f"{n}! - {n-1}! = ?\n(İpucu: Faktöriyel)"
                        ans = math.factorial(n) - math.factorial(n-1)
                else:
                    start = random.randint(1, 10); step = random.randint(2, 7)
                    seq = [start, start+step, start+step*2, "?"]
                    q_text = f"Dizi: {start}, {start+step}, {start+step*2}, ...\n4. terim nedir?"
                    ans = start + step*3
            self.puzzle_data = {"answer": ans, "text": q_text, "mode": mode, "geo": geo_data}
            draw_door("locked")

        def draw_door(state="locked"):
            cv.delete("all")
            w = cv.winfo_width() if cv.winfo_width() > 1 else 1000
            cx = w / 2
            cy = 240
            draw_background_atmosphere()
            
            # --- KAPI ÇERÇEVESİ ---
            cv.create_rectangle(cx-220, 20, cx-180, 460, fill="#2f3542", outline="#57606f", width=3) # Sol
            cv.create_rectangle(cx+180, 20, cx+220, 460, fill="#2f3542", outline="#57606f", width=3) # Sağ
            cv.create_rectangle(cx-240, 20, cx+240, 80, fill="#2f3542", outline="#57606f", width=3) # Üst
            cv.create_text(cx, 50, text="∑ P Y T H A G O R A S ∑", font=("Times New Roman", 20, "bold"), fill="#a4b0be")

            # --- KAPI GÖVDESİ ---
            door_color = "#1e272e" if state == "locked" else "#000000"
            outline_color = "#e17055" if state == "locked" else CFG["COLORS"]["SUCCESS"]
            cv.create_rectangle(cx-180, 80, cx+180, 460, fill=door_color, outline=outline_color, width=4)
            
            if state == "locked":
                cv.create_oval(cx-30, 100, cx+30, 160, outline=outline_color, width=3)
                cv.create_rectangle(cx-20, 160, cx+20, 190, fill=outline_color)
                cv.create_text(cx, 130, text="🔒", font=("Arial", 20))
                
                # --- SORU GÖSTERİMİ ---
                if self.puzzle_data.get("mode") == "geometry":
                    gd = self.puzzle_data["geo"]
                    offset_y = 280
                    if gd["type"] == "triangle":
                        p1 = (cx, offset_y - 80)
                        p2 = (cx - 80, offset_y + 60)
                        p3 = (cx + 80, offset_y + 60)
                        cv.create_polygon(p1, p2, p3, outline="white", fill="", width=3)
                        vals = gd["vals"]
                        cv.create_text(p1[0], p1[1]-20, text=str(vals[2])+"°", fill="#ff9f43", font=("Arial", 14, "bold"))
                        cv.create_text(p2[0]-25, p2[1], text=str(vals[0])+"°", fill="#ff9f43", font=("Arial", 14, "bold"))
                        cv.create_text(p3[0]+25, p3[1], text=str(vals[1])+"°", fill="#ff9f43", font=("Arial", 14, "bold"))
                    elif "rect" in gd["type"]:
                        rx, ry = cx - 70, offset_y - 50
                        cv.create_rectangle(rx, ry, rx+140, ry+100, outline="white", width=3)
                        sides = gd["sides"]
                        # Kenar Yazıları
                        cv.create_text(rx-20, ry+50, text=str(sides[0]), fill="#00d2d3", font=("Arial", 14, "bold")) # Sol kenar
                        cv.create_text(rx+70, ry+120, text=str(sides[1]), fill="#00d2d3", font=("Arial", 14, "bold")) # Alt kenar
                        
                        if "area" in gd:
                             cv.create_text(cx, ry+50, text=f"ALAN\n{gd['area']}", fill="white", font=("Arial", 12), justify="center")

                    # Soru Metni (Alta)
                    cv.create_text(cx, 420, text=self.puzzle_data["text"], fill="white", font=("Arial", 14, "bold"), justify="center")

                else:
                    # Klasik Metin Sorusu
                    q_lines = self.puzzle_data.get("text", "Yükleniyor...").split("\n")
                    y_offset = 250
                    for line in q_lines:
                        cv.create_text(cx, y_offset, text=line, font=("Courier New", 22, "bold"), fill="white")
                        y_offset += 40

            elif state == "open":
                # Açık Kapı Efekti (İçerisi parlıyor)
                for i in range(10, 0, -1):
                      cv.create_oval(cx-10*i, 270-15*i, cx+10*i, 270+15*i, fill=None, outline=CFG["COLORS"]["SUCCESS"], width=2)
                
                cv.create_text(cx, 250, text="KAPI AÇILDI", font=("Impact", 32), fill=CFG["COLORS"]["SUCCESS"])
                cv.create_text(cx, 300, text="DOĞRU CEVAP!", font=("Arial", 16, "bold"), fill="white")

        # --- ALT KONTROL PANELİ ---
        btm_frame = tk.Frame(self.work, bg=CFG["COLORS"]["PANEL"], pady=15, relief="flat")
        btm_frame.pack(fill="x", side="bottom")
        
        lbl_msg = tk.Label(btm_frame, text="Şifreyi Çöz ve Giriş Yap...", font=("Arial", 11), bg=CFG["COLORS"]["PANEL"], fg="#dfe6e9")
        lbl_msg.pack(side="top", pady=(0, 5))
        
        input_container = tk.Frame(btm_frame, bg=CFG["COLORS"]["PANEL"])
        input_container.pack()

        entry_x = tk.Entry(input_container, font=("Consolas", 24, "bold"), width=8, justify="center", bg="#dfe6e9", fg="#2d3436", bd=4, relief="sunken")
        entry_x.pack(side="left", padx=10)
        entry_x.focus()

        def check_answer(e=None):
            try:
                user_ans = int(entry_x.get())
                is_correct = (user_ans == self.puzzle_data["answer"])
                self.db.update_stat(self.user["id"], "Matematik", is_correct)

                if is_correct:
                    earned_xp = 15 * self.alg_level + (10 if self.puzzle_data.get("mode") == "geometry" else 0)
                    self.alg_score += earned_xp
                    self.alg_streak += 1
                    
                    self.db.add_xp(self.user["id"], earned_xp)
                    self.xp_lbl.config(text=f"XP: {self.user['xp'] + earned_xp}")
                    
                    draw_door("open")
                    lbl_msg.config(text=f"MÜKEMMEL! +{earned_xp} PUAN", fg=CFG["COLORS"]["SUCCESS"])
                    
                    # Seviye Atlama Kontrolü
                    if self.alg_streak >= 3:
                        self.alg_level += 1
                        self.alg_streak = 0
                        lbl_msg.config(text=f"SEVİYE ATLADIN! ŞİMDİ SEVİYE {self.alg_level}", fg="#f1c40f")
                    
                    lbl_info.config(text=f"SEVİYE: {self.alg_level} | PUAN: {self.alg_score}")
                    self.work.after(1500, generate_puzzle)
                else:
                    self.alg_streak = 0
                    lbl_msg.config(text="YANLIŞ ŞİFRE! Tekrar dene.", fg=CFG["COLORS"]["ERR"])
                    entry_x.config(bg="#ff7675")
                    self.work.after(500, lambda: entry_x.config(bg="#dfe6e9"))
                
                entry_x.delete(0, tk.END)
            except ValueError:
                lbl_msg.config(text="Sadece SAYI giriniz!", fg="orange")

        btn_check = tk.Button(input_container, text="KİLİDİ AÇ", bg=CFG["COLORS"]["ACCENT"], fg="black", 
                             font=("Arial", 12, "bold"), padx=20, pady=5, cursor="hand2", command=check_answer)
        btn_check.pack(side="left", padx=10)

        entry_x.bind("<Return>", check_answer)
        # İlk bulmacayı başlat
        self.work.after(100, generate_puzzle)

    # [MODÜL 4] BİYOLOJİ: GELİŞMİŞ POPÜLASYON SİMÜLASYONU (GÜNCELLENDİ)
    def mod_bio_graph(self):
        self.set_header("EKOSİSTEM LABORATUVARI: DOĞAL SEÇİLİM")
        
        # --- KONTROL PANELİ ---
        ctrl_frame = tk.Frame(self.work, bg=CFG["COLORS"]["PANEL"], padx=10, pady=10)
        ctrl_frame.pack(fill="x", pady=10)
        
        # Sol Panel: Temel Kontroller
        left_ctrl = tk.Frame(ctrl_frame, bg=CFG["COLORS"]["PANEL"])
        left_ctrl.pack(side="left")
        
        s_rate = tk.Scale(left_ctrl, from_=0.05, to=0.3, resolution=0.01, orient="horizontal", 
                          bg=CFG["COLORS"]["PANEL"], fg="white", label="Tavşan Üreme Hızı", length=180)
        s_rate.set(0.15); s_rate.pack(side="left", padx=10)
        
        # --- GRAFİK ALANI ---
        fig = Figure(figsize=(5, 4), dpi=100); ax = fig.add_subplot(111); ax.set_facecolor("#1e272e")
        canvas = FigureCanvasTkAgg(fig, master=self.work); canvas.get_tk_widget().pack(fill="both", expand=True)
        
        lbl_status = tk.Label(self.work, text="SİMÜLASYON HAZIR", font=("Consolas", 11), bg="#222", fg="white", pady=10)
        lbl_status.pack(fill="x")

        # --- SİMÜLASYON DEĞİŞKENLERİ ---
        self.bio_running = False
        self.bio_camouflage = False # Yeni: Kamuflaj durumu
        self.bio_winter = False     # Yeni: Kış durumu
        
        r, w, t_arr = [50], [20], [0] # Rabbit, Wolf, Time
        time_step = 0
        
        # --- YENİ FONKSİYONLAR ---
        def run_sim():
            self.bio_running = not self.bio_running
            btn_start.config(text="⏸️ DURAKLAT" if self.bio_running else "▶️ BAŞLAT", 
                             bg="orange" if self.bio_running else CFG["COLORS"]["SUCCESS"])
            if self.bio_running: update()

        def toggle_camouflage():
            self.bio_camouflage = not self.bio_camouflage
            if self.bio_camouflage:
                btn_cam.config(text="🧬 KAMUFLAJ: AKTİF", bg="#00d2d3", fg="black")
                self.show_notification("Adaptasyon", "Tavşanlar çevreye uyum sağladı! (Avlanma oranı düştü)", "success")
            else:
                btn_cam.config(text="🧬 KAMUFLAJ MUTASYONU", bg="#34495e", fg="white")

        def toggle_winter():
            self.bio_winter = not self.bio_winter
            if self.bio_winter:
                btn_winter.config(text="❄️ SERT KIŞ MODU", bg="#74b9ff", fg="black")
                self.show_notification("Çevresel Faktör", "Kış geldi! Besin azaldı, hayatta kalmak zorlaştı.", "info")
            else:
                btn_winter.config(text="☀️ YAZ MODU", bg="#e17055", fg="black")
                self.show_notification("Çevresel Faktör", "Yaz geldi! Besin bolluğu başladı.", "success")

        def trigger_migration():
            r[-1] += 50
            self.show_notification("Göç Dalgası", "Bölgeye 50 yeni tavşan göç etti!", "info")

        def trigger_epidemic():
            if len(r) > 0:
                r[-1] = r[-1] * 0.3
                w[-1] = w[-1] * 0.8
                self.show_notification("Biyolojik Tehdit!", "Salgın hastalık popülasyonu çökertti!", "error")

        # --- GÜNCELLENMİŞ MATEMATİKSEL DÖNGÜ ---
        def update():
            try:
                if not s_rate.winfo_exists(): return
            except tk.TclError: return

            nonlocal time_step
            if not self.bio_running: return
            
            dt = 0.2
            # 1. Parametreleri Al
            alpha = s_rate.get() # Tavşan Doğum
            beta = 0.005         # Tavşan Ölüm (Avlanma)
            delta = 0.003        # Kurt Doğum
            gamma = 0.1          # Kurt Ölüm

            # 2. Etkileşimleri Uygula
            if self.bio_camouflage: beta = 0.002
            if self.bio_winter:
                alpha = alpha * 0.5  # Kışın doğum azalır
                gamma = gamma * 1.5  # Kışın kurt ölümü artar (açlık)

            # 3. Hesaplama (Lotka-Volterra)
            R = r[-1]; W = w[-1]
            noise_r = random.uniform(-0.5, 0.5)
            noise_w = random.uniform(-0.2, 0.2)
            
            dR = (alpha * R - beta * R * W) * dt + noise_r
            dW = (delta * R * W - gamma * W) * dt + noise_w
            
            new_R = max(1, R + dR)
            new_W = max(1, W + dW)
            
            r.append(new_R); w.append(new_W)
            time_step += dt; t_arr.append(time_step)
            
            if len(t_arr) > 300: r.pop(0); w.pop(0); t_arr.pop(0)

            # 4. Grafik Çizimi
            ax.clear()
            ax.plot(t_arr, r, color='#00d2d3', label="Tavşan (Av)", linewidth=2.5)
            ax.plot(t_arr, w, color='#ff6b6b', label="Kurt (Avcı)", linewidth=2.5)
            
            # Arka plan rengi mevsime göre değişir
            bg_color = "#2c3e50" if self.bio_winter else "#1e272e"
            ax.set_facecolor(bg_color)

            ax.fill_between(t_arr, r, color='#00d2d3', alpha=0.1)
            ax.fill_between(t_arr, w, color='#ff6b6b', alpha=0.1)
            ax.legend(loc="upper right", facecolor="#333", labelcolor="white")
            
            # Başlık Bilgisi
            extra_info = ""
            if self.bio_camouflage: extra_info += " [🛡️ Kamuflaj]"
            if self.bio_winter: extra_info += " [❄️ Kış]"
            
            ax.set_title(f"Dinamik Popülasyon Modeli {extra_info}", color="white", fontsize=10)
            ax.grid(True, color="#444", linestyle="--", alpha=0.3)
            
            max_val = max(max(r), max(w))
            ax.set_ylim(0, max_val * 1.2)
            ax.set_xlim(t_arr[0], t_arr[-1] + 1)
            
            lbl_status.config(text=f"🐰 Tavşan: {int(new_R)} | 🐺 Kurt: {int(new_W)} | Zaman: {int(time_step)}")
            canvas.draw()
            self.work.after(50, update)

        # --- BUTON YERLEŞİMLERİ ---
        btn_start = tk.Button(left_ctrl, text="▶️ BAŞLAT", bg=CFG["COLORS"]["SUCCESS"], fg="black", font=("Arial", 10, "bold"), command=run_sim)
        btn_start.pack(side="left", padx=10)
        
        # Sağ Panel: Etkileşimler
        right_ctrl = tk.Frame(ctrl_frame, bg=CFG["COLORS"]["PANEL"])
        right_ctrl.pack(side="right")

        # Üst Sıra (Toggle Butonları)
        row1 = tk.Frame(right_ctrl, bg=CFG["COLORS"]["PANEL"])
        row1.pack(pady=2)
        btn_cam = tk.Button(row1, text="🧬 KAMUFLAJ MUTASYONU", bg="#34495e", fg="white", width=22, command=toggle_camouflage)
        btn_cam.pack(side="left", padx=2)
        btn_winter = tk.Button(row1, text="☀️ YAZ MODU", bg="#e17055", fg="black", width=22, command=toggle_winter)
        btn_winter.pack(side="left", padx=2)
        
        # Alt Sıra (Anlık Olaylar)
        row2 = tk.Frame(right_ctrl, bg=CFG["COLORS"]["PANEL"])
        row2.pack(pady=2)
        tk.Button(row2, text="🚚 GÖÇ DALGASI (+50)", bg="#a29bfe", fg="black", width=22, command=trigger_migration).pack(side="left", padx=2)
        tk.Button(row2, text="☣️ SALGIN BAŞLAT", bg=CFG["COLORS"]["ERR"], fg="white", width=22, command=trigger_epidemic).pack(side="left", padx=2)

    # [MODÜL 5] MATEMATİK LAB: ULTRA MODERN GÖRSEL (CYBER-BALLISTICS)
    def mod_math_eng(self):
        self.set_header("BALİSTİK MÜHENDİSLİĞİ: HEDEFİ VUR")
        
        # Grafik Alanı (Matplotlib)
        fig = Figure(figsize=(7, 5), dpi=100)
        ax = fig.add_subplot(111)
        cv = FigureCanvasTkAgg(fig, master=self.work)
        cv.get_tk_widget().pack(fill="both", expand=True, side="left", padx=10, pady=10)
        
        # Sağ Panel (Kontroller)
        right = tk.Frame(self.work, bg=CFG["COLORS"]["PANEL"], width=320)
        right.pack(side="right", fill="y", padx=10, pady=10)
        right.pack_propagate(False)

        tk.Label(right, text="ATIŞ KONTROL SİSTEMİ", font=("Impact", 16), fg=CFG["COLORS"]["ACCENT"], bg=CFG["COLORS"]["PANEL"]).pack(pady=(20, 10))
        
        self.eng_target = 0
        self.eng_mode = "v" 
        
        # Görev Paneli
        mission_frame = tk.Frame(right, bg="#1F2833", bd=1, relief="solid")
        mission_frame.pack(fill="x", padx=10, pady=10)
        
        lbl_mission_title = tk.Label(mission_frame, text="⚠️ AKTİF GÖREV", font=("Arial", 9, "bold"), bg="#1F2833", fg="#ff7675")
        lbl_mission_title.pack(anchor="w", padx=5, pady=(5,0))
        
        lbl_mission = tk.Label(mission_frame, text="Veri Yükleniyor...", font=("Consolas", 10), bg="#1F2833", fg="#66FCF1", wraplength=280, justify="left", padx=5, pady=5)
        lbl_mission.pack(fill="x")

        # Sliderlar
        slide_style = {"bg": CFG["COLORS"]["PANEL"], "fg": "white", "highlightthickness": 0, "troughcolor": "#444", "activebackground": CFG["COLORS"]["ACCENT"]}
        s_v = tk.Scale(right, from_=10, to=120, orient="horizontal", label="🚀 Fırlatma Hızı (m/s)", **slide_style)
        s_v.set(50); s_v.pack(fill="x", padx=15, pady=10)
        s_a = tk.Scale(right, from_=5, to=85, orient="horizontal", label="📐 Atış Açısı (Derece)", **slide_style)
        s_a.set(45); s_a.pack(fill="x", padx=15, pady=10)
        
        # --- GELİŞMİŞ ÇİZİM FONKSİYONU ---
        def draw_scene(traj_x=None, traj_y=None):
            ax.clear()
            # 1. Tema ve Arka Plan
            ax.set_facecolor("#0B0C10") # Çok koyu lacivert/siyah
            fig.patch.set_facecolor("#0B0C10")
            
            # Izgaralar
            ax.grid(True, color="#1F2833", linestyle="-", linewidth=1, alpha=0.5)
            ax.minorticks_on()
            ax.grid(which='minor', color='#1F2833', linestyle=':', linewidth=0.5, alpha=0.3)
            
            # Eksenler
            ax.spines['bottom'].set_color('#66FCF1'); ax.spines['left'].set_color('#66FCF1')
            ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
            ax.tick_params(axis='x', colors='#66FCF1'); ax.tick_params(axis='y', colors='#66FCF1')
            
            # 2. Zemin (Terrain)
            ax.fill_between([-50, 600], -50, 0, color="#111", alpha=1) # Toprak
            ax.axhline(0, color="#66FCF1", linewidth=2) # Zemin çizgisi (Neon)
            
            # 3. MODERN TARET (CANNON) ÇİZİMİ
            angle_deg = s_a.get()
            angle_rad = math.radians(angle_deg)
            wedge = patches.Wedge((0, 0), 15, 0, 180, color="#95a5a6", ec="black")
            ax.add_patch(wedge)
            
            # Namlu
            bar_len = 35
            bx = bar_len * math.cos(angle_rad)
            by = bar_len * math.sin(angle_rad)
            ax.plot([0, bx], [0, by], color="#34495e", linewidth=8, solid_capstyle="round") # Dış namlu
            ax.plot([0, bx], [0, by], color="#7f8c8d", linewidth=4, solid_capstyle="round") # İç detay
            ax.add_patch(patches.Circle((0,0), 5, color="#2c3e50", zorder=10))
            ax.add_patch(patches.Circle((0,0), 2, color="#e74c3c", zorder=11))

            # 4. HOLOGRAFİK HEDEF BÖLGESİ
            tx = self.eng_target; width = 30
            ax.add_patch(patches.Rectangle((tx - width/2, 0), width, 3, color="#ff7675"))
            ax.add_patch(patches.Rectangle((tx - width/2, 0), width, 40, color="#ff7675", alpha=0.15))
            ax.plot([tx - width/2, tx - width/2], [0, 40], color="#ff7675", linestyle="--", alpha=0.6)
            ax.plot([tx + width/2, tx + width/2], [0, 40], color="#ff7675", linestyle="--", alpha=0.6)
            ax.text(tx, -15, f"{tx}m", color="#ff7675", ha="center", fontsize=10, fontweight="bold", backgroundcolor="#0B0C10")

            # 5. YÖRÜNGE VE MERMİ
            if traj_x is not None and traj_y is not None and len(traj_x) > 0:
                ax.plot(traj_x, traj_y, color="#66FCF1", linewidth=2, alpha=0.8)
                ax.plot(traj_x, [0]*len(traj_x), color="#66FCF1", linewidth=2, alpha=0.2)
                cx, cy = traj_x[-1], traj_y[-1]
                ax.plot(cx, cy, 'o', color="white", markersize=6, zorder=20)
                ax.plot(cx, cy, 'o', color="#66FCF1", markersize=14, alpha=0.4, zorder=19)
                ax.text(cx + 10, cy, f"h: {int(cy)}m\nx: {int(cx)}m", color="#66FCF1", fontsize=8)

            ax.set_xlim(-50, 600); ax.set_ylim(-40, 250)
            ax.set_title("SİBER ATIŞ SAHASI SİMÜLASYONU v2.0", color="white", fontsize=10, pad=10)
            cv.draw()

        def new_mission():
            self.eng_target = random.randint(150, 500)
            self.eng_mode = random.choice(["v", "a"])
            
            if self.eng_mode == "v":
                fixed_angle = random.choice([30, 45, 60, 75])
                s_a.set(fixed_angle); s_a.config(state="disabled", fg="gray", troughcolor="#222")
                s_v.config(state="normal", fg="white", troughcolor="#444")
                lbl_mission.config(text=f"Rüzgar Tareti {fixed_angle}° Açısına Kilitledi.\nHedef Menzili: {self.eng_target} metre.\n\n⚡ GÖREV: Gerekli HIZI ayarla ve ateşle!")
            else:
                fixed_v = random.randint(60, 100)
                s_v.set(fixed_v); s_v.config(state="disabled", fg="gray", troughcolor="#222")
                s_a.config(state="normal", fg="white", troughcolor="#444")
                lbl_mission.config(text=f"Motor Gücü {fixed_v} m/s seviyesine sabitlendi.\nHedef Menzili: {self.eng_target} metre.\n\n⚡ GÖREV: Gerekli AÇIYI hesapla ve ateşle!")
            draw_scene()

        def fire_shot():
            try:
                g = 9.8; v0 = s_v.get(); theta = math.radians(s_a.get())
                vox = v0 * math.cos(theta); voy = v0 * math.sin(theta)
                t_flight = (2 * voy) / g
                t_total = np.linspace(0, t_flight, 60)
                x_full = vox * t_total
                y_full = voy * t_total - 0.5 * g * t_total**2
                
                def animate_frame(i):
                    if i >= len(x_full):
                        final_x = x_full[-1]
                        hit = abs(final_x - self.eng_target) < 15 
                        self.db.update_stat(self.user["id"], "Fizik", hit)
                        if hit:
                            self.show_notification("GÖREV BAŞARILI", f"Tam İsabet! +100 XP\nVuruş: {int(final_x)}m", "success")
                            self.db.add_xp(self.user["id"], 100)
                            self.xp_lbl.config(text=f"XP: {self.user['xp'] + 100}")
                            self.work.after(2000, new_mission) 
                        else:
                            diff = int(final_x - self.eng_target)
                            msg = f"Çok İleri ({abs(diff)}m)" if diff > 0 else f"Çok Kısa ({abs(diff)}m)"
                            lbl_mission.config(text=f"❌ ISKALADIN!\nDurum: {msg}\nTekrar Dene!")
                        return

                    draw_scene(x_full[:i+1], y_full[:i+1])
                    self.work.after(20, lambda: animate_frame(i+1)) 
                animate_frame(0)
            except Exception as e: messagebox.showerror("Hata", str(e))

        btn_frame = tk.Frame(right, bg=CFG["COLORS"]["PANEL"])
        btn_frame.pack(side="bottom", fill="x", pady=20)
        tk.Button(btn_frame, text="YENİ KOORDİNAT 📡", bg="#34495e", fg="white", font=("Arial", 9, "bold"), pady=5, bd=0, command=new_mission).pack(fill="x", pady=5, padx=15)
        tk.Button(btn_frame, text="ATEŞLE 🔥", bg="#e74c3c", fg="white", font=("Arial", 14, "bold"), pady=10, bd=0, activebackground="#c0392b", cursor="hand2", command=fire_shot).pack(fill="x", padx=15)
        
        s_a.config(command=lambda e: draw_scene()) 
        self.work.after(100, new_mission)

    # [MODÜL 6] GENEL KÜLTÜR QUİZ
    def mod_quiz(self):
        self.set_header("BÜYÜK BİLİM SINAVI")
        
        # Soru Havuzu (GENİŞLETİLMİŞ - 8. SINIF LGS EKLENTİLİ)
        questions = [
            # --- MEVCUT SORULAR (SABİT) ---
            {"q": "DNA'nın yapısında aşağıdaki bazlardan hangisi YOKTUR?", "opts": ["Adenin", "Guanin", "Urasil", "Timin"], "ans": "Urasil", "cat": "Biyoloji"},
            {"q": "Suyun (H2O) molekül geometrisi nasıldır?", "opts": ["Doğrusal", "Kırık Doğru", "Düzgün Dörtyüzlü", "Piramit"], "ans": "Kırık Doğru", "cat": "Kimya"},
            {"q": "Işık hızı boşlukta yaklaşık ne kadardır?", "opts": ["300.000 km/s", "150.000 km/s", "1.000 km/s", "Sonsuz"], "ans": "300.000 km/s", "cat": "Fizik"},
            {"q": "Bir üçgenin iç açıları toplamı kaç derecedir?", "opts": ["90", "180", "360", "270"], "ans": "180", "cat": "Matematik"},
            {"q": "Hücrenin enerji santrali hangi organeldir?", "opts": ["Ribozom", "Lizozom", "Mitokondri", "Golgi"], "ans": "Mitokondri", "cat": "Biyoloji"},
            {"q": "pH değeri 2 olan bir sıvı nedir?", "opts": ["Kuvvetli Asit", "Zayıf Baz", "Nötr", "Tuzlu Su"], "ans": "Kuvvetli Asit", "cat": "Kimya"},
            {"q": "F = m * a formülü kime aittir?", "opts": ["Einstein", "Newton", "Tesla", "Galileo"], "ans": "Newton", "cat": "Fizik"},
            {"q": "Pi sayısının yaklaşık değeri nedir?", "opts": ["3.14", "2.71", "1.618", "0"], "ans": "3.14", "cat": "Matematik"},
            {"q": "En hafif element hangisidir?", "opts": ["Helyum", "Lityum", "Hidrojen", "Bor"], "ans": "Hidrojen", "cat": "Kimya"},
            {"q": "Gözdeki görüntünün oluştuğu tabaka hangisidir?", "opts": ["Kornea", "İris", "Retina (Ağ Tabaka)", "Mercek"], "ans": "Retina (Ağ Tabaka)", "cat": "Biyoloji"},
            {"q": "Türevi kendisi olan fonksiyon hangisidir?", "opts": ["sin(x)", "x^2", "e^x", "ln(x)"], "ans": "e^x", "cat": "Matematik"},
            {"q": "Işığın kırılması olayına ne ad verilir?", "opts": ["Yansıma", "Refraksiyon", "Difraksiyon", "Girişim"], "ans": "Refraksiyon", "cat": "Fizik"},
            {"q": "Telefonu kim icat etmiştir?", "opts": ["Graham Bell", "Edison", "Tesla", "Marconi"], "ans": "Graham Bell", "cat": "Bilim Tarihi"},
            {"q": "Periyodik tabloda 'Au' simgesi hangi elementi temsil eder?", "opts": ["Gümüş", "Altın", "Bakır", "Alüminyum"], "ans": "Altın", "cat": "Kimya"},
            {"q": "Hangi gezegen 'Kızıl Gezegen' olarak bilinir?", "opts": ["Venüs", "Mars", "Jüpiter", "Satürn"], "ans": "Mars", "cat": "Astronomi"},
            {"q": "Fotosentez sonucunda bitkiler atmosfere ne verir?", "opts": ["Karbondioksit", "Azot", "Oksijen", "Metan"], "ans": "Oksijen", "cat": "Biyoloji"},
            {"q": "Ses en hızlı hangi ortamda yayılır?", "opts": ["Boşluk", "Hava (Gaz)", "Su (Sıvı)", "Çelik (Katı)"], "ans": "Çelik (Katı)", "cat": "Fizik"},
            {"q": "İnsan vücudundaki en büyük organ hangisidir?", "opts": ["Karaciğer", "Beyin", "Deri", "Kalp"], "ans": "Deri", "cat": "Biyoloji"},
            {"q": "Sıfır sayısı hangi medeniyet tarafından matematiğe kazandırılmıştır?", "opts": ["Mısır", "Roma", "Hint", "Yunan"], "ans": "Hint", "cat": "Matematik Tarihi"},
            {"q": "Atomun merkezinde bulunan pozitif yüklü parçacık nedir?", "opts": ["Elektron", "Nötron", "Proton", "Foton"], "ans": "Proton", "cat": "Kimya"},
            {"q": "Bir cismin kütlesi ile yerçekimi ivmesinin çarpımı neyi verir?", "opts": ["Hız", "Ağırlık", "Yoğunluk", "Hacim"], "ans": "Ağırlık", "cat": "Fizik"},
            {"q": "144 sayısının karekökü kaçtır?", "opts": ["10", "11", "12", "14"], "ans": "12", "cat": "Matematik"},
            {"q": "Aspirinin ham maddesi hangi ağacın kabuğundan elde edilir?", "opts": ["Söğüt", "Çam", "Meşe", "Kavak"], "ans": "Söğüt", "cat": "Kimya"},
            {"q": "Nobel ödülleri hangi ülkede verilir?", "opts": ["İsviçre", "İsveç", "Almanya", "ABD"], "ans": "İsveç", "cat": "Genel Kültür"},
            {"q": "Elektrik akım şiddetinin birimi nedir?", "opts": ["Volt", "Watt", "Amper", "Ohm"], "ans": "Amper", "cat": "Fizik"},
            {"q": "Hangi kan grubu 'Genel Verici' olarak bilinir?", "opts": ["A Rh+", "AB Rh-", "0 Rh-", "B Rh+"], "ans": "0 Rh-", "cat": "Biyoloji"},
            {"q": "Bilgisayarın babası olarak kabul edilen bilim insanı kimdir?", "opts": ["Alan Turing", "Bill Gates", "Charles Babbage", "Steve Jobs"], "ans": "Charles Babbage", "cat": "Teknoloji"},
            {"q": "Atmosferde oranı en yüksek olan gaz hangisidir?", "opts": ["Oksijen", "Azot", "Karbondioksit", "Argon"], "ans": "Azot", "cat": "Coğrafya/Kimya"},
            {"q": "Hücre bölünmesini kontrol eden yapı hangisidir?", "opts": ["Hücre Zarı", "Sitoplazma", "Çekirdek", "Koful"], "ans": "Çekirdek", "cat": "Biyoloji"},
            {"q": "Dinamiti kim icat etmiştir?", "opts": ["Alfred Nobel", "Einstein", "Pasteur", "Curie"], "ans": "Alfred Nobel", "cat": "Bilim Tarihi"},
            {"q": "Bir saat kaç saniyedir?", "opts": ["60", "360", "3600", "6000"], "ans": "3600", "cat": "Matematik"},
            {"q": "Hangisi bir yenilenebilir enerji kaynağı DEĞİLDİR?", "opts": ["Güneş", "Rüzgar", "Doğalgaz", "Jeotermal"], "ans": "Doğalgaz", "cat": "Çevre Bilimi"},
            {"q": "Kaldırma kuvvetini bulan bilim insanı kimdir?", "opts": ["Pisagor", "Arşimet", "Öklid", "Thales"], "ans": "Arşimet", "cat": "Fizik"},
            {"q": "İnsan iskeletinde kaç adet kemik bulunur (yetişkin)?", "opts": ["106", "206", "306", "406"], "ans": "206", "cat": "Biyoloji"},
            {"q": "Elmas ve Grafit hangi elementin allotroplarıdır?", "opts": ["Demir", "Karbon", "Silikon", "Azot"], "ans": "Karbon", "cat": "Kimya"},
            {"q": "Dünya'nın uydusu Ay'a ilk ayak basan insan kimdir?", "opts": ["Yuri Gagarin", "Buzz Aldrin", "Neil Armstrong", "Michael Collins"], "ans": "Neil Armstrong", "cat": "Uzay"},
            {"q": "Hangi hayvanın kalbi dakikada en az atar?", "opts": ["Mavi Balina", "Fil", "İnsan", "Serçe"], "ans": "Mavi Balina", "cat": "Biyoloji"},
            {"q": "E = mc^2 formülündeki 'c' neyi temsil eder?", "opts": ["Enerji", "Kütle", "Işık Hızı", "Sıcaklık"], "ans": "Işık Hızı", "cat": "Fizik"},
            {"q": "En küçük asal sayı kaçtır?", "opts": ["0", "1", "2", "3"], "ans": "2", "cat": "Matematik"},
            # --- 8. SINIF LGS SORU EKLENTİSİ ---
            # ÜNİTE 1: MEVSİMLER VE İKLİM
            {"q": "Mevsimlerin oluşumunun TEMEL sebebi nedir?", "opts": ["Dünya'nın güneşe yakınlığı", "Eksen eğikliği", "Dünya'nın kendi etrafında dönüşü", "Ay'ın çekim gücü"], "ans": "Eksen eğikliği", "cat": "Fizik"},
            {"q": "Kuzey Yarım Küre'de en uzun gündüz ne zaman yaşanır?", "opts": ["21 Aralık", "21 Mart", "21 Haziran", "23 Eylül"], "ans": "21 Haziran", "cat": "Fizik"},
            {"q": "Geniş bir bölgede uzun yıllar boyunca gözlemlenen ortalama hava olaylarına ne denir?", "opts": ["İklim", "Hava Durumu", "Meteoroloji", "Atmosfer"], "ans": "İklim", "cat": "Genel"},
            {"q": "Rüzgarın oluşma sebebi nedir?", "opts": ["Sıcaklık farkından doğan basınç farkı", "Dünya'nın dönüşü", "Yağmurun yağması", "Bulutların hareketi"], "ans": "Sıcaklık farkından doğan basınç farkı", "cat": "Fizik"},
            # ÜNİTE 2: DNA VE GENETİK KOD
            {"q": "DNA'nın kendini eşlemesi hangi olaydan hemen önce gerçekleşir?", "opts": ["Protein sentezi", "Hücre bölünmesi", "Solunum", "Sindirim"], "ans": "Hücre bölünmesi", "cat": "Biyoloji"},
            {"q": "Guanin nükleotidinin karşısına her zaman hangi nükleotid gelir?", "opts": ["Adenin", "Timin", "Sitozin", "Urasil"], "ans": "Sitozin", "cat": "Biyoloji"},
            {"q": "Aşağıdakilerden hangisi kalıtsal bir değişikliktir?", "opts": ["Bronzlaşma", "Kas yapma", "Mutasyon", "Modifikasyon"], "ans": "Mutasyon", "cat": "Biyoloji"},
            {"q": "Çevre etkisiyle genlerin işleyişinin değişmesine ne ad verilir?", "opts": ["Mutasyon", "Modifikasyon", "Adaptasyon", "Varyasyon"], "ans": "Modifikasyon", "cat": "Biyoloji"},
            # ÜNİTE 3: BASINÇ
            {"q": "Katı basıncını azaltmak için ne yapılmalıdır?", "opts": ["Yüzey alanı küçültülmeli", "Ağırlık artırılmalı", "Yüzey alanı büyütülmeli", "Kuvvet uygulanmalı"], "ans": "Yüzey alanı büyütülmeli", "cat": "Fizik"},
            {"q": "Sıvı basıncı aşağıdakilerden hangisine bağlıdır?", "opts": ["Sıvının hacmine", "Kabın şekline", "Sıvının derinliğine", "Sıvının rengine"], "ans": "Sıvının derinliğine", "cat": "Fizik"},
            {"q": "Toriçelli Deneyi neyi ölçmek için yapılmıştır?", "opts": ["Sıvı basıncı", "Açık hava basıncı", "Katı basıncı", "Sıcaklık"], "ans": "Açık hava basıncı", "cat": "Fizik"},
            {"q": "Hidrolik fren sistemleri hangi prensibe göre çalışır?", "opts": ["Arşimet Prensibi", "Bernoulli İlkesi", "Pascal Prensibi", "Newton Yasası"], "ans": "Pascal Prensibi", "cat": "Fizik"},
            # ÜNİTE 4: MADDE VE ENDÜSTRİ
            {"q": "Periyodik tabloda 1A grubundaki elementlerin özel adı nedir?", "opts": ["Alkali Metaller", "Toprak Alkali", "Halojenler", "Soygazlar"], "ans": "Alkali Metaller", "cat": "Kimya"},
            {"q": "Aşağıdakilerden hangisi kimyasal bir değişimdir?", "opts": ["Suyun buharlaşması", "Camın kırılması", "Demirin paslanması", "Kağıdın yırtılması"], "ans": "Demirin paslanması", "cat": "Kimya"},
            {"q": "pH değeri 7'den büyük olan maddelere ne denir?", "opts": ["Asit", "Baz", "Nötr", "Tuz"], "ans": "Baz", "cat": "Kimya"},
            {"q": "Mavi turnusol kağıdını kırmızıya çeviren madde nedir?", "opts": ["Baz", "Tuz", "Su", "Asit"], "ans": "Asit", "cat": "Kimya"},
            {"q": "Özısısı büyük olan maddeler için hangisi söylenebilir?", "opts": ["Çabuk ısınır çabuk soğur", "Geç ısınır geç soğur", "Çabuk ısınır geç soğur", "Değişmez"], "ans": "Geç ısınır geç soğur", "cat": "Fizik"},
            
            # ÜNİTE 5: BASİT MAKİNELER
            {"q": "Aşağıdaki basit makinelerden hangisinde kuvvetten kazanç KESİNLİKLE yoktur?", "opts": ["Hareketli Makara", "Eğik Düzlem", "Sabit Makara", "Çıkrık"], "ans": "Sabit Makara", "cat": "Fizik"},
            {"q": "Eğik düzlemde kuvvet kazancını artırmak için ne yapılmalıdır?", "opts": ["Boyu uzatılmalı", "Yüksekliği artırılmalı", "Sürtünme artırılmalı", "Yük artırılmalı"], "ans": "Boyu uzatılmalı", "cat": "Fizik"},
            {"q": "Destek noktasının yük ile kuvvet arasında olduğu kaldıraç örneği hangisidir?", "opts": ["El arabası", "Cımbız", "Tahterevalli", "Ceviz kıracağı"], "ans": "Tahterevalli", "cat": "Fizik"},
            {"q": "Basit makineler neyden kazanç SAĞLAMAZ?", "opts": ["Kuvvetten", "Yoldan", "İş ve Enerjiden", "Zamandan"], "ans": "İş ve Enerjiden", "cat": "Fizik"},
            
            # ÜNİTE 6: ENERJİ DÖNÜŞÜMLERİ VE ÇEVRE
            {"q": "Fotosentez hangi organelde gerçekleşir?", "opts": ["Mitokondri", "Kloroplast", "Koful", "Ribozom"], "ans": "Kloroplast", "cat": "Biyoloji"},
            {"q": "Oksijensiz solunumun (Fermantasyon) insanda görüldüğü yer neresidir?", "opts": ["Beyin hücresi", "Çizgili kaslar", "Karaciğer", "Kan"], "ans": "Çizgili kaslar", "cat": "Biyoloji"},
            {"q": "Havadaki azotun toprağa bağlanmasını sağlayan olay nedir?", "opts": ["Yıldırım ve Şimşek", "Rüzgar", "Güneş ışığı", "Erozyon"], "ans": "Yıldırım ve Şimşek", "cat": "Genel"},
            {"q": "Sera etkisine en çok sebep olan gaz hangisidir?", "opts": ["Oksijen", "Azot", "Karbondioksit", "Hidrojen"], "ans": "Karbondioksit", "cat": "Kimya"},
            
            # ÜNİTE 7: ELEKTRİK YÜKLERİ
            {"q": "Nötr bir cisim elektron kaybederse yükü ne olur?", "opts": ["Nötr kalır", "Pozitif (+)", "Negatif (-)", "Belli olmaz"], "ans": "Pozitif (+)", "cat": "Fizik"},
            {"q": "Yüklü bir cismi nötr hale getirme işlemine ne ad verilir?", "opts": ["Elektriklenme", "Topraklama", "Yalıtım", "Sürtünme"], "ans": "Topraklama", "cat": "Fizik"},
            {"q": "Bir cismin yüklü olup olmadığını anlamaya yarayan alet nedir?", "opts": ["Dinamometre", "Termometre", "Elektroskop", "Barometre"], "ans": "Elektroskop", "cat": "Fizik"},
            {"q": "Aynı cins yüklü cisimler birbirine nasıl kuvvet uygular?", "opts": ["Çeker", "İter", "Etkilemez", "Döndürür"], "ans": "İter", "cat": "Fizik"},
            {"q": "Paratoner (Yıldırımsavar) binaların neresine takılır?", "opts": ["Temeline", "Orta katına", "En tepesine", "Bahçesine"], "ans": "En tepesine", "cat": "Genel"}
        ]
        
        main_frame = tk.Frame(self.work, bg=CFG["COLORS"]["BG"])
        main_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Skor Levhası
        score_frame = tk.Frame(main_frame, bg="#2d3436", pady=10)
        score_frame.pack(fill="x", pady=(0, 20))
        lbl_score = tk.Label(score_frame, text="DOĞRU: 0 | YANLIŞ: 0", font=("Consolas", 14, "bold"), bg="#2d3436", fg="white")
        lbl_score.pack()
        
        # --- STREAK GÖSTERGESİ (YENİ) ---
        self.quiz_streak = 0
        lbl_streak = tk.Label(score_frame, text="🔥 SERİ: 0", font=("Arial", 12, "bold"), bg="#2d3436", fg="#e17055")
        lbl_streak.pack(pady=(5, 0))

        self.quiz_stats = {"correct": 0, "wrong": 0}

        # Soru Kartı
        q_card = tk.Frame(main_frame, bg=CFG["COLORS"]["PANEL"], padx=20, pady=20, relief="raised", borderwidth=2)
        q_card.pack(fill="both", expand=True)
        
        lbl_cat = tk.Label(q_card, text="KATEGORİ", font=("Arial", 10, "bold"), bg=CFG["COLORS"]["PANEL"], fg=CFG["COLORS"]["ACCENT"])
        lbl_cat.pack(anchor="w")
        
        lbl_q = tk.Label(q_card, text="Soru Yükleniyor...", font=("Segoe UI", 18, "bold"), bg=CFG["COLORS"]["PANEL"], fg="white", wraplength=800)
        lbl_q.pack(pady=30)
        
        opts_frame = tk.Frame(q_card, bg=CFG["COLORS"]["PANEL"])
        opts_frame.pack(fill="x", pady=20)
        
        btns = []
        for i in range(4):
            btn = tk.Button(opts_frame, text="", font=("Arial", 12), bg="#4b4b4b", fg="white", height=2, width=30)
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
            btns.append(btn)
        opts_frame.grid_columnconfigure(0, weight=1); opts_frame.grid_columnconfigure(1, weight=1)

        def next_q():
            q = random.choice(questions)
            lbl_cat.config(text=f"📚 KATEGORİ: {q['cat'].upper()}")
            lbl_q.config(text=q['q'])
            
            opts = q['opts'].copy()
            random.shuffle(opts)
            
            for b in btns:
                b.config(text="", command=None, bg="#4b4b4b", state="normal")
            
            def check(val, btn_ref):
                is_correct = (val == q['ans'])
                # İSTATİSTİK KAYDI
                cat_map = {"Biyoloji": "Biyoloji", "Kimya": "Kimya", "Fizik": "Fizik", "Matematik": "Matematik"}
                simple_cat = cat_map.get(q['cat'], "Genel")
                self.db.update_stat(self.user["id"], simple_cat, is_correct)

                if is_correct:
                    btn_ref.config(bg=CFG["COLORS"]["SUCCESS"])
                    self.quiz_streak += 1
                    
                    # Streak Mesajı
                    msg = "+20 XP"
                    if self.quiz_streak >= 10: msg = "DURDURULAMAZ! 🚀 +100 XP"; self.db.add_xp(self.user["id"], 80)
                    elif self.quiz_streak >= 5: msg = "ALEV ALDIN! 🔥🔥 +50 XP"; self.db.add_xp(self.user["id"], 30)
                    elif self.quiz_streak >= 3: msg = "ISINIYORSUN! 🔥 +30 XP"; self.db.add_xp(self.user["id"], 10)
                    
                    self.show_notification("Doğru!", msg, "success")
                    self.db.add_xp(self.user["id"], 20); self.xp_lbl.config(text=f"XP: {self.user['xp'] + 20}")
                    self.quiz_stats["correct"] += 1
                else:
                    btn_ref.config(bg=CFG["COLORS"]["ERR"])
                    self.quiz_streak = 0
                    self.show_notification("Yanlış!", f"Doğru cevap: {q['ans']}", "error")
                    self.quiz_stats["wrong"] += 1
                
                # Update Labels
                lbl_score.config(text=f"DOĞRU: {self.quiz_stats['correct']} | YANLIŞ: {self.quiz_stats['wrong']}")
                lbl_streak.config(text=f"🔥 SERİ: {self.quiz_streak}", fg=CFG["COLORS"]["HIGHLIGHT"] if self.quiz_streak > 2 else "gray")
                
                # Tüm butonları kilitle
                for b in btns: b.config(state="disabled")
                self.root.after(1500, next_q)

            for i, opt in enumerate(opts):
                btns[i].config(text=opt, command=lambda v=opt, b=btns[i]: check(v, b))

        next_q()

    # [MODÜL 7] ALIŞKANLIK & İRADE TAKİP
    def mod_habit_tracker(self):
        self.set_header("İRADE YÖNETİMİ: ZİNCİRİ KIRMA")
        
        # --- Sol Panel: Ekleme ve Liste ---
        left_panel = tk.Frame(self.work, bg=CFG["COLORS"]["PANEL"], width=300)
        left_panel.pack(side="left", fill="y", padx=10)
        
        tk.Label(left_panel, text="ALIŞKANLIK EKLE", font=("Arial", 12, "bold"), fg="white", bg=CFG["COLORS"]["PANEL"]).pack(pady=(10, 5))
        
        entry_habit = tk.Entry(left_panel, font=("Arial", 12), bg="#dfe6e9", fg="#2d3436")
        entry_habit.pack(pady=5, padx=10, fill="x")
        
        # --- Sağ Panel: Detay ve Görsel Yolculuk ---
        right_panel = tk.Frame(self.work, bg="#1a1a1a")
        right_panel.pack(side="right", fill="both", expand=True, padx=10)

        # Detay Çerçevesi (Ana Sahne)
        detail_frame = tk.Frame(right_panel, bg="#1a1a1a")
        detail_frame.pack(fill="both", expand=True)

        # --- ÇOKLU MOTİVASYON FONKSİYONU ---
        def refresh_quotes():
            # Önce eski sözleri temizle (varsa)
            for widget in detail_frame.winfo_children():
                if isinstance(widget, tk.Label) and getattr(widget, "is_quote", False):
                    widget.destroy()

            # Yeni sözler seç
            quotes = random.sample(CFG["FACTS"]["HABIT"].split("|"), 5)
            positions = [
                (0.05, 0.05, "nw"), # Sol Üst
                (0.95, 0.05, "ne"), # Sağ Üst
                (0.05, 0.95, "sw"), # Sol Alt
                (0.95, 0.95, "se"), # Sağ Alt
                (0.5, 0.85, "center") # Orta Alt
            ]

            for i, pos in enumerate(positions):
                q_text = quotes[i].strip()
                # Köşelerdeki sözleri biraz daha küçük yap
                font_size = 14 if i < 4 else 16 # BÜYÜTÜLDÜ
                color = "#bdc3c7" if i < 4 else CFG["COLORS"]["ACCENT"]
                
                # Kart efekti için Frame içinde Label
                card = tk.Frame(detail_frame, bg="#2f3640", padx=10, pady=10, relief="raised", bd=2)
                card.is_quote = True
                card.place(relx=pos[0], rely=pos[1], anchor=pos[2])

                lbl = tk.Label(card, text=q_text, font=("Segoe UI", font_size, "italic"), 
                               bg="#2f3640", fg=color, wraplength=300, justify="center")
                lbl.pack()

        def load_habits():
            for w in list_frame.winfo_children(): w.destroy()
            habits = self.db.cur.execute("SELECT * FROM habits WHERE user_id=?", (self.user["id"],)).fetchall()
            
            for h in habits:
                h_id, h_name, h_streak = h[0], h[2], h[3]
                
                item_frame = tk.Frame(list_frame, bg="#333", pady=5)
                item_frame.pack(fill="x", pady=2)
                
                tk.Label(item_frame, text=h_name, font=("Arial", 11), bg="#333", fg="white").pack(side="left", padx=10)
                tk.Label(item_frame, text=f"{h_streak} Gün", font=("Arial", 10, "bold"), bg="#333", fg=CFG["COLORS"]["SUCCESS"]).pack(side="right", padx=10)
                
                item_frame.bind("<Button-1>", lambda e, hid=h_id: show_details(hid))
                for child in item_frame.winfo_children():
                    child.bind("<Button-1>", lambda e, hid=h_id: show_details(hid))

        def add_new_habit():
            name = entry_habit.get()
            if name:
                self.db.cur.execute("INSERT INTO habits (user_id, name, streak, last_checkin) VALUES (?, ?, 0, '')", (self.user["id"], name))
                self.db.conn.commit()
                entry_habit.delete(0, tk.END)
                load_habits()
                self.show_notification("Başarılı", "Yeni hedef eklendi!", "success")
            else:
                self.show_notification("Hata", "Lütfen bir isim girin.", "error")

        tk.Button(left_panel, text="EKLE", bg=CFG["COLORS"]["ACCENT"], fg="black", font=("Arial", 10, "bold"), command=add_new_habit).pack(pady=5, padx=10, fill="x")
        
        tk.Label(left_panel, text="LİSTEM", font=("Arial", 10), fg="gray", bg=CFG["COLORS"]["PANEL"]).pack(pady=(20, 5))
        
        list_frame = tk.Frame(left_panel, bg=CFG["COLORS"]["PANEL"])
        list_frame.pack(fill="both", expand=True, padx=10)

        def show_details(h_id):
            # Ana içeriği temizle
            for w in detail_frame.winfo_children(): w.destroy()
            
            h = self.db.cur.execute("SELECT * FROM habits WHERE id=?", (h_id,)).fetchone()
            if not h: return
            
            name, streak, last_date = h[2], h[3], h[4]
            today = str(datetime.date.today())
            
            # --- YENİ MODERN GÖRÜNÜM ---
            # 1. Başlık
            tk.Label(detail_frame, text=name.upper(), font=("Impact", 48), fg="white", bg="#1a1a1a").pack(pady=(30, 10))

            # 2. Devasa Sayaç (Hero Section)
            counter_frame = tk.Frame(detail_frame, bg="#1a1a1a")
            counter_frame.pack(pady=20)
            
            tk.Label(counter_frame, text=str(streak), font=("Arial", 100, "bold"), fg=CFG["COLORS"]["SUCCESS"], bg="#1a1a1a").pack(side="left")
            tk.Label(counter_frame, text="GÜN", font=("Arial", 24, "bold"), fg="gray", bg="#1a1a1a").pack(side="left", padx=10, anchor="s", pady=20)

            # 3. İlerleme Çubuğu (Görsel)
            progress_frame = tk.Frame(detail_frame, bg="#1a1a1a")
            progress_frame.pack(fill="x", padx=50, pady=20)
            
            # Hedefler: 7, 21, 90 gün
            next_goal = 90
            if streak < 7: next_goal = 7
            elif streak < 21: next_goal = 21
            elif streak < 90: next_goal = 90
            
            perc = min(streak / next_goal, 1.0)
            
            canvas = tk.Canvas(progress_frame, height=30, bg="#333", highlightthickness=0)
            canvas.pack(fill="x")
            
            # Doluluk
            w = 800 # Yaklaşık genişlik, fill ile esneyecek ama çizim için referans
            canvas.create_rectangle(0, 0, w * perc, 30, fill=CFG["COLORS"]["ACCENT"], width=0)
            
            tk.Label(progress_frame, text=f"Sonraki Hedef: {next_goal} Gün (%{int(perc*100)})", font=("Arial", 12), fg="white", bg="#1a1a1a").pack(pady=5)

            # 4. Kontrol Butonları
            ctrl_frame = tk.Frame(detail_frame, bg="#1a1a1a", pady=20)
            ctrl_frame.pack()
            
            def check_in():
                if last_date == today:
                    self.show_notification("Bilgi", "Bugün zaten işaretledin!", "info")
                    return
                
                new_streak = streak + 1
                self.db.cur.execute("UPDATE habits SET streak=?, last_checkin=? WHERE id=?", (new_streak, today, h_id))
                self.db.conn.commit()
                
                # Milestone ödülü
                reward = 50
                if new_streak in [7, 21, 90]: 
                    reward = 500
                    self.show_notification("MİLESTONE!", f"{new_streak} GÜNLÜK SERİ! +500 XP", "success")
                else:
                    self.show_notification("Tebrikler!", "Zinciri kırmadın! +50 XP", "success")

                self.db.add_xp(self.user["id"], reward) 
                self.xp_lbl.config(text=f"XP: {self.user['xp'] + reward}")
                
                show_details(h_id) 
                load_habits() 

            def break_chain():
                if messagebox.askyesno("Emin misin?", "Seriyi sıfırlamak istiyor musun?"):
                    self.db.cur.execute("UPDATE habits SET streak=0 WHERE id=?", (h_id,))
                    self.db.conn.commit()
                    show_details(h_id)
                    load_habits()

            btn_check = tk.Button(ctrl_frame, text="✅ ZİNCİRE HALKA EKLE", font=("Segoe UI", 14, "bold"), 
                                  bg=CFG["COLORS"]["SUCCESS"] if last_date != today else "gray", 
                                  fg="#1e272e", width=25, height=2, command=check_in)
            btn_check.pack(pady=5)
            
            btn_break = tk.Button(ctrl_frame, text="❌ SIFIRLA", font=("Arial", 10), bg=CFG["COLORS"]["ERR"], fg="white", command=break_chain)
            btn_break.pack(pady=10)
            
            if last_date == today:
                tk.Label(detail_frame, text="✨ BUGÜNLÜK GÖREV TAMAMLANDI ✨", font=("Segoe UI", 16, "bold"), fg=CFG["COLORS"]["HIGHLIGHT"], bg="#1a1a1a").pack()

        # İlk açılışta boş bir ekran ve rastgele sözler göster
        refresh_quotes()
        tk.Label(detail_frame, text="<< LİSTEDEN BİR HEDEF SEÇ", font=("Arial", 16), fg="gray", bg="#1a1a1a").place(relx=0.5, rely=0.5, anchor="center")
        load_habits()

   # [MODÜL 8] ELEKTRİK DEVRE LABORATUVARI (MODERN UI UPDATE)
    def mod_electric_lab(self):
        self.set_header("ELEKTRİK LAB: PRO SİMÜLASYON")
        
        # --- DÜZEN (LAYOUT) ---
        main_container = tk.Frame(self.work, bg="#1e272e")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 1. ALT PANEL: LCD GÖSTERGE (ÖNCE PAKETLE - FOOTER GİBİ DAVRANSIN)
        lcd_frame = tk.Frame(main_container, bg="#111", height=120, bd=4, relief="ridge")
        lcd_frame.pack(side="bottom", fill="x", pady=(10, 0))
        lcd_frame.pack_propagate(False)

        # 2. ÜST BÖLGE (ARAÇLAR + SAHNE)
        upper_area = tk.Frame(main_container, bg="#1e272e")
        upper_area.pack(side="top", fill="both", expand=True)

        # SOL PANEL: ARAÇLAR
        tools_frame = tk.Frame(upper_area, bg="#2f3640", width=220, relief="raised", bd=2)
        tools_frame.pack(side="left", fill="y", padx=(0, 10))
        tools_frame.pack_propagate(False)

        tk.Label(tools_frame, text="DEVRE ELEMANLARI", font=("Segoe UI", 12, "bold"), fg="#00d2d3", bg="#2f3640", pady=15).pack()

        # SAĞ PANEL: SAHNE (CANVAS)
        canvas_frame = tk.Frame(upper_area, bg="#000000", bd=2, relief="sunken")
        canvas_frame.pack(side="left", fill="both", expand=True)

        # Gridli Canvas
        canvas = tk.Canvas(canvas_frame, bg="#191919", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Izgara Çizimi (Grid)
        def draw_grid():
            w = 2000; h = 2000 # Geniş çizim alanı
            for i in range(0, w, 40):
                canvas.create_line(i, 0, i, h, fill="#333", width=1)
            for i in range(0, h, 40):
                canvas.create_line(0, i, w, i, fill="#333", width=1)
        
        draw_grid()

        # --- LCD EKRAN BİLEŞENLERİ ---
        # 3 Bölmeli Dijital Ekran (V, I, R)
        lcd_font = ("Consolas", 24, "bold")
        lbl_info_title = tk.Label(lcd_frame, text="MULTİMETRE ÖLÇÜMÜ", font=("Arial", 10), bg="#111", fg="gray")
        lbl_info_title.pack(side="top", pady=5)

        stats_container = tk.Frame(lcd_frame, bg="#111")
        stats_container.pack(fill="both", expand=True, padx=20)

        # Voltaj
        f_volt = tk.Frame(stats_container, bg="#222", padx=20, relief="sunken", bd=1); f_volt.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        lbl_volt_val = tk.Label(f_volt, text="0.0 V", font=lcd_font, fg="#e74c3c", bg="#222")
        lbl_volt_val.pack(expand=True)
        tk.Label(f_volt, text="GERİLİM (VOLT)", font=("Arial", 9, "bold"), fg="#bdc3c7", bg="#222").pack(side="bottom", pady=5)

        # Akım
        f_amp = tk.Frame(stats_container, bg="#222", padx=20, relief="sunken", bd=1); f_amp.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        lbl_amp_val = tk.Label(f_amp, text="0.00 A", font=lcd_font, fg="#f1c40f", bg="#222")
        lbl_amp_val.pack(expand=True)
        tk.Label(f_amp, text="AKIM (AMPER)", font=("Arial", 9, "bold"), fg="#bdc3c7", bg="#222").pack(side="bottom", pady=5)

        # Direnç
        f_res = tk.Frame(stats_container, bg="#222", padx=20, relief="sunken", bd=1); f_res.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        lbl_res_val = tk.Label(f_res, text="∞ Ω", font=lcd_font, fg="#3498db", bg="#222")
        lbl_res_val.pack(expand=True)
        tk.Label(f_res, text="EŞDEĞER DİRENÇ", font=("Arial", 9, "bold"), fg="#bdc3c7", bg="#222").pack(side="bottom", pady=5)

        # --- DEVRE MANTIĞI VE DEĞİŞKENLER ---
        self.circuit_components = [] 
        self.selected_tool = None
        self.wire_start = None

        # --- MODERN BİLEŞEN ÇİZİMİ ---
        def draw_component_visual(c_type, x, y, tags, state="OFF"):
            if c_type == "BATTERY":
                # Pil Gövdesi
                canvas.create_rectangle(x-20, y-30, x+20, y+30, fill="#2c3e50", outline="#95a5a6", width=2, tags=tags)
                # Pil Şapkası (+)
                canvas.create_rectangle(x-10, y-35, x+10, y-30, fill="#bdc3c7", outline="", tags=tags)
                # Etiketler
                canvas.create_text(x, y-15, text="+", fill="#e74c3c", font=("Arial", 14, "bold"), tags=tags)
                canvas.create_text(x, y+20, text="1.5V", fill="white", font=("Arial", 10, "bold"), tags=tags)
            
            elif c_type == "LAMP":
                # Duy (Alt kısım)
                canvas.create_rectangle(x-10, y+20, x+10, y+35, fill="#e67e22", outline="black", tags=tags)
                # Cam Fanus
                color = "#34495e" # Sönük renk
                if state == "ON": color = "#f1c40f" # Yanık renk
                
                # Işık Hüzmesi (Halo Effect) - Eğer açıksa
                if state == "ON":
                    for i in range(3):
                        r = 45 + (i*10)
                        alpha_col = ["#f1c40f", "#f39c12", "#d35400"][i] # Sarıdan turuncuya
                        canvas.create_oval(x-r, y-20-r, x+r, y-20+r, fill=alpha_col, outline="", stipple="gray25", tags=tags+("glow",))

                # Ana cam
                canvas.create_oval(x-25, y-45, x+25, y+20, fill=color, outline="white", width=2, tags=tags)
                # Filaman
                canvas.create_line(x-10, y+20, x, y-10, x+10, y+20, fill="white", width=1, tags=tags)

            elif c_type == "SWITCH":
                # Taban
                canvas.create_rectangle(x-30, y-10, x+30, y+10, fill="#34495e", outline="", tags=tags)
                # Bağlantı noktaları
                canvas.create_oval(x-25, y-5, x-15, y+5, fill="white", tags=tags)
                canvas.create_oval(x+15, y-5, x+25, y+5, fill="white", tags=tags)
                
                # Kol
                if state == "OFF": # Açık devre (Kol havada)
                    canvas.create_line(x-20, y, x+15, y-20, fill="#e74c3c", width=4, capstyle="round", tags=tags)
                else: # Kapalı devre (Kol inik)
                    canvas.create_line(x-20, y, x+20, y, fill="#2ecc71", width=4, capstyle="round", tags=tags)

        def update_scene():
            pass

        # --- ETKİLEŞİM ---
        def select_tool(tool):
            self.selected_tool = tool
            # Buton renklerini sıfırla
            for btn in btn_list: btn.config(bg="#2f3640", fg="white")
            # Seçili butonu parlat
            tool_colors = {"BATTERY": "#e74c3c", "LAMP": "#f1c40f", "SWITCH": "#3498db", "WIRE": "#e67e22"}
            if tool in btn_ref:
                btn_ref[tool].config(bg=tool_colors.get(tool, "white"), fg="black")

        def on_click(e):
            # Izgaraya yapışma (Snap to grid) - 40px
            gx, gy = round(e.x / 40) * 40, round(e.y / 40) * 40

            if self.selected_tool == "WIRE":
                if self.wire_start is None:
                    self.wire_start = (gx, gy)
                    canvas.create_oval(gx-4, gy-4, gx+4, gy+4, fill="#e67e22", outline="white", tags="temp_guide")
                else:
                    # Kabloyu çiz
                    canvas.create_line(self.wire_start[0], self.wire_start[1], gx, gy, fill="#e67e22", width=4, capstyle="round", tags="wire")
                    # Bağlantı noktalarına lehim efekti
                    canvas.create_oval(self.wire_start[0]-4, self.wire_start[1]-4, self.wire_start[0]+4, self.wire_start[1]+4, fill="white", outline="#e67e22", width=2, tags="solder")
                    canvas.create_oval(gx-4, gy-4, gx+4, gy+4, fill="white", outline="#e67e22", width=2, tags="solder")
                    
                    canvas.delete("temp_guide")
                    self.wire_start = None
                    check_circuit()
            
            elif self.selected_tool in ["BATTERY", "LAMP", "SWITCH"]:
                uid = str(random.randint(10000, 99999))
                tags = ("comp", uid, self.selected_tool)
                
                # Default state
                state = "ON" 
                if self.selected_tool == "SWITCH": state = "OFF"

                self.circuit_components.append({"id": uid, "type": self.selected_tool, "x": gx, "y": gy, "state": state})
                draw_component_visual(self.selected_tool, gx, gy, tags, state)
                check_circuit()

        def on_right_click(e):
            # Anahtarı aç/kapa
            item = canvas.find_closest(e.x, e.y)[0]
            tags = canvas.gettags(item)
            if "comp" in tags:
                uid = tags[1]
                ctype = tags[2]
                if ctype == "SWITCH":
                    comp = next((c for c in self.circuit_components if c["id"] == uid), None)
                    if comp:
                        # Durumu tersine çevir
                        comp["state"] = "ON" if comp["state"] == "OFF" else "OFF"
                        # Eski görseli sil
                        for t_item in canvas.find_withtag(uid): canvas.delete(t_item)
                        # Yeni görseli çiz
                        draw_component_visual("SWITCH", comp["x"], comp["y"], tags, comp["state"])
                        check_circuit()

        def on_middle_click(e):
            pass

        def check_circuit():
            # --- GELİŞMİŞ DEVRE KONTROLÜ (TEMAS TABANLI) ---
            batteries = [c for c in self.circuit_components if c["type"] == "BATTERY"]
            lamps = [c for c in self.circuit_components if c["type"] == "LAMP"]
            switches = [c for c in self.circuit_components if c["type"] == "SWITCH"]
            
            # 1. Genel Kurallar
            switches_closed = all(s["state"] == "ON" for s in switches) # Tüm anahtarlar kapalı olmalı
            has_power = len(batteries) > 0

            # 2. Temas Kontrolü (Collision Detection)
            def is_connected_to_wire(comp):
                # Bileşenin merkezindeki küçük bir alanda "wire" etiketi var mı?
                x, y = comp["x"], comp["y"]
                items = canvas.find_overlapping(x-20, y-20, x+20, y+20)
                for item in items:
                    tags = canvas.gettags(item)
                    if "wire" in tags:
                        return True
                return False

            # Pil bir kabloya bağlı mı?
            battery_connected = False
            for bat in batteries:
                if is_connected_to_wire(bat):
                    battery_connected = True
                    break
            
            # Potansiyel Hesaplama
            voltage = len(batteries) * 1.5
            resistance = 0
            active_lamps = []

            # Eğer güç var, anahtarlar kapalı ve pil bağlıysa -> Ampulleri kontrol et
            if has_power and switches_closed and battery_connected:
                for lamp in lamps:
                    if is_connected_to_wire(lamp):
                        active_lamps.append(lamp)
                        resistance += 5 # Her aktif lamba direnç ekler
            
            # Akım Hesaplama
            if resistance == 0: 
                current = 0
                resistance = 0.1 # Gösterim hatasını önlemek için
            else:
                current = voltage / resistance

            # LCD Güncelleme
            lbl_volt_val.config(text=f"{voltage:.1f} V")
            
            if len(active_lamps) == 0:
                 lbl_res_val.config(text="∞ Ω")
                 lbl_amp_val.config(text="0.00 A")
                 current = 0
            else:
                 lbl_res_val.config(text=f"{int(resistance)} Ω")
                 lbl_amp_val.config(text=f"{current:.2f} A")

            # Görsel Güncelleme (Ampulleri Yak/Söndür)
            canvas.delete("glow")
            for lamp in lamps:
                # Sadece aktif listedeyse ve akım varsa yak
                state = "ON" if (lamp in active_lamps and current > 0) else "OFF"
                
                # Yeniden çiz
                for item in canvas.find_withtag(lamp["id"]): canvas.delete(item)
                tags = ("comp", lamp["id"], "LAMP")
                draw_component_visual("LAMP", lamp["x"], lamp["y"], tags, state)

        def clear_all():
            canvas.delete("all")
            draw_grid()
            self.circuit_components.clear()
            self.wire_start = None
            check_circuit()

        # --- BUTONLAR ---
        btn_list = []
        btn_ref = {}

        def create_tool_btn(txt, tool, col):
            b = tk.Button(tools_frame, text=txt, font=("Arial", 10, "bold"), bg="#2f3640", fg="white", 
                          activebackground=col, activeforeground="white",
                          pady=10, bd=0, cursor="hand2", command=lambda: select_tool(tool))
            b.pack(fill="x", pady=2, padx=5)
            btn_list.append(b)
            btn_ref[tool] = b
            
            # Renk şeridi
            tk.Frame(tools_frame, bg=col, height=2).pack(fill="x", padx=5)

        create_tool_btn("🔋 PİL (1.5V)", "BATTERY", "#e74c3c")
        create_tool_btn("💡 AMPUL", "LAMP", "#f1c40f")
        create_tool_btn("🔌 ANAHTAR", "SWITCH", "#3498db")
        create_tool_btn("〰️ KABLO", "WIRE", "#e67e22")

        tk.Button(tools_frame, text="🗑️ TEMİZLE", bg="#c0392b", fg="white", font=("Arial", 10, "bold"), pady=10, bd=0, command=clear_all).pack(side="bottom", fill="x", pady=20, padx=5)

        # Event Bindings
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<Button-3>", on_right_click)

        # Kullanıcı İpucu
        lbl_hint = tk.Label(canvas, text="SOL: Ekle | SAĞ: Anahtar | Silmek için 'TEMİZLE' butonunu kullanın", bg="#191919", fg="#7f8c8d", font=("Arial", 9))
        lbl_hint.place(relx=0.5, rely=0.98, anchor="s")

        # İlk Başlangıç
        select_tool("WIRE")

    # [MODÜL 9] AI CHATBOT (AKILLI SÜRÜM - V2.0)
    def mod_ai_chat(self):
        self.set_header("AI ASİSTAN: PROF. PİXEL")
        
        chat_frame = tk.Frame(self.work, bg=CFG["COLORS"]["PANEL"])
        chat_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sohbet Geçmişi
        history = tk.Text(chat_frame, bg="#2d3436", fg="white", font=("Segoe UI", 12), state="disabled", wrap="word", padx=10, pady=10)
        history.pack(fill="both", expand=True, pady=(0, 10))
        
        # Giriş Alanı
        input_frame = tk.Frame(chat_frame, bg=CFG["COLORS"]["PANEL"])
        input_frame.pack(fill="x")
        
        entry_msg = tk.Entry(input_frame, font=("Arial", 14), bg="#dfe6e9", fg="black")
        entry_msg.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # --- YARDIMCI: TÜRKÇE NORMALİZASYON ---
        def normalize_text(text):
            # Türkçe karakter sorunlarını çözer
            replacements = {
                "İ": "i", "I": "ı", "Ş": "ş", "Ğ": "ğ", "Ü": "ü", "Ö": "ö", "Ç": "ç",
                "i": "i", "ı": "ı", "ş": "ş", "ğ": "ğ", "ü": "ü", "ö": "ö", "ç": "ç"
            }
            text = text.strip()
            for old, new in replacements.items():
                text = text.replace(old, new)
            return text.lower()

        # --- YARDIMCI: AKILLI ARAMA MOTORU ---
        def get_bot_response(user_input):
            norm_input = normalize_text(user_input)
            
            # 1. EŞ ANLAMLI SÖZLÜĞÜ (Kullanıcı dilini veritabanı diline çevirir)
            synonyms = {
                "su": "h2o", "enerji": "mitokondri", "şeker": "nükleotid", 
                "replikasyon": "eşlenme", "mendel": "kalıtım", "soyağacı": "kalıtım",
                "rampa": "eğik düzlem", "makara": "basit makine", "şimşek": "elektriklenme",
                "paslanma": "kimyasal değişim", "erime": "fiziksel değişim", 
                "katı": "katı basıncı", "sıvı": "sıvı basıncı", "gaz": "açık hava basıncı"
            }
            
            for word in norm_input.split():
                if word in synonyms:
                    norm_input = synonyms[word] # Aramayı bu kelime üzerinden yap
                    break

            keys = SCIENCE_DB.keys()

            # 2. STRATEJİ: TAM VEYA YAKIN EŞLEŞME (fuzzy matching)
            matches = difflib.get_close_matches(norm_input, keys, n=1, cutoff=0.6)
            if matches:
                key = matches[0]
                return f"💡 ({key.upper()}) -> {SCIENCE_DB[key]}"

            # 3. STRATEJİ: CÜMLE İÇİ ANAHTAR KELİME TARAMA
            best_match = None
            max_score = 0
            user_words = norm_input.split()
            
            for key in keys:
                if key in norm_input:
                    return f"💡 ({key.upper()}) hakkında bilgi: {SCIENCE_DB[key]}"

            # 4. STRATEJİ: TERSİNE ARAMA (TANIM TARAMA)
            for key, desc in SCIENCE_DB.items():
                norm_desc = normalize_text(desc)
                score = 0
                for word in user_words:
                    if len(word) > 3 and word in norm_desc: # 3 harften uzun kelimeleri ara
                        score += 1
                if score > max_score:
                    max_score = score
                    best_match = key

            if best_match and max_score >= 1:
                return f"🤔 Şunu mu kastettiniz: ({best_match.upper()})? \nBilgi: {SCIENCE_DB[best_match]}"

            return "Prof. Pixel: Üzgünüm, bunu veritabanımda bulamadım. 🧪\nLütfen 'DNA', 'Basınç', 'Mitoz', 'Asit' gibi bir fen kavramı sor."

        def send_msg(e=None):
            user_text = entry_msg.get()
            if not user_text: return
            
            entry_msg.delete(0, tk.END)
            
            # Kullanıcı mesajını ekle
            history.config(state="normal")
            history.insert(tk.END, f"Sen: {user_text}\n", "user")
            history.tag_config("user", foreground="#00d2d3", justify="right", rmargin=10)
            
            # Bot Cevabı
            response = get_bot_response(user_text)
            
            history.insert(tk.END, f"{response}\n\n", "bot")
            history.tag_config("bot", foreground="#f1c40f", justify="left", lmargin=10)
            history.config(state="disabled")
            history.see(tk.END)
            
        entry_msg.bind("<Return>", send_msg)
        
        # Gönder Butonu
        tk.Button(input_frame, text="GÖNDER", bg=CFG["COLORS"]["SUCCESS"], fg="black", font=("Arial", 10, "bold"), command=send_msg).pack(side="right")
        
        # Karşılama Mesajı
        history.config(state="normal")
        history.insert(tk.END, "Prof. Pixel: Laboratuvarıma hoş geldin!\n8. Sınıf LGS konularına hakimim. Bana 'Mevsimler nasıl oluşur?', 'DNA nedir?', 'Basınç' gibi sorular sorabilirsin.\n\n", "bot")
        history.config(state="disabled")

    # [MODÜL 10] PERFORMANS ANALİTİĞİ (RADAR CHART & SKILL BARS)
    def mod_analytics(self):
        self.set_header("PERFORMANS ANALİZİ: YETENEK HARİTASI")
        
        # --- VERİ ÇEKME ---
        cats = ["Fizik", "Kimya", "Biyoloji", "Matematik", "Genel"]
        values = []
        raw_percentages = []
        
        for c in cats:
            row = self.db.cur.execute("SELECT correct, total FROM performance WHERE user_id=? AND category=?", (self.user["id"], c)).fetchone()
            if row and row[1] > 0:
                perc = (row[0] / row[1]) * 100
                values.append(perc)
                raw_percentages.append(perc)
            else:
                values.append(0)
                raw_percentages.append(0)
        
        # --- ANA KONTEYNER (İKİ BÖLMELİ) ---
        container = tk.Frame(self.work, bg=CFG["COLORS"]["BG"])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. SOL PANEL: RADAR GRAFİĞİ
        left_panel = tk.Frame(container, bg="#1e272e")
        left_panel.pack(side="left", fill="both", expand=True)

        # Matplotlib Radar Grafiği Ayarları
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111, polar=True)
        ax.set_facecolor("#222")
        fig.patch.set_facecolor("#1e272e")

        # Açılar
        angles = np.linspace(0, 2 * np.pi, len(cats), endpoint=False).tolist()
        values += values[:1] # Kapatmak için başa dön
        angles += angles[:1]
        
        # Çizim (Modern Stil)
        ax.grid(color='#555', linestyle='--', linewidth=0.5, alpha=0.7)
        ax.plot(angles, values, color=CFG["COLORS"]["ACCENT"], linewidth=3, linestyle='solid', marker='o')
        ax.fill(angles, values, color=CFG["COLORS"]["ACCENT"], alpha=0.25)
        
        # Etiketler ve Eksen
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(cats, color="white", fontsize=11, fontweight="bold")
        ax.set_yticks([25, 50, 75, 100])
        ax.set_yticklabels(["", "", "", ""], color="#aaa", fontsize=8) 
        ax.set_ylim(0, 100)
        
        canvas = FigureCanvasTkAgg(fig, master=left_panel)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # 2. SAĞ PANEL: SKILL BARS & ÖZET
        right_panel = tk.Frame(container, bg=CFG["COLORS"]["PANEL"], width=400)
        right_panel.pack(side="right", fill="y", padx=(20, 0))
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="DERS BAŞARISI", font=("Segoe UI", 16, "bold"), fg="white", bg=CFG["COLORS"]["PANEL"]).pack(pady=(20, 20))

        # Skill Bars Oluşturma Döngüsü
        for i, cat in enumerate(cats):
            score = raw_percentages[i]
            
            row = tk.Frame(right_panel, bg=CFG["COLORS"]["PANEL"])
            row.pack(fill="x", padx=20, pady=8)
            
            header = tk.Frame(row, bg=CFG["COLORS"]["PANEL"])
            header.pack(fill="x")
            tk.Label(header, text=cat.upper(), font=("Arial", 10, "bold"), fg="#bdc3c7", bg=CFG["COLORS"]["PANEL"]).pack(side="left")
            tk.Label(header, text=f"%{int(score)}", font=("Arial", 10, "bold"), fg="white", bg=CFG["COLORS"]["PANEL"]).pack(side="right")
            
            # Progress Bar (Canvas ile özel çizim)
            pb_height = 10
            pb_width = 360
            cv_bar = tk.Canvas(row, height=pb_height, width=pb_width, bg="#444", highlightthickness=0)
            cv_bar.pack(pady=(5, 0))
            
            bar_color = CFG["COLORS"]["ERR"] # Kırmızı
            if score >= 50: bar_color = "#f1c40f" # Sarı
            if score >= 80: bar_color = CFG["COLORS"]["SUCCESS"] # Yeşil
            
            fill_width = (score / 100) * pb_width
            if fill_width > 0:
                cv_bar.create_rectangle(0, 0, fill_width, pb_height, fill=bar_color, outline="")

        # Özet Kartı (Alt Kısım)
        summary_frame = tk.Frame(right_panel, bg="#222", padx=15, pady=15, relief="ridge", bd=2)
        summary_frame.pack(fill="x", side="bottom", padx=20, pady=20)

        avg = sum(raw_percentages) / len(raw_percentages) if raw_percentages else 0
        
        if avg >= 80: 
            lvl_text = "UZMAN"
            lvl_col = CFG["COLORS"]["SUCCESS"]
            advice = "Harika gidiyorsun! Zirvedesin."
        elif avg >= 50: 
            lvl_text = "GELİŞİYOR"
            lvl_col = "#f1c40f"
            advice = "İyi bir temel attın, pratiğe devam et."
        else: 
            lvl_text = "BAŞLANGIÇ"
            lvl_col = "#ff6b6b"
            advice = "Daha fazla soru çözerek puanını artırabilirsin."

        tk.Label(summary_frame, text="GENEL ORTALAMA", font=("Arial", 9), fg="gray", bg="#222").pack(anchor="w")
        tk.Label(summary_frame, text=f"{int(avg)} / 100", font=("Impact", 28), fg="white", bg="#222").pack(anchor="w")
        tk.Frame(summary_frame, height=2, bg="#444").pack(fill="x", pady=10)
        tk.Label(summary_frame, text=f"SEVİYE: {lvl_text}", font=("Arial", 12, "bold"), fg=lvl_col, bg="#222").pack(anchor="w")
        tk.Label(summary_frame, text=advice, font=("Segoe UI", 9, "italic"), fg="#bdc3c7", bg="#222", wraplength=300).pack(anchor="w", pady=(5,0))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)

    root.mainloop()
