from django.urls import path
from . import views

app_name = 'arastirma'

urlpatterns = [
    path('', views.research_home, name='home'),
    
    # Policies
    path('politikalar/', views.policy_list, name='policy_list'),
    path('politikalar/<int:pk>/', views.policy_detail, name='policy_detail'),
    
    # BAP
    path('bap/', views.bap_list, name='bap_list'),
    path('bap/<int:project_id>/', views.bap_detail, name='bap_detail'),
    path('bap-komisyonu/', views.bap_komisyonu, name='bap_komisyonu'),
    path('bap-bilim-insani/', views.bap_bilim_insani, name='bap_bilim_insani'),
    path('bap-koordinatorlugu/', views.bap_koordinatorlugu, name='bap_koordinatorlugu'),
    
    # Laboratories
    path('laboratuvarlar/', views.lab_list, name='lab_list'),
    path('laboratuvarlar/<int:lab_id>/', views.lab_detail, name='lab_detail'),

    # Research Policies
    path('arastirma-politikalari-danisma-kurulu/', views.arastirma_politikalari_danisma_kurulu, name='arastirma_politikalari_danisma_kurulu'),
    path('arastirma-politikalari-komisyonu/', views.arastirma_politikalari_komisyonu, name='arastirma_politikalari_komisyonu'),

    # Other Pages
    path('arastirma-merkezleri/', views.arastirma_merkezleri, name='arastirma_merkezleri'),
    path('fikri-sinai-mulkiyet/', views.fikri_Sinai_mulkiyet, name='fikri_Sinai_mulkiyet'),
    path('arastirma-ciktilari/', views.arastirma_ciktilari, name='arastirma_ciktilari'),
    path('oduller/', views.oduller, name='oduller'),



    path('kadin_calismalari/', views.kadin, name='kadin'),
    path('bagimlilikla_mucadele/', views.bagimlilikla_mucadele, name='bagimlilikla_mucadele'),
    path('uzaktan_egitim/', views.uzaktan_egitim, name='uzaktan_egitim'),
    path('girisimcilik_yenilikcilik/', views.girisimcilik_yenilikcilik, name='girisimcilik_yenilikcilik'),
    path('gida_egitim/', views.gida_egitim, name='gida_egitim'),
    path('goc_calismalari/', views.goc_calismalari, name='goc_calismalari'),
    path('turkce_ogretimi/', views.turkce_ogretimi, name='turkce_ogretimi'),
    path('kariyer_gelistirme/', views.kariyer_gelistirme, name='kariyer_gelistirme'),
    path('ulastirma_uygulama/', views.ulastirma_uygulama, name='ulastirma_uygulama'),
    path('teknoloji_transfer/', views.teknoloji_transfer, name='teknoloji_transfer'),
    path('surekli_egitim/', views.surekli_egitim, name='surekli_egitim'),
    
]