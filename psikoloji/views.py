from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from duyurular.models import Duyuru, Bolum
from .models import PsikolojiDuyuru, Psi_Etkinlik, DersProgramiDosya
from django.utils import timezone

def etkinlik_listesi(request):
    now = timezone.now()
    
    # رویدادهای آینده (از حالا به بعد)
    gelecek_etkinlikler = Psi_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__gte=now
    ).order_by('baslangic_tarihi')
    
    # رویدادهای گذشته (قبل از حالا)
    gecmis_etkinlikler = Psi_Etkinlik.objects.filter(
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
    
    return render(request, 'psikoloji/includes/etkinlikler/list.html', context)

def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(Psi_Etkinlik, slug=slug, yayinda=True)
    return render(request, 'psikoloji/includes/etkinlikler/detail.html', {
        'etkinlik': etkinlik
    })

def yaklasan_etkinlikler(request):
    """Yaklaşan etkinlikler (7 gün içinde)"""
    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = Psi_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra]
    ).order_by('baslangic_tarihi')
    
    return render(request, 'psikoloji/includes/etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler
    })

def psikoloji_duyurulari(request):
    """نمایش تمام اطلاعیه‌های مربوط به روانشناسی"""
    
    # استفاده از مدل مدیر پروکسی برای فیلتر خودکار
    duyurular = PsikolojiDuyuru.objects.all().order_by('-yayin_tarihi')
    
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
    
    # پیدا کردن رشته روانشناسی برای نمایش اطلاعات
    psikoloji_bolumu = get_object_or_404(Bolum, kod='psikoloji', aktif=True)
    
    context = {
        'duyurular': duyurular,
        'bolum': psikoloji_bolumu,
        'search_query': search_query,
        'tarih_query': tarih_query,
        'toplam_duyuru': duyurular.count(),
    }
    
    return render(request, 'psikoloji/includes/list.html', context)

def psikoloji_duyuru_detay(request, slug):
    """نمایش جزییات یک اطلاعیه روانشناسی"""
    duyuru = get_object_or_404(PsikolojiDuyuru, slug=slug)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = PsikolojiDuyuru.objects.exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    # پیدا کردن رشته روانشناسی برای نمایش اطلاعات
    psikoloji_bolumu = get_object_or_404(Bolum, kod='psikoloji')
    
    return render(request, 'psikoloji/includes/detail.html', {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
        'bolum': psikoloji_bolumu,
    })

def ders_programı(request):
    """صفحه برنامه درسی با فایل‌های آپلود شده"""
    
    # دریافت تمام فایل‌های فعال برنامه درسی
    dosyalar = DersProgramiDosya.objects.filter(aktif=True).order_by('sinif', 'sira')
    
    # گروه‌بندی فایل‌ها بر اساس کلاس
    siniflar = {
        '1': dosyalar.filter(sinif='1'),
        '2': dosyalar.filter(sinif='2'),
        '3': dosyalar.filter(sinif='3'),
        '4': dosyalar.filter(sinif='4'),
        '5': dosyalar.filter(sinif='5'),
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
    
    return render(request, 'psikoloji/includes/ders_programı.html', context)

# صفحات استاتیک روانشناسی
def psikoloji(request):
    return render(request, 'psikoloji/includes/psikoloji.html')

def psikoloji_tarihce(request):
    return render(request, 'psikoloji/includes/tarihce.html')

def psikoloji_misyon_visyon(request):
    return render(request, 'psikoloji/includes/misyon_visyon.html')

def psikoloji_yonetimi(request):
    return render(request, 'psikoloji/includes/psikoloji_yonetimi.html')

def idari_faaliyetler_2024_2025(request):
    return render(request, 'psikoloji/includes/idari_faaliyetler_2024_2025.html')

def idari_faaliyetler_2023_2024(request):
    return render(request, 'psikoloji/idari_faaliyetler_2023_2024.html')

def diğer_faaliyetler_2024_2025(request):
    return render(request, 'psikoloji/includes/diğer_faaliyetler_2024_2025.html')

def diğer_faaliyetler_2023_2024(request):
    return render(request, 'psikoloji/includes/diğer_faaliyetler_2023_2024.html')

def iletişim(request):
    return render(request, 'psikoloji/includes/iletisim.html')

def ogrenci_isleri(request):
    return render(request, 'psikoloji/includes/ogrenci_isleri.html')

def cift_anadal(request):
    return render(request, 'psikoloji/includes/cift_anadal.html')

def erasmus(request):
    return render(request, 'psikoloji/includes/erasmus.html')

def akreditasyon_belgesi(request):
    return render(request, 'psikoloji/includes/akreditasyon_belgesi.html')

def komisyon_sorumlular(request):
    return render(request, 'psikoloji/includes/komisyon_sorumlular.html')

def program_ogretim_amacları(request):
    return render(request, 'psikoloji/includes/program_ogretim_amacları.html')

def program_ogrenim_cıktıları(request):
    return render(request, 'psikoloji/includes/program_ogrenim_cıktıları.html')

def anketler(request):
    return render(request, 'psikoloji/includes/anketler.html')

def ders_planı(request):
    return render(request, 'psikoloji/includes/ders_planı.html')


def kalite_yonetimik(request):
    return render(request, 'psikoloji/includes/kalite_yonetimik.html')



def toplumsal_katki(request):
    return render(request, 'psikoloji/includes/toplumsal_katki.html')