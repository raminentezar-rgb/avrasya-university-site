from modeltranslation.translator import TranslationOptions, register
from .models import Bolum, Duyuru, DuyuruDosya

@register(Bolum)
class BolumTranslationOptions(TranslationOptions):
    fields = ('ad', 'aciklama')

@register(Duyuru)
class DuyuruTranslationOptions(TranslationOptions):
    fields = ('baslik', 'ozet', 'icerik')

@register(DuyuruDosya)
class DuyuruDosyaTranslationOptions(TranslationOptions):
    fields = ('aciklama',)

