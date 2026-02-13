# app_name: adalet/views.py

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from duyurular.models import Duyuru, Bolum
from .models import AdaletDuyuru, AdaletEtkinlik, AdaletDersProgrami
from django.utils import timezone

def etkinlik_listesi(request):
    now = timezone.now()
    
    # رویدادهای آینده (از حالا به بعد)
    gelecek_etkinlikler = AdaletEtkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__gte=now
    ).order_by('baslangic_tarihi')
    
    # رویدادهای گذشته (قبل از حالا)
    gecmis_etkinlikler = AdaletEtkinlik.objects.filter(
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
    
    return render(request, 'adalet/includes/etkinlikler/list.html', context)

def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(AdaletEtkinlik, slug=slug, yayinda=True)
    return render(request, 'adalet/includes/etkinlikler/detail.html', {
        'etkinlik': etkinlik
    })

def yaklasan_etkinlikler(request):
    """Yaklaşan etkinlikler (7 gün içinde)"""
    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = AdaletEtkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra]
    ).order_by('baslangic_tarihi')
    
    return render(request, 'adalet/includes/etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler
    })

def adalet_duyurulari(request):
    """نمایش تمام اطلاعیه‌های مربوط به رشته حقوق و عدالت کیفری"""
    
    # استفاده از مدل مدیر پروکسی برای فیلتر خودکار
    duyurular = AdaletDuyuru.objects.all().order_by('-yayin_tarihi')
    
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
    
    # پیدا کردن رشته حقوق و عدالت کیفری برای نمایش اطلاعات
    adalet_bolumu = get_object_or_404(Bolum, kod='adalet', aktif=True)
    
    context = {
        'duyurular': duyurular,
        'bolum': adalet_bolumu,
        'search_query': search_query,
        'tarih_query': tarih_query,
        'toplam_duyuru': duyurular.count(),
    }
    
    return render(request, 'adalet/includes/list.html', context)

def adalet_duyuru_detay(request, slug):
    """نمایش جزییات یک اطلاعیه رشته حقوق و عدالت کیفری"""
    duyuru = get_object_or_404(AdaletDuyuru, slug=slug)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = AdaletDuyuru.objects.exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    # پیدا کردن رشته حقوق و عدالت کیفری برای نمایش اطلاعات
    adalet_bolumu = get_object_or_404(Bolum, kod='adalet', aktif=True)
    
    return render(request, 'adalet/includes/detail.html', {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
        'bolum': adalet_bolumu,
    })

def ders_programi(request):
    # فقط فایل‌های فعال را نمایش بده
    dosyalar = AdaletDersProgrami.objects.filter(aktif=True)
    
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
    
    return render(request, 'adalet/includes/ders_programi.html', context)

# صفحات استاتیک
def adalet_bolumu(request):
    return render(request, 'adalet/includes/adalet.html')

def idari_faaliyetler_2024_2025(request):
    return render(request, 'adalet/includes/idari_faaliyetler_2024_2025.html')

def diger_faaliyetler_2024_2025(request):
    return render(request, 'adalet/includes/diger_faaliyetler_2024_2025.html')

def kalite_yonetimi(request):
    return render(request, 'adalet/includes/kalite_yonetimi.html')

def toplumsal_katki(request):
    return render(request, 'adalet/includes/toplumsal_katki.html')