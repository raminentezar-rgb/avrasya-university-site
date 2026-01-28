from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from duyurular.models import Duyuru, Bolum
from .models import SiyasetBilimiDuyuru, SiyasetBilimi_Etkinlik, DersProgramiDosyaSiyasetBilimi
from django.utils import timezone

def etkinlik_listesi(request):
    now = timezone.now()
    
    # رویدادهای آینده (از حالا به بعد)
    gelecek_etkinlikler = SiyasetBilimi_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__gte=now
    ).order_by('baslangic_tarihi')
    
    # رویدادهای گذشته (قبل از حالا)
    gecmis_etkinlikler = SiyasetBilimi_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__lt=now
    ).order_by('-baslangic_tarihi')
    
    context = {
        'gelecek_etkinlikler': gelecek_etkinlikler,
        'gecmis_etkinlikler': gecmis_etkinlikler,
    }
    
    return render(request, 'siyaset_bilimi/etkinlikler/list.html', context)

def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(SiyasetBilimi_Etkinlik, slug=slug, yayinda=True)
    return render(request, 'siyaset_bilimi/etkinlikler/detail.html', {
        'etkinlik': etkinlik
    })

def yaklasan_etkinlikler(request):
    """Yaklaşan etkinlikler (7 gün içinde)"""
    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = SiyasetBilimi_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra]
    ).order_by('baslangic_tarihi')
    
    return render(request, 'siyaset_bilimi/etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler
    })

def siyaset_bilimi_duyurulari(request):
    """نمایش تمام اطلاعیه‌های مربوط به علوم سیاسی"""
    
    # استفاده از مدل مدیر پروکسی برای فیلتر خودکار
    duyurular = SiyasetBilimiDuyuru.objects.all().order_by('-yayin_tarihi')
    
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
    
    # پیدا کردن رشته علوم سیاسی برای نمایش اطلاعات
    siyaset_bilimi_bolumu = get_object_or_404(Bolum, kod='siyaset-bilimi', aktif=True)
    
    context = {
        'duyurular': duyurular,
        'bolum': siyaset_bilimi_bolumu,
        'search_query': search_query,
        'tarih_query': tarih_query,
        'toplam_duyuru': duyurular.count(),
    }
    
    return render(request, 'siyaset_bilimi/list.html', context)

def siyaset_bilimi_duyuru_detay(request, slug):
    """نمایش جزییات یک اطلاعیه علوم سیاسی"""
    duyuru = get_object_or_404(SiyasetBilimiDuyuru, slug=slug)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = SiyasetBilimiDuyuru.objects.exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    # پیدا کردن رشته علوم سیاسی برای نمایش اطلاعات
    siyaset_bilimi_bolumu = get_object_or_404(Bolum, kod='siyaset-bilimi')
    
    return render(request, 'siyaset_bilimi/detail.html', {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
        'bolum': siyaset_bilimi_bolumu,
    })

def ders_programi(request):
    """صفحه برنامه درسی با فایل‌های آپلود شده"""
    
    # دریافت تمام فایل‌های فعال برنامه درسی
    dosyalar = DersProgramiDosyaSiyasetBilimi.objects.filter(aktif=True).order_by('sinif', 'sira')
    
    # گروه‌بندی فایل‌ها بر اساس کلاس
    siniflar = {
        '1': dosyalar.filter(sinif='1'),
        '2': dosyalar.filter(sinif='2'),
        '3': dosyalar.filter(sinif='3'),
        '4': dosyalar.filter(sinif='4'),
        'tum': dosyalar.filter(sinif='tum'),
        'lisansustu': dosyalar.filter(sinif='lisansustu'),
    }
    
    # سال‌های تحصیلی منحصر به فرد
    akademik_yillar = dosyalar.values_list('akademik_yil', flat=True).distinct().order_by('-akademik_yil')
    
    context = {
        'siniflar': siniflar,
        'akademik_yillar': akademik_yillar,
        'toplam_dosya': dosyalar.count(),
    }
    
    return render(request, 'siyaset_bilimi/ders_programi.html', context)

# صفحات استاتیک علوم سیاسی
def siyaset_bilimi(request):
    return render(request, 'siyaset_bilimi/siyaset_bilimi.html')

def siyaset_bilimi_tarihce(request):
    return render(request, 'siyaset_bilimi/tarihce.html')

def siyaset_bilimi_misyon_visyon(request):
    return render(request, 'siyaset_bilimi/misyon_visyon.html')

def siyaset_bilimi_yonetimi(request):
    return render(request, 'siyaset_bilimi/yonetimi.html')

def idari_faaliyetler_2024_2025(request):
    return render(request, 'siyaset_bilimi/idari_faaliyetler_2024_2025.html')

def idari_faaliyetler_2023_2024(request):
    return render(request, 'siyaset_bilimi/idari_faaliyetler_2023_2024.html')

def diger_faaliyetler_2024_2025(request):
    return render(request, 'siyaset_bilimi/diger_faaliyetler_2024_2025.html')

def diger_faaliyetler_2023_2024(request):
    return render(request, 'siyaset_bilimi/diger_faaliyetler_2023_2024.html')

def iletisim(request):
    return render(request, 'siyaset_bilimi/iletisim.html')

def ogrenci_isleri(request):
    return render(request, 'siyaset_bilimi/ogrenci_isleri.html')

def cift_anadal(request):
    return render(request, 'siyaset_bilimi/cift_anadal.html')

def erasmus(request):
    return render(request, 'siyaset_bilimi/erasmus.html')

def akreditasyon_belgesi(request):
    return render(request, 'siyaset_bilimi/akreditasyon_belgesi.html')

def komisyon_sorumlular(request):
    return render(request, 'siyaset_bilimi/komisyon_sorumlular.html')

def program_ogretim_amaclari(request):
    return render(request, 'siyaset_bilimi/program_ogretim_amaclari.html')

def program_ogrenim_ciktilari(request):
    return render(request, 'siyaset_bilimi/program_ogrenim_ciktilari.html')

def anketler(request):
    return render(request, 'siyaset_bilimi/anketler.html')

def ders_plani(request):
    return render(request, 'siyaset_bilimi/ders_plani.html')