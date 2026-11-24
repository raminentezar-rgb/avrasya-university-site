from django.urls import path
from .feeds import EtkinliklerFeed
from . import views

app_name = 'etkinlikler'

urlpatterns = [
    path('', views.etkinlik_listesi, name='liste'),
    path('yaklasan/', views.yaklasan_etkinlikler, name='yaklasan'),
    path('rss/', EtkinliklerFeed(), name='rss'),
    path('bildirim/abone/', views.etkinlik_bildirim_abone, name='bildirim_abone'),
    path('bildirim/iptal/<str:token>/', views.etkinlik_bildirim_iptal, name='bildirim_iptal'),
    path('<slug:slug>/takvim.ics', views.etkinlik_takvim_ics, name='takvim_ics'),
    path('<slug:slug>/kayit/', views.etkinlik_kayit_ol, name='kayit_ol'),
    path('<slug:slug>/', views.etkinlik_detay, name='detay'),
]
