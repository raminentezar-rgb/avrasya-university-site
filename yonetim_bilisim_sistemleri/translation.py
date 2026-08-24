from modeltranslation.translator import TranslationOptions, register
from .models import YonetimBilisimEtkinlik, YonetimBilisimDersProgrami, YonetimBilisimSistemleriFaaliyetGrubu, YonetimBilisimSistemleriFaaliyet

@register(YonetimBilisimEtkinlik)
class YonetimBilisimEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(YonetimBilisimDersProgrami)
class YonetimBilisimDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(YonetimBilisimSistemleriFaaliyetGrubu)
class YonetimBilisimSistemleriFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(YonetimBilisimSistemleriFaaliyet)
class YonetimBilisimSistemleriFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

