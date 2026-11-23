from django.core.cache import cache
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from .models import Bolum, Duyuru


def _get_duyuru_sidebar_stats():
    """Aggregate faculty & department announcement counts in 2 queries and cache for 5 minutes."""
    cache_key = "duyurular:stats:v1"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    fakulte_counts_qs = (
        Duyuru.objects.filter(yayinda=True)
        .values('fakulte')
        .annotate(total=Count('id'))
    )
    fakulte_count_map = {row['fakulte']: row['total'] for row in fakulte_counts_qs}
    toplam_duyuru = sum(fakulte_count_map.values())

    fakulte_istatistikleri = {
        fakulte_kodu: {
            'adi': fakulte_adi,
            'sayi': fakulte_count_map.get(fakulte_kodu, 0),
        }
        for fakulte_kodu, fakulte_adi in Duyuru.FAKULTE_CHOICES
    }

    aktif_bolumler = list(
        Bolum.objects.filter(aktif=True).annotate(
            yayinda_sayisi=Count('duyuru', filter=Q(duyuru__yayinda=True))
        )
    )
    bolum_istatistikleri = {
        bolum.kod: {
            'adi': bolum.ad,
            'sayi': bolum.yayinda_sayisi,
            'fakulte': bolum.fakulte,
        }
        for bolum in aktif_bolumler
    }

    stats = {
        'fakulte_istatistikleri': fakulte_istatistikleri,
        'bolum_istatistikleri': bolum_istatistikleri,
        'aktif_bolumler': aktif_bolumler,
        'toplam_duyuru': toplam_duyuru,
    }
    cache.set(cache_key, stats, 300)
    return stats


def duyuru_listesi(request):
    duyurular = Duyuru.objects.filter(yayinda=True).prefetch_related('dosyalar', 'bolumler')

    search_query = request.GET.get('q', '')
    tarih_query = request.GET.get('tarih', '')
    fakulte_filter = request.GET.get('fakulte', '')
    bolum_filter = request.GET.get('bolum', '')

    if search_query:
        duyurular = duyurular.filter(
            Q(baslik__icontains=search_query)
            | Q(icerik__icontains=search_query)
            | Q(fakulte__icontains=search_query)
            | Q(ozet__icontains=search_query)
        )

    if tarih_query:
        duyurular = duyurular.filter(yayin_tarihi__date=tarih_query)

    if fakulte_filter:
        duyurular = duyurular.filter(fakulte=fakulte_filter)

    if bolum_filter:
        duyurular = duyurular.filter(bolumler__kod=bolum_filter)

    stats = _get_duyuru_sidebar_stats()
    bolum_adi = None
    if bolum_filter:
        matched_bolum = stats['bolum_istatistikleri'].get(bolum_filter)
        bolum_adi = matched_bolum['adi'] if matched_bolum else None

    context = {
        'duyurular': duyurular,
        'search_query': search_query,
        'tarih_query': tarih_query,
        'fakulte_filter': fakulte_filter,
        'bolum_filter': bolum_filter,
        'bolum_adi': bolum_adi,
        'fakulte_choices': Duyuru.FAKULTE_CHOICES,
        'fakulte_istatistikleri': stats['fakulte_istatistikleri'],
        'bolum_istatistikleri': stats['bolum_istatistikleri'],
        'toplam_duyuru': stats['toplam_duyuru'],
        'aktif_bolumler': stats['aktif_bolumler'],
    }

    return render(request, 'duyurular/list.html', context)


def duyuru_detay(request, slug):
    duyuru = get_object_or_404(Duyuru, slug=slug, yayinda=True)

    ilgili_duyurular = (
        Duyuru.objects.filter(
            Q(fakulte=duyuru.fakulte) | Q(bolumler__in=duyuru.bolumler.all()),
            yayinda=True,
        )
        .exclude(id=duyuru.id)
        .distinct()
        .order_by('-yayin_tarihi')[:3]
    )

    return render(request, 'duyurular/detail.html', {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    })


def fakulte_duyurulari(request, fakulte_kodu):
    """نمایش اطلاعیه‌های یک دانشکده خاص"""
    fakulte_adi = dict(Duyuru.FAKULTE_CHOICES).get(fakulte_kodu, 'Bilinmeyen')
    duyurular = Duyuru.objects.filter(fakulte=fakulte_kodu, yayinda=True).prefetch_related('dosyalar', 'bolumler')

    bolumler = Bolum.objects.filter(fakulte=fakulte_kodu, aktif=True)

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
    duyurular = Duyuru.objects.filter(bolumler=bolum, yayinda=True).prefetch_related('dosyalar', 'bolumler')

    return render(request, 'duyurular/bolum_list.html', {
        'duyurular': duyurular,
        'bolum': bolum,
        'fakulte_adi': bolum.get_fakulte_display(),
    })
