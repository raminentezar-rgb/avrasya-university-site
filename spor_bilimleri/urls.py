# spor_bilimleri/urls.py
from django.urls import path
from . import views

app_name = 'spor_bilimleri'

urlpatterns = [
    # صفحات اصلی
    path('', views.spor_bilimleri, name='spor_bilimleri'),
    path('tarihce/', views.tarihce, name='tarihce'),
    path('misyon-vizyon/', views.misyon_visyon, name='misyon_visyon'),
    path('dekan-mesaji/', views.dekan_mesaji, name='dekan_mesaji'),
    
    # مدیریت
    path('yonetim/fakulte-yonetimi/', views.fakulte_yonetimi, name='fakulte_yonetimi'),
    path('bolumler/', views.bolumler, name='bolumler'),
    
    # آکادمیک
    path('akademik/kadro/', views.akademik_kadro, name='akademik_kadro'),
    path('tesisler/', views.tesisler, name='tesisler'),
    path('takimlar/', views.takimlar, name='takimlar'),
    
    # اطلاعیه‌ها
    path('duyurular/', views.duyurular, name='duyurular'),
    path('duyurular/<int:id>/', views.duyuru_detay, name='duyuru_detay'),
    
    # سایر صفحات
    path('iletisim/', views.iletisim, name='iletisim'),

    path('yonetim/bolum-baskanlari/', views.bolum_baskanli, name='bolum_baskanli'),

    path('akademik/misafir-kadro/', views.misafir_kadro, name='misafir_kadro'),

    path('kalite/', views.kalite, name='kalite'),
]