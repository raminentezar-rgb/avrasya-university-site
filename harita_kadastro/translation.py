from modeltranslation.translator import TranslationOptions, register
from .models import HaritaKadastroEtkinlik, HaritaKadastroDersProgrami, HaritaKadastroFaaliyetGrubu, HaritaKadastroFaaliyet

@register(HaritaKadastroEtkinlik)
class HaritaKadastroEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(HaritaKadastroDersProgrami)
class HaritaKadastroDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(HaritaKadastroFaaliyetGrubu)
class HaritaKadastroFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(HaritaKadastroFaaliyet)
class HaritaKadastroFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

