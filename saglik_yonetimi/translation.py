from modeltranslation.translator import TranslationOptions, register
from .models import SaglikYonetimiEtkinlik, SaglikYonetimiDersProgrami, SaglikYonetimiFaaliyetGrubu, SaglikYonetimiFaaliyet

@register(SaglikYonetimiEtkinlik)
class SaglikYonetimiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(SaglikYonetimiDersProgrami)
class SaglikYonetimiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(SaglikYonetimiFaaliyetGrubu)
class SaglikYonetimiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(SaglikYonetimiFaaliyet)
class SaglikYonetimiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

