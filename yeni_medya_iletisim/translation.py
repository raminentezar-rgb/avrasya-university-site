from modeltranslation.translator import TranslationOptions, register
from .models import YeniMedya_Etkinlik, YeniMedyaDersProgrami, YeniMedyaIletisimFaaliyetGrubu, YeniMedyaIletisimFaaliyet

@register(YeniMedya_Etkinlik)
class YeniMedya_EtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(YeniMedyaDersProgrami)
class YeniMedyaDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(YeniMedyaIletisimFaaliyetGrubu)
class YeniMedyaIletisimFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(YeniMedyaIletisimFaaliyet)
class YeniMedyaIletisimFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

