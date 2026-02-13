# iletisim/views.py
from django.shortcuts import render, get_object_or_404
from .models import IletisimDuyuru

def iletisim_anasayfa(request):
    """صفحه اصلی بخش ارتباطات"""
    return render(request, 'iletisim/includes/iletisim.html')

def duyurular(request):
    """نمایش تمام اطلاعیه‌های ارتباطات"""
    duyurular = IletisimDuyuru.objects.filter(yayinda=True)
    
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
    return render(request, 'iletisim/includes/duyurular.html', context)

def duyuru_detay(request, id):
    """نمایش جزئیات یک اطلاعیه"""
    duyuru = get_object_or_404(IletisimDuyuru, id=id, yayinda=True)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = IletisimDuyuru.objects.filter(
        kategori=duyuru.kategori,
        yayinda=True
    ).exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    context = {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    }
    return render(request, 'iletisim/includes/duyuru_detay.html', context)

# سایر ویوهای مورد نیاز برای بخش ارتباطات
def akademik_kadro(request):
    return render(request, 'iletisim/includes/akademik_kadro.html')

def kalite(request):
    return render(request, 'iletisim/includes/kalite.html')

def fakulte_yonetimi(request):
    return render(request, 'iletisim/includes/fakulte_yonetimi.html')

def servisler(request):
    return render(request, 'iletisim/includes/servisler.html')

def teknoloji(request):
    return render(request, 'iletisim/includes/teknoloji.html')

def medya(request):
    return render(request, 'iletisim/includes/medya.html')

def iletisim_bilgileri(request):
    return render(request, 'iletisim/includes/iletisim_bilgileri.html')

def sss(request):
    return render(request, 'iletisim/includes/sss.html')

def formlar(request):
    return render(request, 'iletisim/includes/formlar.html')

def acil_durum(request):
    return render(request, 'iletisim/includes/acil_durum.html')

def sosyal_medya(request):
    return render(request, 'iletisim/includes/sosyal_medya.html')