# core/middleware.py
from django.utils import translation
from django.conf import settings

class ForceTurkishMiddleware:
    """
    Middleware برای تنظیم خودکار زبان ترکی
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # بررسی زبان فعلی
        lang_code = translation.get_language()
        
        # اگر زبان انگلیسی یا نامشخص است، ترکی را تنظیم کن
        if not lang_code or lang_code.startswith('en'):
            translation.activate('tr')
            request.LANGUAGE_CODE = 'tr'
        
        response = self.get_response(request)
        
        # تنظیم کوکی زبان
        if not request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME):
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME,
                'tr',
                max_age=365 * 24 * 60 * 60,
                httponly=True,
                path='/',
            )
        
        return response