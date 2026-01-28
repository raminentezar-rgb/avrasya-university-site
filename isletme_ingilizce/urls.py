from django.urls import path
from . import views

app_name = 'isletme_ingilizce'

urlpatterns = [
    # URLهای اطلاعیه‌ها
    path('duyurular/', views.isletme_ingilizce_duyurulari, name='liste'),
    path('duyurular/<slug:slug>/', views.isletme_ingilizce_duyuru_detay, name='detay'),
    
    # URLهای صفحات استاتیک مدیریت کسب و کار انگلیسی
    path('', views.isletme_ingilizce, name='isletme_ingilizce'),
    path('tarihce/', views.isletme_ingilizce_tarihce, name='tarihce'),
    path('misyon_visyon/', views.isletme_ingilizce_misyon_visyon, name='misyon_visyon'),
    path('yonetimi/', views.isletme_ingilizce_yonetimi, name='yonetimi'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('ogrenci_isleri/', views.ogrenci_isleri, name='ogrenci_isleri'),
    path('cift_anadal/', views.cift_anadal, name='cift_anadal'),
    path('erasmus/', views.erasmus, name='erasmus'),
    path('ders_programi/', views.ders_programi, name='ders_programi'),
    
    # URLهای فعالیت‌ها
    path('idari_faaliyetler_2024_2025/', views.idari_faaliyetler_2024_2025, name='idari_faaliyetler_2024_2025'),
    path('idari_faaliyetler_2023_2024/', views.idari_faaliyetler_2023_2024, name='idari_faaliyetler_2023_2024'),
    path('diger_faaliyetler_2024_2025/', views.diger_faaliyetler_2024_2025, name='diger_faaliyetler_2024_2025'),
    path('diger_faaliyetler_2023_2024/', views.diger_faaliyetler_2023_2024, name='diger_faaliyetler_2023_2024'),

    path('akreditasyon_belgesi/', views.akreditasyon_belgesi, name='akreditasyon_belgesi'),
    path('komisyon_sorumlular/', views.komisyon_sorumlular, name='komisyon_sorumlular'),
    path('program_ogretim_amaclari/', views.program_ogretim_amaclari, name='program_ogretim_amaclari'),
    path('program_ogrenim_ciktilari/', views.program_ogrenim_ciktilari, name='program_ogrenim_ciktilari'),
    path('anketler/', views.anketler, name='anketler'),
    path('ders_plani/', views.ders_plani, name='ders_plani'),

    # URLهای فعالیت‌ها
    path('etkinlikler/', views.etkinlik_listesi, name='etkinlik_listesi'),
    path('etkinlikler/yaklasan/', views.yaklasan_etkinlikler, name='yaklasan_etkinlikler'),
    path('etkinlikler/<slug:slug>/', views.etkinlik_detay, name='etkinlik_detay'),
]