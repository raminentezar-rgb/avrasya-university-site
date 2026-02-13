# app_name: makine_muhendisligi/urls.py

from django.urls import path
from . import views

app_name = 'makine_muhendisligi'

urlpatterns = [
    # اطلاعیه‌ها
    path('duyurular/', views.makine_muhendisligi_duyurulari, name='liste'),
    path('duyurular/<slug:slug>/', views.makine_muhendisligi_duyuru_detay, name='detay'),
    
    # صفحه اصلی
    path('', views.makine_muhendisligi_bolumu, name='makine_muhendisligi'),
    
    # برنامه درسی
    path('ders_programi/', views.ders_programi, name='ders_programi'),
    
    # فعالیت‌های اداری
    path('idari_faaliyetler_2024_2025/', views.idari_faaliyetler_2024_2025, name='idari_faaliyetler_2024_2025'),
    path('diger_faaliyetler_2024_2025/', views.diger_faaliyetler_2024_2025, name='diger_faaliyetler_2024_2025'),
    
    # رویدادها
    path('etkinlikler/', views.etkinlik_listesi, name='etkinlik_listesi'),
    path('etkinlikler/yaklasan/', views.yaklasan_etkinlikler, name='yaklasan_etkinlikler'),
    path('etkinlikler/<slug:slug>/', views.etkinlik_detay, name='etkinlik_detay'),
    
    # مدیریت کیفیت
    path('kalite_yonetimi/', views.kalite_yonetimi, name='kalite_yonetimi'),
    
    # مشارکت اجتماعی
    path('toplumsal_katki/', views.toplumsal_katki, name='toplumsal_katki'),
]