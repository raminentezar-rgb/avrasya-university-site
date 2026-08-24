from modeltranslation.translator import TranslationOptions, register
from .models import OptisyenlikEtkinlik, OptisyenlikDersProgrami, OptisyenlikFaaliyetGrubu, OptisyenlikFaaliyet

@register(OptisyenlikEtkinlik)
class OptisyenlikEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(OptisyenlikDersProgrami)
class OptisyenlikDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(OptisyenlikFaaliyetGrubu)
class OptisyenlikFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(OptisyenlikFaaliyet)
class OptisyenlikFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

