from modeltranslation.translator import TranslationOptions, register
from .models import ErgoterapiEtkinlik, ErgoterapiDersProgrami, ErgoterapiFaaliyetGrubu, ErgoterapiFaaliyet

@register(ErgoterapiEtkinlik)
class ErgoterapiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(ErgoterapiDersProgrami)
class ErgoterapiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(ErgoterapiFaaliyetGrubu)
class ErgoterapiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(ErgoterapiFaaliyet)
class ErgoterapiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

