# meslek_yuksekokulu/views.py
from django.shortcuts import render, get_object_or_404
from .models import MeslekYuksekokuluDuyuru

def duyurular(request):
    duyurular = MeslekYuksekokuluDuyuru.objects.filter(yayinda=True)
    
    kategori = request.GET.get('kategori', '')
    if kategori:
        duyurular = duyurular.filter(kategori=kategori)
    
    onemli_duyurular = duyurular.filter(onemli=True)
    
    context = {
        'duyurular': duyurular,
        'onemli_duyurular': onemli_duyurular,
        'kategori': kategori,
    }
    return render(request, 'meslek_yuksekokulu/includes/duyurular.html', context)

def duyuru_detay(request, id):
    duyuru = get_object_or_404(MeslekYuksekokuluDuyuru, id=id, yayinda=True)
    
    ilgili_duyurular = MeslekYuksekokuluDuyuru.objects.filter(
        kategori=duyuru.kategori,
        yayinda=True
    ).exclude(id=duyuru.id).order_by('-yayin_tarihi')[:3]
    
    context = {
        'duyuru': duyuru,
        'ilgili_duyurular': ilgili_duyurular,
    }
    return render(request, 'meslek_yuksekokulu/includes/duyuru_detay.html', context)

def meslek_yuksekokulu(request):
    return render(request, 'meslek_yuksekokulu/includes/meslek_yuksekokulu.html')

def tarihce(request):
    return render(request, 'meslek_yuksekokulu/includes/tarihce.html')

def misyon_visyon(request):
    return render(request, 'meslek_yuksekokulu/includes/misyon_visyon.html')

def mdr_mesaji(request):
    return render(request, 'meslek_yuksekokulu/includes/mdr_mesaji.html')

def fakulte_yonetimi(request):
    return render(request, 'meslek_yuksekokulu/includes/fakulte_yonetimi.html')

def bolumler(request):
    return render(request, 'meslek_yuksekokulu/includes/bolumler.html')

def akademik_kadro(request):
    return render(request, 'meslek_yuksekokulu/includes/akademik_kadro.html')

def ogretim_programlari(request):
    return render(request, 'meslek_yuksekokulu/includes/ogretim_programlari.html')

def kalite(request):
    return render(request, 'meslek_yuksekokulu/includes/kalite.html')

def iletisim(request):
    return render(request, 'meslek_yuksekokulu/includes/iletisim.html')