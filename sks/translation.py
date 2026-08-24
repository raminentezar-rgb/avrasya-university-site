from modeltranslation.translator import TranslationOptions, register
from .models import News, Announcement

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(Announcement)
class AnnouncementTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

