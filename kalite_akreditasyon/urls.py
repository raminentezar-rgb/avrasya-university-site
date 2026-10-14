from django.urls import path
from . import views

app_name = 'kalite_akreditasyon'

urlpatterns = [
    # Ana Sayfa (Varsayılan olarak Hakkında veya Portal)
    path('', views.home, name='home'),

    # 1. Hakkında
    path('hakkinda/', views.hakkinda, name='hakkinda'),

    # 2. Duyurular
    path('duyurular/', views.duyurular, name='duyurular'),
    path('duyuru/<slug:slug>/', views.duyuru_detail, name='duyuru_detail'),

    # 3. Haberler
    path('haberler/', views.haberler, name='haberler'),
    path('haber/<slug:slug>/', views.haber_detail, name='haber_detail'),

    # 4. Mevzuat
    path('mevzuat/', views.mevzuat, name='mevzuat'),

    # 5. Takvim
    path('takvim/', views.takvim, name='takvim'),
    path('komisyon-calisma-takvimi/', views.komisyon_calisma_takvimi, name='komisyon_calisma_takvimi'),
    path('tamamlanan-calismalar/', views.tamamlanan_calismalar, name='tamamlanan_calismalar'),

    # Takım (Mevcut yapı uyumluluğu için)
    path('takim/', views.takim, name='takim'),

    # 6. Raporlar
    path('raporlar/', views.raporlar, name='raporlar'),
    path('kurum-ic-degerlendirme-raporlari/', views.kurum_ic_degerlendirme_raporlari, name='kurum_ic_degerlendirme_raporlari'),

    # 7. İzleme
    path('izleme/', views.izleme, name='izleme'),
    path('bidr-yukleme-sistemi/', views.bidr_yukleme_sistemi, name='bidr_yukleme_sistemi'),
    path('paydas-analizi-sonuclari/', views.paydas_analizi_sonuclari, name='paydas_analizi_sonuclari'),
    path('dis-degerlendirme/', views.dis_degerlendirme, name='dis_degerlendirme'),
    path('surec-degerlendirme/', views.surec_degerlendirme, name='surec_degerlendirme'),

    # 8. Doküman
    path('dokuman/', views.dokuman, name='dokuman'),

    # 9. S.S.S
    path('sss/', views.sss, name='sss'),
]
