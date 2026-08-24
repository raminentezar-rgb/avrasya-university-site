from modeltranslation.translator import TranslationOptions, register
from .models import IktisadiIdariDuyuru, IktisadiIdariDosya

@register(IktisadiIdariDuyuru)
class IktisadiIdariDuyuruTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik', 'ozet')

@register(IktisadiIdariDosya)
class IktisadiIdariDosyaTranslationOptions(TranslationOptions):
    fields = ('aciklama',)

