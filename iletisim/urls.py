# iletisim/urls.py
from django.urls import path
from . import views

app_name = 'iletisim'

urlpatterns = [
    # صفحات اصلی
    path('', views.iletisim_anasayfa, name='iletisim_anasayfa'),
    path('akademik_kadro/', views.akademik_kadro, name='akademik_kadro'),
    path('kalite/', views.kalite, name='kalite'),
    path('fakulte_yonetimi/', views.fakulte_yonetimi, name='fakulte_yonetimi'),
    
    # اطلاعیه‌ها
    path('duyurular/', views.duyurular, name='duyurular'),
    path('duyurular/<int:id>/', views.duyuru_detay, name='duyuru_detay'),
    
    # خدمات ارتباطی
    path('servisler/', views.servisler, name='servisler'),
    path('teknoloji/', views.teknoloji, name='teknoloji'),
    path('medya/', views.medya, name='medya'),
    
    # تماس
    path('iletisim-bilgileri/', views.iletisim_bilgileri, name='iletisim_bilgileri'),
    path('sikca-sorulan-sorular/', views.sss, name='sss'),
    path('formlar/', views.formlar, name='formlar'),
    
    # سایر
    path('acil-durum/', views.acil_durum, name='acil_durum'),
    path('sosyal-medya/', views.sosyal_medya, name='sosyal_medya'),
]