# app_name: tibbi_laboratuvar/urls.py

from django.urls import path
from . import views

app_name = 'tibbi_laboratuvar'

urlpatterns = [
    # URLهای اطلاعیه‌ها
    path('duyurular/', views.tibbi_laboratuvar_duyurulari, name='liste'),
    path('duyurular/<slug:slug>/', views.tibbi_laboratuvar_duyuru_detay, name='detay'),
    
    # URLهای صفحات استاتیک
    path('', views.tibbi_laboratuvar_bolumu, name='tibbi_laboratuvar'),
    
    path('ders_programi/', views.ders_programi, name='ders_programi'),
    
    # URLهای فعالیت‌ها
    path('idari_faaliyetler/', views.idari_faaliyetler, name='idari_faaliyetler'),
    
    path('diger_faaliyetler/', views.diger_faaliyetler, name='diger_faaliyetler'),
    
    # URLهای فعالیت‌ها
    path('etkinlikler/', views.etkinlik_listesi, name='etkinlik_listesi'),
    path('etkinlikler/yaklasan/', views.yaklasan_etkinlikler, name='yaklasan_etkinlikler'),
    path('etkinlikler/<slug:slug>/', views.etkinlik_detay, name='etkinlik_detay'),
    
    path('kalite_yonetimi/', views.kalite_yonetimi, name='kalite_yonetimi'),
    path('toplumsal_katki/', views.toplumsal_katki, name='toplumsal_katki'),
]