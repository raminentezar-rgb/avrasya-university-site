from modeltranslation.translator import TranslationOptions, register
from .models import IcMekanEtkinlik, IcMekanDersProgrami, IcMekanFaaliyetGrubu, IcMekanFaaliyet

@register(IcMekanEtkinlik)
class IcMekanEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(IcMekanDersProgrami)
class IcMekanDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(IcMekanFaaliyetGrubu)
class IcMekanFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(IcMekanFaaliyet)
class IcMekanFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

