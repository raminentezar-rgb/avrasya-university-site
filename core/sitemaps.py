from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import NoReverseMatch, reverse
from django.utils import translation

from chat.voice_directory import get_voice_directory
from duyurular.models import Duyuru
from etkinlikler.models import Etkinlik
from gallery.models import GalleryCategory
from news.models import News


_EXCLUDED_DIRECTORY_PREFIXES = (
    "/adalet",
    "/home",
    "/anasyafa",
    "/test",
    "/elements",
    "/accounts",
    "/chat",
    "/odeme",
    "/support/ticket",
    "/support/takip",
    "/support/taleplerim",
    "/support/department",
    "/support/staff",
)


class CoreStaticSitemap(Sitemap):
    changefreq = "weekly"
    i18n = True
    alternates = True

    _ROUTE_PRIORITIES = [
        ("core:index", 1.0, "daily"),
        ("news:list", 0.9, "daily"),
        ("duyurular:liste", 0.9, "daily"),
        ("etkinlikler:liste", 0.8, "daily"),
        ("aday_ogrenci:aday_anasayfa", 0.9, "weekly"),
        ("aday_ogrenci:yurt_olanaklari", 0.7, "monthly"),
        ("ogrenci_isleri:ogrenci_isleri", 0.8, "weekly"),
        ("ogrenci_isleri:yurtlar", 0.7, "monthly"),
        ("akademik:akademik", 0.8, "weekly"),
        ("idari_birimler:idari_birimler", 0.7, "monthly"),
        ("arastirma:home", 0.8, "weekly"),
        ("international:international", 0.8, "weekly"),
        ("erasmus:erasmus", 0.7, "monthly"),
        ("kutuphane:kutuphane", 0.7, "monthly"),
        ("gallery:main", 0.6, "monthly"),
        ("support:search", 0.7, "weekly"),
        ("support:faq_list", 0.7, "weekly"),
        ("core:iletisim", 0.8, "monthly"),
        ("contact:contact", 0.7, "monthly"),
    ]

    def items(self):
        valid = []
        for url_name, prio, freq in self._ROUTE_PRIORITIES:
            try:
                reverse(url_name)
                valid.append((url_name, prio, freq))
            except NoReverseMatch:
                continue
        return valid

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]


class NewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    i18n = True
    alternates = True

    def items(self):
        return News.objects.filter(is_published=True).order_by("-published_at")[:500]

    def lastmod(self, obj):
        return obj.published_at or obj.created_at


class DuyuruSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    i18n = True
    alternates = True

    def items(self):
        return Duyuru.objects.filter(yayinda=True).order_by("-yayin_tarihi")[:500]

    def lastmod(self, obj):
        return obj.yayin_tarihi or obj.olusturulma_tarihi


class EtkinlikSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    i18n = True
    alternates = True

    def items(self):
        return Etkinlik.objects.filter(yayinda=True).order_by("-baslangic_tarihi")[:500]

    def lastmod(self, obj):
        return obj.guncellenme_tarihi or obj.olusturulma_tarihi


class GallerySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    i18n = True
    alternates = True

    def items(self):
        return GalleryCategory.objects.filter(is_active=True).order_by("order", "name")


class AcademicDirectorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    i18n = True
    alternates = True

    def items(self):
        static_paths = set()
        for url_name, _, _ in CoreStaticSitemap._ROUTE_PRIORITIES:
            try:
                static_paths.add(reverse(url_name))
            except NoReverseMatch:
                pass

        seen = set()
        urls = []
        for entry in get_voice_directory():
            raw_url = (entry.get("url") or "").strip()
            if not raw_url.startswith("/") or "#" in raw_url:
                continue
            lower = raw_url.lower()
            if any(lower == p or lower.startswith(p + "/") for p in _EXCLUDED_DIRECTORY_PREFIXES):
                continue
            normalized = raw_url if raw_url.endswith("/") else raw_url + "/"
            if raw_url in static_paths or normalized in static_paths:
                continue
            if normalized not in seen:
                seen.add(normalized)
                urls.append(raw_url)
        return urls

    def location(self, item):
        lang = translation.get_language() or getattr(settings, "LANGUAGE_CODE", "tr")
        default_lang = getattr(settings, "LANGUAGE_CODE", "tr")
        path = item if item.startswith("/") else "/" + item
        if lang != default_lang and not path.startswith(f"/{lang}/"):
            return f"/{lang}{path}"
        return path


sitemaps = {
    "core": CoreStaticSitemap,
    "news": NewsSitemap,
    "duyurular": DuyuruSitemap,
    "etkinlikler": EtkinlikSitemap,
    "gallery": GallerySitemap,
    "academics": AcademicDirectorySitemap,
}
