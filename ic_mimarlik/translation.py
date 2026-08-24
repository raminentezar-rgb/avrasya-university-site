from modeltranslation.translator import TranslationOptions, register
from .models import IcMimarlikEtkinlik, IcMimarlikDersProgrami, IcMimarlikFaaliyetGrubu, IcMimarlikFaaliyet

@register(IcMimarlikEtkinlik)
class IcMimarlikEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(IcMimarlikDersProgrami)
class IcMimarlikDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(IcMimarlikFaaliyetGrubu)
class IcMimarlikFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(IcMimarlikFaaliyet)
class IcMimarlikFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

