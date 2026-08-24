from modeltranslation.translator import TranslationOptions, register
from .models import Etkinlik

@register(Etkinlik)
class EtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

