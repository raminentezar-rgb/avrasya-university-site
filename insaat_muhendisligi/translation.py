from modeltranslation.translator import TranslationOptions, register
from .models import InsaatMuhendisligiEtkinlik, InsaatMuhendisligiDersProgrami, InsaatMuhendisligiFaaliyetGrubu, InsaatMuhendisligiFaaliyet

@register(InsaatMuhendisligiEtkinlik)
class InsaatMuhendisligiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(InsaatMuhendisligiDersProgrami)
class InsaatMuhendisligiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(InsaatMuhendisligiFaaliyetGrubu)
class InsaatMuhendisligiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(InsaatMuhendisligiFaaliyet)
class InsaatMuhendisligiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

