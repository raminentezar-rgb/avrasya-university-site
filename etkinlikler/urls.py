from django.urls import path
from . import views

app_name = 'etkinlikler'

urlpatterns = [
    path('', views.etkinlik_listesi, name='liste'),
    path('yaklasan/', views.yaklasan_etkinlikler, name='yaklasan'),
    path('<slug:slug>/', views.etkinlik_detay, name='detay'),
]