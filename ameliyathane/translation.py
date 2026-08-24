from modeltranslation.translator import TranslationOptions, register
from .models import AmeliyathaneEtkinlik, AmeliyathaneDersProgrami, AmeliyathaneFaaliyetGrubu, AmeliyathaneFaaliyet

@register(AmeliyathaneEtkinlik)
class AmeliyathaneEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(AmeliyathaneDersProgrami)
class AmeliyathaneDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(AmeliyathaneFaaliyetGrubu)
class AmeliyathaneFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(AmeliyathaneFaaliyet)
class AmeliyathaneFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

