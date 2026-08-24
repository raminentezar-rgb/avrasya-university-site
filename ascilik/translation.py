from modeltranslation.translator import TranslationOptions, register
from .models import Ascilik_Etkinlik, AscilikDersProgrami, AscilikFaaliyetGrubu, AscilikFaaliyet

@register(Ascilik_Etkinlik)
class Ascilik_EtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(AscilikDersProgrami)
class AscilikDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(AscilikFaaliyetGrubu)
class AscilikFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(AscilikFaaliyet)
class AscilikFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

