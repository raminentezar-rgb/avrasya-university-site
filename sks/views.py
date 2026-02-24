from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import News, Announcement, Category
from .forms import NewsSearchForm


def news_list(request):
    """
    Haber listesi görünümü - filtreleme ve arama özellikli
    """
    # Filtre parametrelerini al
    form = NewsSearchForm(request.GET or None)
    
    # Temel sorgu
    news_queryset = News.objects.filter(
        is_published=True,
        published_at__lte=timezone.now()
    ).select_related('category')
    
    # Filtreleri uygula
    if form.is_valid():
        q = form.cleaned_data.get('q')
        news_type = form.cleaned_data.get('news_type')
        category = form.cleaned_data.get('category')
        
        if q:
            news_queryset = news_queryset.filter(
                Q(title__icontains=q) | 
                Q(summary__icontains=q) | 
                Q(content__icontains=q)
            )
        
        if news_type:
            news_queryset = news_queryset.filter(news_type=news_type)
        
        if category:
            news_queryset = news_queryset.filter(category=category)
    
    # Sayfalama
    paginator = Paginator(news_queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Aktif duyuruları al
    announcements = Announcement.objects.filter(
        is_active=True
    ).order_by('-is_important', '-announcement_date')[:5]
    
    # Filtre için kategorileri al
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'announcements': announcements,
        'categories': categories,
        'news_types': News.NEWS_TYPE_CHOICES,
        'featured_news': news_queryset.filter(is_featured=True)[:3],
    }
    
    return render(request, 'sks/news_list.html', context)


def news_detail(request, slug):
    """
    Haber detay görünümü
    """
    news = get_object_or_404(
        News, 
        slug=slug,
        is_published=True,
        published_at__lte=timezone.now()
    )
    
    # Görüntülenme sayısını artır
    news.views_count += 1
    news.save(update_fields=['views_count'])
    
    # İlgili haberler
    related_news = News.objects.filter(
        is_published=True,
        published_at__lte=timezone.now()
    ).exclude(id=news.id)
    
    if news.category:
        related_news = related_news.filter(category=news.category)
    
    related_news = related_news[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    
    return render(request, 'sks/news_detail.html', context)


def news_by_category(request, category_slug):
    """
    Kategoriye göre haber listesi
    """
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    
    news_queryset = News.objects.filter(
        category=category,
        is_published=True,
        published_at__lte=timezone.now()
    )
    
    paginator = Paginator(news_queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'sks/news_by_category.html', context)


def announcements_list(request):
    """
    Tüm duyurular listesi
    """
    announcements = Announcement.objects.filter(
        is_active=True
    ).order_by('-is_important', '-announcement_date')
    
    paginator = Paginator(announcements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'sks/announcements_list.html', context)


def announcement_detail(request, slug):
    """
    Duyuru detay görünümü
    """
    announcement = get_object_or_404(
        Announcement, 
        slug=slug,
        is_active=True
    )
    
    # Diğer duyurular
    other_announcements = Announcement.objects.filter(
        is_active=True
    ).exclude(id=announcement.id)[:5]
    
    context = {
        'announcement': announcement,
        'other_announcements': other_announcements,
    }
    
    return render(request, 'sks/announcement_detail.html', context)


def get_latest_news_announcements():
    """
    Ana sayfa için en son haber ve duyuruları al
    """
    # Haberler
    latest_news_query = News.objects.filter(
        is_published=True,
        published_at__lte=timezone.now()
    ).select_related('category').order_by('-published_at')
    
    # Öne çıkan haberi bul
    featured_news = latest_news_query.filter(is_featured=True).first()
    if not featured_news:
        featured_news = latest_news_query.first()
    
    # Son 4 haberi al
    latest_news = latest_news_query[:4]
    
    # Duyurular - summary yerine content kullan
    announcements = Announcement.objects.filter(
        is_active=True
    ).order_by('-is_important', '-announcement_date')[:4]
    
    return {
        'latest_news': latest_news,
        'featured_news': featured_news,
        'announcements': announcements,
    }


def sks(request):
    """
    SKS ana sayfa - en son haber ve duyurular
    """
    news_data = get_latest_news_announcements()
    
    context = {
        'latest_news': news_data['latest_news'],
        'featured_news': news_data['featured_news'],
        'announcements': news_data['announcements'],
    }
    
    return render(request, 'sks/index.html', context)