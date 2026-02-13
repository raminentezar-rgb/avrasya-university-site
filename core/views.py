from django.shortcuts import render
from news.models import News
from datetime import datetime, timedelta
from django.utils import timezone
from .models import SliderItem  # اضافه کردن این خط
# core/views.py
from django.utils import translation
from django.http import HttpResponseRedirect
from django.urls import translate_url
from django.conf import settings


from django.shortcuts import render
from .models import QuestionAnswer

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
    lang_code = request.POST.get('language', request.GET.get('language'))
    next_url = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', '/')))
    
    if lang_code in dict(settings.LANGUAGES):
        translation.activate(lang_code)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        return response
    
    return HttpResponseRedirect(next_url)






def home(request):
    # Get active sliders - اضافه کردن این بخش
    sliders = SliderItem.objects.filter(is_active=True).order_by('order')
    
    # Get latest news
    latest_news = News.objects.filter(is_published=True)[:6]
    
    # Initialize announcement variables with default values
    latest_announcements = []
    total_announcements = 0
    this_month_announcements = 0
    with_files_count = 0
    recent_week_count = 0
    
    # Try to get announcements if the app exists
    try:
        from duyurular.models import Duyuru
        latest_announcements = Duyuru.objects.filter(yayinda=True)[:4]
        total_announcements = Duyuru.objects.filter(yayinda=True).count()
        
        # This month announcements
        today = datetime.now()
        this_month_start = today.replace(day=1)
        this_month_announcements = Duyuru.objects.filter(
            yayinda=True,
            yayin_tarihi__gte=this_month_start
        ).count()
        
        # Announcements with files - اصلاح شده
        with_files_count = Duyuru.objects.filter(
            yayinda=True,
            dosyalar__isnull=False  # فقط آنهایی که حداقل یک فایل دارند
        ).distinct().count()
        
        # Recent week announcements
        week_ago = today - timedelta(days=7)
        recent_week_count = Duyuru.objects.filter(
            yayinda=True,
            yayin_tarihi__gte=week_ago
        ).count()
        
    except ImportError:
        # If duyurular app is not available, use empty values
        pass
    
    # Get latest events
    latest_events = []
    try:
        from etkinlikler.models import Etkinlik
        latest_events = Etkinlik.objects.filter(
            yayinda=True,
            baslangic_tarihi__gte=timezone.now()
        ).order_by('baslangic_tarihi')[:3]
    except ImportError:
        # If etkinlikler app is not available, use empty values
        pass
    
    context = {
        'sliders': sliders,  # اضافه کردن این خط
        'latest_news': latest_news,
        'latest_announcements': latest_announcements,
        'latest_events': latest_events,
        'total_announcements': total_announcements,
        'this_month_announcements': this_month_announcements,
        'with_files_count': with_files_count,
        'recent_week_count': recent_week_count,
    }
    
    return render(request, 'core/home.html', context)





def anasyafa(request):
    return render(request, 'core/anasyafa.html')





def index(request):
    # فعال کردن زبان ترکی به صورت explicit
    current_lang = translation.get_language()
    
    if not current_lang or current_lang.startswith('en'):
        translation.activate('tr')
        current_lang = 'tr'
    
    # Get latest news
    latest_news = News.objects.filter(is_published=True)[:6]
    
    # Initialize announcement variables with default values
    latest_announcements = []
    total_announcements = 0
    this_month_announcements = 0
    with_files_count = 0
    recent_week_count = 0
    
    # Try to get announcements if the app exists
    try:
        from duyurular.models import Duyuru
        latest_announcements = Duyuru.objects.filter(yayinda=True)[:4]
        total_announcements = Duyuru.objects.filter(yayinda=True).count()
        
        # This month announcements
        today = datetime.now()
        this_month_start = today.replace(day=1)
        this_month_announcements = Duyuru.objects.filter(
            yayinda=True,
            yayin_tarihi__gte=this_month_start
        ).count()
        
        # Announcements with files
        with_files_count = Duyuru.objects.filter(
            yayinda=True,
            dosyalar__isnull=False
        ).distinct().count()
        
        # Recent week announcements
        week_ago = today - timedelta(days=7)
        recent_week_count = Duyuru.objects.filter(
            yayinda=True,
            yayin_tarihi__gte=week_ago
        ).count()
        
    except ImportError:
        pass
    
    # Get latest events
    latest_events = []
    try:
        from etkinlikler.models import Etkinlik
        latest_events = Etkinlik.objects.filter(
            yayinda=True,
            baslangic_tarihi__gte=timezone.now()
        ).order_by('baslangic_tarihi')[:3]
    except ImportError:
        pass
    
    context = {
        'latest_news': latest_news,
        'latest_announcements': latest_announcements,
        'latest_events': latest_events,
        'total_announcements': total_announcements,
        'this_month_announcements': this_month_announcements,
        'with_files_count': with_files_count,
        'recent_week_count': recent_week_count,
        'LANGUAGE_CODE': current_lang,
        'CURRENT_LANG': current_lang,
    }
    
    return render(request, 'core/main/index.html', context)





def elements(request):
    return render(request, 'core/main/elements.html')


def iletisim(request):
    return render(request, 'core/main/iletisim.html')

def test(request):
    return render(request, 'core/main/test.html')
    