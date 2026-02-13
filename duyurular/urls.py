from django.urls import path
from . import views

app_name = 'duyurular'

urlpatterns = [
    path('', views.duyuru_listesi, name='liste'),
    path('fakulte/<str:fakulte_kodu>/', views.fakulte_duyurulari, name='fakulte_liste'),
    path('bolum/<str:bolum_kodu>/', views.bolum_duyurulari, name='bolum_liste'),
    path('<slug:slug>/', views.duyuru_detay, name='detay'),
]