# app_name: ic_mimarlik/views.py

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from duyurular.models import Duyuru, Bolum
from .models import IcMimarlikDuyuru, IcMimarlikEtkinlik, IcMimarlikDersProgrami
from django.utils import timezone


def etkinlik_listesi(request):
    now = timezone.now()
    
    # Upcoming events (from now onwards)
    gelecek_etkinlikler = IcMimarlikEtkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__gte=now
    ).order_by('baslangic_tarihi')
    
    # Past events (before now)
    gecmis_etkinlikler = IcMimarlikEtkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__lt=now
    ).order_by('-baslangic_tarihi')
    
    # Debug - print event counts
    print(f"Gelecek etkinlikler: {gelecek_etkinlikler.count()}")
    print(f"Geçmiş etkinlikler: {gecmis_etkinlikler.count()}")
    
    context = {
        'gelecek_etkinlikler': gelecek_etkinlikler,
        'gecmis_etkinlikler': gecmis_etkinlikler,
    }
    
    return render(request, 'ic_mimarlik/includes/etkinlikler/list.html', context)


def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(IcMimarlikEtkinlik, slug=slug, yayinda=True)
    return render(request, 'ic_mimarlik/includes/etkinlikler/detail.html', {
        'etkinlik': etkinlik
    })


def yaklasan_etkinlikler(request):
    """Upcoming events (within 7 days)"""
    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = IcMimarlikEtkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra]
    ).order_by('baslangic_tarihi')
    
    return render(request, 'ic_mimarlik/includes/etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler
    })


def ic_mimarlik_duyurulari(request):
    """Display all announcements related to İç Mimarlık department"""
    
    # Using proxy model manager for automatic filtering
    duyurular = IcMimarlikDuyuru.objects.all().order_by('-yayin_tarihi')
    
    # Search parameters
    search_query = request.GET.get('q', '')
    tarih_query = request.GET.get('tarih', '')
    
    # Apply filters
    if search_query:
        duyurular = duyurular.filter(
            Q(baslik__icontains=search_query) | 
            Q(icerik__icontains=search_query) |
            Q(ozet__icontains=search_query)
        )
    
    if tarih_query:
        duyurular = duyurular.filter(yayin_tarihi__date=tarih_query)
    
    # Get İç Mimarlık department
    ic_mimarlik_bolumu = get_object_or_404(Bolum, kod='ic_mimarlik', aktif=True)
    
    context = {
        'duyurular': duyurular,
        'bolum': ic_mimarlik_bolumu,
        'search_query': search_query,
        'tarih_query': tarih_query,
        'toplam_duyuru': duyurular.count(),
    }
    
    return render(request, 'ic_mimarlik/includes/list.html', context)


def ic_mimarlik_duyuru_detay(request, slug):
    """Display details of an İç Mimarlık department announcement"""
    duyuru = get_object_or_404(IcMimarlikDuyuru, slug=slug)
    
    # Related announcements
    ilgili_duyurular = IcMimarlikDuyuru.objects.exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    # Get İç Mimarlık department
    ic_mimarlik_bolumu = get_object_or_404(Bolum, kod='ic_mimarlik', aktif=True)
    
    return render(request, 'ic_mimarlik/includes/detail.html', {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
        'bolum': ic_mimarlik_bolumu,
    })


def ders_programi(request):
    # Show only active files
    dosyalar = IcMimarlikDersProgrami.objects.filter(aktif=True)
    
    # Group by class
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
    
    return render(request, 'ic_mimarlik/includes/ders_programi.html', context)


# Static pages
def ic_mimarlik_bolumu(request):
    return render(request, 'ic_mimarlik/includes/ic_mimarlik.html')


def idari_faaliyetler_2024_2025(request):
    return render(request, 'ic_mimarlik/includes/idari_faaliyetler_2024_2025.html')


def diger_faaliyetler_2024_2025(request):
    return render(request, 'ic_mimarlik/includes/diger_faaliyetler_2024_2025.html')


def kalite_yonetimi(request):
    return render(request, 'ic_mimarlik/includes/kalite_yonetimi.html')


def toplumsal_katki(request):
    return render(request, 'ic_mimarlik/includes/toplumsal_katki.html')