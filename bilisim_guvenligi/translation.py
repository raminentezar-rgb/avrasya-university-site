from modeltranslation.translator import TranslationOptions, register
from .models import BilisimGuvenligiEtkinlik, BilisimGuvenligiDersProgrami, BilisimGuvenligiFaaliyetGrubu, BilisimGuvenligiFaaliyet

@register(BilisimGuvenligiEtkinlik)
class BilisimGuvenligiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(BilisimGuvenligiDersProgrami)
class BilisimGuvenligiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(BilisimGuvenligiFaaliyetGrubu)
class BilisimGuvenligiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(BilisimGuvenligiFaaliyet)
class BilisimGuvenligiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

