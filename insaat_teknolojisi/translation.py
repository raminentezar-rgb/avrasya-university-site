from modeltranslation.translator import TranslationOptions, register
from .models import InsaatTeknolojisiEtkinlik, InsaatTeknolojisiDersProgrami, InsaatTeknolojisiFaaliyetGrubu, InsaatTeknolojisiFaaliyet

@register(InsaatTeknolojisiEtkinlik)
class InsaatTeknolojisiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(InsaatTeknolojisiDersProgrami)
class InsaatTeknolojisiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(InsaatTeknolojisiFaaliyetGrubu)
class InsaatTeknolojisiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(InsaatTeknolojisiFaaliyet)
class InsaatTeknolojisiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

