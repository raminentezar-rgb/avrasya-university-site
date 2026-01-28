from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from duyurular.models import Duyuru, Bolum
from .models import HemsirelikDuyuru, Hemsirelik_Etkinlik, HemsirelikDersProgrami
from django.utils import timezone

def etkinlik_listesi(request):
    now = timezone.now()
    
    gelecek_etkinlikler = Hemsirelik_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__gte=now
    ).order_by('baslangic_tarihi')
    
    gecmis_etkinlikler = Hemsirelik_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__lt=now
    ).order_by('-baslangic_tarihi')
    
    print(f"Gelecek etkinlikler: {gelecek_etkinlikler.count()}")
    print(f"Geçmiş etkinlikler: {gecmis_etkinlikler.count()}")
    
    context = {
        'gelecek_etkinlikler': gelecek_etkinlikler,
        'gecmis_etkinlikler': gecmis_etkinlikler,
    }
    
    return render(request, 'hemsirelik/includes/etkinlikler/list.html', context)

def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(Hemsirelik_Etkinlik, slug=slug, yayinda=True)
    return render(request, 'hemsirelik/includes/etkinlikler/detail.html', {
        'etkinlik': etkinlik
    })

def yaklasan_etkinlikler(request):
    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = Hemsirelik_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra]
    ).order_by('baslangic_tarihi')
    
    return render(request, 'hemsirelik/includes/etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler
    })

def hemsirelik_duyurulari(request):
    duyurular = HemsirelikDuyuru.objects.all().order_by('-yayin_tarihi')
    
    search_query = request.GET.get('q', '')
    tarih_query = request.GET.get('tarih', '')
    
    if search_query:
        duyurular = duyurular.filter(
            Q(baslik__icontains=search_query) | 
            Q(icerik__icontains=search_query) |
            Q(ozet__icontains=search_query)
        )
    
    if tarih_query:
        duyurular = duyurular.filter(yayin_tarihi__date=tarih_query)
    
    hemsirelik_bolumu = get_object_or_404(Bolum, kod='hemsirelik', aktif=True)
    
    context = {
        'duyurular': duyurular,
        'bolum': hemsirelik_bolumu,
        'search_query': search_query,
        'tarih_query': tarih_query,
        'toplam_duyuru': duyurular.count(),
    }
    
    return render(request, 'hemsirelik/includes/list.html', context)

def hemsirelik_duyuru_detay(request, slug):
    duyuru = get_object_or_404(HemsirelikDuyuru, slug=slug)
    
    ilgili_duyurular = HemsirelikDuyuru.objects.exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    hemsirelik_bolumu = get_object_or_404(Bolum, kod='hemsirelik')
    
    return render(request, 'hemsirelik/includes/detail.html', {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
        'bolum': hemsirelik_bolumu,
    })

def ders_programi(request):
    dosyalar = HemsirelikDersProgrami.objects.filter(aktif=True)
    
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
    
    return render(request, 'hemsirelik/includes/ders_programi.html', context)

# صفحات استاتیک
def hemsirelik(request):
    return render(request, 'hemsirelik/includes/hemsirelik.html')

def idari_faaliyetler_2024_2025(request):
    return render(request, 'hemsirelik/includes/idari_faaliyetler_2024_2025.html')

def diger_faaliyetler_2024_2025(request):
    return render(request, 'hemsirelik/includes/diger_faaliyetler_2024_2025.html')

def kalite_yonetimi(request):
    return render(request, 'hemsirelik/includes/kalite_yonetimi.html')

def toplumsal_katki(request):
    return render(request, 'hemsirelik/includes/toplumsal_katki.html')