# app_name: yeni_medya_iletisim/views.py

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from duyurular.models import Duyuru, Bolum
from .models import YeniMedyaIletisimDuyuru, YeniMedya_Etkinlik, YeniMedyaDersProgrami
from django.utils import timezone

def etkinlik_listesi(request):
    now = timezone.now()
    
    # رویدادهای آینده (از حالا به بعد)
    gelecek_etkinlikler = YeniMedya_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__gte=now
    ).order_by('baslangic_tarihi')
    
    # رویدادهای گذشته (قبل از حالا)
    gecmis_etkinlikler = YeniMedya_Etkinlik.objects.filter(
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
    
    return render(request, 'yeni_medya_iletisim/includes/etkinlikler/list.html', context)

def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(YeniMedya_Etkinlik, slug=slug, yayinda=True)
    return render(request, 'yeni_medya_iletisim/includes/etkinlikler/detail.html', {
        'etkinlik': etkinlik
    })

def yaklasan_etkinlikler(request):
    """Yaklaşan etkinlikler (7 gün içinde)"""
    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = YeniMedya_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra]
    ).order_by('baslangic_tarihi')
    
    return render(request, 'yeni_medya_iletisim/includes/etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler
    })

def yeni_medya_iletisim_duyurulari(request):
    """نمایش تمام اطلاعیه‌های مربوط به ی‌انیمرسو رسانه و ارتباطات"""
    
    # استفاده از مدل مدیر پروکسی برای فیلتر خودکار
    duyurular = YeniMedyaIletisimDuyuru.objects.all().order_by('-yayin_tarihi')
    
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
    
    # پیدا کردن رشته ی‌انیمرسو رسانه و ارتباطات برای نمایش اطلاعات
    yeni_medya_bolumu = get_object_or_404(Bolum, kod='yeni-medya-ve-iletisim', aktif=True)
    
    context = {
        'duyurular': duyurular,
        'bolum': yeni_medya_bolumu,
        'search_query': search_query,
        'tarih_query': tarih_query,
        'toplam_duyuru': duyurular.count(),
    }
    
    return render(request, 'yeni_medya_iletisim/includes/list.html', context)

def yeni_medya_iletisim_duyuru_detay(request, slug):
    """نمایش جزییات یک اطلاعیه ی‌انیمرسو رسانه و ارتباطات"""
    duyuru = get_object_or_404(YeniMedyaIletisimDuyuru, slug=slug)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = YeniMedyaIletisimDuyuru.objects.exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    # پیدا کردن رشته ی‌انیمرسو رسانه و ارتباطات برای نمایش اطلاعات
    yeni_medya_bolumu = get_object_or_404(Bolum, kod='yeni-medya-ve-iletisim')
    
    return render(request, 'yeni_medya_iletisim/includes/detail.html', {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
        'bolum': yeni_medya_bolumu,
    })

def ders_programi(request):
    # فقط فایل‌های فعال را نمایش بده
    dosyalar = YeniMedyaDersProgrami.objects.filter(aktif=True)
    
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
    
    return render(request, 'yeni_medya_iletisim/includes/ders_programi.html', context)

# صفحات استاتیک
def yeni_medya_iletisim(request):
    return render(request, 'yeni_medya_iletisim/includes/yeni_medya_iletisim.html')

def idari_faaliyetler_2024_2025(request):
    return render(request, 'yeni_medya_iletisim/includes/idari_faaliyetler_2024_2025.html')

def diger_faaliyetler_2024_2025(request):
    return render(request, 'yeni_medya_iletisim/includes/diger_faaliyetler_2024_2025.html')

def kalite_yonetimi(request):
    return render(request, 'yeni_medya_iletisim/includes/kalite_yonetimi.html')

def toplumsal_katki(request):
    return render(request, 'yeni_medya_iletisim/includes/toplumsal_katki.html')