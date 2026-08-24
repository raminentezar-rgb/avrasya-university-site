from modeltranslation.translator import TranslationOptions, register
from .models import ResearchPolicy, BAPProject, IntellectualProperty, ResearchOutput, Award

@register(ResearchPolicy)
class ResearchPolicyTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

@register(BAPProject)
class BAPProjectTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(IntellectualProperty)
class IntellectualPropertyTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(ResearchOutput)
class ResearchOutputTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Award)
class AwardTranslationOptions(TranslationOptions):
    fields = ('title',)

