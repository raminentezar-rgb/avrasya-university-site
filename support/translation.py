from modeltranslation.translator import TranslationOptions, register
from .models import KnowledgeBase, ImportantLink

@register(KnowledgeBase)
class KnowledgeBaseTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(ImportantLink)
class ImportantLinkTranslationOptions(TranslationOptions):
    fields = ('title',)

