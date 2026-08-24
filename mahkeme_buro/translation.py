from modeltranslation.translator import TranslationOptions, register
from .models import MahkemeBuroEtkinlik, MahkemeBuroDersProgrami, MahkemeBuroFaaliyetGrubu, MahkemeBuroFaaliyet

@register(MahkemeBuroEtkinlik)
class MahkemeBuroEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(MahkemeBuroDersProgrami)
class MahkemeBuroDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(MahkemeBuroFaaliyetGrubu)
class MahkemeBuroFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(MahkemeBuroFaaliyet)
class MahkemeBuroFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

