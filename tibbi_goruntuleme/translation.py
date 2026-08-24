from modeltranslation.translator import TranslationOptions, register
from .models import TibbiGoruntulemeEtkinlik, TibbiGoruntulemeDersProgrami, TibbiGoruntulemeFaaliyetGrubu, TibbiGoruntulemeFaaliyet

@register(TibbiGoruntulemeEtkinlik)
class TibbiGoruntulemeEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(TibbiGoruntulemeDersProgrami)
class TibbiGoruntulemeDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(TibbiGoruntulemeFaaliyetGrubu)
class TibbiGoruntulemeFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(TibbiGoruntulemeFaaliyet)
class TibbiGoruntulemeFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

