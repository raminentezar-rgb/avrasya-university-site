from modeltranslation.translator import TranslationOptions, register
from .models import SaglikHizmetleriMYODuyuru, SaglikHizmetleriMYODosya

@register(SaglikHizmetleriMYODuyuru)
class SaglikHizmetleriMYODuyuruTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik', 'ozet')

@register(SaglikHizmetleriMYODosya)
class SaglikHizmetleriMYODosyaTranslationOptions(TranslationOptions):
    fields = ('aciklama',)

