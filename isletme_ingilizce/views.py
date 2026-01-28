from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from duyurular.models import Duyuru, Bolum
from .models import IsletmeIngilizceDuyuru, IsletmeIngilizce_Etkinlik, DersProgramiDosyaIsletmeIngilizce
from django.utils import timezone

def etkinlik_listesi(request):
    now = timezone.now()
    
    # رویدادهای آینده (از حالا به بعد)
    gelecek_etkinlikler = IsletmeIngilizce_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__gte=now
    ).order_by('baslangic_tarihi')
    
    # رویدادهای گذشته (قبل از حالا)
    gecmis_etkinlikler = IsletmeIngilizce_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__lt=now
    ).order_by('-baslangic_tarihi')
    
    context = {
        'gelecek_etkinlikler': gelecek_etkinlikler,
        'gecmis_etkinlikler': gecmis_etkinlikler,
    }
    
    return render(request, 'isletme_ingilizce/etkinlikler/list.html', context)

def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(IsletmeIngilizce_Etkinlik, slug=slug, yayinda=True)
    return render(request, 'isletme_ingilizce/etkinlikler/detail.html', {
        'etkinlik': etkinlik
    })

def yaklasan_etkinlikler(request):
    """Yaklaşan etkinlikler (7 gün içinde)"""
    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = IsletmeIngilizce_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra]
    ).order_by('baslangic_tarihi')
    
    return render(request, 'isletme_ingilizce/etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler
    })

def isletme_ingilizce_duyurulari(request):
    """نمایش تمام اطلاعیه‌های مربوط به مدیریت کسب و کار انگلیسی"""
    
    # استفاده از مدل مدیر پروکسی برای فیلتر خودکار
    duyurular = IsletmeIngilizceDuyuru.objects.all().order_by('-yayin_tarihi')
    
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
    
    # پیدا کردن رشته مدیریت کسب و کار انگلیسی برای نمایش اطلاعات
    isletme_ingilizce_bolumu = get_object_or_404(Bolum, kod='isletme-ingilizce', aktif=True)
    
    context = {
        'duyurular': duyurular,
        'bolum': isletme_ingilizce_bolumu,
        'search_query': search_query,
        'tarih_query': tarih_query,
        'toplam_duyuru': duyurular.count(),
    }
    
    return render(request, 'isletme_ingilizce/list.html', context)

def isletme_ingilizce_duyuru_detay(request, slug):
    """نمایش جزییات یک اطلاعیه مدیریت کسب و کار انگلیسی"""
    duyuru = get_object_or_404(IsletmeIngilizceDuyuru, slug=slug)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = IsletmeIngilizceDuyuru.objects.exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    # پیدا کردن رشته مدیریت کسب و کار انگلیسی برای نمایش اطلاعات
    isletme_ingilizce_bolumu = get_object_or_404(Bolum, kod='isletme-ingilizce')
    
    return render(request, 'isletme_ingilizce/detail.html', {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
        'bolum': isletme_ingilizce_bolumu,
    })

def ders_programi(request):
    """صفحه برنامه درسی با فایل‌های آپلود شده"""
    
    # دریافت تمام فایل‌های فعال برنامه درسی
    dosyalar = DersProgramiDosyaIsletmeIngilizce.objects.filter(aktif=True).order_by('sinif', 'sira')
    
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
    
    return render(request, 'isletme_ingilizce/ders_programi.html', context)

# صفحات استاتیک مدیریت کسب و کار انگلیسی
def isletme_ingilizce(request):
    return render(request, 'isletme_ingilizce/isletme_ingilizce.html')

def isletme_ingilizce_tarihce(request):
    return render(request, 'isletme_ingilizce/tarihce.html')

def isletme_ingilizce_misyon_visyon(request):
    return render(request, 'isletme_ingilizce/misyon_visyon.html')

def isletme_ingilizce_yonetimi(request):
    return render(request, 'isletme_ingilizce/yonetimi.html')

def idari_faaliyetler_2024_2025(request):
    return render(request, 'isletme_ingilizce/idari_faaliyetler_2024_2025.html')

def idari_faaliyetler_2023_2024(request):
    return render(request, 'isletme_ingilizce/idari_faaliyetler_2023_2024.html')

def diger_faaliyetler_2024_2025(request):
    return render(request, 'isletme_ingilizce/diger_faaliyetler_2024_2025.html')

def diger_faaliyetler_2023_2024(request):
    return render(request, 'isletme_ingilizce/diger_faaliyetler_2023_2024.html')

def iletisim(request):
    return render(request, 'isletme_ingilizce/iletisim.html')

def ogrenci_isleri(request):
    return render(request, 'isletme_ingilizce/ogrenci_isleri.html')

def cift_anadal(request):
    return render(request, 'isletme_ingilizce/cift_anadal.html')

def erasmus(request):
    return render(request, 'isletme_ingilizce/erasmus.html')

def akreditasyon_belgesi(request):
    return render(request, 'isletme_ingilizce/akreditasyon_belgesi.html')

def komisyon_sorumlular(request):
    return render(request, 'isletme_ingilizce/komisyon_sorumlular.html')

def program_ogretim_amaclari(request):
    return render(request, 'isletme_ingilizce/program_ogretim_amaclari.html')

def program_ogrenim_ciktilari(request):
    return render(request, 'isletme_ingilizce/program_ogrenim_ciktilari.html')

def anketler(request):
    return render(request, 'isletme_ingilizce/anketler.html')

def ders_plani(request):
    return render(request, 'isletme_ingilizce/ders_plani.html')