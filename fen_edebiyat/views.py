# fen_edebiyat/views.py
from django.shortcuts import render, get_object_or_404
from .models import FenEdebiyatDuyuru




def duyurular(request):
    """نمایش تمام اطلاعیه‌های دانشکده"""
    duyurular = FenEdebiyatDuyuru.objects.filter(yayinda=True)
    
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
    return render(request, 'fen_edebiyat/includes/duyurular.html', context)

def duyuru_detay(request, id):
    """نمایش جزئیات یک اطلاعیه"""
    duyuru = get_object_or_404(FenEdebiyatDuyuru, id=id, yayinda=True)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = FenEdebiyatDuyuru.objects.filter(
        kategori=duyuru.kategori,
        yayinda=True
    ).exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    context = {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    }
    return render(request, 'fen_edebiyat/includes/duyuru_detay.html', context)



# سایر viewهای موجود...
def fen_edebiyat(request):
    return render(request, 'fen_edebiyat/includes/fen_edebiyat.html')

def tarihce(request):
    return render(request, 'fen_edebiyat/includes/tarihce.html')

def misyon_visyon(request):
    return render(request, 'fen_edebiyat/includes/misyon_visyon.html')

def dekan_mesaji(request):
    return render(request, 'fen_edebiyat/includes/dekan_mesaji.html')

def fakulte_yonetimi(request):
    return render(request, 'fen_edebiyat/includes/fakulte_yonetimi.html')

def bolum_baskanli(request):
    return render(request, 'fen_edebiyat/includes/bolum_baskanli.html')

def akademik_kadro(request):
    return render(request, 'fen_edebiyat/includes/akademik_kadro.html')

def misafir_kadro(request):
    return render(request, 'fen_edebiyat/includes/misafir_kadro.html')

def kalite(request):
    return render(request, 'fen_edebiyat/includes/kalite.html')

def iletisim(request):
    return render(request, 'fen_edebiyat/includes/iletisim.html')



