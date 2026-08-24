from modeltranslation.translator import TranslationOptions, register
from .models import EczaneEtkinlik, EczaneDersProgrami, EczaneFaaliyetGrubu, EczaneFaaliyet

@register(EczaneEtkinlik)
class EczaneEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(EczaneDersProgrami)
class EczaneDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(EczaneFaaliyetGrubu)
class EczaneFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(EczaneFaaliyet)
class EczaneFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

