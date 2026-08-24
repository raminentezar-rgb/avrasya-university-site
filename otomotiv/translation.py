from modeltranslation.translator import TranslationOptions, register
from .models import OtomotivEtkinlik, OtomotivDersProgrami, OtomotivFaaliyetGrubu, OtomotivFaaliyet

@register(OtomotivEtkinlik)
class OtomotivEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(OtomotivDersProgrami)
class OtomotivDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(OtomotivFaaliyetGrubu)
class OtomotivFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(OtomotivFaaliyet)
class OtomotivFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

