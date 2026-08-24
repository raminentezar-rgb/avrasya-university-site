from modeltranslation.translator import TranslationOptions, register
from .models import IsSagligiGuvenligiEtkinlik, IsSagligiGuvenligiDersProgrami, IsSagligiGuvenligiFaaliyetGrubu, IsSagligiGuvenligiFaaliyet

@register(IsSagligiGuvenligiEtkinlik)
class IsSagligiGuvenligiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(IsSagligiGuvenligiDersProgrami)
class IsSagligiGuvenligiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(IsSagligiGuvenligiFaaliyetGrubu)
class IsSagligiGuvenligiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(IsSagligiGuvenligiFaaliyet)
class IsSagligiGuvenligiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

