# saglik_bilimleri/views.py
from django.shortcuts import render, get_object_or_404
from .models import SaglikBilimleriDuyuru

def duyurular(request):
    """نمایش تمام اطلاعیه‌های دانشکده"""
    duyurular = SaglikBilimleriDuyuru.objects.filter(yayinda=True)
    
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
    return render(request, 'saglik_bilimleri/includes/duyurular.html', context)

def duyuru_detay(request, id):
    """نمایش جزئیات یک اطلاعیه"""
    duyuru = get_object_or_404(SaglikBilimleriDuyuru, id=id, yayinda=True)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = SaglikBilimleriDuyuru.objects.filter(
        kategori=duyuru.kategori,
        yayinda=True
    ).exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    context = {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    }
    return render(request, 'saglik_bilimleri/includes/duyuru_detay.html', context)

# سایر viewهای موجود...
def saglik_bilimleri(request):
    return render(request, 'saglik_bilimleri/includes/saglik_bilimleri.html')

def tarihce(request):
    return render(request, 'saglik_bilimleri/includes/tarihce.html')

def misyon_visyon(request):
    return render(request, 'saglik_bilimleri/includes/misyon_visyon.html')

def dekan_mesaji(request):
    return render(request, 'saglik_bilimleri/includes/dekan_mesaji.html')

def fakulte_yonetimi(request):
    return render(request, 'saglik_bilimleri/includes/fakulte_yonetimi.html')

def bolum_baskanli(request):
    return render(request, 'saglik_bilimleri/includes/bolum_baskanli.html')

def akademik_kadro(request):
    return render(request, 'saglik_bilimleri/includes/akademik_kadro.html')

def misafir_kadro(request):
    return render(request, 'saglik_bilimleri/includes/misafir_kadro.html')

def kalite(request):
    return render(request, 'saglik_bilimleri/includes/kalite.html')

def iletisim(request):
    return render(request, 'saglik_bilimleri/includes/iletisim.html')