from django import template
from django.core.cache import cache
from django.utils import timezone

register = template.Library()

CATEGORY_DEFINITIONS = [
    ("content", "Ana İçerik & Haberler", "fas fa-layer-group", "#1d61a9", True),
    ("institutional", "Kurumsal, Akademik & İdari", "fas fa-university", "#0f766e", False),
    ("faculties", "Fakülteler & Lisans Bölümleri", "fas fa-graduation-cap", "#2563eb", False),
    ("myo", "Meslek Yüksekokulu (MYO)", "fas fa-tools", "#7c3aed", False),
    ("shmyo", "Sağlık Hizmetleri MYO (SHMYO)", "fas fa-heartbeat", "#be123c", False),
    ("system", "Kullanıcılar, Sohbet & Güvenlik", "fas fa-shield-alt", "#475569", False),
    ("archive", "Arşiv / Kaldırılan Birimler", "fas fa-archive", "#64748b", False),
]

# app_label -> (Turkish Display Name, category_key, FontAwesome icon)
APP_METADATA = {
    # 1. Core Public Content
    "news": ("Haberler", "content", "fas fa-newspaper"),
    "duyurular": ("Duyurular ve Bölüm Kodları", "content", "fas fa-bullhorn"),
    "etkinlikler": ("Etkinlikler, Kayıtlar & Bildirimler", "content", "fas fa-calendar-check"),
    "core": ("Ana Sayfa, Slider & Asistan", "content", "fas fa-home"),
    "gallery": ("Fotoğraf Galerisi", "content", "fas fa-images"),
    "aday_ogrenci": ("Aday Öğrenci & Konukevi", "content", "fas fa-user-graduate"),
    "ogrenci_isleri": ("Öğrenci İşleri Daire Başkanlığı", "content", "fas fa-file-signature"),
    "support": ("Destek Merkezi, Talepler & SSS", "content", "fas fa-life-ring"),
    "contact": ("İletişim Mesajları", "content", "fas fa-envelope-open-text"),
    "tuition": ("Öğrenim Ücretleri & Ödeme", "content", "fas fa-credit-card"),

    # 2. Institutional, Administrative & International
    "avrasya_universitesi_hakkinda": ("Üniversitemiz Hakkında", "institutional", "fas fa-landmark"),
    "avrasya_universitesi_yonetim": ("Üniversite Yönetimi & Senato", "institutional", "fas fa-sitemap"),
    "akademik": ("Akademik Sayfalar & Kadrolar", "institutional", "fas fa-chalkboard-teacher"),
    "fakulteler": ("Fakülteler Genel Portalı", "institutional", "fas fa-building"),
    "enstituler": ("Enstitüler Portalı", "institutional", "fas fa-book-open"),
    "yuksekokullari": ("Yüksekokullar Portalı", "institutional", "fas fa-school"),
    "meslekyuksekokullari": ("Meslek Yüksekokulları Genel", "institutional", "fas fa-city"),
    "idari_birimler": ("İdari Birimler", "institutional", "fas fa-briefcase"),
    "sks": ("Sağlık, Kültür ve Spor (SKS)", "institutional", "fas fa-hands-helping"),
    "kutuphane": ("Kütüphane ve Dokümantasyon", "institutional", "fas fa-book"),
    "kalite_akreditasyon": ("Kalite ve Akreditasyon", "institutional", "fas fa-award"),
    "arastirma": ("Araştırma ve Geliştirme", "institutional", "fas fa-microscope"),
    "international": ("Uluslararası Öğrenci Ofisi", "institutional", "fas fa-globe"),
    "erasmus": ("Erasmus+ Koordinatörlüğü", "institutional", "fas fa-plane-departure"),
    "yatay_gecis": ("Yatay Geçiş Başvuruları", "institutional", "fas fa-exchange-alt"),
    "lee": ("Lisansüstü Eğitim Enstitüsü", "institutional", "fas fa-user-tie"),

    # 3. Faculties & Bachelor Departments
    "fen_edebiyat": ("Fen-Edebiyat Fakültesi", "faculties", "fas fa-atom"),
    "psikoloji": ("Psikoloji", "faculties", "fas fa-brain"),
    "ingiliz_dili_edebiyati": ("İngiliz Dili ve Edebiyatı", "faculties", "fas fa-language"),
    "turk_dili_edebiyati": ("Türk Dili ve Edebiyatı", "faculties", "fas fa-feather-alt"),
    "molekuler_biyoloji_genetik": ("Moleküler Biyoloji ve Genetik", "faculties", "fas fa-dna"),
    "mutercim_tercumanlik": ("İngilizce Mütercim ve Tercümanlık", "faculties", "fas fa-comments"),

    "iktisadi_idari": ("İktisadi ve İdari Bilimler Fakültesi", "faculties", "fas fa-chart-line"),
    "isletme": ("İşletme", "faculties", "fas fa-briefcase"),
    "isletme_ingilizce": ("İşletme (İngilizce)", "faculties", "fas fa-globe-americas"),
    "siyaset_bilimi": ("Siyaset Bilimi ve Kamu Yönetimi", "faculties", "fas fa-balance-scale"),
    "maliye": ("Maliye", "faculties", "fas fa-coins"),
    "uluslararasi_iliskiler": ("Uluslararası İlişkiler", "faculties", "fas fa-handshake"),

    "muhendislik_mimarlik": ("Mühendislik-Mimarlık Fakültesi", "faculties", "fas fa-drafting-compass"),
    "bilgisayar_muhendisligi": ("Bilgisayar Mühendisliği", "faculties", "fas fa-laptop-code"),
    "elektrik_elektronik_muhendisligi": ("Elektrik-Elektronik Mühendisliği", "faculties", "fas fa-bolt"),
    "gida_muhendisligi": ("Gıda Mühendisliği", "faculties", "fas fa-flask"),
    "harita_muhendisligi": ("Harita Mühendisliği", "faculties", "fas fa-map-marked-alt"),
    "ic_mimarlik": ("İç Mimarlık", "faculties", "fas fa-couch"),
    "insaat_muhendisligi": ("İnşaat Mühendisliği", "faculties", "fas fa-hard-hat"),
    "makine_muhendisligi": ("Makine Mühendisliği", "faculties", "fas fa-cogs"),
    "mimarlik": ("Mimarlık", "faculties", "fas fa-archway"),

    "saglik_bilimleri": ("Sağlık Bilimleri Fakültesi", "faculties", "fas fa-clinic-medical"),
    "beslenme_diyetetik": ("Beslenme ve Diyetetik", "faculties", "fas fa-apple-alt"),
    "cocuk_gelisimi": ("Çocuk Gelişimi (Lisans)", "faculties", "fas fa-child"),
    "ebelik": ("Ebelik", "faculties", "fas fa-baby"),
    "ergoterapi": ("Ergoterapi", "faculties", "fas fa-hands"),
    "fizyoterapi_rehabilitasyon": ("Fizyoterapi ve Rehabilitasyon", "faculties", "fas fa-walking"),
    "hemsirelik": ("Hemşirelik", "faculties", "fas fa-user-nurse"),
    "odyoloji": ("Odyoloji", "faculties", "fas fa-assistive-listening-systems"),
    "saglik_yonetimi": ("Sağlık Yönetimi", "faculties", "fas fa-hospital-user"),

    "spor_bilimleri": ("Spor Bilimleri Fakültesi", "faculties", "fas fa-running"),
    "antrenorluk_egitimi": ("Antrenörlük Eğitimi", "faculties", "fas fa-stopwatch"),
    "egzersiz": ("Egzersiz ve Spor Bilimleri", "faculties", "fas fa-dumbbell"),
    "spor_yoneticiligi": ("Spor Yöneticiliği", "faculties", "fas fa-trophy"),
    "rekreasyon": ("Rekreasyon", "faculties", "fas fa-campground"),

    "iletisim": ("İletişim Fakültesi", "faculties", "fas fa-broadcast-tower"),
    "yeni_medya_iletisim": ("Yeni Medya ve İletişim", "faculties", "fas fa-photo-video"),
    "gorsel_iletisim_tasarimi": ("Görsel İletişim Tasarımı", "faculties", "fas fa-palette"),

    "uygulamali_bilimler": ("Uygulamalı Bilimler Yüksekokulu", "faculties", "fas fa-laptop-house"),
    "yonetim_bilisim_sistemleri": ("Yönetim Bilişim Sistemleri", "faculties", "fas fa-database"),
    "gastronomi_mutfak_sanatlari": ("Gastronomi ve Mutfak Sanatları", "faculties", "fas fa-utensils"),

    # 4. MYO
    "meslek_yuksekokulu": ("Meslek Yüksekokulu (Ana Sayfa)", "myo", "fas fa-university"),
    "ascilik": ("Aşçılık", "myo", "fas fa-utensils"),
    "bilgisayar_programciligi": ("Bilgisayar Programcılığı", "myo", "fas fa-code"),
    "bilisim_guvenligi": ("Bilişim Güvenliği Teknolojisi", "myo", "fas fa-user-shield"),
    "dis_ticaret": ("Dış Ticaret", "myo", "fas fa-ship"),
    "e_ticaret": ("E-Ticaret ve Pazarlama", "myo", "fas fa-shopping-cart"),
    "grafik_tasarimi": ("Grafik Tasarımı", "myo", "fas fa-bezier-curve"),
    "halkla_iliskiler": ("Halkla İlişkiler ve Tanıtım", "myo", "fas fa-bullhorn"),
    "harita_kadastro": ("Harita ve Kadastro", "myo", "fas fa-compass"),
    "ic_mekan": ("İç Mekan Tasarımı", "myo", "fas fa-chair"),
    "insaat_teknolojisi": ("İnşaat Teknolojisi", "myo", "fas fa-hammer"),
    "lojistik_programi": ("Lojistik", "myo", "fas fa-truck"),
    "mahkeme_buro": ("Mahkeme Büro Hizmetleri", "myo", "fas fa-gavel"),
    "mimari_restorasyon": ("Mimari Restorasyon", "myo", "fas fa-monument"),
    "moda_tasarimi": ("Moda Tasarımı", "myo", "fas fa-cut"),
    "otomotiv": ("Otomotiv Teknolojisi", "myo", "fas fa-car"),
    "sivil_havacilik": ("Sivil Havacılık Kabin Hizmetleri", "myo", "fas fa-plane"),
    "sosyal_guvenlik": ("Sosyal Güvenlik", "myo", "fas fa-id-card"),
    "sosyal_hizmetler": ("Sosyal Hizmetler (MYO)", "myo", "fas fa-hands-helping"),
    "sosyal_hizmet": ("Sosyal Hizmet", "myo", "fas fa-hand-holding-heart"),
    "spor_yonetimi": ("Spor Yönetimi", "myo", "fas fa-medal"),
    "web_tasarimi": ("Web Tasarımı ve Kodlama", "myo", "fas fa-window-maximize"),

    # 5. SHMYO
    "saglik_hizmetleri_myo": ("Sağlık Hizmetleri MYO (Ana Sayfa)", "shmyo", "fas fa-hospital"),
    "acil_durum": ("Acil Durum ve Afet Yönetimi", "shmyo", "fas fa-ambulance"),
    "agiz_dis": ("Ağız ve Diş Sağlığı", "shmyo", "fas fa-tooth"),
    "ameliyathane": ("Ameliyathane Hizmetleri", "shmyo", "fas fa-procedures"),
    "anestezi": ("Anestezi", "shmyo", "fas fa-syringe"),
    "cocuk_gelisimi_programi": ("Çocuk Gelişimi (Ön Lisans)", "shmyo", "fas fa-baby-carriage"),
    "dis_protezi": ("Diş Protez Teknolojisi", "shmyo", "fas fa-teeth"),
    "diyaliz": ("Diyaliz", "shmyo", "fas fa-tint"),
    "eczane": ("Eczane Hizmetleri", "shmyo", "fas fa-pills"),
    "elektronorofizyoloji": ("Elektronörofizyoloji", "shmyo", "fas fa-wave-square"),
    "fizyoterapi": ("Fizyoterapi (Ön Lisans)", "shmyo", "fas fa-wheelchair"),
    "ilk_acil_yardim": ("İlk ve Acil Yardım", "shmyo", "fas fa-first-aid"),
    "is_sagligi_guvenligi": ("İş Sağlığı ve Güvenliği", "shmyo", "fas fa-hard-hat"),
    "is_ugrasi_terapisi": ("İş ve Uğraşı Terapisi", "shmyo", "fas fa-hands"),
    "odyometri": ("Odyometri", "shmyo", "fas fa-ear-listen"),
    "optisyenlik": ("Optisyenlik", "shmyo", "fas fa-glasses"),
    "ortopedik_protez": ("Ortopedik Protez ve Ortez", "shmyo", "fas fa-crutch"),
    "patoloji_laboratuar": ("Patoloji Laboratuvar Teknikleri", "shmyo", "fas fa-vial"),
    "radyoterapi": ("Radyoterapi", "shmyo", "fas fa-radiation"),
    "saglik_kurumlari": ("Sağlık Kurumları İşletmeciliği", "shmyo", "fas fa-clinic-medical"),
    "tibbi_goruntuleme": ("Tıbbi Görüntüleme Teknikleri", "shmyo", "fas fa-x-ray"),
    "tibbi_laboratuvar": ("Tıbbi Laboratuvar Teknikleri", "shmyo", "fas fa-microscope"),

    # 6. System, Users & Security
    "accounts": ("Kullanıcı Profilleri & Hesaplar", "system", "fas fa-id-badge"),
    "auth": ("Kullanıcılar ve Yetki Grupları", "system", "fas fa-users-cog"),
    "axes": ("Giriş Güvenliği ve Engellemeler", "system", "fas fa-lock"),
    "chat": ("Canlı Destek ve Mesajlaşma", "system", "fas fa-comments"),

    # 7. Archive / Removed Units
    "adalet": ("Adalet Programı (Kaldırıldı - Arşiv)", "archive", "fas fa-archive"),
}

_CONTENT_ORDER = {
    "news": 1,
    "duyurular": 2,
    "etkinlikler": 3,
    "core": 4,
    "gallery": 5,
    "aday_ogrenci": 6,
    "ogrenci_isleri": 7,
    "support": 8,
    "contact": 9,
    "tuition": 10,
}


def _humanize_app_label(app_dict: dict) -> tuple[str, str, str]:
    label = app_dict.get("app_label", "")
    if label in APP_METADATA:
        return APP_METADATA[label]
    fallback_title = app_dict.get("name") or label.replace("_", " ").title()
    return (fallback_title, "institutional", "fas fa-folder-open")


@register.simple_tag
def get_categorized_admin_apps(app_list):
    """Group Django Admin apps into editor-friendly Turkish categories with readable names."""
    if not app_list:
        return []

    buckets = {key: [] for key, _, _, _, _ in CATEGORY_DEFINITIONS}
    for app in app_list:
        display_name, cat_key, icon = _humanize_app_label(app)
        enriched = dict(app)
        enriched["display_name"] = display_name
        enriched["icon"] = icon
        buckets.setdefault(cat_key, []).append(enriched)

    categories = []
    for key, title, icon, color, default_open in CATEGORY_DEFINITIONS:
        apps = buckets.get(key) or []
        if not apps:
            continue
        if key == "content":
            apps.sort(key=lambda a: (_CONTENT_ORDER.get(a["app_label"], 99), a["display_name"]))
        else:
            apps.sort(key=lambda a: a["display_name"])
        categories.append({
            "key": key,
            "title": title,
            "icon": icon,
            "color": color,
            "default_open": default_open,
            "apps": apps,
        })

    # If editor has few apps or no core-content apps, expand all their accessible groups
    total_apps = sum(len(c["apps"]) for c in categories)
    has_content_cat = any(c["key"] == "content" for c in categories)
    if not has_content_cat or total_apps <= 8:
        for c in categories:
            if c["key"] != "archive":
                c["default_open"] = True

    return categories


@register.simple_tag
def get_admin_quick_actions(app_list):
    """Build single-click content creation shortcuts filtered strictly to the user's permissions."""
    if not app_list:
        return []

    model_index = {}
    for app in app_list:
        app_label = app.get("app_label")
        for m in app.get("models", []):
            model_name = (m.get("object_name") or "").lower()
            model_index[(app_label, model_name)] = m

    candidates = [
        ("news", "news", "Haber Ekle", "Yeni haber yayınla", "fas fa-newspaper", "#1d61a9", True),
        ("duyurular", "duyuru", "Duyuru Ekle", "Fakülte / genel duyuru", "fas fa-bullhorn", "#0284c7", True),
        ("etkinlikler", "etkinlik", "Etkinlik Ekle", "Takvim, afiş ve dosya", "fas fa-calendar-plus", "#0d9488", True),
        ("core", "slideritem", "Ana Sayfa Slider", "Manşet görsel & video", "fas fa-images", "#092442", False),
        ("gallery", "galleryimage", "Galeriye Fotoğraf Ekle", "Kampüs fotoğraf albümü", "fas fa-camera-retro", "#7c3aed", False),
        ("support", "ticket", "Destek Talepleri", "Öğrenci & ziyaretçi talepleri", "fas fa-headset", "#0891b2", False),
        ("support", "faq", "Sıkça Sorulan Sorular", "Asistan ve SSS cevapları", "fas fa-question-circle", "#4f46e5", False),
        ("etkinlikler", "etkinlikkayit", "Etkinlik Kayıtları", "Katılımcı listesi & Excel", "fas fa-clipboard-list", "#0f766e", False),
    ]

    actions = []
    for app_label, model_name, title, subtitle, icon, color, prefer_add in candidates:
        entry = model_index.get((app_label, model_name))
        if not entry:
            continue
        url = entry.get("add_url") if (prefer_add and entry.get("add_url")) else (entry.get("admin_url") or entry.get("add_url"))
        if not url:
            continue
        actions.append({
            "title": title,
            "subtitle": subtitle,
            "url": url,
            "list_url": entry.get("admin_url"),
            "icon": icon,
            "color": color,
        })
    return actions


@register.simple_tag
def get_admin_dashboard_stats():
    """Return lightweight cached KPI metrics for the Admin dashboard."""
    cached = cache.get("core:admin_dashboard_stats:v1")
    if cached is not None:
        stats = dict(cached)
    else:
        stats = {
            "news_count": 0,
            "duyuru_count": 0,
            "etkinlik_count": 0,
            "open_tickets": 0,
        }
        try:
            from news.models import News
            stats["news_count"] = News.objects.filter(is_published=True).count()
        except Exception:
            pass
        try:
            from duyurular.models import Duyuru
            stats["duyuru_count"] = Duyuru.objects.filter(yayinda=True).count()
        except Exception:
            pass
        try:
            from etkinlikler.models import Etkinlik
            stats["etkinlik_count"] = Etkinlik.objects.filter(
                yayinda=True,
                baslangic_tarihi__gte=timezone.now(),
            ).count()
        except Exception:
            pass
        try:
            from support.models import Ticket
            stats["open_tickets"] = Ticket.objects.filter(status="open").count()
        except Exception:
            pass
        cache.set("core:admin_dashboard_stats:v1", stats, 60)

    try:
        from core.services.visitors import get_online_visitors_count
        stats["online_visitors"] = get_online_visitors_count()
    except Exception:
        stats["online_visitors"] = 0

    return stats
