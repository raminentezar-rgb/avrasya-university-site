from modeltranslation.translator import TranslationOptions, register
from .models import OdyometriEtkinlik, OdyometriDersProgrami, OdyometriFaaliyetGrubu, OdyometriFaaliyet

@register(OdyometriEtkinlik)
class OdyometriEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(OdyometriDersProgrami)
class OdyometriDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(OdyometriFaaliyetGrubu)
class OdyometriFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(OdyometriFaaliyet)
class OdyometriFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

