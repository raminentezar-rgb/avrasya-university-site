from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Etkinlik

def etkinlik_listesi(request):
    # Get search query and sort parameter
    search_query = request.GET.get('q', '')
    sort_param = request.GET.get('sort', 'newest')
    
    # Base queryset
    etkinlikler = Etkinlik.objects.filter(yayinda=True)
    
    # Apply search filter if query exists
    if search_query:
        etkinlikler = etkinlikler.filter(
            Q(baslik__icontains=search_query) |
            Q(kisa_aciklama__icontains=search_query) |
            Q(detayli_aciklama__icontains=search_query) |
            Q(yer__icontains=search_query) |
            Q(etkinlik_turu__icontains=search_query)
        )
    
    # Separate upcoming and past events
    simdi = timezone.now()
    gelecek_etkinlikler = etkinlikler.filter(baslangic_tarihi__gte=simdi)
    gecmis_etkinlikler = etkinlikler.filter(baslangic_tarihi__lt=simdi)
    
    # Apply sorting
    if sort_param == 'newest':
        gelecek_etkinlikler = gelecek_etkinlikler.order_by('baslangic_tarihi')
        gecmis_etkinlikler = gecmis_etkinlikler.order_by('-baslangic_tarihi')
    elif sort_param == 'oldest':
        gelecek_etkinlikler = gelecek_etkinlikler.order_by('-baslangic_tarihi')
        gecmis_etkinlikler = gecmis_etkinlikler.order_by('baslangic_tarihi')
    elif sort_param == 'upcoming':
        gelecek_etkinlikler = gelecek_etkinlikler.order_by('baslangic_tarihi')
        gecmis_etkinlikler = gecmis_etkinlikler.order_by('-baslangic_tarihi')
    else:
        # Default sorting
        gelecek_etkinlikler = gelecek_etkinlikler.order_by('baslangic_tarihi')
        gecmis_etkinlikler = gecmis_etkinlikler.order_by('-baslangic_tarihi')
    
    return render(request, 'etkinlikler/list.html', {
        'gelecek_etkinlikler': gelecek_etkinlikler,
        'gecmis_etkinlikler': gecmis_etkinlikler,
        'search_query': search_query,
        'sort_param': sort_param,
    })

def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(Etkinlik, slug=slug, yayinda=True)
    return render(request, 'etkinlikler/detail.html', {
        'etkinlik': etkinlik
    })

def yaklasan_etkinlikler(request):
    """Yaklaşan etkinlikler (7 gün içinde)"""
    # Get search query
    search_query = request.GET.get('q', '')
    
    # Base queryset for upcoming events
    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra]
    )
    
    # Apply search filter if query exists
    if search_query:
        etkinlikler = etkinlikler.filter(
            Q(baslik__icontains=search_query) |
            Q(kisa_aciklama__icontains=search_query) |
            Q(detayli_aciklama__icontains=search_query) |
            Q(yer__icontains=search_query) |
            Q(etkinlik_turu__icontains=search_query)
        )
    
    etkinlikler = etkinlikler.order_by('baslangic_tarihi')
    
    # Calculate stats for the template
    kayit_gereken_etkinlikler = etkinlikler.filter(kayit_gerekiyor=True).count()
    farkli_mekanlar = etkinlikler.values('yer').distinct().count()
    
    return render(request, 'etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler,
        'search_query': search_query,
        'kayit_gereken_etkinlikler': kayit_gereken_etkinlikler,
        'farkli_mekanlar': farkli_mekanlar,
    })