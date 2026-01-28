# core/context_processors.py
from django.conf import settings
from django.utils import translation

def languages(request):
    return {
        'LANGUAGES': settings.LANGUAGES,
        'CURRENT_LANGUAGE': translation.get_language(),
    }