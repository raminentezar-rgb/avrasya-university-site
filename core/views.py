from datetime import timedelta
from pathlib import Path
from django.conf import settings
from django.contrib.staticfiles.finders import find as find_static
from django.core.cache import cache
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import translate_url
from django.utils import timezone, translation

from news.models import News
from .models import QuestionAnswer, SliderItem
from .services.visitors import get_visitor_stats


def qa_search(request):
    query = request.GET.get("q")
    results = []

    if query:
        results = QuestionAnswer.objects.filter(question__icontains=query)

    return render(request, "core/qa_result.html", {
        "query": query,
        "results": results
    })


def set_language(request):
    lang_code = request.POST.get('language', 'tr')
    next_url = request.POST.get('next', '/')

    try:
        target_url = translate_url(next_url, lang_code)
    except Exception:
        target_url = None

    if not target_url:
        target_url = f'/{lang_code}/' if lang_code != 'tr' else '/'

    response = HttpResponseRedirect(target_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code, path='/')
    return response


def robots_txt(request):
    """Serve search engine crawl rules dynamically with canonical Sitemap location."""
    site_url = getattr(settings, "SITE_URL", "https://www.avrasya.edu.tr").rstrip("/")
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "Disallow: /admin/",
        "Disallow: /avrasya-yonetim-paneli-2026/",
        "Disallow: /accounts/",
        "Disallow: /chat/",
        "Disallow: /adalet/",
        "Disallow: /en/adalet/",
        "Disallow: /fa/adalet/",
        "Disallow: /ar/adalet/",
        "Disallow: /ru/adalet/",
        "Disallow: /de/adalet/",
        "Disallow: /anasyafa/",
        "Disallow: /home/",
        "Disallow: /test/",
        "Disallow: /elements/",
        "Disallow: /odeme/payment/",
        "Disallow: /support/ticket/",
        "Disallow: /support/takip/",
        "Disallow: /support/taleplerim/",
        "Disallow: /support/department/",
        "Disallow: /support/staff/",
        "Disallow: /ckeditor/",
        "Disallow: /i18n/",
        "Disallow: /set-language/",
        "Disallow: /api/",
        "",
        f"Sitemap: {site_url}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain; charset=utf-8")


def live_visitors_api(request):
    """Return real-time concurrent online visitor statistics as JSON."""
    response = JsonResponse(get_visitor_stats())
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


def favicon_ico(request):
    """Serve the official Avrasya favicon.ico directly at /favicon.ico for all browsers."""
    ico_path = find_static("core/img/favicon.ico")
    if ico_path and Path(ico_path).is_file():
        data = Path(ico_path).read_bytes()
        resp = HttpResponse(data, content_type="image/x-icon")
        resp["Cache-Control"] = "public, max-age=86400"
        return resp
    return HttpResponse(status=404)


def _build_homepage_context():
    """Build cached homepage context across active language without repeating DB queries."""
    lang = translation.get_language() or getattr(settings, "LANGUAGE_CODE", "tr")
    cache_key = f"core:homepage_context:v1:{lang}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    sliders = list(SliderItem.objects.filter(is_active=True).order_by('order'))
    latest_news = list(News.objects.filter(is_published=True)[:6])

    latest_announcements = []
    total_announcements = 0
    this_month_announcements = 0
    with_files_count = 0
    recent_week_count = 0

    now = timezone.now()

    try:
        from duyurular.models import Duyuru
        published_duyurular = Duyuru.objects.filter(yayinda=True)
        latest_announcements = list(
            published_duyurular.prefetch_related('dosyalar', 'bolumler')[:4]
        )

        this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        week_ago = now - timedelta(days=7)

        stats = published_duyurular.aggregate(
            total=Count('id', distinct=True),
            this_month=Count('id', filter=Q(yayin_tarihi__gte=this_month_start), distinct=True),
            with_files=Count('id', filter=Q(dosyalar__isnull=False), distinct=True),
            recent_week=Count('id', filter=Q(yayin_tarihi__gte=week_ago), distinct=True),
        )
        total_announcements = stats['total'] or 0
        this_month_announcements = stats['this_month'] or 0
        with_files_count = stats['with_files'] or 0
        recent_week_count = stats['recent_week'] or 0
    except ImportError:
        pass

    latest_events = []
    try:
        from etkinlikler.models import Etkinlik
        latest_events = list(
            Etkinlik.objects.filter(
                yayinda=True,
                baslangic_tarihi__gte=now
            ).order_by('baslangic_tarihi')[:3]
        )
    except ImportError:
        pass

    context = {
        'sliders': sliders,
        'latest_news': latest_news,
        'latest_announcements': latest_announcements,
        'latest_events': latest_events,
        'total_announcements': total_announcements,
        'this_month_announcements': this_month_announcements,
        'with_files_count': with_files_count,
        'recent_week_count': recent_week_count,
    }
    cache.set(cache_key, context, 300)
    return context


def home(request):
    context = _build_homepage_context()
    return render(request, 'core/home.html', context)


def anasyafa(request):
    return render(request, 'core/anasyafa.html')


def index(request):
    context = _build_homepage_context()
    return render(request, 'core/main/index.html', context)


def elements(request):
    return render(request, 'core/main/elements.html')


def iletisim(request):
    return render(request, 'core/main/iletisim.html')


def test(request):
    return render(request, 'core/main/test.html')
