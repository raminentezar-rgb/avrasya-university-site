from modeltranslation.translator import TranslationOptions, register
from .models import SosyalGuvenlikEtkinlik, SosyalGuvenlikDersProgrami, SosyalGuvenlikFaaliyetGrubu, SosyalGuvenlikFaaliyet

@register(SosyalGuvenlikEtkinlik)
class SosyalGuvenlikEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(SosyalGuvenlikDersProgrami)
class SosyalGuvenlikDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(SosyalGuvenlikFaaliyetGrubu)
class SosyalGuvenlikFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(SosyalGuvenlikFaaliyet)
class SosyalGuvenlikFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

