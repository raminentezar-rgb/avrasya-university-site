from modeltranslation.translator import TranslationOptions, register
from .models import HemsirelikEtkinlik, HemsirelikDersProgrami, HemsirelikFaaliyetGrubu, HemsirelikFaaliyet

@register(HemsirelikEtkinlik)
class HemsirelikEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(HemsirelikDersProgrami)
class HemsirelikDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(HemsirelikFaaliyetGrubu)
class HemsirelikFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(HemsirelikFaaliyet)
class HemsirelikFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

