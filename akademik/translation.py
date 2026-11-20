from modeltranslation.translator import TranslationOptions, register
from .models import (
    FakulteSayfasi,
    FakulteBolumKarti,
    FakulteYonetimUyesi,
    FakulteEkSekme,
    BolumSayfasi,
    BolumYonetimUyesi,
    BolumEkSekme,
    BolumAkademikKadroUyesi,
)


@register(FakulteSayfasi)
class FakulteSayfasiTranslationOptions(TranslationOptions):
    fields = (
        'fakulte_adi',
        'hero_alt_baslik',
        'bolumler_baslik',
        'bolumler_alt_baslik',
        'bolumler_giris_icerik',
        'bolumler_liste_baslik',
        'bolumler_liste_aciklama',
        'istatistik_1_baslik',
        'istatistik_2_baslik',
        'istatistik_3_baslik',
        'istatistik_4_baslik',
        'tarihce_baslik',
        'tarihce_alt_baslik',
        'tarihce_icerik',
        'misyon_vizyon_baslik',
        'misyon_vizyon_alt_baslik',
        'misyon_vizyon_giris',
        'misyon_icerik',
        'vizyon_icerik',
        'temel_degerler_icerik',
        'mesaj_sekme_adi',
        'mesaj_alt_baslik',
        'yonetici_gorevi',
        'yonetici_unvan_rozet',
        'dekan_mesaji',
    )


@register(FakulteYonetimUyesi)
class FakulteYonetimUyesiTranslationOptions(TranslationOptions):
    fields = ('gorev',)


@register(FakulteBolumKarti)
class FakulteBolumKartiTranslationOptions(TranslationOptions):
    fields = ('ad', 'program_turu', 'egitim_dili', 'egitim_suresi', 'aciklama')


@register(FakulteEkSekme)
class FakulteEkSekmeTranslationOptions(TranslationOptions):
    fields = ('baslik', 'alt_baslik', 'icerik')


@register(BolumSayfasi)
class BolumSayfasiTranslationOptions(TranslationOptions):
    fields = (
        'bolum_adi',
        'fakulte_adi',
        'program_turu',
        'tarihce_baslik',
        'tarihce_alt_baslik',
        'tarihce_icerik',
        'misyon_vizyon_baslik',
        'misyon_vizyon_alt_baslik',
        'misyon_icerik',
        'vizyon_icerik',
        'amaclari_icerik',
        'ne_is_yaparlar_baslik',
        'ne_is_yaparlar_alt_baslik',
        'ne_is_yaparlar_icerik',
        'mezunlar_calisma_baslik',
        'mezunlar_calisma_alt_baslik',
        'mezunlar_calisma_icerik',
        'yonetim_baslik',
        'yonetim_alt_baslik',
        'baskan_gorev_etiketi',
        'baskan_unvan_detay',
        'baskan_mesaji',
        'kadro_baslik',
        'kadro_alt_baslik',
        'kadro_aciklama',
    )


@register(BolumYonetimUyesi)
class BolumYonetimUyesiTranslationOptions(TranslationOptions):
    fields = ('gorev',)


@register(BolumAkademikKadroUyesi)
class BolumAkademikKadroUyesiTranslationOptions(TranslationOptions):
    fields = ('unvan_gorev', 'uzmanlik_alani', 'biyografi')


@register(BolumEkSekme)
class BolumEkSekmeTranslationOptions(TranslationOptions):
    fields = ('baslik', 'alt_baslik', 'icerik')
