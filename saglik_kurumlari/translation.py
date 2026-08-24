from modeltranslation.translator import TranslationOptions, register
from .models import SaglikKurumlariEtkinlik, SaglikKurumlariDersProgrami, SaglikKurumlariFaaliyetGrubu, SaglikKurumlariFaaliyet

@register(SaglikKurumlariEtkinlik)
class SaglikKurumlariEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(SaglikKurumlariDersProgrami)
class SaglikKurumlariDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(SaglikKurumlariFaaliyetGrubu)
class SaglikKurumlariFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(SaglikKurumlariFaaliyet)
class SaglikKurumlariFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

