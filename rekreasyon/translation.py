from modeltranslation.translator import TranslationOptions, register
from .models import RekreasyonEtkinlik, RekreasyonDersProgrami, RekreasyonFaaliyetGrubu, RekreasyonFaaliyet

@register(RekreasyonEtkinlik)
class RekreasyonEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(RekreasyonDersProgrami)
class RekreasyonDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(RekreasyonFaaliyetGrubu)
class RekreasyonFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(RekreasyonFaaliyet)
class RekreasyonFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

