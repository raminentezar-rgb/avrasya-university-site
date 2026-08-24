from modeltranslation.translator import TranslationOptions, register
from .models import IsletmeIngilizceEtkinlik, IsletmeIngilizceDersProgrami, IsletmeIngilizceFaaliyetGrubu, IsletmeIngilizceFaaliyet

@register(IsletmeIngilizceEtkinlik)
class IsletmeIngilizceEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(IsletmeIngilizceDersProgrami)
class IsletmeIngilizceDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(IsletmeIngilizceFaaliyetGrubu)
class IsletmeIngilizceFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(IsletmeIngilizceFaaliyet)
class IsletmeIngilizceFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

