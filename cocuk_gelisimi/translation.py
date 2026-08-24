from modeltranslation.translator import TranslationOptions, register
from .models import CocukGelisimiEtkinlik, CocukGelisimiDersProgrami, CocukGelisimiFaaliyetGrubu, CocukGelisimiFaaliyet

@register(CocukGelisimiEtkinlik)
class CocukGelisimiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(CocukGelisimiDersProgrami)
class CocukGelisimiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(CocukGelisimiFaaliyetGrubu)
class CocukGelisimiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(CocukGelisimiFaaliyet)
class CocukGelisimiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

