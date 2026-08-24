from modeltranslation.translator import TranslationOptions, register
from .models import AntrenorlukEgitimiEtkinlik, AntrenorlukEgitimiDersProgrami, AntrenorlukEgitimiFaaliyetGrubu, AntrenorlukEgitimiFaaliyet

@register(AntrenorlukEgitimiEtkinlik)
class AntrenorlukEgitimiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(AntrenorlukEgitimiDersProgrami)
class AntrenorlukEgitimiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(AntrenorlukEgitimiFaaliyetGrubu)
class AntrenorlukEgitimiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(AntrenorlukEgitimiFaaliyet)
class AntrenorlukEgitimiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

