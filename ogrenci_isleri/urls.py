from django.urls import path
from . import views

app_name = 'ogrenci_isleri'

urlpatterns = [
    path('',views.ogrenci_isleri,name='ogrenci_isleri'),
    path('daire_baskanligi/',views.daire_baskanligi,name='daire_baskanligi'),
    path('ogrenim_ucretleri/',views.ogrenim_ucretleri,name='ogrenim_ucretleri'),
    path('kayit_islemleri/',views.kayit,name='kayit'),
    path('burslar_indirimler/',views.burslar,name='burslar'),
    path('yurtlar/',views.yurtlar,name='yurtlar'),
    path('muafiyetler/',views.muafiyetler,name='muafiyetler'),
    path('kulupler/',views.kulupler,name='kulupler'),
    path('yonetmelik/',views.yonetmelik,name='yonetmelik'),
    path('formlar/',views.formlar,name='formlar'),
    path('dikey_gecis/',views.dikey,name='dikey'),
    path('erasmus/',views.erasmus,name='erasmus'),
    path('api/payment-submit/', views.submit_payment_form, name='submit_payment_form'),
    path('api/registration-submit/', views.submit_registration_form, name='submit_registration_form'),
]
