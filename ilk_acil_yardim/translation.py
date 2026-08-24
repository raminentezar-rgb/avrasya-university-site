from modeltranslation.translator import TranslationOptions, register
from .models import IlkAcilYardimEtkinlik, IlkAcilYardimDersProgrami, IlkAcilYardimFaaliyetGrubu, IlkAcilYardimFaaliyet

@register(IlkAcilYardimEtkinlik)
class IlkAcilYardimEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(IlkAcilYardimDersProgrami)
class IlkAcilYardimDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(IlkAcilYardimFaaliyetGrubu)
class IlkAcilYardimFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(IlkAcilYardimFaaliyet)
class IlkAcilYardimFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

