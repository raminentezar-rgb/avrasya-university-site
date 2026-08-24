from modeltranslation.translator import TranslationOptions, register
from .models import PatolojiLaboratuarEtkinlik, PatolojiLaboratuarDersProgrami, PatolojiLaboratuarFaaliyetGrubu, PatolojiLaboratuarFaaliyet

@register(PatolojiLaboratuarEtkinlik)
class PatolojiLaboratuarEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(PatolojiLaboratuarDersProgrami)
class PatolojiLaboratuarDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(PatolojiLaboratuarFaaliyetGrubu)
class PatolojiLaboratuarFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(PatolojiLaboratuarFaaliyet)
class PatolojiLaboratuarFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

