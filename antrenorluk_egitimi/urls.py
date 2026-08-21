# app_name: antrenorluk_egitimi/urls.py

from django.urls import path
from . import views

app_name = 'antrenorluk_egitimi'

urlpatterns = [
    # اطلاعیه‌ها
    path('duyurular/', views.antrenorluk_egitimi_duyurulari, name='liste'),
    path('duyurular/<slug:slug>/', views.antrenorluk_egitimi_duyuru_detay, name='detay'),

    # صفحات استاتیک
    path('', views.antrenorluk_egitimi_bolumu, name='antrenorluk_egitimi'),

    path('ders_programi/', views.ders_programi, name='ders_programi'),

    # فعالیت‌ها
    path('idari_faaliyetler/', views.idari_faaliyetler, name='idari_faaliyetler'),

    path('diger_faaliyetler/', views.diger_faaliyetler, name='diger_faaliyetler'),

    # رویدادها
    path('etkinlikler/', views.etkinlik_listesi, name='etkinlik_listesi'),
    path('etkinlikler/yaklasan/', views.yaklasan_etkinlikler, name='yaklasan_etkinlikler'),
    path('etkinlikler/<slug:slug>/', views.etkinlik_detay, name='etkinlik_detay'),

    path('kalite_yonetimi/', views.kalite_yonetimi, name='kalite_yonetimi'),
    path('toplumsal_katki/', views.toplumsal_katki, name='toplumsal_katki'),
]