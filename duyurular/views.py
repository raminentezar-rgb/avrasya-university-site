from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import Duyuru, Bolum

def duyuru_listesi(request):
    duyurular = Duyuru.objects.filter(yayinda=True)
    
    # دریافت پارامترهای جستجو و فیلتر
    search_query = request.GET.get('q', '')
    tarih_query = request.GET.get('tarih', '')
    fakulte_filter = request.GET.get('fakulte', '')
    bolum_filter = request.GET.get('bolum', '')
    
    # اعمال فیلترهای جستجو
    if search_query:
        duyurular = duyurular.filter(
            Q(baslik__icontains=search_query) | 
            Q(icerik__icontains=search_query) |
            Q(ozet__icontains=search_query)
        )
    
    if tarih_query:
        duyurular = duyurular.filter(yayin_tarihi__date=tarih_query)
    
    if fakulte_filter:
        duyurular = duyurular.filter(fakulte=fakulte_filter)
    
    if bolum_filter:
        duyurular = duyurular.filter(bolumler__kod=bolum_filter)
    
    # محاسبه آمار دانشکده‌ها
    fakulte_istatistikleri = {}
    for fakulte_kodu, fakulte_adi in Duyuru.FAKULTE_CHOICES:
        sayi = Duyuru.objects.filter(fakulte=fakulte_kodu, yayinda=True).count()
        fakulte_istatistikleri[fakulte_kodu] = {
            'adi': fakulte_adi,
            'sayi': sayi
        }
    
    # آمار رشته‌ها و پیدا کردن نام رشته فیلتر شده
    bolum_istatistikleri = {}
    aktif_bolumler = Bolum.objects.filter(aktif=True)
    bolum_adi = None
    
    for bolum in aktif_bolumler:
        sayi = Duyuru.objects.filter(bolumler=bolum, yayinda=True).count()
        bolum_istatistikleri[bolum.kod] = {
            'adi': bolum.ad,
            'sayi': sayi,
            'fakulte': bolum.fakulte
        }
        if bolum.kod == bolum_filter:
            bolum_adi = bolum.ad
    
    # آمار کلی
    toplam_duyuru = Duyuru.objects.filter(yayinda=True).count()
    
    context = {
        'duyurular': duyurular,
        'search_query': search_query,
        'tarih_query': tarih_query,
        'fakulte_filter': fakulte_filter,
        'bolum_filter': bolum_filter,
        'bolum_adi': bolum_adi,  # اضافه کردن این خط
        'fakulte_choices': Duyuru.FAKULTE_CHOICES,
        'fakulte_istatistikleri': fakulte_istatistikleri,
        'bolum_istatistikleri': bolum_istatistikleri,
        'toplam_duyuru': toplam_duyuru,
        'aktif_bolumler': aktif_bolumler,
    }
    
    return render(request, 'duyurular/list.html', context)

def duyuru_detay(request, slug):
    duyuru = get_object_or_404(Duyuru, slug=slug, yayinda=True)
    
    # اطلاعیه‌های مرتبط از همان دانشکده و رشته‌ها
    ilgili_duyurular = Duyuru.objects.filter(
        Q(fakulte=duyuru.fakulte) | Q(bolumler__in=duyuru.bolumler.all()),
        yayinda=True
    ).exclude(id=duyuru.id).distinct().order_by('-yayin_tarihi')[:3]
    
    return render(request, 'duyurular/detail.html', {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    })

def fakulte_duyurulari(request, fakulte_kodu):
    """نمایش اطلاعیه‌های یک دانشکده خاص"""
    fakulte_adi = dict(Duyuru.FAKULTE_CHOICES).get(fakulte_kodu, 'Bilinmeyen')
    duyurular = Duyuru.objects.filter(fakulte=fakulte_kodu, yayinda=True)
    
    # رشته‌های مربوط به این دانشکده
    bolumler = Bolum.objects.filter(fakulte=fakulte_kodu, aktif=True)
    
    # استفاده از متد get_fakulte_adi از مدل
    duyuru_instance = Duyuru()
    fakulte_tam_adi = duyuru_instance.get_fakulte_adi()
    
    return render(request, 'duyurular/fakulte_list.html', {
        'duyurular': duyurular,
        'fakulte_kodu': fakulte_kodu,
        'fakulte_adi': fakulte_adi,
        'fakulte_tam_adi': fakulte_tam_adi,
        'bolumler': bolumler,
    })

def bolum_duyurulari(request, bolum_kodu):
    """نمایش اطلاعیه‌های یک رشته خاص"""
    bolum = get_object_or_404(Bolum, kod=bolum_kodu, aktif=True)
    duyurular = Duyuru.objects.filter(bolumler=bolum, yayinda=True)
    
    return render(request, 'duyurular/bolum_list.html', {
        'duyurular': duyurular,
        'bolum': bolum,
        'fakulte_adi': bolum.get_fakulte_display(),
    })