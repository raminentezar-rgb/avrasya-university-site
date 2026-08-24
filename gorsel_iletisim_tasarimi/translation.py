from modeltranslation.translator import TranslationOptions, register
from .models import Gorsel_Etkinlik, GorselDersProgrami, GorselIletisimTasarimiFaaliyetGrubu, GorselIletisimTasarimiFaaliyet

@register(Gorsel_Etkinlik)
class Gorsel_EtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(GorselDersProgrami)
class GorselDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(GorselIletisimTasarimiFaaliyetGrubu)
class GorselIletisimTasarimiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(GorselIletisimTasarimiFaaliyet)
class GorselIletisimTasarimiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

