# Avrasya Üniversitesi Yeni Nesil Web Ekosistemi: Teknik İnceleme ve Kapsam Raporu

**Hazırlayan:** Antigravity (Yazılım Mimarı & Django Uzmanı)
**Kime:** Avrasya Üniversitesi Rektörlük Makamı

## Giriş
Avrasya Üniversitesi'nin dijital dönüşüm stratejisinin bir parçası olarak geliştirilen bu web platformu, modern üniversitelerin ihtiyaç duyduğu hız, güvenlik ve erişilebilirlik standartlarını en üst seviyede karşılamak üzere tasarlanmıştır. Django framework'ü ile "clean code" prensiplerine uygun olarak inşa edilen bu proje, sadece bir web sitesi değil, üniversitenin tüm akademik ve idari birimlerini kapsayan devasa bir dijital ekosistemdir.

---

## 1. Mimarlık ve Altyapı
Sistemin kalbinde, dünya çapında (Instagram, Pinterest gibi) büyük platformların tercihi olan **Django 4.2+** altyapısı bulunmaktadır. 

*   **Modüler Yapı (Micro-app Architecture):** Proje, 80'den fazla bağımsız uygulamadan (app) oluşmaktadır. Her fakülte, enstitü ve idari birim (örn: Mühendislik Mimarlık Fakültesi, Sağlık Hizmetleri MYO, Öğrenci İşleri vb.) kendi veri yapısına ve yönetim paneline sahiptir. Bu yapı, sistemin bakımını kolaylaştırırken sınırsız genişleyebilirlik sağlar.
*   **Veritabanı Gücü:** Verilerin güvenli ve hızlı bir şekilde işlenmesi için endüstri standardı olan **PostgreSQL** veritabanı kullanılmaktadır.
*   **Asenkron İşlemler:** Gerçek zamanlı trafik ve veri akışı için **ASGI** protokolü ve **Django Channels** entegre edilmiştir.

## 2. Küresel Erişim: Çoklu Dil ve Uluslararasılaşma
Üniversitemizin uluslararası vizyonuna uygun olarak sistem, dünya dillerini tam kapsamlı desteklemektedir:
*   **6 Farklı Dil Desteği:** Türkçe'nin yanı sıra İngilizce, Farsça, Arapça, Rusça ve Almanca dillerinde içerik yönetimi yapılabilmektedir.
*   **RTL (Sağdan Sola) Uyumluluğu:** Arapça ve Farsça gibi sağdan sola yazılan diller için özel arayüz tasarımı otomatik olarak devreye girmektedir.
*   **Dinamik Çeviri:** `django-modeltranslation` teknolojisi sayesinde haberler, duyurular ve akademik içerikler her dilde bağımsız olarak yönetilmektedir.

## 3. İletişim, Destek ve İşbirliği Ekosistemi
Üniversiteler için paydaşlar arası iletişim hayati önem taşır. Bu platformda üç temel iletişim katmanı bulunmaktadır:
*   **Canlı Destek (Canlı Destek / Live Chat):** WebSockets ve Django Channels teknolojisi ile geliştirilmiş, öğrenci adayları ve ziyaretçiler için anlık çözüm sunan bir sistemdir. "Canlı Destek" modülü, personelin gelen talepleri gerçek zamanlı olarak yanıtlamasına olanak tanır.
*   **Resmi Destek Talebi (Ticket) Sistemi:** Kullanıcıların daha karmaşık sorunlarını departman bazlı iletebileceği ve çözüm sürecini adım adım takip edebileceği profesyonel bir biletleme sistemidir.
*   **Personel İşbirliği Sistemi (Internal Staff Chat):** Akademik ve idari personelin kendi aralarında güvenli bir şekilde dosya paylaşımı yapabileceği ve anlık iletişim kurabileceği kurumsal bir sohbet platformu.
*   **SMTP ve Bildirim Entegrasyonu:** Destek talepleri ve önemli güncellemeler için Office365 üzerinden çalışan otomatik bildirim sistemleri.

## 4. Akıllı Arama ve Bilgi Yönetimi
Sitedeki devasa içerik yığını içerisinde bilgiye hızlı erişim için özel bir arama motoru geliştirilmiştir:
*   **Akıllı Arama (Smart Search):** Kullanıcıların anahtar kelime veya soru bazlı aramalarına (Q&A) saniyeler içinde doğru sonucu getiren dinamik bir arama altyapısı mevcuttur.
*   **Bilgi Bankası (Knowledge Base):** Sıkça sorulan sorular (SSS-FAQ), rehberler ve kurumsal bilgiler akıllı arama ile tam uyumlu çalışmaktadır.

## 5. Modern Tasarım ve Kullanıcı Deneyimi (UX/UI)
Sitenin görsel dili, kurumsal kimliği modern çizgilerle birleştirmektedir:
*   **Premium Estetik:** Glassmorphism (cam efekti), yumuşak geçişler (animations) ve derinlik katan katmanlı tasarım.
*   **Mega Navbar:** Karmaşık akademik yapıyı tek tıkla ulaşılabilir kılan, ikonlarla zenginleştirilmiş geniş menü sistemi.
*   **Tam Duyarlılık (Responsive Design):** Mobil cihazlar, tabletler ve masaüstü bilgisayarlarda kusursuz görüntüleme.
*   **Zengin İçerik Sunumu:** Video entegrasyonu, gelişmiş galeri (lightbox) sistemleri ve interaktif haritalar.

## 5. Güvenlik ve Veri Koruma
Sistem, üniversitenin verilerini en üst düzeyde korumak için zırhlı bir yapıya sahiptir:
*   **Brute Force Koruması:** `django-axes` ile kötü niyetli giriş denemelerine karşı otomatik engelleme.
*   **SSL/HTTPS ve HSTS:** Veri transferi için en güvenli şifreleme protokolleri.
*   **Gelişmiş Session Yönetimi:** Kullanıcı oturumlarının güvenliğini sağlayan gelişmiş middleware yapıları.

## 6. İçerik ve Akademik Yönetim
*   **Kullanıcı Dostu Editörler:** CKEditor entegrasyonu ile teknik bilgisi olmayan personeller bile zengin görselli sayfalar oluşturabilir.
*   **Haber ve Duyuru Yönetimi:** Kategorize edilmiş, tarih bazlı ve çok dilli haber akış sistemleri.
*   **Kurumsal Entegrasyonlar:** OBS, EBYS, Bologna süreci ve Online Eğitim sistemlerine tek noktadan erişim köprüleri.

---

## Sonuç
Bu proje, Avrasya Üniversitesi'nin dijital vitrinini en prestijli seviyeye taşımakla kalmayıp, operasyonel süreçleri dijitalleştiren güçlü bir yönetim aracıdır. Gelişmiş mimarisi sayesinde önümüzdeki on yılın teknolojik değişimlerine ayak uydurabilecek esnekliktedir.

**Avrasya Üniversitesi için, geleceğin teknolojisiyle bugün tamamlanmıştır.**
