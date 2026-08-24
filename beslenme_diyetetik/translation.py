from modeltranslation.translator import TranslationOptions, register
from .models import BeslenmeDiyetetikEtkinlik, BeslenmeDiyetetikDersProgrami, BeslenmeDiyetetikFaaliyetGrubu, BeslenmeDiyetetikFaaliyet

@register(BeslenmeDiyetetikEtkinlik)
class BeslenmeDiyetetikEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(BeslenmeDiyetetikDersProgrami)
class BeslenmeDiyetetikDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(BeslenmeDiyetetikFaaliyetGrubu)
class BeslenmeDiyetetikFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(BeslenmeDiyetetikFaaliyet)
class BeslenmeDiyetetikFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

