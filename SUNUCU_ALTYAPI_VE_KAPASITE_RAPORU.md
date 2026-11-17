# AVRASYA ÜNİVERSİTESİ YENİ NESİL WEB EKOSİSTEMİ
## YEREL SUNUCU (ON-PREMISE) DONANIM, KAPASİTE VE PERFORMANS RAPORU

**Sunulan Makam:** Avrasya Üniversitesi Rektörlük Makamı / Genel Sekreterlik  
**Konu:** 10.000+ Öğrenci Kapasiteli Yeni Üniversite Web Platformunun Yerel Sunucu (On-Premise) Donanım ve Altyapı Gereksinimleri  
**Tarih:** 09.11.2026  

---

### 1. YÖNETİCİ ÖZETİ VE GİRİŞ

Avrasya Üniversitesi'nin dijital dönüşüm vizyonu doğrultusunda geliştirilen yeni web ekosistemi; tüm fakülte, enstitü, yüksekokul, meslek yüksekokulu, bölüm, idari birim ve koordinatörlükleri tek bir çatı altında toplayan kapsamlı bir dijital platformdur. 

**10.000'in üzerinde aktif öğrencisi**, akademik/idari personeli ve ulusal/uluslararası aday öğrenci trafiği bulunan üniversitemizin web platformunun, üniversite bünyesindeki yerel sunucu (On-Premise) üzerinde **sıfır gecikme (zero-latency)**, **yüksek hız** ve **kesintisiz erişilebilirlik** ile çalışabilmesi için ihtiyaç duyulan donanım, depolama ve ağ altyapısı bu raporda teknik verilerle ortaya konulmuştur.

---

### 2. PROJENİN TEKNİK KAPSAMI VE MEVCUT VERİ BOYUTU

Geliştirilen platform standart bir tanıtım sitesi olmayıp, yüksek etkileşimli kurumsal bir web uygulamasıdır:
* **Modüler Mimari:** Sistemde fakülteler, bölümler, programlar, Kalite ve Akreditasyon Koordinatörlüğü, Öğrenci İşleri, Canlı Destek ve Personel İletişim Sistemi dahil olmak üzere **114 bağımsız uygulama (app)** ve **621 veritabanı modeli (544 tablo + 77 vekil model)** bulunmaktadır.
* **Küresel Çok Dilli Yapı:** Türkçe, İngilizce, Farsça, Arapça, Rusça ve Almanca olmak üzere **6 farklı dilde** eşzamanlı içerik ve arama desteği sunulmaktadır.
* **Gerçek Zamanlı (Real-Time) İletişim:** Aday öğrenciler için Canlı Destek (WebSockets / ASGI) ve akademik/idari personel için dosya paylaşımlı kurumsal iç mesajlaşma sistemi mevcuttur.

#### Mevcut Başlangıç Disk Boyutu (İlk Kurulum):
* **Tasarım ve Statik Dosyalar (`static/`):** ~115 MB (Sıkıştırılmış üretim dosyalarıyla birlikte ~230 MB)
* **Mevcut Medya ve İçerik Dosyaları (`media/`):** ~567 MB (Haber görselleri, afişler, ders programları, kalite belgeleri)
* **Uygulama Kaynak Kodları ve Python Sanal Ortamı (`venv`):** ~350 MB
* **İlk Kurulum Toplam Disk Kullanımı:** **Yaklaşık 1.5 GB**

---

### 3. DEPOLAMA (DİSK) KAPASİTESİ VE 5 YILLIK BÜYÜME PROJEKSİYONU

Projenin ilk kurulum boyutu (~1.5 GB) küçük olsa da; 114 birimin düzenli olarak yükleyeceği yüksek çözünürlüklü haber fotoğrafları, etkinlik afişleri, kalite ve akreditasyon (BİDR/KİDR) raporları, ders programı PDF'leri, ana sayfa tanıtım videoları ve personel sohbet sistemi dosya paylaşımları nedeniyle disk alanı yıllar içinde düzenli olarak büyüyecektir.

| Sistem Bileşeni | 1. Yıl Öngörülen Alan | 5 Yıllık Öngörülen Alan | Açıklama |
| :--- | :--- | :--- | :--- |
| **İşletim Sistemi (Ubuntu Server) & Paketler** | 20 GB | 25 GB | Sistem dosyaları, Python, PostgreSQL, Nginx, Redis |
| **PostgreSQL Veritabanı** | 5 GB | 20 - 25 GB | 544 tablo, 6 dilde metinler, duyurular, mesaj ve destek kayıtları |
| **Medya Dosyaları (`media/`)** | 35 - 50 GB | 150 - 250 GB | Haber/etkinlik görselleri, PDF/Word belgeleri, tanıtım videoları |
| **Sistem ve Güvenlik Kayıtları (Logs)** | 10 GB | 30 GB | Nginx erişim kayıtları, güvenlik ve veritabanı logları |
| **Yerel Otomatik Yedekleme (Daily Backups)** | 50 GB | 150 - 200 GB | Veritabanı ve medya dosyalarının günlük/haftalık yerel yedekleri |
| **TOPLAM İHTİYAÇ** | **~120 GB** | **~450 - 500 GB** | **Güvenli çalışma payı ile birlikte** |

#### Depolama Sonucu ve Kritik Teknik Şart:
* **Minimum Disk Kapasitesi:** **250 GB**
* **Önerilen (İdeal) Disk Kapasitesi:** **500 GB – 1 TB** (5 yıl boyunca ek disk yatırımı gerektirmemesi ve yerel yedeklerin güvenle tutulabilmesi için 1 TB kapasite idealdir).
* **Disk Teknolojisi (Hayati Önemde):** Sunucu diskleri kesinlikle mekanik sabit disk (**HDD**) **olmamalıdır**. Yüzlerce öğrencinin aynı anda sayfa ve belge açtığı yoğun saatlerde gecikme yaşanmaması için yüksek okuma/yazma hızına (IOPS) sahip **Kurumsal NVMe SSD** (veri güvenliği için **RAID 1** veya **RAID 10** yapısında) kullanılmalıdır.

---

### 4. 10.000+ ÖĞRENCİ İÇİN ÖNERİLEN SUNUCU DONANIM ÖZELLİKLERİ

10.000'den fazla öğrencisi olan bir üniversitede, normal günlerde sitede eşzamanlı **50 ila 150 ziyaretçi** bulunurken; **sınav takvimi açıklamaları, ders kayıt dönemleri, YKS tercih günleri ve önemli duyuru anlarında** eşzamanlı kullanıcı sayısı **500 ila 1.500 kişiye** çıkmaktadır. Sitenin bu yoğun (pik) anlarda dahi **1 saniyenin altında** açılması için gereken donanım tablosu aşağıdadır:

| Donanım Bileşeni | Minimum Kabul Edilebilir | **Önerilen (Sıfır Gecikme & Yüksek Performans)** | Teknik Gerekçe |
| :--- | :--- | :--- | :--- |
| **Bellek (RAM)** | 16 GB DDR4 | **32 GB DDR4 / DDR5 ECC RAM** | 32 GB RAM sayesinde tüm PostgreSQL veritabanı ve Redis önbelleği tamamen RAM üzerinde çalışır; sorgular 1 milisaniyenin altında yanıtlanır. |
| **İşlemci (CPU)** | 8 Çekirdek (8 Cores / vCPU) | **12 veya 16 Çekirdek (Intel Xeon / AMD EPYC)** | Aynı anda hem web sayfalarını, hem canlı destek WebSocket bağlantılarını hem de görsel optimizasyonlarını kesintisiz işlemek için gereklidir. |
| **Depolama (Storage)** | 256 GB SSD | **512 GB veya 1 TB NVMe SSD (RAID 1)** | Yüksek eşzamanlı dosya ve veritabanı okuma/yazma hızı (3.000+ MB/sn) sağlar. |
| **Ağ Kartı (NIC)** | 1 Gbps | **1 Gbps / 10 Gbps Ethernet** | Kampüs içi ve dışı yüksek veri trafiğini darboğaz olmadan iletir. |
| **İnternet Çıkış (Upload) Hızı** | 100 Mbps Simetrik | **300 - 500+ Mbps Simetrik (Dedicated Upload)** | Sunucu üniversite içinde barındırılacağından, dışarıdan bağlanan öğrencilere veriyi sunucunun **Upload (Yükleme)** hattı gönderecektir. |

---

### 5. MAKSİMUM HIZ İÇİN 4 KRİTİK ALTYAPI VE YAZILIM ÖNERİSİ

Sunucu donanımının yanı sıra, sitenin en yüksek hızda açılması için aşağıdaki 4 mimari adımın uygulanması gerekmektedir:

1. **İnternet Upload Bant Genişliği ve CDN (Cloudflare) Kullanımı:**
   * Yerel sunucularda en büyük darboğaz donanım değil, kurumun dış dünyaya olan **İnternet Upload (Yükleme) hızıdır**. 
   * Kampüs dışındaki binlerce öğrencinin görselleri ve videoları anında yükleyebilmesi için üniversitenin simetrik internet çıkış hızının yüksek olması; ayrıca `avrasya.edu.tr` alan adının **Cloudflare CDN** üzerinden geçirilerek statik dosyaların ve görsellerin bulut önbellekten sunulması (sunucu internet trafiğini %70 oranında rahatlatır) şiddetle önerilir.
2. **Çok Çekirdekli ASGI / Uvicorn İşçi (Worker) Yapılandırması:**
   * 12–16 çekirdekli bir sunucuda uygulama sunucusu (Gunicorn + UvicornWorker) **8 ila 12 paralel worker** ile çalıştırılmalıdır. Bu sayede aynı anda gelen yüzlerce talep sıraya girmeden anında işlenir.
3. **Redis Önbellek (In-Memory Cache) Kullanımı:**
   * Ana sayfa akışları, duyuru sayaçları ve akıllı arama sonuçları `Redis` üzerinde RAM'de önbelleklenerek veritabanı yükü minimuma indirilmektedir.
4. **Nginx Sıkıştırma (`gzip`/`brotli`) ve Tarayıcı Önbellekleme:**
   * Web sunucusu katmanında (Nginx) `gzip` sıkıştırması ve statik/medya dosyaları için `30 günlük tarayıcı önbelleklemesi (expires 30d)` aktif edilerek, siteye tekrar giren bir öğrencide sayfaların **anında (0.2 saniye altında)** açılması sağlanacaktır.

---

### 6. SONUÇ

Özetle; Avrasya Üniversitesi'nin yeni web ekosisteminin **10.000+ öğrenci** ve tüm paydaşlara uzun yıllar boyunca **en üst düzey hız, güvenlik ve kararlılıkla** hizmet verebilmesi için:
* **12 - 16 Çekirdek İşlemci (CPU)**,
* **32 GB ECC RAM**,
* **512 GB veya 1 TB Kurumsal NVMe SSD (RAID 1)**,
* **Yüksek Simetrik Upload İnternet Çıkışı + CDN Desteği**

özelliklerine sahip bir yerel sunucu altyapısının tahsis edilmesi teknik olarak en doğru ve uzun ömürlü yatırım olacaktır.

Saygılarımla,  
**Web Yazılım ve Altyapı Geliştirme Ekibi**

