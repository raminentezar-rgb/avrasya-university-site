from modeltranslation.translator import TranslationOptions, register
from .models import HalklaIliskilerEtkinlik, HalklaIliskilerDersProgrami, HalklaIliskilerFaaliyetGrubu, HalklaIliskilerFaaliyet

@register(HalklaIliskilerEtkinlik)
class HalklaIliskilerEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(HalklaIliskilerDersProgrami)
class HalklaIliskilerDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(HalklaIliskilerFaaliyetGrubu)
class HalklaIliskilerFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(HalklaIliskilerFaaliyet)
class HalklaIliskilerFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

