from django.urls import path
from . import views

app_name = 'psikoloji'

urlpatterns = [
    # URLهای اطلاعیه‌ها
    path('duyurular/', views.psikoloji_duyurulari, name='liste'),
    path('duyurular/<slug:slug>/', views.psikoloji_duyuru_detay, name='detay'),
    
    # URLهای صفحات استاتیک روانشناسی
    path('', views.psikoloji, name='psikoloji'),
    path('tarihce/', views.psikoloji_tarihce, name='psikoloji_tarihce'),
    path('misyon_visyon/', views.psikoloji_misyon_visyon, name='psikoloji_misyon_visyon'),
    path('psikoloji_yonetimi/', views.psikoloji_yonetimi, name='psikoloji_yonetimi'),
    path('iletişim/', views.iletişim, name='psikoloji_iletişim'),
    path('ogrenci_isleri/', views.ogrenci_isleri, name='ogrenci_isleri'),
    path('cift_anadal/', views.cift_anadal, name='cift_anadal'),
    path('erasmus/', views.erasmus, name='erasmus'),
    path('ders_programı/', views.ders_programı, name='ders_programı'),
    
    # URLهای فعالیت‌ها
    path('idari_faaliyetler_2024_2025/', views.idari_faaliyetler_2024_2025, name='psikoloji_idari_faaliyetler_2024_2025'),
    path('idari_faaliyetler_2023_2024/', views.idari_faaliyetler_2023_2024, name='psikoloji_idari_faaliyetler_2023_2024'),
    path('diğer_faaliyetler_2024_2025/', views.diğer_faaliyetler_2024_2025, name='psikoloji_diğer_faaliyetler_2024_2025'),
    path('diğer_faaliyetler_2023_2024/', views.diğer_faaliyetler_2023_2024, name='psikoloji_diğer_faaliyetler_2023_2024'),

    path('akreditasyon_belgesi/', views.akreditasyon_belgesi, name='akreditasyon_belgesi'),
    path('komisyon_sorumlular/', views.komisyon_sorumlular, name='komisyon_sorumlular'),
    path('program_ogretim_amacları/', views.program_ogretim_amacları, name='program_ogretim_amacları'),
    path('program_ogrenim_cıktıları/', views.program_ogrenim_cıktıları, name='program_ogrenim_cıktıları'),
    path('anketler/', views.anketler, name='anketler'),
    path('ders_planı/', views.ders_planı, name='ders_planı'),

    # ✅ اصلاح شده: نام‌های URL یکپارچه
    path('etkinlikler/', views.etkinlik_listesi, name='etkinlik_listesi'),
    path('etkinlikler/yaklasan/', views.yaklasan_etkinlikler, name='yaklasan_etkinlikler'),
    path('etkinlikler/<slug:slug>/', views.etkinlik_detay, name='etkinlik_detay'),



    path('kalite_yonetimik/', views.kalite_yonetimik, name='kalite_yonetimik'),

    path('toplumsal_katki/', views.toplumsal_katki, name='toplumsal_katki'),
]