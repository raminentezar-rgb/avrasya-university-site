from modeltranslation.translator import TranslationOptions, register
from .models import MaliyeEtkinlik, MaliyeDersProgrami, MaliyeFaaliyetGrubu, MaliyeFaaliyet

@register(MaliyeEtkinlik)
class MaliyeEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(MaliyeDersProgrami)
class MaliyeDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(MaliyeFaaliyetGrubu)
class MaliyeFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(MaliyeFaaliyet)
class MaliyeFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

