# core/middleware.py
from django.utils import translation
from django.conf import settings

class ForceTurkishMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        
        # 1. آدرس‌های سیستمی را نادیده بگیر
        if any(path.startswith(p) for p in [settings.STATIC_URL, settings.MEDIA_URL, '/admin/', '/i18n/', '/set-language/']):
            return self.get_response(request)

        # 2. از جنگو بپرس آیا این آدرس پیشوند زبان دارد (مثل /ru/ یا /fa/)
        language_from_url = translation.get_language_from_path(path)
        
        # 3. اگر آدرس پیشوند نداشت (مثل /news/ یا /)، زبان ترکی را اجبار کن
        if not language_from_url:
            translation.activate('tr')
            request.LANGUAGE_CODE = 'tr'
            # کوکی زبان را هم به ترکی تغییر می‌دهیم تا با محتوا هماهنگ شود
            # response.set_cookie در اینجا قابل دسترسی نیست، بعد از get_response انجام می‌دهیم
        
        response = self.get_response(request)
        
        # اگر زبان ترکی اجبار شده، کوکی را هم ست می‌کنیم
        if not language_from_url and request.LANGUAGE_CODE == 'tr':
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'tr', path='/')
            
        return response