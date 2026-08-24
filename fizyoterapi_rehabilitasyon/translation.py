from modeltranslation.translator import TranslationOptions, register
from .models import FizyoterapiRehabilitasyonEtkinlik, FizyoterapiRehabilitasyonDersProgrami, FizyoterapiRehabilitasyonFaaliyetGrubu, FizyoterapiRehabilitasyonFaaliyet

@register(FizyoterapiRehabilitasyonEtkinlik)
class FizyoterapiRehabilitasyonEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(FizyoterapiRehabilitasyonDersProgrami)
class FizyoterapiRehabilitasyonDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(FizyoterapiRehabilitasyonFaaliyetGrubu)
class FizyoterapiRehabilitasyonFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(FizyoterapiRehabilitasyonFaaliyet)
class FizyoterapiRehabilitasyonFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

