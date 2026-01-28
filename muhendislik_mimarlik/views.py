# muhendislik_mimarlik/views.py
from django.shortcuts import render, get_object_or_404
from .models import MuhendislikMimarlikDuyuru

def muhendislik_mimarlik(request):
    """صفحه اصلی دانشکده"""
    return render(request, 'muhendislik_mimarlik/includes/muhendislik_mimarlik.html')

def duyurular(request):
    """نمایش تمام اطلاعیه‌های دانشکده"""
    duyurular = MuhendislikMimarlikDuyuru.objects.filter(yayinda=True)
    
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
    return render(request, 'muhendislik_mimarlik/includes/duyurular.html', context)

def duyuru_detay(request, id):
    """نمایش جزئیات یک اطلاعیه"""
    duyuru = get_object_or_404(MuhendislikMimarlikDuyuru, id=id, yayinda=True)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = MuhendislikMimarlikDuyuru.objects.filter(
        kategori=duyuru.kategori,
        yayinda=True
    ).exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    context = {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    }
    return render(request, 'muhendislik_mimarlik/includes/duyuru_detay.html', context)

# سایر ویوهای مورد نیاز برای دانشکده
def tarihce(request):
    return render(request, 'muhendislik_mimarlik/includes/tarihce.html')

def misyon_visyon(request):
    return render(request, 'muhendislik_mimarlik/includes/misyon_visyon.html')

def dekan_mesaji(request):
    return render(request, 'muhendislik_mimarlik/includes/dekan_mesaji.html')

def fakulte_yonetimi(request):
    return render(request, 'muhendislik_mimarlik/includes/fakulte_yonetimi.html')

def bolumler(request):
    return render(request, 'muhendislik_mimarlik/includes/bolumler.html')

def akademik_kadro(request):
    return render(request, 'muhendislik_mimarlik/includes/akademik_kadro.html')

def laboratuvarlar(request):
    return render(request, 'muhendislik_mimarlik/includes/laboratuvarlar.html')

def iletisim(request):
    return render(request, 'muhendislik_mimarlik/includes/iletisim.html')

def bolum_baskanli(request):
    return render(request, 'muhendislik_mimarlik/includes/bolum_baskanli')

def misafir_kadro(request):
    return render(request, 'muhendislik_mimarlik/includes/misafir_kadro.html')

def kalite(request):
    return render(request, 'muhendislik_mimarlik/includes/kalite.html')

