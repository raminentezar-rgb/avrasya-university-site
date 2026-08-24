from modeltranslation.translator import TranslationOptions, register
from .models import TibbiLaboratuvarEtkinlik, TibbiLaboratuvarDersProgrami, TibbiLaboratuvarFaaliyetGrubu, TibbiLaboratuvarFaaliyet

@register(TibbiLaboratuvarEtkinlik)
class TibbiLaboratuvarEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(TibbiLaboratuvarDersProgrami)
class TibbiLaboratuvarDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(TibbiLaboratuvarFaaliyetGrubu)
class TibbiLaboratuvarFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(TibbiLaboratuvarFaaliyet)
class TibbiLaboratuvarFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

