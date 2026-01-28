# iktisadi_idari/views.py
from django.shortcuts import render, get_object_or_404
from .models import IktisadiIdariDuyuru


def duyurular(request):
    """نمایش تمام اطلاعیه‌های دانشکده"""
    duyurular = IktisadiIdariDuyuru.objects.filter(yayinda=True)
    
    # فیلتر بر اساس دسته‌بندی
    kategori = request.GET.get('kategori', '')
    if kategori:
        duyurular = duyurular.filter(kategori=kategori)
    
    # اطلاعیه‌های مهم
    onemli_duyurular = duyurular.filter(onemli=True)
    
    context = {
        'duyurular': duyurular,
        'onemli_duyurular': onemli_duyurular,
        'kategori': kategori,
    }
    return render(request, 'iktisadi_idari/includes/duyurular.html', context)

def duyuru_detay(request, id):
    """نمایش جزئیات یک اطلاعیه"""
    duyuru = get_object_or_404(IktisadiIdariDuyuru, id=id, yayinda=True)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = IktisadiIdariDuyuru.objects.filter(
        kategori=duyuru.kategori,
        yayinda=True
    ).exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    context = {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    }
    return render(request, 'iktisadi_idari/includes/duyuru_detay.html', context)


# سایر viewهای موجود...
def iktisadi_idari(request):
    return render(request, 'iktisadi_idari/includes/iktisadi_idari.html')

def tarihce(request):
    return render(request, 'iktisadi_idari/includes/tarihce.html')

def misyon_visyon(request):
    return render(request, 'iktisadi_idari/includes/misyon_visyon.html')

def dekan_mesaji(request):
    return render(request, 'iktisadi_idari/includes/dekan_mesaji.html')

def fakulte_yonetimi(request):
    return render(request, 'iktisadi_idari/includes/fakulte_yonetimi.html')

def bolum_baskanli(request):
    return render(request, 'iktisadi_idari/includes/bolum_baskanli.html')

def akademik_kadro(request):
    return render(request, 'iktisadi_idari/includes/akademik_kadro.html')

def misafir_kadro(request):
    return render(request, 'iktisadi_idari/includes/misafir_kadro.html')

def kalite(request):
    return render(request, 'iktisadi_idari/includes/kalite.html')

def iletisim(request):
    return render(request, 'iktisadi_idari/includes/iletisim.html')