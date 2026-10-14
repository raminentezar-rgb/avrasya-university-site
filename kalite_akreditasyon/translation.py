from modeltranslation.translator import TranslationOptions, register
from .models import News, Announcement, Mevzuat, Takim, Rapor, Izleme, Dokuman, SSS

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'summary', 'content')

@register(Announcement)
class AnnouncementTranslationOptions(TranslationOptions):
    fields = ('title', 'summary', 'content')

@register(Mevzuat)
class MevzuatTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Takim)
class TakimTranslationOptions(TranslationOptions):
    fields = ('name', 'title', 'role', 'department')

@register(Rapor)
class RaporTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Izleme)
class IzlemeTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(Dokuman)
class DokumanTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(SSS)
class SSSTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')
