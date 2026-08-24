from modeltranslation.translator import TranslationOptions, register
from .models import WebTasarimiEtkinlik, WebTasarimiDersProgrami, WebTasarimiFaaliyetGrubu, WebTasarimiFaaliyet

@register(WebTasarimiEtkinlik)
class WebTasarimiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(WebTasarimiDersProgrami)
class WebTasarimiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(WebTasarimiFaaliyetGrubu)
class WebTasarimiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(WebTasarimiFaaliyet)
class WebTasarimiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

