from modeltranslation.translator import TranslationOptions, register
from .models import MakineMuhendisligiEtkinlik, MakineMuhendisligiDersProgrami, MakineMuhendisligiFaaliyetGrubu, MakineMuhendisligiFaaliyet

@register(MakineMuhendisligiEtkinlik)
class MakineMuhendisligiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(MakineMuhendisligiDersProgrami)
class MakineMuhendisligiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(MakineMuhendisligiFaaliyetGrubu)
class MakineMuhendisligiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(MakineMuhendisligiFaaliyet)
class MakineMuhendisligiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

