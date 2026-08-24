from modeltranslation.translator import TranslationOptions, register
from .models import MuterimTercumanlikEtkinlik, MuterimTercumanlikDersProgrami, MutercimTercumanlikFaaliyetGrubu, MutercimTercumanlikFaaliyet

@register(MuterimTercumanlikEtkinlik)
class MuterimTercumanlikEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(MuterimTercumanlikDersProgrami)
class MuterimTercumanlikDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(MutercimTercumanlikFaaliyetGrubu)
class MutercimTercumanlikFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(MutercimTercumanlikFaaliyet)
class MutercimTercumanlikFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

