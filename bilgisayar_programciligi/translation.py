from modeltranslation.translator import TranslationOptions, register
from .models import BilgisayarProgramciligiEtkinlik, BilgisayarProgramciligiDersProgrami, BilgisayarProgramciligiFaaliyetGrubu, BilgisayarProgramciligiFaaliyet

@register(BilgisayarProgramciligiEtkinlik)
class BilgisayarProgramciligiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(BilgisayarProgramciligiDersProgrami)
class BilgisayarProgramciligiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(BilgisayarProgramciligiFaaliyetGrubu)
class BilgisayarProgramciligiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(BilgisayarProgramciligiFaaliyet)
class BilgisayarProgramciligiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

