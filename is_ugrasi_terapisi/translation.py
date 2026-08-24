from modeltranslation.translator import TranslationOptions, register
from .models import IsUgrasiTerapisiEtkinlik, IsUgrasiTerapisiDersProgrami, IsUgrasiTerapisiFaaliyetGrubu, IsUgrasiTerapisiFaaliyet

@register(IsUgrasiTerapisiEtkinlik)
class IsUgrasiTerapisiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(IsUgrasiTerapisiDersProgrami)
class IsUgrasiTerapisiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(IsUgrasiTerapisiFaaliyetGrubu)
class IsUgrasiTerapisiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(IsUgrasiTerapisiFaaliyet)
class IsUgrasiTerapisiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

