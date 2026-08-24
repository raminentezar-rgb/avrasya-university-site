from modeltranslation.translator import TranslationOptions, register
from .models import EgzersizEtkinlik, EgzersizDersProgrami, EgzersizFaaliyetGrubu, EgzersizFaaliyet

@register(EgzersizEtkinlik)
class EgzersizEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(EgzersizDersProgrami)
class EgzersizDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(EgzersizFaaliyetGrubu)
class EgzersizFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(EgzersizFaaliyet)
class EgzersizFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

