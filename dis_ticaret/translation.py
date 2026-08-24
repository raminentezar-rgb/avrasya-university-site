from modeltranslation.translator import TranslationOptions, register
from .models import DisTicaretEtkinlik, DisTicaretDersProgrami, DisTicaretFaaliyetGrubu, DisTicaretFaaliyet

@register(DisTicaretEtkinlik)
class DisTicaretEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(DisTicaretDersProgrami)
class DisTicaretDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(DisTicaretFaaliyetGrubu)
class DisTicaretFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(DisTicaretFaaliyet)
class DisTicaretFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

