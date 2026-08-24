from modeltranslation.translator import TranslationOptions, register
from .models import MimariRestorasyonEtkinlik, MimariRestorasyonDersProgrami, MimariRestorasyonFaaliyetGrubu, MimariRestorasyonFaaliyet

@register(MimariRestorasyonEtkinlik)
class MimariRestorasyonEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(MimariRestorasyonDersProgrami)
class MimariRestorasyonDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(MimariRestorasyonFaaliyetGrubu)
class MimariRestorasyonFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(MimariRestorasyonFaaliyet)
class MimariRestorasyonFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

