from modeltranslation.translator import TranslationOptions, register
from .models import OdyolojiEtkinlik, OdyolojiDersProgrami, OdyolojiFaaliyetGrubu, OdyolojiFaaliyet

@register(OdyolojiEtkinlik)
class OdyolojiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(OdyolojiDersProgrami)
class OdyolojiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(OdyolojiFaaliyetGrubu)
class OdyolojiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(OdyolojiFaaliyet)
class OdyolojiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

