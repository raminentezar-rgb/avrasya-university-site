from modeltranslation.translator import TranslationOptions, register
from .models import SiyasetBilimiEtkinlik, SiyasetBilimiDersProgrami, SiyasetBilimiFaaliyetGrubu, SiyasetBilimiFaaliyet

@register(SiyasetBilimiEtkinlik)
class SiyasetBilimiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(SiyasetBilimiDersProgrami)
class SiyasetBilimiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(SiyasetBilimiFaaliyetGrubu)
class SiyasetBilimiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(SiyasetBilimiFaaliyet)
class SiyasetBilimiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

