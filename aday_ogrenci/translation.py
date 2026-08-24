from modeltranslation.translator import TranslationOptions, register
from .models import AdayMenu, AdaySayfa, AdaySlider

@register(AdayMenu)
class AdayMenuTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(AdaySayfa)
class AdaySayfaTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(AdaySlider)
class AdaySliderTranslationOptions(TranslationOptions):
    fields = ('title',)

