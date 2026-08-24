from modeltranslation.translator import TranslationOptions, register
from .models import AgizDisEtkinlik, AgizDisDersProgrami, AgizDisFaaliyetGrubu, AgizDisFaaliyet

@register(AgizDisEtkinlik)
class AgizDisEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(AgizDisDersProgrami)
class AgizDisDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(AgizDisFaaliyetGrubu)
class AgizDisFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(AgizDisFaaliyet)
class AgizDisFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

