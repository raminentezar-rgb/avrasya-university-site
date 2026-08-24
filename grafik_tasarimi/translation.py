from modeltranslation.translator import TranslationOptions, register
from .models import GrafikTasarimiEtkinlik, GrafikTasarimiDersProgrami, GrafikTasarimiFaaliyetGrubu, GrafikTasarimiFaaliyet

@register(GrafikTasarimiEtkinlik)
class GrafikTasarimiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(GrafikTasarimiDersProgrami)
class GrafikTasarimiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(GrafikTasarimiFaaliyetGrubu)
class GrafikTasarimiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(GrafikTasarimiFaaliyet)
class GrafikTasarimiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

