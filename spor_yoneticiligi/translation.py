from modeltranslation.translator import TranslationOptions, register
from .models import SporYoneticiligiEtkinlik, SporYoneticiligiDersProgrami, SporYoneticiligiFaaliyetGrubu, SporYoneticiligiFaaliyet

@register(SporYoneticiligiEtkinlik)
class SporYoneticiligiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(SporYoneticiligiDersProgrami)
class SporYoneticiligiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(SporYoneticiligiFaaliyetGrubu)
class SporYoneticiligiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(SporYoneticiligiFaaliyet)
class SporYoneticiligiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

