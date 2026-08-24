from modeltranslation.translator import TranslationOptions, register
from .models import MeslekYuksekokuluDuyuru, MeslekYuksekokuluDosya

@register(MeslekYuksekokuluDuyuru)
class MeslekYuksekokuluDuyuruTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik', 'ozet')

@register(MeslekYuksekokuluDosya)
class MeslekYuksekokuluDosyaTranslationOptions(TranslationOptions):
    fields = ('aciklama',)

