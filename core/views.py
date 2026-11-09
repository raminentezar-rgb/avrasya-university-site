from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone, translation
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.conf import settings
from news.models import News
from .models import SliderItem, QuestionAnswer


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


def _build_homepage_context():
    """ساخت کانتکست مشترک برای صفحات اصلی (home و index) با تاریخ‌های Timezone-aware"""
    sliders = SliderItem.objects.filter(is_active=True).order_by('order')
    latest_news = News.objects.filter(is_published=True)[:6]

    latest_announcements = []
    total_announcements = 0
    this_month_announcements = 0
    with_files_count = 0
    recent_week_count = 0

    now = timezone.now()

    try:
        from duyurular.models import Duyuru
        published_duyurular = Duyuru.objects.filter(yayinda=True)
        latest_announcements = published_duyurular[:4]
        total_announcements = published_duyurular.count()

        this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        this_month_announcements = published_duyurular.filter(
            yayin_tarihi__gte=this_month_start
        ).count()

        with_files_count = published_duyurular.filter(
            dosyalar__isnull=False
        ).distinct().count()

        week_ago = now - timedelta(days=7)
        recent_week_count = published_duyurular.filter(
            yayin_tarihi__gte=week_ago
        ).count()
    except ImportError:
        pass

    latest_events = []
    try:
        from etkinlikler.models import Etkinlik
        latest_events = Etkinlik.objects.filter(
            yayinda=True,
            baslangic_tarihi__gte=now
        ).order_by('baslangic_tarihi')[:3]
    except ImportError:
        pass

    return {
        'sliders': sliders,
        'latest_news': latest_news,
        'latest_announcements': latest_announcements,
        'latest_events': latest_events,
        'total_announcements': total_announcements,
        'this_month_announcements': this_month_announcements,
        'with_files_count': with_files_count,
        'recent_week_count': recent_week_count,
    }


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
