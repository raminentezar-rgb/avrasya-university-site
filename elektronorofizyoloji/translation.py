from modeltranslation.translator import TranslationOptions, register
from .models import ElektronorofizyolojiEtkinlik, ElektronorofizyolojiDersProgrami, ElektronorofizyolojiFaaliyetGrubu, ElektronorofizyolojiFaaliyet

@register(ElektronorofizyolojiEtkinlik)
class ElektronorofizyolojiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(ElektronorofizyolojiDersProgrami)
class ElektronorofizyolojiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(ElektronorofizyolojiFaaliyetGrubu)
class ElektronorofizyolojiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(ElektronorofizyolojiFaaliyet)
class ElektronorofizyolojiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

