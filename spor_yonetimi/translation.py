from modeltranslation.translator import TranslationOptions, register
from .models import SporYonetimiEtkinlik, SporYonetimiDersProgrami, SporYonetimiFaaliyetGrubu, SporYonetimiFaaliyet

@register(SporYonetimiEtkinlik)
class SporYonetimiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(SporYonetimiDersProgrami)
class SporYonetimiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(SporYonetimiFaaliyetGrubu)
class SporYonetimiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(SporYonetimiFaaliyet)
class SporYonetimiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

