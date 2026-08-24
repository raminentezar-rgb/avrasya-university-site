from modeltranslation.translator import TranslationOptions, register
from .models import DisProteziEtkinlik, DisProteziDersProgrami, DisProteziFaaliyetGrubu, DisProteziFaaliyet

@register(DisProteziEtkinlik)
class DisProteziEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(DisProteziDersProgrami)
class DisProteziDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(DisProteziFaaliyetGrubu)
class DisProteziFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(DisProteziFaaliyet)
class DisProteziFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

