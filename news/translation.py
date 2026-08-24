from modeltranslation.translator import TranslationOptions, register
from .models import News, NewsAttachment

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(NewsAttachment)
class NewsAttachmentTranslationOptions(TranslationOptions):
    fields = ('title',)

