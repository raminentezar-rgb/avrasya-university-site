# saglik_hizmetleri_myo/views.py
from django.shortcuts import render, get_object_or_404
from .models import SaglikHizmetleriMYODuyuru

def duyurular(request):
    duyurular = SaglikHizmetleriMYODuyuru.objects.filter(yayinda=True)
    
    kategori = request.GET.get('kategori', '')
    if kategori:
        duyurular = duyurular.filter(kategori=kategori)
    
    onemli_duyurular = duyurular.filter(onemli=True)
    
    context = {
        'duyurular': duyurular,
        'onemli_duyurular': onemli_duyurular,
        'kategori': kategori,
    }
    return render(request, 'saglik_hizmetleri_myo/includes/duyurular.html', context)

def duyuru_detay(request, id):
    duyuru = get_object_or_404(SaglikHizmetleriMYODuyuru, id=id, yayinda=True)
    
    ilgili_duyurular = SaglikHizmetleriMYODuyuru.objects.filter(
        kategori=duyuru.kategori,
        yayinda=True
    ).exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    context = {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    }
    return render(request, 'saglik_hizmetleri_myo/includes/duyuru_detay.html', context)

def saglik_hizmetleri_myo(request):
    return render(request, 'saglik_hizmetleri_myo/includes/saglik_hizmetleri_myo.html')

def tarihce(request):
    return render(request, 'saglik_hizmetleri_myo/includes/tarihce.html')

def misyon_visyon(request):
    return render(request, 'saglik_hizmetleri_myo/includes/misyon_visyon.html')

def mdr_mesaji(request):
    return render(request, 'saglik_hizmetleri_myo/includes/mdr_mesaji.html')

def fakulte_yonetimi(request):
    return render(request, 'saglik_hizmetleri_myo/includes/fakulte_yonetimi.html')

def bolumler(request):
    return render(request, 'saglik_hizmetleri_myo/includes/bolumler.html')

def akademik_kadro(request):
    return render(request, 'saglik_hizmetleri_myo/includes/akademik_kadro.html')

def ogretim_programlari(request):
    return render(request, 'saglik_hizmetleri_myo/includes/ogretim_programlari.html')

def kalite(request):
    return render(request, 'saglik_hizmetleri_myo/includes/kalite.html')

def iletisim(request):
    return render(request, 'saglik_hizmetleri_myo/includes/iletisim.html')