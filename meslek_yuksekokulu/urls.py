# meslek_yuksekokulu/urls.py
from django.urls import path
from . import views

app_name = 'meslek_yuksekokulu'

urlpatterns = [
    path('', views.meslek_yuksekokulu, name='meslek_yuksekokulu'),
    path('tarihce/', views.tarihce, name='tarihce'),
    path('misyon-vizyon/', views.misyon_visyon, name='misyon_visyon'),
    path('mdr-mesaji/', views.mdr_mesaji, name='mdr_mesaji'),
    
    path('fakulte_yonetimi/', views.fakulte_yonetimi, name='fakulte_yonetimi'),
    path('bolumler/', views.bolumler, name='bolumler'),
    
    path('akademik-kadro/', views.akademik_kadro, name='akademik_kadro'),
    path('ogretim-programlari/', views.ogretim_programlari, name='ogretim_programlari'),
    
    path('kalite/', views.kalite, name='kalite'),
    path('iletisim/', views.iletisim, name='iletisim'),

    path('duyurular/', views.duyurular, name='duyurular'),
    path('duyurular/<int:id>/', views.duyuru_detay, name='duyuru_detay'),
]