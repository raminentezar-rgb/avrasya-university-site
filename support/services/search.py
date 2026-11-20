# support/services/search.py
"""Site-wide Turkish-aware smart search engine across pages, academics, news, quality, and support."""

from difflib import SequenceMatcher
import html as html_lib
import re
import time

from django.apps import apps
from django.core.cache import cache
from django.db.models import Q
from django.urls import URLResolver, get_resolver, reverse
from django.utils import translation
from django.utils.html import strip_tags

from akademik.models import BolumAkademikKadroUyesi, BolumSayfasi, FakulteSayfasi
from chat.voice_directory import get_voice_directory
from kalite_akreditasyon.models import BolumKalite, SSS as KaliteSSS, Takim as KaliteTakim
from support.models import Category, Department, FAQ, ImportantLink, KnowledgeBase


TRANSLATION_SUFFIXES = ('_tr', '_en', '_fa', '_ar', '_ru', '_de')
EXCLUDED_DYNAMIC_APPS = {
    'admin', 'auth', 'contenttypes', 'sessions', 'messages',
    'staticfiles', 'axes', 'daphne', 'modeltranslation',
    'crispy_forms', 'crispy_bootstrap5', 'channels', 'support',
    'accounts', 'chat', 'ckeditor', 'ckeditor_uploader', 'gallery',
    'adalet',
}
REMOVED_SEARCH_APPS = {'adalet'}
_EXCLUDED_URL_RE = re.compile(r'^/(?:[a-z]{2}/)?adalet(?:/|$|#)', re.IGNORECASE)
PREFERRED_TITLE_FIELDS = ('baslik', 'title', 'question', 'name', 'ad', 'ad_soyad')
PREFERRED_CONTENT_FIELDS = (
    'ozet', 'summary', 'icerik', 'detayli_aciklama', 'aciklama',
    'answer', 'description', 'kisa_aciklama', 'content',
)

ASCII_FOLD_MAP = str.maketrans({
    'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
    'â': 'a', 'î': 'i', 'û': 'u',
    'Ç': 'c', 'Ğ': 'g', 'İ': 'i', 'I': 'i', 'Ö': 'o', 'Ş': 's', 'Ü': 'u',
})

SYNONYM_GROUPS = [
    ('aday', 'tercih', 'kontenjan', 'taban', 'yks', 'osym'),
    ('shmyo', 'saglik hizmetleri meslek yuksekokulu'),
    ('myo', 'meslek yuksekokulu'),
    ('iibf', 'iktisadi ve idari bilimler'),
    ('lee', 'lisansustu egitim enstitusu', 'yuksek lisans', 'doktora'),
    ('sks', 'saglik kultur ve spor', 'yemekhane', 'konukevi', 'konukevleri', 'yurt', 'kulup'),
    ('wifi', 'eduroam', 'kablosuz ag'),
    ('harc', 'ogrenim ucreti', 'ucret', 'odeme', 'taksit'),
    ('sss', 'sikca sorulan sorular'),
    ('cap', 'cift anadal', 'yandal'),
    ('kalite', 'akreditasyon', 'yokak', 'kidr'),
]

ADAY_AND_OGRENCI_SUBPAGES = [
    {
        'title': 'Aday Öğrenci - Kontenjanlar',
        'category': 'Aday Öğrenci',
        'url_name': 'aday_ogrenci:kontenjanlar',
        'icon': 'fa-list-ol',
        'description': 'Avrasya Üniversitesi bölümlerinin güncel YKS kontenjanları ve doluluk bilgileri.',
        'keywords': 'aday öğrenci kontenjan yks ösym bölüm sayıları',
    },
    {
        'title': 'Aday Öğrenci - Taban Puanlar ve Başarı Sıralamaları',
        'category': 'Aday Öğrenci',
        'url_name': 'aday_ogrenci:taban_puanlar',
        'icon': 'fa-chart-bar',
        'description': 'Fakülte ve yüksekokulların taban puanları, başarı sıralamaları ve puan türleri.',
        'keywords': 'aday öğrenci taban puan başarı sırası tercih yks tyt ayt',
    },
    {
        'title': 'Aday Öğrenci - Eğitim Ücretleri ve Burs Olanakları',
        'category': 'Aday Öğrenci',
        'url_name': 'aday_ogrenci:egitim_ucretleri',
        'icon': 'fa-money-bill-wave',
        'description': 'Aday öğrenciler için bölüm bazlı eğitim ücretleri, burs ve tercih indirim oranları.',
        'keywords': 'aday öğrenci ücret fiyat burs indirim ödeme taksit',
    },
    {
        'title': 'Aday Öğrenci - Online Başvuru Formu',
        'category': 'Aday Öğrenci',
        'url_name': 'aday_ogrenci:basvuru',
        'icon': 'fa-file-signature',
        'description': 'Aday öğrencilerin bilgi almak veya ön başvuru yapmak için kullanabileceği online form.',
        'keywords': 'aday öğrenci online başvuru kayıt ön kayıt',
    },
    {
        'title': 'Aday Öğrenci - Konukevi ve Barınma İmkanları',
        'category': 'Aday Öğrenci',
        'url_name': 'aday_ogrenci:yurt_olanaklari',
        'icon': 'fa-bed',
        'description': 'Üniversite konukevleri, oda kapasiteleri, güvenlik ve konaklama olanakları.',
        'keywords': 'aday öğrenci konukevi konukevleri barınma konaklama kız konukevi erkek konukevi yurt',
    },
    {
        'title': 'Aday Öğrenci - Laboratuvarlar ve Uygulama Alanları',
        'category': 'Aday Öğrenci',
        'url_name': 'aday_ogrenci:laboratuvarlar',
        'icon': 'fa-flask',
        'description': 'Mühendislik, sağlık ve iletişim alanlarındaki modern laboratuvar ve atölyeler.',
        'keywords': 'aday öğrenci laboratuvar atölye uygulama alanı',
    },
    {
        'title': 'Aday Öğrenci - Kampüs Yaşamı',
        'category': 'Aday Öğrenci',
        'url_name': 'aday_ogrenci:kampus_yasam',
        'icon': 'fa-campus' if False else 'fa-university',
        'description': 'Yerleşkeler, yemekhane, spor alanları, kütüphane ve öğrenci toplulukları.',
        'keywords': 'aday öğrenci kampüs yaşamı pelitli yomra ömer yıldız kaşüstü',
    },
    {
        'title': 'Aday Öğrenci - Çift Anadal (ÇAP) ve Yan Dal',
        'category': 'Aday Öğrenci',
        'url_name': 'aday_ogrenci:cap_yan_dal',
        'icon': 'fa-code-branch',
        'description': 'Aday öğrenciler için çift anadal ve yan dal programları hakkında detaylı bilgiler.',
        'keywords': 'aday öğrenci çap çift anadal yan dal',
    },
    {
        'title': 'Aday Öğrenci - Dikey Geçiş (DGS)',
        'category': 'Aday Öğrenci',
        'url_name': 'aday_ogrenci:dikey_gecis',
        'icon': 'fa-exchange-alt',
        'description': 'Ön lisans mezunları için DGS ile lisans tamamlama koşulları.',
        'keywords': 'aday öğrenci dikey geçiş dgs önlisans',
    },
    {
        'title': 'Aday Öğrenci - Uluslararası (Yabancı) Öğrenci',
        'category': 'Aday Öğrenci',
        'url_name': 'aday_ogrenci:yabanci_ogrenci',
        'icon': 'fa-globe',
        'description': 'Yabancı uyruklu aday öğrenciler için başvuru şartları ve kabul süreçleri.',
        'keywords': 'aday öğrenci yabancı uluslararası öğrenci yös',
    },
    {
        'title': 'Öğrenci İşleri - Ders Muafiyet İşlemleri',
        'category': 'Öğrenci Hizmetleri',
        'url_name': 'ogrenci_isleri:muafiyetler',
        'icon': 'fa-check-double',
        'description': 'Daha önce alınan derslerin muafiyet ve intibak başvuru koşulları.',
        'keywords': 'muafiyet intibak ders saydırma öğrenci işleri',
    },
    {
        'title': 'Öğrenci İşleri - Öğrenci Kulüpleri',
        'category': 'Öğrenci Hizmetleri',
        'url_name': 'ogrenci_isleri:kulupler',
        'icon': 'fa-users',
        'description': 'Üniversitemiz bünyesinde faaliyet gösteren aktif öğrenci kulüpleri ve toplulukları.',
        'keywords': 'kulüp topluluk etkinlik öğrenci kulüpleri',
    },
    {
        'title': 'Öğrenci İşleri - Yönetmelik ve Yönergeler',
        'category': 'Öğrenci Hizmetleri',
        'url_name': 'ogrenci_isleri:yonetmelik',
        'icon': 'fa-book',
        'description': 'Eğitim-öğretim, sınav ve disiplin yönetmelikleri ile resmi yönergeler.',
        'keywords': 'yönetmelik yönerge mevzuat sınav kuralları',
    },
    {
        'title': 'Öğrenci İşleri - Dilekçe ve Resmi Formlar',
        'category': 'Öğrenci Hizmetleri',
        'url_name': 'ogrenci_isleri:formlar',
        'icon': 'fa-file-alt',
        'description': 'Öğrencilerin ihtiyaç duyduğu dilekçe örnekleri ve resmi başvuru formları.',
        'keywords': 'form dilekçe belge indir öğrenci işleri',
    },
]

_APP_URL_MAP = None
_INDEX_MEMORY_CACHE = {}
INDEX_TTL_SECONDS = 300


def normalize_tr(text):
    """Lowercase using Turkish rules (İ -> i, I -> ı) and collapse whitespace."""
    if not text:
        return ''
    s = str(text).replace('İ', 'i').replace('I', 'ı').lower()
    s = re.sub(r'[^\wçğıöşüâîû\s]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def normalize_ascii(text):
    """Fold Turkish diacritics into ASCII equivalents for accent-insensitive matching."""
    if not text:
        return ''
    s = str(text).translate(ASCII_FOLD_MAP).lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def _clean_text(raw):
    if not raw:
        return ''
    return re.sub(r'\s+', ' ', html_lib.unescape(strip_tags(str(raw)))).strip()


def _get_app_url_map():
    """Map Django app_label -> mounted URL prefix (handles custom slugs like /harita_kadastror/)."""
    global _APP_URL_MAP
    if _APP_URL_MAP is not None:
        return _APP_URL_MAP

    mapping = {}

    def _walk(patterns, prefix='/'):
        for p in patterns:
            if isinstance(p, URLResolver):
                mod = getattr(p.urlconf_module, '__name__', '')
                app = mod.split('.')[0] if mod else ''
                route = str(p.pattern)
                full_prefix = prefix + route
                if app and app not in {'django'}:
                    mapping.setdefault(app, full_prefix)
                _walk(p.url_patterns, full_prefix)

    _walk(get_resolver().url_patterns)
    _APP_URL_MAP = mapping
    return mapping


def clear_search_index():
    """Clear both in-memory and Django search indexes."""
    _INDEX_MEMORY_CACHE.clear()
    for lang in ('tr', 'en', 'fa', 'ar', 'ru', 'de'):
        cache.delete(f"site_search_index:v2:{lang}")


def _make_doc(
    *,
    doc_type,
    title,
    content='',
    category='',
    department='',
    url='',
    icon='fa-file-alt',
    keywords='',
    quick_links=None,
    created_at=None,
):
    clean_title = _clean_text(title)
    clean_content = _clean_text(content)
    clean_kw = _clean_text(keywords)
    clean_cat = _clean_text(category)
    clean_dept = _clean_text(department)

    if not clean_title or not url:
        return None

    return {
        'type': doc_type,
        'title': clean_title,
        'content': clean_content[:420],
        'category': clean_cat,
        'department': clean_dept,
        'url': url,
        'icon': icon or 'fa-file-alt',
        'quick_links': quick_links or [],
        'created_at': created_at,
        '_t_tr': normalize_tr(clean_title),
        '_t_asc': normalize_ascii(clean_title),
        '_k_tr': normalize_tr(f"{clean_kw} {clean_cat} {clean_dept}"),
        '_k_asc': normalize_ascii(f"{clean_kw} {clean_cat} {clean_dept}"),
        '_b_tr': normalize_tr(clean_content),
        '_b_asc': normalize_ascii(clean_content),
    }


def _classify_faq_label(question, answer):
    text = f"{question} {answer}".lower()
    if any(k in text for k in ('ücret', 'taksit', 'harç', 'burs', 'ödeme')):
        return 'Burs & Ücretler'
    if any(k in text for k in ('tez', 'akts', 'lisansüstü', 'enstitü', 'devam zorunluluğu', 'geçme notu', 'başvuru')):
        return 'Lisansüstü'
    if any(k in text for k in ('yemekhane', 'kütüphane', 'spor', 'wi-fi', 'eduroam', 'internet', 'yerleşke')):
        return 'Kampüs & Teknik'
    if any(k in text for k in ('dekan', 'müdür', 'fakülte', 'yüksekokul')):
        return 'Yönetim & Birimler'
    return 'SSS'


def _build_site_index(lang_code):
    docs = []
    seen_keys = set()

    def _add(doc):
        if not doc:
            return
        if _EXCLUDED_URL_RE.match((doc.get('url') or '').strip()):
            return
        key = (doc['url'], doc['_t_tr'])
        if key in seen_keys:
            return
        seen_keys.add(key)
        docs.append(doc)

    # 1. Support FAQs
    seen_faq = set()
    for faq in FAQ.objects.filter(is_active=True).select_related('department').order_by('id'):
        norm_q = normalize_tr(faq.question)
        if not norm_q or norm_q in seen_faq:
            continue
        seen_faq.add(norm_q)
        _add(_make_doc(
            doc_type='faq',
            title=faq.question,
            content=faq.answer,
            category=_classify_faq_label(faq.question, faq.answer),
            department=faq.department.name if faq.department else 'Destek Merkezi',
            url=reverse('support:faq_detail', kwargs={'pk': faq.pk}),
            icon='fa-question-circle',
            keywords='sss sıkça sorulan sorular destek',
        ))

    # 2. Non-empty KnowledgeBase & ImportantLinks
    for kb in (
        KnowledgeBase.objects.exclude(Q(title='') | Q(title__isnull=True))
        .select_related('category', 'department')[:200]
    ):
        _add(_make_doc(
            doc_type='guide',
            title=kb.title,
            content=kb.content,
            category=kb.category.name if kb.category else 'Bilgi Bankası',
            department=kb.department.name if kb.department else '',
            url=reverse('support:knowledge_detail', kwargs={'pk': kb.pk}),
            icon='fa-book-open',
            created_at=kb.created_at,
        ))

    for link in ImportantLink.objects.exclude(Q(title='') | Q(title__isnull=True))[:100]:
        _add(_make_doc(
            doc_type='page',
            title=link.title,
            content=link.description,
            category='Hızlı Bağlantı',
            url=link.url,
            icon='fa-external-link-alt',
        ))

    # 3. Curated Subpages (Aday Öğrenci & Öğrenci İşleri) BEFORE general directory so subpages carry rich keywords
    for sp in ADAY_AND_OGRENCI_SUBPAGES:
        try:
            url = reverse(sp['url_name'])
        except Exception:
            continue
        _add(_make_doc(
            doc_type='page',
            title=sp['title'],
            content=sp['description'],
            category=sp['category'],
            url=url,
            icon=sp['icon'],
            keywords=sp['keywords'],
        ))

    # 4. Complete Site Directory (120+ Portals, Faculties, Programs, Units from voice_directory)
    try:
        aday_quick_links = []
        for sp in ADAY_AND_OGRENCI_SUBPAGES[:6]:
            try:
                aday_quick_links.append({'title': sp['title'].replace('Aday Öğrenci - ', ''), 'url': reverse(sp['url_name'])})
            except Exception:
                pass

        for item in get_voice_directory():
            item_url = item.get('url') or '/'
            # Fix legacy core:home URL to homepage root if needed
            if item.get('id') == 'anasayfa':
                item_url = '/'
            qlinks = list(item.get('quick_links') or [])
            if item.get('id') == 'aday_ogrenci' and aday_quick_links:
                qlinks = aday_quick_links
            cat_lower = (item.get('category') or '').lower()
            dtype = 'academic' if any(w in cat_lower for w in ('fakülte', 'bölüm', 'program', 'enstitü')) else 'page'
            _add(_make_doc(
                doc_type=dtype,
                title=item.get('title', ''),
                content=item.get('description', ''),
                category=item.get('category', 'Sayfa'),
                url=item_url,
                icon=item.get('icon', 'fa-compass'),
                keywords=' '.join(item.get('keywords') or []),
                quick_links=qlinks[:5],
            ))
    except Exception:
        pass

    # 5. Live Academic Faculties, Departments & Staff (using resolved app URL map)
    app_urls = _get_app_url_map()

    for fak in FakulteSayfasi.objects.filter(aktif=True).prefetch_related('bolum_kartlari'):
        target_app = 'lee' if fak.fakulte_kodu == 'lee' else fak.fakulte_kodu
        f_url = app_urls.get(target_app)
        if not f_url:
            continue
        f_name = fak.get_localized('fakulte_adi', fak.fakulte_kodu)
        card_names = ' '.join(
            k.get_localized('ad', '')
            for k in fak.bolum_kartlari.filter(aktif=True)
            if not _EXCLUDED_URL_RE.match((k.detay_url or '').strip())
        )
        body = f"{fak.get_localized('hero_alt_baslik', '')} {fak.get_localized('dekan_mesaji', '')} {fak.get_localized('tarihce_icerik', '')} {fak.get_localized('misyon_icerik', '')}"
        _add(_make_doc(
            doc_type='academic',
            title=f_name,
            content=body or f"{f_name} bölümleri, yönetim, tarihçe ve akademik bilgiler.",
            category='Fakülte / Yüksekokul',
            department=f_name,
            url=f_url,
            icon='fa-university',
            keywords=f"{fak.yonetici_unvan_ad or ''} {card_names}",
        ))

    for bolum in BolumSayfasi.objects.filter(aktif=True).prefetch_related('akademik_kadro'):
        if bolum.bolum_kodu in REMOVED_SEARCH_APPS:
            continue
        b_url = app_urls.get(bolum.bolum_kodu)
        if not b_url:
            continue
        b_name = bolum.get_localized('bolum_adi', bolum.bolum_kodu)
        f_name = bolum.get_localized('fakulte_adi', '')
        kadro_names = ' '.join(
            f"{k.ad_soyad} {k.unvan_gorev}" for k in bolum.akademik_kadro.filter(aktif=True)
        )
        body = (
            f"{bolum.get_localized('tarihce_icerik', '')} "
            f"{bolum.get_localized('ne_is_yaparlar_icerik', '')} "
            f"{bolum.get_localized('mezunlar_calisma_icerik', '')}"
        )
        _add(_make_doc(
            doc_type='academic',
            title=f"{b_name}" + (f" ({f_name})" if f_name else ""),
            content=body or f"{b_name} bölüm bilgileri, ne iş yaparlar, yönetim ve akademik kadro.",
            category=bolum.get_localized('program_turu', 'Bölüm / Program'),
            department=f_name,
            url=b_url,
            icon='fa-graduation-cap',
            keywords=f"{b_name} {f_name} {bolum.baskan_unvan_ad or ''} {kadro_names}",
        ))

    for staff in BolumAkademikKadroUyesi.objects.filter(aktif=True).select_related('bolum_sayfasi'):
        if staff.bolum_sayfasi.bolum_kodu in REMOVED_SEARCH_APPS:
            continue
        b_url = app_urls.get(staff.bolum_sayfasi.bolum_kodu)
        if not b_url:
            continue
        b_name = staff.bolum_sayfasi.get_localized('bolum_adi', staff.bolum_sayfasi.bolum_kodu)
        _add(_make_doc(
            doc_type='academic',
            title=f"{staff.ad_soyad} - {staff.unvan_gorev}",
            content=f"{b_name} · {staff.uzmanlik_alani or staff.biyografi or 'Akademik Kadro Üyesi'}",
            category='Akademik Kadro',
            department=b_name,
            url=f"{b_url}#akademik-kadro",
            icon='fa-chalkboard-teacher',
            keywords=f"{staff.ad_soyad} {staff.unvan_gorev} {b_name} {staff.uzmanlik_alani}",
        ))

    # 6. Kalite & Akreditasyon SSS & Ekip
    try:
        sss_url = reverse('kalite_akreditasyon:sss')
        for item in KaliteSSS.objects.filter(is_active=True)[:60]:
            _add(_make_doc(
                doc_type='faq',
                title=item.question,
                content=item.answer,
                category='Kalite SSS',
                department='Kalite ve Akreditasyon',
                url=sss_url,
                icon='fa-award',
                keywords='kalite akreditasyon yökak sss',
            ))

        takim_url = reverse('kalite_akreditasyon:takim')
        for member in KaliteTakim.objects.all()[:40]:
            m_name = getattr(member, 'name', '') or getattr(member, 'ad_soyad', '') or str(member)
            m_role = getattr(member, 'role', '') or getattr(member, 'gorev', '') or ''
            if m_name:
                _add(_make_doc(
                    doc_type='guide',
                    title=m_name,
                    content=f"{m_role} - Kalite ve Akreditasyon Koordinatörlüğü",
                    category='Kalite Ekibi',
                    department='Kalite Koordinatörlüğü',
                    url=takim_url,
                    icon='fa-user-tie',
                ))

        rapor_url = reverse('kalite_akreditasyon:raporlar')
        for bk in BolumKalite.objects.all()[:60]:
            b_title = getattr(bk, 'title', '') or getattr(bk, 'bolum_adi', '') or getattr(bk, 'name', '')
            if b_title:
                _add(_make_doc(
                    doc_type='guide',
                    title=f"Kalite: {b_title}",
                    content=getattr(bk, 'description', '') or getattr(bk, 'aciklama', '') or 'Bölüm kalite değerlendirme ve rapor bilgileri.',
                    category='Kalite ve Akreditasyon',
                    url=rapor_url,
                    icon='fa-award',
                ))
    except Exception:
        pass

    # 7. Support Units (direct ticket link for every department)
    for dept in Department.objects.all():
        _add(_make_doc(
            doc_type='page',
            title=f"{dept.name} (Destek Talebi Oluştur)",
            content=f"{dept.name} birimine doğrudan soru veya destek talebi göndermek için tıklayın.",
            category='Destek Birimi',
            department=dept.name,
            url=f"{reverse('support:create_ticket')}?department={dept.id}",
            icon='fa-paper-plane',
            keywords=f"destek talep şikayet başvuru {dept.name}",
        ))

    # 8. Dynamic Public Models with get_absolute_url (News, Duyuru, Etkinlik, Faculty/Dept updates)
    for model in apps.get_models():
        app_label = model._meta.app_label
        if app_label in EXCLUDED_DYNAMIC_APPS or model._meta.proxy:
            continue
        if not hasattr(model, 'get_absolute_url'):
            continue

        field_map = {
            f.name: f for f in model._meta.get_fields()
            if getattr(f, 'get_internal_type', lambda: '')() in ('CharField', 'TextField')
            and getattr(f, 'choices', None) is None
            and f.name != 'slug'
        }
        if not field_map:
            continue

        field_names = {f.name for f in model._meta.get_fields()}
        active_filters = {
            bf: True for bf in ('yayinda', 'is_published', 'aktif', 'is_active') if bf in field_names
        }
        try:
            objs = list(model.objects.filter(**active_filters)[:40])
        except Exception:
            continue

        if not objs:
            continue

        app_verbose = str(apps.get_app_config(app_label).verbose_name)
        model_verbose = str(model._meta.verbose_name).title()

        for obj in objs:
            try:
                obj_url = obj.get_absolute_url()
            except Exception:
                continue

            title_attr = next((a for a in PREFERRED_TITLE_FIELDS if hasattr(obj, a)), None)
            raw_title = getattr(obj, title_attr, str(obj)) if title_attr else str(obj)
            if callable(raw_title):
                raw_title = raw_title()

            content_attr = next((a for a in PREFERRED_CONTENT_FIELDS if hasattr(obj, a)), None)
            raw_content = getattr(obj, content_attr, '') if content_attr else ''
            if callable(raw_content):
                raw_content = raw_content()

            created_at = (
                getattr(obj, 'olusturulma_tarihi', None)
                or getattr(obj, 'created_at', None)
                or getattr(obj, 'yayin_tarihi', None)
            )
            dtype = 'news' if app_label in ('news', 'duyurular', 'etkinlikler') or 'duyuru' in model.__name__.lower() or 'etkinlik' in model.__name__.lower() else 'guide'
            icon = 'fa-bullhorn' if 'duyuru' in model.__name__.lower() else ('fa-calendar-check' if 'etkinlik' in model.__name__.lower() else 'fa-newspaper')

            _add(_make_doc(
                doc_type=dtype,
                title=str(raw_title),
                content=str(raw_content or ''),
                category=model_verbose,
                department=app_verbose,
                url=obj_url,
                icon=icon,
                keywords=f"{app_verbose} {model_verbose}",
                created_at=created_at,
            ))

    return docs


def get_site_index(lang_code='tr'):
    now = time.monotonic()
    entry = _INDEX_MEMORY_CACHE.get(lang_code)
    if entry and (now - entry['ts']) < INDEX_TTL_SECONDS:
        return entry['docs']

    cache_key = f"site_search_index:v2:{lang_code}"
    docs = cache.get(cache_key)
    if docs is None:
        docs = _build_site_index(lang_code)
        cache.set(cache_key, docs, INDEX_TTL_SECONDS)

    _INDEX_MEMORY_CACHE[lang_code] = {'ts': now, 'docs': docs}
    return docs


def _expand_query_tokens(norm_tr_q, norm_asc_q):
    tokens_tr = [t for t in norm_tr_q.split() if len(t) >= 2]
    tokens_asc = [t for t in norm_asc_q.split() if len(t) >= 2]

    extra_asc = set()
    for tok in tokens_asc:
        for group in SYNONYM_GROUPS:
            if tok in group or any(tok == g.split()[0] and tok == g for g in group):
                for alias in group:
                    extra_asc.add(alias)

    return tokens_tr, tokens_asc, list(extra_asc - set(tokens_asc))


def _score_doc(doc, q_tr, q_asc, tokens_tr, tokens_asc, syn_asc):
    score = 0
    t_tr, t_asc = doc['_t_tr'], doc['_t_asc']
    k_tr, k_asc = doc['_k_tr'], doc['_k_asc']
    b_tr, b_asc = doc['_b_tr'], doc['_b_asc']

    # 1. Exact & substring phrase hits
    if q_tr == t_tr or (q_asc and q_asc == t_asc) or (q_asc and t_asc == f"{q_asc} portali"):
        score += 240
    elif q_tr and t_tr.startswith(q_tr):
        score += 170
    elif q_asc and t_asc.startswith(q_asc):
        score += 155
    elif q_tr and q_tr in t_tr:
        score += 135
    elif q_asc and q_asc in t_asc:
        score += 120

    if q_tr and q_tr in k_tr:
        score += 95
    elif q_asc and q_asc in k_asc:
        score += 85

    if q_tr and q_tr in b_tr:
        score += 55
    elif q_asc and q_asc in b_asc:
        score += 45

    # 2. Multi-word token scoring
    matched_tokens = 0
    combined_asc = f"{t_asc} {k_asc} {b_asc}"
    for tok_tr, tok_asc in zip(tokens_tr, tokens_asc):
        hit = False
        if tok_tr in t_tr or tok_asc in t_asc:
            score += 42
            hit = True
        elif any(w.startswith(tok_asc) for w in t_asc.split()):
            score += 30
            hit = True

        if tok_tr in k_tr or tok_asc in k_asc:
            score += 24
            hit = True

        if tok_tr in b_tr or tok_asc in b_asc:
            score += 12
            hit = True

        if not hit and tok_asc in combined_asc:
            hit = True
        if hit:
            matched_tokens += 1

    # Bonus if ALL words in multi-word query are present
    if len(tokens_asc) > 1 and matched_tokens == len(tokens_asc):
        score += 75

    # 3. Synonym bonus using whole-word boundary matching so short aliases never match substrings
    if syn_asc:
        t_words = set(t_asc.split())
        k_words = set(k_asc.split())
        for syn in syn_asc:
            matched_syn = (syn in t_words) if ' ' not in syn else (syn in t_asc)
            if matched_syn:
                score += 28
                break
            matched_kw_syn = (syn in k_words) if ' ' not in syn else (syn in k_asc)
            if matched_kw_syn:
                score += 18
                break

    # Primary root portal boost ONLY when query actually matched this document
    if score > 0:
        clean_path = (doc.get('url') or '').split('#')[0].strip('/')
        if clean_path and '/' not in clean_path and doc.get('type') in ('page', 'academic'):
            score += 35

    return score


def search_site_content(query, lang_code=None, limit=80):
    """Search the entire site with Turkish normalization, ranking, synonyms, and typo tolerance."""
    q_raw = (query or '').strip()
    if len(q_raw) < 2:
        return []

    lang = (lang_code or translation.get_language() or 'tr').split('-')[0]
    q_tr = normalize_tr(q_raw)
    q_asc = normalize_ascii(q_raw)
    if not q_tr and not q_asc:
        return []

    tokens_tr, tokens_asc, syn_asc = _expand_query_tokens(q_tr, q_asc)
    docs = get_site_index(lang)

    scored = []
    for doc in docs:
        sc = _score_doc(doc, q_tr, q_asc, tokens_tr, tokens_asc, syn_asc)
        if sc > 0:
            scored.append((sc, doc))

    # Subtle typo tolerance fallback only when direct hits are sparse
    if len(scored) < 3 and len(q_asc) >= 4:
        already = {id(d) for _, d in scored}
        for doc in docs:
            if id(doc) in already:
                continue
            words = set(doc['_t_asc'].split() + doc['_k_asc'].split())
            best_sim = 0.0
            for q_tok in tokens_asc:
                if len(q_tok) < 4:
                    continue
                for w in words:
                    if len(w) < 4 or abs(len(w) - len(q_tok)) > 2:
                        continue
                    sim = SequenceMatcher(None, q_tok, w).ratio()
                    if sim > best_sim:
                        best_sim = sim
            if best_sim >= 0.78:
                scored.append((int(best_sim * 45), doc))

    # Boost primary portals/FAQ slightly when scores tie
    type_priority = {'page': 4, 'academic': 3, 'faq': 2, 'guide': 1, 'news': 0}
    scored.sort(key=lambda item: (item[0], type_priority.get(item[1]['type'], 0)), reverse=True)

    results = []
    for _, doc in scored[:limit]:
        results.append({
            'type': doc['type'],
            'title': doc['title'],
            'content': doc['content'],
            'category': doc['category'],
            'department': doc['department'],
            'url': doc['url'],
            'icon': doc['icon'],
            'quick_links': doc['quick_links'],
            'created_at': doc['created_at'],
        })
    return results
