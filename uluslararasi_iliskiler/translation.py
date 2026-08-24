from modeltranslation.translator import TranslationOptions, register
from .models import UluslararasiIliskilerEtkinlik, UluslararasiIliskilerDersProgrami, UluslararasiIliskilerFaaliyetGrubu, UluslararasiIliskilerFaaliyet

@register(UluslararasiIliskilerEtkinlik)
class UluslararasiIliskilerEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(UluslararasiIliskilerDersProgrami)
class UluslararasiIliskilerDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(UluslararasiIliskilerFaaliyetGrubu)
class UluslararasiIliskilerFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(UluslararasiIliskilerFaaliyet)
class UluslararasiIliskilerFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

