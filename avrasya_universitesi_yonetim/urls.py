# avrasya_universitesi_yonetim/urls.py
from django.urls import path
from . import views

app_name = 'avrasya_universitesi_yonetim'

urlpatterns = [
    path('mutevelli-heyeti/', views.mutevelli_heyeti, name='mutevelli_heyeti'),
    path('mutevelli-heyet-baskani/', views.mutevelli_heyet_baskani, name='mutevelli_heyet_baskani'),
    path('rektor/', views.rektor, name='rektor'),
    path('rektor-yardimcilari/', views.rektor_yardimcilari, name='rektor_yardimcilari'),
    path('dekanlar/', views.dekanlar, name='dekanlar'),
    path('genel-sekreter/', views.genel_sekreter, name='genel_sekreter'),
    path('universite-senatosu/', views.universite_senatosu, name='universite_senatosu'),
    path('yonetim-kurulu/', views.yonetim_kurulu, name='yonetim_kurulu'),
]