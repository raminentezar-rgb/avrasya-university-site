from modeltranslation.translator import TranslationOptions, register
# به جای .translation از .translator استفاده کردیم
from .models import SliderItem, Page

@register(SliderItem)
class SliderTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content')