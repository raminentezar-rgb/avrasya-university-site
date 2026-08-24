from modeltranslation.translator import TranslationOptions, register
from .models import AcilDurumEtkinlik, AcilDurumDersProgrami, AcilDurumFaaliyetGrubu, AcilDurumFaaliyet

@register(AcilDurumEtkinlik)
class AcilDurumEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(AcilDurumDersProgrami)
class AcilDurumDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(AcilDurumFaaliyetGrubu)
class AcilDurumFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(AcilDurumFaaliyet)
class AcilDurumFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

