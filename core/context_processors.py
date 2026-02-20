# core/context_processors.py
from django.conf import settings
from django.utils import translation

def languages(request):
    # مستقیماً زبان فعال را از موتور ترجمه می‌گیریم
    code = translation.get_language()
    return {
        'LANGUAGE_CODE': code,
        'CURRENT_LANG': code,
        'CURRENT_LANGUAGE': code,
        'LANGUAGE_BIDI': translation.get_language_bidi(),
    }