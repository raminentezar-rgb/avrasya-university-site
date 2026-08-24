from modeltranslation.translator import TranslationOptions, register
from .models import MolekulerBiyolojiGenetikEtkinlik, MolekulerBiyolojiGenetikDersProgrami, MolekulerBiyolojiGenetikFaaliyetGrubu, MolekulerBiyolojiGenetikFaaliyet

@register(MolekulerBiyolojiGenetikEtkinlik)
class MolekulerBiyolojiGenetikEtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

@register(MolekulerBiyolojiGenetikDersProgrami)
class MolekulerBiyolojiGenetikDersProgramiTranslationOptions(TranslationOptions):
    fields = ('baslik', 'aciklama')

@register(MolekulerBiyolojiGenetikFaaliyetGrubu)
class MolekulerBiyolojiGenetikFaaliyetGrubuTranslationOptions(TranslationOptions):
    fields = ('baslik',)

@register(MolekulerBiyolojiGenetikFaaliyet)
class MolekulerBiyolojiGenetikFaaliyetTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik')

