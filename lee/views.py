# lee/views.py
from django.shortcuts import render, get_object_or_404


from .models import LeeDuyuru, Lee_Etkinlik
from django.utils import timezone



def etkinlik_listesi(request):
    now = timezone.now()
    
    # رویدادهای آینده (از حالا به بعد)
    gelecek_etkinlikler = Lee_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__gte=now
    ).order_by('baslangic_tarihi')
    
    # رویدادهای گذشته (قبل از حالا)
    gecmis_etkinlikler = Lee_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__lt=now
    ).order_by('-baslangic_tarihi')
    
    # برای دیباگ - چاپ تعداد رویدادها
    print(f"Gelecek etkinlikler: {gelecek_etkinlikler.count()}")
    print(f"Geçmiş etkinlikler: {gecmis_etkinlikler.count()}")
    
    context = {
        'gelecek_etkinlikler': gelecek_etkinlikler,
        'gecmis_etkinlikler': gecmis_etkinlikler,
    }
    
    return render(request, 'lee/includes/etkinlikler/list.html', context)

def etkinlik_detay(request, slug):
    etkinlik = get_object_or_404(Lee_Etkinlik, slug=slug, yayinda=True)
    return render(request, 'lee/includes/etkinlikler/detail.html', {
        'etkinlik': etkinlik
    })

def yaklasan_etkinlikler(request):
    """Yaklaşan etkinlikler (7 gün içinde)"""
    yedi_gun_sonra = timezone.now() + timezone.timedelta(days=7)
    etkinlikler = Lee_Etkinlik.objects.filter(
        yayinda=True,
        baslangic_tarihi__range=[timezone.now(), yedi_gun_sonra]
    ).order_by('baslangic_tarihi')
    
    return render(request, 'lee/includes/etkinlikler/yaklasan.html', {
        'etkinlikler': etkinlikler
    })




def duyurular(request):
    """نمایش تمام اطلاعیه‌های دانشکده LEE"""
    duyurular = LeeDuyuru.objects.filter(yayinda=True)
    
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
    return render(request, 'lee/includes/duyurular.html', context)

def duyuru_detay(request, id):
    """نمایش جزئیات یک اطلاعیه LEE"""
    duyuru = get_object_or_404(LeeDuyuru, id=id, yayinda=True)
    
    # اطلاعیه‌های مرتبط
    ilgili_duyurular = LeeDuyuru.objects.filter(
        kategori=duyuru.kategori,
        yayinda=True
    ).exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    context = {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    }
    return render(request, 'lee/includes/duyuru_detay.html', context)





# سایر viewهای موجود...
def lee(request):
    return render(request, 'lee/lee.html')

# سایر viewهای موجود...
def lee(request):
    return render(request, 'lee/includes/lee.html')

def tarihce(request):
    return render(request, 'lee/includes/tarihce.html')

def on_basvuru_formu(request):
    return render(request, 'lee/includes/on_basvuru_formu.html')

def tezli_yukseklisans_programlari(request):
    return render(request, 'lee/includes/tezli_yukseklisans_programlari.html')

def akademik_takvim(request):
    return render(request, 'lee/includes/akademik_takvim.html')

def doktora_programları(request):
    return render(request, 'lee/includes/doktora_programları.html')

def akademik_kadro(request):
    return render(request, 'lee/includes/akademik_kadro.html')

def mevzuat_formlar(request):
    return render(request, 'lee/includes/mevzuat_formlar.html')

def kalite(request):
    return render(request, 'lee/includes/kalite.html')

def iletisim(request):
    return render(request, 'lee/includes/iletisim.html')

def tezsiz_yukseklisans_programlari(request):
    return render(request, 'lee/includes/tezsiz_yukseklisans_programlari.html')


