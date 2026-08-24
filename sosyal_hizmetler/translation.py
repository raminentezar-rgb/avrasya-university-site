from modeltranslation.translator import TranslationOptions, register
from .models import SosyalHizmetlerEtkinlik, SosyalHizmetlerDersProgrami, SosyalHizmetlerFaaliyetGrubu, SosyalHizmetlerFaaliyet

@register(SosyalHizmetlerEtkinlik)
class SosyalHizmetlerEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(SosyalHizmetlerDersProgrami)
class SosyalHizmetlerDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(SosyalHizmetlerFaaliyetGrubu)
class SosyalHizmetlerFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(SosyalHizmetlerFaaliyet)
class SosyalHizmetlerFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

