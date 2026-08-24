from modeltranslation.translator import TranslationOptions, register
from .models import FizyoterapiEtkinlik, FizyoterapiDersProgrami, FizyoterapiFaaliyetGrubu, FizyoterapiFaaliyet

@register(FizyoterapiEtkinlik)
class FizyoterapiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(FizyoterapiDersProgrami)
class FizyoterapiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(FizyoterapiFaaliyetGrubu)
class FizyoterapiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(FizyoterapiFaaliyet)
class FizyoterapiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

