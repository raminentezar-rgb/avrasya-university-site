"""
Avrasya Üniversitesi - Sesli Asistan Kapsamlı Konu ve Uygulama Dizini
Bu modül sitedeki tüm uygulamaları (apps), fakülteleri, bölümleri, MYO ve SHMYO programlarını,
koordinatörlükleri (özellikle Kalite ve Akreditasyon), öğrenci işlerini ve idari birimleri kapsar.
"""

from django.urls import reverse
from django.utils.translation import gettext as _
import unicodedata
import re

# Tüm Uygulama ve Konuların Tanımları (120+ Konu)
TOPICS_DEFINITIONS = [
    # =========================================================================
    # 1. KURUMSAL & GENEL
    # =========================================================================
    {
        'id': 'anasayfa',
        'title': 'Ana Sayfa',
        'category': 'Genel',
        'icon': 'fa-house',
        'url_name': 'core:home',
        'description': 'Avrasya Üniversitesi resmi ana sayfası. Güncel haberler, duyurular, etkinlikler, hızlı erişim bağlantıları ve kampüs bilgileri burada yer alır.',
        'keywords': ['ana sayfa', 'anasayfa', 'giriş', 'ana sayfaya', 'home', 'portal', 'avrasya'],
        'quick_links': [
            {'title': 'Son Haberler', 'url': '/#news'},
            {'title': 'Duyurular', 'url': '/#announcements'},
            {'title': 'Etkinlikler', 'url': '/#etkinlikler'}
        ]
    },
    {
        'id': 'hakkimizda',
        'title': 'Üniversitemiz Hakkında',
        'category': 'Kurumsal',
        'icon': 'fa-building-columns',
        'url_name': 'avrasya_universitesi_hakkinda:anasayfa',
        'description': 'Avrasya Üniversitesinin kuruluş tarihçesi, misyonu, vizyonu, temel değerleri, eğitim felsefesi ve kampüs yerleşkeleri hakkında genel bilgiler.',
        'keywords': ['hakkında', 'hakkımızda', 'tarihçe', 'misyon', 'vizyon', 'felsefemiz', 'kampüsler', 'universite hakkinda'],
        'quick_links': [
            {'title': 'Felsefemiz', 'url_name': 'avrasya_universitesi_hakkinda:felsefemiz'},
        ]
    },
    {
        'id': 'yonetim',
        'title': 'Üniversite Yönetimi',
        'category': 'Kurumsal',
        'icon': 'fa-users-gear',
        'url_name': 'avrasya_universitesi_yonetim:mutevelli_heyeti',
        'description': 'Mütevelli Heyeti, Rektörlük, Senato ve Üniversite Yönetim Kurulu üyeleri ile teşkilat yapısı hakkında resmi bilgiler.',
        'keywords': ['yönetim', 'mütevelli heyeti', 'rektör', 'rektörlük', 'senato', 'yönetim kurulu', 'genel sekreter'],
        'quick_links': []
    },
    {
        'id': 'iletisim',
        'title': 'İletişim ve Ulaşım',
        'category': 'Kurumsal',
        'icon': 'fa-location-dot',
        'url_name': 'core:iletisim',
        'description': 'Pelitli, Yomra ve Kaşüstü yerleşkelerimizin telefon numaraları, e-posta adresleri, açık posta adresleri ve ulaşım krokileri.',
        'keywords': ['iletişim', 'telefon', 'adres', 'nerede', 'ulaşım', 'harita', 'konum', 'bize ulaşın', 'pelitli', 'yomra', 'kaşüstü'],
        'quick_links': []
    },
    {
        'id': 'galeri',
        'title': 'Fotoğraf ve Video Galerisi',
        'category': 'Genel',
        'icon': 'fa-images',
        'url_name': 'gallery:main',
        'description': 'Üniversitemizin yerleşkeleri, modern laboratuvarları, derslikleri, sosyal tesisleri ve etkinliklerinden fotoğraf ve video arşivi.',
        'keywords': ['galeri', 'fotoğraf', 'resim', 'video', 'kampüs resimleri', 'foto galeri'],
        'quick_links': []
    },

    # =========================================================================
    # 2. KALİTE VE AKREDİTASYON KOORDİNATÖRLÜĞÜ (ÖZEL YENİ APP)
    # =========================================================================
    {
        'id': 'kalite_home',
        'title': 'Kalite ve Akreditasyon Koordinatörlüğü',
        'category': 'Koordinatörlük',
        'icon': 'fa-award',
        'url_name': 'kalite_akreditasyon:home',
        'description': 'Üniversitemizin eğitim-öğretim, araştırma ve idari süreçlerinde kalite güvencesi kültürünü geliştiren, YÖKAK akreditasyon süreçlerini yürüten ve stratejik planlamayı koordine eden birimdir.',
        'keywords': ['kalite', 'akreditasyon', 'kalite koordinatörlüğü', 'kalite ve akreditasyon', 'yökak', 'kidr', 'akredite', 'kalite güvencesi'],
        'quick_links': [
            {'title': 'Hakkında & Komisyon', 'url_name': 'kalite_akreditasyon:hakkinda'},
            {'title': 'Mevzuat', 'url_name': 'kalite_akreditasyon:mevzuat'},
            {'title': 'Raporlar', 'url_name': 'kalite_akreditasyon:raporlar'},
            {'title': 'Duyurular', 'url_name': 'kalite_akreditasyon:duyurular'},
            {'title': 'Haberler', 'url_name': 'kalite_akreditasyon:haberler'},
            {'title': 'Takım', 'url_name': 'kalite_akreditasyon:takim'},
            {'title': 'S.S.S', 'url_name': 'kalite_akreditasyon:sss'}
        ]
    },
    {
        'id': 'kalite_hakkinda',
        'title': 'Kalite Hakkında ve Komisyonlar',
        'category': 'Koordinatörlük',
        'icon': 'fa-circle-info',
        'url_name': 'kalite_akreditasyon:hakkinda',
        'description': 'Kalite Koordinatörlüğü Yönetimi, Kalite Komisyon Üyeleri, Alt Çalışma Grupları, Danışma Kurulu, Kurum Kalite Politikası, Stratejik Plan ve Organizasyon Şeması bilgileri.',
        'keywords': ['kalite hakkında', 'kalite komisyonu', 'çalışma grupları', 'danışma kurulu', 'kalite politikası', 'stratejik plan', 'organizasyon şeması'],
        'quick_links': []
    },
    {
        'id': 'kalite_duyurular',
        'title': 'Kalite Duyuruları',
        'category': 'Koordinatörlük',
        'icon': 'fa-bullhorn',
        'url_name': 'kalite_akreditasyon:duyurular',
        'description': 'Kalite ve akreditasyon süreçleri, anket çalışmaları, iç ve dış değerlendirme toplantıları ile ilgili güncel duyurular.',
        'keywords': ['kalite duyuruları', 'kalite duyuru', 'akreditasyon duyurusu', 'kalite anket'],
        'quick_links': []
    },
    {
        'id': 'kalite_haberler',
        'title': 'Kalite Haberleri',
        'category': 'Koordinatörlük',
        'icon': 'fa-newspaper',
        'url_name': 'kalite_akreditasyon:haberler',
        'description': 'Üniversitemizde yürütülen kalite toplantıları, akreditasyon saha ziyaretleri, çalıştaylar ve başarı haberleri.',
        'keywords': ['kalite haberleri', 'kalite haber', 'akreditasyon haberi', 'yökak ziyareti'],
        'quick_links': []
    },
    {
        'id': 'kalite_mevzuat',
        'title': 'Kalite Mevzuatı ve Yönergeleri',
        'category': 'Koordinatörlük',
        'icon': 'fa-scale-balanced',
        'url_name': 'kalite_akreditasyon:mevzuat',
        'description': 'YÖKAK Kalite Güvencesi Yönetmeliği, Avrasya Üniversitesi Kalite Güvencesi Yönergesi ve akreditasyon standartları mevzuatı.',
        'keywords': ['kalite mevzuatı', 'kalite yönergesi', 'kalite yönetmelik', 'yökak yönetmeliği'],
        'quick_links': []
    },
    {
        'id': 'kalite_takim',
        'title': 'Kalite Koordinatörlüğü Ekibi',
        'category': 'Koordinatörlük',
        'icon': 'fa-users',
        'url_name': 'kalite_akreditasyon:takim',
        'description': 'Kalite ve Akreditasyon Koordinatörü, koordinatör yardımcıları, uzman personeller ve alt komisyon temsilcileri listesi.',
        'keywords': ['kalite takımı', 'kalite ekibi', 'kalite koordinatörü', 'kalite komisyon üyeleri'],
        'quick_links': []
    },
    {
        'id': 'kalite_raporlar',
        'title': 'Kalite Raporları ve KİDR',
        'category': 'Koordinatörlük',
        'icon': 'fa-file-lines',
        'url_name': 'kalite_akreditasyon:raporlar',
        'description': 'Kurum İç Değerlendirme Raporları (KİDR), Geri Bildirim Raporları, memnuniyet anket sonuçları ve akreditasyon izleme raporları.',
        'keywords': ['kalite raporları', 'kidr', 'kurum iç değerlendirme raporu', 'öz değerlendirme', 'geri bildirim raporu'],
        'quick_links': []
    },
    {
        'id': 'kalite_izleme',
        'title': 'Kalite İzleme ve İyileştirme',
        'category': 'Koordinatörlük',
        'icon': 'fa-chart-line',
        'url_name': 'kalite_akreditasyon:izleme',
        'description': 'Planla-Uygula-Kontrol Et-Önlem Al (PUKÖ) döngüleri, performans göstergeleri ve sürekli iyileştirme mekanizmaları.',
        'keywords': ['kalite izleme', 'pukö döngüsü', 'performans göstergeleri', 'iyileştirme süreçleri'],
        'quick_links': []
    },
    {
        'id': 'kalite_dokuman',
        'title': 'Kalite Dokümanları ve Formlar',
        'category': 'Koordinatörlük',
        'icon': 'fa-folder-open',
        'url_name': 'kalite_akreditasyon:dokuman',
        'description': 'Kalite süreçlerinde kullanılan standart formlar, rehberler, iş akış şemaları ve değerlendirme dokümanları.',
        'keywords': ['kalite doküman', 'kalite formları', 'iş akış şeması', 'süreç kartları'],
        'quick_links': []
    },
    {
        'id': 'kalite_sss',
        'title': 'Kalite Sıkça Sorulan Sorular',
        'category': 'Koordinatörlük',
        'icon': 'fa-circle-question',
        'url_name': 'kalite_akreditasyon:sss',
        'description': 'Kalite güvencesi sistemi, YÖKAK akreditasyonu ve koordinatörlük çalışmaları hakkında sıkça sorulan sorular ve cevapları.',
        'keywords': ['kalite sss', 'kalite soruları', 'akreditasyon nedir', 'kalite güvencesi nedir'],
        'quick_links': []
    },

    # =========================================================================
    # 3. ÖĞRENCİ HİZMETLERİ & MALİ İŞLER
    # =========================================================================
    {
        'id': 'aday_ogrenci',
        'title': 'Aday Öğrenci Portalı',
        'category': 'Öğrenci Hizmetleri',
        'icon': 'fa-user-graduate',
        'url_name': 'aday_ogrenci:aday_anasayfa',
        'description': 'Üniversite adayları için kontenjanlar, taban puanlar, tercih rehberi, kampüs yaşamı ve burs seçenekleri hakkında detaylı bilgiler.',
        'keywords': ['aday', 'aday öğrenci', 'adaylar', 'tercih', 'kontenjan', 'taban puan', 'yks', 'ösym'],
        'quick_links': []
    },
    {
        'id': 'ogrenci_isleri',
        'title': 'Öğrenci İşleri Daire Başkanlığı',
        'category': 'Öğrenci Hizmetleri',
        'icon': 'fa-id-card',
        'url_name': 'ogrenci_isleri:ogrenci_isleri',
        'description': 'Öğrenci kayıtları, transkript, öğrenci belgesi, ders seçimi, askerlik tecili ve mezuniyet işlemlerinin yürütüldüğü idari dairedir.',
        'keywords': ['öğrenci işleri', 'transkript', 'öğrenci belgesi', 'ders kaydı', 'obs', 'mezuniyet'],
        'quick_links': []
    },
    {
        'id': 'kayit_islemleri',
        'title': 'Kayıt İşlemleri Rehberi',
        'category': 'Öğrenci Hizmetleri',
        'icon': 'fa-file-signature',
        'url_name': 'ogrenci_isleri:kayit',
        'description': 'Yeni kayıt yaptıracak öğrenciler için e-Devlet üzerinden kayıt adımları, şahsen kayıt belgeleri ve kayıt kılavuzu.',
        'keywords': ['kayıt', 'kayıt işlemleri', 'yeni kayıt', 'e-devlet kayıt', 'kesin kayıt', 'nasıl kayıt olurum'],
        'quick_links': []
    },
    {
        'id': 'ogrenim_ucretleri',
        'title': 'Öğrenim Ücretleri ve Harçlar',
        'category': 'Mali Hizmetler',
        'icon': 'fa-money-bill-wave',
        'url_name': 'ogrenci_isleri:ogrenim_ucretleri',
        'description': 'Fakülteler ve meslek yüksekokulları bölümlerinin yıllık öğrenim ücretleri, taksitlendirme seçenekleri ve banka anlaşmaları.',
        'keywords': ['ücret', 'ücretler', 'öğrenim ücretleri', 'harç', 'fiyat', 'fiyatlar', 'bölüm ücreti', 'kaç para', 'taksit'],
        'quick_links': []
    },
    {
        'id': 'tuition_odeme',
        'title': 'Online Harç ve Ödeme Portalı',
        'category': 'Mali Hizmetler',
        'icon': 'fa-credit-card',
        'url_name': 'tuition:index',
        'description': 'Öğrenim ücreti, harç ve taksit ödemelerinin kredi kartı ile 3D Secure güvenliğiyle online olarak ödenebildiği sistem.',
        'keywords': ['ödeme', 'online ödeme', 'harç öde', 'kartla öde', 'taksit öde', 'tuition'],
        'quick_links': []
    },
    {
        'id': 'burslar',
        'title': 'Burslar ve İndirim Olanakları',
        'category': 'Öğrenci Hizmetleri',
        'icon': 'fa-hand-holding-dollar',
        'url_name': 'ogrenci_isleri:burslar',
        'description': 'ÖSYM başarı bursları, tercih indirimleri, kardeş indirimi, şehit/gazi yakını bursu ve akademik başarı bursları şartları.',
        'keywords': ['burs', 'burslar', 'indirim', 'tercih indirimi', 'kardeş indirimi', 'tam burs', 'yarı burs'],
        'quick_links': []
    },
    {
        'id': 'akademik_takvim',
        'title': 'Akademik Takvim',
        'category': 'Öğrenci Hizmetleri',
        'icon': 'fa-calendar-days',
        'url_name': 'ogrenci_isleri:akademik_takvim',
        'description': 'Güz ve bahar yarıyılları için kayıt yenileme, ders başlangıç, vize sınavları, final sınavları ve tatil tarihleri.',
        'keywords': ['akademik takvim', 'takvim', 'sınav tarihleri', 'vizeler', 'finaller', 'tatil ne zaman', 'kayıt yenileme'],
        'quick_links': []
    },
    {
        'id': 'yurtlar',
        'title': 'Yurt Olanakları ve Barınma',
        'category': 'Öğrenci Hizmetleri',
        'icon': 'fa-hotel',
        'url_name': 'ogrenci_isleri:yurtlar',
        'description': 'Üniversitemiz bünyesindeki ve anlaşmalı kız ve erkek öğrenci yurtları, konaklama ücretleri, güvenlik ve oda imkânları.',
        'keywords': ['yurt', 'yurtlar', 'barınma', 'konaklama', 'öğrenci yurdu', 'kız yurdu', 'erkek yurdu', 'pansiyon'],
        'quick_links': []
    },
    {
        'id': 'yatay_gecis',
        'title': 'Yatay Geçiş İşlemleri',
        'category': 'Öğrenci Hizmetleri',
        'icon': 'fa-arrow-right-arrow-left',
        'url_name': 'yatay_gecis:yatay_gecis',
        'description': 'Başka üniversitelerden Avrasya Üniversitesine veya kurum içi bölümler arası yatay geçiş şartları, kontenjanları ve başvuru takvimi.',
        'keywords': ['yatay geçiş', 'ek madde 1', 'merkezi yerleştirme puanıyla', 'gano', 'kurumlararası geçiş'],
        'quick_links': []
    },

    # =========================================================================
    # 4. SAĞLIK, KÜLTÜR VE SPOR (SKS) & YAŞAM
    # =========================================================================
    {
        'id': 'sks',
        'title': 'Sağlık, Kültür ve Spor Daire Başkanlığı (SKS)',
        'category': 'Öğrenci Yaşamı',
        'icon': 'fa-volleyball',
        'url_name': 'sks:home',
        'description': 'Öğrenci kulüpleri, yemekhane aylık menüsü, kapalı spor salonları, turnuvalar, sağlık revir hizmetleri ve sosyal etkinlikler.',
        'keywords': ['sks', 'yemekhane', 'yemek menüsü', 'spor salonu', 'öğrenci kulüpleri', 'kulüp', 'revir', 'etkinlik'],
        'quick_links': []
    },

    # =========================================================================
    # 5. HABER, DUYURU, ETKİNLİK
    # =========================================================================
    {
        'id': 'haberler',
        'title': 'Üniversite Haberleri',
        'category': 'Haber & Duyuru',
        'icon': 'fa-newspaper',
        'url_name': 'news:list',
        'description': 'Avrasya Üniversitesinden en güncel bilimsel başarılar, etkinlikler, protokoller ve basın bültenleri.',
        'keywords': ['haber', 'haberler', 'güncel', 'gelişmeler', 'gazete', 'bülten'],
        'quick_links': []
    },
    {
        'id': 'duyurular',
        'title': 'Genel Duyurular',
        'category': 'Haber & Duyuru',
        'icon': 'fa-bell',
        'url_name': 'duyurular:liste',
        'description': 'Öğrencilerimiz, akademik kadromuz ve idari personelimiz için yayımlanan tüm resmi kurumsal duyurular.',
        'keywords': ['duyuru', 'duyurular', 'resmi duyuru', 'ilan', 'ilanlar'],
        'quick_links': []
    },
    {
        'id': 'etkinlikler',
        'title': 'Etkinlikler ve Konferanslar',
        'category': 'Haber & Duyuru',
        'icon': 'fa-calendar-check',
        'url_name': 'etkinlikler:liste',
        'description': 'Üniversitemizde düzenlenen sempozyumlar, kariyer günleri, seminerler, paneller ve konserler takvimi.',
        'keywords': ['etkinlik', 'etkinlikler', 'konferans', 'seminer', 'sempozyum', 'kariyer günleri', 'workshop'],
        'quick_links': []
    },

    # =========================================================================
    # 6. ARAŞTIRMA, KÜTÜPHANE, DIŞ İLİŞKİLER, ENSTİTÜ
    # =========================================================================
    {
        'id': 'kutuphane',
        'title': 'Kütüphane ve Dokümantasyon',
        'category': 'Araştırma',
        'icon': 'fa-book-bookmark',
        'url_name': 'kutuphane:kutuphane',
        'description': 'Zengin basılı kitap koleksiyonu, uluslararası e-veritabanları, katalog tarama sistemi ve açık erişim araştırma portalı.',
        'keywords': ['kütüphane', 'kitap', 'dergi', 'veri tabanı', 'katalog tarama', 'açık erişim', 'e-kaynak'],
        'quick_links': []
    },
    {
        'id': 'arastirma',
        'title': 'Araştırma ve Laboratuvarlar',
        'category': 'Araştırma',
        'icon': 'fa-flask-vial',
        'url_name': 'arastirma:home',
        'description': 'Bilimsel Araştırma Projeleri (BAP), merkezi araştırma laboratuvarları, uygulama merkezleri ve patent çalışmaları.',
        'keywords': ['araştırma', 'laboratuvar', 'bap', 'bilimsel proje', 'tübitak', 'tto', 'teknoloji transfer'],
        'quick_links': []
    },
    {
        'id': 'erasmus',
        'title': 'Erasmus Koordinatörlüğü',
        'category': 'Dış İlişkiler',
        'icon': 'fa-earth-europe',
        'url_name': 'erasmus:erasmus',
        'description': 'Avrupa Birliği Erasmus+ öğrenci öğrenim ve staj hareketliliği, başvuru şartları, hibe oranları ve anlaşmalı üniversiteler.',
        'keywords': ['erasmus', 'öğrenci değişimi', 'avrupa', 'staj hareketliliği', 'yurt dışı eğitim'],
        'quick_links': []
    },
    {
        'id': 'international',
        'title': 'Uluslararası Öğrenci Ofisi',
        'category': 'Dış İlişkiler',
        'icon': 'fa-globe',
        'url_name': 'international:international',
        'description': 'Yabancı uyruklu öğrenci kabul şartları, vize-ikamet süreçleri, denklik ve uluslararası ortaklıklar.',
        'keywords': ['uluslararası', 'international', 'yabancı öğrenci', 'foreign students', 'yös'],
        'quick_links': []
    },
    {
        'id': 'lee',
        'title': 'Lisansüstü Eğitim Enstitüsü (LEE)',
        'category': 'Enstitü',
        'icon': 'fa-graduation-cap',
        'url_name': 'lee:lee',
        'description': 'Tezli ve tezsiz yüksek lisans ile doktora programları, enstitü başvuru tarihleri, mülakatlar ve mezuniyet şartları.',
        'keywords': ['enstitü', 'yüksek lisans', 'doktora', 'lisansüstü', 'tezli', 'tezsiz', 'master', 'lee'],
        'quick_links': []
    },

    # =========================================================================
    # 7. FAKÜLTELER
    # =========================================================================
    {
        'id': 'fakulteler_genel',
        'title': 'Tüm Fakülteler',
        'category': 'Fakülteler',
        'icon': 'fa-building-columns',
        'url_name': 'fakulteler:fakulteler',
        'description': 'Avrasya Üniversitesine bağlı 4 yıllık lisans eğitimi veren tüm fakülteler ve akademik birimler rehberi.',
        'keywords': ['fakülte', 'fakülteler', 'lisans', 'bölümler', 'akademik birimler'],
        'quick_links': []
    },
    {
        'id': 'muhendislik_mimarlik_fakultesi',
        'title': 'Mühendislik ve Mimarlık Fakültesi',
        'category': 'Fakülte',
        'icon': 'fa-compass-drafting',
        'url_name': 'muhendislik_mimarlik:muhendislik_mimarlik',
        'description': 'Bilgisayar, Elektrik-Elektronik, Makine, İnşaat, Harita, Gıda Mühendisliği ile Mimarlık ve İç Mimarlık bölümleri fakültesidir.',
        'keywords': ['mühendislik fakültesi', 'mimarlık fakültesi', 'muhendislik mimarlik'],
        'quick_links': []
    },
    {
        'id': 'fen_edebiyat_fakultesi',
        'title': 'İnsan ve Toplum Bilimleri Fakültesi',
        'category': 'Fakülte',
        'icon': 'fa-brain',
        'url_name': 'fen_edebiyat:fen_edebiyat',
        'description': 'Psikoloji, İngiliz Dili ve Edebiyatı, Türk Dili ve Edebiyatı, Moleküler Biyoloji ve Mütercim-Tercümanlık lisans programları fakültesidir.',
        'keywords': ['insan ve toplum bilimleri', 'fen edebiyat', 'edebiyat fakültesi', 'psikoloji fakültesi'],
        'quick_links': []
    },
    {
        'id': 'iktisadi_idari_fakultesi',
        'title': 'İktisadi ve İdari Bilimler Fakültesi',
        'category': 'Fakülte',
        'icon': 'fa-chart-pie',
        'url_name': 'iktisadi_idari:iktisadi_idari',
        'description': 'İşletme (Türkçe ve İngilizce), Siyaset Bilimi ve Kamu Yönetimi, Maliye ve Uluslararası İlişkiler bölümleri fakültesidir.',
        'keywords': ['iibf', 'iktisadi ve idari bilimler', 'işletme fakültesi', 'kamu yönetimi fakültesi'],
        'quick_links': []
    },
    {
        'id': 'saglik_bilimleri_fakultesi',
        'title': 'Sağlık Bilimleri Fakültesi',
        'category': 'Fakülte',
        'icon': 'fa-stethoscope',
        'url_name': 'saglik_bilimleri:saglik_bilimleri',
        'description': 'Hemşirelik, Beslenme ve Diyetetik, Fizyoterapi ve Rehabilitasyon, Ebelik, Ergoterapi, Çocuk Gelişimi, Odyoloji ve Sağlık Yönetimi fakültesidir.',
        'keywords': ['sağlık bilimleri fakültesi', 'hemşirelik fakültesi', 'beslenme fakültesi', 'fizyoterapi fakültesi'],
        'quick_links': []
    },
    {
        'id': 'spor_bilimleri_fakultesi',
        'title': 'Spor Bilimleri Fakültesi',
        'category': 'Fakülte',
        'icon': 'fa-dumbbell',
        'url_name': 'spor_bilimleri:spor_bilimleri',
        'description': 'Antrenörlük Eğitimi, Egzersiz ve Spor Bilimleri, Spor Yöneticiliği ve Rekreasyon 4 yıllık lisans programları fakültesidir.',
        'keywords': ['spor bilimleri fakültesi', 'besyo', 'beden eğitimi fakültesi', 'antrenörlük fakültesi'],
        'quick_links': []
    },
    {
        'id': 'iletisim_fakultesi',
        'title': 'İletişim Fakültesi',
        'category': 'Fakülte',
        'icon': 'fa-bullhorn',
        'url_name': 'iletisim:iletisim_anasayfa',
        'description': 'Görsel İletişim Tasarımı, Yeni Medya ve İletişim ile Halkla İlişkiler ve Reklamcılık bölümlerini kapsayan fakültemizdir.',
        'keywords': ['iletişim fakültesi', 'medya fakültesi', 'görsel iletişim', 'yeni medya'],
        'quick_links': []
    },

    # =========================================================================
    # 8. YÜKSEKOKULLAR & MYO ÜST BİRİMLERİ
    # =========================================================================
    {
        'id': 'yuksekokullari_genel',
        'title': 'Yüksekokullar',
        'category': 'Yüksekokul',
        'icon': 'fa-graduation-cap',
        'url_name': 'yuksekokullari:yuksekokullari',
        'description': 'Üniversitemizin 4 yıllık mesleki lisans eğitimi veren Uygulamalı Bilimler Yüksekokulu ve diğer birimlerimiz.',
        'keywords': ['yüksekokul', 'yüksekokullar', 'uygulamalı birimler'],
        'quick_links': []
    },
    {
        'id': 'uygulamali_bilimler',
        'title': 'Uygulamalı Bilimler Yüksekokulu',
        'category': 'Yüksekokul',
        'icon': 'fa-briefcase',
        'url_name': 'uygulamali_bilimler:uygulamali_bilimler',
        'description': 'Yönetim Bilişim Sistemleri (YBS) ile Gastronomi ve Mutfak Sanatları 4 yıllık lisans programlarını içeren yüksekokuldur.',
        'keywords': ['uygulamalı bilimler', 'uby', 'gastronomi', 'yönetim bilişim'],
        'quick_links': []
    },
    {
        'id': 'meslekyuksekokullari_genel',
        'title': 'Tüm Meslek Yüksekokulları (MYO)',
        'category': 'MYO',
        'icon': 'fa-screwdriver-wrench',
        'url_name': 'meslekyuksekokullari:meslekyuksekokullari',
        'description': '2 yıllık önlisans derecesi veren Meslek Yüksekokulu ile Sağlık Hizmetleri Meslek Yüksekokulu programları rehberi.',
        'keywords': ['myo', 'meslek yüksekokulu', 'meslek yüksekokulları', 'önlisans', '2 yıllık'],
        'quick_links': []
    },
    {
        'id': 'meslek_yuksekokulu_ust',
        'title': 'Meslek Yüksekokulu (Teknik & Sosyal)',
        'category': 'MYO',
        'icon': 'fa-laptop-code',
        'url_name': 'meslek_yuksekokulu:meslek_yuksekokulu',
        'description': 'Adalet, Bilgisayar Programcılığı, Aşçılık, Grafik Tasarımı, Harita Kadastro gibi teknik ve idari 2 yıllık önlisans programları.',
        'keywords': ['meslek yüksekokulu programları', 'teknik myo', 'sosyal myo'],
        'quick_links': []
    },
    {
        'id': 'saglik_hizmetleri_myo_ust',
        'title': 'Sağlık Hizmetleri Meslek Yüksekokulu (SHMYO)',
        'category': 'SHMYO',
        'icon': 'fa-heart-pulse',
        'url_name': 'saglik_hizmetleri_myo:saglik_hizmetleri_myo',
        'description': 'İlk ve Acil Yardım (Paramedik), Anestezi, Tıbbi Görüntüleme, Ağız ve Diş Sağlığı gibi sağlık teknikeri yetiştiren programlar.',
        'keywords': ['shmyo', 'sağlık hizmetleri myo', 'sağlık meslek yüksekokulu', 'paramedik', 'anestezi'],
        'quick_links': []
    },
    {
        'id': 'idari_birimler',
        'title': 'İdari Birimler',
        'category': 'İdari',
        'icon': 'fa-sitemap',
        'url_name': 'idari_birimler:idari_birimler',
        'description': 'Genel Sekreterlik, Personel, Bilgi İşlem, İdari ve Mali İşler, Yapı İşleri ve Yazı İşleri müdürlükleri.',
        'keywords': ['idari', 'idari birimler', 'personel', 'bilgi işlem', 'mali işler', 'genel sekreterlik'],
        'quick_links': []
    },

    # =========================================================================
    # 9. LİSANS BÖLÜMLERİ (MÜHENDİSLİK & MİMARLIK)
    # =========================================================================
    {
        'id': 'bilgisayar_muhendisligi',
        'title': 'Bilgisayar Mühendisliği Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-laptop-code',
        'url_name': 'bilgisayar_muhendisligi:liste',
        'description': 'Yazılım geliştirme, yapay zeka, veri tabanı, algoritma ve bilgisayar donanım sistemleri alanında 4 yıllık lisans mühendislik eğitimi.',
        'keywords': ['bilgisayar mühendisliği', 'bilgisayar mühendisi', 'yazılım mühendisliği', 'kodlama', 'yapay zeka', 'yazılım'],
        'quick_links': []
    },
    {
        'id': 'elektrik_elektronik_muhendisligi',
        'title': 'Elektrik-Elektronik Mühendisliği Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-microchip',
        'url_name': 'elektrik_elektronik_muhendisligi:liste',
        'description': 'Elektronik devreler, enerji sistemleri, haberleşme teknolojileri, sinyal işleme ve otomasyon mühendisliği lisans programı.',
        'keywords': ['elektrik elektronik', 'elektrik mühendisliği', 'elektronik mühendisliği', 'haberleşme', 'devre tasarımı'],
        'quick_links': []
    },
    {
        'id': 'insaat_muhendisligi',
        'title': 'İnşaat Mühendisliği Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-trowel-bricks',
        'url_name': 'insaat_muhendisligi:liste',
        'description': 'Yapı statiği, deprem mühendisliği, geoteknik, hidrolik ve şantiye proje yönetimi 4 yıllık lisans eğitimi.',
        'keywords': ['inşaat mühendisliği', 'inşaat mühendisi', 'yapı mühendisliği', 'şantiye'],
        'quick_links': []
    },
    {
        'id': 'makine_muhendisligi',
        'title': 'Makine Mühendisliği Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-gear',
        'url_name': 'makine_muhendisligi:liste',
        'description': 'Termodinamik, mekanik tasarım, CAD/CAM imalat sistemleri, otomotiv ve enerji teknolojileri mühendisliği lisans eğitimi.',
        'keywords': ['makine mühendisliği', 'makine mühendisi', 'termodinamik', 'mekanik tasarım'],
        'quick_links': []
    },
    {
        'id': 'mimarlik',
        'title': 'Mimarlık Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-building',
        'url_name': 'mimarlik:liste',
        'description': 'Mimari proje tasarımı, bina bilgisi, kentsel tasarım, restorasyon ve yapı teknolojileri 4 yıllık lisans programı.',
        'keywords': ['mimarlık', 'mimar', 'bina tasarımı', 'mimari çizim', 'proje'],
        'quick_links': []
    },
    {
        'id': 'ic_mimarlik',
        'title': 'İç Mimarlık ve Çevre Tasarımı',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-couch',
        'url_name': 'ic_mimarlik:liste',
        'description': 'İç mekan tasarımı, ergonomi, mobilya tasarımı, aydınlatma ve çevre düzenleme lisans eğitimi.',
        'keywords': ['iç mimarlık', 'iç mimar', 'çevre tasarımı', 'dekorasyon', 'mekan tasarımı'],
        'quick_links': []
    },
    {
        'id': 'harita_muhendisligi',
        'title': 'Harita Mühendisliği Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-map-location-dot',
        'url_name': 'harita_muhendisligi:liste',
        'description': 'Jeodezi, fotogrametri, coğrafi bilgi sistemleri (CBS), uydu konumlama (GPS) ve kadastro mühendisliği lisans eğitimi.',
        'keywords': ['harita mühendisliği', 'harita mühendisi', 'cbs', 'jeodezi', 'kadastro'],
        'quick_links': []
    },
    {
        'id': 'gida_muhendisligi',
        'title': 'Gıda Mühendisliği Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-wheat-awn',
        'url_name': 'gida_muhendisligi:liste',
        'description': 'Gıda güvenliği, gıda mikrobiyolojisi, gıda işleme teknolojileri ve kalite kontrol sistemleri lisans programı.',
        'keywords': ['gıda mühendisliği', 'gıda mühendisi', 'gıda güvenliği', 'gıda teknolojisi'],
        'quick_links': []
    },

    # =========================================================================
    # 10. LİSANS BÖLÜMLERİ (İNSAN VE TOPLUM BİLİMLERİ)
    # =========================================================================
    {
        'id': 'psikoloji',
        'title': 'Psikoloji Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-brain',
        'url_name': 'psikoloji:liste',
        'description': 'Klinik psikoloji, gelişim psikolojisi, sosyal psikoloji ve psikolojik testler alanında kapsamlı 4 yıllık lisans eğitimi.',
        'keywords': ['psikoloji', 'psikolog', 'ruh sağlığı', 'terapi', 'davranış bilimleri'],
        'quick_links': []
    },
    {
        'id': 'ingiliz_dili_edebiyati',
        'title': 'İngiliz Dili ve Edebiyatı Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-book',
        'url_name': 'ingiliz_dili_edebiyati:liste',
        'description': 'İngiliz edebiyatı, dilbilim, çeviri kuramları ve edebi eleştiri alanında 4 yıllık lisans programı.',
        'keywords': ['ingiliz dili', 'ingiliz edebiyatı', 'filoloji', 'dilbilim', 'english'],
        'quick_links': []
    },
    {
        'id': 'turk_dili_edebiyati',
        'title': 'Türk Dili ve Edebiyatı Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-book-open',
        'url_name': 'turk_dili_edebiyati:liste',
        'description': 'Eski ve yeni Türk edebiyatı, halk edebiyatı ve Türk dilbilimi alanında 4 yıllık lisans eğitimi.',
        'keywords': ['türk dili', 'türk edebiyatı', 'divan edebiyatı', 'türkçe', 'halk edebiyatı'],
        'quick_links': []
    },
    {
        'id': 'molekuler_biyoloji_genetik',
        'title': 'Moleküler Biyoloji ve Genetik',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-dna',
        'url_name': 'molekuler_biyoloji_genetik:liste',
        'description': 'Hücre biyolojisi, genetik tanı, DNA analizleri ve biyoteknoloji alanında modern laboratuvar destekli lisans eğitimi.',
        'keywords': ['moleküler biyoloji', 'genetik', 'dna', 'hücre', 'biyoteknoloji'],
        'quick_links': []
    },
    {
        'id': 'mutercim_tercumanlik',
        'title': 'Mütercim-Tercümanlık Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-language',
        'url_name': 'mutercim_tercumanlik:liste',
        'description': 'Simültane ve ardıl sözlü çeviri ile teknik ve edebi metin çevirmenliği alanında profesyonel 4 yıllık lisans eğitimi.',
        'keywords': ['mütercim', 'tercümanlık', 'çevirmenlik', 'simültane', 'çeviri'],
        'quick_links': []
    },

    # =========================================================================
    # 11. LİSANS BÖLÜMLERİ (İKTİSADİ VE İDARİ BİLİMLER)
    # =========================================================================
    {
        'id': 'isletme',
        'title': 'İşletme Bölümü (Türkçe)',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-briefcase',
        'url_name': 'isletme:liste',
        'description': 'Yönetim organizasyon, pazarlama, finansman, muhasebe ve insan kaynakları yönetimi 4 yıllık lisans eğitimi.',
        'keywords': ['işletme', 'yönetim', 'pazarlama', 'muhasebe', 'finans', 'şirket yönetimi'],
        'quick_links': []
    },
    {
        'id': 'isletme_ingilizce',
        'title': 'İşletme Bölümü (İngilizce)',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-globe',
        'url_name': 'isletme_ingilizce:liste',
        'description': 'Uluslararası standartlarda yüzde yüz İngilizce işletme, küresel pazarlama ve stratejik yönetim lisans eğitimi.',
        'keywords': ['business administration', 'ingilizce işletme', 'isletme ingilizce'],
        'quick_links': []
    },
    {
        'id': 'siyaset_bilimi',
        'title': 'Siyaset Bilimi ve Kamu Yönetimi',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-landmark',
        'url_name': 'siyaset_bilimi:liste',
        'description': 'Kamu politikaları, siyaset teorisi, yerel yönetimler, bürokrasi ve anayasa hukuku 4 yıllık lisans programı.',
        'keywords': ['siyaset bilimi', 'kamu yönetimi', 'kaymakamlık', 'belediye', 'politika'],
        'quick_links': []
    },
    {
        'id': 'maliye',
        'title': 'Maliye Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-coins',
        'url_name': 'maliye:liste',
        'description': 'Kamu maliyesi, vergi hukuku, bütçe denetimi, maliye teorisi ve vergi müfettişliği hazırlık lisans eğitimi.',
        'keywords': ['maliye', 'vergi', 'bütçe', 'mali hukuk', 'kamu harcamaları'],
        'quick_links': []
    },
    {
        'id': 'uluslararasi_iliskiler',
        'title': 'Uluslararası İlişkiler Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-handshake',
        'url_name': 'uluslararasi_iliskiler:liste',
        'description': 'Diplomasi tarihi, uluslararası hukuk, dış politika analizi, bölgesel çatışmalar ve küresel örgütler lisans eğitimi.',
        'keywords': ['uluslararası ilişkiler', 'diplomasi', 'dış politika', 'küresel siyaset', 'elçilik'],
        'quick_links': []
    },

    # =========================================================================
    # 12. LİSANS BÖLÜMLERİ (SAĞLIK BİLİMLERİ)
    # =========================================================================
    {
        'id': 'hemsirelik',
        'title': 'Hemşirelik Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-user-nurse',
        'url_name': 'hemsirelik:liste',
        'description': 'Dahiliye, cerrahi, çocuk ve halk sağlığı klinik hemşireliği alanında modern laboratuvar ve hastane stajlı 4 yıllık lisans eğitimi.',
        'keywords': ['hemşirelik', 'hemşire', 'sağlık', 'hasta bakımı', 'yoğun bakım'],
        'quick_links': []
    },
    {
        'id': 'beslenme_diyetetik',
        'title': 'Beslenme ve Diyetetik Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-apple-whole',
        'url_name': 'beslenme_diyetetik:liste',
        'description': 'Klinik diyetisyenlik, obezite tedavisi, sporcu beslenmesi ve toplu beslenme yönetimi 4 yıllık lisans eğitimi.',
        'keywords': ['beslenme', 'diyetetik', 'diyetisyen', 'sağlıklı beslenme', 'kilo kontrolü'],
        'quick_links': []
    },
    {
        'id': 'fizyoterapi_rehabilitasyon',
        'title': 'Fizyoterapi ve Rehabilitasyon (Lisans)',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-person-walking',
        'url_name': 'fizyoterapi_rehabilitasyon:liste',
        'description': 'Ortopedik, nörolojik ve sporcu rehabilitasyonu alanında uzman fizyoterapist yetiştiren 4 yıllık lisans programı.',
        'keywords': ['fizyoterapi', 'rehabilitasyon', 'fizyoterapist', 'fizik tedavi'],
        'quick_links': []
    },
    {
        'id': 'ebelik',
        'title': 'Ebelik Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-baby',
        'url_name': 'ebelik:liste',
        'description': 'Gebelikte takip, doğum öncesi ve sonrası anne-bebek bakımı alanında yetkin ebeler yetiştiren 4 yıllık lisans eğitimi.',
        'keywords': ['ebelik', 'ebe', 'doğum', 'anne bebek sağlığı'],
        'quick_links': []
    },
    {
        'id': 'ergoterapi',
        'title': 'Ergoterapi Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-hands-holding-circle',
        'url_name': 'ergoterapi:liste',
        'description': 'Fiziksel veya duyusal engelleri olan bireylerin günlük yaşam becerilerini geliştiren ergoterapistlik lisans programı.',
        'keywords': ['ergoterapi', 'ergoterapist', 'duyu bütünleme', 'günlük yaşam becerileri'],
        'quick_links': []
    },
    {
        'id': 'cocuk_gelisimi_lisans',
        'title': 'Çocuk Gelişimi Bölümü (Lisans)',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-children',
        'url_name': 'cocuk_gelisimi:liste',
        'description': '0-18 yaş arası normal ve özel gereksinimli çocukların gelişim takibi, aile danışmanlığı ve çocuk pedagojisi 4 yıllık eğitimi.',
        'keywords': ['çocuk gelişimi', 'pedagoji', 'çocuk gelişimi lisans', 'özel eğitim'],
        'quick_links': []
    },
    {
        'id': 'odyoloji',
        'title': 'Odyoloji Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-ear-listen',
        'url_name': 'odyoloji:liste',
        'description': 'İşitme ve denge sistemi bozukluklarının tespiti, işitme cihazı uyarlaması ve işitme rehabilitasyonu lisans programı.',
        'keywords': ['odyoloji', 'odyolog', 'işitme testi', 'kulak', 'işitme cihazı'],
        'quick_links': []
    },
    {
        'id': 'saglik_yonetimi',
        'title': 'Sağlık Yönetimi Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-hospital-user',
        'url_name': 'saglik_yonetimi:liste',
        'description': 'Hastane yöneticiliği, sağlık kurumlarında insan kaynakları, sağlık ekonomisi ve kalite standartları lisans eğitimi.',
        'keywords': ['sağlık yönetimi', 'hastane yöneticiliği', 'sağlık idaresi'],
        'quick_links': []
    },
    {
        'id': 'sosyal_hizmet',
        'title': 'Sosyal Hizmet Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-hand-holding-heart',
        'url_name': 'sosyal_hizmet:liste',
        'description': 'Dezavantajlı bireyler, aile, çocuk ve yaşlı refahı alanında sosyal hizmet uzmanı yetiştiren 4 yıllık lisans eğitimi.',
        'keywords': ['sosyal hizmet', 'sosyal hizmet uzmanı', 'sosyal yardım', 'rehberlik'],
        'quick_links': []
    },

    # =========================================================================
    # 13. LİSANS BÖLÜMLERİ (SPOR, İLETİŞİM, UYGULAMALI BİLİMLER)
    # =========================================================================
    {
        'id': 'antrenorluk_egitimi',
        'title': 'Antrenörlük Eğitimi Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-stopwatch',
        'url_name': 'antrenorluk_egitimi:liste',
        'description': 'Futbol, basketbol, yüzme ve bireysel spor dallarında lisanslı antrenör ve kondisyoner yetiştiren 4 yıllık eğitim.',
        'keywords': ['antrenörlük', 'antrenör', 'teknik direktör', 'kondisyoner', 'spor koçu'],
        'quick_links': []
    },
    {
        'id': 'egzersiz_spor_bilimleri',
        'title': 'Egzersiz ve Spor Bilimleri',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-heart-pulse',
        'url_name': 'egzersiz:liste',
        'description': 'Egzersiz fizyolojisi, hareket bilimi, biyomekanik ve sağlıklı yaşam egzersiz liderliği lisans programı.',
        'keywords': ['egzersiz', 'spor bilimleri', 'hareket bilimi', 'fitness'],
        'quick_links': []
    },
    {
        'id': 'spor_yoneticiligi',
        'title': 'Spor Yöneticiliği Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-trophy',
        'url_name': 'spor_yoneticiligi:liste',
        'description': 'Spor kulüpleri yönetimi, spor hukuku, spor pazarlaması ve spor tesisleri işletmeciliği lisans eğitimi.',
        'keywords': ['spor yöneticiliği', 'spor yöneticisi', 'kulüp yönetimi'],
        'quick_links': []
    },
    {
        'id': 'rekreasyon',
        'title': 'Rekreasyon Bölümü',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-campground',
        'url_name': 'rekreasyon:liste',
        'description': 'Boş zaman etkinlikleri yönetimi, açık alan sporları, animasyon ve doğa rekreasyonu lisans programı.',
        'keywords': ['rekreasyon', 'boş zaman yönetimi', 'animasyon', 'açık alan sporları'],
        'quick_links': []
    },
    {
        'id': 'gorsel_iletisim_tasarimi',
        'title': 'Görsel İletişim Tasarımı',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-pen-nib',
        'url_name': 'gorsel_iletisim_tasarimi:liste',
        'description': 'Grafik tasarım, dijital illüstrasyon, animasyon, video kurgu ve arayüz tasarımı (UI/UX) lisans eğitimi.',
        'keywords': ['görsel iletişim', 'grafik tasarım lisans', 'animasyon', 'ui ux', 'dijital tasarım'],
        'quick_links': []
    },
    {
        'id': 'yeni_medya_iletisim',
        'title': 'Yeni Medya ve İletişim',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-mobile-screen-button',
        'url_name': 'yeni_medya_iletisim:liste',
        'description': 'Dijital gazetecilik, sosyal medya stratejisi, dijital yayıncılık ve veri haberciliği 4 yıllık lisans programı.',
        'keywords': ['yeni medya', 'dijital gazetecilik', 'sosyal medya yönetimi', 'içerik üreticiliği'],
        'quick_links': []
    },
    {
        'id': 'yonetim_bilisim_sistemleri',
        'title': 'Yönetim Bilişim Sistemleri (YBS)',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-chart-simple',
        'url_name': 'yonetim_bilisim:liste',
        'description': 'İşletme süreçleri ile bilgi teknolojilerinin kesişimi; veri analitiği, ERP ve yazılım yönetimi 4 yıllık lisans eğitimi.',
        'keywords': ['yönetim bilişim sistemleri', 'ybs', 'mis', 'veri analitiği', 'erp', 'iş analisti'],
        'quick_links': []
    },
    {
        'id': 'gastronomi_mutfak',
        'title': 'Gastronomi ve Mutfak Sanatları',
        'category': 'Bölüm (Lisans)',
        'icon': 'fa-utensils',
        'url_name': 'gastronomi:liste',
        'description': 'Dünya mutfakları, Türk mutfak kültürü, profesyonel aşçılık ve restoran işletmeciliği 4 yıllık lisans eğitimi.',
        'keywords': ['gastronomi', 'mutfak sanatları', 'şef', 'aşçı lisans', 'restoran yönetimi'],
        'quick_links': []
    },

    # =========================================================================
    # 14. MESLEK YÜKSEKOKULU (MYO) 2 YILLIK ÖNLİSANS PROGRAMLARI
    # =========================================================================
    {
        'id': 'adalet',
        'title': 'Adalet Programı',
        'category': 'Program (MYO)',
        'icon': 'fa-scale-balanced',
        'url_name': 'adalet:liste',
        'description': 'Hukuk büroları, adliyeler, cezaevleri ve noterliklerde görev alacak nitelikli zabıt katibi ve adalet ara elemanı yetiştiren 2 yıllık önlisans programıdır.',
        'keywords': ['adalet', 'adalet programı', 'zabıt katibi', 'adliye', 'mahkeme', 'hukuk önlisans', 'icra memuru'],
        'quick_links': []
    },
    {
        'id': 'ascilik',
        'title': 'Aşçılık Programı',
        'category': 'Program (MYO)',
        'icon': 'fa-kitchen-set',
        'url_name': 'ascilik:liste',
        'description': 'Sıcak ve soğuk mutfak, pastacılık teknikleri, hijyen ve ziyafet yönetimi alanında profesyonel şef yardımcısı yetiştiren programdır.',
        'keywords': ['aşçılık', 'aşçılık programı', 'mutfak', 'pastacılık', 'şef', 'yemek pişirme'],
        'quick_links': []
    },
    {
        'id': 'bilgisayar_programciligi',
        'title': 'Bilgisayar Programcılığı',
        'category': 'Program (MYO)',
        'icon': 'fa-code',
        'url_name': 'bilgisayar_programciligi:liste',
        'description': 'Web tasarımı, mobil uygulama, veri tabanı ve yazılım geliştirme alanında sektöre doğrudan ara eleman yetiştiren 2 yıllık programdır.',
        'keywords': ['bilgisayar programcılığı', 'kodlama myo', 'yazılımcı', 'web geliştirici'],
        'quick_links': []
    },
    {
        'id': 'bilisim_guvenligi',
        'title': 'Bilişim Güvenliği Teknolojisi',
        'category': 'Program (MYO)',
        'icon': 'fa-shield-halved',
        'url_name': 'bilisim_guvenligi:liste',
        'description': 'Siber saldırı savunması, ağ güvenliği, sızma testleri ve veri güvenliği alanında teknik personel yetiştiren programdır.',
        'keywords': ['bilişim güvenliği', 'siber güvenlik', 'ağ güvenliği', 'hacker', 'veri koruma'],
        'quick_links': []
    },
    {
        'id': 'dis_ticaret',
        'title': 'Dış Ticaret Programı',
        'category': 'Program (MYO)',
        'icon': 'fa-ship',
        'url_name': 'dis_ticaret:liste',
        'description': 'İthalat, ihracat mevzuatı, gümrük işlemleri ve uluslararası lojistik süreçlerinde görev alacak uzman tekniker eğitimi.',
        'keywords': ['dış ticaret', 'ithalat', 'ihracat', 'gümrük', 'uluslararası ticaret'],
        'quick_links': []
    },
    {
        'id': 'e_ticaret',
        'title': 'E-Ticaret ve Pazarlama',
        'category': 'Program (MYO)',
        'icon': 'fa-cart-shopping',
        'url_name': 'e_ticaret:liste',
        'description': 'Online mağaza yönetimi, dijital pazarlama, SEO ve sosyal medya reklamcılığı alanında 2 yıllık önlisans eğitimi.',
        'keywords': ['e-ticaret', 'eticaret', 'pazarlama', 'dijital pazar', 'online satış'],
        'quick_links': []
    },
    {
        'id': 'grafik_tasarimi',
        'title': 'Grafik Tasarımı Programı',
        'category': 'Program (MYO)',
        'icon': 'fa-palette',
        'url_name': 'grafik_tasarimi:liste',
        'description': 'Photoshop, Illustrator, kurumsal kimlik tasarımı ve matbaa hazırlık teknikeri yetiştiren 2 yıllık önlisans programıdır.',
        'keywords': ['grafik tasarımı', 'grafik tasarım', 'grafiker', 'logo', 'illüstrasyon'],
        'quick_links': []
    },
    {
        'id': 'halkla_iliskiler',
        'title': 'Halkla İlişkiler ve Tanıtım',
        'category': 'Program (MYO)',
        'icon': 'fa-comments',
        'url_name': 'halkla_iliskiler:liste',
        'description': 'Kurumsal imaj yönetimi, basın bülteni hazırlığı ve halkla ilişkiler etkinlik koordinasyonu eğitimi.',
        'keywords': ['halkla ilişkiler', 'tanıtım', 'kurumsal iletişim önlisans'],
        'quick_links': []
    },
    {
        'id': 'harita_kadastro',
        'title': 'Harita ve Kadastro',
        'category': 'Program (MYO)',
        'icon': 'fa-map-pin',
        'url_name': 'harita_kadastro:liste',
        'description': 'Arazi ölçüm aletleri kullanımı (Total Station, GPS), parselasyon ve kadastro teknikeri yetiştiren önlisans eğitimi.',
        'keywords': ['harita ve kadastro', 'kadastro teknikeri', 'topoğrafya', 'arazi ölçümü'],
        'quick_links': []
    },
    {
        'id': 'ic_mekan',
        'title': 'İç Mekan Tasarımı',
        'category': 'Program (MYO)',
        'icon': 'fa-table-cells',
        'url_name': 'ic_mekan:liste',
        'description': 'Autocad, 3ds Max çizimleri, mobilya detay projeleri ve iç mimarlık ofis teknikeri yetiştiren 2 yıllık eğitim.',
        'keywords': ['iç mekan tasarımı', 'iç mekan', 'dekorasyon myo', 'teknik çizim'],
        'quick_links': []
    },
    {
        'id': 'insaat_teknolojisi',
        'title': 'İnşaat Teknolojisi',
        'category': 'Program (MYO)',
        'icon': 'fa-helmet-safety',
        'url_name': 'insaat_teknolojisi:liste',
        'description': 'Şantiye teknikeri, metraj hesaplama, hakediş ve beton laboratuvar testleri alanında önlisans eğitimi.',
        'keywords': ['inşaat teknolojisi', 'inşaat teknikeri', 'şantiye teknikeri'],
        'quick_links': []
    },
    {
        'id': 'lojistik_programi',
        'title': 'Lojistik Programı',
        'category': 'Program (MYO)',
        'icon': 'fa-truck-fast',
        'url_name': 'lojistik_programi:liste',
        'description': 'Tedarik zinciri, depo yönetimi, uluslararası taşımacılık ve kargo operasyonları uzman teknikerliği eğitimi.',
        'keywords': ['lojistik', 'tedarik zinciri', 'taşımacılık', 'depolama', 'kargo'],
        'quick_links': []
    },
    {
        'id': 'mimari_restorasyon',
        'title': 'Mimari Restorasyon',
        'category': 'Program (MYO)',
        'icon': 'fa-monument',
        'url_name': 'mimari_restorasyon:liste',
        'description': 'Tarihi binaların rölöve, restitüsyon ve restorasyon projelerinde görev alacak koruma teknikeri eğitimi.',
        'keywords': ['mimari restorasyon', 'restorasyon', 'tarihi eser', 'rölöve', 'koruma'],
        'quick_links': []
    },
    {
        'id': 'mahkeme_buro',
        'title': 'Mahkeme Büro Hizmetleri',
        'category': 'Program (MYO)',
        'icon': 'fa-file-lines',
        'url_name': 'mahkeme_buro:liste',
        'description': 'Adli yargı ve idari yargı kalemlerinde dosyalama, UYAP kullanımı ve duruşma zabıt işlemleri eğitimi.',
        'keywords': ['mahkeme büro', 'mahkeme büro hizmetleri', 'adliye kalemi', 'uyap'],
        'quick_links': []
    },
    {
        'id': 'moda_tasarimi',
        'title': 'Moda Tasarımı Programı',
        'category': 'Program (MYO)',
        'icon': 'fa-shirt',
        'url_name': 'moda_tasarimi:liste',
        'description': 'Kalıp çıkarma, dikiş atölyesi, kumaş bilgisi ve hazır giyim koleksiyon hazırlığı 2 yıllık eğitimi.',
        'keywords': ['moda tasarımı', 'moda', 'stilist', 'modelist', 'tekstil'],
        'quick_links': []
    },
    {
        'id': 'otomotiv',
        'title': 'Otomotiv Teknolojisi',
        'category': 'Program (MYO)',
        'icon': 'fa-car',
        'url_name': 'otomotiv:liste',
        'description': 'İçten yanmalı motorlar, hibrit ve elektrikli araç teknolojileri ve oto arıza teşhis teknikeri eğitimi.',
        'keywords': ['otomotiv', 'otomotiv teknolojisi', 'motor', 'araç servisi', 'oto tamir'],
        'quick_links': []
    },
    {
        'id': 'sivil_havacilik',
        'title': 'Sivil Havacılık Kabin Hizmetleri',
        'category': 'Program (MYO)',
        'icon': 'fa-plane-departure',
        'url_name': 'sivil_havacilik:liste',
        'description': 'Uçak içi emniyet kuralları, kabin memurluğu (hostes/host) ve yolcu ilişkileri 2 yıllık önlisans eğitimi.',
        'keywords': ['sivil havacılık', 'kabin memuru', 'hostes', 'host', 'uçuş', 'havacılık'],
        'quick_links': []
    },
    {
        'id': 'sosyal_guvenlik',
        'title': 'Sosyal Güvenlik Programı',
        'category': 'Program (MYO)',
        'icon': 'fa-file-invoice-dollar',
        'url_name': 'sosyal_guvenlik:liste',
        'description': 'SGK mevzuatı, iş hukuku, bordrolama ve çalışan özlük işleri teknikeri yetiştiren 2 yıllık eğitim.',
        'keywords': ['sosyal güvenlik', 'sgk', 'bordro', 'özlük işleri', 'iş hukuku'],
        'quick_links': []
    },
    {
        'id': 'sosyal_hizmetler_myo',
        'title': 'Sosyal Hizmetler (Önlisans)',
        'category': 'Program (MYO)',
        'icon': 'fa-hands-holding-child',
        'url_name': 'sosyal_hizmetler:liste',
        'description': 'Huzurevleri, çocuk esirgeme ve engelli bakım merkezlerinde görev alacak sosyal hizmet teknisyeni eğitimi.',
        'keywords': ['sosyal hizmetler', 'sosyal hizmetler önlisans', 'bakım teknikeri'],
        'quick_links': []
    },
    {
        'id': 'spor_yonetimi_myo',
        'title': 'Spor Yönetimi (Önlisans)',
        'category': 'Program (MYO)',
        'icon': 'fa-medal',
        'url_name': 'spor_yonetimi:liste',
        'description': 'Spor salonları, fitness merkezleri ve belediye spor tesisleri işletmeciliği ara elemanı eğitimi.',
        'keywords': ['spor yönetimi önlisans', 'spor tesisi işletmeciliği'],
        'quick_links': []
    },
    {
        'id': 'web_tasarimi',
        'title': 'Web Tasarımı ve Kodlama',
        'category': 'Program (MYO)',
        'icon': 'fa-window-maximize',
        'url_name': 'web_tasarimi:liste',
        'description': 'HTML, CSS, JavaScript, responsive web tasarımı ve içerik yönetim sistemleri (CMS) önlisans eğitimi.',
        'keywords': ['web tasarımı', 'web tasarım', 'web kodlama', 'frontend', 'html css'],
        'quick_links': []
    },

    # =========================================================================
    # 15. SAĞLIK HİZMETLERİ MYO (SHMYO) 2 YILLIK ÖNLİSANS PROGRAMLARI
    # =========================================================================
    {
        'id': 'ilk_acil_yardim',
        'title': 'İlk ve Acil Yardım (Paramedik)',
        'category': 'Program (SHMYO)',
        'icon': 'fa-truck-medical',
        'url_name': 'ilk_acil_yardim:liste',
        'description': '112 acil ambulans ekiplerinde hayat kurtarıcı müdahale yapan nitelikli paramedik teknikerleri yetiştirir.',
        'keywords': ['ilk ve acil yardım', 'paramedik', '112', 'acil tıp teknisyeni', 'ambulans'],
        'quick_links': []
    },
    {
        'id': 'anestezi',
        'title': 'Anestezi Programı',
        'category': 'Program (SHMYO)',
        'icon': 'fa-syringe',
        'url_name': 'anestezi:liste',
        'description': 'Ameliyat öncesi, sırası ve sonrasında anestezi uzmanı hekime yardımcı olan anestezi teknikeri yetiştirir.',
        'keywords': ['anestezi', 'anestezi teknikeri', 'narkoz', 'ameliyat'],
        'quick_links': []
    },
    {
        'id': 'ameliyathane',
        'title': 'Ameliyathane Hizmetleri',
        'category': 'Program (SHMYO)',
        'icon': 'fa-scissors',
        'url_name': 'ameliyathane:liste',
        'description': 'Cerrahi operasyon öncesinde ameliyat masasını ve aletleri steril olarak hazırlayan cerrahi tekniker eğitimi.',
        'keywords': ['ameliyathane', 'ameliyathane hizmetleri', 'cerrahi tekniker', 'sterilizasyon'],
        'quick_links': []
    },
    {
        'id': 'agiz_dis',
        'title': 'Ağız ve Diş Sağlığı',
        'category': 'Program (SHMYO)',
        'icon': 'fa-tooth',
        'url_name': 'agiz_dis:liste',
        'description': 'Diş hekimliği kliniklerinde hekim asistanlığı ve klinik hijyeni yürüten diş sağlığı teknikeri eğitimi.',
        'keywords': ['ağız ve diş sağlığı', 'diş hekimi asistanı', 'diş teknikeri', 'diş sağlığı'],
        'quick_links': []
    },
    {
        'id': 'dis_protezi',
        'title': 'Diş Protez Teknolojisi',
        'category': 'Program (SHMYO)',
        'icon': 'fa-teeth',
        'url_name': 'dis_protezi:liste',
        'description': 'Laboratuvar ortamında sabit ve hareketli diş protezleri, porselen ve implant üstü protez üretimi eğitimi.',
        'keywords': ['diş protez', 'diş protezi', 'protez teknikeri', 'porselen diş'],
        'quick_links': []
    },
    {
        'id': 'diyaliz',
        'title': 'Diyaliz Programı',
        'category': 'Program (SHMYO)',
        'icon': 'fa-droplet',
        'url_name': 'diyaliz:liste',
        'description': 'Kronik böbrek yetmezliği hastalarına hemodiyaliz cihazını bağlayan ve takip eden diyaliz teknikeri eğitimi.',
        'keywords': ['diyaliz', 'diyaliz teknikeri', 'hemodiyaliz', 'böbrek hastası'],
        'quick_links': []
    },
    {
        'id': 'eczane',
        'title': 'Eczane Hizmetleri',
        'category': 'Program (SHMYO)',
        'icon': 'fa-pills',
        'url_name': 'eczane:liste',
        'description': 'Eczanelerde ve hastane eczane depolarında ilaç hazırlama ve reçete takibi yapan eczane teknikeri eğitimi.',
        'keywords': ['eczane', 'eczane hizmetleri', 'eczane teknikeri', 'ilaç', 'reçete'],
        'quick_links': []
    },
    {
        'id': 'elektronorofizyoloji',
        'title': 'Elektronörofizyoloji Programı',
        'category': 'Program (SHMYO)',
        'icon': 'fa-bolt',
        'url_name': 'elektronorofizyoloji:liste',
        'description': 'Beyin dalgaları (EEG), kas aktivitesi (EMG) ve uyku testlerini uygulayan nöroloji teknikeri eğitimi.',
        'keywords': ['elektronörofizyoloji', 'eeg', 'emg', 'uyku laboratuvarı', 'nöroloji teknikeri'],
        'quick_links': []
    },
    {
        'id': 'fizyoterapi_myo',
        'title': 'Fizyoterapi (Önlisans)',
        'category': 'Program (SHMYO)',
        'icon': 'fa-wheelchair',
        'url_name': 'fizyoterapi:liste',
        'description': 'Fizik tedavi kliniklerinde uzman fizyoterapist gözetiminde elektroterapi ve egzersiz uygulayan tekniker eğitimi.',
        'keywords': ['fizyoterapi önlisans', 'fizik tedavi teknikeri', 'elektroterapi'],
        'quick_links': []
    },
    {
        'id': 'cocuk_gelisimi_myo',
        'title': 'Çocuk Gelişimi (Önlisans)',
        'category': 'Program (SHMYO)',
        'icon': 'fa-shapes',
        'url_name': 'cocuk_gelisimi_programi:liste',
        'description': 'Kreş, gündüz bakımevi ve anaokullarında çocuk bakım ve eğitimine destek veren 2 yıllık önlisans programıdır.',
        'keywords': ['çocuk gelişimi önlisans', 'kreş öğretmeni', 'çocuk bakımı'],
        'quick_links': []
    },
    {
        'id': 'is_sagligi_guvenligi',
        'title': 'İş Sağlığı ve Güvenliği',
        'category': 'Program (SHMYO)',
        'icon': 'fa-hard-hat',
        'url_name': 'is_sagligi_guvenligi:liste',
        'description': 'İşyerlerinde risk analizi, iş kazalarını önleme tedbirleri ve C sınıfı iş güvenliği uzman yardımcılığı eğitimi.',
        'keywords': ['iş sağlığı ve güvenliği', 'isg', 'iş güvenliği teknikeri', 'iş kazası önleme'],
        'quick_links': []
    },
    {
        'id': 'is_ugrasi_terapisi',
        'title': 'İş ve Uğraşı Terapisi (Önlisans)',
        'category': 'Program (SHMYO)',
        'icon': 'fa-hands',
        'url_name': 'is_ugrasi_terapisi:liste',
        'description': 'Rehabilitasyon merkezlerinde hastaların el-kol fonksiyonlarını geri kazandıran mesleki uğraşı teknikeri eğitimi.',
        'keywords': ['iş ve uğraşı terapisi', 'ergoterapi teknikeri', 'uğraşı terapisi'],
        'quick_links': []
    },
    {
        'id': 'odyometri',
        'title': 'Odyometri Programı',
        'category': 'Program (SHMYO)',
        'icon': 'fa-headphones',
        'url_name': 'odyometri:liste',
        'description': 'İşitme testleri (odyogram) uygulayan ve KBB kliniklerinde işitme cihazı uyarlayan odyometri teknikeri eğitimi.',
        'keywords': ['odyometri', 'odyometri teknikeri', 'işitme testi', 'odyogram'],
        'quick_links': []
    },
    {
        'id': 'optisyenlik',
        'title': 'Optisyenlik Programı',
        'category': 'Program (SHMYO)',
        'icon': 'fa-glasses',
        'url_name': 'optisyenlik:liste',
        'description': 'Göz hekimi reçetesine göre gözlük camı odaklayan, çerçeve montajı yapan ve optisyenlik müessesesi açma yetkili eğitim.',
        'keywords': ['optisyenlik', 'optisyen', 'gözlük', 'gözlükçü', 'lens'],
        'quick_links': []
    },
    {
        'id': 'ortopedik_protez',
        'title': 'Ortopedik Protez ve Ortez',
        'category': 'Program (SHMYO)',
        'icon': 'fa-crutch',
        'url_name': 'ortopedik_protez:liste',
        'description': 'Uzuv kaybı yaşayan hastalar için yapay el-bacak protezleri ve ortopedik cihazlar üreten tekniker eğitimi.',
        'keywords': ['ortopedik protez', 'ortez', 'yapay bacak', 'protez bacak', 'medikal cihaz'],
        'quick_links': []
    },
    {
        'id': 'patoloji_laboratuar',
        'title': 'Patoloji Laboratuvar Teknikleri',
        'category': 'Program (SHMYO)',
        'icon': 'fa-microscope',
        'url_name': 'patoloji_laboratuar:liste',
        'description': 'Ameliyatla alınan doku örneklerinin mikroskop altında incelenmesi için biyopsi kesiti hazırlayan laboratuvar teknikeri eğitimi.',
        'keywords': ['patoloji', 'patoloji laboratuvarı', 'biyopsi', 'doku takibi'],
        'quick_links': []
    },
    {
        'id': 'radyoterapi',
        'title': 'Radyoterapi Programı',
        'category': 'Program (SHMYO)',
        'icon': 'fa-radiation',
        'url_name': 'radyoterapi:liste',
        'description': 'Kanser hastalarının tedavisinde kullanılan lineer hızlandırıcı radyasyon cihazlarını kullanan onkoloji teknikeri eğitimi.',
        'keywords': ['radyoterapi', 'ışın tedavisi', 'kanser tedavisi', 'radyasyon teknikeri'],
        'quick_links': []
    },
    {
        'id': 'saglik_kurumlari',
        'title': 'Sağlık Kurumları İşletmeciliği',
        'category': 'Program (SHMYO)',
        'icon': 'fa-hospital',
        'url_name': 'saglik_kurumlari:liste',
        'description': 'Hastanelerin hasta kabul, faturalandırma, medikal muhasebe ve hasta hakları birimlerinde görev yapan önlisans programıdır.',
        'keywords': ['sağlık kurumları', 'hasta kabul', 'tıbbi sekreterlik', 'hastane muhasebesi'],
        'quick_links': []
    },
    {
        'id': 'tibbi_goruntuleme',
        'title': 'Tıbbi Görüntüleme Teknikleri (Radyoloji)',
        'category': 'Program (SHMYO)',
        'icon': 'fa-x-ray',
        'url_name': 'tibbi_goruntuleme:liste',
        'description': 'Röntgen, Bilgisayarlı Tomografi (BT), Manyetik Rezonans (MR) ve Mamografi çekimi yapan radyoloji teknikeri eğitimi.',
        'keywords': ['tıbbi görüntüleme', 'radyoloji', 'röntgen', 'tomografi', 'mr', 'emare'],
        'quick_links': []
    },
    {
        'id': 'tibbi_laboratuvar',
        'title': 'Tıbbi Laboratuvar Teknikleri',
        'category': 'Program (SHMYO)',
        'icon': 'fa-vial',
        'url_name': 'tibbi_laboratuvar:liste',
        'description': 'Biyokimya, mikrobiyoloji ve hematoloji laboratuvarlarında kan ve idrar tahlillerini gerçekleştiren tahlil teknikeri eğitimi.',
        'keywords': ['tıbbi laboratuvar', 'kan tahlili', 'biyokimya', 'tahlil teknikeri', 'laborant'],
        'quick_links': []
    },
    {
        'id': 'acil_durum',
        'title': 'Acil Durum ve Afet Yönetimi',
        'category': 'Program (SHMYO)',
        'icon': 'fa-shield-heart',
        'url_name': 'acil_durum:liste',
        'description': 'Deprem, sel, yangın gibi afetlerde arama-kurtarma ve kriz koordinasyonu sağlayan AFAD ve acil durum teknikeri eğitimi.',
        'keywords': ['acil durum', 'afet yönetimi', 'arama kurtarma', 'afad', 'kriz yönetimi', 'yangın'],
        'quick_links': []
    }
]

_CACHED_RESOLVED_DIRECTORY = None

def normalize_text(text):
    """Metni Türkçe ve küçük harfe normalize eder."""
    if not text:
        return ""
    text = str(text).lower()
    # Türkçe özel karakter eşleştirmeleri
    replacements = {
        'ı': 'i', 'İ': 'i', 'I': 'i',
        'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u',
        'ş': 's', 'Ş': 's',
        'ö': 'o', 'Ö': 'o',
        'ç': 'c', 'Ç': 'c'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def get_voice_directory(force_reload=False):
    """Tüm konuların URL'lerini reverse ederek hazır dizin listesi döner."""
    global _CACHED_RESOLVED_DIRECTORY
    if _CACHED_RESOLVED_DIRECTORY and not force_reload:
        return _CACHED_RESOLVED_DIRECTORY

    resolved_list = []
    for item in TOPICS_DEFINITIONS:
        try:
            url = reverse(item['url_name'])
        except Exception:
            url = '/'

        # Quick links URL'lerini de çözümle
        resolved_quick = []
        for ql in item.get('quick_links', []):
            q_url = ql.get('url')
            if not q_url and ql.get('url_name'):
                try:
                    q_url = reverse(ql['url_name'])
                except Exception:
                    q_url = '#'
            resolved_quick.append({
                'title': ql.get('title', ''),
                'url': q_url or '#'
            })

        topic_entry = {
            'id': item['id'],
            'title': item['title'],
            'category': item['category'],
            'icon': item['icon'],
            'url': url,
            'description': item['description'],
            'keywords': item['keywords'],
            'quick_links': resolved_quick,
            # Normalleştirilmiş arama metinleri
            '_norm_title': normalize_text(item['title']),
            '_norm_cat': normalize_text(item['category']),
            '_norm_keywords': [normalize_text(kw) for kw in item['keywords']],
            '_norm_desc': normalize_text(item['description'])
        }
        resolved_list.append(topic_entry)

    _CACHED_RESOLVED_DIRECTORY = resolved_list
    return _CACHED_RESOLVED_DIRECTORY


def search_voice_topics(query_text, max_results=8):
    """
    Kullanıcının söylediği veya yazdığı metne göre konuları akıllıca filtreler ve sıralar.
    Ayrıca veritabanındaki güncel haber ve duyuruları da sorgular.
    """
    if not query_text or not query_text.strip():
        return []

    norm_query = normalize_text(query_text)
    query_tokens = [t for t in norm_query.split() if len(t) > 1]
    
    directory = get_voice_directory()
    scored_results = []

    for item in directory:
        score = 0
        norm_title = item['_norm_title']
        norm_desc = item['_norm_desc']
        norm_keywords = item['_norm_keywords']
        norm_cat = item['_norm_cat']

        # 1. Tam Eşleşme
        if norm_query == norm_title:
            score += 150
        elif norm_query in norm_title:
            score += 80

        # 2. Anahtar Kelime Tam ve Kısmi Eşleşmesi
        for kw in norm_keywords:
            if norm_query == kw:
                score += 120
                break
            elif norm_query in kw or kw in norm_query:
                score += 50
                break

        # 3. Kategori Eşleşmesi
        if norm_query == norm_cat or norm_query in norm_cat:
            score += 40

        # 4. Token / Kelime bazlı puanlama
        for token in query_tokens:
            if token in norm_title:
                score += 30
            for kw in norm_keywords:
                if token in kw:
                    score += 20
            if token in norm_desc:
                score += 10
            if token in norm_cat:
                score += 15

        if score > 0:
            scored_results.append((score, {
                'id': item['id'],
                'title': item['title'],
                'category': item['category'],
                'icon': item['icon'],
                'url': item['url'],
                'description': item['description'],
                'quick_links': item['quick_links'],
                'source': 'app'
            }))

    # Puanına göre sırala
    scored_results.sort(key=lambda x: x[0], reverse=True)
    results = [item for score, item in scored_results[:max_results]]

    # Canlı Veritabanı Araması (Haber, Duyuru, Kalite)
    try:
        live_results = search_live_content(query_text, limit=3)
        results.extend(live_results)
    except Exception as e:
        pass

    return results


def search_live_content(query_text, limit=3):
    """Haber, Duyuru ve Kalite tablolarından canlı arama yapar."""
    from django.db.models import Q
    live_items = []
    
    # 1. Kalite Duyuruları ve Haberleri
    try:
        from kalite_akreditasyon.models import News as KaliteNews, Announcement as KaliteAnn
        k_news = KaliteNews.objects.filter(
            Q(title__icontains=query_text) | Q(summary__icontains=query_text),
            is_published=True
        )[:2]
        for kn in k_news:
            live_items.append({
                'id': f'kalite_news_{kn.id}',
                'title': kn.title,
                'category': 'Kalite Haberi',
                'icon': 'fa-newspaper',
                'url': reverse('kalite_akreditasyon:haber_detail', args=[kn.slug]),
                'description': kn.summary or kn.title,
                'quick_links': [],
                'source': 'live_news'
            })
            if len(live_items) >= limit:
                return live_items

        k_ann = KaliteAnn.objects.filter(
            Q(title__icontains=query_text) | Q(summary__icontains=query_text),
            is_published=True
        )[:2]
        for ka in k_ann:
            live_items.append({
                'id': f'kalite_ann_{ka.id}',
                'title': ka.title,
                'category': 'Kalite Duyurusu',
                'icon': 'fa-bullhorn',
                'url': reverse('kalite_akreditasyon:duyuru_detail', args=[ka.slug]),
                'description': ka.summary or ka.title,
                'quick_links': [],
                'source': 'live_announcement'
            })
            if len(live_items) >= limit:
                return live_items
    except Exception:
        pass

    # 2. Genel Haberler
    try:
        from news.models import News
        g_news = News.objects.filter(
            Q(title__icontains=query_text) | Q(summary__icontains=query_text),
            is_published=True
        )[:2]
        for gn in g_news:
            live_items.append({
                'id': f'news_{gn.id}',
                'title': gn.title,
                'category': 'Üniversite Haberi',
                'icon': 'fa-newspaper',
                'url': reverse('news:detail', args=[gn.slug]),
                'description': gn.summary or gn.title,
                'quick_links': [],
                'source': 'live_news'
            })
            if len(live_items) >= limit:
                return live_items
    except Exception:
        pass

    # 3. Genel Duyurular
    try:
        from duyurular.models import Duyuru
        g_ann = Duyuru.objects.filter(
            Q(baslik__icontains=query_text) | Q(ozet__icontains=query_text),
            yayinda=True
        )[:2]
        for ga in g_ann:
            live_items.append({
                'id': f'ann_{ga.id}',
                'title': ga.baslik,
                'category': 'Resmi Duyuru',
                'icon': 'fa-bullhorn',
                'url': reverse('duyurular:detay', args=[ga.slug]),
                'description': ga.ozet or ga.baslik,
                'quick_links': [],
                'source': 'live_announcement'
            })
            if len(live_items) >= limit:
                return live_items
    except Exception:
        pass

    return live_items
