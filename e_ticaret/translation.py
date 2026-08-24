from modeltranslation.translator import TranslationOptions, register
from .models import ETicaretEtkinlik, ETicaretDersProgrami, ETicaretFaaliyetGrubu, ETicaretFaaliyet

@register(ETicaretEtkinlik)
class ETicaretEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(ETicaretDersProgrami)
class ETicaretDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(ETicaretFaaliyetGrubu)
class ETicaretFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(ETicaretFaaliyet)
class ETicaretFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

