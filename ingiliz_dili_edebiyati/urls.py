# app_name: ingiliz_dili_edebiyati/urls.py

from django.urls import path
from . import views

app_name = 'ingiliz_dili_edebiyati'

urlpatterns = [
    # URLهای اطلاعیه‌ها
    path('duyurular/', views.ingiliz_dili_edebiyati_duyurulari, name='liste'),
    path('duyurular/<slug:slug>/', views.ingiliz_dili_edebiyati_duyuru_detay, name='detay'),
    
    # URLهای صفحات استاتیک
    path('', views.ingiliz_dili_edebiyati, name='ingiliz_dili_edebiyati'),
   
    
    
    
    
    
    
    path('ders_programi/', views.ders_programi, name='ders_programi'),
    
    # URLهای فعالیت‌ها
    path('idari_faaliyetler_2024_2025/', views.idari_faaliyetler_2024_2025, name='idari_faaliyetler_2024_2025'),
    path('idari_faaliyetler_2023_2024/', views.idari_faaliyetler_2023_2024, name='idari_faaliyetler_2023_2024'),
    path('diğer_faaliyetler_2024_2025/', views.diger_faaliyetler_2024_2025, name='diger_faaliyetler_2024_2025'),
    path('diğer_faaliyetler_2023_2024/', views.diger_faaliyetler_2023_2024, name='diger_faaliyetler_2023_2024'),

   

    # URLهای فعالیت‌ها
    path('etkinlikler/', views.etkinlik_listesi, name='etkinlik_listesi'),
    path('etkinlikler/yaklasan/', views.yaklasan_etkinlikler, name='yaklasan_etkinlikler'),
    path('etkinlikler/<slug:slug>/', views.etkinlik_detay, name='etkinlik_detay'),

    path('kalite_yonetimi/', views.kalite_yonetimi, name='kalite_yonetimi'),
    path('toplumsal_katki/', views.toplumsal_katki, name='toplumsal_katki'),
]