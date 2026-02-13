# muhendislik_mimarlik/urls.py
from django.urls import path
from . import views

app_name = 'muhendislik_mimarlik'

urlpatterns = [
    # صفحات اصلی
    path('', views.muhendislik_mimarlik, name='muhendislik_mimarlik'),
    path('tarihce/', views.tarihce, name='tarihce'),
    path('misyon-vizyon/', views.misyon_visyon, name='misyon_visyon'),
    path('dekan-mesaji/', views.dekan_mesaji, name='dekan_mesaji'),
    
    # مدیریت
    path('yonetim/fakulte-yonetimi/', views.fakulte_yonetimi, name='fakulte_yonetimi'),
    path('yonetim/bolum-baskanlari/', views.bolum_baskanli, name='bolum_baskanli'),
    
    # آکادمیک
    path('akademik/kadro/', views.akademik_kadro, name='akademik_kadro'),
    path('akademik/misafir-kadro/', views.misafir_kadro, name='misafir_kadro'),
    
    # سایر صفحات
    path('kalite/', views.kalite, name='kalite'),
    path('iletisim/', views.iletisim, name='iletisim'),

   
    
    # اطلاعیه‌ها
    path('duyurular/', views.duyurular, name='duyurular'),
    path('duyurular/<int:id>/', views.duyuru_detay, name='duyuru_detay'),
    
    # سایر صفحات
    path('iletisim/', views.iletisim, name='iletisim'),
]