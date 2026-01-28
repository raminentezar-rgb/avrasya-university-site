# yatay_gecis/views.py
from django.shortcuts import render

def yatay_gecis_view(request):
    return render(request, 'yatay_gecis/includes/yatay_gecis.html')

def yatay_Kontenjanlar(request):
    return render(request, 'yatay_gecis/includes/yatay_Kontenjanlar.html')

def yatay_geciste_istenilen_Bbelgeler(request):
    return render(request, 'yatay_gecis/includes/yatay_geciste_istenilen_Bbelgeler.html')


def ortalama(request):
    return render(request, 'yatay_gecis/includes/ortalama.html')

def ek_madde(request):
    return render(request, 'yatay_gecis/includes/ek_madde.html')

def degerlendirme_bicimi(request):
    return render(request, 'yatay_gecis/includes/degerlendirme_bicimi.html')

def burslar(request):
    return render(request, 'yatay_gecis/includes/burslar.html')


def kayıt_yeri(request):
    return render(request, 'yatay_gecis/includes/kayıt_yeri.html')


def yatay_taban(request):
    return render(request, 'yatay_gecis/includes/yatay_taban_puanlar.html')

def orenci_isleri_daire_baskanli(request):
    return render(request, 'yatay_gecis/includes/orenci_isleri_daire_baskanli.html')

def takvim(request):
    return render(request, 'yatay_gecis/includes/takvim.html')

def bahar(request):
    return render(request, 'yatay_gecis/includes/bahar.html')