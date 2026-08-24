from modeltranslation.translator import TranslationOptions, register
from .models import ModaTasarimiEtkinlik, ModaTasarimiDersProgrami, ModaTasarimiFaaliyetGrubu, ModaTasarimiFaaliyet

@register(ModaTasarimiEtkinlik)
class ModaTasarimiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(ModaTasarimiDersProgrami)
class ModaTasarimiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(ModaTasarimiFaaliyetGrubu)
class ModaTasarimiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(ModaTasarimiFaaliyet)
class ModaTasarimiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

