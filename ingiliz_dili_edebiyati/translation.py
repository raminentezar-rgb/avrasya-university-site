from modeltranslation.translator import TranslationOptions, register
from .models import Ing_Etkinlik, DersProgrami, IngilizDiliEdebiyatiFaaliyetGrubu, IngilizDiliEdebiyatiFaaliyet

@register(Ing_Etkinlik)
class Ing_EtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(DersProgrami)
class DersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(IngilizDiliEdebiyatiFaaliyetGrubu)
class IngilizDiliEdebiyatiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(IngilizDiliEdebiyatiFaaliyet)
class IngilizDiliEdebiyatiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

