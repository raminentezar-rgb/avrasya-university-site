from modeltranslation.translator import TranslationOptions, register
from .models import IletisimDuyuru

@register(IletisimDuyuru)
class IletisimDuyuruTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik', 'ozet')

