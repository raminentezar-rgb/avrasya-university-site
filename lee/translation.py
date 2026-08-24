from modeltranslation.translator import TranslationOptions, register
from .models import LeeDuyuru, LeeDosya, Lee_Etkinlik

@register(LeeDuyuru)
class LeeDuyuruTranslationOptions(TranslationOptions):
    fields = ('baslik', 'icerik', 'ozet')

@register(LeeDosya)
class LeeDosyaTranslationOptions(TranslationOptions):
    fields = ('aciklama',)

@register(Lee_Etkinlik)
class Lee_EtkinlikTranslationOptions(TranslationOptions):
    fields = ('baslik', 'kisa_aciklama', 'detayli_aciklama')

