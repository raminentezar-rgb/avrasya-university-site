from modeltranslation.translator import TranslationOptions, register
from .models import LojistikProgramiEtkinlik, LojistikProgramiDersProgrami, LojistikProgramiFaaliyetGrubu, LojistikProgramiFaaliyet

@register(LojistikProgramiEtkinlik)
class LojistikProgramiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(LojistikProgramiDersProgrami)
class LojistikProgramiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(LojistikProgramiFaaliyetGrubu)
class LojistikProgramiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(LojistikProgramiFaaliyet)
class LojistikProgramiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

