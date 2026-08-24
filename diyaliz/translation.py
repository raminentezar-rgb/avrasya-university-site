from modeltranslation.translator import TranslationOptions, register
from .models import DiyalizEtkinlik, DiyalizDersProgrami, DiyalizFaaliyetGrubu, DiyalizFaaliyet

@register(DiyalizEtkinlik)
class DiyalizEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(DiyalizDersProgrami)
class DiyalizDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(DiyalizFaaliyetGrubu)
class DiyalizFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(DiyalizFaaliyet)
class DiyalizFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

