from modeltranslation.translator import TranslationOptions, register
from .models import MimarlikEtkinlik, MimarlikDersProgrami, MimarlikFaaliyetGrubu, MimarlikFaaliyet

@register(MimarlikEtkinlik)
class MimarlikEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(MimarlikDersProgrami)
class MimarlikDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(MimarlikFaaliyetGrubu)
class MimarlikFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(MimarlikFaaliyet)
class MimarlikFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

