from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language  # این خط را اضافه کنید


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('news/', include('news.urls', namespace='news')),
    path('contact/', include('contact.urls',namespace='contact')),
    path('duyurular/', include('duyurular.urls')),
    path('etkinlikler/', include('etkinlikler.urls')), 
    path('aday_ogrenci/', include('aday_ogrenci.urls', namespace='aday_ogrenci')),
    path('akademik/', include('akademik.urls')),
    path('fakulteler/', include('fakulteler.urls')),
    path('enstituler/', include('enstituler.urls')),
    path('yuksekokullari/', include('yuksekokullari.urls')),
    path('meslekyuksekokullari/', include('meslekyuksekokullari.urls')),
    path('fen_edebiyat/', include('fen_edebiyat.urls')),
    path('iktisadi_idari/', include('iktisadi_idari.urls')),
    path('muhendislik_mimarlik/', include('muhendislik_mimarlik.urls')),
    path('saglik_bilimleri/', include('saglik_bilimleri.urls')),
    path('spor_bilimleri/', include('spor_bilimleri.urls')),
    path('iletisim/', include('iletisim.urls')),
    path('meslek_yuksekokulu/', include('meslek_yuksekokulu.urls')),
    path('saglik_hizmetleri_myo/', include('saglik_hizmetleri_myo.urls')),
    path('uygulamali_bilimler/', include('uygulamali_bilimler.urls')),
    path('psikoloji/', include('psikoloji.urls')),
    path('ingiliz_dili_edebiyati/', include('ingiliz_dili_edebiyati.urls')),
    path('turk_dili_edebiyati/', include('turk_dili_edebiyati.urls')),
    path('molekuler_biyoloji_genetik/', include('molekuler_biyoloji_genetik.urls')),
    path('mutercim_tercumanlik/', include('mutercim_tercumanlik.urls')),
    path('bilgisayar_muhendisligi/', include('bilgisayar_muhendisligi.urls')),
    path('elektrik_elektronik_muhendisligi/', include('elektrik_elektronik_muhendisligi.urls')),
    path('gida_muhendisligi/', include('gida_muhendisligi.urls')),
    path('harita_muhendisligi/', include('harita_muhendisligi.urls')),
    path('ic_mimarlik/', include('ic_mimarlik.urls')),
    path('insaat_muhendisligi/', include('insaat_muhendisligi.urls')),
    path('makine_muhendisligi/', include('makine_muhendisligi.urls')),
    path('mimarlik/', include('mimarlik.urls')),
    path('isletme/', include('isletme.urls')),
    path('isletme_ingilizce/', include('isletme_ingilizce.urls')),
    path('avrasya_universitesi_hakkinda/', include('avrasya_universitesi_hakkinda.urls')),
    path('siyaset_bilimi/', include('siyaset_bilimi.urls')),
    path('maliye/', include('maliye.urls')),
    path('uluslararasi_iliskiler/', include('uluslararasi_iliskiler.urls')),
    path('avrasya_universitesi_yonetim/', include('avrasya_universitesi_yonetim.urls')),
    path('beslenme_diyetetik/', include('beslenme_diyetetik.urls')),
    path('cocuk_gelisimi/', include('cocuk_gelisimi.urls')),
    path('ebelik/', include('ebelik.urls')),
    path('ergoterapi/', include('ergoterapi.urls')),
    path('fizyoterapi_rehabilitasyon/', include('fizyoterapi_rehabilitasyon.urls')),
    path('hemsirelik/', include('hemsirelik.urls')),
    path('kutuphane/', include('kutuphane.urls')),
    path('odyoloji/', include('odyoloji.urls')),
    path('saglik_yonetimi/', include('saglik_yonetimi.urls')),
    path('antrenorluk_egitimi/', include('antrenorluk_egitimi.urls')),
    path('egzersiz/', include('egzersiz.urls')),
    path('ogrenci_isleri/', include('ogrenci_isleri.urls')),
    path('spor_yoneticiligi/', include('spor_yoneticiligi.urls')),
    path('rekreasyon/', include('rekreasyon.urls')),
    path('yatay_gecis/', include('yatay_gecis.urls')),
    path('gallery/', include('gallery.urls')),
    path('yeni_medya_iletisim/', include('yeni_medya_iletisim.urls')),
    path('arastirma/', include('arastirma.urls')),
    path('international/', include('international.urls')),
    path('erasmus/', include('erasmus.urls')),
    path('lisansustu_egitim_enstitusu/', include('lee.urls')),
    path('support/', include('support.urls')),
    path('accounts/', include('accounts.urls')),
    path('gorsel_iletisim_tasarimi/', include('gorsel_iletisim_tasarimi.urls')),
    path('idari_birimler/', include('idari_birimler.urls')),


    #MYO 
    path('adalet/', include('adalet.urls')),
    path('ascilik/', include('ascilik.urls')),
    path('bilgisayar_programciligi/', include('bilgisayar_programciligi.urls')),
    path('bilisim_guvenligi/', include('bilisim_guvenligi.urls')),
    path('dis_ticaret/', include('dis_ticaret.urls')),
    path('e_ticaret/', include('e_ticaret.urls')),
    path('grafik_tasarimi/', include('grafik_tasarimi.urls')),
    path('halkla_iliskiler/', include('halkla_iliskiler.urls')),
    path('harita_kadastror/', include('harita_kadastro.urls')),
    path('ic_mekan/', include('ic_mekan.urls')),
    path('insaat_teknolojisi/', include('insaat_teknolojisi.urls')),
    path('lojistik_programi/', include('lojistik_programi.urls')),
    path('mimari_restorasyon/', include('mimari_restorasyon.urls')),
    path('mahkeme_buro/', include('mahkeme_buro.urls')),
    path('moda_tasarimi/', include('moda_tasarimi.urls')),
    path('otomotiv/', include('otomotiv.urls')),
    path('sivil_havacilik/', include('sivil_havacilik.urls')),
    path('sosyal_guvenlik/', include('sosyal_guvenlik.urls')),
    path('sosyal_hizmetler/', include('sosyal_hizmetler.urls')),
    path('spor_yonetimi/', include('spor_yonetimi.urls')),
    path('web_tasarimi/', include('web_tasarimi.urls')),

    #SHMYO
    path('acil_durum/', include('acil_durum.urls')),
    path('agiz_dis/', include('agiz_dis.urls')),
    path('ameliyathane_hizmetler/', include('ameliyathane.urls')),
    path('anestezi_programi/', include('anestezi.urls')),
    path('diyaliz_programi/', include('diyaliz.urls')),
    path('dis_protezi/', include('dis_protezi.urls')),
    path('elektronorofizyoloji/', include('elektronorofizyoloji.urls')),
    path('eczane_hizmetleri/', include('eczane.urls')),
    path('fizyoterapi_programi/', include('fizyoterapi.urls')),
    path('cocuk_gelisimi_programi/', include('cocuk_gelisimi_programi.urls')),
    path('ilk_acil_yardim/', include('ilk_acil_yardim.urls')),
    path('is_sagligi_guvenligi/', include('is_sagligi_guvenligi.urls')),
    path('is_ugrasi_terapisi/', include('is_ugrasi_terapisi.urls')),
    path('odyometri/', include('odyometri.urls')),
    path('optisyenlik/', include('optisyenlik.urls')),
    path('ortopedik_protez/', include('ortopedik_protez.urls')),
    path('patoloji_laboratuar_teknikleri/', include('patoloji_laboratuar.urls')),
    path('radyoterapi/', include('radyoterapi.urls')),
    path('saglik_kurumlari_isletmeciligi/', include('saglik_kurumlari.urls')),
    path('tibbi_goruntuleme_teknikleri/', include('tibbi_goruntuleme.urls')),
    path('tibbi_laboratuvar_teknikleri/', include('tibbi_laboratuvar.urls')),

    #UBYO
    path('yonetim_bilisim_sistemleri/', include('yonetim_bilisim_sistemleri.urls')),
    path('gastronomi_mutfak_sanatlari/', include('gastronomi_mutfak_sanatlari.urls')),
    
    
    

    
   
   
   
   
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
