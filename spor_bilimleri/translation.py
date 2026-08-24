from modeltranslation.translator import TranslationOptions, register
from .models import SporBilimleriDuyuru

@register(SporBilimleriDuyuru)
class SporBilimleriDuyuruTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik', 'ozet')

