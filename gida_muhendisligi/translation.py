from modeltranslation.translator import TranslationOptions, register
from .models import GidaMuhendisligiEtkinlik, GidaMuhendisligiDersProgrami, GidaMuhendisligiFaaliyetGrubu, GidaMuhendisligiFaaliyet

@register(GidaMuhendisligiEtkinlik)
class GidaMuhendisligiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(GidaMuhendisligiDersProgrami)
class GidaMuhendisligiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(GidaMuhendisligiFaaliyetGrubu)
class GidaMuhendisligiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(GidaMuhendisligiFaaliyet)
class GidaMuhendisligiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

