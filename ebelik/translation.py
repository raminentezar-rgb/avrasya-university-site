from modeltranslation.translator import TranslationOptions, register
from .models import EbelikEtkinlik, EbelikDersProgrami, EbelikFaaliyetGrubu, EbelikFaaliyet

@register(EbelikEtkinlik)
class EbelikEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(EbelikDersProgrami)
class EbelikDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(EbelikFaaliyetGrubu)
class EbelikFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(EbelikFaaliyet)
class EbelikFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

