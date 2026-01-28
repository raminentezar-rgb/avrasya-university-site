# spor_bilimleri/views.py
from django.shortcuts import render, get_object_or_404
from .models import SporBilimleriDuyuru

def spor_bilimleri(request):
    """صفحه اصلی دانشکده"""
    return render(request, 'spor_bilimleri/includes/spor_bilimleri.html')

def duyurular(request):
    """نمایش تمام اطلاعیه‌های دانشکده"""
    duyurular = SporBilimleriDuyuru.objects.filter(yayinda=True)
    
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
    return render(request, 'spor_bilimleri/includes/duyurular.html', context)

def duyuru_detay(request, id):
    """نمایش جزئیات یک اطلاعیه"""
    duyuru = get_object_or_404(SporBilimleriDuyuru, id=id, yayinda=True)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = SporBilimleriDuyuru.objects.filter(
        kategori=duyuru.kategori,
        yayinda=True
    ).exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    context = {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    }
    return render(request, 'spor_bilimleri/includes/duyuru_detay.html', context)

# سایر ویوهای مورد نیاز برای دانشکده
def tarihce(request):
    return render(request, 'spor_bilimleri/includes/tarihce.html')

def misyon_visyon(request):
    return render(request, 'spor_bilimleri/misyon_visyon.html')

def dekan_mesaji(request):
    return render(request, 'spor_bilimleri/includes/dekan_mesaji.html')

def fakulte_yonetimi(request):
    return render(request, 'spor_bilimleri/includes/fakulte_yonetimi.html')

def bolumler(request):
    return render(request, 'spor_bilimleri/includes/bolumler.html')

def akademik_kadro(request):
    return render(request, 'spor_bilimleri/includes/akademik_kadro.html')

def tesisler(request):
    return render(request, 'spor_bilimleri/includes/tesisler.html')

def takimlar(request):
    return render(request, 'spor_bilimleri/includes/takimlar.html')

def iletisim(request):
    return render(request, 'spor_bilimleri/includes/iletisim.html')

def bolum_baskanli(request):
    return render(request, 'spor_bilimleri/includes/bolum_baskanli.html')

def misafir_kadro(request):
    return render(request, 'spor_bilimleri/includes/misafir_kadro.html')

def kalite(request):
    return render(request, 'spor_bilimleri/includes/kalite.html')
