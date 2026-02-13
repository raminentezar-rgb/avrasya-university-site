# lee/urls.py
from django.urls import path
from . import views

app_name = 'lee'

urlpatterns = [
    # صفحات اصلی
    path('', views.lee, name='lee'),
    path('tarihce/', views.tarihce, name='tarihce'),
    path('on_basvuru_formu/', views.on_basvuru_formu, name='on_basvuru_formu'),
    path('tezli_yukseklisans_programlari/', views.tezli_yukseklisans_programlari, name='tezli_yukseklisans_programlari'),
    path('tezsiz_yukseklisans_programlari/', views.tezsiz_yukseklisans_programlari, name='tezsiz_yukseklisans_programlari'),
    
    # Form APIs
    path('api/basvuru/online/', views.submit_online_application, name='submit_online'),
    path('api/basvuru/international/', views.submit_international_application, name='submit_international'),
    
    # مدیریت
    path('akademik_takvim/', views.akademik_takvim, name='akademik_takvim'),
    path('doktora_programları/', views.doktora_programları, name='doktora_programları'),
    
    # آکادمیک
    path('akademik_kadro/', views.akademik_kadro, name='akademik_kadro'),
    path('mevzuat_formlar/', views.mevzuat_formlar, name='mevzuat_formlar'),
    
    # سایر صفحات
    path('kalite/', views.kalite, name='kalite'),
    path('iletisim/', views.iletisim, name='iletisim'),

    path('duyurular/', views.duyurular, name='duyurular'),
    path('duyurular/<int:id>/', views.duyuru_detay, name='duyuru_detay'),



    path('etkinlikler/', views.etkinlik_listesi, name='etkinlik_listesi'),
    path('etkinlikler/yaklasan/', views.yaklasan_etkinlikler, name='yaklasan_etkinlikler'),
    path('etkinlikler/<slug:slug>/', views.etkinlik_detay, name='etkinlik_detay'),



  

]