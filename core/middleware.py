# core/middleware.py
from django.conf import settings
from django.utils import translation

from .context_processors import is_noindex_path
from .services.visitors import record_visitor, should_track_request


class ForceTurkishMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Ignore static, media, crawler, and system/API endpoints
        if any(path.startswith(p) for p in [
            settings.STATIC_URL,
            settings.MEDIA_URL,
            '/admin/',
            '/avrasya-yonetim-paneli-2026/',
            '/i18n/',
            '/set-language/',
            '/ckeditor/',
            '/robots.txt',
            '/sitemap.xml',
            '/api/',
        ]):
            return self.get_response(request)

        # Check whether URL carries an explicit i18n language prefix
        language_from_url = translation.get_language_from_path(path)

        # Force Turkish on unprefixed URLs
        if not language_from_url:
            translation.activate('tr')
            request.LANGUAGE_CODE = 'tr'

        response = self.get_response(request)

        if not language_from_url and getattr(request, 'LANGUAGE_CODE', None) == 'tr':
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'tr', path='/')

        return response


class OnlineVisitorMiddleware:
    """Tracks real active visitors in a 5-minute sliding window with zero SQL overhead."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if should_track_request(request):
            try:
                record_visitor(request)
            except Exception:
                pass
        return self.get_response(request)


class NoIndexHeadersMiddleware:
    """Attaches X-Robots-Tag: noindex, nofollow on de-listed and internal endpoints."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if is_noindex_path(request.path_info):
            response.headers['X-Robots-Tag'] = 'noindex, nofollow'
        return response
