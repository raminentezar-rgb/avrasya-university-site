from modeltranslation.translator import TranslationOptions, register
from .models import GastronomiEtkinlik, GastronomiDersProgrami, GastronomiMutfakSanatlariFaaliyetGrubu, GastronomiMutfakSanatlariFaaliyet

@register(GastronomiEtkinlik)
class GastronomiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(GastronomiDersProgrami)
class GastronomiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(GastronomiMutfakSanatlariFaaliyetGrubu)
class GastronomiMutfakSanatlariFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(GastronomiMutfakSanatlariFaaliyet)
class GastronomiMutfakSanatlariFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

