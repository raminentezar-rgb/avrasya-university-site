from django.urls import path
from . import views

app_name = 'idari_birimler'

urlpatterns = [
    path('',views.idari_birimler,name='idari_birimler'),
    path('kurumsal_iletisim/',views.kurumsal_iletisim,name='kurumsal_iletisim'),
    path('bilgi_islem/',views.bilgi_islem,name='bilgi_islem'),
    path('idari_mali/',views.idari_mali,name='idari_mali'),
    path('kutuphane_dokumantasyon/',views.kutuphane_dokumantasyon,name='kutuphane_dokumantasyon'),
    path('ogrenci_isleri_daire_baskanligi/',views.oğrenci_isleri_daire_baskanligi,name='ogrenci_isleri_daire_baskanligi'),
    path('personel_daire_baskanligi/',views.personel_daire_baskanligi,name='personel_daire_baskanligi'),
    path('yazi_isleri/',views.yazi_isleri,name='yazi_isleri'),
    path('yapi_isleri_mudurlugu/',views.yapi_isleri_mudurlugu,name='yapi_isleri_mudurlugu'),
    
]