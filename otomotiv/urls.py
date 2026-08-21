# app_name: otomotiv/urls.py

from django.urls import path
from . import views

app_name = 'otomotiv'

urlpatterns = [
    # URLهای اطلاعیه‌ها
    path('duyurular/', views.otomotiv_duyurulari, name='liste'),
    path('duyurular/<slug:slug>/', views.otomotiv_duyuru_detay, name='detay'),
    
    # URLهای صفحات استاتیک
    path('', views.otomotiv_bolumu, name='otomotiv'),
    
    path('ders_programi/', views.ders_programi, name='ders_programi'),
    
    # URLهای فعالیت‌ها
    path('idari_faaliyetler/', views.idari_faaliyetler, name='idari_faaliyetler'),
    
    path('diger_faaliyetler/', views.diger_faaliyetler, name='diger_faaliyetler'),
    
    # URLهای فعالیت‌ها (اتفاقات)
    path('etkinlikler/', views.etkinlik_listesi, name='etkinlik_listesi'),
    path('etkinlikler/yaklasan/', views.yaklasan_etkinlikler, name='yaklasan_etkinlikler'),
    path('etkinlikler/<slug:slug>/', views.etkinlik_detay, name='etkinlik_detay'),
    
    path('kalite_yonetimi/', views.kalite_yonetimi, name='kalite_yonetimi'),
    path('toplumsal_katki/', views.toplumsal_katki, name='toplumsal_katki'),
]