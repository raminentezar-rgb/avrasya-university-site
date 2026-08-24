from modeltranslation.translator import TranslationOptions, register
from .models import AdaletEtkinlik, AdaletDersProgrami, AdaletFaaliyetGrubu, AdaletFaaliyet

@register(AdaletEtkinlik)
class AdaletEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(AdaletDersProgrami)
class AdaletDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(AdaletFaaliyetGrubu)
class AdaletFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(AdaletFaaliyet)
class AdaletFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

