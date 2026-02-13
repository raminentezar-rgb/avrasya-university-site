from django.shortcuts import render


def kutuphane(request):
    return render(request,'kutuphane/includes/anasayfa.html')

def genel_bilgiler(request):
    return render(request, 'kutuphane/includes/genel_bilgiler.html')


def acik_erisim(request):
    return render(request, 'kutuphane/includes/acik_erisim.html')

def calisma_takvimi(request):
    return render(request, 'kutuphane/includes/calisma_takvimi.html')


def hizli_baglantilar(request):
    return render(request, 'kutuphane/includes/hizli_baglantilar.html')


def iletisim(request):
    return render(request, 'kutuphane/includes/iletisim.html')

