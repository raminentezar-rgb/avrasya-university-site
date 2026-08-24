from modeltranslation.translator import TranslationOptions, register
from .models import UygulamaliBilimlerDuyuru, UygulamaliBilimlerDosya

@register(UygulamaliBilimlerDuyuru)
class UygulamaliBilimlerDuyuruTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik', 'ozet')

@register(UygulamaliBilimlerDosya)
class UygulamaliBilimlerDosyaTranslationOptions(TranslationOptions):
    fields = ('aciklama',)

