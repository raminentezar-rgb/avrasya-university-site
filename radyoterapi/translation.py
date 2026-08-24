from modeltranslation.translator import TranslationOptions, register
from .models import RadyoterapiEtkinlik, RadyoterapiDersProgrami, RadyoterapiFaaliyetGrubu, RadyoterapiFaaliyet

@register(RadyoterapiEtkinlik)
class RadyoterapiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(RadyoterapiDersProgrami)
class RadyoterapiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(RadyoterapiFaaliyetGrubu)
class RadyoterapiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(RadyoterapiFaaliyet)
class RadyoterapiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

