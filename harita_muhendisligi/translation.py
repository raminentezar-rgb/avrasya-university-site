from modeltranslation.translator import TranslationOptions, register
from .models import HaritaMuhendisligiEtkinlik, HaritaMuhendisligiDersProgrami, HaritaMuhendisligiFaaliyetGrubu, HaritaMuhendisligiFaaliyet

@register(HaritaMuhendisligiEtkinlik)
class HaritaMuhendisligiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(HaritaMuhendisligiDersProgrami)
class HaritaMuhendisligiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(HaritaMuhendisligiFaaliyetGrubu)
class HaritaMuhendisligiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(HaritaMuhendisligiFaaliyet)
class HaritaMuhendisligiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

