from django.shortcuts import render

def idari_birimler(request):
    return render(request,'idari_birimler/includes/idari_birimler.html')

def kurumsal_iletisim(request):
    return render(request,'idari_birimler/includes/kurumsal_iletisim.html')

def bilgi_islem(request):
    return render(request,'idari_birimler/includes/bilgi_islem.html')

def idari_mali(request):
    return render(request,'idari_birimler/includes/idari_mali.html')

def kutuphane_dokumantasyon(request):
    return render(request,'idari_birimler/includes/kutuphane_dokumantasyon.html')

def oğrenci_isleri_daire_baskanligi(request):
    return render(request,'idari_birimler/includes/ogrenci_isleri_daire_baskanligi.html')

def personel_daire_baskanligi(request):
    return render(request,'idari_birimler/includes/personel_daire_baskanligi.html')

def yazi_isleri(request):
    return render(request,'idari_birimler/includes/yazi_isleri.html')

def yapi_isleri_mudurlugu(request):
    return render(request,'idari_birimler/includes/yapi_isleri_mudurlugu.html')