from modeltranslation.translator import TranslationOptions, register
from .models import SosyalHizmetEtkinlik, SosyalHizmetDersProgrami, SosyalHizmetFaaliyetGrubu, SosyalHizmetFaaliyet

@register(SosyalHizmetEtkinlik)
class SosyalHizmetEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(SosyalHizmetDersProgrami)
class SosyalHizmetDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(SosyalHizmetFaaliyetGrubu)
class SosyalHizmetFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(SosyalHizmetFaaliyet)
class SosyalHizmetFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

