from modeltranslation.translator import TranslationOptions, register
from .models import IsletmeEtkinlik, IsletmeDersProgrami, IsletmeFaaliyetGrubu, IsletmeFaaliyet

@register(IsletmeEtkinlik)
class IsletmeEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(IsletmeDersProgrami)
class IsletmeDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(IsletmeFaaliyetGrubu)
class IsletmeFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(IsletmeFaaliyet)
class IsletmeFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

