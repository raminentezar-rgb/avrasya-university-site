from modeltranslation.translator import TranslationOptions, register
from .models import ElektrikElektronikMuhendisligiEtkinlik, ElektrikElektronikMuhendisligiDersProgrami, ElektrikElektronikMuhendisligiFaaliyetGrubu, ElektrikElektronikMuhendisligiFaaliyet

@register(ElektrikElektronikMuhendisligiEtkinlik)
class ElektrikElektronikMuhendisligiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(ElektrikElektronikMuhendisligiDersProgrami)
class ElektrikElektronikMuhendisligiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(ElektrikElektronikMuhendisligiFaaliyetGrubu)
class ElektrikElektronikMuhendisligiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(ElektrikElektronikMuhendisligiFaaliyet)
class ElektrikElektronikMuhendisligiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

