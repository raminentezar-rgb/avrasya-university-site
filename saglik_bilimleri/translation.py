from modeltranslation.translator import TranslationOptions, register
from .models import SaglikBilimleriDuyuru, SaglikBilimleriDosya

@register(SaglikBilimleriDuyuru)
class SaglikBilimleriDuyuruTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik', 'ozet')

@register(SaglikBilimleriDosya)
class SaglikBilimleriDosyaTranslationOptions(TranslationOptions):
    fields = ('aciklama',)

