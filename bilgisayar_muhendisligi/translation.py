from modeltranslation.translator import TranslationOptions, register
from .models import BilgisayarMuhendisligiEtkinlik, BilgisayarMuhendisligiDersProgrami, BilgisayarMuhendisligiFaaliyetGrubu, BilgisayarMuhendisligiFaaliyet

@register(BilgisayarMuhendisligiEtkinlik)
class BilgisayarMuhendisligiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(BilgisayarMuhendisligiDersProgrami)
class BilgisayarMuhendisligiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(BilgisayarMuhendisligiFaaliyetGrubu)
class BilgisayarMuhendisligiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(BilgisayarMuhendisligiFaaliyet)
class BilgisayarMuhendisligiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

