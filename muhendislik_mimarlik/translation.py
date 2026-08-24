from modeltranslation.translator import TranslationOptions, register
from .models import MuhendislikMimarlikDuyuru

@register(MuhendislikMimarlikDuyuru)
class MuhendislikMimarlikDuyuruTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik', 'ozet')

