from modeltranslation.translator import TranslationOptions, register
from .models import TurkDiliEdebiyatiEtkinlik, TurkDiliEdebiyatiDersProgrami, TurkDiliEdebiyatiFaaliyetGrubu, TurkDiliEdebiyatiFaaliyet

@register(TurkDiliEdebiyatiEtkinlik)
class TurkDiliEdebiyatiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(TurkDiliEdebiyatiDersProgrami)
class TurkDiliEdebiyatiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(TurkDiliEdebiyatiFaaliyetGrubu)
class TurkDiliEdebiyatiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(TurkDiliEdebiyatiFaaliyet)
class TurkDiliEdebiyatiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

