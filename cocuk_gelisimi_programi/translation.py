from modeltranslation.translator import TranslationOptions, register
from .models import CocukGelisimiEtkinlik, CocukGelisimiDersProgrami, CocukGelisimiProgramiFaaliyetGrubu, CocukGelisimiProgramiFaaliyet

@register(CocukGelisimiEtkinlik)
class CocukGelisimiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(CocukGelisimiDersProgrami)
class CocukGelisimiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(CocukGelisimiProgramiFaaliyetGrubu)
class CocukGelisimiProgramiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(CocukGelisimiProgramiFaaliyet)
class CocukGelisimiProgramiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

