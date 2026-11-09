import os
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.utils import timezone
from django.utils.text import get_valid_filename
from django.conf import settings
from django.contrib import messages
from .models import (
    Category, News, Announcement, Mevzuat,
    Takim, Rapor, Izleme, Dokuman, SSS
)

ALLOWED_BIDR_EXTENSIONS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar'}
MAX_BIDR_FILE_SIZE = 25 * 1024 * 1024  # 25MB
ALLOWED_BIRIM_VALUES = {
    'Enstitü',
    'Fakülte',
    'Meslek Yüksekokulu',
    'Yüksekokul',
    'Uygulama ve Araştırma Merkezi',
    'Koordinatörlük',
    'Daire Başkanlığı',
}


def home(request):
    """Koordinatörlük Varsayılan Görünümü (Hakkında)"""
    return hakkinda(request)


# 1. Hakkında
def hakkinda(request):
    """Hakkında Görünümü"""
    context = {
        'page_title': 'Hakkında',
        'active_menu': 'hakkinda',
    }
    return render(request, 'kalite_akreditasyon/hakkinda.html', context)


# 2. Duyurular
def duyurular(request):
    """Duyurular Listesi"""
    q = request.GET.get('q', '').strip()
    ann_qs = Announcement.objects.filter(is_active=True)

    if q:
        ann_qs = ann_qs.filter(
            Q(title__icontains=q) |
            Q(summary__icontains=q) |
            Q(content__icontains=q)
        )

    paginator = Paginator(ann_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'Duyurular',
        'active_menu': 'duyurular',
        'page_obj': page_obj,
        'search_query': q,
    }
    return render(request, 'kalite_akreditasyon/duyurular.html', context)


def duyuru_detail(request, slug):
    """Duyuru Detay Görünümü"""
    item = get_object_or_404(Announcement, slug=slug, is_active=True)
    Announcement.objects.filter(pk=item.pk).update(views_count=F('views_count') + 1)
    item.refresh_from_db(fields=['views_count'])

    other_announcements = Announcement.objects.filter(
        is_active=True
    ).exclude(pk=item.pk).order_by('-announcement_date')[:5]

    context = {
        'page_title': item.title,
        'active_menu': 'duyurular',
        'announcement': item,
        'other_announcements': other_announcements,
    }
    return render(request, 'kalite_akreditasyon/duyuru_detail.html', context)


# 3. Haberler
def haberler(request):
    """Haberler Listesi"""
    q = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    news_qs = News.objects.filter(
        is_published=True,
        published_at__lte=timezone.now()
    ).select_related('category')

    if q:
        news_qs = news_qs.filter(
            Q(title__icontains=q) |
            Q(summary__icontains=q) |
            Q(content__icontains=q)
        )

    if category_slug:
        news_qs = news_qs.filter(category__slug=category_slug)

    paginator = Paginator(news_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(is_active=True)

    context = {
        'page_title': 'Haberler',
        'active_menu': 'haberler',
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': q,
    }
    return render(request, 'kalite_akreditasyon/haberler.html', context)


def haber_detail(request, slug):
    """Haber Detay Görünümü"""
    item = get_object_or_404(News, slug=slug, is_published=True)
    News.objects.filter(pk=item.pk).update(views_count=F('views_count') + 1)
    item.refresh_from_db(fields=['views_count'])

    related_news = News.objects.filter(
        is_published=True
    ).exclude(pk=item.pk).order_by('-published_at')[:4]

    context = {
        'page_title': item.title,
        'active_menu': 'haberler',
        'news': item,
        'related_news': related_news,
    }
    return render(request, 'kalite_akreditasyon/haber_detail.html', context)


# 4. Mevzuat
def mevzuat(request):
    """Mevzuat Görünümü"""
    type_filter = request.GET.get('type', '').strip()
    mevzuat_qs = Mevzuat.objects.filter(is_active=True)

    if type_filter:
        mevzuat_qs = mevzuat_qs.filter(mevzuat_type=type_filter)

    mevzuat_qs = mevzuat_qs.order_by('order', 'title')

    context = {
        'page_title': 'Mevzuat',
        'active_menu': 'mevzuat',
        'mevzuat_list': mevzuat_qs,
        'mevzuat_types': Mevzuat.MEVZUAT_TYPES,
        'current_type': type_filter,
    }
    return render(request, 'kalite_akreditasyon/mevzuat.html', context)


# 5. Takvim
def takvim(request):
    """Takvim Ana Sayfası - İki Sekmeli Yapı (Komisyon Çalışma Takvimi & Tamamlanan Çalışmalar)"""
    context = {
        'page_title': 'Takvim',
        'active_menu': 'takvim',
        'active_tab': 'tab-komisyon-takvim',
    }
    return render(request, 'kalite_akreditasyon/takvim.html', context)


def komisyon_calisma_takvimi(request):
    """Komisyon Çalışma Takvimi Görünümü"""
    context = {
        'page_title': 'Komisyon Çalışma Takvimi',
        'active_menu': 'takvim',
        'active_tab': 'tab-komisyon-takvim',
    }
    return render(request, 'kalite_akreditasyon/takvim.html', context)


def tamamlanan_calismalar(request):
    """Tamamlanan Çalışmalar Görünümü"""
    context = {
        'page_title': 'Tamamlanan Çalışmalar',
        'active_menu': 'takvim',
        'active_tab': 'tab-tamamlanan-calismalar',
    }
    return render(request, 'kalite_akreditasyon/takvim.html', context)


# Takım (Mevcut yapı uyumluluğu için)
def takim(request):
    """Takım Görünümü"""
    members = Takim.objects.filter(is_active=True).order_by('order', 'name')
    context = {
        'page_title': 'Takım',
        'active_menu': 'takim',
        'members': members,
    }
    return render(request, 'kalite_akreditasyon/takim.html', context)


# 6. Raporlar
def raporlar(request):
    """Raporlar Görünümü - Kurum İç Değerlendirme Raporları"""
    context = {
        'page_title': 'İç Değerlendirme Raporları',
        'active_menu': 'raporlar',
    }
    return render(request, 'kalite_akreditasyon/raporlar.html', context)


def kurum_ic_degerlendirme_raporlari(request):
    """Kurum İç Değerlendirme Raporları Görünümü"""
    return raporlar(request)


# 7. İzleme
def izleme(request):
    """İzleme Ana Sayfası - 4 Sekmeli Yapı (BİDR Yükleme, Paydaş Analizi, Dış Değerlendirme, Süreç Değerlendirme)"""
    submitted = False
    error_message = None

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        birim = request.POST.get('birim', '').strip()
        uploaded_file = request.FILES.get('rapor_dosyasi')

        if not uploaded_file or not name or not email or birim not in ALLOWED_BIRIM_VALUES:
            error_message = 'Lütfen tüm zorunlu alanları geçerli bilgilerle doldurunuz.'
        else:
            original_name = os.path.basename(uploaded_file.name)
            _, ext = os.path.splitext(original_name)
            ext = ext.lower()

            if ext not in ALLOWED_BIDR_EXTENSIONS:
                error_message = 'Sadece PDF, Word (.doc, .docx), Excel (.xls, .xlsx) veya Arşiv (.zip, .rar) dosyaları yüklenebilir.'
            elif uploaded_file.size > MAX_BIDR_FILE_SIZE:
                error_message = 'Dosya boyutu en fazla 25 MB olabilir.'
            else:
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'kalite_akreditasyon', 'bidr_yuklemeleri')
                os.makedirs(upload_dir, exist_ok=True)
                timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
                safe_birim = get_valid_filename(birim)[:40]
                safe_name = get_valid_filename(name)[:50]
                safe_orig = get_valid_filename(original_name)[:100]
                safe_filename = f"{timestamp}_{safe_birim}_{safe_name}_{safe_orig}"
                file_path = os.path.abspath(os.path.join(upload_dir, safe_filename))

                # جلوگیری کامل از Path Traversal
                if not file_path.startswith(os.path.abspath(upload_dir) + os.sep):
                    error_message = 'Geçersiz dosya adı.'
                else:
                    with open(file_path, 'wb+') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)
                    messages.success(request, 'Birim İç Değerlendirme Raporunuz başarıyla iletilmiştir.')
                    submitted = True

        if error_message:
            messages.error(request, error_message)

    context = {
        'page_title': 'İzleme',
        'active_menu': 'izleme',
        'active_tab': 'tab-bidr-yukleme',
        'submitted': submitted,
        'error_message': error_message,
    }
    return render(request, 'kalite_akreditasyon/izleme.html', context)


def bidr_yukleme_sistemi(request):
    """BİDR Yükleme Sistemi Görünümü"""
    return izleme(request)


def paydas_analizi_sonuclari(request):
    """Paydaş Analizi Sonuçları Görünümü"""
    context = {
        'page_title': 'Paydaş Analizi Sonuçları',
        'active_menu': 'izleme',
        'active_tab': 'tab-paydas-analizi',
    }
    return render(request, 'kalite_akreditasyon/izleme.html', context)


def dis_degerlendirme(request):
    """Dış Değerlendirme Görünümü"""
    context = {
        'page_title': 'Dış Değerlendirme',
        'active_menu': 'izleme',
        'active_tab': 'tab-dis-degerlendirme',
    }
    return render(request, 'kalite_akreditasyon/izleme.html', context)


def surec_degerlendirme(request):
    """Süreç Değerlendirme Görünümü"""
    context = {
        'page_title': 'Süreç Değerlendirme',
        'active_menu': 'izleme',
        'active_tab': 'tab-surec-degerlendirme',
    }
    return render(request, 'kalite_akreditasyon/izleme.html', context)


# 8. Doküman
def dokuman(request):
    """Doküman Görünümü"""
    type_filter = request.GET.get('type', '').strip()
    dokuman_qs = Dokuman.objects.filter(is_active=True)

    if type_filter:
        dokuman_qs = dokuman_qs.filter(dokuman_type=type_filter)

    dokuman_qs = dokuman_qs.order_by('dokuman_type', 'order', 'title')

    context = {
        'page_title': 'Döküman',
        'active_menu': 'dokuman',
        'dokuman_list': dokuman_qs,
        'dokuman_types': Dokuman.DOKUMAN_TYPES,
        'current_type': type_filter,
    }
    return render(request, 'kalite_akreditasyon/dokuman.html', context)


# 9. S.S.S
def sss(request):
    """Sıkça Sorulan Sorular Görünümü"""
    faq_list = SSS.objects.filter(is_active=True).order_by('order', 'question')
    context = {
        'page_title': 'Sık Sorulan Sorular',
        'active_menu': 'sss',
        'faq_list': faq_list,
    }
    return render(request, 'kalite_akreditasyon/sss.html', context)
