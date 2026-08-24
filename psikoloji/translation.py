from modeltranslation.translator import TranslationOptions, register
from .models import PsikolojiEtkinlik, PsikolojiDersProgrami, PsikolojiFaaliyetGrubu, PsikolojiFaaliyet

@register(PsikolojiEtkinlik)
class PsikolojiEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(PsikolojiDersProgrami)
class PsikolojiDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(PsikolojiFaaliyetGrubu)
class PsikolojiFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(PsikolojiFaaliyet)
class PsikolojiFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

