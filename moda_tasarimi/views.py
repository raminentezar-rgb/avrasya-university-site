# app_name: moda_tasarimi/views.py

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from duyurular.models import Duyuru, Bolum
from .models import ModaTasarimiDuyuru, ModaTasarimiEtkinlik, ModaTasarimiDersProgrami
from django.utils import timezone

def etkinlik_listesi(request):
    now = timezone.now()
    
    # رویدادهای آینده (از حالا به بعد)
    gelecek_etkinlikler = ModaTasarimiEtkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__gte=now
    ).order_by('baslangic_tarihi')
    
    # رویدادهای گذشته (قبل از حالا)
    gecmis_etkinlikler = ModaTasarimiEtkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__lt=now
    ).order_by('-baslangic_tarihi')
    
    # برای دیباگ - چاپ تعداد رویدادها
    print(f"Gelecek etkinlikler: {gelecek_etkinlikler.count()}")
    print(f"Geçmiş etkinlikler: {gecmis_etkinlikler.count()}")
    
    context = {
        'gelecek_etkinlikler': gelecek_etkinlikler,
        'gecmis_etkinlikler': gecmis_etkinlikler,
    }
    
    return render(request, 'moda_tasarimi/includes/etkinlikler/list.html', context)

def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(ModaTasarimiEtkinlik, slug=slug, yayinda=True)
    return render(request, 'moda_tasarimi/includes/etkinlikler/detail.html', {
        'etkinlik': etkinlik
    })

def yaklasan_etkinlikler(request):
    """Yaklaşan etkinlikler (7 gün içinde)"""
    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = ModaTasarimiEtkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra]
    ).order_by('baslangic_tarihi')
    
    return render(request, 'moda_tasarimi/includes/etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler
    })

def moda_tasarimi_duyurulari(request):
    """نمایش تمام اطلاعیه‌های مربوط به رشته مد طراحی"""
    
    # استفاده از مدل مدیر پروکسی برای فیلتر خودکار
    duyurular = ModaTasarimiDuyuru.objects.all().order_by('-yayin_tarihi')
    
    # پارامترهای جستجو
    search_query = request.GET.get('q', '')
    tarih_query = request.GET.get('tarih', '')
    
    # اعمال فیلترها
    if search_query:
        duyurular = duyurular.filter(
            Q(baslik__icontains=search_query) | 
            Q(icerik__icontains=search_query) |
            Q(ozet__icontains=search_query)
        )
    
    if tarih_query:
        duyurular = duyurular.filter(yayin_tarihi__date=tarih_query)
    
    # پیدا کردن رشته مد طراحی برای نمایش اطلاعات
    moda_tasarimi_bolumu = get_object_or_404(Bolum, kod='moda_tasarimi', aktif=True)
    
    context = {
        'duyurular': duyurular,
        'bolum': moda_tasarimi_bolumu,
        'search_query': search_query,
        'tarih_query': tarih_query,
        'toplam_duyuru': duyurular.count(),
    }
    
    return render(request, 'moda_tasarimi/includes/list.html', context)

def moda_tasarimi_duyuru_detay(request, slug):
    """نمایش جزییات یک اطلاعیه رشته مد طراحی"""
    duyuru = get_object_or_404(ModaTasarimiDuyuru, slug=slug)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = ModaTasarimiDuyuru.objects.exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    # پیدا کردن رشته مد طراحی برای نمایش اطلاعات
    moda_tasarimi_bolumu = get_object_or_404(Bolum, kod='moda_tasarimi', aktif=True)
    
    return render(request, 'moda_tasarimi/includes/detail.html', {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
        'bolum': moda_tasarimi_bolumu,
    })

def ders_programi(request):
    # فقط فایل‌های فعال را نمایش بده
    dosyalar = ModaTasarimiDersProgrami.objects.filter(aktif=True)
    
    # گروه‌بندی بر اساس کلاس
    gruplar = {}
    for dosya in dosyalar:
        sinif = dosya.get_sinif_display()
        if sinif not in gruplar:
            gruplar[sinif] = []
        gruplar[sinif].append(dosya)
    
    context = {
        'gruplar': gruplar,
        'toplam_dosya': dosyalar.count()
    }
    
    return render(request, 'moda_tasarimi/includes/ders_programi.html', context)

# صفحات استاتیک
def moda_tasarimi_bolumu(request):
    return render(request, 'moda_tasarimi/includes/moda_tasarimi.html')

def idari_faaliyetler_2024_2025(request):
    return render(request, 'moda_tasarimi/includes/idari_faaliyetler_2024_2025.html')

def diger_faaliyetler_2024_2025(request):
    return render(request, 'moda_tasarimi/includes/diger_faaliyetler_2024_2025.html')

def kalite_yonetimi(request):
    return render(request, 'moda_tasarimi/includes/kalite_yonetimi.html')

def toplumsal_katki(request):
    return render(request, 'moda_tasarimi/includes/toplumsal_katki.html')