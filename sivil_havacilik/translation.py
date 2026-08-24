from modeltranslation.translator import TranslationOptions, register
from .models import SivilHavacilikEtkinlik, SivilHavacilikDersProgrami, SivilHavacilikFaaliyetGrubu, SivilHavacilikFaaliyet

@register(SivilHavacilikEtkinlik)
class SivilHavacilikEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(SivilHavacilikDersProgrami)
class SivilHavacilikDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(SivilHavacilikFaaliyetGrubu)
class SivilHavacilikFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(SivilHavacilikFaaliyet)
class SivilHavacilikFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

