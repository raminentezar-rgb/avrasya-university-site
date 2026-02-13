from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from .models import AdayMenu, AdaySayfa, AdaySlider, AdayIletisim
from .forms import AdayIletisimForm

def aday_anasayfa(request):
    
    return render(request, 'aday_ogrenci/includes/anasayfa.html')



# سایر viewهای مورد نیاز
def kontenjanlar(request):
    
    return render(request, 'aday_ogrenci/includes/kontenjanlar.html')

def egitim_ucretleri(request):
    return render(request, 'aday_ogrenci/includes/egitim-ucretleri.html')

def taban_puanlar(request):
    
    return render(request, 'aday_ogrenci/includes/taban-puanlar.html')

# def yatay_gecis(request):
#     sayfa = get_object_or_404(AdaySayfa, slug='yatay-gecis', is_published=True)
#     return render(request, 'aday_ogrenci/includes/sayfa_detay.html', {'sayfa': sayfa})

def dikey_gecis(request):
    
    return render(request, 'aday_ogrenci/includes/dikey-gecis.html')

def foto_galeri(request):
    
    return render(request, 'aday_ogrenci/includes/foto-galeri.html')

def laboratuvarlar(request):
    
    return render(request, 'aday_ogrenci/includes/laboratuvarlar.html')

def kampus_yasam(request):
   
    return render(request, 'aday_ogrenci/includes/kampus-yasam.html')

def yurt_olanaklari(request):
    
    return render(request, 'aday_ogrenci/includes/yurt-olanaklari.html')

def cap_yan_dal(request):
   
    return render(request, 'aday_ogrenci/includes/cap-yan-dal.html')

def yabanci_ogrenci(request):
    
    return render(request, 'aday_ogrenci/includes/yabanci-ogrenci.html')

def basvuru(request):
    
    return render(request, 'aday_ogrenci/includes/erasmus.html')

def erasmus(request):
    return render(request, 'aday_ogrenci/includes/erasmus.html')