from modeltranslation.translator import TranslationOptions, register
from .models import AnesteziEtkinlik, AnesteziDersProgrami, AnesteziFaaliyetGrubu, AnesteziFaaliyet

@register(AnesteziEtkinlik)
class AnesteziEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(AnesteziDersProgrami)
class AnesteziDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(AnesteziFaaliyetGrubu)
class AnesteziFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(AnesteziFaaliyet)
class AnesteziFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

