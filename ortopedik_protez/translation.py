from modeltranslation.translator import TranslationOptions, register
from .models import OrtopedikProtezEtkinlik, OrtopedikProtezDersProgrami, OrtopedikProtezFaaliyetGrubu, OrtopedikProtezFaaliyet

@register(OrtopedikProtezEtkinlik)
class OrtopedikProtezEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(OrtopedikProtezDersProgrami)
class OrtopedikProtezDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(OrtopedikProtezFaaliyetGrubu)
class OrtopedikProtezFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(OrtopedikProtezFaaliyet)
class OrtopedikProtezFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

