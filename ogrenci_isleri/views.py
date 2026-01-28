from django.shortcuts import render




def ogrenci_isleri(request):
    return render(request,'ogrenci_isleri/includes/ogrenci_isleri.html')


def daire_baskanligi(request):
    return render(request,'ogrenci_isleri/includes/daire_baskanligi.html')


def ogrenim_ucretleri(request):
    return render(request,'ogrenci_isleri/includes/ogrenim_ucretleri.html')


def kayit(request):
    return render(request,'ogrenci_isleri/includes/kayit.html')


def burslar(request):
    return render(request,'ogrenci_isleri/includes/burslar.html')

def yurtlar(request):
    return render(request,'ogrenci_isleri/includes/yurtlar.html')

def muafiyetler(request):
    return render(request,'ogrenci_isleri/includes/muafiyetler.html')

def kulupler(request):
    return render(request,'ogrenci_isleri/includes/kulupler.html')

def yonetmelik(request):
    return render(request,'ogrenci_isleri/includes/yonetmelik.html')

def formlar(request):
    return render(request,'ogrenci_isleri/includes/formlar.html')

def dikey(request):
    return render(request,'ogrenci_isleri/includes/dikey.html')

def erasmus(request):
    return render(request,'ogrenci_isleri/includes/erasmus.html')


