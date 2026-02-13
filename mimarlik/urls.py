# app_name: mimarlik/urls.py

from django.urls import path
from . import views

app_name = 'mimarlik'

urlpatterns = [
    # URLهای اطلاعیه‌ها
    path('duyurular/', views.mimarlik_duyurulari, name='liste'),
    path('duyurular/<slug:slug>/', views.mimarlik_duyuru_detay, name='detay'),
    
    # URLهای صفحات استاتیک
    path('', views.mimarlik_bolumu, name='mimarlik'),
    
    path('ders_programi/', views.ders_programi, name='ders_programi'),
    
    # URLهای فعالیت‌ها
    path('idari_faaliyetler_2024_2025/', views.idari_faaliyetler_2024_2025, name='idari_faaliyetler_2024_2025'),
    
    path('diger_faaliyetler_2024_2025/', views.diger_faaliyetler_2024_2025, name='diger_faaliyetler_2024_2025'),
    
    # URLهای رویدادها
    path('etkinlikler/', views.etkinlik_listesi, name='etkinlik_listesi'),
    path('etkinlikler/yaklasan/', views.yaklasan_etkinlikler, name='yaklasan_etkinlikler'),
    path('etkinlikler/<slug:slug>/', views.etkinlik_detay, name='etkinlik_detay'),
    
    path('kalite_yonetimi/', views.kalite_yonetimi, name='kalite_yonetimi'),
    path('toplumsal_katki/', views.toplumsal_katki, name='toplumsal_katki'),
]