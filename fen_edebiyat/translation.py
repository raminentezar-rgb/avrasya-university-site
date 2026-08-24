from modeltranslation.translator import TranslationOptions, register
from .models import FenEdebiyatDuyuru, FenEdebiyatDosya

@register(FenEdebiyatDuyuru)
class FenEdebiyatDuyuruTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik', 'ozet')

@register(FenEdebiyatDosya)
class FenEdebiyatDosyaTranslationOptions(TranslationOptions):
    fields = ('aciklama',)

