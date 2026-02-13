# yatay_gecis/urls.py
from django.urls import path
from . import views

app_name = 'yatay_gecis'

urlpatterns = [
    path('', views.yatay_gecis_view, name='yatay_gecis'),
    path('yatay_gecis_Kontenjanlar', views.yatay_Kontenjanlar, name='yatay_Kontenjanlar'),
    path('yatay_geciste_istenilen_Bbelgeler', views.yatay_geciste_istenilen_Bbelgeler, name='yatay_geciste_istenilen_Bbelgeler'),
    path('ortalama', views.ortalama, name='ortalama'),
    path('ek_madde', views.ek_madde, name='ek_madde'),
    path('degerlendirme_bicimi', views.degerlendirme_bicimi, name='degerlendirme_bicimi'),
    path('burslar', views.burslar, name='burslar'),
    path('kayit_yeri', views.kayıt_yeri, name='kayıt_yeri'),
    path('taban_puanlar', views.yatay_taban, name='yatay_taban'),
    path('orenci_isleri_daire_baskanli', views.orenci_isleri_daire_baskanli, name='orenci_isleri_daire_baskanli'),
    path('basvuru_takvim', views.takvim, name='takvim'),
    path('bahar', views.bahar, name='bahar'),
]