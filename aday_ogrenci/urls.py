from django.urls import path
from . import views

app_name = 'aday_ogrenci'

urlpatterns = [
    path('', views.aday_anasayfa, name='aday_anasayfa'),
   
    
    # Özel sayfalar
    path('kontenjanlar/', views.kontenjanlar, name='kontenjanlar'),
    path('egitim-ucretleri/', views.egitim_ucretleri, name='egitim_ucretleri'),
    path('taban-puanlar/', views.taban_puanlar, name='taban_puanlar'),
    # path('yatay-gecis/', views.yatay_gecis, name='yatay_gecis'),
    path('dikey-gecis/', views.dikey_gecis, name='dikey_gecis'),
    path('foto-galeri/', views.foto_galeri, name='foto_galeri'),
    path('laboratuvarlar/', views.laboratuvarlar, name='laboratuvarlar'),
    path('kampus-yasam/', views.kampus_yasam, name='kampus_yasam'),
    path('yurt-olanaklari/', views.yurt_olanaklari, name='yurt_olanaklari'),
    path('cap-yan-dal/', views.cap_yan_dal, name='cap_yan_dal'),
    path('yabanci-ogrenci/', views.yabanci_ogrenci, name='yabanci_ogrenci'),
    path('basvuru/', views.basvuru, name='basvuru'),
    path('erasmus/', views.erasmus, name='erasmus'),
]