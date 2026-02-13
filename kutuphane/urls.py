from django.urls import path
from . import views
app_name = 'kutuphane'

urlpatterns = [

    path('',views.kutuphane, name='kutuphane'),
    path('genel_bilgiler/', views.genel_bilgiler, name='genel_bilgiler'),
    path('acik_erisim/', views.acik_erisim, name='acik_erisim'),
    path('calisma_takvimi/', views.calisma_takvimi, name='calisma_takvimi'),
    path('hizli_baglantilar/', views.hizli_baglantilar, name='hizli_baglantilar'),
    path('iletisim/', views.iletisim, name='iletisim'),


]